"""
Module to provide for an encapsulation of a generic list start element.
"""

# pylint: disable=too-many-instance-attributes
import logging
from typing import Optional

from pymarkdown.general.parser_helper import ParserHelper
from pymarkdown.general.parser_logger import ParserLogger
from pymarkdown.general.position_marker import PositionMarker
from pymarkdown.tokens.container_markdown_token import ContainerMarkdownToken
from pymarkdown.tokens.markdown_token import MarkdownToken
from pymarkdown.tokens.new_list_item_markdown_token import NewListItemMarkdownToken

POGGER = ParserLogger(logging.getLogger(__name__))


class ListStartMarkdownToken(ContainerMarkdownToken):
    """
    Class to provide for an encapsulation of a generic list start element.
    """

    # pylint: disable=too-many-arguments
    def __init__(
        self,
        token_name: str,
        position_marker: PositionMarker,
        list_start_sequence: str,
        list_start_content: str,
        indent_level: int,
        tabbed_adjust: int,
        extracted_whitespace: str,
        tabbed_whitespace_to_add: Optional[str],
    ) -> None:
        ContainerMarkdownToken.__init__(
            self,
            token_name,
            "",
            position_marker=position_marker,
        )
        POGGER.debug("tabbed_adjust>:$:<", tabbed_adjust)
        POGGER.debug("type(tabbed_adjust)>:$:<", type(tabbed_adjust))
        self.leading_spaces_index = 0
        self.is_loose = True
        (
            self.__list_start_sequence,
            self.__list_start_content,
            self.__indent_level,
            self.__extracted_whitespace,
            self.__tabbed_whitespace_to_add,
            self.__tabbed_adjust,
        ) = (
            list_start_sequence,
            list_start_content,
            indent_level,
            extracted_whitespace,
            tabbed_whitespace_to_add,
            tabbed_adjust,
        )
        self.__last_new_list_token: Optional[NewListItemMarkdownToken] = None
        self.__leading_spaces: Optional[str] = None
        self.__compose_extra_data_field()

    # pylint: enable=too-many-arguments

    @property
    def list_start_sequence(self) -> str:
        """
        Returns the sequence used to start this list element.
        """
        return self.__list_start_sequence

    @property
    def list_start_content(self) -> str:
        """
        Returns the content used to start this list element.
        """
        return self.__list_start_content

    @property
    def indent_level(self) -> int:
        """
        Returns the indent level to apply for the list element.
        """
        return self.__indent_level

    @property
    def extracted_whitespace(self) -> str:
        """
        Returns any whitespace that was extracted before the processing of this element occurred.
        """
        return self.__extracted_whitespace

    @property
    def tabbed_extracted_whitespace(self) -> Optional[str]:
        """
        extracted_whitespace, but with any tabs.
        """
        return self.__tabbed_whitespace_to_add

    @property
    def tabbed_adjust(self) -> int:
        """
        Adjustments for tabbed.
        """
        return self.__tabbed_adjust

    @property
    def leading_spaces(self) -> Optional[str]:
        """
        Returns the leading spaces that occur before the list element.
        """
        return self.__leading_spaces

    def reset_last_list_item(self) -> None:
        """
        Reset the last new list token seens for this list.
        """
        self.__last_new_list_token = None

    def adjust_for_new_list_item(
        self,
        new_list_item_token: NewListItemMarkdownToken,
        skip_adjustment: bool = False,
    ) -> None:
        """
        Adjust this token for a new list item (uses copy to keep track).
        """
        assert new_list_item_token and new_list_item_token.is_new_list_item

        self.__last_new_list_token = new_list_item_token

        if not skip_adjustment:
            self.__indent_level, self.__extracted_whitespace = (
                new_list_item_token.indent_level,
                new_list_item_token.extracted_whitespace,
            )

    def __compose_extra_data_field(self) -> None:
        """
        Compose the object's self.extra_data field from the local object's variables.
        """

        item_list = [
            self.__list_start_sequence,
            self.__list_start_content,
            str(self.__indent_level),
            self.__extracted_whitespace,
        ]
        is_leading_spaces_valid = self.__leading_spaces is not None
        is_tabbed_whitespace_valid = self.__tabbed_whitespace_to_add is not None
        is_tabbed_adjust_valid = (
            isinstance(self.__tabbed_adjust, int) and self.__tabbed_adjust >= 0
        )

        if (
            is_leading_spaces_valid
            or is_tabbed_whitespace_valid
            or is_tabbed_adjust_valid
        ):
            item_list.append(self.__leading_spaces or "")
        if is_tabbed_whitespace_valid or is_tabbed_adjust_valid:
            item_list.append(self.__tabbed_whitespace_to_add or "")
        if is_tabbed_adjust_valid:
            item_list.append(str(self.__tabbed_adjust))
        self._set_extra_data(MarkdownToken.extra_data_separator.join(item_list))

    def remove_last_leading_space(self) -> Optional[str]:
        """
        Remove the last leading space and return it.
        """
        assert self.__leading_spaces is not None
        last_separator_index = self.__leading_spaces.rfind("\n")
        if last_separator_index == -1:
            extracted_text = self.__leading_spaces
            self.__leading_spaces = None
        else:
            extracted_text = self.__leading_spaces[last_separator_index:]
            self.__leading_spaces = self.__leading_spaces[:last_separator_index]
        self.__compose_extra_data_field()
        return extracted_text

    def add_leading_spaces(self, ws_add: str) -> None:
        """
        Add any leading spaces to the token, separating them with line feeds.
        """
        POGGER.debug("__leading_spaces>>:$:<<", self.__leading_spaces)
        POGGER.debug("add_leading_spaces>>:$:<<", ws_add)
        self.__leading_spaces = (
            ws_add
            if self.__leading_spaces is None
            else f"{self.__leading_spaces}{ParserHelper.newline_character}{ws_add}"
        )
        POGGER.debug("__leading_spaces>>:$:<<", self.__leading_spaces)
        self.__compose_extra_data_field()

    @property
    def last_new_list_token(self) -> Optional[NewListItemMarkdownToken]:
        """
        Returns the last new-list token associated with this stack token.
        """
        return self.__last_new_list_token

    def set_extracted_whitespace(self, new_whitespace: str) -> None:
        """
        Set the extracted whitespace for the token.  To be used sparingly.
        """
        self.__extracted_whitespace = new_whitespace
        self.__compose_extra_data_field()


# pylint: enable=too-many-instance-attributes
