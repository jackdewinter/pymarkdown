from typing import Dict, List, Optional, cast

from pymarkdown.general.parser_helper import ParserHelper
from pymarkdown.tokens.link_reference_definition_markdown_token import (
    LinkReferenceDefinitionMarkdownToken,
)
from pymarkdown.tokens.markdown_token import MarkdownToken
from pymarkdown.tokens.paragraph_markdown_token import ParagraphMarkdownToken
from pymarkdown.tokens.text_markdown_token import TextMarkdownToken


class ContainerTokenManager:
    """
    TBD
    """

    def __init__(self) -> None:
        """
        TBD
        """
        self.container_token_stack: List[MarkdownToken] = []
        self.bq_line_index: Dict[int, int] = {}
        self.last_leaf_token: Optional[MarkdownToken] = None

    def clear(self) -> None:
        """
        TBD
        """
        self.container_token_stack = []
        self.bq_line_index = {}
        self.last_leaf_token = None

    @classmethod
    def __is_simple_delta(cls, token: MarkdownToken) -> bool:
        return (
            token.is_blank_line
            or token.is_thematic_break
            or token.is_atx_heading
            or token.is_paragraph_end
        )

    @classmethod
    def __is_remember_leaf_token(cls, token: MarkdownToken) -> bool:
        return bool(
            token.is_setext_heading
            or token.is_indented_code_block
            or token.is_html_block
        )

    @classmethod
    def __is_clear_leaf_token(cls, token: MarkdownToken) -> bool:
        return bool(
            token.is_indented_code_block_end
            or token.is_html_block_end
            or token.is_setext_heading_end
            or token.is_fenced_code_block_end
        )

    def __manage_leaf_tokens_text(self, token: MarkdownToken) -> int:
        assert self.last_leaf_token is not None
        text_token = cast(TextMarkdownToken, token)
        if self.last_leaf_token.is_setext_heading:
            assert text_token.end_whitespace is not None
            return text_token.end_whitespace.count(ParserHelper.newline_character) + 1
        assert self.last_leaf_token.is_html_block or self.last_leaf_token.is_code_block
        return text_token.token_text.count(ParserHelper.newline_character) + 1

    def __manage_leaf_tokens(self, token: MarkdownToken) -> None:
        bq_delta = 0
        if self.__is_simple_delta(token):
            bq_delta = 1
        elif self.__is_remember_leaf_token(token):
            self.last_leaf_token = token
        elif self.__is_clear_leaf_token(token):
            self.last_leaf_token = None
            if token.is_setext_heading_end or token.is_fenced_code_block_end:
                bq_delta = 1
        elif token.is_fenced_code_block:
            bq_delta = 1
            self.last_leaf_token = token
        elif token.is_paragraph:
            paragraph_token = cast(ParagraphMarkdownToken, token)
            bq_delta = paragraph_token.extracted_whitespace.count(
                ParserHelper.newline_character
            )
        elif token.is_link_reference_definition:
            bq_delta = self.__manage_lrd_token(token)
        elif token.is_text and self.last_leaf_token:
            bq_delta = self.__manage_leaf_tokens_text(token)
        self.bq_line_index[len(self.container_token_stack)] += bq_delta

    @classmethod
    def __manage_lrd_token(cls, token: MarkdownToken) -> int:
        lrd_token = cast(LinkReferenceDefinitionMarkdownToken, token)
        assert lrd_token.link_title_raw is not None
        assert lrd_token.link_title_whitespace is not None
        assert lrd_token.link_destination_whitespace is not None
        assert lrd_token.link_name_debug is not None
        return (
            1
            + lrd_token.link_name_debug.count(ParserHelper.newline_character)
            + lrd_token.link_destination_whitespace.count(
                ParserHelper.newline_character
            )
            + lrd_token.link_title_whitespace.count(ParserHelper.newline_character)
            + lrd_token.link_title_raw.count(ParserHelper.newline_character)
        )

    def manage_container_tokens(self, token: MarkdownToken) -> None:
        """
        Manage the container tokens, especially the block quote indices.
        """
        if token.is_block_quote_start:
            self.container_token_stack.append(token)
            self.bq_line_index[len(self.container_token_stack)] = 0
        elif token.is_block_quote_end:
            del self.bq_line_index[len(self.container_token_stack)]
            del self.container_token_stack[-1]
        elif token.is_list_start:
            self.container_token_stack.append(token)
        elif token.is_list_end:
            del self.container_token_stack[-1]
        elif (
            self.container_token_stack
            and self.container_token_stack[-1].is_block_quote_start
        ):
            self.__manage_leaf_tokens(token)
