"""
Module to provide for an encapsulation of the inline email autolink element.
"""

from typing import Callable, Optional, cast

from pymarkdown.tokens.inline_markdown_token import InlineMarkdownToken
from pymarkdown.tokens.markdown_token import MarkdownToken
from pymarkdown.transform_markdown.markdown_transform_context import (
    MarkdownTransformContext,
)
from pymarkdown.transform_state import TransformState


class EmailAutolinkMarkdownToken(InlineMarkdownToken):
    """
    Class to provide for an encapsulation of the inline email autolink element.
    """

    def __init__(
        self, autolink_text: str, line_number: int, column_number: int
    ) -> None:
        self.__autolink_text = autolink_text
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

    def register_for_markdown_transform(
        self,
        registration_function: Callable[
            [
                type,
                Callable[
                    [MarkdownTransformContext, MarkdownToken, Optional[MarkdownToken]],
                    str,
                ],
                Optional[
                    Callable[
                        [
                            MarkdownTransformContext,
                            MarkdownToken,
                            Optional[MarkdownToken],
                            Optional[MarkdownToken],
                        ],
                        str,
                    ]
                ],
            ],
            None,
        ],
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
        return (
            ""
            if context.block_stack[-1].is_inline_link
            else f"<{current_email_token.autolink_text}>"
        )

    @staticmethod
    def register_for_html_transform(
        register_handlers: Callable[
            [
                type,
                Callable[[str, MarkdownToken, TransformState], str],
                Optional[Callable[[str, MarkdownToken, TransformState], str]],
            ],
            None,
        ]
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
