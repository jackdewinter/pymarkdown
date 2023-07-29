"""
Module to provide for an encapsulation of the atx heading element.
"""

from pymarkdown.position_marker import PositionMarker
from pymarkdown.tokens.leaf_markdown_token import LeafMarkdownToken
from pymarkdown.tokens.markdown_token import MarkdownToken


class AtxHeadingMarkdownToken(LeafMarkdownToken):
    """
    Class to provide for an encapsulation of the atx heading element.
    """

    def __init__(
        self,
        hash_count: int,
        remove_trailing_count: int,
        extracted_whitespace: str,
        position_marker: PositionMarker,
    ) -> None:
        self.__hash_count, self.__remove_trailing_count = (
            hash_count,
            remove_trailing_count,
        )

        LeafMarkdownToken.__init__(
            self,
            MarkdownToken._token_atx_heading,
            "",
            position_marker=position_marker,
            extracted_whitespace=extracted_whitespace,
            requires_end_token=True,
            can_force_close=False,
        )
        self.__compose_extra_data_field()

    # pylint: disable=protected-access
    @staticmethod
    def get_markdown_token_type() -> str:
        """
        Get the type of markdown token for rehydration purposes.
        """
        return MarkdownToken._token_atx_heading

    # pylint: enable=protected-access

    @property
    def hash_count(self) -> int:
        """
        Returns the number of hash marks specified at the start of the line.
        """
        return self.__hash_count

    @property
    def remove_trailing_count(self) -> int:
        """
        Returns the number of hash marks specified at the end of the line.
        """
        return self.__remove_trailing_count

    def __compose_extra_data_field(self) -> None:
        """
        Compose the object's self.extra_data field from the local object's variables.
        """
        self._set_extra_data(
            MarkdownToken.extra_data_separator.join(
                [
                    str(self.__hash_count),
                    str(self.__remove_trailing_count),
                    self.extracted_whitespace,
                ]
            )
        )
