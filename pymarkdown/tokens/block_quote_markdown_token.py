"""
Module to provide for an encapsulation of the block quote element.
"""

import logging
from typing import Dict, Optional

from pymarkdown.parser_helper import ParserHelper
from pymarkdown.parser_logger import ParserLogger
from pymarkdown.position_marker import PositionMarker
from pymarkdown.tokens.container_markdown_token import ContainerMarkdownToken
from pymarkdown.tokens.markdown_token import MarkdownToken

POGGER = ParserLogger(logging.getLogger(__name__))


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
