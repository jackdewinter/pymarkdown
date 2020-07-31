"""
Module to provide helper methods for tests.
"""
import difflib
import json
import tempfile
from test.transform_to_markdown import TransformToMarkdown

from pymarkdown.inline_helper import InlineHelper
from pymarkdown.parser_helper import ParserHelper
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
    Compare two lists and make sure they are equal, asserting if not.
    """

    print("\n---")
    print(
        "expected_tokens: "
        + ParserHelper.make_value_visible(expected_tokens)
        .replace("\x02", "\\x02")
        .replace("\x03", "\\x03")
    )
    print(
        "parsed_tokens  : "
        + ParserHelper.make_value_visible(actual_tokens)
        .replace("\n", "\\n")
        .replace("\t", "\\t")
        .replace("\x02", "\\x02")
        .replace("\x03", "\\x03")
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
            + ParserHelper.make_value_visible(expected_str)
            .replace("\n", "\\n")
            .replace("\x02", "\\x02")
            .replace("\x03", "\\x03")
            + "<<"
        )
        print(
            "actual_tokens  ("
            + str(len(actual_str))
            + ")>>"
            + ParserHelper.make_value_visible(actual_str)
            .replace("\t", "\\t")
            .replace("\n", "\\n")
            .replace("\x02", "\\x02")
            .replace("\x03", "\\x03")
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
    Compare two strings and make sure they are equal, asserting if not.
    """

    print(
        "expected_string(" + str(len(expected_string)) + ")>>" + expected_string + "<<"
    )
    print(
        "expected_string>>"
        + ParserHelper.make_value_visible(expected_string)
        .replace("\t", "\\t")
        .replace("\n", "\\n")
        .replace("\x02", "\\x02")
        .replace("\x03", "\\x03")
        + "<<"
    )

    print("actual_string  (" + str(len(actual_string)) + ")>>" + actual_string + "<<")
    print(
        "actual_string>>"
        + ParserHelper.make_value_visible(actual_string)
        .replace("\t", "\\t")
        .replace("\n", "\\n")
        .replace("\x02", "\\x02")
        .replace("\x03", "\\x03")
        + "<<"
    )

    diff = difflib.ndiff(expected_string, actual_string)

    diff_values = "\n".join(list(diff)) + "\n---\n"

    assert expected_string == actual_string, "Strings are not equal." + diff_values


def __calc_initial_whitespace(calc_token):

    had_tab = False
    if calc_token.token_name in (
        MarkdownToken.token_indented_code_block,
        MarkdownToken.token_atx_heading,
        MarkdownToken.token_new_list_item,
        MarkdownToken.token_thematic_break,
        MarkdownToken.token_fenced_code_block,
        MarkdownToken.token_block_quote,
        MarkdownToken.token_link_reference_definition,
        MarkdownToken.token_setext_heading,
    ):
        indent_level = len(calc_token.extracted_whitespace)
        had_tab = bool("\t" in calc_token.extracted_whitespace)
    elif (
        calc_token.token_name == MarkdownToken.token_ordered_list_start
        or calc_token.token_name == MarkdownToken.token_unordered_list_start
    ):
        indent_level = len(calc_token.extracted_whitespace)
        had_tab = bool(
            "\t" in calc_token.extracted_whitespace
            or (calc_token.leading_spaces and "\t" in calc_token.leading_spaces)
        )
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


def __maintain_block_stack(container_block_stack, current_token):
    """
    Maintain a stack of the block elements, to allow better understanding of
    what container a given token is kept within.
    """

    if current_token.token_class == MarkdownTokenClass.CONTAINER_BLOCK:
        print("--")
        print(">>CON>>before>>" + str(container_block_stack))
        if (
            current_token.is_new_list_item
            and container_block_stack[-1].is_new_list_item
        ):
            del container_block_stack[-1]

        container_block_stack.append(current_token)
        print(">>CON>>after>>" + str(container_block_stack))

    # TODO Do this better.
    elif isinstance(current_token, EndMarkdownToken):

        token_name_without_prefix = current_token.token_name[
            len(EndMarkdownToken.type_name_prefix) :
        ]
        if token_name_without_prefix in (
            MarkdownToken.token_block_quote,
            MarkdownToken.token_unordered_list_start,
            MarkdownToken.token_ordered_list_start,
            MarkdownToken.token_new_list_item,
        ):
            print("--")
            print("<<CON<<before<<" + str(container_block_stack))

            if (
                container_block_stack[-1].token_name
                == MarkdownToken.token_new_list_item
            ):
                del container_block_stack[-1]

            assert container_block_stack[-1].token_name == token_name_without_prefix
            del container_block_stack[-1]
            print("<<CON<<after<<" + str(container_block_stack))


def __validate_same_line(
    container_block_stack, current_token, current_position, last_token, last_position
):

    print(">>__validate_same_line")
    if container_block_stack:
        top_block = container_block_stack[-1]
        _, had_tab = __calc_initial_whitespace(top_block)
        print(">>top_block>>w/ tab=" + str(had_tab))
        if had_tab:
            return

    _, had_tab = __calc_initial_whitespace(current_token)
    print(">>current_token>>w/ tab=" + str(had_tab))
    if had_tab:
        return

    assert last_token.token_class == MarkdownTokenClass.CONTAINER_BLOCK

    # TODO replace > with computation for block quote cases
    assert current_position.index_number > last_position.index_number
    if last_token.token_name != MarkdownToken.token_block_quote:
        assert last_token.token_name in (
            MarkdownToken.token_unordered_list_start,
            MarkdownToken.token_ordered_list_start,
            MarkdownToken.token_new_list_item,
        )
        print(">>current_token>>" + str(current_token))
        print(">>current_position.index_number>>" + str(current_position.index_number))
        print(">>last_token.indent_level>>" + str(last_token.indent_level))
        if current_token.token_name == MarkdownToken.token_blank_line:
            assert current_position.index_number == last_token.indent_level
        elif current_token.token_name == MarkdownToken.token_indented_code_block:
            assert (
                current_position.index_number - len(current_token.extracted_whitespace)
                == last_token.indent_level + 1
            )
        else:
            assert current_position.index_number == last_token.indent_level + 1


