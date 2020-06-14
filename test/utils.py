"""
Module to provide helper methods for tests.
"""
import difflib
import json
import tempfile

from pymarkdown.markdown_token import (
    EndMarkdownToken,
    MarkdownToken,
    MarkdownTokenClass,
)
from pymarkdown.parser_helper import PositionMarker


def write_temporary_configuration(supplied_configuration):
    """
    Write the configuration as a temporary file that is kept around.
    """
    try:
        with tempfile.TemporaryFile("wt", delete=False) as outfile:
            if isinstance(supplied_configuration, str):
                outfile.write(supplied_configuration)
            else:
                json.dump(supplied_configuration, outfile)
            return outfile.name
    except IOError as ex:
        assert False, "Test configuration file was not written (" + str(ex) + ")."


def assert_if_lists_different(expected_tokens, actual_tokens):
    """
    Compart two lists and make sure they are equal, asserting if not.
    """

    print("\n---")
    print("expected_tokens: " + str(expected_tokens))
    print(
        "parsed_tokens  : "
        + str(actual_tokens).replace("\n", "\\n").replace("\t", "\\t")
    )
    assert len(expected_tokens) == len(actual_tokens), (
        "List lengths are not the same: ("
        + str(len(expected_tokens))
        + ") vs "
        + "("
        + str(len(actual_tokens))
        + ")"
    )
    print("---")

    # pylint: disable=consider-using-enumerate
    for element_index in range(0, len(expected_tokens)):

        expected_str = str(expected_tokens[element_index])
        actual_str = str(actual_tokens[element_index])

        print(
            "expected_tokens("
            + str(len(expected_str))
            + ")>>"
            + expected_str.replace("\t", "\\t")
            + "<<"
        )
        print(
            "actual_tokens  ("
            + str(len(actual_str))
            + ")>>"
            + actual_str.replace("\t", "\\t")
            + "<<"
        )

        diff = difflib.ndiff(expected_str, actual_str)

        diff_values = "\n".join(list(diff)) + "\n---\n"

        assert expected_str == str(actual_tokens[element_index]), (
            "List items " + str(element_index) + " are not equal." + diff_values
        )
    print("---\nToken lists are equal.\n---")
    # pylint: enable=consider-using-enumerate


def assert_if_strings_different(expected_string, actual_string):
    """
    Compart two strings and make sure they are equal, asserting if not.
    """

    print(
        "expected_string(" + str(len(expected_string)) + ")>>" + expected_string + "<<"
    )
    print("actual_string  (" + str(len(actual_string)) + ")>>" + actual_string + "<<")

    diff = difflib.ndiff(expected_string, actual_string)

    diff_values = "\n".join(list(diff)) + "\n---\n"

    assert expected_string == actual_string, "Strings are not equal." + diff_values


def __calc_initial_whitespace(calc_token):

    had_tab = False
    if calc_token.token_name in (
        MarkdownToken.token_indented_code_block,
        MarkdownToken.token_atx_heading,
        MarkdownToken.token_ordered_list_start,
        MarkdownToken.token_unordered_list_start,
        MarkdownToken.token_new_list_item,
        MarkdownToken.token_thematic_break,
        MarkdownToken.token_fenced_code_block,
        MarkdownToken.token_block_quote,
        MarkdownToken.token_link_reference_definition,
    ):
        indent_level = len(calc_token.extracted_whitespace)
        had_tab = bool("\t" in calc_token.extracted_whitespace)
    elif calc_token.token_name == MarkdownToken.token_setext_heading:
        indent_level = len(calc_token.remaining_line)
        had_tab = bool("\t" in calc_token.remaining_line)
    elif (
        calc_token.token_name == MarkdownToken.token_html_block
        or calc_token.token_name == MarkdownToken.token_blank_line
    ):
        indent_level = 0
    elif calc_token.token_name == MarkdownToken.token_paragraph:

        if "\n" in calc_token.extracted_whitespace:
            end_of_line_index = calc_token.extracted_whitespace.index("\n")
            first_para_ws = calc_token.extracted_whitespace[0:end_of_line_index]
        else:
            first_para_ws = calc_token.extracted_whitespace
        print(">>first_para_ws>>" + first_para_ws.replace("\t", "\\t") + ">>")
        indent_level = len(first_para_ws)
        had_tab = bool("\t" in first_para_ws)
        print(">>indent_level>>" + str(indent_level) + ">>had_tab>>" + str(had_tab))
    else:
        assert False, "Token " + calc_token.token_name + " not handled."
    return indent_level, had_tab


def __calc_adjusted_position(markdown_token):
    if markdown_token.token_name == MarkdownToken.token_setext_heading:
        line_number = markdown_token.original_line_number
        index_number = markdown_token.original_column_number
    else:
        line_number = markdown_token.line_number
        index_number = markdown_token.column_number
    return PositionMarker(line_number, index_number, "")


