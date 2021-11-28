"""
Module to provide for a container element that can be added to markdown parsing stream.
"""
import logging

from pymarkdown.markdown_token import MarkdownToken, MarkdownTokenClass
from pymarkdown.parser_helper import ParserHelper
from pymarkdown.parser_logger import ParserLogger

POGGER = ParserLogger(logging.getLogger(__name__))


# pylint: disable=too-many-arguments
class ContainerMarkdownToken(MarkdownToken):
    """
    Class to provide for a container element that can be added to markdown parsing stream.
    """

    def __init__(
        self,
        token_name,
        extra_data,
        line_number=0,
        column_number=0,
        position_marker=None,
    ):
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
        self, indent_level, position_marker, extracted_whitespace, list_start_content
    ):
        self.__indent_level, self.__extracted_whitespace, self.__list_start_content = (
            indent_level,
            extracted_whitespace,
            list_start_content,
        )
        ContainerMarkdownToken.__init__(
            self,
            MarkdownToken._token_new_list_item,
            MarkdownToken.extra_data_separator.join(
                [str(indent_level), extracted_whitespace, list_start_content]
            ),
            position_marker=position_marker,
        )

    @property
    def extracted_whitespace(self):
        """
        Returns any whitespace that was extracted before the processing of this element occurred.
        """
        return self.__extracted_whitespace

    @property
    def indent_level(self):
        """
        Returns the indent level to apply for the list element.
        """
        return self.__indent_level

    @property
    def list_start_content(self):
        """
        Returns the content used to start this list element.
        """
        return self.__list_start_content


class OrderedListStartMarkdownToken(ContainerMarkdownToken):
    """
    Class to provide for an encapsulation of the ordered list start element.
    """

    # pylint: disable=too-many-arguments
    def __init__(
        self,
        list_start_sequence,
        list_start_content,
        indent_level,
        extracted_whitespace,
        position_marker,
    ):
        (
            self.__list_start_sequence,
            self.__list_start_content,
            self.__indent_level,
            self.__extracted_whitespace,
            self.__leading_spaces,
            self.is_loose,
            self.leading_spaces_index,
        ) = (
            list_start_sequence,
            list_start_content,
            indent_level,
            extracted_whitespace,
            None,
            True,
            0,
        )
        ContainerMarkdownToken.__init__(
            self,
            MarkdownToken._token_ordered_list_start,
            "",
            position_marker=position_marker,
        )
        self.__compose_extra_data_field()

    # pylint: enable=too-many-arguments

    @property
    def extracted_whitespace(self):
        """
        Returns any whitespace that was extracted before the processing of this element occurred.
        """
        return self.__extracted_whitespace

    @property
    def indent_level(self):
        """
        Returns the indent level to apply for the list element.
        """
        return self.__indent_level

    @property
    def list_start_sequence(self):
        """
        Returns the sequence used to start this list element.
        """
        return self.__list_start_sequence

    @property
    def list_start_content(self):
        """
        Returns the content used to start this list element.
        """
        return self.__list_start_content

    @property
    def leading_spaces(self):
        """
        Returns the leading spaces that occur before the list element.
        """
        return self.__leading_spaces

    def adjust_for_new_list_item(self, new_list_item_token):
        """
        Adjust this token for a new list item (uses copy to keep track).
        """
        assert new_list_item_token and new_list_item_token.is_new_list_item

        self.__indent_level, self.__extracted_whitespace = (
            new_list_item_token.indent_level,
            new_list_item_token.extracted_whitespace,
        )
        self.__compose_extra_data_field()

    def __compose_extra_data_field(self):
        """
        Compose the object's self.extra_data field from the local object's variables.
        """

        item_list = [
            self.__list_start_sequence,
            self.__list_start_content,
            str(self.__indent_level),
            self.__extracted_whitespace,
        ]
        if self.__leading_spaces is not None:
            item_list.append(self.__leading_spaces)
        self._set_extra_data(MarkdownToken.extra_data_separator.join(item_list))

    def add_leading_spaces(self, ws_add):
        """
        Add any leading spaces to the token, separating them with line feeds.
        """
        self.__leading_spaces = (
            ws_add
            if self.__leading_spaces is None
            else f"{self.__leading_spaces}{ParserHelper.newline_character}{ws_add}"
        )
        self.__compose_extra_data_field()


