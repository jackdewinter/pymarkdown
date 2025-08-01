"""
Module to provide helper methods for tests.
"""

import difflib
import io
import json
import logging
import os
import shutil
import sys
import tempfile
from contextlib import contextmanager
from typing import IO, TYPE_CHECKING, Any, Dict, Generator, List, Optional, Union, cast

from application_properties import ApplicationProperties

from pymarkdown.extension_manager.extension_manager import ExtensionManager
from pymarkdown.general.main_presentation import MainPresentation
from pymarkdown.general.parser_helper import ParserHelper
from pymarkdown.general.parser_logger import ParserLogger
from pymarkdown.general.tab_helper import TabHelper
from pymarkdown.general.tokenized_markdown import TokenizedMarkdown
from pymarkdown.tokens.markdown_token import MarkdownToken
from pymarkdown.transform_gfm.transform_to_gfm import TransformToGfm
from pymarkdown.transform_markdown.transform_to_markdown import TransformToMarkdown

# from test.verify_line_and_column_numbers import verify_line_and_column_numbers


# pylint: disable=too-many-arguments, too-many-locals
def act_and_assert(
    source_markdown: str,
    expected_gfm: str,
    expected_tokens: List[str],
    show_debug: bool = False,
    config_map: Optional[Dict[str, Any]] = None,
    disable_consistency_checks: bool = False,
    allow_alternate_markdown: bool = False,
    do_add_end_of_stream_token: bool = False,
) -> None:
    """
    Act and assert on the expected behavior of parsing the source_markdown.
    """

    keep_directory = os.getenv("PTEST_KEEP_DIRECTORY", None)
    if keep_directory and os.path.isdir(keep_directory):
        with tempfile.NamedTemporaryFile(
            "wt", encoding="utf-8", dir=keep_directory, suffix=".md", delete=False
        ) as temp_file:
            temp_file.write(source_markdown)

    # Arrange
    logging.getLogger().setLevel(logging.DEBUG if show_debug else logging.WARNING)
    ParserLogger.sync_on_next_call()

    tokenizer = TokenizedMarkdown()
    test_properties = ApplicationProperties()
    if config_map:
        test_properties.load_from_dict(config_map)
        if test_properties.get_boolean_property("mode.strict-config", strict_mode=True):
            test_properties.enable_strict_mode()

    extension_manager = ExtensionManager(MainPresentation())
    extension_manager.initialize(test_properties)
    extension_manager.apply_configuration("")
    tokenizer.apply_configuration(test_properties, extension_manager)
    transformer = TransformToGfm()

    # Act
    actual_tokens = tokenizer.transform(
        source_markdown,
        show_debug=show_debug,
        do_add_end_of_stream_token=do_add_end_of_stream_token,
    )
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


# pylint: enable=too-many-arguments, too-many-locals


def read_contents_of_text_file(source_path: str) -> str:
    """
    Read the entire contents of the specified file into the variable.
    """
    with open(source_path, "rt", encoding="utf-8") as source_file:
        return source_file.read()


def assert_file_is_as_expected(source_path: str, expected_file_contents: str) -> None:
    """
    Assert that the file contents match the expected contents.
    """
    actual_file_contents = read_contents_of_text_file(source_path)

    if expected_file_contents != actual_file_contents:
        print(
            "Expected:"
            + expected_file_contents.replace("\n", "\\n").replace("\t", "\\t")
            + ":"
        )
        print(
            "  Actual:"
            + actual_file_contents.replace("\n", "\\n").replace("\t", "\\t")
            + ":"
        )
        expected_file_lines = expected_file_contents.splitlines(keepends=True)
        # print("Expected:" + str(ex) + ":")
        actual_file_lines = actual_file_contents.splitlines(keepends=True)
        # print("  Actual:" + str(ac) + ":")
        diff = difflib.ndiff(expected_file_lines, actual_file_lines)
        diff_values = "-\n-".join(list(diff))
        print("-" + diff_values + "-")
        raise AssertionError()


def assert_if_lists_different(
    expected_tokens: List[Any], actual_tokens: List[Any]
) -> None:
    """
    Compare two lists and make sure they are equal, asserting if not.
    """

    print("\n---")
    print(f"expected_tokens: {ParserHelper.make_value_visible(expected_tokens)}")
    print(f"parsed_tokens  : {ParserHelper.make_value_visible(actual_tokens)}")
    assert len(expected_tokens) == len(
        actual_tokens
    ), f"List lengths are not the same: ({len(expected_tokens)}:{expected_tokens}) vs ({len(actual_tokens)}:{actual_tokens})"
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
    print("---\nLists are equal.\n---")


def assert_if_strings_different(expected_string: str, actual_string: str) -> None:
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
    source_markdown: str,
    actual_tokens: List[MarkdownToken],
    allow_alternate_markdown: bool,
) -> None:
    """
    Compare the markdown document against the tokens that are expected.
    """
    __verify_markdown_roundtrip(
        source_markdown, actual_tokens, allow_alternate_markdown
    )
    # verify_line_and_column_numbers(source_markdown, actual_tokens)


def __verify_markdown_roundtrip(
    source_markdown: str,
    actual_tokens: List[MarkdownToken],
    allow_alternate_markdown: bool,
) -> None:
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


def copy_to_temporary_file(source_path: str) -> str:
    """
    Copy an existing markdown file to a temporary markdown file,
    to allow fo fixing the file without destroying the original.
    """
    with tempfile.NamedTemporaryFile("wt", delete=False, suffix=".md") as outfile:
        temporary_file = outfile.name

        shutil.copyfile(source_path, temporary_file)
        return os.path.abspath(temporary_file)