# pylint: disable=too-many-branches, too-many-statements
def assert_token_consistency(source_markdown, expected_tokens):  # noqa: C901
    """
    Compare the markdown document against the tokens that are expected.
    """

    split_lines = source_markdown.split("\n")
    number_of_lines = len(split_lines)
    print(">>" + str(number_of_lines))

    last_token = None
    container_block_stack = []
    for current_token in expected_tokens:
        if (
            current_token.token_class == MarkdownTokenClass.INLINE_BLOCK
            and not isinstance(current_token, EndMarkdownToken)
        ):
            continue

        current_position = __calc_adjusted_position(current_token)

        print("--")
        if current_token.token_class == MarkdownTokenClass.CONTAINER_BLOCK:
            if current_token.token_name == MarkdownToken.token_new_list_item:

                if (
                    container_block_stack[-1].token_name
                    == MarkdownToken.token_new_list_item
                ):
                    del container_block_stack[-1]

            print(">>CON>>before>>" + str(container_block_stack))
            container_block_stack.append(current_token)
            print(">>CON>>after>>" + str(container_block_stack))
        # TODO Do this better.
        elif isinstance(current_token, EndMarkdownToken):

            token_name_without_prefix = current_token.token_name[
                len(EndMarkdownToken.type_name_prefix) :
            ]
            print("<<CON??" + token_name_without_prefix)
            if token_name_without_prefix in (
                MarkdownToken.token_block_quote,
                MarkdownToken.token_unordered_list_start,
                MarkdownToken.token_ordered_list_start,
                MarkdownToken.token_new_list_item,
            ):
                print("<<CON<<before<<" + str(container_block_stack))

                if (
                    container_block_stack[-1].token_name
                    == MarkdownToken.token_new_list_item
                ):
                    del container_block_stack[-1]

                assert container_block_stack[-1].token_name == token_name_without_prefix
                del container_block_stack[-1]
                print("<<CON<<after<<" + str(container_block_stack))

        if isinstance(current_token, EndMarkdownToken):
            continue

        print("--")
        print(
            "this>>"
            + str(current_token.token_name)
            + ">>"
            + str(current_token.token_class)
            + ">>("
            + str(current_position.line_number)
            + ","
            + str(current_position.index_number)
            + ")"
        )
        if last_token:
            last_position = __calc_adjusted_position(last_token)
            print(
                "last>>"
                + str(last_token.token_name)
                + ">>"
                + str(last_token.token_class)
                + ">>("
                + str(last_position.line_number)
                + ","
                + str(last_position.index_number)
                + ")"
            )

            # TODO later - block quotes ln 307-308 removes, but does not store anywhere
            found_block_quote = False
            for i in container_block_stack:
                if i.token_name == MarkdownToken.token_block_quote:
                    found_block_quote = True
            if found_block_quote:
                last_token = current_token
                continue

            if last_position.line_number == current_position.line_number:
                assert last_token.token_class == MarkdownTokenClass.CONTAINER_BLOCK
                assert current_position.index_number > last_position.index_number
            elif current_token.token_name == MarkdownToken.token_new_list_item:
                # TODO later
                pass
            else:
                init_ws, had_tab = __calc_initial_whitespace(current_token)

                if (
                    container_block_stack
                    and current_token.token_name != MarkdownToken.token_blank_line
                    and current_token.token_name
                    != MarkdownToken.token_unordered_list_start
                    and current_token.token_name
                    != MarkdownToken.token_ordered_list_start
                ):
                    print("stack>>" + str(container_block_stack[-1]))
                    top_block = container_block_stack[-1]

                    if (
                        top_block.token_name == MarkdownToken.token_unordered_list_start
                        or top_block.token_name
                        == MarkdownToken.token_ordered_list_start
                        or top_block.token_name == MarkdownToken.token_new_list_item
                    ):
                        print("indent>>" + str(top_block.indent_level))
                        init_ws += top_block.indent_level

                print(
                    ">>current_position.index_number>>"
                    + str(current_position.index_number)
                )
                print(
                    ">>current_position.index_indent>>"
                    + str(current_position.index_indent)
                )
                print(">>1 + init_ws>>" + str(1 + init_ws))
                if not had_tab:
                    assert current_position.index_number == 1 + init_ws, (
                        "Line:"
                        + str(current_position.line_number)
                        + ":"
                        + str(current_token)
                    )
        else:
            assert current_position.line_number == 1

            init_ws, had_tab = __calc_initial_whitespace(current_token)
            if not had_tab:
                assert current_position.index_number == 1 + init_ws

        last_token = current_token


# pylint: enable=too-many-branches, too-many-statements
