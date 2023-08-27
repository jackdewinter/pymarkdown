from typing import Optional

from pymarkdown.tokens.markdown_token import MarkdownToken, MarkdownTokenClass
from pymarkdown.transform_gfm.transform_state import TransformState
from pymarkdown.transform_markdown.markdown_transform_context import (
    MarkdownTransformContext,
    RegisterHtmlTransformHandlersProtocol,
    RegisterMarkdownTransformHandlersProtocol,
)


class SpecialMarkdownToken(MarkdownToken):
    def __init__(
        self,
        token_name: str,
        extra_data: Optional[str],
        line_number: int = 0,
        is_special: bool = True,
    ):
        MarkdownToken.__init__(
            self,
            token_name,
            MarkdownTokenClass.SPECIAL,
            extra_data,
            line_number=line_number,
            is_special=is_special,
        )


class EndOfStreamToken(SpecialMarkdownToken):
    def __init__(self, line_number: int) -> None:
        SpecialMarkdownToken.__init__(
            self, MarkdownToken._token_end_of_stream, None, line_number=line_number
        )

    @staticmethod
    def get_markdown_token_type() -> str:
        """
        Get the type of markdown token for rehydration purposes.
        """
        return MarkdownToken._token_end_of_stream

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
        next_token: MarkdownToken,
        transform_state: TransformState,
    ) -> str:
        _ = (transform_state, next_token)

        return output_html
