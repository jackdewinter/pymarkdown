"""
Module to provide transformations for a new list item.
"""
import logging
from typing import Optional, cast

from pymarkdown.general.parser_helper import ParserHelper
from pymarkdown.general.parser_logger import ParserLogger
from pymarkdown.tokens.block_quote_markdown_token import BlockQuoteMarkdownToken
from pymarkdown.tokens.list_start_markdown_token import ListStartMarkdownToken
from pymarkdown.tokens.markdown_token import MarkdownToken
from pymarkdown.tokens.new_list_item_markdown_token import NewListItemMarkdownToken
from pymarkdown.transform_markdown.markdown_transform_context import (
    MarkdownTransformContext,
)
from pymarkdown.transform_markdown.transform_list_block import TransformListBlock

POGGER = ParserLogger(logging.getLogger(__name__))

# pylint: disable=too-few-public-methods


class TransformNewListItem:
    """
    Class to provide transformations for a new list item.
    """

    @staticmethod
    def rehydrate_next_list_item(
        context: MarkdownTransformContext,
        current_token: MarkdownToken,
        previous_token: Optional[MarkdownToken],
        next_token: Optional[MarkdownToken],
        transformed_data: str,
    ) -> str:
        """
        Rehydrate the next list item token.
        """
        _ = previous_token
        assert next_token is not None

        assert context.container_token_stack[-1].is_list_start
        assert isinstance(context.container_token_stack[-1], ListStartMarkdownToken)

        current_list_token = cast(NewListItemMarkdownToken, current_token)

        POGGER.debug("__rehydrate_next_list_item")
        context.container_token_stack[-1].adjust_for_new_list_item(current_list_token)

        (
            adjustment_since_newline,
            extracted_whitespace,
        ) = TransformListBlock.adjust_whitespace_for_block_quote(
            transformed_data, current_list_token.extracted_whitespace
        )
        POGGER.debug(f"rnli->adjustment_since_newline>:{adjustment_since_newline}:")
        POGGER.debug(f"rnli->extracted_whitespace>:{extracted_whitespace}:")

        did_container_start_midline = False
        had_weird_block_quote_in_list = False
        assert previous_token
        (
            previous_indent,
            extracted_whitespace2,
            _,
            post_adjust_whitespace,
            did_container_start_midline,
            had_weird_block_quote_in_list,
        ) = TransformListBlock.rehydrate_list_start_previous_token(
            context,
            current_list_token,
            previous_token,
            next_token,
            extracted_whitespace,
        )
        # else:
        #     previous_indent, post_adjust_whitespace = (0, None)
        POGGER.debug(f">>previous_indent>>{previous_indent}<<")
        POGGER.debug(f">>extracted_whitespace2>>{extracted_whitespace2}<<")
        POGGER.debug(f">>post_adjust_whitespace>>{post_adjust_whitespace}<<")
        POGGER.debug(
            f">>had_weird_block_quote_in_list>>{had_weird_block_quote_in_list}<<"
        )

        adjustment_since_newline = (
            TransformNewListItem.__recalc_adjustment_since_newline(
                context, adjustment_since_newline
            )
        )
        # assert len(post_adjust_whitespace) == adjustment_since_newline

        whitespace_to_use = (
            post_adjust_whitespace
            if did_container_start_midline or had_weird_block_quote_in_list
            else extracted_whitespace
        )

        POGGER.debug(f"rnli->whitespace_to_use>:{whitespace_to_use}:")
        POGGER.debug(f"rnli->adjustment_since_newline>:{adjustment_since_newline}:")
        POGGER.debug(f"rnli->extracted_whitespace>:{extracted_whitespace}:")
        start_sequence = (
            f"{whitespace_to_use}{current_list_token.list_start_content}"
            + f"{context.container_token_stack[-1].list_start_sequence}"
        )

        POGGER.debug(f"rnli->start_sequence>:{start_sequence}:")
        if next_token.is_blank_line:
            start_sequence = TransformNewListItem.__rehydrate_next_list_item_blank_line(
                start_sequence, current_list_token, next_token
            )
        else:
            start_sequence = (
                TransformNewListItem.__rehydrate_next_list_item_not_blank_line(
                    context,
                    start_sequence,
                    did_container_start_midline,
                    adjustment_since_newline,
                    had_weird_block_quote_in_list,
                    next_token,
                )
            )
        POGGER.debug(f"rnli->start_sequence>:{start_sequence}:")

        return start_sequence

    @staticmethod
    # pylint: disable=too-many-arguments
    def __rehydrate_next_list_item_not_blank_line(
        context: MarkdownTransformContext,
        start_sequence: str,
        did_container_start_midline: bool,
        adjustment_since_newline: int,
        had_weird_block_quote_in_list: bool,
        next_token: MarkdownToken,
    ) -> str:
        POGGER.debug("__rehydrate_next_list_item_not_blank_line")
        # POGGER.debug(f"start_sequence={start_sequence}=")
        # POGGER.debug(f"did_container_start_midline={did_container_start_midline}=")
        # POGGER.debug(f"adjustment_since_newline={adjustment_since_newline}=")

        assert context.container_token_stack[-1].is_list_start
        assert isinstance(context.container_token_stack[-1], ListStartMarkdownToken)

        if did_container_start_midline:
            POGGER.debug("did start midline")
            # POGGER.debug(f"next_token:{ParserHelper.make_value_visible(next_token)}")
            project_indent_level = context.container_token_stack[-1].indent_level
            if next_token and next_token.is_block_quote_start:
                next_block_token = cast(BlockQuoteMarkdownToken, next_token)
                next_block_quote_leading_space = (
                    next_block_token.calculate_next_bleading_space_part(
                        increment_index=False
                    )
                )
                # POGGER.debug(
                #     f"did start midline:next_block_quote_leading_space:{next_block_quote_leading_space}:"
                # )
                ex_whitespace, _ = ParserHelper.extract_spaces(
                    next_block_quote_leading_space, 0
                )
                assert ex_whitespace is not None
                # POGGER.debug(f"did start midline:ab:{ex_whitespace}:")
                project_indent_level -= ex_whitespace
            start_sequence = start_sequence.ljust(project_indent_level, " ")
        else:
            POGGER.debug("did not start midline")
            calculated_indent = (
                context.container_token_stack[-1].indent_level
                - adjustment_since_newline
            )
            POGGER.debug(
                f"calculated_indent:{calculated_indent} = indent_level:{context.container_token_stack[-1].indent_level} - adjustment_since_newline:{adjustment_since_newline}"
            )
            POGGER.debug(
                f"had_weird_block_quote_in_list:{had_weird_block_quote_in_list}"
            )
            if had_weird_block_quote_in_list:
                POGGER.debug(f"calculated_indent:{calculated_indent}")
                calculated_indent += 2
                POGGER.debug(f"calculated_indent:{calculated_indent}")
            POGGER.debug(
                f"rnli->calculated_indent={calculated_indent} = "
                + f"indent_level={context.container_token_stack[-1].indent_level} - "
                + f"adjustment_since_newline={adjustment_since_newline}"
            )
            POGGER.debug(f"start_sequence:{start_sequence}")
            start_sequence = start_sequence.ljust(calculated_indent, " ")

            # TODO This is a kludge.  The calc_indent is not properly computed.
            if not start_sequence.endswith(" "):
                start_sequence = f"{start_sequence} "
            POGGER.debug(f"start_sequence:{start_sequence}")
        return start_sequence

    # pylint: enable=too-many-arguments

    @staticmethod
    def __rehydrate_next_list_item_blank_line(
        start_sequence: str,
        current_token: NewListItemMarkdownToken,
        next_token: MarkdownToken,
    ) -> str:
        POGGER.debug(f">>next_token.column_number>>:{next_token.column_number}:<<")
        POGGER.debug(
            f">>current_token.column_number>>:{current_token.column_number}:<<"
        )
        start_content_length = 1
        if current_token.list_start_content:
            start_content_length += len(current_token.list_start_content)
        new_column_number = (
            next_token.column_number
            - current_token.column_number
            - start_content_length
        )
        start_sequence += ParserHelper.repeat_string(" ", new_column_number)
        return start_sequence

    @staticmethod
    def __recalc_adjustment_since_newline(
        context: MarkdownTransformContext, adjustment_since_newline: int
    ) -> int:
        assert not adjustment_since_newline
        POGGER.debug(
            f"rnli->container_token_stack>:{ParserHelper.make_value_visible(context.container_token_stack)}:"
        )
        stack_index = len(context.container_token_stack) - 1
        found_block_quote_token: Optional[BlockQuoteMarkdownToken] = None
        while stack_index >= 0:
            if context.container_token_stack[stack_index].is_block_quote_start:
                found_block_quote_token = cast(
                    BlockQuoteMarkdownToken, context.container_token_stack[stack_index]
                )
                break
            stack_index -= 1
        POGGER.debug(
            f"rnli->found_block_quote_token>:{ParserHelper.make_value_visible(found_block_quote_token)}:"
        )
        if found_block_quote_token:
            leading_space = found_block_quote_token.calculate_next_bleading_space_part(
                increment_index=False, delta=-1
            )
            POGGER.debug(f"rnli->leading_space>:{leading_space}:")
            adjustment_since_newline = len(leading_space)
        return adjustment_since_newline


# pylint: enable=too-few-public-methods
