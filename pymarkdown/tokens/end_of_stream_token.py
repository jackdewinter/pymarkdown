"""
Module to provide for an encapsulation of the end of stream element.
"""

from typing import Optional

from typing import List, Optional

from pymarkdown.tokens.html_items import HtmlItems
from pymarkdown.tokens.markdown_token import MarkdownToken, MarkdownTokenClass
from pymarkdown.transform_gfm.transform_state import TransformState
from pymarkdown.transform_markdown.markdown_transform_context import (
    MarkdownTransformContext,
    RegisterHtmlTransformHandlersProtocol,
    RegisterMarkdownTransformHandlersProtocol,
)


class SpecialMarkdownToken(MarkdownToken):
    """
    Class to provide for an encapsulation of special stream elements.
    """

    def __init__(
        self,
        token_name: str,
        extra_data: Optional[str],
        line_number: int = 0,
        is_special: bool = True,
    ):
        """
        Initialize an instance of the SpecialMarkdownToken class.
        """
        MarkdownToken.__init__(
            self,
            token_name,
            MarkdownTokenClass.SPECIAL,
            extra_data,
            line_number=line_number,
            is_special=is_special,
        )


class EndOfStreamToken(SpecialMarkdownToken):
    """
    Class to provide for an encapsulation of the end of stream element.
    """

    def __init__(self, line_number: int) -> None:
        """
        Initialize an instance of the EndOfStreamToken class.
        """
        SpecialMarkdownToken.__init__(
            self, MarkdownToken._token_end_of_stream, None, line_number=line_number
        )

    # pylint: disable=protected-access
    @staticmethod
    def get_markdown_token_type() -> str:
        """
        Get the type of markdown token for rehydration purposes.
        """
        return MarkdownToken._token_end_of_stream

    # pylint: enable=protected-access

    def register_for_markdown_transform(
        self,
        registration_function: RegisterMarkdownTransformHandlersProtocol,
    ) -> None:
        """
        Register any rehydration handlers for leaf markdown tokens.
        """

        registration_function(
            EndOfStreamToken,
            EndOfStreamToken.__rehydrate_end_of_stream,
            None,
        )

    @staticmethod
    def __rehydrate_end_of_stream(
        context: MarkdownTransformContext,
        current_token: MarkdownToken,
        previous_token: Optional[MarkdownToken],
    ) -> str:
        """
        Rehydrate nothing, as this is a placeholder.
        """
        _ = context, current_token, previous_token
        return ""

    @staticmethod
    def register_for_html_transform(
        register_handlers: RegisterHtmlTransformHandlersProtocol,
    ) -> None:
        """
        Register any functions required to generate HTML from the tokens.
        """
        register_handlers(
            EndOfStreamToken,
            EndOfStreamToken.__handle_end_of_stream_token,
            None,
        )

    @staticmethod
    def __handle_end_of_stream_token(
        output_html: str,
        output_parts: List[HtmlItems],
        next_token: MarkdownToken,
        transform_state: TransformState,
    ) -> str:
        _ = (transform_state, next_token, output_parts)
        return output_html
