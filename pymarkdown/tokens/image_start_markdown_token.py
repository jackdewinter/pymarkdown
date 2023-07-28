"""
Module to provide for an encapsulation of the image element.
"""

from pymarkdown.links.link_helper_properties import LinkHelperProperties
from pymarkdown.tokens.markdown_token import MarkdownToken
from pymarkdown.tokens.reference_markdown_token import ReferenceMarkdownToken


class ImageStartMarkdownToken(ReferenceMarkdownToken):
    """
    Class to provide for an encapsulation of the image element.
    """

    # pylint: disable=too-many-arguments
    def __init__(
        self,
        image_alt_text: str,
        text_from_blocks: str,
        line_number: int,
        column_number: int,
        lhp: LinkHelperProperties,
    ) -> None:
        assert lhp.label_type is not None
        assert lhp.pre_inline_link is not None
        assert lhp.inline_link is not None

        self.__image_alt_text = image_alt_text
        ReferenceMarkdownToken.__init__(
            self,
            lhp,
            ImageStartMarkdownToken.get_markdown_token_type(),
            self.__image_alt_text,
            text_from_blocks,
            line_number=line_number,
            column_number=column_number,
        )

    # pylint: enable=too-many-arguments

    # pylint: disable=protected-access
    @staticmethod
    def get_markdown_token_type() -> str:
        """
        Get the type of markdown token for rehydration purposes.
        """
        return MarkdownToken._token_inline_image

    # pylint: enable=protected-access

    @property
    def image_alt_text(self) -> str:
        """
        Returns the text extracted from the blocks of the link, after processing.
        """
        return self.__image_alt_text
