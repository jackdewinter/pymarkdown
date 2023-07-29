"""
Module to provide for an encapsulation of the fenced code block element.
"""

from pymarkdown.position_marker import PositionMarker
from pymarkdown.tokens.leaf_markdown_token import LeafMarkdownToken
from pymarkdown.tokens.markdown_token import MarkdownToken


class FencedCodeBlockMarkdownToken(LeafMarkdownToken):
    """
    Class to provide for an encapsulation of the fenced code block element.
    """

    # pylint: disable=too-many-arguments
    def __init__(
        self,
        fence_character: str,
        fence_count: int,
        extracted_text: str,
        pre_extracted_text: str,
        text_after_extracted_text: str,
        pre_text_after_extracted_text: str,
        extracted_whitespace: str,
        extracted_whitespace_before_info_string: str,
        position_marker: PositionMarker,
    ) -> None:
        (
            self.__extracted_text,
            self.__pre_extracted_text,
            self.__extracted_whitespace_before_info_string,
            self.__text_after_extracted_text,
            self.__pre_text_after_extracted_text,
            self.__fence_character,
            self.__fence_count,
        ) = (
            extracted_text,
            pre_extracted_text,
            extracted_whitespace_before_info_string,
            text_after_extracted_text,
            pre_text_after_extracted_text,
            fence_character,
            fence_count,
        )
        LeafMarkdownToken.__init__(
            self,
            MarkdownToken._token_fenced_code_block,
            "",
            position_marker=position_marker,
            extracted_whitespace=extracted_whitespace,
            requires_end_token=True,
        )
        self.__compose_extra_data_field()

    # pylint: enable=too-many-arguments
    # pylint: disable=protected-access
    @staticmethod
    def get_markdown_token_type() -> str:
        """
        Get the type of markdown token for rehydration purposes.
        """
        return MarkdownToken._token_fenced_code_block

    # pylint: enable=protected-access

    @property
    def fence_character(self) -> str:
        """
        Returns the character used for the fence.
        """
        return self.__fence_character

    @property
    def fence_count(self) -> int:
        """
        Returns the number of fence characters used for the fence.
        """
        return self.__fence_count

    @property
    def extracted_text(self) -> str:
        """
        Returns the text extracted from the info string.
        """
        return self.__extracted_text

    @property
    def pre_extracted_text(self) -> str:
        """
        Returns the text extracted from the info string.
        """
        return self.__pre_extracted_text

    @property
    def text_after_extracted_text(self) -> str:
        """
        Returns the text extracted after the info string.
        """
        return self.__text_after_extracted_text

    @property
    def pre_text_after_extracted_text(self) -> str:
        """
        Returns the text extracted after after the info string.
        """
        return self.__pre_text_after_extracted_text

    @property
    def extracted_whitespace_before_info_string(self) -> str:
        """
        Returns any whitespace that was extracted before the info string was processed.
        """
        return self.__extracted_whitespace_before_info_string

    def __compose_extra_data_field(self) -> None:
        """
        Compose the object's self.extra_data field from the local object's variables.
        """
        self._set_extra_data(
            MarkdownToken.extra_data_separator.join(
                [
                    self.__fence_character,
                    str(self.__fence_count),
                    self.__extracted_text,
                    self.__pre_extracted_text,
                    self.__text_after_extracted_text,
                    self.__pre_text_after_extracted_text,
                    self.extracted_whitespace,
                    self.__extracted_whitespace_before_info_string,
                ]
            )
        )
