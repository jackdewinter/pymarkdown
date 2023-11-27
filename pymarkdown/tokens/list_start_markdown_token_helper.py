from typing import cast

from pymarkdown.general.parser_helper import ParserHelper
from pymarkdown.tokens.list_start_markdown_token import ListStartMarkdownToken
from pymarkdown.tokens.markdown_token import MarkdownToken
from pymarkdown.transform_gfm.transform_state import TransformState
from pymarkdown.transform_gfm.transform_to_gfm_list_looseness import (
    TransformToGfmListLooseness,
)


class ListStartMarkdownTokenHelper:
    @staticmethod
    def handle_start_list_token(
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
            if int(list_token.list_start_content) != 1:
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
    def handle_end_list_token(
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
