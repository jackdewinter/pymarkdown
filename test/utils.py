"""
Module to provide helper methods for tests.
"""
import difflib
import json
import logging
import os
import tempfile
from test.transform_to_markdown import TransformToMarkdown

from application_properties import ApplicationProperties

from pymarkdown.extension_manager.extension_manager import ExtensionManager
from pymarkdown.main_presentation import MainPresentation
from pymarkdown.parser_helper import ParserHelper
from pymarkdown.parser_logger import ParserLogger
from pymarkdown.tab_helper import TabHelper
from pymarkdown.tokenized_markdown import TokenizedMarkdown
from pymarkdown.transform_gfm.transform_to_gfm import TransformToGfm

# from test.verify_line_and_column_numbers import verify_line_and_column_numbers


# pylint: disable=too-many-arguments
def act_and_assert(
    source_markdown,
    expected_gfm,
    expected_tokens,
    show_debug=False,
    config_map=None,
    disable_consistency_checks=False,
    allow_alternate_markdown=False,
):
    """
    Act and assert on the expected behavior of parsing the source_markdown.
    """

    # Arrange
    logging.getLogger().setLevel(logging.DEBUG if show_debug else logging.WARNING)
    ParserLogger.sync_on_next_call()

    tokenizer = TokenizedMarkdown()
    test_properties = ApplicationProperties()
    if config_map:
        test_properties.load_from_dict(config_map)
    extension_manager = ExtensionManager(MainPresentation())
    extension_manager.initialize(None, test_properties)
    extension_manager.apply_configuration()
    tokenizer.apply_configuration(test_properties, extension_manager)
    transformer = TransformToGfm()

    # Act
    actual_tokens = tokenizer.transform(source_markdown, show_debug=show_debug)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    if (
        ParserHelper.tab_character in expected_gfm
        and ParserHelper.tab_character not in actual_gfm
    ):
        raise AssertionError()
    if not disable_consistency_checks:
        __assert_token_consistency(
            source_markdown, actual_tokens, allow_alternate_markdown
        )


# pylint: enable=too-many-arguments


def write_temporary_configuration(
    supplied_configuration, file_name=None, directory=None
):
    """
    Write the configuration as a temporary file that is kept around.
    """
    try:
        if file_name:
            full_file_name = (
                os.path.join(directory, file_name) if directory else file_name
            )
            with open(full_file_name, "wt", encoding="utf-8") as outfile:
                if isinstance(supplied_configuration, str):
                    outfile.write(supplied_configuration)
                else:
                    json.dump(supplied_configuration, outfile)
                return full_file_name
        else:
            with tempfile.NamedTemporaryFile(
                "wt", delete=False, dir=directory
            ) as outfile:
                if isinstance(supplied_configuration, str):
                    outfile.write(supplied_configuration)
                else:
                    json.dump(supplied_configuration, outfile)
                return outfile.name
    except IOError as this_exception:
        raise AssertionError(
            f"Test configuration file was not written ({this_exception})."
        ) from this_exception


def assert_if_lists_different(expected_tokens, actual_tokens):
    """
    Compare two lists and make sure they are equal, asserting if not.
    """

    print("\n---")
    print(f"expected_tokens: {ParserHelper.make_value_visible(expected_tokens)}")
    print(f"parsed_tokens  : {ParserHelper.make_value_visible(actual_tokens)}")
    assert len(expected_tokens) == len(
        actual_tokens
    ), f"List lengths are not the same: ({len(expected_tokens)}) vs ({len(actual_tokens)})"
    print("---")

    for element_index, next_expected_token in enumerate(expected_tokens):
        expected_str = str(next_expected_token)
        actual_str = str(actual_tokens[element_index])

        print(
            f"expected_tokens({len(expected_str)})>>{ParserHelper.make_value_visible(expected_str)}<<"
        )
        print(
            f"actual_tokens  ({len(actual_str)})>>{ParserHelper.make_value_visible(actual_str)}<<"
        )

        diff = difflib.ndiff(expected_str, actual_str)

        diff_values = f"{ParserHelper.newline_character.join(list(diff))}\n---\n"

        assert expected_str == str(
            actual_tokens[element_index]
        ), f"List items {element_index} are not equal.{diff_values}"
    print("---\nToken lists are equal.\n---")


def assert_if_strings_different(expected_string, actual_string):
    """
    Compare two strings and make sure they are equal, asserting if not.
    """

    print(f"expected_string({len(expected_string)})>>{expected_string}<<")
    print(f"expected_string>>{ParserHelper.make_value_visible(expected_string)}<<")

    print(f"actual_string  ({len(actual_string)})>>{actual_string}<<")
    print(f"actual_string  >>{ParserHelper.make_value_visible(actual_string)}<<")

    diff = difflib.ndiff(expected_string, actual_string)

    diff_values = f"{ParserHelper.newline_character.join(list(diff))}\n---\n"

    assert expected_string == actual_string, f"Strings are not equal.{diff_values}"


def __assert_token_consistency(
    source_markdown, actual_tokens, allow_alternate_markdown
):
    """
    Compare the markdown document against the tokens that are expected.
    """
    __verify_markdown_roundtrip(
        source_markdown, actual_tokens, allow_alternate_markdown
    )
    # verify_line_and_column_numbers(source_markdown, actual_tokens)


def __verify_markdown_roundtrip(
    source_markdown, actual_tokens, allow_alternate_markdown
):
    """
    Verify that we can use the information in the tokens to do a round trip back
    to the original Markdown that created the token.
    """

    if ParserHelper.tab_character in source_markdown and allow_alternate_markdown:
        new_source = []
        alternate_source = []
        split_source = source_markdown.split(ParserHelper.newline_character)
        for next_line in split_source:
            alternate_line = (
                TabHelper.detabify_string(next_line)
                if ParserHelper.tab_character in next_line
                else next_line
            )
            alternate_source.append(alternate_line)
            new_source.append(next_line)
        source_markdown = ParserHelper.newline_character.join(new_source)
        detabified_source_markdown = ParserHelper.newline_character.join(
            alternate_source
        )
    else:
        detabified_source_markdown = None

    transformer = TransformToMarkdown()
    markdown_from_tokens = transformer.transform(actual_tokens)

    print(
        "".join(
            [
                "\n-=-=-\nExpected\n-=-=-\n-->",
                ParserHelper.make_value_visible(source_markdown),
                "<--\n-=-=-\nActual\n-=-=-\n-->",
                ParserHelper.make_value_visible(markdown_from_tokens),
                "<--\n-=-=-\n",
            ]
        )
    )
    diff = difflib.ndiff(source_markdown, markdown_from_tokens)
    diff_values = "".join(
        [
            "\n-=-=-n",
            ParserHelper.newline_character.join(list(diff)),
            "\n-=-=-expected\n-->",
            ParserHelper.make_value_visible(source_markdown),
            "<--\n-=-=-actual\n-->",
            ParserHelper.make_value_visible(markdown_from_tokens),
            "<--\n-=-=-\n",
        ]
    )

    assert source_markdown == markdown_from_tokens or (
        (detabified_source_markdown is not None)
        and (detabified_source_markdown == markdown_from_tokens)
    ), f"Markdown strings are not equal.{diff_values}"
