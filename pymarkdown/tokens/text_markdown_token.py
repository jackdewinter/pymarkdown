"""
Module to provide for an encapsulation of the text element.
"""

import logging
from typing import Optional, Tuple, cast

from pymarkdown.constants import Constants
from pymarkdown.parser_helper import ParserHelper
from pymarkdown.parser_logger import ParserLogger
from pymarkdown.position_marker import PositionMarker
from pymarkdown.tokens.inline_markdown_token import InlineMarkdownToken
from pymarkdown.tokens.markdown_token import MarkdownToken

POGGER = ParserLogger(logging.getLogger(__name__))


class TextMarkdownToken(InlineMarkdownToken):
    """
    Class to provide for an encapsulation of the text element.
    """

    # pylint: disable=too-many-arguments
    def __init__(
        self,
        token_text: str,
        extracted_whitespace: str,
        end_whitespace: Optional[str] = None,
        position_marker: Optional[PositionMarker] = None,
        line_number: int = 0,
        column_number: int = 0,
        is_special: bool = False,
        tabified_text: Optional[str] = None,
    ):
        (
            self.__token_text,
            self.__extracted_whitespace,
            self.__end_whitespace,
            self.__tabified_text,
        ) = (token_text, extracted_whitespace, end_whitespace, tabified_text)
        InlineMarkdownToken.__init__(
            self,
            MarkdownToken._token_text,
            "",
            position_marker=position_marker,
            line_number=line_number,
            column_number=column_number,
            is_special=is_special,
        )
        self.__compose_extra_data_field()

    # pylint: enable=too-many-arguments
    # pylint: disable=protected-access
    @staticmethod
    def get_markdown_token_type() -> str:
        """
        Get the type of markdown token for rehydration purposes.
        """
        return MarkdownToken._token_text

    # pylint: enable=protected-access

    def _set_token_text(self, new_text: str) -> None:
        self.__token_text = new_text
        self.__compose_extra_data_field()

    @property
    def token_text(self) -> str:
        """
        Returns the text associated with the token.
        """
        return self.__token_text

    @property
    def extracted_whitespace(self) -> str:
        """
        Returns any whitespace that was extracted before the processing of this element occurred.
        """
        return self.__extracted_whitespace

    @property
    def end_whitespace(self) -> Optional[str]:
        """
        Returns any whitespace that was extracted after the processing of this element occurred.
        """
        return self.__end_whitespace

    @property
    def tabified_text(self) -> Optional[str]:
        """
        Returns any text that had a tab character in it.
        """
        return self.__tabified_text

    def create_copy(self) -> "TextMarkdownToken":
        """
        Create a copy of this token.
        """
        return TextMarkdownToken(
            self.__token_text,
            self.__extracted_whitespace,
            self.__end_whitespace,
            line_number=self.line_number,
            column_number=self.column_number,
        )

    def __compose_extra_data_field(self) -> None:
        """
        Compose the object's self.extra_data field from the local object's variables.
        """

        data_field_parts = [self.__token_text, self.__extracted_whitespace]
        if self.__end_whitespace:
            data_field_parts.append(self.__end_whitespace)
            assert not self.__tabified_text
        elif self.__tabified_text:
            data_field_parts.extend(("", self.__tabified_text))
        self._set_extra_data(MarkdownToken.extra_data_separator.join(data_field_parts))

    def remove_final_whitespace(self) -> str:
        """
        Remove any final whitespace.  Used by paragraph blocks so that they do not
        end with a hard break.
        """

        removed_whitespace = ""
        # POGGER.debug("self.__tabified_text=:$:", self.__tabified_text)
        # POGGER.debug("self.__token_text=:$:", self.__token_text)
        (
            collected_whitespace_length,
            first_non_whitespace_index,
        ) = ParserHelper.collect_backwards_while_one_of_characters(
            self.__token_text, -1, Constants.ascii_whitespace
        )
        # POGGER.debug("collected_whitespace_length=:$:", collected_whitespace_length)
        # POGGER.debug("first_non_whitespace_index=:$:", first_non_whitespace_index)

        assert first_non_whitespace_index is not None
        if collected_whitespace_length:
            removed_whitespace = self.__token_text[
                first_non_whitespace_index : first_non_whitespace_index
                + collected_whitespace_length
            ]
            self.__token_text = self.__token_text[:first_non_whitespace_index]
            if self.__tabified_text:
                (
                    collected_whitespace_length,
                    first_non_whitespace_index,
                ) = ParserHelper.collect_backwards_while_one_of_characters(
                    self.__tabified_text, -1, Constants.ascii_whitespace
                )
                # POGGER.debug("collected_whitespace_length=:$:", collected_whitespace_length)
                # POGGER.debug("first_non_whitespace_index=:$:", first_non_whitespace_index)
                assert collected_whitespace_length is not None
                assert first_non_whitespace_index is not None
                removed_whitespace = self.__tabified_text[
                    first_non_whitespace_index : first_non_whitespace_index
                    + collected_whitespace_length
                ]
                self.__tabified_text = self.__tabified_text[:first_non_whitespace_index]
        self.__compose_extra_data_field()
        return removed_whitespace

    def combine(
        self, other_text_token: MarkdownToken, remove_leading_spaces: int
    ) -> str:
        """
        Combine the two text tokens together with a line feed between.
        If remove_leading_spaces > 0, then that many leading spaces will be
        removed from each line, if present.
        If remove_leading_spaces == -1, then.
        If remove_leading_spaces == 0, then.
        """

        if other_text_token.is_blank_line:
            text_to_combine = ""
            tabified_text_to_combine: Optional[str] = ""
            (
                whitespace_present,
                blank_line_sequence,
            ) = (
                other_text_token.extra_data,
                ParserHelper.replace_noop_character,
            )
        else:
            assert other_text_token.is_text
            text_other_token = cast(TextMarkdownToken, other_text_token)

            text_to_combine = text_other_token.token_text
            tabified_text_to_combine = text_other_token.tabified_text
            (
                whitespace_present,
                blank_line_sequence,
            ) = (
                text_other_token.extracted_whitespace,
                "",
            )

        removed_whitespace, prefix_whitespace = self.__combine_handle_whitespace(
            remove_leading_spaces, whitespace_present
        )

        if self.__tabified_text or tabified_text_to_combine:
            other_token_text = tabified_text_to_combine or text_to_combine

            this_token_text = self.__tabified_text or self.__token_text
            # POGGER.debug("this_token_text>:$:<", this_token_text)
            # POGGER.debug("blank_line_sequence>:$:<", blank_line_sequence)
            # POGGER.debug("prefix_whitespace>:$:<", prefix_whitespace)
            # POGGER.debug("other_token_text>:$:<", other_token_text)

            self.__tabified_text = (
                f"{this_token_text}{ParserHelper.newline_character}{blank_line_sequence}"
                + f"{prefix_whitespace}{other_token_text}"
            )
        self.__token_text = (
            f"{self.__token_text}{ParserHelper.newline_character}{blank_line_sequence}"
            + f"{prefix_whitespace}{text_to_combine}"
        )
        self.__compose_extra_data_field()
        return removed_whitespace

    def __combine_handle_whitespace(
        self, remove_leading_spaces: int, whitespace_present: Optional[str]
    ) -> Tuple[str, str]:
        prefix_whitespace = ""
        whitespace_to_append, removed_whitespace = None, ""
        if not remove_leading_spaces:
            assert whitespace_present is not None
            prefix_whitespace = whitespace_present
        elif remove_leading_spaces == -1:
            whitespace_to_append, prefix_whitespace = whitespace_present, ""
        else:
            assert whitespace_present is not None
            whitespace_present_size = len(whitespace_present)
            POGGER.debug(
                "whitespace_present>>$>>$<<",
                whitespace_present_size,
                whitespace_present,
            )
            POGGER.debug("remove_leading_spaces>>$<<", remove_leading_spaces)
            if whitespace_present_size < remove_leading_spaces:
                removed_whitespace, prefix_whitespace = whitespace_present, ""
            else:
                removed_whitespace, prefix_whitespace = (
                    whitespace_present[:remove_leading_spaces],
                    whitespace_present[remove_leading_spaces:],
                )

        if whitespace_to_append is not None:
            self.__extracted_whitespace = (
                f"{self.__extracted_whitespace}"
                + f"{ParserHelper.newline_character}{whitespace_to_append}"
            )
        return removed_whitespace, prefix_whitespace
