"""
Module to provide for a leaf element that can be added to markdown parsing stream that handles front matter.
"""
import logging
from typing import Dict, List, Optional, Tuple, cast

from pymarkdown.general.parser_helper import ParserHelper
from pymarkdown.general.parser_logger import ParserLogger
from pymarkdown.general.position_marker import PositionMarker
from pymarkdown.tokens.leaf_markdown_token import LeafMarkdownToken
from pymarkdown.tokens.markdown_token import MarkdownToken
from pymarkdown.transform_gfm.transform_state import TransformState
from pymarkdown.transform_markdown.markdown_transform_context import (
    MarkdownTransformContext,
    RegisterHtmlTransformHandlersProtocol,
    RegisterMarkdownTransformHandlersProtocol,
)

POGGER = ParserLogger(logging.getLogger(__name__))


class FrontMatterMarkdownToken(LeafMarkdownToken):
    """
    Class to provide for an encapsulation of the front matter data.
    """

    # pylint: disable=too-many-arguments
    def __init__(
        self,
        start_boundary_line: str,
        end_boundary_line: str,
        collected_lines: List[str],
        matter_map: Dict[str, str],
        position_marker: PositionMarker,
    ) -> None:
        self.__start_boundary_line = start_boundary_line
        self.__end_boundary_line = end_boundary_line
        self.__collected_lines = collected_lines
        self.__matter_map = matter_map

        LeafMarkdownToken.__init__(
            self,
            MarkdownToken._token_front_matter,
            "",
            position_marker=position_marker,
            is_extension=True,
        )
        self.__compose_extra_data_field()

    # pylint: enable=too-many-arguments
    # pylint: disable=protected-access
    @staticmethod
    def get_markdown_token_type() -> str:
        """
        Get the type of markdown token for rehydration purposes.
        """
        return MarkdownToken._token_front_matter

    # pylint: enable=protected-access

    @property
    def start_boundary_line(self) -> str:
        """
        Returns the boundary line used to start the front matter block.
        """
        return self.__start_boundary_line

    @property
    def end_boundary_line(self) -> str:
        """
        Returns the boundary line used to stop the front matter block.
        """
        return self.__end_boundary_line

    @property
    def collected_lines(self) -> List[str]:
        """
        Returns the collected lines that comprise the front matter block.
        """
        return self.__collected_lines

    @property
    def matter_map(self) -> Dict[str, str]:
        """
        Returns the processed lines from the front matter block.
        """
        return self.__matter_map

    def __compose_extra_data_field(self) -> None:
        """
        Compose the object's self.extra_data field from the local object's variables.
        """
        self._set_extra_data(
            MarkdownToken.extra_data_separator.join(
                [
                    self.__start_boundary_line,
                    self.__end_boundary_line,
                    str(self.__collected_lines),
                    str(self.__matter_map),
                ]
            )
        )

    @classmethod
    def calculate_block_token_height(cls, last_token: MarkdownToken) -> int:
        """
        Calculate the height of the token with the given properties.
        """
        front_matter_token = cast(FrontMatterMarkdownToken, last_token)
        return 2 + len(front_matter_token.collected_lines)

    @classmethod
    def calculate_initial_whitespace(cls) -> Tuple[int, bool]:
        """
        Calculate the amount of whitespace for the token.
        """
        return 0, False

    def register_for_markdown_transform(
        self,
        registration_function: RegisterMarkdownTransformHandlersProtocol,
    ) -> None:
        """
        Register any rehydration handlers for leaf markdown tokens.
        """
        registration_function(
            FrontMatterMarkdownToken,
            FrontMatterMarkdownToken.__rehydrate_front_matter,
            None,
        )

    @staticmethod
    def __rehydrate_front_matter(
        context: MarkdownTransformContext,
        current_token: MarkdownToken,
        previous_token: Optional[MarkdownToken],
    ) -> str:
        """
        Rehydrate the front matter text from the token.
        """
        _ = previous_token, context

        front_mater_token = cast(FrontMatterMarkdownToken, current_token)
        front_matter_parts = [front_mater_token.start_boundary_line]
        front_matter_parts.extend(front_mater_token.collected_lines)
        front_matter_parts.extend([front_mater_token.end_boundary_line, ""])
        return ParserHelper.newline_character.join(front_matter_parts)

    @staticmethod
    def register_for_html_transform(
        register_handlers: RegisterHtmlTransformHandlersProtocol,
    ) -> None:
        """
        Register any functions required to generate HTML from the tokens.
        """
        register_handlers(
            FrontMatterMarkdownToken,
            FrontMatterMarkdownToken.__handle_front_matter_token,
            None,
        )

    @staticmethod
    def __handle_front_matter_token(
        output_html: str, next_token: MarkdownToken, transform_state: TransformState
    ) -> str:
        """
        Handle the front matter token.  Note that it does not contribute anything
        at all to the HTML output.
        """
        _ = (next_token, transform_state)

        return output_html
