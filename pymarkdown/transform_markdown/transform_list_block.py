"""
Module to provide transformations for a list block.
"""
import copy
import logging
from typing import List, Optional, Tuple, Union, cast

from pymarkdown.general.parser_helper import ParserHelper
from pymarkdown.general.parser_logger import ParserLogger
from pymarkdown.tokens.block_quote_markdown_token import BlockQuoteMarkdownToken
from pymarkdown.tokens.list_start_markdown_token import ListStartMarkdownToken
from pymarkdown.tokens.markdown_token import EndMarkdownToken, MarkdownToken
from pymarkdown.tokens.new_list_item_markdown_token import NewListItemMarkdownToken
from pymarkdown.transform_markdown.markdown_transform_context import (
    MarkdownTransformContext,
)

POGGER = ParserLogger(logging.getLogger(__name__))


class TransformListBlock:
    """
    Class to provide transformations for a list block.
    """

    @staticmethod
    def rehydrate_list_start(
        context: MarkdownTransformContext,
        current_token: MarkdownToken,
        previous_token: Optional[MarkdownToken],
        next_token: Optional[MarkdownToken],
        transformed_data: str,
    ) -> str:
        """
        Rehydrate the unordered list start token.
        """

        assert next_token is not None
        POGGER.debug(
            f">>current_token>>{ParserHelper.make_value_visible(current_token)}<<"
        )
        current_list_token = cast(ListStartMarkdownToken, current_token)

        extracted_whitespace = current_list_token.extracted_whitespace
        POGGER.debug(f">>extracted_whitespace>>{extracted_whitespace}<<")
        had_weird_block_quote_in_list = False
        if previous_token:
            (
                previous_indent,
                extracted_whitespace,
                was_within_block_token,
                post_adjust_whitespace,
                _,
                had_weird_block_quote_in_list,
            ) = TransformListBlock.rehydrate_list_start_previous_token(
                context,
                current_list_token,
                previous_token,
                next_token,
                extracted_whitespace,
            )
            POGGER.debug(f">>extracted_whitespace>>{extracted_whitespace}<<")
            POGGER.debug(f">>post_adjust_whitespace>>{post_adjust_whitespace}<<")
        else:
            previous_indent, post_adjust_whitespace, was_within_block_token = (
                0,
                None,
                False,
            )

        POGGER.debug(
            f">>had_weird_block_quote_in_list>>{had_weird_block_quote_in_list}<<"
        )
        context.container_token_stack.append(copy.deepcopy(current_list_token))

        POGGER.debug(f">>extracted_whitespace>>{extracted_whitespace}<<")
        POGGER.debug(
            f">>transformed_data>>{ParserHelper.make_value_visible(transformed_data)}<<"
        )

        if was_within_block_token:
            adjustment_since_newline = 0
        else:
            (
                adjustment_since_newline,
                extracted_whitespace,
            ) = TransformListBlock.adjust_whitespace_for_block_quote(
                transformed_data, extracted_whitespace
            )
        POGGER.debug(f">>adjustment_since_newline>>{adjustment_since_newline}<<")
        POGGER.debug(f">>extracted_whitespace>>{extracted_whitespace}<<")

        return TransformListBlock.__rehydrate_list_start_calculate_start(
            current_list_token,
            next_token,
            extracted_whitespace,
            previous_indent,
            adjustment_since_newline,
            post_adjust_whitespace,
        )

    @staticmethod
    def rehydrate_list_start_end(
        context: MarkdownTransformContext,
        current_token: MarkdownToken,
        actual_tokens: List[MarkdownToken],
        token_index: int,
    ) -> str:
        """
        Rehydrate the ordered list end token.
        """
        _ = actual_tokens, token_index
        del context.container_token_stack[-1]

        current_end_token = cast(EndMarkdownToken, current_token)
        current_start_token = cast(
            ListStartMarkdownToken, current_end_token.start_markdown_token
        )

        leading_spaces_index, expected_leading_spaces_index = (
            current_start_token.leading_spaces_index,
            ParserHelper.count_newlines_in_text(
                current_start_token.extracted_whitespace
            ),
        )

        assert leading_spaces_index == expected_leading_spaces_index, (
            f"leading_spaces_index={leading_spaces_index};"
            + f"expected_leading_spaces_index={expected_leading_spaces_index}"
        )
        return ""

    @staticmethod
    def adjust_whitespace_for_block_quote(
        transformed_data: str, extracted_whitespace: str
    ) -> Tuple[int, str]:
        """
        Make sure lists can adjust for block quote.
        """
        transformed_data_since_newline = transformed_data
        if ParserHelper.newline_character in transformed_data_since_newline:
            last_newline_index = transformed_data_since_newline.rindex(
                ParserHelper.newline_character
            )
            transformed_data_since_newline = transformed_data_since_newline[
                last_newline_index + 1 :
            ]
        adjustment_since_newline = 0
        # transformed_data_since_newline_size = len(
        #     transformed_data_since_newline
        # )
        POGGER.debug(
            f">>transformed_data_since_newline>>:{transformed_data_since_newline}:<<"
        )
        # POGGER.debug(f">>adjustment_since_newline>>:{adjustment_since_newline}:<<")
        # POGGER.debug(
        #     f">>transformed_data_since_newline_size>>:{transformed_data_since_newline_size}:<<"
        # )
        # POGGER.debug(f">>extracted_whitespace>>:{extracted_whitespace}:<<")
        # if (
        #     extracted_whitespace
        #     and len(extracted_whitespace) >= transformed_data_since_newline_size
        #     and ">" in transformed_data_since_newline
        # ):
        #     adjustment_since_newline = transformed_data_since_newline_size
        #     extracted_whitespace = extracted_whitespace[adjustment_since_newline:]
        POGGER.debug(f">>adjustment_since_newline>>:{adjustment_since_newline}:<<")
        POGGER.debug(f">>extracted_whitespace>>:{extracted_whitespace}:<<")
        return adjustment_since_newline, extracted_whitespace

    @staticmethod
    def rehydrate_list_start_previous_token(
        context: MarkdownTransformContext,
        current_token: Union[ListStartMarkdownToken, NewListItemMarkdownToken],
        previous_token: MarkdownToken,
        next_token: MarkdownToken,
        extracted_whitespace: str,
    ) -> Tuple[int, str, bool, Optional[str], bool, bool]:
        """
        Rehydrate the list start previous.
        """
        (
            previous_indent,
            post_adjust_whitespace,
            was_within_block_token,
            containing_block_quote_token,
            containing_list_token,
            deeper_containing_block_quote_token,
        ) = TransformListBlock.__rehydrate_list_start_previous_token_start(
            context, current_token, previous_token, extracted_whitespace
        )

        had_weird_block_quote_in_list = False
        did_container_start_midline = False
        if previous_token.is_list_start:
            POGGER.debug("rlspt>>is_list_start")
            previous_list_token = cast(ListStartMarkdownToken, previous_token)
            (
                previous_indent,
                extracted_whitespace,
            ) = TransformListBlock.__rehydrate_list_start_prev_list(
                current_token, previous_list_token
            )
        elif previous_token.is_block_quote_start:
            POGGER.debug("rlspt>>is_block_quote_start")
            assert containing_block_quote_token is not None
            (
                previous_indent,
                post_adjust_whitespace,
                extracted_whitespace,
            ) = TransformListBlock.__rehydrate_list_start_prev_block_quote(
                current_token,
                previous_token,
                containing_block_quote_token,
            )
        elif containing_block_quote_token:
            POGGER.debug("rlspt>>containing_block_quote_token")
            (
                was_within_block_token,
                previous_indent,
            ) = TransformListBlock.__rehydrate_list_start_contained_in_block_quote(
                current_token, containing_block_quote_token
            )
        elif containing_list_token:
            POGGER.debug("rlspt>>containing_list_token")
            (
                previous_indent,
                extracted_whitespace,
                post_adjust_whitespace,
                did_container_start_midline,
                had_weird_block_quote_in_list,
            ) = TransformListBlock.__rehydrate_list_start_contained_in_list(
                current_token,
                containing_list_token,
                deeper_containing_block_quote_token,
                extracted_whitespace,
                previous_token,
                next_token,
            )

        POGGER.debug(f"xx>>previous_indent:{previous_indent}:")
        POGGER.debug(f"xx>>extracted_whitespace:{extracted_whitespace}:")
        POGGER.debug(f"xx>>was_within_block_token:{was_within_block_token}:")
        POGGER.debug(f"xx>>post_adjust_whitespace:{post_adjust_whitespace}:")
        POGGER.debug(f"xx>>did_container_start_midline:{did_container_start_midline}:")
        return (
            previous_indent,
            extracted_whitespace,
            was_within_block_token,
            post_adjust_whitespace,
            did_container_start_midline,
            had_weird_block_quote_in_list,
        )

    @staticmethod
    def __rehydrate_list_start_previous_token_start(
        context: MarkdownTransformContext,
        current_token: Union[ListStartMarkdownToken, NewListItemMarkdownToken],
        previous_token: MarkdownToken,
        extracted_whitespace: str,
    ) -> Tuple[
        int,
        Optional[str],
        bool,
        Optional[BlockQuoteMarkdownToken],
        Optional[ListStartMarkdownToken],
        Optional[BlockQuoteMarkdownToken],
    ]:
        previous_indent, was_within_block_token = 0, False
        post_adjust_whitespace: Optional[str] = None
        POGGER.debug(
            f"rlspt>>current_token>>{ParserHelper.make_value_visible(current_token)}<<"
        )
        POGGER.debug(
            f"rlspt>>previous_token>>{ParserHelper.make_value_visible(previous_token)}<<"
        )
        POGGER.debug(
            f"rlspt>>extracted_whitespace>>{ParserHelper.make_value_visible(extracted_whitespace)}<<"
        )
        POGGER.debug(
            f"rls>>self.context.container_token_stack>>{ParserHelper.make_value_visible(context.container_token_stack)}<<"
        )
        containing_block_quote_token = TransformListBlock.__look_for_last_block_token(
            context
        )
        POGGER.debug(
            f"rls>>containing_block_quote_token>>{ParserHelper.make_value_visible(containing_block_quote_token)}<<"
        )
        if containing_block_quote_token:
            POGGER.debug(
                f"rls>>containing_block_quote_token>>{ParserHelper.make_value_visible(containing_block_quote_token.leading_text_index)}<<"
            )

        token_stack_index = (
            TransformListBlock.__look_backward_for_list_or_block_quote_start(context)
        )
        POGGER.debug(f"rls>>token_stack_index2>>{token_stack_index}<<")

        containing_list_token, deeper_containing_block_quote_token = None, None
        if (
            token_stack_index >= 0
            and containing_block_quote_token
            != context.container_token_stack[token_stack_index]
        ):
            containing_list_token = cast(
                ListStartMarkdownToken, context.container_token_stack[token_stack_index]
            )
            deeper_containing_block_quote_token = containing_block_quote_token
            containing_block_quote_token = None

        return (
            previous_indent,
            post_adjust_whitespace,
            was_within_block_token,
            containing_block_quote_token,
            containing_list_token,
            deeper_containing_block_quote_token,
        )

    @staticmethod
    def __rehydrate_list_start_prev_list(
        current_token: Union[ListStartMarkdownToken, NewListItemMarkdownToken],
        previous_token: ListStartMarkdownToken,
    ) -> Tuple[int, str]:
        _ = current_token
        return previous_token.indent_level, ""

    @staticmethod
    def __rehydrate_list_start_prev_block_quote(
        current_token: Union[ListStartMarkdownToken, NewListItemMarkdownToken],
        previous_token: MarkdownToken,
        containing_block_quote_token: BlockQuoteMarkdownToken,
    ) -> Tuple[int, str, str]:
        previous_block_token = cast(BlockQuoteMarkdownToken, previous_token)
        assert previous_block_token.bleading_spaces is not None
        previous_indent = (
            len(
                previous_block_token.calculate_next_bleading_space_part(
                    increment_index=False
                )
            )
            if ParserHelper.newline_character in previous_block_token.bleading_spaces
            else len(previous_block_token.bleading_spaces)
        )
        POGGER.debug(
            f"adj->current_token>>:{ParserHelper.make_value_visible(current_token)}:<<"
        )
        POGGER.debug(
            f"adj->containing_block_quote_token>>:{ParserHelper.make_value_visible(containing_block_quote_token)}:<<"
        )
        assert current_token.line_number == containing_block_quote_token.line_number
        assert containing_block_quote_token.bleading_spaces is not None
        split_leading_spaces = containing_block_quote_token.bleading_spaces.split(
            ParserHelper.newline_character
        )
        block_quote_leading_space = split_leading_spaces[0]
        block_quote_leading_space_length = len(block_quote_leading_space)

        POGGER.debug(
            f"bq->len>>:{block_quote_leading_space}: {block_quote_leading_space_length}"
        )

        post_adjust_whitespace = "".ljust(
            current_token.column_number - block_quote_leading_space_length - 1, " "
        )
        extracted_whitespace = ""
        POGGER.debug(
            f"post_adjust_whitespace:{post_adjust_whitespace}: extracted_whitespace:{extracted_whitespace}:"
        )
        return previous_indent, post_adjust_whitespace, extracted_whitespace

    @staticmethod
    def __rehydrate_list_start_contained_in_block_quote(
        current_token: Union[ListStartMarkdownToken, NewListItemMarkdownToken],
        containing_block_quote_token: BlockQuoteMarkdownToken,
    ) -> Tuple[bool, int]:
        block_quote_leading_space = (
            containing_block_quote_token.calculate_next_bleading_space_part(
                increment_index=False, delta=-1
            )
        )
        previous_indent = len(block_quote_leading_space)
        POGGER.debug(f"adj->rls>>previous_indent>>:{previous_indent}:<<")
        POGGER.debug(
            f"adj->rls>>current_token.indent_level>>:{current_token.indent_level}:<<"
        )

        return True, previous_indent

    # pylint: disable=too-many-arguments, too-many-locals
    @staticmethod
    def __rehydrate_list_start_contained_in_list(
        current_token: Union[ListStartMarkdownToken, NewListItemMarkdownToken],
        containing_list_token: ListStartMarkdownToken,
        deeper_containing_block_quote_token: Optional[BlockQuoteMarkdownToken],
        extracted_whitespace: str,
        previous_token: MarkdownToken,
        next_token: MarkdownToken,
    ) -> Tuple[int, str, str, bool, bool]:
        # POGGER.debug(
        #     f"adj->containing_list_token>>:{ParserHelper.make_value_visible(containing_list_token)}:<<"
        # )
        # POGGER.debug(
        #     f"adj->deeper_containing_block_quote_token>>:{ParserHelper.make_value_visible(deeper_containing_block_quote_token)}:<<"
        # )

        # POGGER.debug(
        #     f"adj->extracted_whitespace>>:{ParserHelper.make_value_visible(extracted_whitespace)}:<<"
        # )
        (
            starting_whitespace,
            did_container_start_midline,
            block_quote_leading_space_length,
            had_weird_block_quote_in_list,
            list_leading_space_length,
        ) = TransformListBlock.__rehydrate_list_start_contained_in_list_start(
            previous_token, current_token, deeper_containing_block_quote_token
        )

        list_start_content_length = 0
        add_extracted_whitespace_at_end = False
        # POGGER.debug(
        #     f"previous_token-->{ParserHelper.make_value_visible(previous_token)}"
        # )
        # POGGER.debug(
        #     f"current_token-->{ParserHelper.make_value_visible(current_token)}"
        # )
        # POGGER.debug(f"next_token-->{ParserHelper.make_value_visible(next_token)}")
        if current_token.is_new_list_item and previous_token.is_end_token:
            previous_end_token = cast(EndMarkdownToken, previous_token)
            # POGGER.debug(
            #     f"previous_token.start_markdown_token-->{ParserHelper.make_value_visible(previous_end_token.start_markdown_token)}"
            # )
            if previous_end_token.start_markdown_token.is_block_quote_start:
                new_list_token = cast(NewListItemMarkdownToken, containing_list_token)
                list_start_content_length = (
                    len(new_list_token.list_start_content)
                    if new_list_token.is_ordered_list_start
                    else 0
                )
                add_extracted_whitespace_at_end = not next_token.is_block_quote_start

        post_adjust_whitespace = TransformListBlock.__calculate_post_adjust_whitespace(
            starting_whitespace,
            containing_list_token,
            block_quote_leading_space_length,
            list_leading_space_length,
            list_start_content_length,
            add_extracted_whitespace_at_end,
            current_token,
        )

        (
            previous_indent,
            extracted_whitespace,
        ) = TransformListBlock.__rehydrate_list_start_contained_in_list_spacingx(
            containing_list_token, current_token, block_quote_leading_space_length
        )
        # POGGER.debug(f"adj->post_adjust_whitespace>>:{post_adjust_whitespace}:<<")
        return (
            previous_indent,
            extracted_whitespace,
            post_adjust_whitespace,
            did_container_start_midline,
            had_weird_block_quote_in_list,
        )

    # pylint: enable=too-many-arguments, too-many-locals

    @staticmethod
    def __look_for_last_block_token(
        context: MarkdownTransformContext,
    ) -> Optional[BlockQuoteMarkdownToken]:
        found_block_token: Optional[BlockQuoteMarkdownToken] = None
        found_token = next(
            (
                context.container_token_stack[i]
                for i in range(len(context.container_token_stack) - 1, -1, -1)
                if context.container_token_stack[i].is_block_quote_start
            ),
            None,
        )
        POGGER.debug(
            f">>found_block_token>>{ParserHelper.make_value_visible(found_token)}<"
        )
        if found_token:
            found_block_token = cast(BlockQuoteMarkdownToken, found_token)
            POGGER.debug(
                f">>found_block_token-->index>>{found_block_token.leading_text_index}<"
            )
        return found_block_token

    @staticmethod
    def __look_backward_for_list_or_block_quote_start(
        context: MarkdownTransformContext,
    ) -> int:
        token_stack_index = len(context.container_token_stack) - 1
        POGGER.debug(f"rls>>token_stack_index>>{token_stack_index}<<")
        if token_stack_index >= 0:
            assert (
                context.container_token_stack[token_stack_index].is_list_start
                or context.container_token_stack[token_stack_index].is_block_quote_start
            )
        # while (
        #     token_stack_index >= 0
        #     and not self.context.container_token_stack[token_stack_index].is_list_start
        #     and not self.context.container_token_stack[token_stack_index].is_block_quote_start
        # ):
        #     token_stack_index -= 1
        return token_stack_index

    @staticmethod
    def __rehydrate_list_start_contained_in_list_start(
        previous_token: MarkdownToken,
        current_token: Union[ListStartMarkdownToken, NewListItemMarkdownToken],
        deeper_containing_block_quote_token: Optional[BlockQuoteMarkdownToken],
    ) -> Tuple[str, bool, int, bool, int]:
        starting_whitespace = ""
        check_list_for_indent = True
        did_container_start_midline = False
        block_quote_leading_space_length = 0
        had_weird_block_quote_in_list = False
        list_leading_space_length = 0

        if deeper_containing_block_quote_token:
            (
                check_list_for_indent,
                starting_whitespace,
                did_container_start_midline,
                block_quote_leading_space_length,
                had_weird_block_quote_in_list,
            ) = TransformListBlock.__rehydrate_list_start_contained_in_list_deeper_block_quote(
                previous_token, deeper_containing_block_quote_token, current_token
            )

        if (
            check_list_for_indent
            and previous_token
            and previous_token.line_number == current_token.line_number
            and previous_token.is_new_list_item
        ):
            previous_new_list_token = cast(NewListItemMarkdownToken, previous_token)
            list_leading_space_length = previous_new_list_token.indent_level

        return (
            starting_whitespace,
            did_container_start_midline,
            block_quote_leading_space_length,
            had_weird_block_quote_in_list,
            list_leading_space_length,
        )

    # pylint: disable=too-many-arguments
    @staticmethod
    def __calculate_post_adjust_whitespace(
        starting_whitespace: str,
        containing_list_token: ListStartMarkdownToken,
        block_quote_leading_space_length: int,
        list_leading_space_length: int,
        list_start_content_length: int,
        add_extracted_whitespace_at_end: bool,
        current_token: Union[ListStartMarkdownToken, NewListItemMarkdownToken],
    ) -> str:
        POGGER.debug(f"adj->starting_whitespace>>:{starting_whitespace}:<<")
        POGGER.debug(
            f"adj->containing_list_token.indent_level>>:{containing_list_token.indent_level}:<<"
        )
        POGGER.debug(
            f"adj->block_quote_leading_space_length>>:{block_quote_leading_space_length}:<<"
        )
        POGGER.debug(f"adj->list_leading_space_length>>:{list_leading_space_length}:<<")
        POGGER.debug(f"list_start_content_length:{list_start_content_length}:<<")

        pad_to_length = (
            containing_list_token.indent_level
            - block_quote_leading_space_length
            - list_leading_space_length
            - list_start_content_length
        )
        POGGER.debug(f"pad_to_length:{pad_to_length}:<<")
        POGGER.debug(f"adj->starting_whitespace>>:{starting_whitespace}:<<")
        post_adjust_whitespace = starting_whitespace.ljust(pad_to_length, " ")
        POGGER.debug(f"adj->post_adjust_whitespace>>:{post_adjust_whitespace}:<<")
        if add_extracted_whitespace_at_end:
            post_adjust_whitespace += current_token.extracted_whitespace
        POGGER.debug(f"adj->post_adjust_whitespace>>:{post_adjust_whitespace}:<<")
        return post_adjust_whitespace

    # pylint: enable=too-many-arguments

    @staticmethod
    def __rehydrate_list_start_contained_in_list_spacingx(
        containing_list_token: ListStartMarkdownToken,
        current_token: Union[NewListItemMarkdownToken, ListStartMarkdownToken],
        block_quote_leading_space_length: int,
    ) -> Tuple[int, str]:
        previous_indent = containing_list_token.indent_level
        white_space_length = (
            len(current_token.extracted_whitespace) + block_quote_leading_space_length
        )
        POGGER.debug(f"adj->len(ws)>>:{white_space_length}:<<")
        extracted_whitespace = (
            "".ljust(white_space_length - previous_indent, " ")
            if white_space_length > previous_indent
            else ""
        )
        POGGER.debug(f"adj->previous_indent>>:{previous_indent}:<<")
        POGGER.debug(
            f"adj->extracted_whitespace>>:{ParserHelper.make_value_visible(extracted_whitespace)}:<<"
        )
        return previous_indent, extracted_whitespace

    @staticmethod
    def __rehydrate_list_start_contained_in_list_deeper_block_quote(
        previous_token: MarkdownToken,
        deeper_containing_block_quote_token: BlockQuoteMarkdownToken,
        current_token: Union[ListStartMarkdownToken, NewListItemMarkdownToken],
    ) -> Tuple[bool, str, bool, int, bool]:
        assert previous_token is not None
        POGGER.debug(
            f"previous_token:{ParserHelper.make_value_visible(previous_token)}:"
        )
        # if previous_token.is_end_token:
        #     POGGER.debug(
        #         f"previous_token.start_markdown_token:{previous_token.start_markdown_token}:"
        #     )
        POGGER.debug(
            f"deeper_containing_block_quote_token:{ParserHelper.make_value_visible(deeper_containing_block_quote_token)}:"
        )
        had_weird_block_quote_in_list = False
        do_perform_block_quote_ending = False
        if previous_token and previous_token.is_end_token:
            previous_end_token = cast(EndMarkdownToken, previous_token)
            if previous_end_token.start_markdown_token.is_block_quote_start:
                had_weird_block_quote_in_list = True
                POGGER.debug(f"previous_token:{previous_token}:")
                POGGER.debug(
                    f"previous_token.start_markdown_token:{previous_end_token.start_markdown_token}:"
                )
                block_quote_token = cast(
                    BlockQuoteMarkdownToken, previous_end_token.start_markdown_token
                )
                POGGER.debug(
                    f"previous_token.start_markdown_token.leading_spaces:{block_quote_token.bleading_spaces}:"
                )
                assert block_quote_token.bleading_spaces is not None
                newline_count = ParserHelper.count_characters_in_text(
                    block_quote_token.bleading_spaces, "\n"
                )
                previous_start_line = block_quote_token.line_number
                POGGER.debug(f"newline_count:{newline_count}:")
                POGGER.debug(f"previous_start_line:{previous_start_line}:")
                projected_start_line = previous_start_line + (newline_count + 1)
                POGGER.debug(f"projected_start_line:{projected_start_line}:")
                do_perform_block_quote_ending = (
                    projected_start_line != current_token.line_number
                )
        (
            block_quote_leading_space,
            starting_whitespace,
            did_container_start_midline,
            check_list_for_indent,
        ) = TransformListBlock.__rehydrate_list_start_deep(
            do_perform_block_quote_ending,
            previous_token,
            current_token,
            deeper_containing_block_quote_token,
            had_weird_block_quote_in_list,
        )
        POGGER.debug(
            f"block_quote_leading_space:{ParserHelper.make_value_visible(block_quote_leading_space)}:"
        )

        POGGER.debug(f"starting_whitespace:{starting_whitespace}:")
        return (
            check_list_for_indent,
            starting_whitespace,
            did_container_start_midline,
            len(block_quote_leading_space),
            had_weird_block_quote_in_list,
        )

    @staticmethod
    def __rehydrate_list_start_deep(
        do_perform_block_quote_ending: bool,
        previous_token: MarkdownToken,
        current_token: MarkdownToken,
        deeper_containing_block_quote_token: Optional[BlockQuoteMarkdownToken],
        had_weird_block_quote_in_list: bool,
    ) -> Tuple[str, str, bool, bool]:
        starting_whitespace = ""
        did_container_start_midline = False
        check_list_for_indent = True
        if do_perform_block_quote_ending:
            assert isinstance(previous_token, EndMarkdownToken)
            previous_block_quote_token = cast(
                BlockQuoteMarkdownToken, previous_token.start_markdown_token
            )
            assert previous_block_quote_token.bleading_spaces is not None
            split_leading_spaces = previous_block_quote_token.bleading_spaces.split(
                ParserHelper.newline_character
            )
            POGGER.debug(f"split_leading_spaces>>{split_leading_spaces}")
            POGGER.debug(
                f"current_token>>{ParserHelper.make_value_visible(current_token)}"
            )
            # if (
            #     current_token.is_new_list_item
            #     and len(split_leading_spaces) <= 2
            #     and False
            # ):
            #     block_quote_leading_space = ""
            #     starting_whitespace = ""
            # else:
            POGGER.debug(
                f">>{ParserHelper.make_value_visible(previous_token.start_markdown_token)}"
            )

            block_quote_leading_space = split_leading_spaces[-1]
            starting_whitespace = block_quote_leading_space
            did_container_start_midline = True
            # up to here?
            check_list_for_indent = False
        else:
            assert deeper_containing_block_quote_token is not None
            POGGER.debug(
                f"adj->deeper_containing_block_quote_token.line_number>>:{deeper_containing_block_quote_token.line_number}:<<"
            )

            POGGER.debug(
                f"adj->current_token.line_number>>:{current_token.line_number}:<<"
            )
            line_number_delta = (
                current_token.line_number
                - deeper_containing_block_quote_token.line_number
            )
            POGGER.debug(f"index:{line_number_delta}")
            assert deeper_containing_block_quote_token.bleading_spaces is not None
            split_leading_spaces = (
                deeper_containing_block_quote_token.bleading_spaces.split(
                    ParserHelper.newline_character
                )
            )
            POGGER.debug(
                f"split_leading_spaces:{ParserHelper.make_value_visible(split_leading_spaces)}"
            )

            block_quote_leading_space = split_leading_spaces[line_number_delta]
            if had_weird_block_quote_in_list:
                starting_whitespace = block_quote_leading_space
        return (
            block_quote_leading_space,
            starting_whitespace,
            did_container_start_midline,
            check_list_for_indent,
        )

    # pylint: disable=too-many-arguments
    @staticmethod
    def __rehydrate_list_start_calculate_start(
        current_token: ListStartMarkdownToken,
        next_token: MarkdownToken,
        extracted_whitespace: str,
        previous_indent: int,
        adjustment_since_newline: int,
        post_adjust_whitespace: Optional[str],
    ) -> str:
        start_sequence = (
            f"{extracted_whitespace}{current_token.list_start_sequence}"
            if current_token.is_unordered_list_start
            else f"{extracted_whitespace}{current_token.list_start_content}{current_token.list_start_sequence}"
        )
        POGGER.debug(f">>start_sequence>>:{start_sequence}:<<")
        old_start_sequence = start_sequence
        if next_token.is_blank_line:
            POGGER.debug("blank-line")
            POGGER.debug(f">>next_token.column_number>>:{next_token.column_number}:<<")
            POGGER.debug(
                f">>current_token.column_number>>:{current_token.column_number}:<<"
            )
            list_content_length = 1
            if not current_token.is_unordered_list_start:
                list_content_length += len(current_token.list_start_content)
            new_column_number = (
                next_token.column_number
                - current_token.column_number
                - list_content_length
            )
            start_sequence += ParserHelper.repeat_string(" ", new_column_number)
        elif next_token.is_list_end:
            POGGER.debug("list-end")
        else:
            POGGER.debug("not list-end and not blank-line")
            # POGGER.debug(
            #     f">>current_token>>:{ParserHelper.make_value_visible(current_token)}:<<"
            # )
            # POGGER.debug(
            #     f">>current_token.indent_level>>:{current_token.indent_level}:<<"
            # )
            POGGER.debug(f">>previous_indent>>:{previous_indent}:<<")
            POGGER.debug(f">>adjustment_since_newline>>:{adjustment_since_newline}:<<")
            requested_indent = (
                current_token.indent_level
                + len(extracted_whitespace)
                - (current_token.column_number - 1)
            )
            POGGER.debug(f">>requested_indent>>:{requested_indent}:<<")
            start_sequence = start_sequence.ljust(requested_indent, " ")
        POGGER.debug(
            f">>current_token>>:{ParserHelper.make_value_visible(current_token)}:<<"
        )
        POGGER.debug(f">>next_token>>:{ParserHelper.make_value_visible(next_token)}:<<")

        start_sequence = TransformListBlock.__rehydrate_list_start_calculate_start_calc(
            current_token,
            start_sequence,
            old_start_sequence,
            post_adjust_whitespace,
        )
        return start_sequence

    # pylint: enable=too-many-arguments

    @classmethod
    def __rehydrate_list_start_calculate_start_calc(
        cls,
        current_token: ListStartMarkdownToken,
        start_sequence: str,
        old_start_sequence: str,
        post_adjust_whitespace: Optional[str],
    ) -> str:
        POGGER.debug(f">>tabbed_adjust>>:{str(current_token.tabbed_adjust)}:<<")
        if current_token.tabbed_adjust >= 0:
            POGGER.debug(f">>start_sequence>>:{start_sequence}:<<")
            POGGER.debug(f">>old_start_sequence>>:{old_start_sequence}:<<")
            spaces_to_consume = current_token.tabbed_adjust + 1
            POGGER.debug(f">>spaces_to_consume>>:{str(spaces_to_consume)}:<<")
            start_sequence = (
                start_sequence[: len(old_start_sequence)]
                + "\t"
                + start_sequence[len(old_start_sequence) + spaces_to_consume :]
            )
            POGGER.debug(
                f">>start_sequence>>:{ParserHelper.make_value_visible(start_sequence)}:<<"
            )

        POGGER.debug(f"<<start_sequence<<:{start_sequence}:<<")
        if post_adjust_whitespace:
            POGGER.debug(
                f"<<post_adjust_whitespace<<(post):{post_adjust_whitespace}:<<"
            )
            start_sequence = post_adjust_whitespace + start_sequence
            POGGER.debug(f"<<start_sequence<<(post):{start_sequence}:<<")

        if current_token.tabbed_extracted_whitespace is not None:
            start_sequence = (
                current_token.tabbed_extracted_whitespace
                + start_sequence[len(current_token.extracted_whitespace) :]
            )
        return start_sequence
