"""
Module to provide for verification of the line numbers and column numbers in tokens.
"""
from pymarkdown.markdown_token import (
    EndMarkdownToken,
    MarkdownToken,
    MarkdownTokenClass,
)
from pymarkdown.parser_helper import ParserHelper, PositionMarker

# pylint: disable=too-many-lines


# pylint: disable=too-many-branches,too-many-statements,too-many-locals
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
    last_token_stack = None
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
                    last_token_stack,
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
            last_token_stack = token_stack[0:]
        else:
            print("skipping last")

    print("Total lines in source document: " + str(number_of_lines))

    __validate_block_token_height(
        last_token,
        None,
        number_of_lines + 1,
        last_token_index,
        actual_tokens,
        token_stack,
    )
    verify_inline(actual_tokens, last_token, last_token_index, None, last_token_stack)

    assert not token_stack
    assert not container_block_stack


# pylint: enable=too-many-branches,too-many-statements,too-many-locals


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
    last_token_index,
    actual_tokens,
    token_stack,
):
    print("last_token:" + ParserHelper.make_value_visible(last_token))
    print("last_token_index:" + ParserHelper.make_value_visible(last_token_index))
    print("last_line_number:" + ParserHelper.make_value_visible(last_line_number))

    skip_check = False
    if current_token and current_token.token_name == MarkdownToken.token_blank_line:
        print("blank:" + ParserHelper.make_value_visible(token_stack))
        if token_stack and (
            token_stack[-1].token_name == MarkdownToken.token_html_block
            or token_stack[-1].token_name == MarkdownToken.token_fenced_code_block
        ):
            skip_check = True

    delta = last_token.line_number
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
        token_height = last_token.line_number - last_token.original_line_number + 1
        delta = last_token.original_line_number
    else:
        assert False, "Token " + last_token.token_name + " not supported."

    if not skip_check:
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


# pylint: disable=too-many-arguments
def __verify_token_height(
    current_token,
    last_token,
    last_token_index,
    actual_tokens,
    token_stack,
    last_token_stack,
):
    """
    Verify the height of a given token.
    """

    remember_token_as_last_token = __push_to_stack_if_required(
        token_stack, current_token
    )
    assert last_token
    verify_inline(
        actual_tokens, last_token, last_token_index, current_token, last_token_stack
    )

    token_line_number = current_token.line_number
    if current_token.token_name == MarkdownToken.token_setext_heading:
        token_line_number = current_token.original_line_number
    __validate_block_token_height(
        last_token,
        current_token,
        token_line_number,
        last_token_index,
        actual_tokens,
        token_stack,
    )
    return remember_token_as_last_token


# pylint: enable=too-many-arguments


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


def __verify_first_inline(last_non_inline_token, first_inline_token, last_token_stack):
    """
    Verify the first inline token in a sequence.  This means that the previous token
    is guaranteed to be a leaf block token.
    """
    if last_non_inline_token.token_name == MarkdownToken.token_atx_heading:
        __verify_first_inline_atx(last_non_inline_token, first_inline_token)
    elif last_non_inline_token.token_name == MarkdownToken.token_setext_heading:
        __verify_first_inline_setext(last_non_inline_token, first_inline_token)
    elif last_non_inline_token.token_name == MarkdownToken.token_paragraph:
        __verify_first_inline_paragraph(last_non_inline_token, first_inline_token)
    elif last_non_inline_token.token_name == MarkdownToken.token_fenced_code_block:
        __verify_first_inline_fenced_code_block(
            last_non_inline_token, first_inline_token, last_token_stack
        )
    elif last_non_inline_token.token_name == MarkdownToken.token_indented_code_block:
        __verify_first_inline_indented_code_block(
            last_non_inline_token, first_inline_token
        )
    elif last_non_inline_token.token_name == MarkdownToken.token_html_block:
        __verify_first_inline_html_block(last_non_inline_token, first_inline_token)
    else:
        assert False, last_non_inline_token.token_name


def __verify_first_inline_fenced_code_block(
    last_non_inline_token, first_inline_token, last_token_stack
):
    """
    Handle the case where the last non-inline token is an Fecned Code Block token.
    """

    assert (
        first_inline_token.token_name == MarkdownToken.token_text
        or first_inline_token.token_name == MarkdownToken.token_blank_line
    )

    if len(last_token_stack) > 1:
        split_leading_spaces = last_token_stack[-2].leading_spaces.split("\n")
        col_pos = len(split_leading_spaces[1])
    else:
        resolved_extracted_whitespace = ParserHelper.resolve_replacement_markers_from_text(
            first_inline_token.extracted_whitespace
        )
        col_pos = len(resolved_extracted_whitespace)

    assert last_non_inline_token.line_number + 1 == first_inline_token.line_number
    assert first_inline_token.column_number == 1 + col_pos


