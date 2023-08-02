"""
Module to provide for an encapsulation of the inline uri autolink element.
"""

from typing import Callable, Optional, cast

from pymarkdown.inline.inline_helper import InlineHelper
from pymarkdown.tokens.inline_markdown_token import InlineMarkdownToken
from pymarkdown.tokens.markdown_token import MarkdownToken
from pymarkdown.transform_markdown.markdown_transform_context import (
    MarkdownTransformContext,
)
from pymarkdown.transform_state import TransformState


class UriAutolinkMarkdownToken(InlineMarkdownToken):
    """
    Class to provide for an encapsulation of the inline uri autolink element.
    """

    __uri_autolink_html_character_escape_map = {
        "<": "&lt;",
        ">": "&gt;",
        "&": "&amp;",
    }

    __raw_html_percent_escape_ascii_chars = '"%[\\]^`{}|'

    def __init__(
        self, autolink_text: str, line_number: int, column_number: int
    ) -> None:
        self.__autolink_text = autolink_text
        InlineMarkdownToken.__init__(
            self,
            MarkdownToken._token_inline_uri_autolink,
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
        return MarkdownToken._token_inline_uri_autolink

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
            UriAutolinkMarkdownToken,
            UriAutolinkMarkdownToken.__rehydrate_inline_uri_autolink,
            None,
        )

    @staticmethod
    def __rehydrate_inline_uri_autolink(
        context: MarkdownTransformContext,
        current_token: MarkdownToken,
        previous_token: Optional[MarkdownToken],
    ) -> str:
        """
        Rehydrate the uri autolink from the token.
        """
        _ = previous_token

        current_uri_token = cast(UriAutolinkMarkdownToken, current_token)
        return (
            ""
            if context.block_stack[-1].is_inline_link
            else f"<{current_uri_token.autolink_text}>"
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
            UriAutolinkMarkdownToken,
            UriAutolinkMarkdownToken.__handle_uri_autolink,
            None,
        )

    @classmethod
    def __handle_uri_autolink(
        cls,
        output_html: str,
        next_token: MarkdownToken,
        transform_state: TransformState,
    ) -> str:
        _ = transform_state

        autolink_token = cast(UriAutolinkMarkdownToken, next_token)
        in_tag_pretext = InlineHelper.append_text(
            "",
            autolink_token.autolink_text,
            alternate_escape_map=UriAutolinkMarkdownToken.__uri_autolink_html_character_escape_map,
            add_text_signature=False,
        )

        tag_text_parts = []
        for next_character in in_tag_pretext:
            if (
                next_character
                in UriAutolinkMarkdownToken.__raw_html_percent_escape_ascii_chars
            ):
                tag_text_parts.extend(["%", (hex(ord(next_character))[2:]).upper()])
            elif ord(next_character) >= 128:
                encoded_data = next_character.encode("utf8")
                for encoded_byte in encoded_data:
                    tag_text_parts.extend(["%", (hex(encoded_byte)[2:]).upper()])
            else:
                tag_text_parts.append(next_character)

        return "".join(
            [
                output_html,
                '<a href="',
                "".join(tag_text_parts),
                '">',
                InlineHelper.append_text(
                    "", autolink_token.autolink_text, add_text_signature=False
                ),
                "</a>",
            ]
        )
