"""
Module to provide for an encapsulation of the link element.
"""

from pymarkdown.links.link_helper_properties import LinkHelperProperties
from pymarkdown.tokens.markdown_token import MarkdownToken
from pymarkdown.tokens.reference_markdown_token import ReferenceMarkdownToken


class LinkStartMarkdownToken(ReferenceMarkdownToken):
    """
    Class to provide for an encapsulation of the link element.
    """

    def __init__(
        self,
        text_from_blocks: str,
        line_number: int,
        column_number: int,
        lhp: LinkHelperProperties,
    ) -> None:
        assert lhp.pre_inline_link is not None
        assert lhp.label_type is not None
        assert lhp.inline_link is not None
        ReferenceMarkdownToken.__init__(
            self,
            lhp,
            LinkStartMarkdownToken.get_markdown_token_type(),
            "",
            text_from_blocks,
            line_number=line_number,
            column_number=column_number,
            requires_end_token=True,
            can_force_close=False,
        )

    # pylint: disable=protected-access
    @staticmethod
    def get_markdown_token_type() -> str:
        """
        Get the type of markdown token for rehydration purposes.
        """
        return MarkdownToken._token_inline_link

    # pylint: enable=protected-access