def __verify_first_inline_indented_code_block(
    last_non_inline_token, first_inline_token
):
    """
    Handle the case where the last non-inline token is an Indented Code Block token.
    """

    assert first_inline_token.token_name == MarkdownToken.token_text
    assert last_non_inline_token.line_number == first_inline_token.line_number
    assert last_non_inline_token.column_number == first_inline_token.column_number


def __verify_first_inline_html_block(last_non_inline_token, first_inline_token):
    """
    Handle the case where the last non-inline token is a HTML Block token.
    """

    assert first_inline_token.token_name == MarkdownToken.token_text
    leading_whitespace_count = len(first_inline_token.extracted_whitespace)
    assert last_non_inline_token.line_number == first_inline_token.line_number
    assert (
        last_non_inline_token.column_number + leading_whitespace_count
        == first_inline_token.column_number
    )


def __verify_first_inline_atx(last_non_inline_token, first_inline_token):
    """
    Handle the case where the last non-inline token is an Atx Heading token.
    """

    col_pos = last_non_inline_token.column_number + last_non_inline_token.hash_count

    if first_inline_token.token_name == MarkdownToken.token_text:
        replaced_extracted_whitespace = ParserHelper.resolve_replacement_markers_from_text(
            first_inline_token.extracted_whitespace
        )
        col_pos += len(replaced_extracted_whitespace)
        assert first_inline_token.line_number == last_non_inline_token.line_number
        assert first_inline_token.column_number == col_pos
    elif first_inline_token.token_name == MarkdownToken.token_inline_hard_break:
        assert False
    elif first_inline_token.token_name == MarkdownToken.token_inline_code_span:
        assert False
    elif first_inline_token.token_name == MarkdownToken.token_inline_raw_html:
        assert False
    elif first_inline_token.token_name == MarkdownToken.token_inline_uri_autolink:
        assert False
    elif first_inline_token.token_name == MarkdownToken.token_inline_email_autolink:
        assert False
    elif first_inline_token.token_name == MarkdownToken.token_inline_emphasis:
        assert False
    elif first_inline_token.token_name == MarkdownToken.token_blank_line:
        assert False
    elif first_inline_token.token_name == MarkdownToken.token_inline_image:
        assert False

    # if a link is first, it creates the whitespace in a text token before it
    else:
        assert (
            first_inline_token.token_name != MarkdownToken.token_inline_link
            and first_inline_token.token_name
            != EndMarkdownToken.type_name_prefix + MarkdownToken.token_inline_link
        ), first_inline_token.token_name


def __verify_first_inline_paragraph(last_non_inline_token, first_inline_token):
    """
    Handle the case where the last non-inline token is a Paragraph token.
    """

    if first_inline_token.token_name == MarkdownToken.token_text:
        assert first_inline_token.line_number == last_non_inline_token.line_number
        assert first_inline_token.column_number == last_non_inline_token.column_number
    elif first_inline_token.token_name == MarkdownToken.token_inline_emphasis:
        assert first_inline_token.line_number == last_non_inline_token.line_number
        assert first_inline_token.column_number == last_non_inline_token.column_number
    elif first_inline_token.token_name == MarkdownToken.token_inline_raw_html:
        assert first_inline_token.line_number == last_non_inline_token.line_number
        assert first_inline_token.column_number == last_non_inline_token.column_number
    elif first_inline_token.token_name == MarkdownToken.token_inline_link:
        assert first_inline_token.line_number == last_non_inline_token.line_number
        assert first_inline_token.column_number == last_non_inline_token.column_number
    elif first_inline_token.token_name == MarkdownToken.token_inline_uri_autolink:
        assert first_inline_token.line_number == last_non_inline_token.line_number
        assert first_inline_token.column_number == last_non_inline_token.column_number
    elif first_inline_token.token_name == MarkdownToken.token_inline_email_autolink:
        assert first_inline_token.line_number == last_non_inline_token.line_number
        assert first_inline_token.column_number == last_non_inline_token.column_number
    elif first_inline_token.token_name == MarkdownToken.token_inline_code_span:
        assert first_inline_token.line_number == last_non_inline_token.line_number
        assert first_inline_token.column_number == last_non_inline_token.column_number

    elif first_inline_token.token_name == MarkdownToken.token_inline_hard_break:
        assert first_inline_token.line_number == 0
        assert first_inline_token.column_number == 0
    elif first_inline_token.token_name == MarkdownToken.token_inline_image:
        assert first_inline_token.line_number == 0
        assert first_inline_token.column_number == 0

    else:
        assert (
            first_inline_token.token_name != MarkdownToken.token_blank_line
        ), first_inline_token.token_name


