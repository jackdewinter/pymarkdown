"""
Module to provide for verification of the line numbers and column numbers in tokens.
"""
from pymarkdown.markdown_token import (
    EndMarkdownToken,
    MarkdownToken,
    MarkdownTokenClass,
)
from pymarkdown.parser_helper import ParserHelper, PositionMarker


# pylint: disable=too-many-branches,too-many-statements
def verify_line_and_column_numbers(source_markdown, actual_tokens):
    """
    Verify that the line numbers and column numbers in tokens are as expected,
    based on the data in the tokens.
    """
    print("---\nLine/Column Numbers\n---")

    split_lines = source_markdown.split(ParserHelper.newline_character)
    number_of_lines = len(split_lines)
    print("Total lines in source document: " + str(number_of_lines))

    last_token = None
    last_token_index = None
    container_block_stack = []
    token_stack = []

    for ind, current_token in enumerate(actual_tokens):

        remember_token_as_last_token = True

        print("\n\n-->" + ParserHelper.make_value_visible(current_token))
        if (
            current_token.token_class == MarkdownTokenClass.INLINE_BLOCK
            and not isinstance(current_token, EndMarkdownToken)
        ):
            print("Inline, skipping")
            if (
                container_block_stack
                and container_block_stack[-1].token_name
                == MarkdownToken.token_block_quote
                and current_token.token_name == MarkdownToken.token_text
            ):
                print("xxx:" + ParserHelper.make_value_visible(actual_tokens[ind - 1]))
                if actual_tokens[ind - 1].token_name == MarkdownToken.token_html_block:
                    container_block_stack[-1].leading_text_index += 1
                    print(
                        ">>implicit newline>>index>"
                        + str(container_block_stack[-1].leading_text_index)
                    )
            continue

        current_position = __calc_adjusted_position(current_token)

        __maintain_block_stack(container_block_stack, current_token)

        if isinstance(current_token, EndMarkdownToken):
            print("end token, skipping")
            __pop_from_stack_if_required(token_stack, current_token)
            if (
                container_block_stack
                and container_block_stack[-1].token_name
                == MarkdownToken.token_block_quote
            ):
                print("block quotes: looking for implicit newlines")
                if (
                    current_token.token_name
                    == EndMarkdownToken.type_name_prefix
                    + MarkdownToken.token_atx_heading
                    or current_token.token_name
                    == EndMarkdownToken.type_name_prefix + MarkdownToken.token_paragraph
                    or current_token.token_name
                    == EndMarkdownToken.type_name_prefix
                    + MarkdownToken.token_html_block
                ):
                    container_block_stack[-1].leading_text_index += 1
                    print(
                        ">>implicit newline>>index>"
                        + str(container_block_stack[-1].leading_text_index)
                    )
            continue

        if current_token.token_name == MarkdownToken.token_block_quote:
            print("block token index reset")
            print(
                ">>start bq>>index>" + str(container_block_stack[-1].leading_text_index)
            )
            current_token.leading_text_index = 0

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

            top_block_token = None
            for next_container_block in container_block_stack:
                if next_container_block.token_name == MarkdownToken.token_block_quote:
                    top_block_token = next_container_block
                elif (
                    next_container_block.token_name
                    == MarkdownToken.token_unordered_list_start
                    or next_container_block.token_name
                    == MarkdownToken.token_ordered_list_start
                ):
                    break
            print(
                "top_block_token>>" + ParserHelper.make_value_visible(top_block_token)
            )

            if last_position.line_number == current_position.line_number:
                __validate_same_line(
                    container_block_stack,
                    current_token,
                    current_position,
                    last_token,
                    last_position,
                )
                remember_token_as_last_token = __push_to_stack_if_required(
                    token_stack, current_token
                )
            else:
                __validate_new_line(
                    container_block_stack, current_token, current_position
                )
                remember_token_as_last_token = __verify_token_height(
                    current_token,
                    last_token,
                    last_token_index,
                    actual_tokens,
                    token_stack,
                )

            print(
                "top_block_token<<" + ParserHelper.make_value_visible(top_block_token)
            )
            if top_block_token:
                print(
                    "current_token<<" + ParserHelper.make_value_visible(current_token)
                )
                if top_block_token != current_token and (
                    current_token.token_name == MarkdownToken.token_blank_line
                ):
                    print(
                        ">>saw bl>>index>"
                        + str(container_block_stack[-1].leading_text_index)
                    )
                    top_block_token.leading_text_index += 1
        else:
            __validate_first_token(current_token, current_position)
            remember_token_as_last_token = __push_to_stack_if_required(
                token_stack, current_token
            )

        if remember_token_as_last_token:
            print("saving last")
            last_token = current_token
            last_token_index = ind
        else:
            print("skipping last")

    print("Total lines in source document: " + str(number_of_lines))
    __validate_block_token_height(
        last_token, None, number_of_lines, True, None, actual_tokens, token_stack
    )

    assert not token_stack
    assert not container_block_stack
    # pylint: enable=too-many-branches,too-many-statements


