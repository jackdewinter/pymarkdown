"""
Inline processing
"""
import logging
from typing import List, cast

from pymarkdown.inline.inline_handler_helper import InlineHandlerHelper
from pymarkdown.inline.inline_helper import InlineHelper
from pymarkdown.inline.inline_text_block_helper import InlineTextBlockHelper
from pymarkdown.parser_helper import ParserHelper
from pymarkdown.parser_logger import ParserLogger
from pymarkdown.tokens.atx_heading_markdown_token import AtxHeadingMarkdownToken
from pymarkdown.tokens.block_quote_markdown_token import BlockQuoteMarkdownToken
from pymarkdown.tokens.list_start_markdown_token import ListStartMarkdownToken
from pymarkdown.tokens.markdown_token import MarkdownToken
from pymarkdown.tokens.paragraph_markdown_token import ParagraphMarkdownToken
from pymarkdown.tokens.text_markdown_token import TextMarkdownToken

POGGER = ParserLogger(logging.getLogger(__name__))


class InlineProcessor:
    """
    Handle the inline processing of the token stream.
    """

    @staticmethod
    def initialize() -> None:
        """
        Initialize the inline processor subsystem.
        """
        InlineHandlerHelper.initialize()

    @staticmethod
    def parse_inline(coalesced_results: List[MarkdownToken]) -> List[MarkdownToken]:
        """
        Parse and resolve any inline elements.
        """
        POGGER.info("coalesced_results")
        POGGER.info("-----")
        for next_token in coalesced_results:
            POGGER.info(">>$<<", next_token)
        POGGER.info("-----")

        coalesced_stack: List[MarkdownToken] = []
        current_token = coalesced_results[0]
        coalesced_list: List[MarkdownToken] = []
        coalesced_list.extend(coalesced_results[:1])

        POGGER.debug("STACK?:$", current_token)
        if current_token.is_container:
            POGGER.debug("STACK:$", coalesced_stack)
            coalesced_stack.append(current_token)
            POGGER.debug("STACK-ADD:$", current_token)
            POGGER.debug("STACK:$", coalesced_stack)
            if current_token.is_block_quote_start:
                block_quote_token = cast(BlockQuoteMarkdownToken, current_token)
                block_quote_token.leading_text_index = 0
                POGGER.info("-->last->block->$", block_quote_token.leading_text_index)
            else:
                POGGER.info("-->not bq-")

        for coalesce_index in range(1, len(coalesced_results)):
            InlineProcessor.__process_next_coalesce_item(
                coalesced_results, coalesce_index, coalesced_list, coalesced_stack
            )
        return coalesced_list

    @staticmethod
    def __adjust_stack(
        coalesced_results: List[MarkdownToken],
        coalesced_stack: List[MarkdownToken],
        coalesce_index: int,
    ) -> None:
        current_token = coalesced_results[coalesce_index]
        POGGER.debug("STACK?:$", current_token)
        if current_token.is_container and not current_token.is_new_list_item:
            POGGER.debug("STACK:$", coalesced_stack)
            coalesced_stack.append(current_token)
            POGGER.debug("STACK-ADD:$", current_token)
            POGGER.debug("STACK:$", coalesced_stack)
            if current_token.is_block_quote_start:
                block_quote_token = cast(BlockQuoteMarkdownToken, current_token)
                block_quote_token.leading_text_index = 0
                POGGER.info("-->last->block->$", block_quote_token.leading_text_index)
            else:
                POGGER.info("-->not bq-")

        elif current_token.is_list_end or current_token.is_block_quote_end:
            POGGER.debug("STACK:$", coalesced_stack)
            del coalesced_stack[-1]
            POGGER.debug(
                "STACK-REMOVE:$",
                current_token,
            )
            POGGER.debug("STACK:$", coalesced_stack)

    @staticmethod
    def __process_next_coalesce_item(
        coalesced_results: List[MarkdownToken],
        coalesce_index: int,
        coalesced_list: List[MarkdownToken],
        coalesced_stack: List[MarkdownToken],
    ) -> None:
        POGGER.info("coalesced_results:$<", coalesced_list[-1])
        POGGER.info("coalesced_stack:$<", coalesced_stack)
        for i in range(len(coalesced_stack) - 1, -1, -1):
            if coalesced_stack[i].is_block_quote_start:
                block_quote_token = cast(BlockQuoteMarkdownToken, coalesced_stack[i])
                POGGER.info(
                    "$-->last->block->$", i, block_quote_token.leading_text_index
                )
        if coalesced_results[coalesce_index].is_text and (
            coalesced_list[-1].is_paragraph
            or coalesced_list[-1].is_setext_heading
            or coalesced_list[-1].is_atx_heading
            or coalesced_list[-1].is_code_block
        ):
            if coalesced_list[-1].is_code_block:
                processed_tokens = InlineProcessor.__parse_code_block(
                    coalesced_results, coalesce_index, coalesced_list, coalesced_stack
                )
            elif coalesced_list[-1].is_setext_heading:
                processed_tokens = InlineProcessor.__parse_setext_heading(
                    coalesced_results, coalesce_index, coalesced_stack
                )
            elif coalesced_list[-1].is_atx_heading:
                processed_tokens = InlineProcessor.__parse_atx_heading(
                    coalesced_results, coalesce_index, coalesced_stack, coalesced_list
                )
            else:
                processed_tokens = InlineProcessor.__parse_paragraph(
                    coalesced_list, coalesced_results, coalesce_index, coalesced_stack
                )
            coalesced_list.extend(processed_tokens)
        else:
            coalesced_list.append(coalesced_results[coalesce_index])

        InlineProcessor.__adjust_stack(
            coalesced_results, coalesced_stack, coalesce_index
        )

    @staticmethod
    def __parse_paragraph(
        coalesced_list: List[MarkdownToken],
        coalesced_results: List[MarkdownToken],
        coalesce_index: int,
        coalesced_stack: List[MarkdownToken],
    ) -> List[MarkdownToken]:
        assert coalesced_list[-1].is_paragraph
        paragraph_token = cast(ParagraphMarkdownToken, coalesced_list[-1])
        assert coalesced_results[coalesce_index].is_text
        text_token = cast(TextMarkdownToken, coalesced_results[coalesce_index])
        POGGER.debug(
            ">>before_add_ws>>$>>add>>$>>",
            coalesced_list[-1],
            text_token.extracted_whitespace,
        )
        paragraph_token.add_whitespace(text_token.extracted_whitespace)
        POGGER.debug(">>after_add_ws>>$", coalesced_list[-1])
        POGGER.debug(
            ">>text_token>>$", ParserHelper.make_whitespace_visible(str(text_token))
        )
        POGGER.debug(
            "text_token.token_text>:$:<",
            ParserHelper.make_whitespace_visible(str(text_token.token_text)),
        )
        return InlineTextBlockHelper.process_inline_text_block(
            text_token.token_text,
            coalesced_stack,
            is_para=True,
            para_space=text_token.extracted_whitespace,
            line_number=text_token.line_number,
            column_number=text_token.column_number,
            para_owner=paragraph_token,
            tabified_text=text_token.tabified_text,
        )

    @staticmethod
    def __parse_atx_heading(
        coalesced_results: List[MarkdownToken],
        coalesce_index: int,
        coalesced_stack: List[MarkdownToken],
        coalesced_list: List[MarkdownToken],
    ) -> List[MarkdownToken]:
        assert coalesced_results[coalesce_index].is_text
        text_token = cast(TextMarkdownToken, coalesced_results[coalesce_index])
        POGGER.debug("atx-block>>$<<", text_token)
        POGGER.debug(
            "atx-block-text>>$<<",
            text_token.token_text,
        )
        POGGER.debug(
            "atx-block-ws>>$<<",
            text_token.extracted_whitespace,
        )

        assert coalesced_list[-1].is_atx_heading
        atx_token = cast(AtxHeadingMarkdownToken, coalesced_list[-1])
        POGGER.debug(">>text_token>>$", text_token)
        return InlineTextBlockHelper.process_inline_text_block(
            text_token.token_text,
            coalesced_stack,
            text_token.extracted_whitespace,
            line_number=text_token.line_number,
            column_number=text_token.column_number
            + len(text_token.extracted_whitespace)
            + atx_token.hash_count,
            tabified_text=text_token.tabified_text,
        )

    @staticmethod
    def __parse_setext_heading(
        coalesced_results: List[MarkdownToken],
        coalesce_index: int,
        coalesced_stack: List[MarkdownToken],
    ) -> List[MarkdownToken]:
        assert coalesced_results[coalesce_index].is_text
        text_token = cast(TextMarkdownToken, coalesced_results[coalesce_index])
        POGGER.debug(">>text_token>>$", text_token)
        processed_tokens = InlineTextBlockHelper.process_inline_text_block(
            text_token.token_text,
            coalesced_stack,
            whitespace_to_recombine=text_token.extracted_whitespace,
            is_setext=True,
            para_space=text_token.extracted_whitespace,
            line_number=text_token.line_number,
            column_number=text_token.column_number,
            tabified_text=text_token.tabified_text,
        )
        POGGER.debug(
            "processed_tokens>>$",
            processed_tokens,
        )
        return processed_tokens

    @staticmethod
    def __parse_code_block(
        coalesced_results: List[MarkdownToken],
        coalesce_index: int,
        coalesced_list: List[MarkdownToken],
        coalesced_stack: List[MarkdownToken],
    ) -> List[MarkdownToken]:
        assert coalesced_results[coalesce_index].is_text
        text_token = cast(TextMarkdownToken, coalesced_results[coalesce_index])
        encoded_text = InlineHelper.append_text("", text_token.token_text)
        if coalesced_list[-1].is_fenced_code_block:
            line_number_delta, new_column_number = 1, 1

            POGGER.info("coalesced_stack:$<", coalesced_stack)
            if coalesced_stack:
                if coalesced_stack[-1].is_block_quote_start:
                    block_quote_token = cast(
                        BlockQuoteMarkdownToken, coalesced_stack[-1]
                    )
                    assert block_quote_token.bleading_spaces
                    split_leading_spaces = block_quote_token.bleading_spaces.split(
                        ParserHelper.newline_character
                    )
                else:
                    list_token = cast(ListStartMarkdownToken, coalesced_stack[-1])
                    assert list_token.leading_spaces
                    split_leading_spaces = list_token.leading_spaces.split(
                        ParserHelper.newline_character
                    )
                new_column_number += (
                    (len(split_leading_spaces[1]))
                    if len(split_leading_spaces) >= 2
                    else (len(split_leading_spaces[0]))
                )
            else:
                leading_whitespace = text_token.extracted_whitespace
                POGGER.debug(">>$<<", text_token)
                assert ParserHelper.newline_character not in leading_whitespace
                POGGER.info(
                    "leading_whitespace:$<",
                    leading_whitespace,
                )
                leading_whitespace = ParserHelper.remove_all_from_text(
                    leading_whitespace
                )
                POGGER.info("leading_whitespace:$<", leading_whitespace)
                new_column_number += len(leading_whitespace)
        else:
            line_number_delta, new_column_number = (
                0,
                coalesced_list[-1].column_number,
            )
        processed_tokens: List[MarkdownToken] = [
            TextMarkdownToken(
                encoded_text,
                text_token.extracted_whitespace,
                line_number=coalesced_list[-1].line_number + line_number_delta,
                column_number=new_column_number,
            )
        ]
        POGGER.debug(
            "new Text>>$>>",
            processed_tokens,
        )
        return processed_tokens