def __verify_first_inline_setext(last_non_inline_token, first_inline_token):
    """
    Handle the case where the last non-inline token is a SetExt Heading token.
    """

    if first_inline_token.token_name == MarkdownToken.token_text:
        assert (
            last_non_inline_token.original_line_number == first_inline_token.line_number
        )
        assert (
            last_non_inline_token.original_column_number
            == first_inline_token.column_number
        )
    elif first_inline_token.token_name == MarkdownToken.token_inline_emphasis:
        assert False
    elif first_inline_token.token_name == MarkdownToken.token_inline_hard_break:
        assert False
    elif first_inline_token.token_name == MarkdownToken.token_inline_code_span:
        assert False
    elif first_inline_token.token_name == MarkdownToken.token_inline_raw_html:
        assert False
    elif first_inline_token.token_name == MarkdownToken.token_inline_uri_autolink:
        assert False
    elif first_inline_token.token_name == MarkdownToken.token_inline_email_autolink:
        assert False
    elif first_inline_token.token_name == MarkdownToken.token_inline_image:
        assert False
    elif first_inline_token.token_name == MarkdownToken.token_inline_link:
        assert False
    elif (
        first_inline_token.token_name
        == EndMarkdownToken.type_name_prefix + MarkdownToken.token_inline_link
    ):
        assert False
    elif first_inline_token.token_name == EndMarkdownToken.token_blank_line:
        assert False

    else:
        assert False, first_inline_token.token_name


# pylint: disable=too-many-branches,too-many-statements,too-many-locals
def __verify_next_inline(  # noqa: C901
    last_token, pre_previous_inline_token, previous_inline_token, current_inline_token
):
    """
    Verify any pair of inline tokens past the first inline token.
    """

    if (
        previous_inline_token.line_number == 0
        and previous_inline_token.column_number == 0
    ):
        return
    if (
        current_inline_token.line_number == 0
        and current_inline_token.column_number == 0
    ):
        return

    estimated_line_number = previous_inline_token.line_number
    estiated_column_number = previous_inline_token.column_number

    print(
        ">>before-"
        + previous_inline_token.token_name
        + ">>"
        + str(estimated_line_number)
        + ","
        + str(estiated_column_number)
    )

    if previous_inline_token.token_name == MarkdownToken.token_text:
        estimated_line_number, estiated_column_number = __verify_next_inline_text(
            last_token,
            pre_previous_inline_token,
            previous_inline_token,
            estimated_line_number,
            estiated_column_number,
        )
    elif previous_inline_token.token_name == MarkdownToken.token_inline_emphasis:
        (
            estimated_line_number,
            estiated_column_number,
        ) = __verify_next_inline_emphasis_start(
            previous_inline_token, estimated_line_number, estiated_column_number,
        )
    elif (
        previous_inline_token.token_name
        == EndMarkdownToken.type_name_prefix + MarkdownToken.token_inline_emphasis
    ):
        (
            estimated_line_number,
            estiated_column_number,
        ) = __verify_next_inline_emphasis_end(
            previous_inline_token, estimated_line_number, estiated_column_number,
        )
    elif previous_inline_token.token_name == MarkdownToken.token_blank_line:
        estimated_line_number, estiated_column_number = __verify_next_inline_blank_line(
            current_inline_token, estimated_line_number, estiated_column_number,
        )
    elif previous_inline_token.token_name == MarkdownToken.token_inline_hard_break:
        estimated_line_number, estiated_column_number = __verify_next_inline_hard_break(
            last_token,
            previous_inline_token,
            current_inline_token,
            estimated_line_number,
            estiated_column_number,
        )
    elif previous_inline_token.token_name == MarkdownToken.token_inline_code_span:
        estimated_line_number, estiated_column_number = __verify_next_inline_code_span(
            previous_inline_token, estimated_line_number, estiated_column_number,
        )
    elif previous_inline_token.token_name == MarkdownToken.token_inline_raw_html:
        estimated_line_number, estiated_column_number = __verify_next_inline_raw_html(
            previous_inline_token, estimated_line_number, estiated_column_number,
        )
    elif previous_inline_token.token_name == MarkdownToken.token_inline_uri_autolink:
        estimated_line_number, estiated_column_number = __verify_next_inline_autolink(
            previous_inline_token, estimated_line_number, estiated_column_number,
        )
    elif previous_inline_token.token_name == MarkdownToken.token_inline_email_autolink:
        estimated_line_number, estiated_column_number = __verify_next_inline_autolink(
            previous_inline_token, estimated_line_number, estiated_column_number,
        )
    elif previous_inline_token.token_name == MarkdownToken.token_inline_link:
        (
            estimated_line_number,
            estiated_column_number,
        ) = __verify_next_inline_inline_link(
            estimated_line_number, estiated_column_number,
        )
    elif (
        previous_inline_token.token_name
        == EndMarkdownToken.type_name_prefix + MarkdownToken.token_inline_link
    ):
        assert False
    elif previous_inline_token.token_name == MarkdownToken.token_inline_image:
        assert False
    else:
        assert False, previous_inline_token.token_name

    print(
        ">>before-blank>>"
        + str(estimated_line_number)
        + ","
        + str(estiated_column_number)
    )
    if current_inline_token.token_name == MarkdownToken.token_blank_line:
        if previous_inline_token.token_name != MarkdownToken.token_blank_line:
            estimated_line_number += 1
        estiated_column_number = 1
    print(">>after>>" + str(estimated_line_number) + "," + str(estiated_column_number))

    assert estimated_line_number == current_inline_token.line_number, (
        ">>est>"
        + str(estimated_line_number)
        + ">act>"
        + str(current_inline_token.line_number)
    )
    assert estiated_column_number == current_inline_token.column_number, (
        ">>est>"
        + str(estiated_column_number)
        + ">act>"
        + str(current_inline_token.column_number)
    )


