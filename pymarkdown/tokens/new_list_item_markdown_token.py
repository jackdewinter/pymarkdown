"""
Module to provide for an encapsulation of the new list item element.
"""

from typing import Union

from typing_extensions import override

from pymarkdown.general.parser_helper import ParserHelper
from pymarkdown.general.position_marker import PositionMarker
from pymarkdown.tokens.container_markdown_token import ContainerMarkdownToken
from pymarkdown.tokens.markdown_token import MarkdownToken
from pymarkdown.transform_gfm.transform_state import TransformState
from pymarkdown.transform_markdown.markdown_transform_context import (
    RegisterHtmlTransformHandlersProtocol,
)


class NewListItemMarkdownToken(ContainerMarkdownToken):
    """
    Class to provide for an encapsulation of the new list item element..
    """

    def __init__(
        self,
        indent_level: int,
        position_marker: PositionMarker,
        extracted_whitespace: str,
        list_start_content: str,
    ) -> None:
        self.__indent_level, self.__extracted_whitespace, self.__list_start_content = (
            indent_level,
            extracted_whitespace,
            list_start_content,
        )
        assert extracted_whitespace is not None
        ContainerMarkdownToken.__init__(
            self,
            MarkdownToken._token_new_list_item,
            self.__compose_extra_data_field(),
            position_marker=position_marker,
        )

    # pylint: disable=protected-access
    @staticmethod
    def get_markdown_token_type() -> str:
        """
        Get the type of markdown token for rehydration purposes.
        """
        return MarkdownToken._token_new_list_item

    # pylint: enable=protected-access

    @property
    def extracted_whitespace(self) -> str:
        """
        Returns any whitespace that was extracted before the processing of this element occurred.
        """
        return self.__extracted_whitespace

    @property
    def indent_level(self) -> int:
        """
        Returns the indent level to apply for the list element.
        """
        return self.__indent_level

    @property
    def list_start_content(self) -> str:
        """
        Returns the content used to start this list element.
        """
        return self.__list_start_content

    @override
    def _modify_token(self, field_name: str, field_value: Union[str, int]) -> bool:
        if field_name == "list_start_content" and isinstance(field_value, str):
            self.__list_start_content = field_value
            self.__compose_extra_data_field()
            return True
        return False

    def __compose_extra_data_field(self) -> str:
        """
        Compose the object's self.extra_data field from the local object's variables.
        """

        new_field = MarkdownToken.extra_data_separator.join(
            [
                str(self.__indent_level),
                self.__extracted_whitespace,
                self.__list_start_content,
            ]
        )
        self._set_extra_data(new_field)
        return new_field

    @staticmethod
    def register_for_html_transform(
        register_handlers: RegisterHtmlTransformHandlersProtocol,
    ) -> None:
        """
        Register any functions required to generate HTML from the tokens.
        """
        register_handlers(
            NewListItemMarkdownToken,
            NewListItemMarkdownToken.__handle_new_list_item_token,
            None,
        )

    @staticmethod
    def __handle_new_list_item_token(
        output_html: str,
        next_token: MarkdownToken,
        transform_state: TransformState,
    ) -> str:
        _ = next_token
        transform_state.add_trailing_text, transform_state.add_leading_text = (
            "</li>",
            "<li>",
        )
        token_parts = [output_html]
        if output_html and output_html[-1] == ">" and not output_html.endswith("</a>"):
            token_parts.append(ParserHelper.newline_character)
        return "".join(token_parts)
