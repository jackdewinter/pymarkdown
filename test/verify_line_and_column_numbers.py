"""
Module to provide for verification of the line numbers and column numbers in tokens.
"""
from pymarkdown.parser_helper import ParserHelper, PositionMarker

# pylint: disable=too-many-lines


def find_last_block_quote_on_stack(container_block_stack):
    """
    Simple function to calculate if a block quote is in progress.
    """
    last_block_quote_token = None
    if container_block_stack:
        statck_index = len(container_block_stack) - 1
        while (
            statck_index >= 0
            and not container_block_stack[statck_index].is_block_quote_start
        ):
            statck_index -= 1
        if statck_index >= 0:
            last_block_quote_token = container_block_stack[statck_index]
    return last_block_quote_token


# pylint: disable=too-many-branches,too-many-statements,too-many-locals, too-many-boolean-expressions
def verify_line_and_column_numbers(source_markdown, actual_tokens):  # noqa: C901
    """
    Verify that the line numbers and column numbers in tokens are as expected,
    based on the data in the tokens.
    """
    print("\n\n---\nLine/Column Numbers\n---")

    number_of_lines = ParserHelper.count_newlines_in_text(source_markdown) + 1
    print(f"Total lines in source document: {str(number_of_lines)}")

    (
        last_token,
        last_token_index,
        last_token_stack,
        container_block_stack,
        token_stack,
    ) = (None, None, None, [], [])

    for ind, current_token in enumerate(actual_tokens):

        print(f"\n\n-->{ParserHelper.make_value_visible(current_token)}")

        if current_token.is_paragraph_end:
            assert current_token.start_markdown_token
            split_count = (
                ParserHelper.count_newlines_in_text(
                    current_token.start_markdown_token.extracted_whitespace
                )
                + 1
            )
            assert (
                current_token.start_markdown_token.rehydrate_index + 1
            ) == split_count, f"index={str(current_token.start_markdown_token.rehydrate_index)};split={str(split_count)}"

        if current_token.is_inline and not current_token.is_end_token:
            print(f"Inline, skipping:{ParserHelper.make_value_visible(token_stack)}")
            last_block_quote_token = find_last_block_quote_on_stack(
                container_block_stack
            )
            if last_block_quote_token:
                print(
                    f"number_of_lines:{ParserHelper.make_value_visible(actual_tokens[ind - 1])}"
                )
                if current_token.is_text:
                    if (
                        actual_tokens[ind - 1].is_html_block
                        or actual_tokens[ind - 1].is_indented_code_block
                        or actual_tokens[ind - 1].is_fenced_code_block
                        or actual_tokens[ind - 1].is_setext_heading
                        or actual_tokens[ind - 1].is_paragraph
                    ):
                        newlines_in_text_token = ParserHelper.count_newlines_in_text(
                            current_token.token_text
                        )
                        print(f">>newlines_in_text_token>{str(newlines_in_text_token)}")
                        print(
                            f">>mainline-html>>leading_text_index>{str(last_block_quote_token.leading_text_index)}"
                        )
                        last_block_quote_token.leading_text_index += (
                            newlines_in_text_token
                        )
                        print(
                            f">>mainline-html>>leading_text_index>{str(last_block_quote_token.leading_text_index)}"
                        )
                elif current_token.is_inline_image or current_token.is_inline_link:
                    print(
                        f">>mainline-inline>>leading_text_index>{str(last_block_quote_token.leading_text_index)}"
                    )
                    last_block_quote_token.leading_text_index += (
                        ParserHelper.count_newlines_in_text(
                            current_token.text_from_blocks
                        )
                    )
                    print(
                        f">>mainline-inline>>leading_text_index>{str(last_block_quote_token.leading_text_index)}"
                    )
                elif current_token.is_inline_raw_html:
                    print(
                        f">>mainline-inline>>leading_text_index>{str(last_block_quote_token.leading_text_index)}"
                    )
                    last_block_quote_token.leading_text_index += (
                        ParserHelper.count_newlines_in_text(current_token.raw_tag)
                    )
                    print(
                        f">>mainline-inline>>leading_text_index>{str(last_block_quote_token.leading_text_index)}"
                    )
                elif current_token.is_inline_code_span:
                    print(
                        f">>mainline-inline>>leading_text_index>{str(last_block_quote_token.leading_text_index)}"
                    )
                    last_block_quote_token.leading_text_index += (
                        ParserHelper.count_newlines_in_texts(
                            current_token.leading_whitespace,
                            current_token.span_text,
                            current_token.trailing_whitespace,
                        )
                    )
                    print(
                        f">>mainline-inline>>leading_text_index>{str(last_block_quote_token.leading_text_index)}"
                    )
            continue

        current_position = __calc_adjusted_position(current_token)

        __maintain_block_stack(container_block_stack, current_token)

        if current_token.is_end_token:
            print("end token, skipping")
            __pop_from_stack_if_required(token_stack, current_token)
            last_block_quote_token = find_last_block_quote_on_stack(
                container_block_stack
            )
            if last_block_quote_token:
                print("block quotes: looking for implicit newlines")
                if (
                    current_token.is_atx_heading_end
                    or current_token.is_paragraph_end
                    or current_token.is_html_block_end
                    or current_token.is_indented_code_block_end
                    or current_token.is_fenced_code_block_end
                    or current_token.is_setext_heading_end
                ):
                    print(
                        f">>mainline-ends>>leading_text_index>{str(last_block_quote_token.leading_text_index)}"
                    )
                    if current_token.is_fenced_code_block_end:
                        last_block_quote_token.leading_text_index += 3
                    elif current_token.is_setext_heading_end:
                        last_block_quote_token.leading_text_index += 2
                    else:
                        last_block_quote_token.leading_text_index += 1
                    print(
                        f">>mainline-ends>>leading_text_index>{str(last_block_quote_token.leading_text_index)}"
                    )
            continue

        if current_token.is_block_quote_start:
            print("block token index reset")
            current_token.leading_text_index = 0
            print(
                f">>start bq>>leading_text_index>{str(container_block_stack[-1].leading_text_index)}"
            )

        print("--")
        print(
            f"this>>{str(current_token.token_name)}>>({str(current_position.line_number)},{str(current_position.index_number)})"
        )
        if last_token:
            last_position = __calc_adjusted_position(last_token)
            print(
                f"last>>{str(last_token.token_name)}>>{str(last_position.line_number)},{str(last_position.index_number)})"
            )

            top_block_token = None
            for next_container_block in container_block_stack:
                if next_container_block.is_block_quote_start:
                    top_block_token = next_container_block
                elif next_container_block.is_list_start:
                    break
            print(
                f"top_block_token>>{ParserHelper.make_value_visible(top_block_token)}"
            )
            if top_block_token and last_token.is_link_reference_definition:

                print(
                    f">>mainline-top_block_token>>leading_text_index>{str(container_block_stack[-1].leading_text_index)}"
                )
                top_block_token.leading_text_index += (
                    ParserHelper.count_newlines_in_texts(
                        last_token.link_name_debug,
                        last_token.link_destination_whitespace,
                        last_token.link_title_whitespace,
                        last_token.link_title,
                    )
                )
                print(
                    f">>mainline-top_block_token>>leading_text_index>{str(container_block_stack[-1].leading_text_index)}"
                )

            did_x = False
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
                did_x = __validate_new_line(
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

            __xx(current_token, token_stack)

            print(
                f"top_block_token<<{ParserHelper.make_value_visible(top_block_token)}"
            )
            if top_block_token:
                print(
                    f"current_token<<{ParserHelper.make_value_visible(current_token)}"
                )
                if (
                    top_block_token != current_token
                    and current_token.is_blank_line
                    and not did_x
                ):
                    print(
                        f">>mainline-top_block_token>>leading_text_index>{str(container_block_stack[-1].leading_text_index)}"
                    )
                    top_block_token.leading_text_index += 1
                    print(
                        f">>mainline-top_block_token>>leading_text_index>{str(container_block_stack[-1].leading_text_index)}"
                    )
        else:
            __validate_first_token(current_token, current_position)
            remember_token_as_last_token = __push_to_stack_if_required(
                token_stack, current_token
            )

        if remember_token_as_last_token:
            print("saving last")
            last_token, last_token_index, last_token_stack = (
                current_token,
                ind,
                token_stack[0:],
            )
        else:
            print("skipping last")

    print(f"Total lines in source document: {str(number_of_lines)}")

    __validate_block_token_height(
        last_token,
        None,
        number_of_lines + 1,
        last_token_index,
        actual_tokens,
        token_stack,
    )
    __verify_inline(
        actual_tokens,
        last_token,
        last_token_index,
        None,
        last_token_stack,
        number_of_lines,
    )

    assert (
        not token_stack
    ), f"Token stack should be empty: {ParserHelper.make_value_visible(token_stack)}"
    assert (
        not container_block_stack
    ), f"Container block stack should be empty: {ParserHelper.make_value_visible(container_block_stack)}"


# pylint: enable=too-many-branches,too-many-statements,too-many-locals, too-many-boolean-expressions


def __push_to_stack_if_required(token_stack, current_token):
    print(
        f"__push_to_stack_if_required->before->{ParserHelper.make_value_visible(token_stack)}"
    )
    remember_token_as_last_token = True

    if (
        not current_token.is_blank_line
        and not current_token.is_new_list_item
        and not current_token.is_link_reference_definition
        and not current_token.is_thematic_break
        and not current_token.is_front_matter
    ):
        token_stack.append(current_token)
    else:
        remember_token_as_last_token = not (
            token_stack
            and (token_stack[-1].is_html_block or token_stack[-1].is_fenced_code_block)
        )
    print(
        f"__push_to_stack_if_required->after->{str(remember_token_as_last_token)}:{ParserHelper.make_value_visible(token_stack)}"
    )
    return remember_token_as_last_token


def __pop_from_stack_if_required(token_stack, current_token):
    print(
        f"__pop_from_stack_if_required->current_token->{ParserHelper.make_value_visible(current_token)}"
    )
    print(
        f"__pop_from_stack_if_required->before->{ParserHelper.make_value_visible(token_stack)}"
    )
    assert token_stack
    if (
        current_token.is_end_token
        and current_token.type_name == token_stack[-1].token_name
    ):
        del token_stack[-1]
    print(
        f"__pop_from_stack_if_required->after->{ParserHelper.make_value_visible(token_stack)}"
    )


# pylint: disable=too-many-arguments,too-many-branches
def __validate_block_token_height(
    last_token,
    current_token,
    last_line_number,
    last_token_index,
    actual_tokens,
    token_stack,
):
    print(f"last_token:{ParserHelper.make_value_visible(last_token)}")
    print(f"last_token_index:{ParserHelper.make_value_visible(last_token_index)}")
    print(f"last_line_number:{ParserHelper.make_value_visible(last_line_number)}")

    skip_check = False
    if current_token and current_token.is_blank_line:
        print(f"blank:{ParserHelper.make_value_visible(token_stack)}")
        skip_check = token_stack and (
            token_stack[-1].is_html_block or token_stack[-1].is_fenced_code_block
        )

    delta = last_token.line_number
    if last_token.is_extension:
        token_height = last_token.calculate_block_token_height(last_token)
    elif last_token.is_paragraph:
        token_height = 1 + ParserHelper.count_newlines_in_text(
            last_token.extracted_whitespace
        )
    elif last_token.is_indented_code_block:
        token_height = 1 + ParserHelper.count_newlines_in_text(
            last_token.indented_whitespace
        )
    elif last_token.is_html_block or last_token.is_fenced_code_block:
        current_token_index, token_height = (
            last_token_index + 1,
            1 if last_token.is_fenced_code_block else 0,
        )
        while not (
            actual_tokens[current_token_index].is_end_token
            and actual_tokens[current_token_index].type_name == last_token.token_name
        ):
            if actual_tokens[current_token_index].is_text:
                token_height += 1 + ParserHelper.count_newlines_in_text(
                    actual_tokens[current_token_index].token_text
                )
            else:
                assert actual_tokens[current_token_index].is_blank_line
                token_height += 1
            current_token_index += 1
        if (
            last_token.is_fenced_code_block
            and not actual_tokens[current_token_index].was_forced
        ):
            token_height += 1
    elif last_token.is_link_reference_definition:
        token_height = 1 + ParserHelper.count_newlines_in_texts(
            last_token.extracted_whitespace,
            last_token.link_name_debug,
            last_token.link_destination_whitespace,
            last_token.link_title_raw,
            last_token.link_title_whitespace,
        )
    elif (
        last_token.is_thematic_break
        or last_token.is_atx_heading
        or last_token.is_blank_line
    ):
        token_height = 1
    else:
        assert (
            last_token.is_setext_heading
        ), f"Token {last_token.token_name} not supported."
        token_height = last_token.line_number - last_token.original_line_number + 1
        delta = last_token.original_line_number

    if not skip_check:
        print(
            f"delta:{ParserHelper.make_value_visible(delta)}; height:{str(token_height)}"
        )
        delta += token_height
        print(f"calc current_line_number:{ParserHelper.make_value_visible(delta)}")
        assert (
            delta == last_line_number
        ), f"Calculated line number '{str(delta)}' does not equal the actual line number '{str(last_line_number)}'."


# pylint: enable=too-many-arguments,too-many-branches


# pylint: disable=too-many-arguments
def __verify_token_height(
    current_block_token,
    last_block_token,
    last_token_index,
    actual_tokens,
    token_stack,
    last_token_stack,
):
    """
    Verify the height of a given token.
    """

    remember_token_as_last_token = __push_to_stack_if_required(
        token_stack, current_block_token
    )
    assert last_block_token
    __verify_inline(
        actual_tokens,
        last_block_token,
        last_token_index,
        current_block_token,
        last_token_stack,
        None,
    )

    token_line_number = (
        current_block_token.original_line_number
        if current_block_token.is_setext_heading
        else current_block_token.line_number
    )
    __validate_block_token_height(
        last_block_token,
        current_block_token,
        token_line_number,
        last_token_index,
        actual_tokens,
        token_stack,
    )

    return remember_token_as_last_token


# pylint: enable=too-many-arguments


def __xx(current_block_token, token_stack):
    if current_block_token.is_link_reference_definition:
        print(
            f"vth>>current_token>>{ParserHelper.make_value_visible(current_block_token)}"
        )
        print(f"vth>>token_stack>>{ParserHelper.make_value_visible(token_stack)}")
        if token_stack:
            i = len(token_stack) - 1
            if token_stack[i].is_block_quote_start:
                token_stack[i].leading_text_index += 1


# pylint: disable=too-many-branches, too-many-statements
def __validate_same_line(
    container_block_stack, current_token, current_position, last_token, last_position
):

    print(">>__validate_same_line")
    if container_block_stack:
        top_block = container_block_stack[-1]
        _, had_tab = __calc_initial_whitespace(top_block)
        print(f">>top_block>>w/ tab={str(had_tab)}")
        if had_tab:
            return

    _, had_tab = __calc_initial_whitespace(current_token)
    print(f">>current_token>>w/ tab={str(had_tab)}")
    if had_tab:
        return

    assert last_token.is_container

    # TODO replace > with computation for block quote cases
    assert current_position.index_number > last_position.index_number
    if not last_token.is_block_quote_start:
        assert last_token.is_list_start or last_token.is_new_list_item
        print(f">>current_token>>{str(current_token)}")
        print(f">>current_position.index_number>>{str(current_position.index_number)}")
        print(f">>last_token>>{str(last_token)}")
        print(f">>last_token.indent_level>>{str(last_token.indent_level)}")
        if current_token.is_blank_line:
            assert current_position.index_number == last_token.indent_level
        elif current_token.is_indented_code_block:
            assert (
                current_position.index_number - len(current_token.extracted_whitespace)
                == last_token.indent_level + 1
            )
        else:
            assert current_position.index_number == last_token.indent_level + 1


# pylint: enable=too-many-branches, too-many-statements


# pylint: disable=too-many-branches, too-many-statements
def __validate_new_line(container_block_stack, current_token, current_position):
    print(">>__validate_new_line")
    init_ws, had_tab = __calc_initial_whitespace(current_token)
    print(f">>init_ws({str(init_ws)})>>w/ tab={str(had_tab)}")
    if had_tab:
        return False

    did_x = False

    if (
        container_block_stack
        and not current_token.is_blank_line
        and not current_token.is_list_start
        and not current_token.is_new_list_item
    ):
        print(">>__vnl->list-ish")
        top_block = container_block_stack[-1]
        _, had_tab = __calc_initial_whitespace(top_block)
        print(f">>top_block>>={ParserHelper.make_value_visible(top_block)}")
        print(f">>top_block>>w/ tab={str(had_tab)}")
        if had_tab:
            return False

        if top_block.is_list_start or top_block.is_new_list_item:
            print(">>__vnl->list")
            init_ws += top_block.indent_level
        elif (
            container_block_stack
            and container_block_stack[-1] != current_token
            and not current_token.is_blank_line
            and top_block.is_block_quote_start
        ):
            print(">>__vnl->not block")
            next_leading_space_part = top_block.calculate_next_leading_space_part(
                increment_index=False
            )
            init_ws += len(next_leading_space_part)
    elif container_block_stack and current_token.is_new_list_item:
        print(">>__vnl->li-ish")
        assert container_block_stack[-1] == current_token
        if len(container_block_stack) > 1:
            top_block = container_block_stack[-2]
            init_ws = (
                top_block.column_number
                - 1
                + (current_token.indent_level - top_block.indent_level)
            )
    elif container_block_stack and current_token.is_blank_line:
        print(">>__vnl->blank-ish")
        if container_block_stack[-1].is_block_quote_start:

            leading_text, did_x = (
                container_block_stack[-1].calculate_next_leading_space_part(),
                True,
            )
            init_ws += len(leading_text)

    print(f">>current_position.index_number>>{str(current_position.index_number)}")
    print(f">>current_position.index_indent>>{str(current_position.index_indent)}")
    print(f">>1 + init_ws({str(init_ws)})>>{str(1 + init_ws)}")
    if not had_tab:
        assert (
            current_position.index_number == 1 + init_ws
        ), f"Line:{str(current_position.line_number)}:{str(current_token)}"
    return did_x


# pylint: enable=too-many-branches, too-many-statements


def __validate_first_token(current_token, current_position):
    print(">>__validate_first_line")
    assert current_position.line_number == 1

    init_ws, had_tab = __calc_initial_whitespace(current_token)
    if not had_tab:
        assert current_position.index_number == 1 + init_ws


# pylint: disable=too-many-boolean-expressions
def __calc_initial_whitespace(calc_token):
    had_tab = False
    if calc_token.is_extension:
        indent_level, had_tab = calc_token.calculate_initial_whitespace()
    elif (
        calc_token.is_new_list_item
        or calc_token.is_block_quote_start
        or calc_token.is_atx_heading
        or calc_token.is_setext_heading
        or calc_token.is_thematic_break
        or calc_token.is_link_reference_definition
        or calc_token.is_fenced_code_block
        or calc_token.is_indented_code_block
    ):
        indent_level, had_tab = (
            len(calc_token.extracted_whitespace),
            ParserHelper.tab_character in calc_token.extracted_whitespace,
        )
    elif calc_token.is_list_start:
        indent_level, had_tab = len(calc_token.extracted_whitespace), (
            ParserHelper.tab_character in calc_token.extracted_whitespace
            or (
                calc_token.leading_spaces
                and ParserHelper.tab_character in calc_token.leading_spaces
            )
        )
    elif calc_token.is_html_block or calc_token.is_blank_line:
        indent_level = 0
    else:
        assert calc_token.is_paragraph, f"Token {calc_token.token_name} not handled."

        if ParserHelper.newline_character in calc_token.extracted_whitespace:
            end_of_line_index = calc_token.extracted_whitespace.index(
                ParserHelper.newline_character
            )
            first_para_ws = calc_token.extracted_whitespace[0:end_of_line_index]
        else:
            first_para_ws = calc_token.extracted_whitespace
        print(f">>first_para_ws>>{ParserHelper.make_value_visible(first_para_ws)}>>")
        indent_level, had_tab = (
            len(first_para_ws),
            ParserHelper.tab_character in first_para_ws,
        )
        print(f">>indent_level>>{str(indent_level)}>>had_tab>>{str(had_tab)}")
    return indent_level, had_tab


# pylint: enable=too-many-boolean-expressions


def __calc_adjusted_position(markdown_token):
    if markdown_token.is_setext_heading:
        line_number, index_number = (
            markdown_token.original_line_number,
            markdown_token.original_column_number,
        )
    else:
        line_number, index_number = (
            markdown_token.line_number,
            markdown_token.column_number,
        )
    return PositionMarker(line_number, index_number, "")


def __maintain_block_stack(container_block_stack, current_token):
    """
    Maintain a stack of the block elements, to allow better understanding of
    what container a given token is kept within.
    """

    if current_token.is_container:
        print("--")
        print(
            f">>CON>>before>>{ParserHelper.make_value_visible(container_block_stack)}"
        )
        if (
            current_token.is_new_list_item
            and container_block_stack[-1].is_new_list_item
        ):
            del container_block_stack[-1]

        container_block_stack.append(current_token)
        print(f">>CON>>after>>{ParserHelper.make_value_visible(container_block_stack)}")

    elif current_token.is_end_token and (
        current_token.is_block_quote_end
        or current_token.is_list_end
        or current_token.is_new_list_item
    ):
        print("--")
        print(
            f"<<CON<<before<<{ParserHelper.make_value_visible(container_block_stack)}"
        )

        if container_block_stack[-1].is_new_list_item:
            del container_block_stack[-1]

        assert container_block_stack[-1].token_name == current_token.type_name
        del container_block_stack[-1]
        print(f"<<CON<<after<<{ParserHelper.make_value_visible(container_block_stack)}")
        # if current_token.is_block_quote_end:
        #    leading_text_index, expected_leading_text_index = (
        #        current_token.start_markdown_token.leading_text_index,
        #        ParserHelper.count_newlines_in_text(
        #            current_token.start_markdown_token.leading_spaces
        #        ),
        #    )

        # assert True or (
        #    leading_text_index == expected_leading_text_index + 1
        #   or (leading_text_index == expected_leading_text_index)
        # ), f"leading_text_index={str(leading_text_index)};expected_leading_text_index={str(expected_leading_text_index)}"


def __verify_first_inline(last_non_inline_token, first_inline_token, last_token_stack):
    """
    Verify the first inline token in a sequence.  This means that the previous token
    is guaranteed to be a leaf block token.
    """
    if last_non_inline_token.is_atx_heading:
        __verify_first_inline_atx(last_non_inline_token, first_inline_token)
    elif last_non_inline_token.is_setext_heading:
        __verify_first_inline_setext(last_non_inline_token, first_inline_token)
    elif last_non_inline_token.is_paragraph:
        __verify_first_inline_paragraph(last_non_inline_token, first_inline_token)
    elif last_non_inline_token.is_fenced_code_block:
        __verify_first_inline_fenced_code_block(
            last_non_inline_token, first_inline_token, last_token_stack
        )
    elif last_non_inline_token.is_indented_code_block:
        __verify_first_inline_indented_code_block(
            last_non_inline_token, first_inline_token
        )
    else:
        assert last_non_inline_token.is_html_block, last_non_inline_token.token_name
        __verify_first_inline_html_block(last_non_inline_token, first_inline_token)


def __verify_first_inline_fenced_code_block(
    last_non_inline_token, first_inline_token, last_token_stack
):
    """
    Handle the case where the last non-inline token is an Fenced Code Block token.
    """

    assert first_inline_token.is_text or first_inline_token.is_blank_line

    print(f">last_token_stack>{ParserHelper.make_value_visible(last_token_stack)}")
    if len(last_token_stack) > 1:
        split_leading_spaces = last_token_stack[-2].leading_spaces.split(
            ParserHelper.newline_character
        )
        col_pos = (
            len(split_leading_spaces[1])
            if len(split_leading_spaces) >= 2
            else len(split_leading_spaces[0])
        )
    else:
        if first_inline_token.is_blank_line:
            col_pos = 0
        else:
            resolved_extracted_whitespace = ParserHelper.remove_all_from_text(
                first_inline_token.extracted_whitespace
            )
            print(
                f">resolved_extracted_whitespace>{ParserHelper.make_value_visible(resolved_extracted_whitespace)}<"
            )
            col_pos = len(resolved_extracted_whitespace)

    print(f">first_inline_token.column_number>{str(first_inline_token.column_number)}")
    print(f">col_pos>{str(col_pos)}")
    assert last_non_inline_token.line_number + 1 == first_inline_token.line_number
    assert first_inline_token.column_number == 1 + col_pos


def __verify_first_inline_indented_code_block(
    last_non_inline_token, first_inline_token
):
    """
    Handle the case where the last non-inline token is an Indented Code Block token.
    """

    assert first_inline_token.is_text
    assert last_non_inline_token.line_number == first_inline_token.line_number
    assert last_non_inline_token.column_number == first_inline_token.column_number


def __verify_first_inline_html_block(last_non_inline_token, first_inline_token):
    """
    Handle the case where the last non-inline token is a HTML Block token.
    """

    assert first_inline_token.is_text
    assert last_non_inline_token.line_number == first_inline_token.line_number
    assert (
        last_non_inline_token.column_number
        + len(first_inline_token.extracted_whitespace)
        == first_inline_token.column_number
    )


def __verify_first_inline_atx(last_non_inline_token, first_inline_token):
    """
    Handle the case where the last non-inline token is an Atx Heading token.
    """

    assert first_inline_token.is_text, first_inline_token.token_name

    col_pos = (
        last_non_inline_token.column_number
        + last_non_inline_token.hash_count
        + len(
            ParserHelper.remove_all_from_text(first_inline_token.extracted_whitespace)
        )
    )
    assert first_inline_token.line_number == last_non_inline_token.line_number
    assert first_inline_token.column_number == col_pos


# pylint: disable=too-many-boolean-expressions
def __verify_first_inline_paragraph(last_non_inline_token, first_inline_token):
    """
    Handle the case where the last non-inline token is a Paragraph token.
    """

    if (
        first_inline_token.is_text
        or first_inline_token.is_inline_emphasis
        or first_inline_token.is_inline_raw_html
        or first_inline_token.is_inline_link
        or first_inline_token.is_inline_autolink
        or first_inline_token.is_inline_code_span
        or first_inline_token.is_inline_image
        or first_inline_token.is_inline_hard_break
    ):
        assert first_inline_token.line_number == last_non_inline_token.line_number
        assert first_inline_token.column_number == last_non_inline_token.column_number
    else:
        assert not first_inline_token.is_blank_line, first_inline_token.token_name


# pylint: enable=too-many-boolean-expressions


# pylint: disable=too-many-boolean-expressions
def __verify_first_inline_setext(last_non_inline_token, first_inline_token):
    """
    Handle the case where the last non-inline token is a SetExt Heading token.
    """

    if (
        first_inline_token.is_text
        or first_inline_token.is_inline_emphasis
        or first_inline_token.is_inline_code_span
        or first_inline_token.is_inline_raw_html
        or first_inline_token.is_inline_autolink
        or first_inline_token.is_inline_image
        or first_inline_token.is_inline_link
    ):
        assert (
            last_non_inline_token.original_line_number == first_inline_token.line_number
        )
        assert (
            last_non_inline_token.original_column_number
            == first_inline_token.column_number
        )
    elif (
        first_inline_token.is_inline_hard_break
        or first_inline_token.is_inline_link_end
        or first_inline_token.is_blank_line
    ):
        assert False
    else:
        assert False, first_inline_token.token_name


# pylint: enable=too-many-boolean-expressions


# pylint: disable=too-many-branches,too-many-locals,too-many-statements
def __verify_next_inline_handle_previous_end(  # noqa: C901
    last_token, previous_inline_token, current_inline_token, inline_tokens, token_index
):
    """
    This function is intentionally longer than the matching function in
    the source code.  To verify that the source code's function is working
    properly, a second method of computing the values needed to be used.
    Otherwise, it wouldn't really be testing anything!
    """
    print(
        f"  previous has no position: {ParserHelper.make_value_visible(previous_inline_token)}"
    )
    if not current_inline_token:
        return
    print(
        f"  current has position: {ParserHelper.make_value_visible(current_inline_token)}"
    )
    search_token_index = token_index - 1
    print(
        f"{str(search_token_index)}>>{ParserHelper.make_value_visible(inline_tokens[search_token_index])}"
    )
    while (
        search_token_index >= 0
        and inline_tokens[search_token_index].is_end_token
        and inline_tokens[search_token_index].line_number == 0
    ):
        print(f">>{ParserHelper.make_value_visible(inline_tokens[search_token_index])}")
        search_token_index -= 1
    print(
        f"{str(search_token_index)}<<{ParserHelper.make_value_visible(inline_tokens[search_token_index])}"
    )
    assert search_token_index == token_index - 2

    estimated_line_number, estimated_column_number = (
        inline_tokens[search_token_index].line_number,
        inline_tokens[search_token_index].column_number,
    )

    pre_pre_token, pre_token, cur_token = (
        inline_tokens[search_token_index - 1],
        inline_tokens[search_token_index],
        inline_tokens[search_token_index + 1],
    )
    assert cur_token.is_inline_link_end
    parent_cur_token = cur_token.start_markdown_token

    new_lines = 0

    if parent_cur_token.label_type == "inline":
        print(">>inline")

        link_uri_size, link_title = (
            len(parent_cur_token.active_link_uri),
            parent_cur_token.active_link_title,
        )

        part_1, part_2, part_3, part_4, part_5, part_6, part_7 = (
            2,
            len(parent_cur_token.before_link_whitespace),
            (
                (link_uri_size + 2)
                if parent_cur_token.did_use_angle_start
                else link_uri_size
            ),
            len(parent_cur_token.before_title_whitespace),
            0,
            0,
            1,
        )
        if parent_cur_token.inline_title_bounding_character:
            part_5, part_6 = len(link_title) + 2, len(
                parent_cur_token.after_title_whitespace
            )

        newline_count = ParserHelper.count_newlines_in_text(
            parent_cur_token.before_link_whitespace
        )
        if newline_count:
            new_lines += newline_count
            _, delta_column_number = ParserHelper.calculate_deltas(
                parent_cur_token.before_link_whitespace
            )
            part_1, part_2 = 0, -delta_column_number

        newline_count = ParserHelper.count_newlines_in_text(
            parent_cur_token.before_title_whitespace
        )
        if newline_count:
            new_lines += newline_count
            _, delta_column_number = ParserHelper.calculate_deltas(
                parent_cur_token.before_title_whitespace
            )
            part_1, part_2, part_3, part_4 = 0, 0, 0, -delta_column_number

        if parent_cur_token.inline_title_bounding_character:
            newline_count = ParserHelper.count_newlines_in_text(link_title)
            if newline_count:
                new_lines += newline_count
                _, delta_column_number = ParserHelper.calculate_deltas(f"{link_title}]")
                part_1, part_2, part_3, part_4, part_5 = (
                    0,
                    0,
                    0,
                    0,
                    -delta_column_number,
                )

            newline_count = ParserHelper.count_newlines_in_text(
                parent_cur_token.after_title_whitespace
            )
            if newline_count:
                new_lines += newline_count
                _, delta_column_number = ParserHelper.calculate_deltas(
                    parent_cur_token.after_title_whitespace
                )
                part_1, part_2, part_3, part_4, part_5, part_6 = (
                    0,
                    0,
                    0,
                    0,
                    0,
                    -delta_column_number,
                )
        adjust_column_by = part_1 + part_2 + part_3 + part_4 + part_5 + part_6 + part_7
        print(
            f"adjust_column_by={str(adjust_column_by)}({str(part_1)},{str(part_2)},{str(part_3)},{str(part_4)},{str(part_5)},{str(part_6)},{str(part_7)})"
        )
        print(f"newlines={str(new_lines)}")

        if new_lines and last_token.is_paragraph:
            split_para_extracted_whitespace = last_token.extracted_whitespace.split(
                ParserHelper.newline_character
            )
            adjust_column_by += len(
                split_para_extracted_whitespace[last_token.rehydrate_index - 1]
            )
            print(f"adjust_column_by={str(adjust_column_by)}")

    elif parent_cur_token.label_type == "full":
        print(f">>full:{str(parent_cur_token.ex_label)}:")
        newline_count = ParserHelper.count_newlines_in_text(parent_cur_token.ex_label)
        if newline_count:
            new_lines += newline_count
            last_label_line = ParserHelper.calculate_last_line(
                parent_cur_token.ex_label
            )
            adjust_column_by = len(last_label_line) + 2
        else:
            adjust_column_by = len(parent_cur_token.ex_label) + 3

    # Tests test_reference_links_extra_03jx and test_reference_links_extra_03ja added
    # to ensure that this is correct.  Those tests confirm that any newlines in the
    # label are already accounted for, and as such, do not require any further
    # modifications.

    elif parent_cur_token.label_type == "shortcut":
        print(f">>shortcut:{str(parent_cur_token.ex_label)}:")
        adjust_column_by = 1
    else:
        assert parent_cur_token.label_type == "collapsed", parent_cur_token.label_type
        adjust_column_by = 3

    print(f"adj->{str(new_lines)},{str(adjust_column_by)})")

    print(f"before->({str(estimated_line_number)},{str(estimated_column_number)})")
    previous_line_number_delta, _ = __process_previous_token(
        None, pre_pre_token, pre_token, cur_token, None, 0, 0
    )
    print(f"previous_line_number_delta={str(previous_line_number_delta)}")

    previous_rehydrate_index = None
    if last_token.is_paragraph and previous_line_number_delta:
        previous_rehydrate_index = last_token.rehydrate_index
        last_token.rehydrate_index -= previous_line_number_delta
        print(f"rehydrate_index(saved)={str(previous_rehydrate_index)}")
        print(f"last_token.rehydrate_index={str(last_token.rehydrate_index)}")

    new_estimated_line_number, new_estimated_column_number = __process_previous_token(
        last_token,
        pre_pre_token,
        pre_token,
        cur_token,
        None,
        estimated_line_number,
        estimated_column_number,
    )

    if previous_rehydrate_index:
        last_token.rehydrate_index = previous_rehydrate_index
        print(f"rehydrate_index(restored)={str(last_token.rehydrate_index)}")
    print(
        f"after->({str(new_estimated_line_number)},{str(new_estimated_column_number)})"
    )

    print(f"adj->({str(new_lines)},{str(adjust_column_by)})")
    if new_lines:
        new_estimated_line_number += new_lines
        new_estimated_column_number = adjust_column_by
    else:
        new_estimated_column_number += adjust_column_by

    print(f"end->({str(new_estimated_line_number)},{str(new_estimated_column_number)})")
    print(
        f"exp->({str(current_inline_token.line_number)},{str(current_inline_token.column_number)})"
    )
    assert (
        new_estimated_line_number == current_inline_token.line_number
        and new_estimated_column_number == current_inline_token.column_number
    ), f">>est>{str(new_estimated_line_number)},{str(new_estimated_column_number)}>act>{str(current_inline_token.line_number)},{str(current_inline_token.column_number)}"


# pylint: enable=too-many-branches,too-many-locals,too-many-statements


def __verify_next_inline_handle_current_end(last_token, current_inline_token):
    print(
        f"  current has no position: {ParserHelper.make_value_visible(current_inline_token)}"
    )
    print(f"  last_token: {ParserHelper.make_value_visible(last_token)}")

    if current_inline_token.is_inline_link_end and last_token.is_paragraph:
        newline_count = ParserHelper.count_newlines_in_texts(
            current_inline_token.start_markdown_token.before_link_whitespace,
            current_inline_token.start_markdown_token.active_link_uri,
            current_inline_token.start_markdown_token.before_title_whitespace,
            current_inline_token.start_markdown_token.active_link_title,
            current_inline_token.start_markdown_token.after_title_whitespace,
        )
        print(f">>>>>>>>>>newline_count>{str(newline_count)}")
        last_token.rehydrate_index += newline_count
        print(
            f"rehydrate_index(__verify_next_inline_handle_current_end)>{str(last_token.rehydrate_index)}"
        )


# pylint: disable=too-many-arguments
def __verify_next_inline(
    last_token,
    pre_previous_inline_token,
    previous_inline_token,
    current_inline_token,
    link_stack,
    inline_tokens,
    token_index,
):
    """
    Verify any pair of inline tokens past the first inline token.
    """

    if (
        previous_inline_token.line_number == 0
        and previous_inline_token.column_number == 0
    ):
        __verify_next_inline_handle_previous_end(
            last_token,
            previous_inline_token,
            current_inline_token,
            inline_tokens,
            token_index,
        )
        return
    if (
        current_inline_token.line_number == 0
        and current_inline_token.column_number == 0
    ):
        __verify_next_inline_handle_current_end(last_token, current_inline_token)
        return

    estimated_line_number, estimated_column_number = (
        previous_inline_token.line_number,
        previous_inline_token.column_number,
    )

    print(
        f">>before-{previous_inline_token.token_name}>>{str(estimated_line_number)},{str(estimated_column_number)}"
    )

    estimated_line_number, estimated_column_number = __process_previous_token(
        last_token,
        pre_previous_inline_token,
        previous_inline_token,
        current_inline_token,
        link_stack,
        estimated_line_number,
        estimated_column_number,
    )

    assert (
        estimated_line_number == current_inline_token.line_number
        and estimated_column_number == current_inline_token.column_number
    ), f">>est>{str(estimated_line_number)},{str(estimated_column_number)}>act>{str(current_inline_token.line_number)},{str(current_inline_token.column_number)}"


# pylint: enable=too-many-arguments


# pylint: disable=too-many-branches,too-many-arguments
def __process_previous_token(
    last_token,
    pre_previous_inline_token,
    previous_inline_token,
    current_inline_token,
    link_stack,
    estimated_line_number,
    estimated_column_number,
):

    if previous_inline_token.is_text:
        estimated_line_number, estimated_column_number = __verify_next_inline_text(
            last_token,
            pre_previous_inline_token,
            previous_inline_token,
            estimated_line_number,
            estimated_column_number,
            link_stack,
        )
    elif previous_inline_token.is_inline_emphasis:
        (
            estimated_line_number,
            estimated_column_number,
        ) = __verify_next_inline_emphasis_start(
            previous_inline_token,
            estimated_line_number,
            estimated_column_number,
        )
    elif previous_inline_token.is_inline_emphasis_end:
        (
            estimated_line_number,
            estimated_column_number,
        ) = __verify_next_inline_emphasis_end(
            previous_inline_token,
            estimated_line_number,
            estimated_column_number,
        )
    elif previous_inline_token.is_blank_line:
        (
            estimated_line_number,
            estimated_column_number,
        ) = __verify_next_inline_blank_line(
            current_inline_token,
            estimated_line_number,
            estimated_column_number,
        )
    elif previous_inline_token.is_inline_hard_break:
        (
            estimated_line_number,
            estimated_column_number,
        ) = __verify_next_inline_hard_break(
            last_token,
            previous_inline_token,
            current_inline_token,
            estimated_line_number,
            estimated_column_number,
            link_stack,
        )
    elif previous_inline_token.is_inline_code_span:
        estimated_line_number, estimated_column_number = __verify_next_inline_code_span(
            last_token,
            previous_inline_token,
            estimated_line_number,
            estimated_column_number,
            link_stack,
        )
    elif previous_inline_token.is_inline_raw_html:
        estimated_line_number, estimated_column_number = __verify_next_inline_raw_html(
            last_token,
            previous_inline_token,
            estimated_line_number,
            estimated_column_number,
            link_stack,
        )
    elif previous_inline_token.is_inline_autolink:
        estimated_line_number, estimated_column_number = __verify_next_inline_autolink(
            previous_inline_token,
            estimated_line_number,
            estimated_column_number,
        )
    elif previous_inline_token.is_inline_link:
        (
            estimated_line_number,
            estimated_column_number,
        ) = __verify_next_inline_inline_link(
            estimated_line_number,
            estimated_column_number,
        )
    elif previous_inline_token.is_inline_image:
        (
            estimated_line_number,
            estimated_column_number,
        ) = __verify_next_inline_inline_image(
            last_token,
            previous_inline_token,
            estimated_line_number,
            estimated_column_number,
        )
    else:
        assert False, previous_inline_token.token_name

    print(
        f">>before-blank>>{str(estimated_line_number)},{str(estimated_column_number)}"
    )
    if current_inline_token.is_blank_line:
        if not previous_inline_token.is_blank_line:
            estimated_line_number += 1
        estimated_column_number = 1
    print(f">>after>>{str(estimated_line_number)},{str(estimated_column_number)}")
    return estimated_line_number, estimated_column_number


# pylint: enable=too-many-branches,too-many-arguments


def __verify_next_inline_blank_line(
    current_inline_token,
    estimated_line_number,
    estimated_column_number,
):
    _ = estimated_column_number

    return (
        estimated_line_number + 1,
        estimated_column_number + len(current_inline_token.extracted_whitespace)
        if current_inline_token.is_text
        else 1,
    )


def __verify_next_inline_inline_link(
    estimated_line_number,
    estimated_column_number,
):
    return estimated_line_number, estimated_column_number + 1


# pylint: disable=too-many-branches, too-many-statements, too-many-arguments, too-many-locals
def __verify_next_inline_inline_image_inline(  # noqa: C901
    previous_inline_token,
    para_owner,
    before_link_whitespace,
    before_title_whitespace,
    label_data_raw,
    title_data,
    url_data,
    split_paragraph_lines,
    estimated_line_number,
    estimated_column_number,
):

    include_part_1, include_part_2, include_part_3, include_part_4, include_part_5 = (
        True,
        True,
        True,
        True,
        True,
    )

    (
        after_title_whitespace,
        label_data_raw,
    ) = previous_inline_token.after_title_whitespace, ParserHelper.remove_all_from_text(
        label_data_raw
    )

    newline_count = ParserHelper.count_newlines_in_text(
        previous_inline_token.text_from_blocks
    )
    if newline_count:
        estimated_line_number += newline_count
        if para_owner:
            para_owner.rehydrate_index += newline_count
            print(
                f"rehydrate_index(__verify_next_inline_inline_image_inline#1)>{str(para_owner.rehydrate_index)}"
            )
        include_part_1, estimated_column_number, label_data_raw = (
            False,
            0,
            ParserHelper.calculate_last_line(label_data_raw),
        )
        print(f"text_from_blocks>>estimated_line_number>>{str(estimated_line_number)}")

    newline_count = ParserHelper.count_newlines_in_text(before_link_whitespace)
    if newline_count:
        estimated_line_number += newline_count
        if para_owner:
            para_owner.rehydrate_index += newline_count
            print(
                f"rehydrate_index(__verify_next_inline_inline_image_inline#2)>{str(para_owner.rehydrate_index)}"
            )
        (
            estimated_column_number,
            include_part_1,
            include_part_2,
            before_link_whitespace,
        ) = (0, False, False, ParserHelper.calculate_last_line(before_link_whitespace))
        print(
            f"before_link_whitespace>>estimated_line_number>>{str(estimated_line_number)}"
        )

    newline_count = ParserHelper.count_newlines_in_text(before_title_whitespace)
    if newline_count:
        estimated_line_number += newline_count
        if para_owner:
            para_owner.rehydrate_index += newline_count
            print(
                f"rehydrate_index(__verify_next_inline_inline_image_inline#3)>{str(para_owner.rehydrate_index)}"
            )
        (
            estimated_column_number,
            include_part_1,
            include_part_2,
            include_part_3,
            before_title_whitespace,
        ) = (
            0,
            False,
            False,
            False,
            ParserHelper.calculate_last_line(before_title_whitespace),
        )
        print(
            f"before_title_whitespace>>estimated_line_number>>{str(estimated_line_number)}"
        )

    newline_count = ParserHelper.count_newlines_in_text(title_data)
    if newline_count:
        estimated_line_number += newline_count
        if para_owner:
            para_owner.rehydrate_index += newline_count
            print(
                f"rehydrate_index(__verify_next_inline_inline_image_inline#4)>{str(para_owner.rehydrate_index)}"
            )
        (
            estimated_column_number,
            include_part_1,
            include_part_2,
            include_part_3,
            include_part_4,
            title_data,
        ) = (
            0,
            False,
            False,
            False,
            False,
            ParserHelper.calculate_last_line(title_data),
        )
        print(f"title_data>>estimated_line_number>>{str(estimated_line_number)}")

    newline_count = ParserHelper.count_newlines_in_text(after_title_whitespace)
    if newline_count:
        estimated_line_number += newline_count
        if para_owner:
            para_owner.rehydrate_index += newline_count
            print(
                f"rehydrate_index(__verify_next_inline_inline_image_inline#5)>{str(para_owner.rehydrate_index)}"
            )
        (
            estimated_column_number,
            include_part_1,
            include_part_2,
            include_part_3,
            include_part_4,
            include_part_5,
            after_title_whitespace,
        ) = (
            0,
            False,
            False,
            False,
            False,
            False,
            ParserHelper.calculate_last_line(after_title_whitespace),
        )
        print(
            f"after_title_whitespace>>estimated_line_number>>{str(estimated_line_number)}"
        )

    print(f">>estimated_column_number>>{str(estimated_column_number)}")
    if include_part_1:
        estimated_column_number += 1
        print(f">>include_part_1>>{str(estimated_column_number)}")
    if include_part_2:
        estimated_column_number += len(label_data_raw) + 2
        print(f">>label_data_raw>>{ParserHelper.make_value_visible(label_data_raw)}<<")
        print(f">>include_part_2>>{str(estimated_column_number)}")
    if include_part_3:
        estimated_column_number += len(before_link_whitespace) + len(url_data)
        if previous_inline_token.did_use_angle_start:
            estimated_column_number += 2
        print(f">>include_part_3>>{str(estimated_column_number)}")
    if include_part_4:
        print(f">>include_part_4>>{str(before_title_whitespace)}<")
        estimated_column_number += len(before_title_whitespace)
        print(f">>include_part_4>>{str(estimated_column_number)}")
    if previous_inline_token.inline_title_bounding_character:
        if include_part_4:
            estimated_column_number += 1
            print(f">>include_part_4a>>{str(estimated_column_number)}")
        if include_part_5:
            estimated_column_number += len(title_data) + 1 + len(after_title_whitespace)
            print(f">>include_part_5>>{str(estimated_column_number)}")
        else:
            estimated_column_number += len(after_title_whitespace)
            print(f">>include_part_5a>>{str(estimated_column_number)}")
    estimated_column_number += +1
    if not include_part_1 and para_owner:
        print(f">>split_paragraph_lines>>{str(split_paragraph_lines)}")
        print(f">>para_owner.rehydrate_index>>{str(para_owner.rehydrate_index)}")
        print(
            f"rehydrate_index(__verify_next_inline_inline_image_inline#6)>{str(para_owner.rehydrate_index)}"
        )
        estimated_column_number += len(
            split_paragraph_lines[para_owner.rehydrate_index - 1]
        )
    return estimated_line_number, estimated_column_number + 1


# pylint: enable=too-many-branches, too-many-statements, too-many-arguments, too-many-locals

# pylint: disable=too-many-locals, too-many-branches, too-many-statements
def __verify_next_inline_inline_image(  # noqa: C901
    last_token, previous_inline_token, estimated_line_number, estimated_column_number
):

    print(
        f">>image_alt_text>>{ParserHelper.make_value_visible(previous_inline_token.image_alt_text)}"
    )
    print(
        f">>ex_label>>{ParserHelper.make_value_visible(previous_inline_token.ex_label)}"
    )
    label_data = (
        previous_inline_token.ex_label
        if previous_inline_token.ex_label
        else previous_inline_token.image_alt_text
    )
    print(f">>label_data>>{ParserHelper.make_value_visible(label_data)}")

    before_link_whitespace, url_data, before_title_whitespace, title_data = (
        previous_inline_token.before_link_whitespace,
        previous_inline_token.active_link_uri,
        previous_inline_token.before_title_whitespace,
        previous_inline_token.active_link_title,
    )

    print(f">>last_token>>{ParserHelper.make_value_visible(last_token)}")
    print(
        f">>previous_inline_token>>{ParserHelper.make_value_visible(previous_inline_token)}"
    )
    print(f">>label_data>>{ParserHelper.make_value_visible(label_data)}")
    print(f">>url_data>>{ParserHelper.make_value_visible(url_data)}")
    print(f">>title_data>>{ParserHelper.make_value_visible(title_data)}")
    para_owner, split_paragraph_lines = None, None
    if last_token and last_token.is_paragraph:
        print(f">>last_token_index>>{str(last_token.rehydrate_index)}")
        para_owner = last_token
        split_paragraph_lines = para_owner.extracted_whitespace.split(
            ParserHelper.newline_character
        )
    print(f">>before>>{str(estimated_column_number)}")
    if previous_inline_token.label_type == "inline":
        print(">>>>>>>>>inline")
        (
            estimated_line_number,
            estimated_column_number,
        ) = __verify_next_inline_inline_image_inline(
            previous_inline_token,
            para_owner,
            before_link_whitespace,
            before_title_whitespace,
            previous_inline_token.text_from_blocks,
            title_data,
            url_data,
            split_paragraph_lines,
            estimated_line_number,
            estimated_column_number,
        )
    elif previous_inline_token.label_type == "shortcut":
        print(">>>>>>>>>shortcut")
        label_text, token_prefix = previous_inline_token.text_from_blocks, 1
        newline_count = ParserHelper.count_newlines_in_text(label_text)
        if newline_count:
            print(f">>x>>{ParserHelper.make_value_visible(label_text)}")
            label_text = ParserHelper.remove_all_from_text(label_text)
            print(f">>x>>{ParserHelper.make_value_visible(label_text)}")
            estimated_line_number += newline_count
            if para_owner:
                para_owner.rehydrate_index += newline_count
                print(f"rehydrate_index(shortcut)>{str(para_owner.rehydrate_index)}")
            estimated_column_number = 0

            label_text, token_prefix = ParserHelper.calculate_last_line(label_text), 0
        estimated_column_number += 2 + token_prefix + len(label_text)

    elif previous_inline_token.label_type == "collapsed":
        print(">>>>>>>>>collapsed")
        image_alt_text = (
            previous_inline_token.text_from_blocks
            if previous_inline_token.text_from_blocks
            else previous_inline_token.image_alt_text
        )

        token_prefix = 1
        newline_count = ParserHelper.count_newlines_in_text(image_alt_text)
        if newline_count:
            print(f">>x>>{ParserHelper.make_value_visible(image_alt_text)}")
            image_alt_text = ParserHelper.remove_all_from_text(image_alt_text)
            print(f">>x>>{ParserHelper.make_value_visible(image_alt_text)}")
            estimated_line_number += newline_count
            if para_owner:
                para_owner.rehydrate_index += newline_count
                print(f"rehydrate_index(collapsed)>{str(para_owner.rehydrate_index)}")
            estimated_column_number = 0

            image_alt_text, token_prefix = (
                ParserHelper.calculate_last_line(image_alt_text),
                0,
            )

        estimated_column_number += 2
        estimated_column_number += 2 + token_prefix + len(image_alt_text)
    else:
        assert previous_inline_token.label_type == "full"
        print(">>>>>>>>>full")

        image_alt_text = (
            previous_inline_token.text_from_blocks
            if previous_inline_token.text_from_blocks
            else previous_inline_token.image_alt_text
        )

        print(f">>image_alt_text>>{ParserHelper.make_value_visible(image_alt_text)}")
        print(f">>label_data>>{ParserHelper.make_value_visible(label_data)}")

        token_prefix = 3
        newline_count = ParserHelper.count_newlines_in_text(image_alt_text)
        if newline_count:
            print(f">>x>>{ParserHelper.make_value_visible(image_alt_text)}")
            image_alt_text = ParserHelper.remove_all_from_text(image_alt_text)
            print(f">>x>>{ParserHelper.make_value_visible(image_alt_text)}")

            estimated_line_number += newline_count
            if para_owner:
                para_owner.rehydrate_index += newline_count
                print(f"rehydrate_index(full#1)>{str(para_owner.rehydrate_index)}")
            estimated_column_number = 0

            image_alt_text, token_prefix = (
                ParserHelper.calculate_last_line(image_alt_text),
                2,
            )
        newline_count = ParserHelper.count_newlines_in_text(
            previous_inline_token.ex_label
        )
        if newline_count:
            estimated_line_number += newline_count
            if para_owner:
                para_owner.rehydrate_index += newline_count
                print(f"rehydrate_index(full#2)>{str(para_owner.rehydrate_index)}")
            estimated_column_number = 0

            image_alt_text, token_prefix = (
                ParserHelper.calculate_last_line(previous_inline_token.ex_label),
                0,
            )

        print(f">>image_alt_text>>{ParserHelper.make_value_visible(image_alt_text)}")
        print(f">>label_data>>{ParserHelper.make_value_visible(label_data)}")

        if token_prefix:
            estimated_column_number += token_prefix + len(label_data)
        estimated_column_number += 2 + len(image_alt_text)
    return estimated_line_number, estimated_column_number


# pylint: enable=too-many-locals, too-many-branches, too-many-statements


def __verify_next_inline_autolink(
    previous_inline_token, estimated_line_number, estimated_column_number
):
    return (
        estimated_line_number,
        estimated_column_number + len(previous_inline_token.autolink_text) + 2,
    )


def __verify_next_inline_raw_html(
    last_token,
    previous_inline_token,
    estimated_line_number,
    estimated_column_number,
    link_stack,
):

    delta_line_number, delta_column_number = ParserHelper.calculate_deltas(
        f"<{previous_inline_token.raw_tag}>"
    )
    estimated_column_number = (
        -delta_column_number
        if delta_column_number < 0
        else estimated_column_number + delta_column_number
    )
    if last_token.is_paragraph and not link_stack:
        last_token.rehydrate_index += delta_line_number
    return estimated_line_number + delta_line_number, estimated_column_number


# pylint: disable=unused-argument,too-many-arguments
def __verify_next_inline_hard_break(
    last_token,
    previous_inline_token,
    current_inline_token,
    estimated_line_number,
    estimated_column_number,
    link_stack,
):
    _ = (previous_inline_token, estimated_column_number)

    new_column_number = 1
    if last_token.is_paragraph:
        split_whitespace = last_token.extracted_whitespace.split(
            ParserHelper.newline_character
        )
        ws_for_new_line = split_whitespace[last_token.rehydrate_index]
        if not link_stack:
            last_token.rehydrate_index += 1
        print(
            f"rehydrate_index(__verify_next_inline_hard_break)>{str(last_token.rehydrate_index)}"
        )
        new_column_number += len(ws_for_new_line)

    elif last_token.is_setext_heading:
        assert current_inline_token.is_text
        # assert (
        #    current_inline_token.token_text
        #    and current_inline_token.token_text[0] == ParserHelper.newline_character
        # )
        # assert (
        #    current_inline_token.end_whitespace
        #    and current_inline_token.end_whitespace[0] == ParserHelper.newline_character
        # )
        print(
            f"previous_inline_token>{ParserHelper.make_value_visible(previous_inline_token)}<"
        )
        print(
            f"current_inline_token>{ParserHelper.make_value_visible(current_inline_token)}<"
        )
        end_ws = current_inline_token.end_whitespace
        print(f"current_inline_token>{ParserHelper.make_value_visible(end_ws)}<")

        ws_for_new_line = ""
        if end_ws is not None:
            split_whitespace = current_inline_token.end_whitespace.split(
                ParserHelper.newline_character
            )

            print(
                f"split_whitespace>{ParserHelper.make_value_visible(split_whitespace)}<"
            )
            if len(split_whitespace) >= 2:
                ws_for_new_line = split_whitespace[1]
            else:
                ws_for_new_line = split_whitespace[0]
            if ws_for_new_line.endswith(ParserHelper.whitespace_split_character):
                ws_for_new_line = ws_for_new_line[0:-1]
            print(
                f"ws_for_new_line>{ParserHelper.make_value_visible(ws_for_new_line)}<"
            )

        new_column_number += len(ws_for_new_line)
    return estimated_line_number + 1, new_column_number


# pylint: enable=unused-argument,too-many-arguments


def __verify_next_inline_code_span(
    last_token,
    previous_inline_token,
    estimated_line_number,
    estimated_column_number,
    link_stack,
):

    resolved_leading_whitespace, resolved_span_text, resolved_trailing_whitespace = (
        ParserHelper.remove_all_from_text(previous_inline_token.leading_whitespace),
        ParserHelper.remove_all_from_text(previous_inline_token.span_text),
        ParserHelper.remove_all_from_text(previous_inline_token.trailing_whitespace),
    )

    print(
        f"here>>resolved_leading_whitespace>>{ParserHelper.make_value_visible(resolved_leading_whitespace)}<<"
    )
    print(
        f"here>>resolved_span_text>>{ParserHelper.make_value_visible(resolved_span_text)}<<"
    )
    print(
        f"here>>trailing_ws>>{ParserHelper.make_value_visible(resolved_trailing_whitespace)}<<"
    )

    delta_line_number, delta_column_number = ParserHelper.calculate_deltas(
        f"{previous_inline_token.extracted_start_backticks}{resolved_leading_whitespace}{resolved_span_text}{resolved_trailing_whitespace}{previous_inline_token.extracted_start_backticks}"
    )
    if last_token.is_paragraph and not link_stack:
        last_token.rehydrate_index += delta_line_number
    return (
        estimated_line_number + delta_line_number,
        -delta_column_number
        if delta_column_number < 0
        else estimated_column_number + delta_column_number,
    )


def __verify_next_inline_emphasis_start(
    previous_inline_token,
    estimated_line_number,
    estimated_column_number,
):
    return (
        estimated_line_number,
        estimated_column_number + previous_inline_token.emphasis_length,
    )


def __verify_next_inline_emphasis_end(
    previous_inline_token,
    estimated_line_number,
    estimated_column_number,
):
    return estimated_line_number, estimated_column_number + (
        previous_inline_token.start_markdown_token.emphasis_length
    )


def __create_newline_tuple():

    newline_pattern_list = [
        "\a&NewLine;\a",
        "\a&#xa;\a",
        "\a&#xA;\a",
        "\a&#Xa;\a",
        "\a&#XA;\a",
    ]

    prefix = ""
    while (1 + len(prefix)) <= 6:
        prefix += "0"
        newline_pattern_list.append("\a&#x" + prefix + "a;\a")
        newline_pattern_list.append("\a&#x" + prefix + "A;\a")
        newline_pattern_list.append("\a&#X" + prefix + "a;\a")
        newline_pattern_list.append("\a&#X" + prefix + "A;\a")

    prefix = ""
    newline_pattern_list.append("\a&#10;\a")
    while (2 + len(prefix)) <= 7:
        prefix += "0"
        newline_pattern_list.append("\a&#" + prefix + "10;\a")

    return tuple(newline_pattern_list)


def __handle_newline_character_entity_split(split_current_line):

    try_again = True
    while try_again:
        try_again = False
        for search_index in range(1, len(split_current_line)):
            print(f">>search_index>>{str(search_index)}")
            if split_current_line[search_index].startswith("\a") and split_current_line[
                search_index - 1
            ].endswith(__create_newline_tuple()):
                combined_line = f"{split_current_line[search_index - 1]}{ParserHelper.newline_character}{split_current_line[search_index]}"
                split_current_line[search_index - 1] = combined_line
                del split_current_line[search_index]
                try_again = True
                break
    return split_current_line


# pylint: disable=too-many-statements, too-many-arguments
def __verify_next_inline_text(
    last_token,
    pre_previous_inline_token,
    previous_inline_token,
    estimated_line_number,
    estimated_column_number,
    link_stack,
):
    current_line = previous_inline_token.token_text
    if not pre_previous_inline_token and last_token.is_atx_heading:
        pass
    else:
        current_line = f"{previous_inline_token.extracted_whitespace}{current_line}"

    print(f"last_token>{ParserHelper.make_value_visible(last_token)}<")
    split_extracted_whitespace, split_end_whitespace = None, None
    if last_token:
        if last_token.is_paragraph:
            print(
                f"last_token.rehydrate_index>{ParserHelper.make_value_visible(last_token.rehydrate_index)}<"
            )
            split_extracted_whitespace = last_token.extracted_whitespace.split(
                ParserHelper.newline_character
            )
            print(
                f"split_extracted_whitespace>{ParserHelper.make_value_visible(split_extracted_whitespace)}<"
            )
        elif last_token.is_setext_heading and previous_inline_token.end_whitespace:
            split_end_whitespace = ParserHelper.calculate_last_line(
                previous_inline_token.end_whitespace
            )

            if split_end_whitespace:
                assert split_end_whitespace[-1] == "\x02"
                split_end_whitespace = split_end_whitespace[0:-1]
                print(
                    f"split_end_whitespace>{ParserHelper.make_value_visible(split_end_whitespace)}<"
                )
                split_end_whitespace = len(split_end_whitespace)
                print(
                    f"split_end_whitespace>{ParserHelper.make_value_visible(split_end_whitespace)}<"
                )

    split_current_line = current_line.split(ParserHelper.newline_character)
    print(f"split_current_line>{ParserHelper.make_value_visible(split_current_line)}<")
    split_current_line = __handle_newline_character_entity_split(split_current_line)
    print(f"split_current_line>{ParserHelper.make_value_visible(split_current_line)}<")

    delta_line = len(split_current_line) - 1

    if split_extracted_whitespace and last_token.rehydrate_index < len(
        split_extracted_whitespace
    ):
        rehydrate_index = last_token.rehydrate_index
        print(f"rehydrate_index(__verify_next_inline_text)>{str(rehydrate_index)}")
        for next_line_index in range(1, len(split_current_line)):
            combined_index = next_line_index - 1 + rehydrate_index
            print(f"combined_index:{str(combined_index)}")
            print(
                f"split_extracted_whitespace[{str(combined_index)}]>{ParserHelper.make_value_visible(split_extracted_whitespace[combined_index])}<"
            )
            print(
                f"split_current_line[{str(next_line_index)}]>{ParserHelper.make_value_visible(split_current_line[next_line_index])}<"
            )
            split_current_line[
                next_line_index
            ] = f"{split_extracted_whitespace[combined_index]}{split_current_line[next_line_index]}"
            print(f">>link_stack={ParserHelper.make_value_visible(link_stack)}")
            if not link_stack:
                last_token.rehydrate_index += 1
            print(
                f"rehydrate_index(__verify_next_inline_text#2)>{str(last_token.rehydrate_index)}"
            )
        print(
            f"split_current_line>{ParserHelper.make_value_visible(split_current_line)}<"
        )

    split_current_line = split_current_line[-1]
    print(f"split_current_line>{ParserHelper.make_value_visible(split_current_line)}<")
    split_current_line = ParserHelper.remove_all_from_text(split_current_line)
    print(f"split_current_line>{ParserHelper.make_value_visible(split_current_line)}<")
    delta_column = len(split_current_line)

    if delta_line:
        estimated_column_number = 1
    estimated_column_number += delta_column
    if split_end_whitespace:
        estimated_column_number += split_end_whitespace
    return estimated_line_number + delta_line, estimated_column_number


# pylint: enable=too-many-statements, too-many-arguments


def __handle_last_token_text(
    last_block_token,
    second_last_inline_token,
    current_token,
    last_inline_token,
):
    _ = second_last_inline_token

    resolved_text = ParserHelper.remove_all_from_text(last_inline_token.token_text)

    if last_block_token.is_paragraph:
        inline_height = ParserHelper.count_newlines_in_text(resolved_text)
        print(
            f"last_block_token.rehydrate_index>>{str(last_block_token.rehydrate_index)}"
        )
        last_block_token.rehydrate_index += inline_height
        print(
            f"rehydrate_index(__handle_last_token_text)>>{str(last_block_token.rehydrate_index)}"
        )
        print(
            f"last_block_token.extracted_whitespace>>{ParserHelper.make_value_visible(last_block_token.extracted_whitespace)}"
        )
        num_newlines = ParserHelper.count_newlines_in_text(
            last_block_token.extracted_whitespace
        )
        print(f"num_newlines>>{str(num_newlines)}")
        if last_block_token.rehydrate_index > 1:
            assert last_block_token.rehydrate_index == (
                num_newlines + 1
            ), f"rehydrate_index ({str(last_block_token.rehydrate_index)}) != num_newlines({str(num_newlines)} + 1)"

    elif (
        last_block_token.is_html_block
        or last_block_token.is_indented_code_block
        or last_block_token.is_atx_heading
    ):
        inline_height = ParserHelper.count_newlines_in_text(resolved_text)
    elif last_block_token.is_fenced_code_block:
        inline_height = ParserHelper.count_newlines_in_text(resolved_text)
        if current_token:
            assert current_token.is_fenced_code_block_end
            if not current_token.was_forced:
                inline_height += 1
    else:
        assert (
            last_block_token.is_setext_heading
        ), f"bad block token: {str(last_block_token)}"
        inline_height = ParserHelper.count_newlines_in_text(resolved_text) + 1
    return inline_height


# pylint: disable=unused-argument
def __handle_last_token_end_link(
    last_block_token,
    second_last_inline_token,
    current_token,
    last_inline_token,
):
    _ = (second_last_inline_token, current_token)

    assert last_inline_token.start_markdown_token
    use_line_number_from_start_token = True

    inline_height = ParserHelper.count_newlines_in_texts(
        last_inline_token.start_markdown_token.text_from_blocks,
        last_inline_token.start_markdown_token.ex_label,
        last_inline_token.start_markdown_token.before_link_whitespace,
        last_inline_token.start_markdown_token.before_title_whitespace,
        last_inline_token.start_markdown_token.after_title_whitespace,
    )
    if last_inline_token.start_markdown_token.label_type != "shortcut":
        link_title = last_inline_token.start_markdown_token.active_link_title
        inline_height += ParserHelper.count_newlines_in_text(link_title)

    return (
        inline_height + 1 if last_block_token.is_setext_heading else inline_height,
        use_line_number_from_start_token,
    )


# pylint: enable=unused-argument


# pylint: disable=unused-argument
def __handle_last_token_image(
    last_block_token,
    second_last_inline_token,
    current_token,
    last_inline_token,
):
    _ = (second_last_inline_token, current_token)

    inline_height = ParserHelper.count_newlines_in_texts(
        last_inline_token.ex_label
        if last_inline_token.ex_label
        else last_inline_token.image_alt_text,
        last_inline_token.active_link_uri,
        last_inline_token.active_link_title,
        last_inline_token.before_link_whitespace,
        last_inline_token.before_title_whitespace,
        last_inline_token.after_title_whitespace,
    )
    if last_inline_token.label_type == "full":
        inline_height += ParserHelper.count_newlines_in_text(
            last_inline_token.text_from_blocks
        )

    return inline_height + 1 if last_block_token.is_setext_heading else inline_height


# pylint: enable=unused-argument


# pylint: disable=unused-argument
def __handle_last_token_code_span(
    last_block_token,
    second_last_inline_token,
    current_token,
    last_inline_token,
):
    _ = (second_last_inline_token, current_token)

    inline_height = ParserHelper.count_newlines_in_texts(
        last_inline_token.span_text,
        last_inline_token.leading_whitespace,
        last_inline_token.trailing_whitespace,
    )

    return inline_height + 1 if last_block_token.is_setext_heading else inline_height


# pylint: enable=unused-argument


# pylint: disable=unused-argument
def __handle_last_token_autolink(
    last_block_token,
    second_last_inline_token,
    current_token,
    last_inline_token,
):
    _ = (second_last_inline_token, current_token, last_inline_token)

    return 1 if last_block_token.is_setext_heading else 0


# pylint: enable=unused-argument


# pylint: disable=unused-argument
def __handle_last_token_raw_html(
    last_block_token,
    second_last_inline_token,
    current_token,
    last_inline_token,
):
    _ = (second_last_inline_token, current_token)

    inline_height = ParserHelper.count_newlines_in_text(last_inline_token.raw_tag)
    return inline_height + 1 if last_block_token.is_setext_heading else inline_height


# pylint: enable=unused-argument


# pylint: disable=unused-argument
def __handle_last_token_end_emphasis(
    last_block_token,
    second_last_inline_token,
    current_token,
    last_inline_token,
):
    _ = (last_block_token, second_last_inline_token, last_inline_token)

    return 1 if current_token and current_token.is_setext_heading_end else 0


# pylint: enable=unused-argument


# pylint: disable=unused-argument
def __handle_last_token_blank_line(
    last_block_token,
    second_last_inline_token,
    current_token,
    last_inline_token,
    current_block_token,
):
    _ = second_last_inline_token

    inline_height = 1
    print(f">>>last_block_token>{str(last_block_token)}")
    print(f">>>current_block_token>{str(current_block_token)}")
    print(f">>>last_inline_token>{str(last_inline_token)}")
    print(f">>>current_token>{str(current_token)}")

    if (
        last_block_token.is_fenced_code_block
        and current_block_token
        and current_block_token.is_blank_line
    ):
        inline_height -= 1
    elif (
        last_block_token.is_fenced_code_block
        and not current_block_token
        and last_inline_token
        and last_inline_token.is_blank_line
    ):
        assert current_token.is_fenced_code_block_end
        if current_token.was_forced:
            inline_height -= 1
    return inline_height


# pylint: enable=unused-argument


# pylint: disable=too-many-arguments
def __verify_last_inline(
    last_block_token,
    current_block_token,
    last_inline_token,
    second_last_inline_token,
    removed_end_token,
    expected_end_line_number,
):
    """
    Verify the last inline against the next block token.
    """

    print("---\n__verify_last_inline\n---")
    print(f"last_block_token>>{ParserHelper.make_value_visible(last_block_token)}")
    print(
        f"current_block_token>>{ParserHelper.make_value_visible(current_block_token)}"
    )
    print(
        f"second_last_inline_token>>{ParserHelper.make_value_visible(second_last_inline_token)}"
    )
    print(f"removed_end_token>>{ParserHelper.make_value_visible(removed_end_token)}")
    print(f"last_inline_token>>{ParserHelper.make_value_visible(last_inline_token)}")
    print(
        f"expected_end_line_number>>{ParserHelper.make_value_visible(expected_end_line_number)}"
    )

    use_line_number_from_start_token = False
    if last_inline_token.is_text:
        inline_height = __handle_last_token_text(
            last_block_token,
            second_last_inline_token,
            removed_end_token,
            last_inline_token,
        )
    elif last_inline_token.is_inline_link_end:
        inline_height, use_line_number_from_start_token = __handle_last_token_end_link(
            last_block_token,
            second_last_inline_token,
            removed_end_token,
            last_inline_token,
        )

    elif last_inline_token.is_inline_image:
        inline_height = __handle_last_token_image(
            last_block_token,
            second_last_inline_token,
            removed_end_token,
            last_inline_token,
        )

    elif last_inline_token.is_inline_code_span:
        inline_height = __handle_last_token_code_span(
            last_block_token,
            second_last_inline_token,
            removed_end_token,
            last_inline_token,
        )
    elif last_inline_token.is_inline_raw_html:
        inline_height = __handle_last_token_raw_html(
            last_block_token,
            second_last_inline_token,
            removed_end_token,
            last_inline_token,
        )
    elif last_inline_token.is_inline_autolink:
        inline_height = __handle_last_token_autolink(
            last_block_token,
            second_last_inline_token,
            removed_end_token,
            last_inline_token,
        )
    elif last_inline_token.is_inline_emphasis_end:
        inline_height = __handle_last_token_end_emphasis(
            last_block_token,
            second_last_inline_token,
            removed_end_token,
            last_inline_token,
        )
    else:
        assert (
            last_inline_token.is_blank_line
        ), f"bad inline token: {str(last_inline_token)}"
        inline_height = __handle_last_token_blank_line(
            last_block_token,
            second_last_inline_token,
            removed_end_token,
            last_inline_token,
            current_block_token,
        )

    print(f"inline_height>>{ParserHelper.make_value_visible(inline_height)}")
    if use_line_number_from_start_token:
        print(
            f"last_inline_token.start_markdown_token.line_number>>{ParserHelper.make_value_visible(last_inline_token.start_markdown_token.line_number)}"
        )
        inline_end_line_number = (
            last_inline_token.start_markdown_token.line_number + inline_height
        )
    else:
        print(
            f"last_inline_token.line_number>>{ParserHelper.make_value_visible(last_inline_token.line_number)}"
        )
        inline_end_line_number = last_inline_token.line_number + inline_height
    assert (
        inline_end_line_number == expected_end_line_number
    ), f"Expected line number '{str(expected_end_line_number)}' does not equal computed line number '{str(inline_end_line_number)}'."


# pylint: enable=too-many-arguments

# pylint: disable=too-many-branches, too-many-arguments, too-many-statements, too-many-locals, too-many-nested-blocks
def __verify_inline(  # noqa: C901
    actual_tokens,
    last_block_token,
    block_token_index,
    current_block_token,
    last_token_stack,
    number_of_lines,
):
    """
    Validate the inline tokens between block tokens.
    """

    print(f"\n\n>>__verify_inline:{ParserHelper.make_value_visible(last_block_token)}")

    print(f">>last_block_token:{ParserHelper.make_value_visible(last_block_token)}")
    print(
        f">>current_block_token:{ParserHelper.make_value_visible(current_block_token)}"
    )
    next_token_index = block_token_index + 1
    inline_tokens = []
    while (
        next_token_index < len(actual_tokens)
        and actual_tokens[next_token_index] != current_block_token
    ):
        inline_tokens.append(actual_tokens[next_token_index])
        next_token_index += 1

    # TODO does this need repeating for deeper nesting?
    while len(inline_tokens) >= 2 and (
        inline_tokens[-1].is_list_end or inline_tokens[-1].is_block_quote_end
    ):
        del inline_tokens[-1]

    if inline_tokens and (
        inline_tokens[-1].is_list_end or inline_tokens[-1].is_block_quote_end
    ):
        del inline_tokens[-1]

    removed_end_token = None
    if (
        inline_tokens
        and inline_tokens[-1].is_end_token
        and inline_tokens[-1].type_name == last_block_token.token_name
    ):
        removed_end_token = inline_tokens[-1]
        print(f"removed_end_token>{str(removed_end_token)}")
        del inline_tokens[-1]

    if last_block_token.is_paragraph:
        last_block_token.rehydrate_index = 1
        print(f"rehydrate_index(start#1)>>{str(last_block_token.rehydrate_index)}")

    if inline_tokens:
        print(f">inline_tokens>{ParserHelper.make_value_visible(inline_tokens)}")
        link_stack = []
        for token_index, current_inline_token in enumerate(inline_tokens):
            print(
                f"{str(token_index)}-token:{ParserHelper.make_value_visible(current_inline_token)}"
            )
            print(f"  links:{ParserHelper.make_value_visible(link_stack)}")
            print(">>>>>>")
            if not token_index:
                __verify_first_inline(
                    last_block_token, current_inline_token, last_token_stack
                )
            else:
                pre_last_token = (
                    inline_tokens[token_index - 2] if token_index >= 2 else None
                )
                __verify_next_inline(
                    last_block_token,
                    pre_last_token,
                    inline_tokens[token_index - 1],
                    current_inline_token,
                    link_stack,
                    inline_tokens,
                    token_index,
                )

            print("<<<<<<")
            if current_inline_token.is_inline_link:
                link_stack.append(current_inline_token)
            elif current_inline_token.is_inline_link_end:
                del link_stack[-1]
            elif link_stack and last_block_token.is_paragraph:
                print(
                    f"inside link: {ParserHelper.make_value_visible(current_inline_token)}"
                )
                if ParserHelper.newline_character in str(current_inline_token):
                    if current_inline_token.is_inline_code_span:
                        # Don't need to resolve replacement characters as the & in
                        # the replacement is changed to an &amp; + the rest.
                        newlines_in_text_token = ParserHelper.count_newlines_in_text(
                            current_inline_token.span_text
                        )
                        last_block_token.rehydrate_index += newlines_in_text_token
                        print(
                            f"rehydrate_index(start#2)>>{str(last_block_token.rehydrate_index)}"
                        )
                    elif current_inline_token.is_inline_raw_html:
                        # Don't need to resolve replacement characters as the & in
                        # the replacement and following characters are not interpretted.
                        newlines_in_text_token = ParserHelper.count_newlines_in_text(
                            current_inline_token.raw_tag
                        )
                        last_block_token.rehydrate_index += newlines_in_text_token
                        print(
                            f"rehydrate_index(start#3)>>{str(last_block_token.rehydrate_index)}"
                        )
                    elif current_inline_token.is_inline_image:
                        pass
                    elif current_inline_token.is_inline_hard_break:
                        if not link_stack:
                            last_block_token.rehydrate_index += 1
                    else:
                        assert (
                            current_inline_token.is_text
                        ), ParserHelper.make_value_visible(current_inline_token)
                        print(
                            f"current_inline_token.token_text>>{ParserHelper.make_value_visible(current_inline_token.token_text)}"
                        )

                        token_text = ParserHelper.remove_all_from_text(
                            current_inline_token.token_text
                        )
                        print(
                            f"token_text>>{ParserHelper.make_value_visible(token_text)}"
                        )

                        newlines_in_text_token = ParserHelper.count_newlines_in_text(
                            token_text
                        )
                        print(f"newlines_in_text_token>>{str(newlines_in_text_token)}")
                        last_block_token.rehydrate_index += newlines_in_text_token
                        print(
                            f"rehydrate_index(start#4)>>{str(last_block_token.rehydrate_index)}"
                        )

        assert not link_stack

        second_last_inline_token = inline_tokens[-2] if len(inline_tokens) > 1 else None

        if number_of_lines is None:
            assert current_block_token
            if current_block_token.is_setext_heading:
                number_of_lines = current_block_token.original_line_number - 1
                print(f"number_of_lines from setext>{str(number_of_lines)}")
            else:
                number_of_lines = current_block_token.line_number - 1
                print(f"number_of_lines from normal>{str(number_of_lines)}")
        else:
            print(f"number_of_lines is not None>{str(number_of_lines)}")
            assert not current_block_token

        last_inline_token = inline_tokens[-1]
        __verify_last_inline(
            last_block_token,
            current_block_token,
            last_inline_token,
            second_last_inline_token,
            removed_end_token,
            number_of_lines,
        )

    if next_token_index < len(actual_tokens):
        print(
            f"<<current_block_token:{ParserHelper.make_value_visible(current_block_token)}"
        )
    else:
        print("<<[EOL]")
    print("<<__verify_inline\n\n")


# pylint: enable=too-many-branches, too-many-arguments, too-many-statements, too-many-locals, too-many-nested-blocks
