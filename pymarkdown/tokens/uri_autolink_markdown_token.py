"""
Module to provide for an encapsulation of the inline uri autolink element.
"""

from typing import Optional, cast

from pymarkdown.inline.inline_helper import InlineHelper
from pymarkdown.tokens.inline_markdown_token import InlineMarkdownToken
from pymarkdown.tokens.markdown_token import MarkdownToken
from pymarkdown.transform_gfm.transform_state import TransformState
from pymarkdown.transform_markdown.markdown_transform_context import (
    MarkdownTransformContext,
    RegisterHtmlTransformHandlersProtocol,
    RegisterMarkdownTransformHandlersProtocol,
)


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

    # pylint: disable=too-many-arguments
    def __init__(
        self,
        autolink_text: str,
        line_number: int,
        column_number: int,
        add_http_prefix: bool = False,
        add_angle_brackets: bool = True,
    ) -> None:
        self.__autolink_text = autolink_text
        self.__add_http_prefix = add_http_prefix
        self.__add_angle_brackets = add_angle_brackets
        InlineMarkdownToken.__init__(
            self,
            MarkdownToken._token_inline_uri_autolink,
            f"1:{self.__autolink_text}"
            if self.__add_http_prefix
            else self.__autolink_text,
            line_number=line_number,
            column_number=column_number,
        )

    # pylint: enable=too-many-arguments

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

    @property
    def add_http_prefix(self) -> bool:
        """
        Returns the whether a http prefix needs to be appended.
        """
        return self.__add_http_prefix

    @property
    def add_angle_brackets(self) -> bool:
        """
        Returns the whether rendered markdown needs to add angle brackets.
        """
        return self.__add_angle_brackets

    def register_for_markdown_transform(
        self, registration_function: RegisterMarkdownTransformHandlersProtocol
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
        if current_uri_token.add_http_prefix:
            return f"{current_uri_token.autolink_text}"
        prefix_char, suffix_char = (
            ("<", ">") if current_uri_token.add_angle_brackets else ("", "")
        )
        return (
            ""
            if context.block_stack[-1].is_inline_link
            else f"{prefix_char}{current_uri_token.autolink_text}{suffix_char}"
        )

    @staticmethod
    def register_for_html_transform(
        register_handlers: RegisterHtmlTransformHandlersProtocol,
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
                "http://" if autolink_token.add_http_prefix else "",
                "".join(tag_text_parts),
                '">',
                InlineHelper.append_text(
                    "", autolink_token.autolink_text, add_text_signature=False
                ),
                "</a>",
            ]
        )
