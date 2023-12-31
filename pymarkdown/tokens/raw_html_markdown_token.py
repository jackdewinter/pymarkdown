"""
Module to provide for an encapsulation of the inline raw html element.
"""

import logging
from typing import Optional, Union, cast

from typing_extensions import override

from pymarkdown.general.parser_helper import ParserHelper
from pymarkdown.general.parser_logger import ParserLogger
from pymarkdown.tokens.inline_markdown_token import InlineMarkdownToken
from pymarkdown.tokens.markdown_token import MarkdownToken
from pymarkdown.tokens.paragraph_markdown_token import ParagraphMarkdownToken
from pymarkdown.transform_gfm.transform_state import TransformState
from pymarkdown.transform_markdown.markdown_transform_context import (
    MarkdownTransformContext,
    RegisterHtmlTransformHandlersProtocol,
    RegisterMarkdownTransformHandlersProtocol,
)

POGGER = ParserLogger(logging.getLogger(__name__))


class RawHtmlMarkdownToken(InlineMarkdownToken):
    """
    Class to provide for an encapsulation of the inline raw html element.
    """

    def __init__(self, raw_tag: str, line_number: int, column_number: int) -> None:
        self.__raw_tag = raw_tag
        InlineMarkdownToken.__init__(
            self,
            MarkdownToken._token_inline_raw_html,
            self.__raw_tag,
            line_number=line_number,
            column_number=column_number,
        )

    # pylint: disable=protected-access
    @staticmethod
    def get_markdown_token_type() -> str:
        """
        Get the type of markdown token for rehydration purposes.
        """
        return MarkdownToken._token_inline_raw_html

    # pylint: enable=protected-access

    @property
    def raw_tag(self) -> str:
        """
        Returns the text that is the raw html tag.
        """
        return self.__raw_tag

    def register_for_markdown_transform(
        self, registration_function: RegisterMarkdownTransformHandlersProtocol
    ) -> None:
        """
        Register any rehydration handlers for leaf markdown tokens.
        """
        registration_function(
            RawHtmlMarkdownToken,
            RawHtmlMarkdownToken.__rehydrate_inline_raw_html,
            None,
        )

    @staticmethod
    def __rehydrate_inline_raw_html(
        context: MarkdownTransformContext,
        current_token: MarkdownToken,
        previous_token: Optional[MarkdownToken],
    ) -> str:
        """
        Rehydrate the email raw html from the token.
        """
        _ = previous_token

        if context.block_stack[-1].is_inline_link:
            return ""

        current_raw_token = cast(RawHtmlMarkdownToken, current_token)
        raw_text = ParserHelper.remove_all_from_text(current_raw_token.raw_tag)

        if context.block_stack[-1].is_paragraph:
            block_paragraph_token = cast(
                ParagraphMarkdownToken, context.block_stack[-1]
            )
            POGGER.debug(
                f"raw_html>>before>>{ParserHelper.make_value_visible(raw_text)}"
            )
            block_paragraph_token.rehydrate_index += (
                ParserHelper.count_newlines_in_text(raw_text)
            )
            POGGER.debug(
                f"raw_html>>after>>{ParserHelper.make_value_visible(raw_text)}"
            )
        return f"<{raw_text}>"

    @staticmethod
    def register_for_html_transform(
        register_handlers: RegisterHtmlTransformHandlersProtocol,
    ) -> None:
        """
        Register any functions required to generate HTML from the tokens.
        """
        register_handlers(
            RawHtmlMarkdownToken, RawHtmlMarkdownToken.__handle_raw_html_token, None
        )

    @staticmethod
    def __handle_raw_html_token(
        output_html: str,
        next_token: MarkdownToken,
        transform_state: TransformState,
    ) -> str:
        _ = transform_state

        raw_html_token = cast(RawHtmlMarkdownToken, next_token)
        return "".join(
            [
                output_html,
                "<",
                ParserHelper.resolve_all_from_text(raw_html_token.raw_tag),
                ">",
            ]
        )

    @override
    def _modify_token(self, field_name: str, field_value: Union[str, int]) -> bool:
        if field_name == "raw_tag" and isinstance(field_value, str):
            self.__raw_tag = field_value
            self._set_extra_data(field_value)
            return True
        return False
