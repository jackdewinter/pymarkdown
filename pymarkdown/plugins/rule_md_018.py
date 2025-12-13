"""
Module to implement a plugin that looks for text in a paragraph where a line starts
with what could be an atx heading, except there is no spaces between the hashes and
the text of the heading.
"""

import re
from typing import Any, Optional, Tuple, cast

from pymarkdown.general.constants import Constants
from pymarkdown.general.parser_helper import ParserHelper
from pymarkdown.plugin_manager.plugin_details import PluginDetails
from pymarkdown.plugin_manager.plugin_scan_context import PluginScanContext
from pymarkdown.plugin_manager.rule_plugin import RulePlugin
from pymarkdown.tokens.inline_code_span_markdown_token import (
    InlineCodeSpanMarkdownToken,
)
from pymarkdown.tokens.link_start_markdown_token import LinkStartMarkdownToken
from pymarkdown.tokens.markdown_token import MarkdownToken
from pymarkdown.tokens.paragraph_markdown_token import ParagraphMarkdownToken
from pymarkdown.tokens.raw_html_markdown_token import RawHtmlMarkdownToken
from pymarkdown.tokens.text_markdown_token import TextMarkdownToken


class StartOfLineTokenParser:
    """
    Token parser that activates a check only on valid newlines within
    a paragraph.
    """

    def __init__(self) -> None:
        self.__last_paragraph_token: Optional[ParagraphMarkdownToken] = None
        self.__paragraph_index = -1
        self.__first_line_after_other_token = False
        self.__paragraph_column_number = 0
        self.__inside_of_link = False
        self.__first_line_after_hard_break = False
        self.__delayed_line: Optional[
            Tuple[str, PluginScanContext, MarkdownToken, int, int]
        ] = None

    def starting_new_file(self) -> None:
        """
        Event that the a new file to be scanned is starting.
        """
        self.__last_paragraph_token = None
        self.__paragraph_index = -1
        self.__first_line_after_other_token = False
        self.__paragraph_column_number = 0

    def next_token(self, context: PluginScanContext, token: MarkdownToken) -> None:
        """
        Event that a new token is being processed.
        """
        if token.is_paragraph:
            paragraph_token = cast(ParagraphMarkdownToken, token)
            self.__next_token_paragraph_start(paragraph_token)
        elif token.is_paragraph_end:
            self.__next_token_paragraph_end()
        elif self.__last_paragraph_token:
            if self.__inside_of_link:
                if token.is_inline_link_end:
                    self.__inside_of_link = False
            elif token.is_text:
                text_token = cast(TextMarkdownToken, token)
                self.__next_token_paragraph_text_inline(text_token, context)
            else:
                self.__next_token_paragraph_non_text_inline(token)

    def __next_token_paragraph_start(self, token: ParagraphMarkdownToken) -> None:
        self.__last_paragraph_token = token
        self.__paragraph_index = 0
        self.__first_line_after_other_token = True
        self.__first_line_after_hard_break = False
        self.__inside_of_link = False
        self.__paragraph_column_number = token.column_number
        self.__delayed_line = None

    def __next_token_paragraph_end(self) -> None:
        if self.__delayed_line:
            self.check_start_of_line(
                self.__delayed_line[0],
                self.__delayed_line[1],
                self.__delayed_line[2],
                self.__delayed_line[3],
                self.__delayed_line[4],
            )
            self.__delayed_line = None
        self.__last_paragraph_token = None

    def __next_token_paragraph_non_text_inline_image(
        self, token: MarkdownToken
    ) -> None:  # sourcery skip: extract-method
        link_token = cast(LinkStartMarkdownToken, token)
        self.__paragraph_index += link_token.text_from_blocks.count(
            ParserHelper.newline_character
        )
        if link_token.label_type == Constants.link_type__inline:
            assert link_token.before_link_whitespace is not None
            self.__paragraph_index += link_token.before_link_whitespace.count(
                ParserHelper.newline_character
            )
            assert link_token.before_title_whitespace is not None
            self.__paragraph_index += link_token.before_title_whitespace.count(
                ParserHelper.newline_character
            )
            assert link_token.after_title_whitespace is not None
            self.__paragraph_index += link_token.after_title_whitespace.count(
                ParserHelper.newline_character
            )
            assert link_token.active_link_title is not None
            self.__paragraph_index += link_token.active_link_title.count(
                ParserHelper.newline_character
            )
        if link_token.label_type == Constants.link_type__full:
            assert link_token.ex_label is not None
            self.__paragraph_index += link_token.ex_label.count(
                ParserHelper.newline_character
            )
        self.__inside_of_link = token.is_inline_link

    def __next_token_paragraph_non_text_inline(self, token: MarkdownToken) -> None:
        if token.is_inline_code_span:
            code_span_token = cast(InlineCodeSpanMarkdownToken, token)
            self.__paragraph_index += (
                code_span_token.leading_whitespace.count(ParserHelper.newline_character)
                + code_span_token.span_text.count(ParserHelper.newline_character)
                + code_span_token.trailing_whitespace.count(
                    ParserHelper.newline_character
                )
            )
        elif token.is_inline_raw_html:
            raw_html_token = cast(RawHtmlMarkdownToken, token)
            self.__paragraph_index += raw_html_token.raw_tag.count(
                ParserHelper.newline_character
            )
        elif token.is_inline_image or token.is_inline_link:
            self.__next_token_paragraph_non_text_inline_image(token)
        elif token.is_inline_hard_break:
            self.__paragraph_index += 1
            self.__first_line_after_hard_break = True
        else:
            assert (
                token.is_inline_emphasis
                or token.is_inline_emphasis_end
                or token.is_inline_autolink
                or token.is_task_list
            )
        self.__delayed_line = None

    def __next_token_paragraph_text_inline(
        self, token: TextMarkdownToken, context: PluginScanContext
    ) -> None:
        assert self.__last_paragraph_token is not None
        split_whitespace = self.__last_paragraph_token.extracted_whitespace.split(
            ParserHelper.newline_character
        )
        split_text = token.token_text.split(ParserHelper.newline_character)

        for split_index, next_text in enumerate(split_text):
            combined_text = (
                f"{split_whitespace[split_index + self.__paragraph_index]}{next_text}"
            )
            if (
                self.__first_line_after_hard_break
                or self.__first_line_after_other_token
                or split_index
            ):
                adjusted_column_number = (
                    self.__paragraph_column_number
                    if self.__first_line_after_other_token
                    else self.__paragraph_column_number
                    + len(split_whitespace[split_index + self.__paragraph_index])
                )

                if split_index == len(split_text) - 1:
                    self.__delayed_line = (
                        combined_text,
                        context,
                        token,
                        split_index,
                        -adjusted_column_number,
                    )
                else:
                    self.check_start_of_line(
                        combined_text,
                        context,
                        token,
                        split_index,
                        -adjusted_column_number,
                    )
            self.__first_line_after_other_token = False
            self.__first_line_after_hard_break = False
        self.__paragraph_index += token.token_text.count(ParserHelper.newline_character)

    # pylint: disable=too-many-arguments
    def check_start_of_line(
        self,
        combined_text: str,
        context: Any,
        token: MarkdownToken,
        line_number_delta: int,
        column_number_delta: int,
    ) -> None:
        """
        Check for a pattern at the start of the line.
        """

    # pylint: enable=too-many-arguments


