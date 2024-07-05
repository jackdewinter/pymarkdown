"""
Module to provide transformations for containers.
"""

import logging
from dataclasses import dataclass
from typing import List, Optional, Tuple, cast

from pymarkdown.general.parser_helper import ParserHelper
from pymarkdown.general.parser_logger import ParserLogger
from pymarkdown.tokens.block_quote_markdown_token import BlockQuoteMarkdownToken
from pymarkdown.tokens.list_start_markdown_token import ListStartMarkdownToken
from pymarkdown.tokens.markdown_token import EndMarkdownToken, MarkdownToken

POGGER = ParserLogger(logging.getLogger(__name__))


@dataclass
class MarkdownChangeRecord:
    """
    Class to keep track of changes.
    """

    item_a: bool
    item_b: int
    item_c: MarkdownToken
    item_d: Optional[EndMarkdownToken]


# pylint: disable=too-few-public-methods
class TransformContainers:
    """
    Class to provide transformations for containers.
    """

    # pylint: disable=too-many-arguments
    @staticmethod
    def handle_current_token(
        current_token: MarkdownToken,
        transformed_data: str,
        container_stack: List[MarkdownToken],
        container_records: List[MarkdownChangeRecord],
        transformed_data_length_before_add: int,
        actual_tokens: List[MarkdownToken],
    ) -> str:
        """
        Handle the current token as far as it concerns any containers.
        """
        if (
            current_token.is_block_quote_start
            or current_token.is_list_start
            or current_token.is_new_list_item
        ):
            TransformContainers.__transform_container_start(
                container_stack,
                container_records,
                transformed_data_length_before_add,
                current_token,
            )
        elif current_token.is_block_quote_end or current_token.is_list_end:
            transformed_data = TransformContainers.__transform_container_end(
                container_stack,
                container_records,
                current_token,
                transformed_data,
                actual_tokens,
            )
        return transformed_data

    # pylint: enable=too-many-arguments

    @staticmethod
    def __transform_container_start(
        container_stack: List[MarkdownToken],
        container_records: List[MarkdownChangeRecord],
        transformed_data_length_before_add: int,
        current_token: MarkdownToken,
    ) -> None:
        if not container_stack:
            container_records.clear()
        container_stack.append(current_token)
        record_item = MarkdownChangeRecord(
            True, transformed_data_length_before_add, current_token, None
        )
        container_records.append(record_item)
        # POGGER.debug("START:" + ParserHelper.make_value_visible(current_token))
        # POGGER.debug(">>" + ParserHelper.make_value_visible(container_stack))
        # POGGER.debug(">>" + ParserHelper.make_value_visible(container_records))

    @staticmethod
    def __transform_container_end(
        container_stack: List[MarkdownToken],
        container_records: List[MarkdownChangeRecord],
        current_token: MarkdownToken,
        transformed_data: str,
        actual_tokens: List[MarkdownToken],
    ) -> str:
        current_end_token = cast(EndMarkdownToken, current_token)
        POGGER.debug(
            f"END:{ParserHelper.make_value_visible(current_end_token.start_markdown_token)}"
        )
        while container_stack[-1].is_new_list_item:
            del container_stack[-1]
        assert str(container_stack[-1]) == str(
            current_end_token.start_markdown_token
        ), (
            ParserHelper.make_value_visible(container_stack[-1])
            + "=="
            + ParserHelper.make_value_visible(current_end_token.start_markdown_token)
        )
        del container_stack[-1]
        record_item = MarkdownChangeRecord(
            False,
            len(transformed_data),
            current_end_token.start_markdown_token,
            current_end_token,
        )
        container_records.append(record_item)
        POGGER.debug(f">>{ParserHelper.make_value_visible(container_stack)}")
        POGGER.debug(f">>{ParserHelper.make_value_visible(container_records)}")

        if not container_stack:
            record_item = container_records[0]
            pre_container_text = transformed_data[: record_item.item_b]
            container_text = transformed_data[record_item.item_b :]
            adjusted_text = TransformContainers.__apply_container_transformation(
                container_text, container_records, actual_tokens
            )
            POGGER.debug(f"pre>:{pre_container_text}:<")
            POGGER.debug(f"adj>:{adjusted_text}:<")
            transformed_data = pre_container_text + adjusted_text
            POGGER.debug(f"trn>:{transformed_data}:<")
        return transformed_data

    # pylint: disable=too-many-locals
    @staticmethod
    def __apply_container_transformation(
        container_text: str,
        container_records: List[MarkdownChangeRecord],
        actual_tokens: List[MarkdownToken],
    ) -> str:
        POGGER.debug(
            f">>incoming>>:{ParserHelper.make_value_visible(container_text)}:<<"
        )

        POGGER.debug(
            f">>container_records>>{ParserHelper.make_value_visible(container_records)}"
        )

        token_stack: List[MarkdownToken] = []
        container_token_indices: List[int] = []
        (
            base_line_number,
            delta_line,
            split_container_text,
            transformed_parts,
            record_index,
            container_text_index,
            current_changed_record,
        ) = (
            container_records[0].item_c.line_number,
            0,
            container_text.split(ParserHelper.newline_character),
            [],
            -1,
            container_records[0].item_b,
            None,
        )
        POGGER.debug(
            ">>split_container_text>>"
            + ParserHelper.make_value_visible(split_container_text)
        )

        for container_line in split_container_text:  # pragma: no cover
            container_line_length = len(container_line)
            # POGGER.debug(
            #     ParserHelper.newline_character
            #     + str(delta_line)
            #     + "("
            #     + str(base_line_number + delta_line)
            #     + ")>>container_line>>"
            #     + str(container_text_index)
            #     + "-"
            #     + str(container_text_index + container_line_length)
            #     + ":>:"
            #     + ParserHelper.make_value_visible(container_line)
            #     + ":<"
            # )

            old_record_index = record_index
            (
                record_index,
                did_move_ahead,
                current_changed_record,
                removed_tokens,
            ) = TransformContainers.__move_to_current_record(
                old_record_index,
                container_records,
                container_text_index,
                token_stack,
                container_token_indices,
                container_line_length,
            )

            if not container_token_indices:
                transformed_parts.append(container_line)
                break

            (
                last_container_token_index,
                applied_leading_spaces_to_start_of_container_line,
                container_line,
                was_abrupt_block_quote_end,
            ) = TransformContainers.__apply_primary_transformation(
                did_move_ahead,
                token_stack,
                container_token_indices,
                current_changed_record,
                container_line,
                actual_tokens,
            )

            container_line = TransformContainers.__adjust_for_list(
                token_stack,
                applied_leading_spaces_to_start_of_container_line,
                container_token_indices,
                container_line,
                removed_tokens,
            )
            container_line = TransformContainers.__adjust_for_block_quote(
                token_stack,
                container_line,
                container_token_indices,
                base_line_number + delta_line,
            )

            TransformContainers.__adjust_state_for_element(
                token_stack,
                container_token_indices,
                did_move_ahead,
                current_changed_record,
                last_container_token_index,
                was_abrupt_block_quote_end,
            )

            transformed_parts.append(container_line)
            container_text_index += container_line_length + 1
            delta_line += 1

        POGGER.debug(
            "\n<<transformed<<" + ParserHelper.make_value_visible(transformed_parts)
        )
        return ParserHelper.newline_character.join(transformed_parts)

    # pylint: enable=too-many-locals

    # pylint: disable=too-many-arguments
    @staticmethod
    def __move_to_current_record(
        old_record_index: int,
        container_records: List[MarkdownChangeRecord],
        container_text_index: int,
        token_stack: List[MarkdownToken],
        container_token_indices: List[int],
        container_line_length: int,
    ) -> Tuple[int, bool, Optional[MarkdownChangeRecord], List[MarkdownToken]]:
        record_index, current_changed_record, did_move_ahead = (
            old_record_index,
            None,
            False,
        )

        POGGER.debug(f"({container_text_index})")
        POGGER.debug(
            "("
            + str(record_index + 1)
            + "):"
            + ParserHelper.make_value_visible(container_records[1])
        )
        while record_index + 1 < len(container_records) and container_records[
            record_index + 1
        ].item_b <= (container_text_index + container_line_length):
            record_index += 1
        POGGER.debug(
            "("
            + str(record_index + 1)
            + "):"
            + ParserHelper.make_value_visible(container_records[1])
        )
        removed_tokens: List[MarkdownToken] = []
        while old_record_index != record_index:
            (
                old_record_index,
                did_move_ahead,
                current_changed_record,
            ) = TransformContainers.__manage_records(
                container_records,
                old_record_index,
                token_stack,
                container_token_indices,
                removed_tokens,
            )

        POGGER.debug(
            f"   removed_tokens={ParserHelper.make_value_visible(removed_tokens)}"
        )
        return record_index, did_move_ahead, current_changed_record, removed_tokens

    # pylint: enable=too-many-arguments

    @staticmethod
    def __manage_records(
        container_records: List[MarkdownChangeRecord],
        old_record_index: int,
        token_stack: List[MarkdownToken],
        container_token_indices: List[int],
        removed_tokens: List[MarkdownToken],
    ) -> Tuple[int, bool, MarkdownChangeRecord]:
        did_move_ahead, current_changed_record = (
            True,
            container_records[old_record_index + 1],
        )
        POGGER.debug(
            "   current_changed_record("
            + str(old_record_index + 1)
            + ")-->"
            + ParserHelper.make_value_visible(current_changed_record)
        )
        if current_changed_record.item_a:
            token_stack.append(current_changed_record.item_c)
            container_token_indices.append(0)
        else:
            POGGER.debug(f"   -->{ParserHelper.make_value_visible(token_stack)}")
            POGGER.debug(
                f"   -->{ParserHelper.make_value_visible(container_token_indices)}"
            )

            if token_stack[-1].is_new_list_item:
                removed_tokens.append(token_stack[-1])
                del token_stack[-1]
                del container_token_indices[-1]

            assert str(current_changed_record.item_c) == str(token_stack[-1]), (
                "end:"
                + ParserHelper.make_value_visible(current_changed_record.item_c)
                + "!="
                + ParserHelper.make_value_visible(token_stack[-1])
            )
            removed_tokens.append(token_stack[-1])
            del token_stack[-1]
            del container_token_indices[-1]

        POGGER.debug(
            "   -->current_changed_recordx>"
            + ParserHelper.make_value_visible(current_changed_record)
        )
        POGGER.debug(f"   -->{ParserHelper.make_value_visible(token_stack)}")
        POGGER.debug(
            f"   -->{ParserHelper.make_value_visible(container_token_indices)}"
        )
        old_record_index += 1
        return old_record_index, did_move_ahead, current_changed_record

    # pylint: disable=too-many-arguments
    @staticmethod
    def __adjust_state_for_element(
        token_stack: List[MarkdownToken],
        container_token_indices: List[int],
        did_move_ahead: bool,
        current_changed_record: Optional[MarkdownChangeRecord],
        last_container_token_index: int,
        was_abrupt_block_quote_end: bool,
    ) -> None:
        if was_abrupt_block_quote_end:
            return
        POGGER.debug(f" -->{ParserHelper.make_value_visible(token_stack)}")
        POGGER.debug(f" -->{ParserHelper.make_value_visible(container_token_indices)}")
        did_change_to_list_token = (
            did_move_ahead
            and (current_changed_record is not None and current_changed_record.item_a)
            and (token_stack[-1].is_list_start or token_stack[-1].is_new_list_item)
        )

        # May need earlier if both new item and start of new list on same line
        if not did_change_to_list_token:
            container_token_indices[-1] = last_container_token_index + 1
        elif token_stack[-1].is_new_list_item:
            del token_stack[-1]
            del container_token_indices[-1]
        POGGER.debug(f" -->{ParserHelper.make_value_visible(token_stack)}")
        POGGER.debug(f" -->{ParserHelper.make_value_visible(container_token_indices)}")

    # pylint: enable=too-many-arguments

    @staticmethod
    def __adjust_for_block_quote(
        token_stack: List[MarkdownToken],
        container_line: str,
        container_token_indices: List[int],
        line_number: int,
    ) -> str:
        if not (len(token_stack) > 1 and token_stack[-1].is_block_quote_start):
            return container_line

        POGGER.debug(" looking for nested list start")
        nested_list_start_index = TransformContainers.__get_last_list_index(token_stack)
        POGGER.debug(f" afbq={len(token_stack) - 1}")
        POGGER.debug(f" nested_list_start_index={nested_list_start_index}")
        if nested_list_start_index == -1:
            POGGER.debug(" nope")
        elif (
            nested_list_start_index == len(token_stack) - 2
            and nested_list_start_index > 0
            and token_stack[-1].line_number == line_number
            and token_stack[nested_list_start_index - 1].is_block_quote_start
            and token_stack[-1].line_number != token_stack[-2].line_number
        ):
            container_line = TransformContainers.__adjust_for_block_quote_same_line(
                container_line,
                nested_list_start_index,
                token_stack,
                container_token_indices,
            )
        else:
            container_line = TransformContainers.__adjust_for_block_quote_previous_line(
                container_line,
                nested_list_start_index,
                token_stack,
                container_token_indices,
                line_number,
            )
        return container_line

    @staticmethod
    def __adjust_for_list(
        token_stack: List[MarkdownToken],
        applied_leading_spaces_to_start_of_container_line: bool,
        container_token_indices: List[int],
        container_line: str,
        removed_tokens: List[MarkdownToken],
    ) -> str:
        if (
            len(token_stack) > 1
            and token_stack[-1].is_list_start
            or token_stack[-1].is_new_list_item
        ):
            nested_block_start_index = (
                TransformContainers.__find_last_block_quote_on_stack(token_stack)
            )
            if nested_block_start_index != -1:
                POGGER.debug(f"nested_block_start_index>{nested_block_start_index}")
                previous_token = token_stack[nested_block_start_index]
                POGGER.debug(
                    f"previous={ParserHelper.make_value_visible(previous_token)}"
                )
                POGGER.debug(
                    " applied_leading_spaces_to_start_of_container_line->"
                    + str(applied_leading_spaces_to_start_of_container_line)
                )
                inner_token_index = container_token_indices[nested_block_start_index]
                POGGER.debug(
                    f"applied:{applied_leading_spaces_to_start_of_container_line} or "
                    + f"end.line:{token_stack[-1].line_number} != prev.line:{previous_token.line_number}"
                )

                container_line = TransformContainers.__adjust_for_list_end(
                    container_line,
                    token_stack,
                    removed_tokens,
                    applied_leading_spaces_to_start_of_container_line,
                    previous_token,
                    container_token_indices,
                    inner_token_index,
                    nested_block_start_index,
                )
        return container_line

    # pylint: disable=too-many-arguments
    @staticmethod
    def __adjust_for_list_end(
        container_line: str,
        token_stack: List[MarkdownToken],
        removed_tokens: List[MarkdownToken],
        applied_leading_spaces_to_start_of_container_line: bool,
        previous_token: MarkdownToken,
        container_token_indices: List[int],
        inner_token_index: int,
        nested_block_start_index: int,
    ) -> str:
        if TransformContainers.__adjust_for_list_check(
            token_stack,
            removed_tokens,
            applied_leading_spaces_to_start_of_container_line,
            previous_token,
        ):
            previous_block_token = cast(BlockQuoteMarkdownToken, previous_token)
            assert (
                previous_block_token.bleading_spaces is not None
            ), "Bleading spaces must be defined by this point."
            split_leading_spaces = previous_block_token.bleading_spaces.split(
                ParserHelper.newline_character
            )
            POGGER.debug(
                f"inner_token_index={inner_token_index} < len(split)={len(split_leading_spaces)}"
            )
            if inner_token_index < len(split_leading_spaces):
                POGGER.debug(
                    " adj-->container_line>:"
                    + ParserHelper.make_value_visible(container_line)
                    + ":<"
                )
                container_line = (
                    split_leading_spaces[inner_token_index] + container_line
                )
                POGGER.debug(
                    " adj-->container_line>:"
                    + ParserHelper.make_value_visible(container_line)
                    + ":<"
                )
        container_token_indices[nested_block_start_index] = inner_token_index + 1
        return container_line

    # pylint: enable=too-many-arguments
    @staticmethod
    def __adjust_for_list_check(
        token_stack: List[MarkdownToken],
        removed_tokens: List[MarkdownToken],
        applied_leading_spaces_to_start_of_container_line: bool,
        previous_token: MarkdownToken,
    ) -> bool:
        if not token_stack[-1].is_new_list_item:
            return (
                applied_leading_spaces_to_start_of_container_line
                or token_stack[-1].line_number != previous_token.line_number
            )
        new_list_item_adjust = True
        if len(removed_tokens) == 1 and removed_tokens[-1].is_block_quote_start:
            removed_block_token = cast(BlockQuoteMarkdownToken, removed_tokens[-1])
            assert (
                removed_block_token.bleading_spaces is not None
            ), "Bleading spaces must be defined by this point."
            leading_spaces_newline_count = removed_block_token.bleading_spaces.count(
                "\n"
            )
            block_quote_end_line = (
                leading_spaces_newline_count + removed_block_token.line_number
            )
            POGGER.debug(
                f"block_quote_end_line={block_quote_end_line} = "
                + f"fg={leading_spaces_newline_count} + "
                + f"line={removed_block_token.line_number}"
            )
            CHANGE_6 = True
            if CHANGE_6:
                weird_kludge_one_count = removed_tokens[-1].weird_kludge_one
                new_list_item_adjust = leading_spaces_newline_count > 1 and (
                    weird_kludge_one_count is None or weird_kludge_one_count <= 1
                )
            else:
                new_list_item_adjust = leading_spaces_newline_count > 1
            POGGER.debug(f"new_list_item_adjust:{new_list_item_adjust}")

        return (
            token_stack[-1].line_number != previous_token.line_number
            and new_list_item_adjust
        )

    @staticmethod
    def __find_last_block_quote_on_stack(token_stack: List[MarkdownToken]) -> int:
        POGGER.debug(" looking for nested block start")
        stack_index = len(token_stack) - 2
        nested_block_start_index = -1
        while stack_index >= 0:
            if token_stack[stack_index].is_block_quote_start:
                nested_block_start_index = stack_index
                break
            stack_index -= 1
        return nested_block_start_index

    @staticmethod
    def __adjust_for_block_quote_previous_line(
        container_line: str,
        nested_list_start_index: int,
        token_stack: List[MarkdownToken],
        container_token_indices: List[int],
        line_number: int,
    ) -> str:
        previous_token = token_stack[nested_list_start_index]
        # POGGER.debug(f"nested_list_start_index->{nested_list_start_index}")
        # POGGER.debug(f" yes->{ParserHelper.make_value_visible(previous_token)}")

        # POGGER.debug(f"token_stack[-1].line_number->{token_stack[-1].line_number}")
        # POGGER.debug(f"previous_token.line_number->{previous_token.line_number}")
        # POGGER.debug(f"line_number->{line_number}")
        if (
            token_stack[-1].line_number != previous_token.line_number
            or line_number != previous_token.line_number
        ):
            POGGER.debug("different line as list start")
            container_line = TransformContainers.__adjust(
                nested_list_start_index,
                token_stack,
                container_token_indices,
                container_line,
                False,
            )
        else:
            POGGER.debug("same line as list start")
            if nested_list_start_index > 0:
                next_level_index = nested_list_start_index - 1
                pre_previous_token = token_stack[next_level_index]
                # POGGER.debug(
                #     f" pre_previous_token->{ParserHelper.make_value_visible(pre_previous_token)}"
                # )
                if pre_previous_token.is_block_quote_start:
                    # sourcery skip: move-assign
                    different_line_prefix = TransformContainers.__adjust(
                        next_level_index,
                        token_stack,
                        container_token_indices,
                        "",
                        False,
                    )
                    # POGGER.debug(f"different_line_prefix>:{different_line_prefix}:<")
                    if pre_previous_token.line_number != previous_token.line_number:
                        container_line = different_line_prefix + container_line
        return container_line

    @staticmethod
    def __adjust_for_block_quote_same_line(
        container_line: str,
        nested_list_start_index: int,
        token_stack: List[MarkdownToken],
        container_token_indices: List[int],
    ) -> str:
        adj_line = ""
        POGGER.debug(f"adj_line->:{adj_line}:")
        adj_line = TransformContainers.__adjust(
            nested_list_start_index - 1,
            token_stack,
            container_token_indices,
            adj_line,
            True,
        )
        POGGER.debug(f"adj_line->:{adj_line}:")
        adj_line = TransformContainers.__adjust(
            nested_list_start_index,
            token_stack,
            container_token_indices,
            adj_line,
            True,
        )
        POGGER.debug(f"adj_line->:{adj_line}:")
        return adj_line + container_line

    # pylint: disable=too-many-arguments
    @staticmethod
    def __apply_primary_transformation(
        did_move_ahead: bool,
        token_stack: List[MarkdownToken],
        container_token_indices: List[int],
        current_changed_record: Optional[MarkdownChangeRecord],
        container_line: str,
        actual_tokens: List[MarkdownToken],
    ) -> Tuple[int, bool, str, bool]:
        POGGER.debug(
            f" -->did_move_ahead>{ParserHelper.make_value_visible(did_move_ahead)}"
        )
        POGGER.debug(f" -->{ParserHelper.make_value_visible(token_stack)}")
        POGGER.debug(f" -->{ParserHelper.make_value_visible(container_token_indices)}")
        POGGER.debug(
            f" -->current_changed_record>{ParserHelper.make_value_visible(current_changed_record)}"
        )

        is_list_start_after_two_block_starts = (
            TransformContainers.__apply_primary_transformation_start(
                current_changed_record, actual_tokens
            )
        )

        was_abrupt_block_quote_end = bool(
            current_changed_record
            and current_changed_record.item_d is not None
            and current_changed_record.item_d.is_block_quote_end
        )
        if was_abrupt_block_quote_end:
            assert (
                current_changed_record is not None
            ), "If an abrupt bq end, the change record must be defined."
            assert (
                current_changed_record.item_d is not None
            ), "If an abrupt bq end, the change record's item_d field must be defined."
            was_abrupt_block_quote_end = bool(
                current_changed_record.item_d.was_forced
                and current_changed_record.item_d.extra_end_data
                and ">" in current_changed_record.item_d.extra_end_data
            )

        applied_leading_spaces_to_start_of_container_line = (
            (
                not did_move_ahead
                or current_changed_record is None
                or not current_changed_record.item_a
            )
            and not is_list_start_after_two_block_starts
            and not was_abrupt_block_quote_end
        )

        last_container_token_index = container_token_indices[-1]
        if applied_leading_spaces_to_start_of_container_line:
            container_line = TransformContainers.__apply_primary_transformation_adjust_container_line(
                token_stack, last_container_token_index, container_line
            )
        return (
            last_container_token_index,
            applied_leading_spaces_to_start_of_container_line,
            container_line,
            was_abrupt_block_quote_end,
        )

    # pylint: enable=too-many-arguments

    @classmethod
    def __apply_primary_transformation_adjust_container_line(
        cls,
        token_stack: List[MarkdownToken],
        last_container_token_index: int,
        container_line: str,
    ) -> str:
        POGGER.debug(f" container->{ParserHelper.make_value_visible(token_stack[-1])}")
        tabbed_leading_space: Optional[str] = None
        if token_stack[-1].is_block_quote_start:
            prev_block_token = cast(BlockQuoteMarkdownToken, token_stack[-1])
            assert (
                prev_block_token.bleading_spaces is not None
            ), "Bleading spaces must be defined by this point."
            split_leading_spaces = prev_block_token.bleading_spaces.split(
                ParserHelper.newline_character
            )
            if last_container_token_index in prev_block_token.tabbed_bleading_spaces:
                tabbed_leading_space = prev_block_token.tabbed_bleading_spaces[
                    last_container_token_index
                ]
        else:
            prev_list_token = cast(ListStartMarkdownToken, token_stack[-1])
            assert (
                prev_list_token.leading_spaces is not None
            ), "Leading spaces must be defined by this point."
            split_leading_spaces = prev_list_token.leading_spaces.split(
                ParserHelper.newline_character
            )
        if last_container_token_index < len(split_leading_spaces):
            POGGER.debug(f" -->{ParserHelper.make_value_visible(split_leading_spaces)}")
            POGGER.debug(
                " primary-->container_line>:"
                + ParserHelper.make_value_visible(container_line)
                + ":<"
            )
            container_line = (
                tabbed_leading_space + container_line
                if tabbed_leading_space
                else split_leading_spaces[last_container_token_index] + container_line
            )
            POGGER.debug(
                " -->container_line>:"
                + ParserHelper.make_value_visible(container_line)
                + ":<"
            )
        return container_line

    @staticmethod
    def __apply_primary_transformation_start(
        current_changed_record: Optional[MarkdownChangeRecord],
        actual_tokens: List[MarkdownToken],
    ) -> bool:
        is_list_start_after_two_block_starts = False
        if current_changed_record and current_changed_record.item_c.is_list_start:
            list_start_token = current_changed_record.item_c
            list_start_token_index = actual_tokens.index(list_start_token)
            POGGER.debug(
                f" -->list_start_token_index>{ParserHelper.make_value_visible(list_start_token_index)}"
            )

            # pylint: disable=too-many-boolean-expressions
            if (
                list_start_token_index >= 2
                and actual_tokens[list_start_token_index - 1].is_block_quote_start
                and actual_tokens[list_start_token_index - 2].is_block_quote_start
                and actual_tokens[list_start_token_index - 1].line_number
                == list_start_token.line_number
                and actual_tokens[list_start_token_index - 2].line_number
                == list_start_token.line_number
                and actual_tokens[list_start_token_index + 1].is_list_end
                and actual_tokens[list_start_token_index + 2].is_blank_line
            ):
                is_list_start_after_two_block_starts = True
                # pylint: enable=too-many-boolean-expressions
        return is_list_start_after_two_block_starts

    @staticmethod
    def __adjust(
        nested_list_start_index: int,
        token_stack: List[MarkdownToken],
        container_token_indices: List[int],
        container_line: str,
        apply_list_fix: bool,
    ) -> str:
        previous_token = token_stack[nested_list_start_index]
        if apply_list_fix and previous_token.is_list_start:
            previous_list_token = cast(ListStartMarkdownToken, previous_token)
            delta = previous_list_token.indent_level - len(container_line)
            POGGER.debug(f"delta->{delta}")
            container_line += ParserHelper.repeat_string(" ", delta)
        if previous_token.is_block_quote_start:
            previous_block_token = cast(BlockQuoteMarkdownToken, previous_token)
            leading_spaces = (
                ""
                if previous_block_token.bleading_spaces is None
                else previous_block_token.bleading_spaces
            )
        else:
            previous_list_token = cast(ListStartMarkdownToken, previous_token)
            leading_spaces = (
                ""
                if previous_list_token.leading_spaces is None
                else previous_list_token.leading_spaces
            )
        split_leading_spaces = leading_spaces.split(ParserHelper.newline_character)
        inner_token_index = container_token_indices[nested_list_start_index]
        assert inner_token_index < len(
            split_leading_spaces
        ), "Index must be within the string."
        POGGER.debug(
            f"inner_index->{str(container_token_indices[nested_list_start_index])}"
        )
        container_line = split_leading_spaces[inner_token_index] + container_line
        container_token_indices[nested_list_start_index] = inner_token_index + 1
        POGGER.debug(
            f"inner_index->{str(container_token_indices[nested_list_start_index])}"
        )
        return container_line

    @classmethod
    def __get_last_list_index(cls, token_stack: List[MarkdownToken]) -> int:
        stack_index = len(token_stack) - 2
        nested_list_start_index = -1
        while stack_index >= 0:
            if (
                token_stack[stack_index].is_list_start
                or token_stack[stack_index].is_new_list_item
            ):
                nested_list_start_index = stack_index
                break
            stack_index -= 1
        return nested_list_start_index


# pylint: enable=too-few-public-methods