def __push_to_stack_if_required(token_stack, current_token):
    print(
        "__push_to_stack_if_required->before->"
        + ParserHelper.make_value_visible(token_stack)
    )
    remember_token_as_last_token = True

    # TODO replace with attribute from token?
    if (
        current_token.token_name != MarkdownToken.token_blank_line
        and current_token.token_name != MarkdownToken.token_new_list_item
        and current_token.token_name != MarkdownToken.token_link_reference_definition
        and current_token.token_name != MarkdownToken.token_thematic_break
    ):
        token_stack.append(current_token)
    else:
        if token_stack and (
            token_stack[-1].token_name == MarkdownToken.token_html_block
            or token_stack[-1].token_name == MarkdownToken.token_fenced_code_block
        ):
            remember_token_as_last_token = False
    print(
        "__push_to_stack_if_required->after->"
        + str(remember_token_as_last_token)
        + ":"
        + ParserHelper.make_value_visible(token_stack)
    )
    return remember_token_as_last_token


def __pop_from_stack_if_required(token_stack, current_token):
    print(
        "__pop_from_stack_if_required->current_token->"
        + ParserHelper.make_value_visible(current_token)
    )
    print(
        "__pop_from_stack_if_required->before->"
        + ParserHelper.make_value_visible(token_stack)
    )
    assert token_stack
    if (
        EndMarkdownToken.type_name_prefix + token_stack[-1].token_name
        == current_token.token_name
    ):
        del token_stack[-1]
    print(
        "__pop_from_stack_if_required->after->"
        + ParserHelper.make_value_visible(token_stack)
    )


def __count_newlines_in_text(text_to_examine):
    """
    Count the number of new line characters in a given string.
    """
    original_length = len(text_to_examine)
    removed_length = len(text_to_examine.replace("\n", ""))
    return original_length - removed_length


# pylint: disable=too-many-arguments,too-many-branches
def __validate_block_token_height(
    last_token,
    current_token,
    last_line_number,
    was_last,
    last_token_index,
    actual_tokens,
    token_stack,
):
    print("last_token:" + ParserHelper.make_value_visible(last_token))
    print("last_token_index:" + ParserHelper.make_value_visible(last_token_index))
    print("last_line_number:" + ParserHelper.make_value_visible(last_line_number))
    print("was_last:" + ParserHelper.make_value_visible(was_last))
    if was_last:
        return

    skip_check = False
    if current_token and current_token.token_name == MarkdownToken.token_blank_line:
        print("blank:" + ParserHelper.make_value_visible(token_stack))
        if token_stack and (
            token_stack[-1].token_name == MarkdownToken.token_html_block
            or token_stack[-1].token_name == MarkdownToken.token_fenced_code_block
        ):
            skip_check = True

    if last_token.token_name == MarkdownToken.token_paragraph:
        token_height = 1 + __count_newlines_in_text(last_token.extracted_whitespace)
    elif last_token.token_name == MarkdownToken.token_indented_code_block:
        token_height = 1 + __count_newlines_in_text(last_token.indented_whitespace)
    elif (
        last_token.token_name == MarkdownToken.token_html_block
        or last_token.token_name == MarkdownToken.token_fenced_code_block
    ):
        current_token_index = last_token_index + 1
        end_name = EndMarkdownToken.type_name_prefix + last_token.token_name
        token_height = 0
        if last_token.token_name == MarkdownToken.token_fenced_code_block:
            token_height += 1
        while actual_tokens[current_token_index].token_name != end_name:
            if (
                actual_tokens[current_token_index].token_name
                == MarkdownToken.token_text
            ):
                token_height += 1 + __count_newlines_in_text(
                    actual_tokens[current_token_index].token_text
                )
            else:
                assert (
                    actual_tokens[current_token_index].token_name
                    == MarkdownToken.token_blank_line
                )
                token_height += 1
            current_token_index += 1
        if last_token.token_name == MarkdownToken.token_fenced_code_block:
            if not actual_tokens[current_token_index].was_forced:
                token_height += 1
    elif last_token.token_name == MarkdownToken.token_blank_line:
        token_height = 1
    elif last_token.token_name == MarkdownToken.token_link_reference_definition:
        token_height = (
            1
            + __count_newlines_in_text(last_token.extracted_whitespace)
            + __count_newlines_in_text(last_token.link_name_debug)
            + __count_newlines_in_text(last_token.link_destination_whitespace)
            + __count_newlines_in_text(last_token.link_title_raw)
            + __count_newlines_in_text(last_token.link_title_whitespace)
        )
    elif (
        last_token.token_name == MarkdownToken.token_thematic_break
        or last_token.token_name == MarkdownToken.token_atx_heading
    ):
        token_height = 1
    elif last_token.token_name == MarkdownToken.token_setext_heading:
        token_height = last_token.line_number - last_token.original_line_number
    else:
        assert False, "Token " + last_token.token_name + " not supported."

    if not skip_check:
        delta = last_token.line_number
        print(
            "delta:"
            + ParserHelper.make_value_visible(delta)
            + "; height:"
            + str(token_height)
        )
        delta += token_height
        print("calc current_line_number:" + ParserHelper.make_value_visible(delta))
        assert delta == last_line_number, (
            "Calculated line number '"
            + str(delta)
            + "' does not equal the actual line number '"
            + str(last_line_number)
            + "'."
        )