def __validate_new_line(container_block_stack, current_token, current_position):
    print(">>__validate_new_line")
    init_ws, had_tab = __calc_initial_whitespace(current_token)
    print(">>init_ws(" + str(init_ws) + ")>>w/ tab=" + str(had_tab))
    if had_tab:
        return

    # TODO validate line number based on content, need enablement of inline

    if (
        container_block_stack
        and current_token.token_name != MarkdownToken.token_blank_line
        and current_token.token_name != MarkdownToken.token_unordered_list_start
        and current_token.token_name != MarkdownToken.token_ordered_list_start
        and current_token.token_name != MarkdownToken.token_new_list_item
    ):
        top_block = container_block_stack[-1]
        _, had_tab = __calc_initial_whitespace(top_block)
        print(">>top_block>>w/ tab=" + str(had_tab))
        if had_tab:
            return

        if (
            top_block.token_name == MarkdownToken.token_unordered_list_start
            or top_block.token_name == MarkdownToken.token_ordered_list_start
            or top_block.token_name == MarkdownToken.token_new_list_item
        ):
            init_ws += top_block.indent_level
    elif (
        container_block_stack
        and current_token.token_name == MarkdownToken.token_new_list_item
    ):
        assert container_block_stack[-1] == current_token
        if len(container_block_stack) > 1:
            top_block = container_block_stack[-2]
            init_ws = (
                top_block.column_number
                - 1
                + (current_token.indent_level - top_block.indent_level)
            )

    print(">>current_position.index_number>>" + str(current_position.index_number))
    print(">>current_position.index_indent>>" + str(current_position.index_indent))
    print(">>1 + init_ws(" + str(init_ws) + ")>>" + str(1 + init_ws))
    if not had_tab:
        assert current_position.index_number == 1 + init_ws, (
            "Line:" + str(current_position.line_number) + ":" + str(current_token)
        )


def __validate_first_token(current_token, current_position):
    print(">>__validate_first_line")
    assert current_position.line_number == 1

    init_ws, had_tab = __calc_initial_whitespace(current_token)
    if not had_tab:
        assert current_position.index_number == 1 + init_ws


def assert_token_consistency(source_markdown, actual_tokens):
    """
    Compare the markdown document against the tokens that are expected.
    """

    verify_markdown_roundtrip(source_markdown, actual_tokens)

    split_lines = source_markdown.split("\n")
    number_of_lines = len(split_lines)
    print(">>" + str(number_of_lines))

    last_token = None
    container_block_stack = []
    for current_token in actual_tokens:
        if (
            current_token.token_class == MarkdownTokenClass.INLINE_BLOCK
            and not isinstance(current_token, EndMarkdownToken)
        ):
            continue

        current_position = __calc_adjusted_position(current_token)

        __maintain_block_stack(container_block_stack, current_token)

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
            # Until block quotes are handled, if we see one in the stack, don't validate
            # any more.
            found_block_quote = False
            for i in container_block_stack:
                if i.token_name == MarkdownToken.token_block_quote:
                    found_block_quote = True
            if found_block_quote:
                last_token = current_token
                continue

            if last_position.line_number == current_position.line_number:
                __validate_same_line(
                    container_block_stack,
                    current_token,
                    current_position,
                    last_token,
                    last_position,
                )
            else:
                __validate_new_line(
                    container_block_stack, current_token, current_position
                )
        else:
            __validate_first_token(current_token, current_position)

        last_token = current_token


def verify_markdown_roundtrip(source_markdown, actual_tokens):
    """
    Verify that we can use the information in the tokens to do a round trip back
    to the original Markdown that created the token.
    """

    if "\t" in source_markdown:
        return

    transformer = TransformToMarkdown()
    original_markdown, avoid_processing = transformer.transform(actual_tokens)

    if avoid_processing:
        print("Processing of xx avoided")
    else:
        print(
            "\n-=-=-\nExpected\n-=-=-\n"
            + ParserHelper.make_value_visible(source_markdown)
            .replace("\x02", "\\x02")
            .replace("\x03", "\\x03")
            .replace("\n", "\\n")
            .replace("\t", "\\t")
            + "\n-=-=-\nActual\n-=-=-\n"
            + ParserHelper.make_value_visible(original_markdown)
            .replace("\x02", "\\x02")
            .replace("\x03", "\\x03")
            .replace("\n", "\\n")
            .replace("\t", "\\t")
            + "\n-=-=-\n"
        )
        diff = difflib.ndiff(source_markdown, original_markdown)
        diff_values = (
            "\n-=-=-n"
            + "\n".join(list(diff))
            + "\n-=-=-expected\n"
            + source_markdown.replace("\n", "\\n")
            + "\n-=-=-actual\n"
            + original_markdown.replace("\n", "\\n")
            + "\n-=-=-\n"
        )
        assert source_markdown == original_markdown, (
            "Strings are not equal." + diff_values
        )
