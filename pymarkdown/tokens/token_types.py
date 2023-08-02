"""
Module to contain lists of the available token types.
"""


from typing import List

from pymarkdown.tokens.atx_heading_markdown_token import AtxHeadingMarkdownToken
from pymarkdown.tokens.blank_line_markdown_token import BlankLineMarkdownToken
from pymarkdown.tokens.block_quote_markdown_token import BlockQuoteMarkdownToken
from pymarkdown.tokens.email_autolink_markdown_token import EmailAutolinkMarkdownToken
from pymarkdown.tokens.emphasis_markdown_token import EmphasisMarkdownToken
from pymarkdown.tokens.fenced_code_block_markdown_token import (
    FencedCodeBlockMarkdownToken,
)
from pymarkdown.tokens.hard_break_markdown_token import HardBreakMarkdownToken
from pymarkdown.tokens.html_block_markdown_token import HtmlBlockMarkdownToken
from pymarkdown.tokens.image_start_markdown_token import ImageStartMarkdownToken
from pymarkdown.tokens.indented_code_block_markdown_token import (
    IndentedCodeBlockMarkdownToken,
)
from pymarkdown.tokens.inline_code_span_markdown_token import (
    InlineCodeSpanMarkdownToken,
)
from pymarkdown.tokens.link_reference_definition_markdown_token import (
    LinkReferenceDefinitionMarkdownToken,
)
from pymarkdown.tokens.link_start_markdown_token import LinkStartMarkdownToken
from pymarkdown.tokens.new_list_item_markdown_token import NewListItemMarkdownToken
from pymarkdown.tokens.ordered_list_start_markdown_token import (
    OrderedListStartMarkdownToken,
)
from pymarkdown.tokens.paragraph_markdown_token import ParagraphMarkdownToken
from pymarkdown.tokens.raw_html_markdown_token import RawHtmlMarkdownToken
from pymarkdown.tokens.setext_heading_markdown_token import SetextHeadingMarkdownToken
from pymarkdown.tokens.text_markdown_token import TextMarkdownToken
from pymarkdown.tokens.thematic_break_markdown_token import ThematicBreakMarkdownToken
from pymarkdown.tokens.unordered_list_start_markdown_token import (
    UnorderedListStartMarkdownToken,
)
from pymarkdown.tokens.uri_autolink_markdown_token import UriAutolinkMarkdownToken


class TokenTypes:
    """
    Class to contain lists of the available token types.
    """

    __INLINE_TOKEN_TYPES: List[type] = [
        EmphasisMarkdownToken,
        UriAutolinkMarkdownToken,
        EmailAutolinkMarkdownToken,
        RawHtmlMarkdownToken,
        HardBreakMarkdownToken,
        InlineCodeSpanMarkdownToken,
        ImageStartMarkdownToken,
        LinkStartMarkdownToken,
        TextMarkdownToken,
    ]
    __LEAF_TOKEN_TYPES: List[type] = [
        HtmlBlockMarkdownToken,
        ThematicBreakMarkdownToken,
        LinkReferenceDefinitionMarkdownToken,
        BlankLineMarkdownToken,
        SetextHeadingMarkdownToken,
        AtxHeadingMarkdownToken,
        FencedCodeBlockMarkdownToken,
        IndentedCodeBlockMarkdownToken,
        ParagraphMarkdownToken,
    ]

    __CONTAINER_TOKEN_TYPES: List[type] = [
        BlockQuoteMarkdownToken,
        NewListItemMarkdownToken,
        UnorderedListStartMarkdownToken,
        OrderedListStartMarkdownToken,
    ]

    @staticmethod
    def get_inline_token_types() -> List[type]:
        """
        Get a list of all available inline token types.
        """
        return TokenTypes.__INLINE_TOKEN_TYPES[:]

    @staticmethod
    def get_leaf_token_types() -> List[type]:
        """
        Get a list of all available leaf token types.
        """
        return TokenTypes.__LEAF_TOKEN_TYPES[:]

    @staticmethod
    def get_container_token_types() -> List[type]:
        """
        Get a list of all available container token types.
        """
        return TokenTypes.__CONTAINER_TOKEN_TYPES[:]
