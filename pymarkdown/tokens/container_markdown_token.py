"""
Module to provide for a container element that can be added to markdown parsing stream.
"""
import logging
from typing import Dict, Optional

from pymarkdown.parser_helper import ParserHelper
from pymarkdown.parser_logger import ParserLogger
from pymarkdown.position_marker import PositionMarker
from pymarkdown.tokens.markdown_token import MarkdownToken, MarkdownTokenClass

POGGER = ParserLogger(logging.getLogger(__name__))


# pylint: disable=too-many-arguments
class ContainerMarkdownToken(MarkdownToken):
    """
    Class to provide for a container element that can be added to markdown parsing stream.
    """

    def __init__(
        self,
        token_name: str,
        extra_data: str,
        line_number: int = 0,
        column_number: int = 0,
        position_marker: Optional[PositionMarker] = None,
    ) -> None:
        MarkdownToken.__init__(
            self,
            token_name,
            MarkdownTokenClass.CONTAINER_BLOCK,
            extra_data,
            line_number=line_number,
            column_number=column_number,
            position_marker=position_marker,
            requires_end_token=True,
        )


# pylint: enable=too-many-arguments


class NewListItemMarkdownToken(ContainerMarkdownToken):
    """
    Class to provide for an encapsulation of the new list item element.
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
            MarkdownToken.extra_data_separator.join(
                [str(indent_level), extracted_whitespace, list_start_content]
            ),
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


# pylint: disable=too-many-instance-attributes
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

    def adjust_for_new_list_item(
        self, new_list_item_token: NewListItemMarkdownToken
    ) -> None:
        """
        Adjust this token for a new list item (uses copy to keep track).
        """
        assert new_list_item_token and new_list_item_token.is_new_list_item

        self.__last_new_list_token = new_list_item_token

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
        assert last_separator_index == -1
        extracted_text = self.__leading_spaces
        self.__leading_spaces = None
        # else:
        #     extracted_text = self.__leading_spaces[last_separator_index:]
        #     self.__leading_spaces = self.__leading_spaces[:last_separator_index]
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


class OrderedListStartMarkdownToken(ListStartMarkdownToken):
    """
    Class to provide for an encapsulation of the ordered list start element.
    """

    # pylint: disable=too-many-arguments
    def __init__(
        self,
        list_start_sequence: str,
        list_start_content: str,
        indent_level: int,
        tabbed_adjust: int,
        extracted_whitespace: str,
        tabbed_whitespace_to_add: Optional[str],
        position_marker: PositionMarker,
    ) -> None:
        ListStartMarkdownToken.__init__(
            self,
            MarkdownToken._token_ordered_list_start,
            position_marker,
            list_start_sequence,
            list_start_content,
            indent_level,
            tabbed_adjust,
            extracted_whitespace,
            tabbed_whitespace_to_add,
        )

    # pylint: enable=too-many-arguments
    # pylint: disable=protected-access
    @staticmethod
    def get_markdown_token_type() -> str:
        """
        Get the type of markdown token for rehydration purposes.
        """
        return MarkdownToken._token_ordered_list_start

    # pylint: enable=protected-access


class UnorderedListStartMarkdownToken(ListStartMarkdownToken):
    """
    Class to provide for an encapsulation of the unordered list start element.
    """

    # pylint: disable=too-many-arguments
    def __init__(
        self,
        list_start_sequence: str,
        indent_level: int,
        tabbed_adjust: int,
        extracted_whitespace: str,
        tabbed_whitespace_to_add: Optional[str],
        position_marker: PositionMarker,
    ) -> None:
        ListStartMarkdownToken.__init__(
            self,
            MarkdownToken._token_unordered_list_start,
            position_marker,
            list_start_sequence,
            "",
            indent_level,
            tabbed_adjust,
            extracted_whitespace,
            tabbed_whitespace_to_add,
        )

    # pylint: enable=too-many-arguments
    # pylint: disable=protected-access
    @staticmethod
    def get_markdown_token_type() -> str:
        """
        Get the type of markdown token for rehydration purposes.
        """
        return MarkdownToken._token_unordered_list_start

    # pylint: enable=protected-access


class BlockQuoteMarkdownToken(ContainerMarkdownToken):
    """
    Class to provide for an encapsulation of the block quote element.
    """

    def __init__(
        self, extracted_whitespace: str, position_marker: PositionMarker
    ) -> None:
        self.__extracted_whitespace, self.__leading_spaces, self.leading_text_index = (
            extracted_whitespace,
            "",
            0,
        )
        self.__tabbed_leading_spaces: Dict[int, str] = {}
        ContainerMarkdownToken.__init__(
            self,
            MarkdownToken._token_block_quote,
            "",
            position_marker=position_marker,
        )
        self.__compose_extra_data_field()

    # pylint: disable=protected-access
    @staticmethod
    def get_markdown_token_type() -> str:
        """
        Get the type of markdown token for rehydration purposes.
        """
        return MarkdownToken._token_block_quote

    # pylint: enable=protected-access

    @property
    def extracted_whitespace(self) -> str:
        """
        Returns any whitespace that was extracted before the processing of this element occurred.
        """
        return self.__extracted_whitespace

    @property
    def bleading_spaces(self) -> Optional[str]:
        """
        Returns any leading spaces that preface the block quote.
        """
        return self.__leading_spaces

    @property
    def tabbed_bleading_spaces(self) -> Dict[int, str]:
        """
        Returns the tabbed information for any leading spaces
        """
        return self.__tabbed_leading_spaces

    def add_bleading_spaces(
        self,
        leading_spaces_to_add: str,
        skip_adding_newline: bool = False,
        tabbed_leading_spaces: Optional[str] = None,
    ) -> None:
        """
        Add any leading spaces to the token, separating them with line feeds.
        """
        POGGER.debug(
            "__leading_spaces>>:$:<<",
            self.__leading_spaces,
        )
        POGGER.debug("add_leading_spaces>>:$:<<", leading_spaces_to_add)
        if skip_adding_newline:
            self.__leading_spaces = f"{self.__leading_spaces}{leading_spaces_to_add}"
        else:
            self.__leading_spaces = (
                f"{self.__leading_spaces}{ParserHelper.newline_character}{leading_spaces_to_add}"
                if self.__leading_spaces
                else leading_spaces_to_add
            )
        POGGER.debug(
            "__leading_spaces>>:$:<<",
            self.__leading_spaces,
        )
        if not skip_adding_newline and tabbed_leading_spaces:
            POGGER.debug(
                "__tabbed_leading_spaces>>:$:<<",
                self.__tabbed_leading_spaces,
            )
            newline_count = ParserHelper.count_newlines_in_text(self.__leading_spaces)
            self.__tabbed_leading_spaces[newline_count] = tabbed_leading_spaces
            POGGER.debug(
                "__tabbed_leading_spaces>>:$:<<",
                self.__tabbed_leading_spaces,
            )
        self.__compose_extra_data_field()

    def remove_last_bleading_space(self) -> str:
        """
        Remove the last leading space and return it.
        """
        last_separator_index = self.__leading_spaces.rfind("\n")
        if last_separator_index == -1:
            extracted_text = self.__leading_spaces
            self.__leading_spaces = ""
        else:
            extracted_text = self.__leading_spaces[last_separator_index:]
            self.__leading_spaces = self.__leading_spaces[:last_separator_index]
        self.leading_text_index -= 1
        self.__compose_extra_data_field()
        return extracted_text

    def __compose_extra_data_field(self) -> None:
        """
        Compose the object's self.extra_data field from the local object's variables.
        """
        item_list = [self.__extracted_whitespace, self.__leading_spaces]
        if self.__tabbed_leading_spaces:
            item_list.append(
                ParserHelper.make_value_visible(self.__tabbed_leading_spaces).replace(
                    "'", '"'
                )
            )
        self._set_extra_data(MarkdownToken.extra_data_separator.join(item_list))

    def calculate_next_bleading_space_part(
        self, increment_index: bool = True, delta: int = 0, allow_overflow: bool = False
    ) -> str:
        """
        Calculate the next leading space based on the leading_text_index,
        optonally incrementing it as well.
        """
        assert self.bleading_spaces is not None

        # print(f"increment_index>>:{increment_index}:<<")
        tabbed_leading = None
        if increment_index and self.__tabbed_leading_spaces:
            tabbed_leading = self.__tabbed_leading_spaces[self.leading_text_index]
            # print(f"dg>>:{ParserHelper.make_value_visible(dg)}:<<")

        split_leading_spaces = self.bleading_spaces.split(
            ParserHelper.newline_character
        )
        absolute_index = self.leading_text_index + delta
        if allow_overflow and absolute_index >= len(split_leading_spaces):
            leading_text = ""
        else:
            leading_text = split_leading_spaces[self.leading_text_index + delta]
            if increment_index:
                self.leading_text_index += 1

        if tabbed_leading is not None:
            leading_text = tabbed_leading

        return leading_text
