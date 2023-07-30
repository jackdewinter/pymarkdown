"""
Module to provide for an encapsulation of the html block element.
"""

from typing import Callable, Optional

from pymarkdown.position_marker import PositionMarker
from pymarkdown.tokens.leaf_markdown_token import LeafMarkdownToken
from pymarkdown.tokens.markdown_token import MarkdownToken
from pymarkdown.transform_markdown.markdown_transform_context import (
    MarkdownTransformContext,
)


class HtmlBlockMarkdownToken(LeafMarkdownToken):
    """
    Class to provide for an encapsulation of the html block element.
    """

    def __init__(
        self, position_marker: PositionMarker, extracted_whitespace: str
    ) -> None:
        if position_marker:
            line_number, column_number = position_marker.line_number, (
                position_marker.index_number
                + position_marker.index_indent
                + 1
                - len(extracted_whitespace)
            )
        else:
            # TODO better way to do this.
            line_number, column_number = -1, -1

        LeafMarkdownToken.__init__(
            self,
            MarkdownToken._token_html_block,
            "",
            line_number=line_number,
            column_number=column_number,
            extracted_whitespace=extracted_whitespace,
            requires_end_token=True,
        )

    # pylint: disable=protected-access
    @staticmethod
    def get_markdown_token_type() -> str:
        """
        Get the type of markdown token for rehydration purposes.
        """
        return MarkdownToken._token_html_block

    # pylint: enable=protected-access

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
            HtmlBlockMarkdownToken,
            HtmlBlockMarkdownToken.__rehydrate_html_block,
            HtmlBlockMarkdownToken.__rehydrate_html_block_end,
        )

    @staticmethod
    def __rehydrate_html_block(
        context: MarkdownTransformContext,
        current_token: MarkdownToken,
        previous_token: Optional[MarkdownToken],
    ) -> str:
        """
        Rehydrate the html block from the token.
        """
        _ = (current_token, previous_token)

        context.block_stack.append(current_token)
        return ""

    @staticmethod
    def __rehydrate_html_block_end(
        context: MarkdownTransformContext,
        current_token: MarkdownToken,
        previous_token: Optional[MarkdownToken],
        next_token: Optional[MarkdownToken],
    ) -> str:
        """
        Rehydrate the end of the html block from the token.
        """
        _ = (current_token, previous_token, next_token)

        del context.block_stack[-1]
        return ""
