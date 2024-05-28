"""
Module to implement a plugin that looks for hard tabs in the files.
"""

from typing import List, Optional, cast

from pymarkdown.general.tab_helper import TabHelper
from pymarkdown.plugin_manager.plugin_details import (
    PluginDetails,
    PluginDetailsV3,
    QueryConfigItem,
)
from pymarkdown.plugin_manager.plugin_scan_context import PluginScanContext
from pymarkdown.plugin_manager.rule_plugin import RulePlugin
from pymarkdown.tokens.fenced_code_block_markdown_token import (
    FencedCodeBlockMarkdownToken,
)
from pymarkdown.tokens.markdown_token import EndMarkdownToken, MarkdownToken


class RuleMd010(RulePlugin):
    """
    Class to implement a plugin that looks for hard tabs in the files.
    """

    def __init__(self) -> None:
        super().__init__()
        self.__leaf_tokens: List[MarkdownToken] = []
        self.__line_index = -1
        self.__leaf_token_index = -1
        self.__check_in_code_blocks: bool = False
        self.__last_fenced_code_end_token: Optional[EndMarkdownToken] = None

    def get_details(self) -> PluginDetails:
        """
        Get the details for the plugin.
        """
        return PluginDetailsV3(
            plugin_name="no-hard-tabs",
            plugin_id="MD010",
            plugin_enabled_by_default=True,
            plugin_description="Hard tabs",
            plugin_version="0.6.0",
            plugin_url="https://pymarkdown.readthedocs.io/en/latest/plugins/rule_md010.md",
            plugin_configuration="code_blocks",
            plugin_supports_fix=True,
            plugin_fix_level=0,
        )

    def initialize_from_config(self) -> None:
        """
        Event to allow the plugin to load configuration information.
        """
        self.__check_in_code_blocks = self.plugin_configuration.get_boolean_property(
            "code_blocks",
            default_value=True,
        )

    def query_config(self) -> List[QueryConfigItem]:
        """
        Query to find out the configuration that the rule is using.
        """
        return [QueryConfigItem("code_blocks", self.__check_in_code_blocks)]

    def starting_new_file(self) -> None:
        """
        Event that the a new file to be scanned is starting.
        """
        # self.__container_tokens = []
        # self.__end_container_tokens_to_match :List[EndMarkdownToken] = []
        # self.__container_end_line_numbers = {}
        self.__leaf_tokens = []
        self.__line_index = 1
        self.__leaf_token_index = 0
        self.__last_fenced_code_end_token = None

    def next_token(self, context: PluginScanContext, token: MarkdownToken) -> None:
        """
        Event that a new token is being processed.
        """
        _ = context
        # if token.is_block_quote_start or token.is_list_start:
        #     container_token = cast(ContainerMarkdownToken, token)
        #     self.__container_tokens.append(container_token)
        # elif token.is_block_quote_end or token.is_list_end:
        #     end_token = cast(EndMarkdownToken, token)
        #     self.__end_container_tokens_to_match.append(end_token)
        # elif self.__end_container_tokens_to_match:
        #     while self.__end_container_tokens_to_match:
        #         next_end_token = self.__end_container_tokens_to_match[0]
        #         del self.__end_container_tokens_to_match[0]
        #         self.__container_end_line_numbers[next_end_token.start_markdown_token] = token.line_number

        if token.is_blank_line or token.is_leaf or token.is_end_of_stream:
            self.__leaf_tokens.append(token)
        elif token.is_fenced_code_block_end:
            self.__last_fenced_code_end_token = cast(EndMarkdownToken, token)

    def __is_line_inside_of_fenced_code_block(self) -> bool:
        is_inside_of_fenced_code_block = False
        leaf_token = self.__leaf_tokens[self.__leaf_token_index]
        if leaf_token.is_fenced_code_block:
            fenced_leaf_token = cast(FencedCodeBlockMarkdownToken, leaf_token)
            last_line_number = self.__leaf_tokens[
                self.__leaf_token_index + 1
            ].line_number
            end_code_block_line_number = (
                last_line_number
                if self.__last_fenced_code_end_token
                and self.__last_fenced_code_end_token.was_forced
                else last_line_number - 1
            )
            is_inside_of_fenced_code_block = (
                self.__line_index > fenced_leaf_token.line_number
                and self.__line_index < end_code_block_line_number
            )
        return is_inside_of_fenced_code_block

    def next_line(self, context: PluginScanContext, line: str) -> None:
        """
        Event that a new line is being processed.
        """
        if (
            self.__leaf_token_index + 1 < len(self.__leaf_tokens)
            and self.__line_index
            == self.__leaf_tokens[self.__leaf_token_index + 1].line_number
        ):
            self.__leaf_token_index += 1

        if "\t" in line:
            is_inside_of_fenced_code_block = (
                self.__is_line_inside_of_fenced_code_block()
            )
            can_trigger = (
                not self.__check_in_code_blocks and not is_inside_of_fenced_code_block
            )
            do_process = self.__check_in_code_blocks or can_trigger
            # if not do_process and not xx:
            #     ff = 0
            #     fj = []
            #     while ff < len(self.__container_tokens):
            #         fg = self.__container_tokens[ff]
            #         if self.__line_index < fg.line_number:
            #             break
            #         fh = self.__container_end_line_numbers[fg]
            #         if self.__line_index >fg.line_number and self.__line_index < fh:
            #             fj.append(fg)
            #         ff += 1
            #     x = 1
            #     assert False
        else:
            do_process = False
        if do_process:
            if context.in_fix_mode:
                context.set_current_fix_line(TabHelper.detabify_string(line))
            else:
                next_index = line.find("\t", 0)
                while next_index != -1:
                    line_before_tab = line[:next_index]
                    untabified_line_before_tab = TabHelper.detabify_string(
                        line_before_tab
                    )
                    column_number_of_tab = len(untabified_line_before_tab) + 1
                    self.report_next_line_error(
                        context,
                        column_number_of_tab,
                        extra_error_information=f"Column: {column_number_of_tab}",
                    )
                    next_index = line.find("\t", next_index + 1)

        self.__line_index += 1