@contextmanager
def copy_to_temp_file(file_to_copy: str) -> Generator[str, None, None]:
    """
    Context manager to copy a file to a temporary file, returning the name of the temporary file.
    """
    temp_source_path = None
    try:
        temp_source_path = copy_to_temporary_file(file_to_copy)
        yield temp_source_path
    finally:
        if temp_source_path:
            os.remove(temp_source_path)


def write_temporary_configuration(
    supplied_configuration: Union[str, Dict[str, Any], None],
    file_name: Optional[str] = None,
    directory: Optional[str] = None,
    file_name_prefix: Optional[str] = None,
    file_name_suffix: Optional[str] = None,
) -> str:
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
                "wt",
                delete=False,
                dir=directory,
                suffix=file_name_suffix,
                prefix=file_name_prefix,
                encoding="utf-8",
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


@contextmanager
def create_temporary_configuration_file(
    supplied_configuration: Union[str, Dict[str, Any]],
    file_name: Optional[str] = None,
    directory: Optional[str] = None,
    file_name_suffix: Optional[str] = None,
    file_name_prefix: Optional[str] = None,
) -> Generator[str, None, None]:
    """
    Context manager to create a temporary configuration file.
    """
    temp_source_path = None
    try:
        temp_source_path = write_temporary_configuration(
            supplied_configuration,
            file_name=file_name,
            directory=directory,
            file_name_suffix=file_name_suffix,
            file_name_prefix=file_name_prefix,
        )
        yield temp_source_path
    finally:
        if temp_source_path and os.path.exists(temp_source_path):
            os.remove(temp_source_path)


@contextmanager
def temporary_change_to_directory(
    path_to_change_to: str,
) -> Generator[None, None, None]:
    """
    Context manager to temporarily change to a given directory.
    """
    old_current_working_directory = os.getcwd()
    try:
        os.chdir(path_to_change_to)
        yield
    finally:
        os.chdir(old_current_working_directory)


@contextmanager
def capture_stdout() -> Generator[io.StringIO, None, None]:
    """
    Context manager to capture stdout into a StringIO buffer.
    """
    std_output = io.StringIO()
    old_output = sys.stdout
    try:
        sys.stdout = std_output
        yield std_output
    finally:
        sys.stdout = old_output


@contextmanager
def create_temporary_file_for_reuse() -> Generator[str, None, None]:
    """
    Create a temporary file and return its path name for reuse.
    """
    log_pathxx = None
    try:
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            log_pathxx = temp_file.name

        yield log_pathxx
    finally:
        if log_pathxx and os.path.exists(log_pathxx):
            os.remove(log_pathxx)


if TYPE_CHECKING:
    LOGHANDLER = logging.StreamHandler[IO[str]]
else:
    LOGHANDLER = logging.StreamHandler


@contextmanager
def capture_logging_changes_with_new_handler() -> (
    Generator[tuple[LOGHANDLER, io.StringIO], None, None]
):
    """
    Capture any simple logging changes to allow for logging to be more thoroughly tested.
    """
    old_log_level = logging.getLogger().level
    log_output = io.StringIO()
    new_handler = logging.StreamHandler(log_output)
    try:
        yield (new_handler, log_output)  # type: ignore
    finally:
        logging.getLogger().setLevel(old_log_level)
        new_handler.close()


def compare_expected_to_actual(
    expected_text: str, actual_text: str, xx_title: str = "Text"
) -> None:
    """
    Compare the expected text to the actual text.
    """
    if actual_text.strip() != expected_text.strip():
        diff = difflib.ndiff(expected_text.splitlines(), actual_text.splitlines())
        diff_values = "\n".join(list(diff))
        raise AssertionError(f"{xx_title} not as expected:\n{diff_values}")


# pylint: disable=broad-exception-caught
def assert_that_exception_is_raised(
    type_of_exception: type,
    exception_output: str,
    function_to_test: Any,
    *args: Any,
    **kwargs: Any,
) -> Exception:
    """
    Assert that the specified type of exception is thrown when the specified
    function is called with the supplied parameters.  This version of the function
    checks to see if the exception text equals the text supplied by the
    `exception_output` parameter.
    """
    try:
        function_to_test(*args, **kwargs)
        raise AssertionError(
            "Function execution did not raise any expected exceptions."
        )
    except Exception as this_exception:
        assert isinstance(
            this_exception, type_of_exception
        ), f"Function execution did not raise the expected {type_of_exception}."

        text_to_compare = (
            cast(str, this_exception.reason)
            if hasattr(this_exception, "reason")
            else str(this_exception)
        )
        compare_expected_to_actual(exception_output, text_to_compare)
        return this_exception


# pylint: enable=broad-exception-caught


# pylint: disable=broad-exception-caught
def assert_that_exception_is_raised2(
    type_of_exception: type,
    exception_output: str,
    function_to_test: Any,
    *args: Any,
    **kwargs: Any,
) -> Exception:
    """
    Assert that the specified type of exception is thrown when the specified
    function is called with the supplied parameters.  This version of the function
    checks to see if the exception text starts with the text supplied by the
    `exception_output` parameter.
    """
    try:
        function_to_test(*args, **kwargs)
        raise AssertionError(
            "Function execution did not raise any expected exceptions."
        )
    except Exception as this_exception:
        assert isinstance(
            this_exception, type_of_exception
        ), f"Function execution did not raise the expected {type_of_exception}."

        text_to_compare = (
            cast(str, this_exception.reason)
            if hasattr(this_exception, "reason")
            else str(this_exception)
        )
        assert text_to_compare.startswith(
            exception_output
        ), f"Text: '{text_to_compare}' does not begin with '{exception_output}'."
        return this_exception


# pylint: enable=broad-exception-caught