class UnorderedListStartMarkdownToken(ContainerMarkdownToken):
    """
    Class to provide for an encapsulation of the unordered list start element.
    """

    def __init__(
        self, list_start_sequence, indent_level, extracted_whitespace, position_marker
    ):
        (
            self.__list_start_sequence,
            self.__indent_level,
            self.__extracted_whitespace,
            self.__leading_spaces,
            self.is_loose,
            self.leading_spaces_index,
        ) = (list_start_sequence, indent_level, extracted_whitespace, None, True, 0)
        ContainerMarkdownToken.__init__(
            self,
            MarkdownToken._token_unordered_list_start,
            "",
            position_marker=position_marker,
        )
        self.__compose_extra_data_field()

    @property
    def extracted_whitespace(self):
        """
        Returns any whitespace that was extracted before the processing of this element occurred.
        """
        return self.__extracted_whitespace

    @property
    def indent_level(self):
        """
        Returns the indent level to apply for the list element.
        """
        return self.__indent_level

    @property
    def list_start_sequence(self):
        """
        Returns the sequence used to start this list element.
        """
        return self.__list_start_sequence

    @property
    def leading_spaces(self):
        """
        Returns the leading spaces that occur before the list element.
        """
        return self.__leading_spaces

    def adjust_for_new_list_item(self, new_list_item_token):
        """
        Adjust this token for a new list item (uses copy to keep track).
        """
        assert new_list_item_token and new_list_item_token.is_new_list_item

        self.__indent_level, self.__extracted_whitespace = (
            new_list_item_token.indent_level,
            new_list_item_token.extracted_whitespace,
        )
        self.__compose_extra_data_field()

    def __compose_extra_data_field(self):
        """
        Compose the object's self.extra_data field from the local object's variables.
        """

        item_list = [
            self.__list_start_sequence,
            "",
            str(self.__indent_level),
            self.__extracted_whitespace,
        ]
        if self.__leading_spaces is not None:
            item_list.append(self.__leading_spaces)
        self._set_extra_data(MarkdownToken.extra_data_separator.join(item_list))

    def add_leading_spaces(self, ws_add):
        """
        Add any leading spaces to the token, separating them with line feeds.
        """
        self.__leading_spaces = (
            ws_add
            if self.__leading_spaces is None
            else f"{self.__leading_spaces}{ParserHelper.newline_character}{ws_add}"
        )
        self.__compose_extra_data_field()


class BlockQuoteMarkdownToken(ContainerMarkdownToken):
    """
    Class to provide for an encapsulation of the block quote element.
    """

    def __init__(self, extracted_whitespace, position_marker):
        self.__extracted_whitespace, self.__leading_spaces, self.leading_text_index = (
            extracted_whitespace,
            "",
            0,
        )
        ContainerMarkdownToken.__init__(
            self,
            MarkdownToken._token_block_quote,
            "",
            position_marker=position_marker,
        )
        self.__compose_extra_data_field()

    @property
    def extracted_whitespace(self):
        """
        Returns any whitespace that was extracted before the processing of this element occurred.
        """
        return self.__extracted_whitespace

    @property
    def leading_spaces(self):
        """
        Returns any leading spaces that preface the block quote.
        """
        return self.__leading_spaces

    def add_leading_spaces(self, leading_spaces_to_add, skip_adding_newline=False):
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
        self.__compose_extra_data_field()

    def __compose_extra_data_field(self):
        """
        Compose the object's self.extra_data field from the local object's variables.
        """
        item_list = [self.__extracted_whitespace, self.__leading_spaces]
        self._set_extra_data(MarkdownToken.extra_data_separator.join(item_list))

    def calculate_next_leading_space_part(self, increment_index=True, delta=0):
        """
        Calculate the next leading space based on the leading_text_index,
        optonally incrementing it as well.
        """
        split_leading_spaces = self.leading_spaces.split(ParserHelper.newline_character)
        leading_text = split_leading_spaces[self.leading_text_index + delta]
        if increment_index:
            self.leading_text_index += 1
        return leading_text
