"""
Module to provide for an encapsulation of the thematic break element.
"""

from typing import Callable, Optional, cast

from pymarkdown.parser_helper import ParserHelper
from pymarkdown.position_marker import PositionMarker
from pymarkdown.tokens.leaf_markdown_token import LeafMarkdownToken
from pymarkdown.tokens.markdown_token import MarkdownToken
from pymarkdown.transform_markdown.markdown_transform_context import (
    MarkdownTransformContext,
)


class ThematicBreakMarkdownToken(LeafMarkdownToken):
    """
    Class to provide for an encapsulation of the thematic break element.
    """

    def __init__(
        self,
        start_character: str,
        extracted_whitespace: Optional[str],
        rest_of_line: str,
        position_marker: PositionMarker,
    ) -> None:
        assert extracted_whitespace is not None
        self.__rest_of_line = rest_of_line
        LeafMarkdownToken.__init__(
            self,
            MarkdownToken._token_thematic_break,
            MarkdownToken.extra_data_separator.join(
                [start_character, extracted_whitespace, self.__rest_of_line]
            ),
            position_marker=position_marker,
            extracted_whitespace=extracted_whitespace,
        )

    # pylint: disable=protected-access
    @staticmethod
    def get_markdown_token_type() -> str:
        """
        Get the type of markdown token for rehydration purposes.
        """
        return MarkdownToken._token_thematic_break

    # pylint: enable=protected-access

    @property
    def rest_of_line(self) -> str:
        """
        Returns any whitespace that was extracted before the processing of this element occurred.
        """
        return self.__rest_of_line

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
            ThematicBreakMarkdownToken,
            ThematicBreakMarkdownToken.__rehydrate_thematic_break,
            None,
        )

    @staticmethod
    def __rehydrate_thematic_break(
        context: MarkdownTransformContext,
        current_token: MarkdownToken,
        previous_token: Optional[MarkdownToken],
    ) -> str:
        """
        Rehydrate the thematic break text from the token.
        """
        _ = previous_token, context

        current_thematic_token = cast(ThematicBreakMarkdownToken, current_token)
        return "".join(
            [
                current_thematic_token.extracted_whitespace,
                current_thematic_token.rest_of_line,
                ParserHelper.newline_character,
            ]
        )
