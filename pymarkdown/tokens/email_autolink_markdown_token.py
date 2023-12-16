"""
Module to provide for an encapsulation of the inline email autolink element.
"""

from typing import Optional, cast

from pymarkdown.tokens.inline_markdown_token import InlineMarkdownToken
from pymarkdown.tokens.markdown_token import MarkdownToken
from pymarkdown.transform_gfm.transform_state import TransformState
from pymarkdown.transform_markdown.markdown_transform_context import (
    MarkdownTransformContext,
    RegisterHtmlTransformHandlersProtocol,
    RegisterMarkdownTransformHandlersProtocol,
)


class EmailAutolinkMarkdownToken(InlineMarkdownToken):
    """
    Class to provide for an encapsulation of the inline email autolink element.
    """

    def __init__(
        self,
        autolink_text: str,
        line_number: int,
        column_number: int,
        add_angle_brackets: bool = True,
    ) -> None:
        self.__autolink_text = autolink_text
        self.__add_angle_brackets = add_angle_brackets
        InlineMarkdownToken.__init__(
            self,
            MarkdownToken._token_inline_email_autolink,
            self.__autolink_text,
            line_number=line_number,
            column_number=column_number,
        )

    # pylint: disable=protected-access
    @staticmethod
    def get_markdown_token_type() -> str:
        """
        Get the type of markdown token for rehydration purposes.
        """
        return MarkdownToken._token_inline_email_autolink

    # pylint: enable=protected-access

    @property
    def autolink_text(self) -> str:
        """
        Returns the text that is the autolink.
        """
        return self.__autolink_text

    @property
    def add_angle_brackets(self) -> bool:
        """
        Returns whether to add angle brackets.
        """
        return self.__add_angle_brackets

    def register_for_markdown_transform(
        self, registration_function: RegisterMarkdownTransformHandlersProtocol
    ) -> None:
        """
        Register any rehydration handlers for leaf markdown tokens.
        """
        registration_function(
            EmailAutolinkMarkdownToken,
            EmailAutolinkMarkdownToken.__rehydrate_inline_email_autolink,
            None,
        )

    @staticmethod
    def __rehydrate_inline_email_autolink(
        context: MarkdownTransformContext,
        current_token: MarkdownToken,
        previous_token: Optional[MarkdownToken],
    ) -> str:
        """
        Rehydrate the email autolink from the token.
        """
        _ = previous_token

        current_email_token = cast(EmailAutolinkMarkdownToken, current_token)
        prefix_char = "<"
        suffix_char = ">"
        if not current_email_token.add_angle_brackets:
            prefix_char = ""
            suffix_char = ""
        return (
            ""
            if context.block_stack[-1].is_inline_link
            else f"{prefix_char}{current_email_token.autolink_text}{suffix_char}"
        )

    @staticmethod
    def register_for_html_transform(
        register_handlers: RegisterHtmlTransformHandlersProtocol,
    ) -> None:
        """
        Register any functions required to generate HTML from the tokens.
        """
        register_handlers(
            EmailAutolinkMarkdownToken,
            EmailAutolinkMarkdownToken.__handle_email_autolink_token,
            None,
        )

    @classmethod
    def __handle_email_autolink_token(
        cls,
        output_html: str,
        next_token: MarkdownToken,
        transform_state: TransformState,
    ) -> str:
        _ = transform_state

        email_token = cast(EmailAutolinkMarkdownToken, next_token)
        return "".join(
            [
                output_html,
                '<a href="mailto:',
                email_token.autolink_text,
                '">',
                email_token.autolink_text,
                "</a>",
            ]
        )