# pylint: enable=too-many-branches,too-many-statements,too-many-locals


def __verify_next_inline_blank_line(
    current_inline_token, estimated_line_number, estiated_column_number,
):
    estimated_line_number += 1
    estiated_column_number = 1
    if current_inline_token.token_name == MarkdownToken.token_text:
        estiated_column_number += len(current_inline_token.extracted_whitespace)
    return estimated_line_number, estiated_column_number


def __verify_next_inline_inline_link(
    estimated_line_number, estiated_column_number,
):
    estiated_column_number += 1
    return estimated_line_number, estiated_column_number


def __verify_next_inline_autolink(
    previous_inline_token, estimated_line_number, estiated_column_number
):
    return (
        estimated_line_number,
        estiated_column_number + len(previous_inline_token.autolink_text) + 2,
    )


def __verify_next_inline_raw_html(
    previous_inline_token, estimated_line_number, estiated_column_number,
):

    if "\n" in previous_inline_token.raw_tag:
        split_raw_tag = previous_inline_token.raw_tag.split("\n")
        estimated_line_number += len(split_raw_tag) - 1
        estiated_column_number = len(split_raw_tag[-1]) + 2
    else:
        estiated_column_number += len(previous_inline_token.raw_tag) + 2
    return estimated_line_number, estiated_column_number


# pylint: disable=unused-argument
def __verify_next_inline_hard_break(
    last_token,
    previous_inline_token,
    current_inline_token,
    estimated_line_number,
    estiated_column_number,
):
    new_column_number = 1
    if last_token.token_name == MarkdownToken.token_paragraph:
        split_whitespace = last_token.extracted_whitespace.split("\n")
        ws_for_new_line = split_whitespace[last_token.rehydrate_index]
        last_token.rehydrate_index += 1
        new_column_number += len(ws_for_new_line)
    elif last_token.token_name == MarkdownToken.token_setext_heading:
        assert current_inline_token.token_name == MarkdownToken.token_text
        assert current_inline_token.token_text.startswith("\n")
        assert current_inline_token.end_whitespace.startswith("\n")
        split_whitespace = current_inline_token.end_whitespace.split("\n")
        print(
            "split_whitespace>"
            + ParserHelper.make_value_visible(split_whitespace)
            + "<"
        )
        ws_for_new_line = split_whitespace[1]
        print(
            "ws_for_new_line>" + ParserHelper.make_value_visible(ws_for_new_line) + "<"
        )
        new_column_number += len(ws_for_new_line)
    return estimated_line_number + 1, new_column_number


