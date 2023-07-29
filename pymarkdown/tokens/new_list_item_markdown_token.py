"""
Module to provide for an encapsulation of the new list item element.
"""

from pymarkdown.position_marker import PositionMarker
from pymarkdown.tokens.container_markdown_token import ContainerMarkdownToken
from pymarkdown.tokens.markdown_token import MarkdownToken


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
