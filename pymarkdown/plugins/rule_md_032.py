"""
Module to implement a plugin that ensures that top-level lists are surrounded by Blank Lines.

Note:  Because of the "weird" way in which this rule triggers, it must provide its own
       `override_is_error_token_prefaced_by_blank_line` logic, as modifying the normal
       logic for this one rule was not feasible.
"""

from typing import List, Optional, cast

from pymarkdown.general.parser_helper import ParserHelper
from pymarkdown.plugin_manager.plugin_details import PluginDetails
from pymarkdown.plugin_manager.plugin_scan_context import PluginScanContext
from pymarkdown.plugin_manager.rule_plugin import RulePlugin
from pymarkdown.tokens.markdown_token import MarkdownToken
from pymarkdown.tokens.text_markdown_token import TextMarkdownToken


class RuleMd032(RulePlugin):
    """
    Class to implement a plugin that ensures that top-level lists are surrounded by Blank Lines.
    """

    def __init__(self) -> None:
        super().__init__()
        self.__last_non_end_token: Optional[MarkdownToken] = None
        self.__container_token_stack: List[MarkdownToken] = []
        self.__end_list_end_token: Optional[MarkdownToken] = None
        self.__previous_tokens: List[MarkdownToken] = []

    def get_details(self) -> PluginDetails:
        """
        Get the details for the plugin.
        """
        return PluginDetails(
            plugin_name="blanks-around-lists",
            plugin_id="MD032",
            plugin_enabled_by_default=True,
            plugin_description="Lists should be surrounded by blank lines",
            plugin_version="0.5.1",
            plugin_interface_version=1,
            plugin_url="https://pymarkdown.readthedocs.io/en/latest/plugins/rule_md032.md",
        )

    def starting_new_file(self) -> None:
        """
        Event that the a new file to be scanned is starting.
        """
        self.__last_non_end_token = None
        self.__container_token_stack.clear()
        self.__end_list_end_token = None
        self.__previous_tokens.clear()

    def __next_token_list_start(
        self, context: PluginScanContext, token: MarkdownToken
    ) -> None:
        if (
            self.__last_non_end_token
            and not self.__last_non_end_token.is_blank_line
            and not (
                self.__container_token_stack
                and (
                    self.__container_token_stack[-1].is_list_start
                    or (
                        self.__container_token_stack[-1].is_block_quote_start
                        and self.__container_token_stack[-1].line_number
                        == token.line_number
                    )
                )
            )
        ):
            self.report_next_token_error(context, token)

        self.__container_token_stack.append(token)

    def __calculate_override_for_blank_line(
        self,
        token: MarkdownToken,
        token_index: int,
        parent_leaf_or_container_token: MarkdownToken,
    ) -> bool:
        # If we run into a blank line, there is a possibility that the blank line is followed
        # by a single line of text and then the HTML block end.  In that case, we need to
        # enable the override.
        #
        # i.e With the following markdown, we would get here via line 6 (second <script>),
        #     l0 would be line 4 (the blank line), and there is a text line (line 5) with
        #     an HTML block end and a list end that were skipped over.
        #
        # 1. a list
        #    <script>
        # <!-- pyml disable-next-line blanks-around-lists -->
        #
        #    </script>
        # <script>
        # </script>

        are_line_numbers_same = (
            parent_leaf_or_container_token.line_number == token.line_number - 2
        )
        is_eligible_text_token = (
            self.__previous_tokens[token_index + 1].line_number == token.line_number - 1
            and self.__previous_tokens[token_index + 1].is_text
        )
        is_html_end_present = self.__previous_tokens[token_index + 2].is_html_block_end
        return are_line_numbers_same and is_eligible_text_token and is_html_end_present

    def __calculate_override_for_fenced_code_block(self, token_index: int) -> bool:
        expected_fcb_text_token = self.__previous_tokens[token_index + 1]
        if expected_fcb_text_token.is_text:
            text_token = cast(TextMarkdownToken, expected_fcb_text_token)
            return not text_token.token_text or text_token.token_text.endswith(
                f"{ParserHelper.newline_character}{ParserHelper.replace_noop_character}"
            )
        return False

    def __calculate_override(self, token: MarkdownToken) -> bool:

        token_index = len(self.__previous_tokens) - 1
        while (
            token_index >= 0
            and not self.__previous_tokens[token_index].is_leaf
            and not self.__previous_tokens[token_index].is_container
        ):
            token_index -= 1

        parent_leaf_or_container_token = self.__previous_tokens[token_index]
        if parent_leaf_or_container_token.is_blank_line:
            return self.__calculate_override_for_blank_line(
                token, token_index, parent_leaf_or_container_token
            )
        if parent_leaf_or_container_token.is_fenced_code_block:
            return self.__calculate_override_for_fenced_code_block(token_index)

        assert self.__previous_tokens[token_index].is_leaf
        token_index -= 1
        if self.__previous_tokens[token_index].is_container:
            token_index -= 1
        base_token = self.__previous_tokens[token_index]

        is_base_token_blank = base_token.is_blank_line
        are_parent_and_token_on_same_line = (
            parent_leaf_or_container_token.line_number == token.line_number - 1
        )
        is_base_at_right_place = base_token.line_number == token.line_number - 2
        return (
            is_base_token_blank
            and are_parent_and_token_on_same_line
            and is_base_at_right_place
        )

    def __report_token(self, context: PluginScanContext, token: MarkdownToken) -> None:

        override_is_error_token_prefaced_by_blank_line = self.__calculate_override(
            token
        )

        line_number_delta = -1
        while context.is_pragma_on_line(token.line_number + line_number_delta):
            line_number_delta -= 1
        self.report_next_token_error(
            context,
            token,
            line_number_delta=line_number_delta,
            override_is_error_token_prefaced_by_blank_line=override_is_error_token_prefaced_by_blank_line,
        )

    def next_token(self, context: PluginScanContext, token: MarkdownToken) -> None:
        """
        Event that a new token is being processed.
        """
        if self.__end_list_end_token:
            if (
                not token.is_blank_line
                and not token.is_new_list_item
                and not token.is_list_end
                and not token.is_block_quote_end
                and not token.is_end_of_stream
            ):
                self.__report_token(context, token)
            self.__end_list_end_token = None

        if token.is_block_quote_start:
            self.__container_token_stack.append(token)
        elif token.is_block_quote_end:
            del self.__container_token_stack[-1]
        elif token.is_list_start:
            self.__next_token_list_start(context, token)
        elif token.is_list_end:
            assert self.__last_non_end_token is not None
            if not self.__last_non_end_token.is_blank_line:
                self.__end_list_end_token = token
                del self.__container_token_stack[-1]

        if (
            not token.is_end_token
            and not token.is_block_quote_start
            and not token.is_list_start
        ):
            self.__last_non_end_token = token

        self.__previous_tokens.append(token)
