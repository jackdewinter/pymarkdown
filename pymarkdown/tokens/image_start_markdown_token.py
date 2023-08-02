"""
Module to provide for an encapsulation of the image element.
"""

import logging
from typing import Callable, Optional, cast

from pymarkdown.links.link_helper_properties import LinkHelperProperties
from pymarkdown.parser_helper import ParserHelper
from pymarkdown.parser_logger import ParserLogger
from pymarkdown.tokens.link_start_markdown_token import LinkStartMarkdownToken
from pymarkdown.tokens.markdown_token import MarkdownToken
from pymarkdown.tokens.reference_markdown_token import ReferenceMarkdownToken
from pymarkdown.transform_markdown.markdown_transform_context import (
    MarkdownTransformContext,
)
from pymarkdown.transform_state import TransformState

POGGER = ParserLogger(logging.getLogger(__name__))


class ImageStartMarkdownToken(ReferenceMarkdownToken):
    """
    Class to provide for an encapsulation of the image element.
    """

    # pylint: disable=too-many-arguments
    def __init__(
        self,
        image_alt_text: str,
        text_from_blocks: str,
        line_number: int,
        column_number: int,
        lhp: LinkHelperProperties,
    ) -> None:
        # assert lhp.label_type is not None
        # assert lhp.pre_inline_link is not None
        # assert lhp.inline_link is not None

        self.__image_alt_text = image_alt_text
        ReferenceMarkdownToken.__init__(
            self,
            lhp,
            ImageStartMarkdownToken.get_markdown_token_type(),
            self.__image_alt_text,
            text_from_blocks,
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
        return MarkdownToken._token_inline_image

    # pylint: enable=protected-access

    @property
    def image_alt_text(self) -> str:
        """
        Returns the text extracted from the blocks of the link, after processing.
        """
        return self.__image_alt_text

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
            ImageStartMarkdownToken,
            ImageStartMarkdownToken.__rehydrate_inline_image,
            None,
        )

    @staticmethod
    def __rehydrate_inline_image(
        context: MarkdownTransformContext,
        current_token: MarkdownToken,
        previous_token: Optional[MarkdownToken],
    ) -> str:
        """
        Rehydrate the image text from the token.
        """
        _ = previous_token

        if context.block_stack[-1].is_inline_link:
            return ""
        inline_current_token = cast(ImageStartMarkdownToken, current_token)
        POGGER.debug(
            f">>>>>>>>:{ParserHelper.make_value_visible(inline_current_token)}:<<<<<"
        )
        rehydrated_text = (
            ImageStartMarkdownToken.rehydrate_inline_image_text_from_token(
                inline_current_token
            )
        )
        POGGER.debug(
            f">>>>>>>>:{ParserHelper.make_value_visible(rehydrated_text)}:<<<<<"
        )
        return LinkStartMarkdownToken.insert_leading_whitespace_at_newlines(
            context, rehydrated_text
        )

    @staticmethod
    def rehydrate_inline_image_text_from_token(
        image_token: "ImageStartMarkdownToken",
    ) -> str:
        """
        Given an image token, rehydrate it's original text from the token.
        """
        return f"!{LinkStartMarkdownToken.rehydrate_inline_link_text_from_token(image_token)}"

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
            ImageStartMarkdownToken, ImageStartMarkdownToken.__handle_image_token, None
        )

    @classmethod
    def __handle_image_token(
        cls,
        output_html: str,
        next_token: MarkdownToken,
        transform_state: TransformState,
    ) -> str:
        _ = transform_state

        image_token = cast(ImageStartMarkdownToken, next_token)
        return "".join(
            [
                output_html,
                '<img src="',
                image_token.link_uri,
                '" alt="',
                image_token.image_alt_text,
                '" ',
                (
                    f'title="{image_token.link_title}" '
                    if image_token.link_title
                    else ""
                ),
                "/>",
            ]
        )
