import copy
import logging
from typing import List, Optional, Tuple, cast

from pymarkdown.general.parser_helper import ParserHelper
from pymarkdown.general.parser_logger import ParserLogger
from pymarkdown.tokens.block_quote_markdown_token import BlockQuoteMarkdownToken
from pymarkdown.tokens.list_start_markdown_token import ListStartMarkdownToken
from pymarkdown.tokens.markdown_token import EndMarkdownToken, MarkdownToken
from pymarkdown.transform_markdown.markdown_transform_context import (
    MarkdownTransformContext,
)

POGGER = ParserLogger(logging.getLogger(__name__))


class TransformBlockQuote:
    @staticmethod
    def rehydrate_block_quote(
        context: MarkdownTransformContext,
        current_token: MarkdownToken,
        previous_token: Optional[MarkdownToken],
        next_token: Optional[MarkdownToken],
        transformed_data: str,
    ) -> str:
        _ = (previous_token, transformed_data)

        current_block_token = cast(BlockQuoteMarkdownToken, current_token)
        (
            token_stack_index,
            are_tokens_viable,
            new_instance,
        ) = TransformBlockQuote.__rehydrate_block_quote_start(
            context, current_block_token
        )

        if are_tokens_viable:
            container_list_token = cast(
                ListStartMarkdownToken, context.container_token_stack[token_stack_index]
            )
            matching_list_token = (
                container_list_token.last_new_list_token or container_list_token
            )
            POGGER.debug(
                f">matching_list_token>{ParserHelper.make_value_visible(matching_list_token)}"
            )

            POGGER.debug(f">current_token.line_number>{current_token.line_number}")
            POGGER.debug(
                ">container_token_stack[token_stack_index].line_number>"
                + f"{container_list_token.line_number}"
            )

        if (
            are_tokens_viable
            and current_token.line_number == matching_list_token.line_number
        ):
            container_list_token = cast(
                ListStartMarkdownToken, context.container_token_stack[token_stack_index]
            )
            already_existing_whitespace = ParserHelper.repeat_string(
                " ", container_list_token.indent_level
            )
        else:
            already_existing_whitespace = None

        POGGER.debug(
            f">bquote>current_token>{ParserHelper.make_value_visible(current_token)}"
        )
        POGGER.debug(
            f">bquote>next_token>{ParserHelper.make_value_visible(next_token)}"
        )

        if (
            next_token
            and next_token.is_block_quote_start
            and current_token.line_number == next_token.line_number
        ):
            POGGER.debug(">bquote> will be done by following bquote>")
            selected_leading_sequence = ""
        else:
            POGGER.debug(f">bquote>bleading_spaces>{new_instance.bleading_spaces}<")
            POGGER.debug(
                f">bquote>tabbed_bleading_spaces>{ParserHelper.make_value_visible(new_instance.tabbed_bleading_spaces)}"
            )
            selected_leading_sequence = (
                new_instance.calculate_next_bleading_space_part()
            )
            POGGER.debug(
                f">bquote>selected_leading_sequence>{selected_leading_sequence}<"
            )

        POGGER.debug(
            f">bquote>already_existing_whitespace>:{already_existing_whitespace}:<"
        )
        POGGER.debug(
            f">bquote>selected_leading_sequence>:{selected_leading_sequence}:<"
        )
        if already_existing_whitespace and selected_leading_sequence.startswith(
            already_existing_whitespace
        ):
            selected_leading_sequence = selected_leading_sequence[
                len(already_existing_whitespace) :
            ]
            POGGER.debug(
                f">bquote>new selected_leading_sequence>{selected_leading_sequence}<"
            )
        return selected_leading_sequence

    @staticmethod
    def __rehydrate_block_quote_start(
        context: MarkdownTransformContext, current_token: BlockQuoteMarkdownToken
    ) -> Tuple[int, bool, BlockQuoteMarkdownToken]:
        POGGER.debug(
            f">bquote>tabbed_bleading_spaces>{ParserHelper.make_value_visible(current_token.tabbed_bleading_spaces)}"
        )
        new_instance = copy.deepcopy(current_token)
        POGGER.debug(
            f">bquote>tabbed_bleading_spaces>{ParserHelper.make_value_visible(new_instance.tabbed_bleading_spaces)}"
        )
        new_instance.leading_text_index = 0
        context.container_token_stack.append(new_instance)
        POGGER.debug(f">bquote>{ParserHelper.make_value_visible(new_instance)}")
        POGGER.debug(
            f">self.container_token_stack>{ParserHelper.make_value_visible(context.container_token_stack)}"
        )
        token_stack_index = TransformBlockQuote.__search_backward_for_block_quote_start(
            context
        )
        are_tokens_viable = (
            len(context.container_token_stack) > 1 and token_stack_index >= 0
        )
        POGGER.debug(f">are_tokens_viable>{are_tokens_viable}")
        return token_stack_index, are_tokens_viable, new_instance

    @staticmethod
    def __search_backward_for_block_quote_start(
        context: MarkdownTransformContext,
    ) -> int:
        token_stack_index = len(context.container_token_stack) - 2
        while (
            token_stack_index >= 0
            and context.container_token_stack[token_stack_index].is_block_quote_start
        ):
            token_stack_index -= 1
        POGGER.debug(f">token_stack_index>{token_stack_index}")
        POGGER.debug(
            f">token_stack_token-->{ParserHelper.make_value_visible(context.container_token_stack[token_stack_index])}"
        )
        return token_stack_index

    @staticmethod
    def rehydrate_block_quote_end(
        context: MarkdownTransformContext,
        current_token: MarkdownToken,
        actual_tokens: List[MarkdownToken],
        token_index: int,
    ) -> str:
        POGGER.debug(">>__rehydrate_block_quote_end")
        _ = current_token

        current_end_token = cast(EndMarkdownToken, current_token)
        current_start_token = cast(
            BlockQuoteMarkdownToken, current_end_token.start_markdown_token
        )

        POGGER.debug(
            f"current_start_block_token>:{ParserHelper.make_value_visible(current_start_token)}:<"
        )
        current_end_token_extra = current_end_token.extra_end_data
        POGGER.debug(
            f"current_end_token_extra>:{ParserHelper.make_value_visible(current_end_token_extra)}:<"
        )
        start_leading_index = current_start_token.leading_text_index
        assert current_start_token.bleading_spaces is not None
        split_start_leading = current_start_token.bleading_spaces.split(
            ParserHelper.newline_character
        )
        POGGER.debug(
            f"start_leading_index>>:{ParserHelper.make_value_visible(start_leading_index)}:<"
        )
        POGGER.debug(
            f"split_start_leading>>:{ParserHelper.make_value_visible(split_start_leading)}:<"
        )
        adjusted_end_string = (
            current_end_token_extra
            if start_leading_index + 1 < len(split_start_leading)
            and current_end_token_extra is not None
            else ""
        )
        POGGER.debug(
            f">>{ParserHelper.make_value_visible(actual_tokens[token_index:])}"
        )
        search_index = token_index + 1
        while (
            search_index < len(actual_tokens)
            and actual_tokens[search_index].is_container_end_token
        ):
            search_index += 1
        POGGER.debug(f">>{search_index}")
        any_non_container_end_tokens = search_index < len(actual_tokens)
        POGGER.debug(f">>{any_non_container_end_tokens}")

        del context.container_token_stack[-1]

        return adjusted_end_string