class MyStartOfLineTokenParser(StartOfLineTokenParser):
    """
    Local implementation of the token parser.
    """

    def __init__(self, owner: "RuleMd018") -> None:
        super().__init__()
        self.__owner = owner

    # pylint: disable=too-many-arguments
    def check_start_of_line(
        self,
        combined_text: str,
        context: PluginScanContext,
        token: MarkdownToken,
        line_number_delta: int,
        column_number_delta: int,
    ) -> None:
        """
        Check for a pattern at the start of the line.

        Note that the logic here is a bit weird for the `\\S` at the end of the
        regular expression.  If everything else is good except for that `\\S`,
        which is equivalent to any whitespace character, and it was a space character,
        it would match the Atx code in the leaf processor and be an Atx Heading token
        already.  Hence, what is left is any other whitespace character which is not
        the space character, which should still trigger the rule.
        """
        if re.search(r"^[ ]{0,3}#{1,6}[^ ]", combined_text) and not re.search(
            r"#[ ]*$", combined_text
        ):
            self.__owner.report_next_token_error(
                context,
                token,
                line_number_delta=line_number_delta
                + context.calc_pragma_offset(token, line_number_delta),
                column_number_delta=column_number_delta,
            )

    # pylint: enable=too-many-arguments


class RuleMd018(RulePlugin):
    """
    Class to implement a plugin that looks for text in a paragraph where a line starts
    with what could be an atx heading, except there is no spaces between the hashes and
    the text of the heading.
    """

    def __init__(self) -> None:
        super().__init__()
        self.__token_parser = MyStartOfLineTokenParser(self)

    def get_details(self) -> PluginDetails:
        """
        Get the details for the plugin.
        """
        return PluginDetails(
            plugin_name="no-missing-space-atx",
            plugin_id="MD018",
            plugin_enabled_by_default=True,
            plugin_description="No space present after the hash character on a possible Atx Heading.",
            plugin_version="0.5.0",
            plugin_interface_version=1,
            plugin_url="https://pymarkdown.readthedocs.io/en/latest/plugins/rule_md018.md",
        )

    def starting_new_file(self) -> None:
        """
        Event that the a new file to be scanned is starting.
        """
        self.__token_parser.starting_new_file()

    def next_token(self, context: PluginScanContext, token: MarkdownToken) -> None:
        """
        Event that a new token is being processed.
        """
        self.__token_parser.next_token(context, token)
