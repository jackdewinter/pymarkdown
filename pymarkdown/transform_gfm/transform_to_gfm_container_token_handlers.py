"""
Module to provide for the handlers for container tokens to allow transformation into HTML.
"""
import logging
from typing import Callable, Optional, cast

from pymarkdown.parser_helper import ParserHelper
from pymarkdown.parser_logger import ParserLogger
from pymarkdown.tokens.container_markdown_token import (
    BlockQuoteMarkdownToken,
    ListStartMarkdownToken,
    NewListItemMarkdownToken,
    OrderedListStartMarkdownToken,
    UnorderedListStartMarkdownToken,
)
from pymarkdown.tokens.markdown_token import MarkdownToken
from pymarkdown.transform_gfm.transform_to_gfm_list_looseness import (
    TransformToGfmListLooseness,
)
from pymarkdown.transform_state import TransformState

POGGER = ParserLogger(logging.getLogger(__name__))

# pylint: disable=too-few-public-methods


class TransformToGfmContainerTokenHandlers:
    """
    Module to provide for the handlers for container tokens to allow transformation into HTML.
    """

    @staticmethod
    def register_handlers(
        register_fn: Callable[
            [
                type,
                Callable[[str, MarkdownToken, TransformState], str],
                Optional[Callable[[str, MarkdownToken, TransformState], str]],
            ],
            None,
        ]
    ) -> None:
        """
        Register the handlers for this module.
        """

        register_fn(
            BlockQuoteMarkdownToken,
            TransformToGfmContainerTokenHandlers.__handle_start_block_quote_token,
            TransformToGfmContainerTokenHandlers.__handle_end_block_quote_token,
        )
        register_fn(
            NewListItemMarkdownToken,
            TransformToGfmContainerTokenHandlers.__handle_new_list_item_token,
            None,
        )
        register_fn(
            OrderedListStartMarkdownToken,
            TransformToGfmContainerTokenHandlers.__handle_start_list_token,
            TransformToGfmContainerTokenHandlers.__handle_end_list_token,
        )
        register_fn(
            UnorderedListStartMarkdownToken,
            TransformToGfmContainerTokenHandlers.__handle_start_list_token,
            TransformToGfmContainerTokenHandlers.__handle_end_list_token,
        )

    @staticmethod
    def __handle_start_block_quote_token(
        output_html: str,
        next_token: MarkdownToken,
        transform_state: TransformState,
    ) -> str:
        _ = next_token

        token_parts = [output_html]
        if output_html and output_html[-1] != ParserHelper.newline_character:
            token_parts.append(ParserHelper.newline_character)
        transform_state.is_in_loose_list = True
        token_parts.extend(["<blockquote>", ParserHelper.newline_character])
        return "".join(token_parts)

    @staticmethod
    def __handle_end_block_quote_token(
        output_html: str,
        next_token: MarkdownToken,
        transform_state: TransformState,
    ) -> str:
        _ = next_token

        token_parts = [output_html]
        if output_html[-1] != ParserHelper.newline_character:
            token_parts.append(ParserHelper.newline_character)
        transform_state.is_in_loose_list = (
            TransformToGfmListLooseness.reset_list_looseness(
                transform_state.actual_tokens,
                transform_state.actual_token_index,
            )
        )
        token_parts.extend(["</blockquote>", ParserHelper.newline_character])
        return "".join(token_parts)

    @staticmethod
    def __handle_new_list_item_token(
        output_html: str,
        next_token: MarkdownToken,
        transform_state: TransformState,
    ) -> str:
        _ = next_token
        transform_state.add_trailing_text, transform_state.add_leading_text = (
            "</li>",
            "<li>",
        )
        token_parts = [output_html]
        if output_html and output_html[-1] == ">" and not output_html.endswith("</a>"):
            token_parts.append(ParserHelper.newline_character)
        return "".join(token_parts)

    @staticmethod
    def __handle_start_list_token(
        output_html: str,
        next_token: MarkdownToken,
        transform_state: TransformState,
    ) -> str:
        list_token = cast(ListStartMarkdownToken, next_token)
        transform_state.is_in_loose_list = (
            TransformToGfmListLooseness.calculate_list_looseness(
                transform_state.actual_tokens,
                transform_state.actual_token_index,
                list_token,
            )
        )
        if list_token.is_ordered_list_start:
            token_parts = ["<ol"]
            if list_token.list_start_content != "1":
                token_parts.extend(
                    [' start="', str(int(list_token.list_start_content)), '"']
                )
            token_parts.extend([">", ParserHelper.newline_character, "<li>"])
            transform_state.add_leading_text = "".join(token_parts)
        else:
            transform_state.add_leading_text = "".join(
                ["<ul>", ParserHelper.newline_character, "<li>"]
            )
        return output_html

    @staticmethod
    def __handle_end_list_token(
        output_html: str,
        next_token: MarkdownToken,
        transform_state: TransformState,
    ) -> str:
        transform_state.is_in_loose_list = (
            TransformToGfmListLooseness.reset_list_looseness(
                transform_state.actual_tokens,
                transform_state.actual_token_index,
            )
        )
        transform_state.add_trailing_text = "".join(
            [
                "</li>",
                ParserHelper.newline_character,
                "</ul>" if next_token.is_unordered_list_end else "</ol>",
            ]
        )
        return output_html


# pylint: enable=too-few-public-methods