# pylint: enable=too-many-arguments,too-many-branches


def __verify_token_height(
    current_token, last_token, last_token_index, actual_tokens, token_stack
):
    remember_token_as_last_token = __push_to_stack_if_required(
        token_stack, current_token
    )
    assert last_token
    print("current_token:" + ParserHelper.make_value_visible(current_token))

    token_line_number = current_token.line_number
    if current_token.token_name == MarkdownToken.token_setext_heading:
        token_line_number = current_token.original_line_number
    __validate_block_token_height(
        last_token,
        current_token,
        token_line_number,
        False,
        last_token_index,
        actual_tokens,
        token_stack,
    )
    return remember_token_as_last_token


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
        print(">>top_block>>=" + ParserHelper.make_value_visible(top_block))
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
            and container_block_stack[-1] != current_token
            and current_token.token_name != MarkdownToken.token_blank_line
            and top_block.token_name == MarkdownToken.token_block_quote
        ):

            split_leading_spaces = top_block.leading_spaces.split("\n")
            print(">>in bq>>split>" + str(split_leading_spaces))
            print(">>in bq>>index>" + str(top_block.leading_text_index))
            init_ws += len(split_leading_spaces[top_block.leading_text_index])
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
    elif (
        container_block_stack
        and current_token.token_name == MarkdownToken.token_blank_line
    ):
        if container_block_stack[-1].token_name == MarkdownToken.token_block_quote:
            init_ws += len(current_token.extracted_whitespace)
            split_leading_spaces = container_block_stack[-1].leading_spaces.split("\n")
            print(">>blank_line>>split>" + str(split_leading_spaces))
            print(
                ">>blank_line>>index>"
                + str(container_block_stack[-1].leading_text_index)
            )
            init_ws += len(
                split_leading_spaces[container_block_stack[-1].leading_text_index]
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
        had_tab = bool(ParserHelper.tab_character in calc_token.extracted_whitespace)
    elif (
        calc_token.token_name == MarkdownToken.token_ordered_list_start
        or calc_token.token_name == MarkdownToken.token_unordered_list_start
    ):
        indent_level = len(calc_token.extracted_whitespace)
        had_tab = bool(
            ParserHelper.tab_character in calc_token.extracted_whitespace
            or (
                calc_token.leading_spaces
                and ParserHelper.tab_character in calc_token.leading_spaces
            )
        )
    elif (
        calc_token.token_name == MarkdownToken.token_html_block
        or calc_token.token_name == MarkdownToken.token_blank_line
    ):
        indent_level = 0
    elif calc_token.token_name == MarkdownToken.token_paragraph:

        if ParserHelper.newline_character in calc_token.extracted_whitespace:
            end_of_line_index = calc_token.extracted_whitespace.index(
                ParserHelper.newline_character
            )
            first_para_ws = calc_token.extracted_whitespace[0:end_of_line_index]
        else:
            first_para_ws = calc_token.extracted_whitespace
        print(
            ">>first_para_ws>>" + ParserHelper.make_value_visible(first_para_ws) + ">>"
        )
        indent_level = len(first_para_ws)
        had_tab = bool(ParserHelper.tab_character in first_para_ws)
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