# pylint: enable=unused-argument


def __verify_next_inline_code_span(
    previous_inline_token, estimated_line_number, estiated_column_number
):

    resolved_span_text = ParserHelper.remove_backspaces_from_text(
        previous_inline_token.span_text
    )
    resolved_span_text = ParserHelper.resolve_replacement_markers_from_text(
        resolved_span_text
    )

    leading_ws_length = len(previous_inline_token.leading_whitespace)
    trailing_ws_length = len(previous_inline_token.trailing_whitespace)
    backtick_length = len(previous_inline_token.extracted_start_backticks)

    if "\n" in resolved_span_text:
        split_span_text = resolved_span_text.split("\n")
        estimated_line_number += len(split_span_text) - 1
        estiated_column_number = (
            len(split_span_text[-1]) + 1 + trailing_ws_length + backtick_length
        )
    else:
        estiated_column_number += (
            len(resolved_span_text)
            + (2 * backtick_length)
            + leading_ws_length
            + trailing_ws_length
        )
    return estimated_line_number, estiated_column_number


def __verify_next_inline_emphasis_start(
    previous_inline_token, estimated_line_number, estiated_column_number,
):
    estiated_column_number += previous_inline_token.emphasis_length
    return estimated_line_number, estiated_column_number


def __verify_next_inline_emphasis_end(
    previous_inline_token, estimated_line_number, estiated_column_number,
):
    print(">>" + str(previous_inline_token.extra_end_data) + "<<")
    split_extra_end_data = previous_inline_token.extra_end_data.split(":")
    print(">>" + str(split_extra_end_data) + "<<")
    estiated_column_number += int(split_extra_end_data[0])
    return estimated_line_number, estiated_column_number


# pylint: disable=too-many-statements, too-many-arguments
def __verify_next_inline_text(
    last_token,
    pre_previous_inline_token,
    previous_inline_token,
    estimated_line_number,
    estiated_column_number,
):
    current_line = previous_inline_token.token_text
    if (
        pre_previous_inline_token
        and pre_previous_inline_token.token_name
        == MarkdownToken.token_inline_hard_break
    ):
        assert current_line.startswith("\n")
        current_line = current_line[1:]
    else:
        if (
            not pre_previous_inline_token
            and last_token.token_name == MarkdownToken.token_atx_heading
        ):
            pass
        else:
            current_line = previous_inline_token.extracted_whitespace + current_line

    print("last_token>" + ParserHelper.make_value_visible(last_token) + "<")
    split_extracted_whitespace = None
    split_end_whitespace = None
    if last_token.token_name == MarkdownToken.token_paragraph:
        print(
            "last_token.rehydrate_index>"
            + ParserHelper.make_value_visible(last_token.rehydrate_index)
            + "<"
        )
        split_extracted_whitespace = last_token.extracted_whitespace.split("\n")
        print(
            "split_extracted_whitespace>"
            + ParserHelper.make_value_visible(split_extracted_whitespace)
            + "<"
        )
    elif (
        last_token.token_name == MarkdownToken.token_setext_heading
        and previous_inline_token.end_whitespace
    ):
        split_end_whitespace = previous_inline_token.end_whitespace.split("\n")
        print(
            "split_end_whitespace>"
            + ParserHelper.make_value_visible(split_end_whitespace)
            + "<"
        )
        split_end_whitespace = split_end_whitespace[-1]
        print(
            "split_end_whitespace>"
            + ParserHelper.make_value_visible(split_end_whitespace)
            + "<"
        )
        if split_end_whitespace:
            assert split_end_whitespace.endswith("\x02")
            split_end_whitespace = split_end_whitespace[0:-1]
            print(
                "split_end_whitespace>"
                + ParserHelper.make_value_visible(split_end_whitespace)
                + "<"
            )
            split_end_whitespace = len(split_end_whitespace)
            print(
                "split_end_whitespace>"
                + ParserHelper.make_value_visible(split_end_whitespace)
                + "<"
            )

    split_current_line = current_line.split("\n")
    print(
        "split_current_line>"
        + ParserHelper.make_value_visible(split_current_line)
        + "<"
    )
    delta_line = len(split_current_line) - 1

    if split_extracted_whitespace and last_token.rehydrate_index < len(
        split_extracted_whitespace
    ):
        rehydrate_index = last_token.rehydrate_index
        for next_line_index in range(1, len(split_current_line)):
            combined_index = next_line_index - 1 + rehydrate_index
            print("combined_index:" + str(combined_index))
            print(
                "split_extracted_whitespace["
                + str(combined_index)
                + "]>"
                + ParserHelper.make_value_visible(
                    split_extracted_whitespace[combined_index]
                )
                + "<"
            )
            print(
                "split_current_line["
                + str(next_line_index)
                + "]>"
                + ParserHelper.make_value_visible(split_current_line[next_line_index])
                + "<"
            )
            split_current_line[next_line_index] = (
                split_extracted_whitespace[combined_index]
                + split_current_line[next_line_index]
            )
            last_token.rehydrate_index += 1
        print(
            "split_current_line>"
            + ParserHelper.make_value_visible(split_current_line)
            + "<"
        )

    split_current_line = split_current_line[-1]
    print(
        "split_current_line>"
        + ParserHelper.make_value_visible(split_current_line)
        + "<"
    )
    split_current_line = ParserHelper.remove_backspaces_from_text(split_current_line)
    split_current_line = ParserHelper.resolve_replacement_markers_from_text(
        split_current_line
    )
    print(
        "split_current_line>"
        + ParserHelper.make_value_visible(split_current_line)
        + "<"
    )
    delta_column = len(split_current_line)

    estimated_line_number += delta_line
    if delta_line:
        estiated_column_number = 1
    estiated_column_number += delta_column
    if split_end_whitespace:
        estiated_column_number += split_end_whitespace
    return estimated_line_number, estiated_column_number


