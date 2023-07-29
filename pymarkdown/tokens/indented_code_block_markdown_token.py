"""
Module to provide for an encapsulation of the indented code block element.
"""

from pymarkdown.parser_helper import ParserHelper
from pymarkdown.tokens.leaf_markdown_token import LeafMarkdownToken
from pymarkdown.tokens.markdown_token import MarkdownToken


class IndentedCodeBlockMarkdownToken(LeafMarkdownToken):
    """
    Class to provide for an encapsulation of the indented code block element.
    """

    def __init__(
        self, extracted_whitespace: str, line_number: int, column_number: int
    ) -> None:
        self.__indented_whitespace = ""
        LeafMarkdownToken.__init__(
            self,
            MarkdownToken._token_indented_code_block,
            extracted_whitespace,
            line_number=line_number,
            column_number=column_number,
            extracted_whitespace=extracted_whitespace,
            requires_end_token=True,
        )
        self.__compose_extra_data_field()

    # pylint: disable=protected-access
    @staticmethod
    def get_markdown_token_type() -> str:
        """
        Get the type of markdown token for rehydration purposes.
        """
        return MarkdownToken._token_indented_code_block

    # pylint: enable=protected-access

    @property
    def indented_whitespace(self) -> str:
        """
        Returns any indented whitespace that comes before the text.
        """
        return self.__indented_whitespace

    def __compose_extra_data_field(self) -> None:
        """
        Compose the object's self.extra_data field from the local object's variables.
        """
        self._set_extra_data(
            MarkdownToken.extra_data_separator.join(
                [self.extracted_whitespace, self.indented_whitespace]
            )
        )

    def add_indented_whitespace(self, indented_whitespace: str) -> None:
        """
        Add the indented whitespace that comes before the text.
        """
        self.__indented_whitespace = (
            f"{self.__indented_whitespace}{ParserHelper.newline_character}"
            + f"{indented_whitespace}"
        )
        self.__compose_extra_data_field()
