"""
Module to provide for an encapsulation of the thematic break element.
"""

from typing import Optional, Union, cast

from typing_extensions import override

from pymarkdown.general.parser_helper import ParserHelper
from pymarkdown.general.position_marker import PositionMarker
from pymarkdown.tokens.leaf_markdown_token import LeafMarkdownToken
from pymarkdown.tokens.markdown_token import MarkdownToken
from pymarkdown.transform_gfm.transform_state import TransformState
from pymarkdown.transform_markdown.markdown_transform_context import (
    MarkdownTransformContext,
    RegisterHtmlTransformHandlersProtocol,
    RegisterMarkdownTransformHandlersProtocol,
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
        self.__start_character = start_character
        self.__extracted_whitespace = extracted_whitespace
        self.__rest_of_line = rest_of_line
        LeafMarkdownToken.__init__(
            self,
            MarkdownToken._token_thematic_break,
            self.__compose_extra_data_field(),
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

    def __compose_extra_data_field(self) -> str:
        """
        Compose the object's self.extra_data field from the local object's variables.
        """
        x = MarkdownToken.extra_data_separator.join(
            [self.__start_character, self.__extracted_whitespace, self.__rest_of_line]
        )
        self._set_extra_data(x)
        return x

    @override
    def _modify_token(self, field_name: str, field_value: Union[str, int]) -> bool:
        if field_name == "start_character" and isinstance(field_value, str):
            self.__start_character = field_value
            self.__compose_extra_data_field()
            return True
        if field_name == "rest_of_line" and isinstance(field_value, str):
            self.__rest_of_line = field_value
            self.__compose_extra_data_field()
            return True
        return super()._modify_token(field_name, field_value)

    def register_for_markdown_transform(
        self, registration_function: RegisterMarkdownTransformHandlersProtocol
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

    @staticmethod
    def register_for_html_transform(
        register_handlers: RegisterHtmlTransformHandlersProtocol,
    ) -> None:
        """
        Register any functions required to generate HTML from the tokens.
        """
        register_handlers(
            ThematicBreakMarkdownToken,
            ThematicBreakMarkdownToken.__handle_thematic_break_token,
            None,
        )

    @staticmethod
    def __handle_thematic_break_token(
        output_html: str,
        next_token: MarkdownToken,
        transform_state: TransformState,
    ) -> str:
        _ = (next_token, transform_state)

        token_parts = [output_html]
        if output_html and output_html[-1] != ParserHelper.newline_character:
            token_parts.append(ParserHelper.newline_character)
        token_parts.extend(["<hr />", ParserHelper.newline_character])
        return "".join(token_parts)
