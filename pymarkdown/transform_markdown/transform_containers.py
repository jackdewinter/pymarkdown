"""
Module to provide transformations for containers.
"""

import logging
from dataclasses import dataclass
from typing import List, Optional, Tuple, cast

from pymarkdown.general.parser_helper import ParserHelper
from pymarkdown.general.parser_logger import ParserLogger
from pymarkdown.general.tab_helper import TabHelper
from pymarkdown.tokens.block_quote_markdown_token import BlockQuoteMarkdownToken
from pymarkdown.tokens.list_start_markdown_token import ListStartMarkdownToken
from pymarkdown.tokens.markdown_token import EndMarkdownToken, MarkdownToken

POGGER = ParserLogger(logging.getLogger(__name__))

# pylint: disable=too-many-lines


@dataclass
class MarkdownChangeRecord:
    """
    Class to keep track of changes.
    """

    is_container_start: bool
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

        MarkdownToken.assert_tokens_are_same_except_for_line_number(
            container_stack[-1], current_end_token.start_markdown_token
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
                container_text, container_records, actual_tokens, []
            )
            POGGER.debug(f"pre>:{pre_container_text}:<")
            POGGER.debug(f"adj>:{adjusted_text}:<")
            transformed_data = pre_container_text + adjusted_text
            POGGER.debug(f"trn>:{transformed_data}:<")
        return transformed_data

    # pylint: disable=too-many-arguments, too-many-locals
    @staticmethod
    def __apply_line_transformation(
        did_move_ahead: bool,
        token_stack: List[MarkdownToken],
        container_token_indices: List[int],
        current_changed_record: Optional[MarkdownChangeRecord],
        container_line: str,
        actual_tokens: List[MarkdownToken],
        removed_tokens: List[MarkdownToken],
        removed_token_indices: List[int],
        base_line_number: int,
        delta_line: int,
        is_in_multiline_paragraph: bool,
    ) -> str:

        container_line_old = container_line
        token_stack_copy = token_stack[:]
        removed_tokens_copy = removed_tokens[:]
        container_token_indices_copy = container_token_indices[:]
        removed_token_indices_copy = removed_token_indices[:]
        (
            last_container_token_index,
            applied_leading_spaces_to_start_of_container_line,
            container_line,
            did_adjust_due_to_block_quote_start,
        ) = TransformContainers.__apply_primary_transformation(
            did_move_ahead,
            token_stack,
            container_token_indices,
            current_changed_record,
            container_line,
            actual_tokens,
        )

        container_line, block_me = TransformContainers.__adjust_for_list(
            token_stack,
            applied_leading_spaces_to_start_of_container_line,
            container_token_indices,
            container_line,
            container_line_old,
            removed_tokens,
            removed_token_indices,
            current_changed_record,
        )
        container_line = TransformContainers.__adjust_for_block_quote(
            token_stack,
            applied_leading_spaces_to_start_of_container_line,
            container_line,
            container_token_indices,
            base_line_number + delta_line,
            did_adjust_due_to_block_quote_start,
            is_in_multiline_paragraph,
            removed_tokens,
            removed_token_indices,
            container_line_old,
        )

        TransformContainers.__adjust_state_for_element(
            token_stack,
            container_token_indices,
            did_move_ahead,
            current_changed_record,
            last_container_token_index,
            removed_tokens,
            removed_token_indices,
            block_me,
        )

        container_token_indices_copy_length = len(container_token_indices_copy)
        container_token_indices_length = len(container_token_indices)
        if container_token_indices_copy_length > container_token_indices_length:
            assert (
                container_token_indices_copy_length
                == container_token_indices_length + 1
            )
            assert token_stack_copy[-1].is_new_list_item
        for next_index in range(container_token_indices_length):
            delta = (
                container_token_indices[next_index]
                - container_token_indices_copy[next_index]
            )
            if delta > 1:
                container_token_indices[next_index] = (
                    container_token_indices_copy[next_index] + 1
                )

        TransformContainers.__apply_line_transformation_check(
            container_line_old,
            container_line,
            removed_token_indices,
            container_token_indices,
            token_stack_copy,
            container_token_indices_copy,
            removed_tokens_copy,
            removed_token_indices_copy,
        )
        return container_line

    # pylint: enable=too-many-arguments, too-many-locals

    @staticmethod
    def __apply_line_transformation_check_loop(
        token_stack_copy: List[MarkdownToken],
        search_index: int,
        container_token_indices_copy: List[int],
        prefix_text_parts: List[str],
        container_line_old: str,
    ) -> str:
        stack_token_copy = token_stack_copy[search_index]
        stack_token_copy_spaces = (
            cast(BlockQuoteMarkdownToken, stack_token_copy).bleading_spaces
            if stack_token_copy.is_block_quote_start
            else cast(ListStartMarkdownToken, stack_token_copy).leading_spaces
        )
        assert stack_token_copy_spaces is not None
        split_stack_token_copy_spaces = stack_token_copy_spaces.split("\n")
        indent_text = split_stack_token_copy_spaces[
            container_token_indices_copy[search_index]
        ]
        if (
            indent_text
            and indent_text[-1] == ParserLogger.blah_sequence
            and len(prefix_text_parts) == 1
            and container_line_old.startswith(prefix_text_parts[0])
        ):
            container_line_old = container_line_old[len(prefix_text_parts[0]) :]
            indent_text = indent_text[:-1]
            prefix_text_parts.insert(0, indent_text)
        else:
            prefix_text_parts.append(indent_text)
        return container_line_old

    @staticmethod
    def __apply_line_transformation_check_removed(
        removed_tokens_copy: List[MarkdownToken],
        removed_token_indices: List[int],
        removed_token_indices_copy: List[int],
        prefix_text_parts: List[str],
    ) -> None:
        if (removed_token_indices[-1] - removed_token_indices_copy[-1]) > 0:
            removed_leading_spaces = (
                cast(BlockQuoteMarkdownToken, removed_tokens_copy[-1]).bleading_spaces
                if removed_tokens_copy[-1].is_block_quote_start
                else cast(
                    ListStartMarkdownToken, removed_tokens_copy[-1]
                ).leading_spaces
            )
            assert removed_leading_spaces is not None
            split_removed_leading_spaces = removed_leading_spaces.split("\n")
            prefix_text_parts.append(
                split_removed_leading_spaces[removed_token_indices_copy[-1]]
            )

    # pylint: disable=too-many-arguments
    @staticmethod
    def __apply_line_transformation_check(
        container_line_old: str,
        container_line: str,
        removed_token_indices: List[int],
        container_token_indices: List[int],
        token_stack_copy: List[MarkdownToken],
        container_token_indices_copy: List[int],
        removed_tokens_copy: List[MarkdownToken],
        removed_token_indices_copy: List[int],
    ) -> None:
        if container_line_old == container_line or not removed_tokens_copy:
            return
        prefix_text_parts: List[str] = []

        TransformContainers.__apply_line_transformation_check_removed(
            removed_tokens_copy,
            removed_token_indices,
            removed_token_indices_copy,
            prefix_text_parts,
        )
        start_index = len(token_stack_copy) - 1
        if token_stack_copy[start_index].is_new_list_item:
            start_index -= 1
        for search_index in range(start_index, -1, -1):
            if (
                container_token_indices_copy[search_index]
                != container_token_indices[search_index]
            ):
                container_line_old = (
                    TransformContainers.__apply_line_transformation_check_loop(
                        token_stack_copy,
                        search_index,
                        container_token_indices_copy,
                        prefix_text_parts,
                        container_line_old,
                    )
                )
        constructed_prefix_text = "".join(prefix_text_parts[::-1])

        # kludge_flag - these SHOULD always match up, but until we do
        # allow for a relief valve
        detabified_constructed_line = TabHelper.detabify_string(
            constructed_prefix_text + container_line_old
        )
        detabified_container_line = TabHelper.detabify_string(container_line)
        if detabified_constructed_line != detabified_container_line:
            kludge_flag = True
            assert (
                kludge_flag or detabified_constructed_line == detabified_container_line
            ), f"-->{detabified_constructed_line}=={detabified_container_line}<--"

    # pylint: enable=too-many-arguments

    # pylint: disable=too-many-arguments
    @staticmethod
    def __abcd(
        current_changed_record: Optional[MarkdownChangeRecord],
        actual_tokens: List[MarkdownToken],
        removed_tokens: List[MarkdownToken],
        removed_token_indices: List[int],
        container_stack: List[MarkdownToken],
        container_token_indices: List[int],
    ) -> Optional[str]:
        prefix = None
        assert current_changed_record is not None
        token_to_match = (
            current_changed_record.item_c
            if current_changed_record.is_container_start
            else current_changed_record.item_d
        )
        token_index = 0
        while (
            token_index < len(actual_tokens)
            and actual_tokens[token_index] != token_to_match
        ):
            token_index += 1

        while token_index < len(actual_tokens) and (
            actual_tokens[token_index].is_block_quote_end
            or actual_tokens[token_index].is_list_end
        ):
            token_index += 1
        assert token_index != len(actual_tokens)
        while removed_tokens:
            do_check = True
            if removed_tokens[0].is_list_start:
                current_leading_spaces = cast(
                    ListStartMarkdownToken, removed_tokens[0]
                ).leading_spaces
            else:
                bq_token = cast(BlockQuoteMarkdownToken, removed_tokens[0])
                current_leading_spaces = bq_token.bleading_spaces
                do_check = bq_token.weird_kludge_five
            if do_check:
                split_space_index = (
                    len(current_leading_spaces.split("\n"))
                    if current_leading_spaces is not None
                    else 0
                )
                if split_space_index != removed_token_indices[0]:
                    break
            del removed_tokens[0]
            del removed_token_indices[0]
        keep_going = len(removed_tokens) > 1
        if keep_going:
            prefix = TransformContainers.__abcd_final(
                container_stack,
                container_token_indices,
                removed_tokens,
                removed_token_indices,
                prefix,
            )

        keep_going = len(removed_tokens) <= 1
        assert keep_going
        return prefix

    # pylint: enable=too-many-arguments

    @staticmethod
    def __abcd_final(
        container_stack: List[MarkdownToken],
        container_token_indices: List[int],
        removed_tokens: List[MarkdownToken],
        removed_token_indices: List[int],
        prefix: Optional[str],
    ) -> Optional[str]:
        container_stack_copy = container_stack[:]
        container_indices_copy = container_token_indices[:]
        container_stack_copy.extend(removed_tokens[::-1])
        container_indices_copy.extend(removed_token_indices[::-1])

        if container_stack_copy[-1].is_block_quote_start:
            bq_spaces = cast(
                BlockQuoteMarkdownToken, container_stack_copy[-1]
            ).bleading_spaces
            assert bq_spaces is not None
            bq_split_spaces = bq_spaces.split("\n")
            assert container_indices_copy[-1] == len(bq_split_spaces) - 1
            prefix = bq_split_spaces[container_indices_copy[-1]]
            del removed_tokens[0]
            del removed_token_indices[0]
            if container_stack_copy[-2].is_list_start:
                list_spaces = cast(
                    ListStartMarkdownToken, container_stack_copy[-2]
                ).leading_spaces
                assert list_spaces is not None
                list_split_spaces = list_spaces.split("\n")
                assert container_indices_copy[-1] == len(list_split_spaces) - 1
                prefix += list_split_spaces[container_indices_copy[-2]]
                del removed_tokens[0]
                del removed_token_indices[0]
        else:
            del removed_tokens[0]
            del removed_token_indices[0]
            del removed_tokens[0]
            del removed_token_indices[0]
        return prefix

    # pylint: disable=too-many-locals
    @staticmethod
    def __apply_container_transformation(
        container_text: str,
        container_records: List[MarkdownChangeRecord],
        actual_tokens: List[MarkdownToken],
        token_stack: List[MarkdownToken],
    ) -> str:
        # POGGER.debug(
        #     f">>incoming>>:{ParserHelper.make_value_visible(container_text)}:<<"
        # )

        # POGGER.debug(
        #     f">>container_records>>{ParserHelper.make_value_visible(container_records)}"
        # )

        token_stack = []
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

        is_in_multiline_paragraph = False
        for _, container_line in enumerate(split_container_text):  # pragma: no cover
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

            is_para_start_in_line = ParserLogger.start_range_sequence in container_line
            is_para_end_in_line = ParserLogger.end_range_sequence in container_line
            old_record_index = record_index
            (
                record_index,
                did_move_ahead,
                current_changed_record,
                removed_tokens,
                removed_token_indices,
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

            container_line = TransformContainers.__apply_container_transformation_inner(
                container_line,
                actual_tokens,
                did_move_ahead,
                token_stack,
                container_token_indices,
                removed_tokens,
                removed_token_indices,
                current_changed_record,
                base_line_number,
                delta_line,
                is_in_multiline_paragraph,
            )

            TransformContainers.__apply_container_transformation_removed(
                removed_tokens, removed_token_indices
            )

            is_in_multiline_paragraph = (
                not is_para_end_in_line
                if is_in_multiline_paragraph
                else is_para_start_in_line and not is_para_end_in_line
            )

            transformed_parts.append(container_line)
            container_text_index += container_line_length + 1
            delta_line += 1

        # POGGER.debug(
        #     "\n<<transformed<<" + ParserHelper.make_value_visible(transformed_parts)
        # )
        return ParserHelper.newline_character.join(transformed_parts)

    # pylint: enable=too-many-locals

    # pylint: disable=too-many-arguments
    @staticmethod
    def __apply_container_transformation_inner(
        container_line: str,
        actual_tokens: List[MarkdownToken],
        did_move_ahead: bool,
        token_stack: List[MarkdownToken],
        container_token_indices: List[int],
        removed_tokens: List[MarkdownToken],
        removed_token_indices: List[int],
        current_changed_record: Optional[MarkdownChangeRecord],
        base_line_number: int,
        delta_line: int,
        is_in_multiline_paragraph: bool,
    ) -> str:
        prefix_to_use = None
        if len(removed_tokens) > 1 and current_changed_record:
            prefix_to_use = TransformContainers.__abcd(
                current_changed_record,
                actual_tokens,
                removed_tokens,
                removed_token_indices,
                token_stack,
                container_token_indices,
            )
        return (
            prefix_to_use + container_line
            if prefix_to_use is not None
            else TransformContainers.__apply_line_transformation(
                did_move_ahead,
                token_stack,
                container_token_indices,
                current_changed_record,
                container_line,
                actual_tokens,
                removed_tokens,
                removed_token_indices,
                base_line_number,
                delta_line,
                is_in_multiline_paragraph,
            )
        )

    # pylint: enable=too-many-arguments

    @staticmethod
    def __apply_container_transformation_removed(
        removed_tokens: List[MarkdownToken], removed_token_indices: List[int]
    ) -> None:
        if removed_tokens:
            last_removed_token = removed_tokens[-1]
            last_removed_token_index = removed_token_indices[-1]

            if last_removed_token.is_block_quote_start:
                last_removed_token_leading_spaces = cast(
                    BlockQuoteMarkdownToken, last_removed_token
                ).bleading_spaces
            else:
                last_removed_token_leading_spaces = cast(
                    ListStartMarkdownToken, last_removed_token
                ).leading_spaces
            calc_index = (
                len(last_removed_token_leading_spaces.split("\n"))
                if last_removed_token_leading_spaces is not None
                else 0
            )
            if last_removed_token_index < calc_index and (
                last_removed_token_index + 1 != calc_index
                or (
                    last_removed_token_leading_spaces is not None
                    and last_removed_token_leading_spaces.split("\n")[-1] != ""
                )
            ):
                fred = calc_index > -1
                assert fred

    # pylint: disable=too-many-arguments
    @staticmethod
    def __move_to_current_record(
        old_record_index: int,
        container_records: List[MarkdownChangeRecord],
        container_text_index: int,
        token_stack: List[MarkdownToken],
        container_token_indices: List[int],
        container_line_length: int,
    ) -> Tuple[
        int,
        bool,
        Optional[MarkdownChangeRecord],
        List[MarkdownToken],
        List[int],
    ]:
        record_index, current_changed_record, did_move_ahead = (
            old_record_index,
            None,
            False,
        )

        POGGER.debug(f"({container_text_index})")
        POGGER.debug(
            f"({record_index + 1}):{ParserHelper.make_value_visible(container_records[1])}"
        )
        while record_index + 1 < len(container_records) and container_records[
            record_index + 1
        ].item_b <= (container_text_index + container_line_length):
            record_index += 1
        POGGER.debug(
            f"({str(record_index + 1)}):{ParserHelper.make_value_visible(container_records[1])}"
        )
        removed_token_indices: List[int] = []
        added_tokens: List[MarkdownToken] = []
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
                removed_token_indices,
                added_tokens,
            )

        POGGER.debug(
            f"   removed_tokens={ParserHelper.make_value_visible(removed_tokens)}"
        )
        return (
            record_index,
            did_move_ahead,
            current_changed_record,
            removed_tokens,
            removed_token_indices,
        )

    # pylint: enable=too-many-arguments

    # pylint: disable=too-many-arguments
    @staticmethod
    def __manage_records(
        container_records: List[MarkdownChangeRecord],
        old_record_index: int,
        token_stack: List[MarkdownToken],
        container_token_indices: List[int],
        removed_tokens: List[MarkdownToken],
        removed_token_indices: List[int],
        added_tokens: List[MarkdownToken],
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
        if current_changed_record.is_container_start:
            added_tokens.append(current_changed_record.item_c)
            token_stack.append(current_changed_record.item_c)
            container_token_indices.append(0)
        else:
            TransformContainers.__manage_records_check(
                token_stack,
                container_token_indices,
                removed_tokens,
                removed_token_indices,
                current_changed_record,
            )

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

    # pylint: enable=too-many-arguments

    @staticmethod
    def __manage_records_check(
        token_stack: List[MarkdownToken],
        container_token_indices: List[int],
        removed_tokens: List[MarkdownToken],
        removed_token_indices: List[int],
        current_changed_record: Optional[MarkdownChangeRecord],
    ) -> None:
        POGGER.debug(f"   -->{ParserHelper.make_value_visible(token_stack)}")
        POGGER.debug(
            f"   -->{ParserHelper.make_value_visible(container_token_indices)}"
        )

        if token_stack[-1].is_new_list_item:
            removed_tokens.append(token_stack[-1])
            del token_stack[-1]
            del container_token_indices[-1]

        assert current_changed_record is not None
        MarkdownToken.assert_tokens_are_same_except_for_line_number(
            current_changed_record.item_c, token_stack[-1]
        )

        top_of_stack_token = token_stack[-1]
        removed_tokens.append(token_stack[-1])
        del token_stack[-1]
        top_of_stack_index = container_token_indices[-1]
        removed_token_indices.append(top_of_stack_index)
        del container_token_indices[-1]

        if top_of_stack_token.is_block_quote_start:
            top_of_stack_bq_token = cast(BlockQuoteMarkdownToken, top_of_stack_token)
            top_of_stack_leading_spaces = top_of_stack_bq_token.bleading_spaces
        else:
            top_of_stack_list_token = cast(ListStartMarkdownToken, top_of_stack_token)
            top_of_stack_leading_spaces = top_of_stack_list_token.leading_spaces
        top_of_stack_split_leading_spaces = (
            len(top_of_stack_leading_spaces.split("\n"))
            if top_of_stack_leading_spaces is not None
            else 0
        )
        if top_of_stack_index < top_of_stack_split_leading_spaces and (
            top_of_stack_index + 1 != top_of_stack_split_leading_spaces
            or (
                top_of_stack_leading_spaces is not None
                and top_of_stack_leading_spaces.split("\n")[-1] != ""
            )
        ):
            fred = top_of_stack_token is not None
            assert fred

    # pylint: disable=too-many-arguments,too-many-boolean-expressions
    @staticmethod
    def __adjust_state_for_element(
        token_stack: List[MarkdownToken],
        container_token_indices: List[int],
        did_move_ahead: bool,
        current_changed_record: Optional[MarkdownChangeRecord],
        last_container_token_index: int,
        removed_tokens: List[MarkdownToken],
        removed_token_indices: List[int],
        block_me: bool,
    ) -> None:
        # POGGER.debug(f" -->{ParserHelper.make_value_visible(token_stack)}")
        # POGGER.debug(f" -->{ParserHelper.make_value_visible(container_token_indices)}")
        did_change_to_list_token = (
            did_move_ahead
            and (
                current_changed_record is not None
                and current_changed_record.is_container_start
            )
            and (token_stack[-1].is_list_start or token_stack[-1].is_new_list_item)
        )

        # Attempt to address one of the open issues.
        # if False:
        #     xx = did_move_ahead and not did_change_to_list_token and last_container_token_index == 0 and \
        #         current_changed_record and current_changed_record.item_c and current_changed_record.item_c.is_block_quote_start and\
        #         len(token_stack) > 2 and token_stack[-1].is_block_quote_start and token_stack[-2].is_block_quote_start
        #     if xx:
        #         x1 = token_stack[-1]
        #         i1 = container_token_indices[len(token_stack) - 1]
        #         l1 = token_stack[-1].bleading_spaces.split("\n")
        #         c1 = l1[i1]
        #         x2 = token_stack[-2]
        #         i2 = container_token_indices[len(token_stack) - 2]
        #         l2 = token_stack[-2].bleading_spaces.split("\n")
        #         if i2 < len(l2) and token_stack[-1].line_number != token_stack[-2].line_number:
        #             c2 = l2[i2]
        #             if c1 and c2 and c1.startswith(c2):
        #                 assert False

        # This corresponds to __do_block_quote_leading_spaces_adjustments_adjust_bleading
        # and yes... this is a kludge.
        if (
            did_move_ahead
            and not did_change_to_list_token
            and last_container_token_index == 0
            and current_changed_record
            and current_changed_record.item_c
            and current_changed_record.item_c.is_block_quote_start
            and len(token_stack) >= 4
            and token_stack[-1].is_block_quote_start
            and token_stack[-2].is_list_start
            and token_stack[-3].is_list_start
            and token_stack[-4].is_block_quote_start
            and token_stack[-1].line_number != token_stack[-2].line_number
        ):
            container_token_indices[-4] += 1

        # May need earlier if both new item and start of new list on same line
        if not did_change_to_list_token:
            TransformContainers.__adjust_state_for_element_inner(
                token_stack,
                container_token_indices,
                removed_tokens,
                removed_token_indices,
                block_me,
                last_container_token_index,
            )
        elif token_stack[-1].is_new_list_item:
            del token_stack[-1]
            del container_token_indices[-1]
        POGGER.debug(f" -->{ParserHelper.make_value_visible(token_stack)}")
        POGGER.debug(f" -->{ParserHelper.make_value_visible(container_token_indices)}")

    # pylint: enable=too-many-arguments,too-many-boolean-expressions

    # pylint: disable=too-many-arguments
    @staticmethod
    def __adjust_state_for_element_inner(
        token_stack: List[MarkdownToken],
        container_token_indices: List[int],
        removed_tokens: List[MarkdownToken],
        removed_token_indices: List[int],
        block_me: bool,
        last_container_token_index: int,
    ) -> None:
        previous_token = None
        if removed_tokens and removed_tokens[-1].is_block_quote_start:
            nested_block_start_index = len(removed_tokens) - 1

            previous_token = removed_tokens[nested_block_start_index]
            assert previous_token.is_block_quote_start
            previous_bq_token = cast(BlockQuoteMarkdownToken, previous_token)
            assert previous_bq_token.bleading_spaces is not None
            dd = previous_bq_token.bleading_spaces.split("\n")
            inner_token_index = removed_token_indices[-1]
            if inner_token_index >= len(dd):
                previous_token = None
            else:
                removed_token_indices[-1] += 1
        if previous_token is None:
            if not block_me:
                container_token_indices[-1] = last_container_token_index + 1
            current_block_quote_token_index = len(container_token_indices) - 1
            if token_stack[current_block_quote_token_index].is_block_quote_start:
                TransformContainers.__adjust_state_for_element_inner_block_quote(
                    token_stack,
                    container_token_indices,
                    current_block_quote_token_index,
                )

    # pylint: enable=too-many-arguments

    @staticmethod
    def __adjust_state_for_element_inner_block_quote(
        token_stack: List[MarkdownToken],
        container_token_indices: List[int],
        current_block_quote_token_index: int,
    ) -> None:
        previous_block_quote_token_index = current_block_quote_token_index - 1
        while (
            previous_block_quote_token_index >= 0
            and not token_stack[previous_block_quote_token_index].is_block_quote_start
        ):
            previous_block_quote_token_index -= 1
        if (
            previous_block_quote_token_index >= 0
            and token_stack[previous_block_quote_token_index].line_number
            == token_stack[current_block_quote_token_index].line_number
            and not cast(
                BlockQuoteMarkdownToken, token_stack[current_block_quote_token_index]
            ).weird_kludge_three
            and container_token_indices[current_block_quote_token_index] == 1
        ):
            container_token_indices[previous_block_quote_token_index] += 1
        elif (
            previous_block_quote_token_index >= 0
            and container_token_indices[current_block_quote_token_index] == 1
            and token_stack[previous_block_quote_token_index].line_number
            != token_stack[current_block_quote_token_index].line_number
        ):
            TransformContainers.__adjust_state_for_element_inner_part_1(
                token_stack,
                container_token_indices,
                previous_block_quote_token_index,
                current_block_quote_token_index,
            )

    # pylint: disable=too-many-locals
    @staticmethod
    def __adjust_state_for_element_inner_part_1(
        token_stack: List[MarkdownToken],
        container_token_indices: List[int],
        previous_block_quote_token_index: int,
        current_block_quote_token_index: int,
    ) -> None:
        rt_previous_token = cast(
            BlockQuoteMarkdownToken, token_stack[previous_block_quote_token_index]
        )
        assert rt_previous_token.bleading_spaces is not None
        rt_previous = rt_previous_token.bleading_spaces.split("\n")
        # rt_current = token_stack[current_block_quote_token_index].bleading_spaces.split(
        #     "\n"
        # )
        # tp_current = rt_current[0]
        ci_prev = container_token_indices[previous_block_quote_token_index]
        if (
            ci_prev < len(rt_previous)
            and token_stack[current_block_quote_token_index].is_block_quote_start
            and cast(
                BlockQuoteMarkdownToken, token_stack[current_block_quote_token_index]
            ).weird_kludge_four
            is not None
        ):
            # tp_previous = rt_previous[ci_prev]
            fff = cast(
                BlockQuoteMarkdownToken, token_stack[current_block_quote_token_index]
            ).weird_kludge_four
            assert fff is not None

            prev_line = token_stack[previous_block_quote_token_index].line_number
            par_line = fff[0]
            prev_col = token_stack[previous_block_quote_token_index].column_number
            par_col = fff[1]
            prev_cti = container_token_indices[previous_block_quote_token_index]
            par_cti = fff[2]
            prev_leading = rt_previous[prev_cti]
            par_leading = fff[3]

            if (
                prev_line == par_line
                and prev_col == par_col
                and prev_cti == par_cti
                and prev_leading == par_leading
            ):
                container_token_indices[previous_block_quote_token_index] += 1

    # pylint: enable=too-many-locals

    # pylint: disable=too-many-arguments
    @staticmethod
    def __adjust_for_block_quote(
        token_stack: List[MarkdownToken],
        applied_leading_spaces_to_start_of_container_line: bool,
        container_line: str,
        container_token_indices: List[int],
        line_number: int,
        did_adjust_due_to_block_quote_start: bool,
        is_in_multiline_paragraph: bool,
        removed_tokens: List[MarkdownToken],
        removed_token_indices: List[int],
        container_line_old: str,
    ) -> str:
        if not (len(token_stack) > 1 and token_stack[-1].is_block_quote_start):
            return container_line

        POGGER.debug(" looking for nested list start")
        nested_list_start_index = TransformContainers.__get_last_list_index(token_stack)
        POGGER.debug(f" afbq={len(token_stack) - 1}")
        POGGER.debug(f" nested_list_start_index={nested_list_start_index}")
        if nested_list_start_index == -1:
            POGGER.debug(" nope")
            return container_line
        if (
            nested_list_start_index == len(token_stack) - 2
            and nested_list_start_index > 0
            and token_stack[-1].line_number == line_number
            and token_stack[nested_list_start_index - 1].is_block_quote_start
            and token_stack[-1].line_number != token_stack[-2].line_number
        ):
            return TransformContainers.__adjust_for_block_quote_same_line(
                container_line,
                nested_list_start_index,
                token_stack,
                container_token_indices,
            )
        return TransformContainers.__adjust_for_block_quote_previous_line(
            container_line,
            nested_list_start_index,
            token_stack,
            container_token_indices,
            line_number,
            applied_leading_spaces_to_start_of_container_line,
            did_adjust_due_to_block_quote_start,
            is_in_multiline_paragraph,
            removed_tokens,
            removed_token_indices,
            container_line_old,
        )

    # pylint: enable=too-many-arguments

    # pylint: disable=too-many-arguments
    @staticmethod
    def __adjust_for_list(
        token_stack: List[MarkdownToken],
        applied_leading_spaces_to_start_of_container_line: bool,
        container_token_indices: List[int],
        container_line: str,
        container_line_old: str,
        removed_tokens: List[MarkdownToken],
        removed_token_indices: List[int],
        current_changed_record: Optional[MarkdownChangeRecord],
    ) -> Tuple[str, bool]:
        block_me = False
        if (
            token_stack
            and token_stack[-1].is_list_start
            or token_stack[-1].is_new_list_item
        ):
            (
                previous_token,
                inner_token_index,
                nested_block_start_index,
                block_start_on_remove,
                container_line,
            ) = TransformContainers.__adjust_for_list_adjust(
                container_line,
                container_line_old,
                token_stack,
                container_token_indices,
                removed_tokens,
                removed_token_indices,
                applied_leading_spaces_to_start_of_container_line,
            )
            if previous_token:
                container_line, block_me = TransformContainers.__adjust_for_list_end(
                    container_line,
                    token_stack,
                    removed_tokens,
                    removed_token_indices,
                    applied_leading_spaces_to_start_of_container_line,
                    previous_token,
                    container_token_indices,
                    inner_token_index,
                    nested_block_start_index,
                    current_changed_record,
                    block_start_on_remove,
                )
        return container_line, block_me

    # pylint: enable=too-many-arguments

    @staticmethod
    def __adjust_for_list_adjust_block_quote(
        removed_tokens: List[MarkdownToken], removed_token_indices: List[int]
    ) -> Tuple[int, bool, Optional[MarkdownToken], int]:
        nested_block_start_index = len(removed_tokens) - 1
        block_start_on_remove = True

        previous_token: Optional[MarkdownToken] = removed_tokens[
            nested_block_start_index
        ]
        assert previous_token is not None
        assert previous_token.is_block_quote_start
        previous_bq_token = cast(BlockQuoteMarkdownToken, previous_token)
        assert previous_bq_token.bleading_spaces is not None
        dd = previous_bq_token.bleading_spaces.split("\n")
        inner_token_index = removed_token_indices[-1]
        if inner_token_index >= len(dd):
            previous_token = None
        return (
            nested_block_start_index,
            block_start_on_remove,
            previous_token,
            inner_token_index,
        )

    @staticmethod
    def __adjust_for_list_adjust_list(
        removed_tokens: List[MarkdownToken],
        removed_token_indices: List[int],
        container_line: str,
        container_line_old: str,
    ) -> str:
        removed_list_token = cast(ListStartMarkdownToken, removed_tokens[-1])
        if removed_list_token.leading_spaces is not None:
            split_list_leading_spaces = removed_list_token.leading_spaces.split("\n")
            if removed_token_indices[-1] < len(split_list_leading_spaces):
                if removed_leading_spaces := split_list_leading_spaces[
                    removed_token_indices[-1]
                ]:
                    assert container_line.endswith(container_line_old)
                    actual_leading_spaces = container_line[: -len(container_line_old)]

                    _, ex_ws = ParserHelper.extract_spaces_verified(container_line, 0)
                    if (
                        "\t" not in ex_ws
                        and not actual_leading_spaces
                        and removed_leading_spaces != actual_leading_spaces
                    ):
                        container_line = removed_leading_spaces + container_line
        return container_line

    # pylint: disable=too-many-arguments
    @staticmethod
    def __adjust_for_list_adjust(
        container_line: str,
        container_line_old: str,
        token_stack: List[MarkdownToken],
        container_token_indices: List[int],
        removed_tokens: List[MarkdownToken],
        removed_token_indices: List[int],
        applied_leading_spaces_to_start_of_container_line: bool,
    ) -> Tuple[Optional[MarkdownToken], int, int, bool, str]:
        block_start_on_remove = False
        inner_token_index = nested_block_start_index = -1
        previous_token = None
        if removed_tokens and removed_tokens[-1].is_block_quote_start:
            (
                nested_block_start_index,
                block_start_on_remove,
                previous_token,
                inner_token_index,
            ) = TransformContainers.__adjust_for_list_adjust_block_quote(
                removed_tokens, removed_token_indices
            )
        elif removed_tokens and removed_tokens[-1].is_list_start:
            container_line = TransformContainers.__adjust_for_list_adjust_list(
                removed_tokens,
                removed_token_indices,
                container_line,
                container_line_old,
            )
        if previous_token is None:
            block_start_on_remove = False
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
                    f" applied_leading_spaces_to_start_of_container_line->{applied_leading_spaces_to_start_of_container_line}"
                )
                inner_token_index = container_token_indices[nested_block_start_index]
                # POGGER.debug(
                #     f"applied:{applied_leading_spaces_to_start_of_container_line} or "
                #     + f"end.line:{token_stack[-1].line_number} != prev.line:{previous_token.line_number}"
                # )
        return (
            previous_token,
            inner_token_index,
            nested_block_start_index,
            block_start_on_remove,
            container_line,
        )

    # pylint: enable=too-many-arguments

    # pylint: disable=too-many-arguments
    @staticmethod
    def __adjust_for_list_end(
        container_line: str,
        token_stack: List[MarkdownToken],
        removed_tokens: List[MarkdownToken],
        removed_token_indices: List[int],
        applied_leading_spaces_to_start_of_container_line: bool,
        previous_token: MarkdownToken,
        container_token_indices: List[int],
        inner_token_index: int,
        nested_block_start_index: int,
        current_changed_record: Optional[MarkdownChangeRecord],
        block_start_on_remove: bool,
    ) -> Tuple[str, bool]:
        block_me = False
        if TransformContainers.__adjust_for_list_check(
            token_stack,
            removed_tokens,
            applied_leading_spaces_to_start_of_container_line,
            previous_token,
            container_line,
        ):
            container_line = TransformContainers.__adjust_for_list_end_part_2(
                container_line,
                previous_token,
                inner_token_index,
                current_changed_record,
            )

        check_end_data = current_changed_record is not None and (
            current_changed_record.item_d is None
            or (
                current_changed_record.item_d is not None
                and not current_changed_record.item_d.extra_end_data
            )
        )
        if (
            not removed_tokens
            or not removed_tokens[-1].is_block_quote_start
            or check_end_data
        ):
            TransformContainers.__adjust_for_list_end_part_3(
                block_start_on_remove,
                token_stack,
                container_token_indices,
                removed_token_indices,
                nested_block_start_index,
                inner_token_index,
            )

        if (
            removed_tokens
            and current_changed_record
            and current_changed_record.item_d is not None
        ):
            container_line, block_me = TransformContainers.__adjust_for_list_end_part_4(
                container_line,
                block_me,
                token_stack,
                container_token_indices,
                removed_tokens,
                removed_token_indices,
            )
        return container_line, block_me

    # pylint: enable=too-many-arguments

    @staticmethod
    def __adjust_for_list_end_part_2(
        container_line: str,
        previous_token: MarkdownToken,
        inner_token_index: int,
        current_changed_record: Optional[MarkdownChangeRecord],
    ) -> str:
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
                f" adj-->container_line>:{ParserHelper.make_value_visible(container_line)}:<"
            )
            token_leading_spaces = split_leading_spaces[inner_token_index]
            if (
                current_changed_record
                and not current_changed_record.is_container_start
                and current_changed_record.item_d is not None
                and current_changed_record.item_d.extra_end_data is not None
            ):
                token_end_data = current_changed_record.item_d.extra_end_data
                assert token_end_data.startswith(
                    token_leading_spaces
                ) and container_line.startswith(token_end_data)
                token_leading_spaces = ""

            container_line = token_leading_spaces + container_line
            POGGER.debug(
                f" adj-->container_line>:{ParserHelper.make_value_visible(container_line)}:<"
            )
        return container_line

    # pylint: disable=too-many-arguments
    @staticmethod
    def __adjust_for_list_end_part_3(
        block_start_on_remove: bool,
        token_stack: List[MarkdownToken],
        container_token_indices: List[int],
        removed_token_indices: List[int],
        nested_block_start_index: int,
        inner_token_index: int,
    ) -> None:
        if block_start_on_remove:
            old_index_value = removed_token_indices[nested_block_start_index]
            removed_token_indices[nested_block_start_index] = inner_token_index + 1
        else:
            old_index_value = container_token_indices[nested_block_start_index]
            container_token_indices[nested_block_start_index] = inner_token_index + 1
        ## This is a guess...
        if (
            not block_start_on_remove
            and not old_index_value
            and nested_block_start_index
        ):
            assert token_stack[nested_block_start_index].is_block_quote_start
            new_start_index = nested_block_start_index - 1
            while (
                new_start_index >= 0
                and not token_stack[new_start_index].is_block_quote_start
            ):
                new_start_index -= 1
            if new_start_index >= 0:
                container_token_indices[new_start_index] += 1

    # pylint: enable=too-many-arguments

    # pylint: disable=too-many-arguments
    @staticmethod
    def __adjust_for_list_end_part_4(
        container_line: str,
        block_me: bool,
        token_stack: List[MarkdownToken],
        container_token_indices: List[int],
        removed_tokens: List[MarkdownToken],
        removed_token_indices: List[int],
    ) -> Tuple[str, bool]:
        do_it = True
        if token_stack[-1].is_list_start and removed_tokens[-1].is_list_start:
            removed_list_token = cast(ListStartMarkdownToken, removed_tokens[-1])
            assert removed_list_token.leading_spaces is not None
            removed_token_split_spaces = removed_list_token.leading_spaces.split("\n")
            removed_token_index = removed_token_indices[-1]
            assert removed_token_index < len(removed_token_split_spaces)
            removed_token_indices[-1] += 1
            do_it = False
            block_me = True
        if do_it:
            if (
                removed_tokens[-1].is_block_quote_start
                and token_stack[-1].is_list_start
            ):
                container_line = TransformContainers.__adjust_for_list_end_part_4_inner(
                    container_line,
                    token_stack,
                    container_token_indices,
                    removed_tokens,
                    removed_token_indices,
                )
            container_token_indices[-1] += 1
        return container_line, block_me

    # pylint: enable=too-many-arguments

    @staticmethod
    def __adjust_for_list_end_part_4_inner(
        container_line: str,
        token_stack: List[MarkdownToken],
        container_token_indices: List[int],
        removed_tokens: List[MarkdownToken],
        removed_token_indices: List[int],
    ) -> str:
        removed_block_quote_token = cast(BlockQuoteMarkdownToken, removed_tokens[-1])
        assert removed_block_quote_token.bleading_spaces is not None
        list_token = cast(ListStartMarkdownToken, token_stack[-1])
        assert list_token.leading_spaces is not None
        split_leading_spaces = list_token.leading_spaces.split("\n")
        removed_split_leading_spaces = removed_block_quote_token.bleading_spaces.split(
            "\n"
        )
        leading_space_to_use = None
        leading_index_to_use = None
        if removed_token_indices[-1] < len(removed_split_leading_spaces):
            leading_space_to_use = removed_split_leading_spaces[
                removed_token_indices[-1]
            ]
            leading_index_to_use = split_leading_spaces[container_token_indices[-1]]
        if (
            leading_space_to_use is not None
            and leading_index_to_use is not None
            and leading_index_to_use.endswith(ParserLogger.blah_sequence)
            and container_line.startswith(leading_space_to_use)
        ):
            container_line = (
                leading_space_to_use
                + leading_index_to_use[:-1]
                + container_line[len(leading_space_to_use) :]
            )
        return container_line

    @staticmethod
    def __adjust_for_list_check(
        token_stack: List[MarkdownToken],
        removed_tokens: List[MarkdownToken],
        applied_leading_spaces_to_start_of_container_line: bool,
        previous_token: MarkdownToken,
        container_line: str,
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
            weird_kludge_one_count = removed_block_token.weird_kludge_one
            new_list_item_adjust = leading_spaces_newline_count > 1 and (
                weird_kludge_one_count is None or weird_kludge_one_count <= 1
            )
            POGGER.debug(f"new_list_item_adjust:{new_list_item_adjust}")

            if new_list_item_adjust and container_line:
                new_list_item_adjust = TransformContainers.__look_for_container_prefix(
                    token_stack, container_line
                )
        return (
            token_stack[-1].line_number != previous_token.line_number
            and new_list_item_adjust
        )

    @staticmethod
    def __look_for_container_prefix(
        token_stack: List[MarkdownToken], container_line: str
    ) -> bool:
        end_stack_index = len(token_stack) - 1
        assert token_stack[end_stack_index].is_new_list_item
        end_stack_index -= 1
        assert token_stack[end_stack_index].is_list_start

        stack_index = 0
        container_lindex_index, _ = ParserHelper.collect_while_spaces_verified(
            container_line, 0
        )
        is_tracking = True
        while stack_index < end_stack_index and is_tracking:
            if token_stack[stack_index].is_block_quote_start:  # pragma: no cover
                is_tracking = ParserHelper.is_character_at_index(
                    container_line, container_lindex_index, ">"
                )
                container_lindex_index, _ = ParserHelper.collect_while_spaces_verified(
                    container_line, container_lindex_index + 1
                )
            stack_index += 1
        assert is_tracking
        list_token = cast(ListStartMarkdownToken, token_stack[end_stack_index])
        if not list_token.is_unordered_list_start:
            container_lindex_index, numeric_prefix = (
                ParserHelper.collect_while_one_of_characters_verified(
                    container_line, container_lindex_index, "0123456789"
                )
            )
            assert len(numeric_prefix) > 0
        is_tracking = ParserHelper.is_character_at_index(
            container_line, container_lindex_index, list_token.list_start_sequence
        )
        return not is_tracking

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

    # pylint: disable=too-many-arguments
    @staticmethod
    def __adjust_for_block_quote_previous_line(
        container_line: str,
        nested_list_start_index: int,
        token_stack: List[MarkdownToken],
        container_token_indices: List[int],
        line_number: int,
        applied_leading_spaces_to_start_of_container_line: bool,
        did_adjust_due_to_block_quote_start: bool,
        is_in_multiline_paragraph: bool,
        removed_tokens: List[MarkdownToken],
        removed_token_indices: List[int],
        container_line_old: str,
    ) -> str:
        previous_cl = container_line
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
            container_line = TransformContainers.__adjust_for_block_quote_previous_line_nudge_different(
                container_line,
                nested_list_start_index,
                token_stack,
                container_token_indices,
                did_adjust_due_to_block_quote_start,
                is_in_multiline_paragraph,
                applied_leading_spaces_to_start_of_container_line,
                removed_tokens,
                removed_token_indices,
            )
        else:
            POGGER.debug("same line as list start")
            container_line = (
                TransformContainers.__adjust_for_block_quote_previous_line_nudge_same(
                    container_line,
                    nested_list_start_index,
                    token_stack,
                    container_token_indices,
                    previous_token,
                )
            )
        container_line = (
            TransformContainers.__adjust_for_block_quote_previous_line_nudge(
                container_line, previous_cl, container_line_old
            )
        )
        return container_line

    # pylint: enable=too-many-arguments

    # pylint: disable=too-many-arguments
    @staticmethod
    def __adjust_for_block_quote_previous_line_nudge_different(
        container_line: str,
        nested_list_start_index: int,
        token_stack: List[MarkdownToken],
        container_token_indices: List[int],
        did_adjust_due_to_block_quote_start: bool,
        is_in_multiline_paragraph: bool,
        applied_leading_spaces_to_start_of_container_line: bool,
        removed_tokens: List[MarkdownToken],
        removed_token_indices: List[int],
    ) -> str:
        POGGER.debug("different line as list start")
        is_special_case = not (
            did_adjust_due_to_block_quote_start and not is_in_multiline_paragraph
        )
        container_line_change_required = (
            not applied_leading_spaces_to_start_of_container_line
            or (applied_leading_spaces_to_start_of_container_line and is_special_case)
        )
        if removed_tokens and removed_tokens[0].is_list_start:
            removed_list_token = cast(ListStartMarkdownToken, removed_tokens[0])
            if removed_list_token.leading_spaces is not None:
                removed_tokens_spaces = removed_list_token.leading_spaces.split("\n")
                if removed_token_indices[0] < len(removed_tokens_spaces):
                    nested_list_start_index = 0
                    token_stack = removed_tokens
                    container_token_indices = removed_token_indices
        return TransformContainers.__adjust(
            nested_list_start_index,
            token_stack,
            container_token_indices,
            container_line,
            False,
            apply_change_to_container_line=container_line_change_required,
        )

    # pylint: enable=too-many-arguments

    @staticmethod
    def __adjust_for_block_quote_previous_line_nudge_same(
        container_line: str,
        nested_list_start_index: int,
        token_stack: List[MarkdownToken],
        container_token_indices: List[int],
        previous_token: MarkdownToken,
    ) -> str:
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
    def __adjust_for_block_quote_previous_line_nudge(
        container_line: str, previous_cl: str, container_line_old: str
    ) -> str:
        if previous_cl != container_line and container_line.endswith(previous_cl):
            adj_container_line = container_line[: -len(previous_cl)]
            if adj_container_line[-1] == ParserLogger.blah_sequence:
                assert previous_cl.endswith(container_line_old)
                adj_container_line = adj_container_line[:-1]
                prefix = previous_cl[: -len(container_line_old)]
                suffix = previous_cl[-len(container_line_old) :]
                container_line = prefix + adj_container_line + suffix
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
                or not current_changed_record.is_container_start
            )
            and not is_list_start_after_two_block_starts
            and not was_abrupt_block_quote_end
        )

        last_container_token_index = container_token_indices[-1]
        if applied_leading_spaces_to_start_of_container_line:
            container_line, did_adjust_due_to_block_quote_start = (
                TransformContainers.__apply_primary_transformation_adjust_container_line(
                    token_stack,
                    last_container_token_index,
                    container_line,
                )
            )
        else:
            did_adjust_due_to_block_quote_start = False
        return (
            last_container_token_index,
            applied_leading_spaces_to_start_of_container_line,
            container_line,
            did_adjust_due_to_block_quote_start,
        )

    # pylint: enable=too-many-arguments

    @classmethod
    def __apply_primary_transformation_adjust_container_line(
        cls,
        token_stack: List[MarkdownToken],
        last_container_token_index: int,
        container_line: str,
    ) -> Tuple[str, bool]:
        POGGER.debug(f" container->{ParserHelper.make_value_visible(token_stack[-1])}")
        did_adjust_due_to_block_quote_start = False
        tabbed_leading_space: Optional[str] = None
        if token_stack[-1].is_block_quote_start:
            did_adjust_due_to_block_quote_start = True
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
            prev_list_token = (
                cast(ListStartMarkdownToken, token_stack[-2])
                if token_stack[-1].is_new_list_item
                else cast(ListStartMarkdownToken, token_stack[-1])
            )
            assert (
                prev_list_token.leading_spaces is not None
            ), "Leading spaces must be defined by this point."
            split_leading_spaces = prev_list_token.leading_spaces.split(
                ParserHelper.newline_character
            )
        if last_container_token_index < len(split_leading_spaces):
            POGGER.debug(f" -->{ParserHelper.make_value_visible(split_leading_spaces)}")
            POGGER.debug(
                f" primary-->container_line>:{ParserHelper.make_value_visible(container_line)}:<"
            )
            container_line = (
                tabbed_leading_space + container_line
                if tabbed_leading_space
                else split_leading_spaces[last_container_token_index] + container_line
            )
            POGGER.debug(
                f" -->container_line>:{ParserHelper.make_value_visible(container_line)}:<"
            )
        else:
            did_adjust_due_to_block_quote_start = False
        return container_line, did_adjust_due_to_block_quote_start

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

    # pylint: disable=too-many-arguments
    @staticmethod
    def __adjust(
        nested_list_start_index: int,
        token_stack: List[MarkdownToken],
        container_token_indices: List[int],
        container_line: str,
        apply_list_fix: bool,
        apply_change_to_container_line: bool = True,
    ) -> str:
        previous_token = token_stack[nested_list_start_index]
        if (
            apply_list_fix
            and apply_change_to_container_line
            and previous_token.is_list_start
        ):
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
            if previous_token.is_new_list_item:
                previous_token = token_stack[nested_list_start_index - 1]
                assert previous_token.is_list_start
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
        if apply_change_to_container_line:
            container_line = split_leading_spaces[inner_token_index] + container_line
        container_token_indices[nested_list_start_index] = inner_token_index + 1
        POGGER.debug(
            f"inner_index->{str(container_token_indices[nested_list_start_index])}"
        )
        return container_line

    # pylint: enable=too-many-arguments

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
