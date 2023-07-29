"""
Module to provide for an encapsulation of the paragraph element.
"""

from pymarkdown.position_marker import PositionMarker
from pymarkdown.tokens.leaf_markdown_token import LeafMarkdownToken
from pymarkdown.tokens.markdown_token import MarkdownToken


class ParagraphMarkdownToken(LeafMarkdownToken):
    """
    Class to provide for an encapsulation of the paragraph element.
    """

    def __init__(
        self, extracted_whitespace: str, position_marker: PositionMarker
    ) -> None:
        self.__extracted_whitespace: str = extracted_whitespace
        self.__final_whitespace, self.rehydrate_index = (
            "",
            0,
        )
        LeafMarkdownToken.__init__(
            self,
            MarkdownToken._token_paragraph,
            "",
            position_marker=position_marker,
            requires_end_token=True,
        )
        self.__compose_extra_data_field()

    # pylint: disable=protected-access
    @staticmethod
    def get_markdown_token_type() -> str:
        """
        Get the type of markdown token for rehydration purposes.
        """
        return MarkdownToken._token_paragraph

    # pylint: enable=protected-access

    @property
    def extracted_whitespace(self) -> str:
        """
        Returns any whitespace that was extracted before the processing of this element occurred.
        """
        return self.__extracted_whitespace

    @property
    def final_whitespace(self) -> str:
        """
        Returns any final whitespace at the end of the paragraph that was removed.
        """
        return self.__final_whitespace

    def __compose_extra_data_field(self) -> None:
        """
        Compose the object's self.extra_data field from the local object's variables.
        """

        self._set_extra_data(
            f"{self.__extracted_whitespace}{MarkdownToken.extra_data_separator}{self.__final_whitespace}"
            if self.final_whitespace
            else self.__extracted_whitespace
        )

    def add_whitespace(self, whitespace_to_add: str) -> None:
        """
        Add extra whitespace to the end of the current paragraph.  Should only be
        used when combining text blocks in a paragraph.
        """

        self.__extracted_whitespace = (
            f"{self.__extracted_whitespace}{whitespace_to_add}"
        )
        self.__compose_extra_data_field()

    def set_final_whitespace(self, whitespace_to_set: str) -> None:
        """
        Set the final whitespace for the paragraph. That is any whitespace at the very
        end of the paragraph, removed to prevent hard lines at the end.
        """

        self.__final_whitespace = whitespace_to_set
        self.__compose_extra_data_field()