# pylint: enable=too-many-statements, too-many-arguments


# pylint: disable=too-many-branches
def verify_inline(
    actual_tokens, last_token, last_token_index, current_token, last_token_stack
):
    """
    Validate the inline tokens between block tokens.
    """

    print(">>last_token:" + ParserHelper.make_value_visible(last_token))
    next_token_index = last_token_index + 1

    inline_tokens = []
    while (
        next_token_index < len(actual_tokens)
        and actual_tokens[next_token_index] != current_token
    ):
        inline_tokens.append(actual_tokens[next_token_index])
        next_token_index += 1

    while (
        len(inline_tokens) >= 2
        and isinstance(inline_tokens[-1], EndMarkdownToken)
        and (
            inline_tokens[-1].type_name == MarkdownToken.token_unordered_list_start
            or inline_tokens[-1].type_name == MarkdownToken.token_ordered_list_start
            or inline_tokens[-1].type_name == MarkdownToken.token_block_quote
        )
    ):
        del inline_tokens[-1]

    if (
        inline_tokens
        and isinstance(inline_tokens[-1], EndMarkdownToken)
        and (
            inline_tokens[-1].type_name == MarkdownToken.token_unordered_list_start
            or inline_tokens[-1].type_name == MarkdownToken.token_ordered_list_start
            or inline_tokens[-1].type_name == MarkdownToken.token_block_quote
        )
    ):
        del inline_tokens[-1]

    if (
        inline_tokens
        and isinstance(inline_tokens[-1], EndMarkdownToken)
        and inline_tokens[-1].type_name == last_token.token_name
    ):
        del inline_tokens[-1]

    if last_token.token_name == MarkdownToken.token_paragraph:
        last_token.rehydrate_index = 1

    if inline_tokens:
        link_stack = []
        for token_index, current_inline_token in enumerate(inline_tokens):
            print(
                str(token_index)
                + "-token:"
                + ParserHelper.make_value_visible(current_inline_token)
            )
            print("  links:" + ParserHelper.make_value_visible(link_stack))
            if not token_index:
                __verify_first_inline(
                    last_token, current_inline_token, last_token_stack
                )
            else:
                pre_last_token = None
                if token_index >= 2:
                    pre_last_token = inline_tokens[token_index - 2]
                __verify_next_inline(
                    last_token,
                    pre_last_token,
                    inline_tokens[token_index - 1],
                    current_inline_token,
                )

            if current_inline_token.token_name == MarkdownToken.token_inline_link:
                link_stack.append(current_inline_token)
            elif (
                current_inline_token.token_name
                == EndMarkdownToken.type_name_prefix + MarkdownToken.token_inline_link
            ):
                del link_stack[-1]

        assert not link_stack

        # verify_last_inline(inline_tokens[-1], current_inline_token)

    if next_token_index < len(actual_tokens):
        print("<<current_token:" + ParserHelper.make_value_visible(current_token))
    else:
        print("<<[EOL]")


# pylint: enable=too-many-branches
