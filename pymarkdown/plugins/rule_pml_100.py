"""
Module to implement a plugin that
"""

from typing import List, Set, Tuple, cast

from pymarkdown.extensions.disallowed_raw_html import MarkdownDisallowRawHtmlExtension
from pymarkdown.general.parser_helper import ParserHelper
from pymarkdown.plugin_manager.plugin_details import (
    PluginDetails,
    PluginDetailsV3,
    QueryConfigItem,
)
from pymarkdown.plugin_manager.plugin_scan_context import PluginScanContext
from pymarkdown.plugin_manager.rule_plugin import RulePlugin
from pymarkdown.plugins.utils.container_token_manager import ContainerTokenManager
from pymarkdown.tokens.block_quote_markdown_token import BlockQuoteMarkdownToken
from pymarkdown.tokens.list_start_markdown_token import ListStartMarkdownToken
from pymarkdown.tokens.markdown_token import MarkdownToken
from pymarkdown.tokens.raw_html_markdown_token import RawHtmlMarkdownToken
from pymarkdown.tokens.text_markdown_token import TextMarkdownToken


class RulePml100(RulePlugin):
    """
    Class to implement a plugin that
    """

    def __init__(self) -> None:
        super().__init__()
        self.__container_manager = ContainerTokenManager()
        self.__in_block = False
        self.__disallowed_tag_names: Set[str] = set()
        self.__modify_tag_names: str = ""

    def get_details(self) -> PluginDetails:
        """
        Get the details for the plugin.
        """
        return PluginDetailsV3(
            plugin_name="disallowed-html",
            plugin_id="PML100",
            plugin_enabled_by_default=False,
            plugin_description="Disallowed HTML",
            plugin_version="0.6.0",
            plugin_url="https://pymarkdown.readthedocs.io/en/latest/plugins/rule_pml100.md",
            plugin_configuration=None,
            plugin_supports_fix=False,
        )

    def initialize_from_config(self) -> None:
        """
        Event to allow the plugin to load configuration information.
        """
        self.__disallowed_tag_names = {
            "title",
            "textarea",
            "style",
            "xmp",
            "iframe",
            "noembed",
            "noframes",
            "script",
            "plaintext",
        }
        self.__modify_tag_names = (
            self.plugin_configuration.get_string_property_with_default(
                "change_tag_names", ""
            )
        )
        if self.__modify_tag_names:
            tag_config_name = "plugins.disallowed-html.change_tag_names"
            for next_tag_part in self.__modify_tag_names.split(","):
                next_tag_part = next_tag_part.strip(" ")
                if not next_tag_part:
                    raise ValueError(
                        f"Configuration item '{tag_config_name}' contains at least one empty string."
                    )
                if next_tag_part[0] not in ("+", "-"):
                    raise ValueError(
                        f"Configuration item '{tag_config_name}' elements must either start with '+' or '-'."
                    )
                remaining_tag_part = next_tag_part[1:]
                if not MarkdownDisallowRawHtmlExtension.is_valid_tag_name(
                    remaining_tag_part
                ):
                    raise ValueError(
                        f"Configuration item '{tag_config_name}' contains an element '{remaining_tag_part}' that is not a valid tag name."
                    )
                if next_tag_part[0] == "+":
                    self.__disallowed_tag_names.add(remaining_tag_part.lower())
                else:
                    self.__disallowed_tag_names.remove(remaining_tag_part.lower())

    def query_config(self) -> List[QueryConfigItem]:
        """
        Query to find out the configuration that the rule is using.
        """
        return [
            QueryConfigItem("change_tag_names", self.__modify_tag_names),
        ]

    def starting_new_file(self) -> None:
        """
        Event that the a new file to be scanned is starting.
        """
        self.__in_block = False
        self.__container_manager.clear()

    def next_token(self, context: PluginScanContext, token: MarkdownToken) -> None:
        """
        Event that a new token is being processed.
        """
        if token.is_html_block:
            self.__in_block = True
        elif token.is_html_block_end:
            self.__in_block = False
        elif self.__in_block and token.is_text:
            self.__scan_text_block(context, cast(TextMarkdownToken, token))
        elif token.is_inline_raw_html:
            self.__scan_text_token(context, cast(RawHtmlMarkdownToken, token))

        self.__container_manager.manage_container_tokens(token)

    def __find_delta_column(self, delta_text: str) -> Tuple[int, int]:
        if "\n" in delta_text:
            split_delta_text = delta_text.split(ParserHelper.newline_character)
            column_number_delta = -(len(split_delta_text[-1]) + 1)
            return len(split_delta_text) - 1, column_number_delta
        return 0, len(delta_text)

    def __scan_text_block(
        self, context: PluginScanContext, text_token: TextMarkdownToken
    ) -> None:
        ind = text_token.token_text.find("<")
        while ind >= 0:
            (
                after_text_index,
                collected_text,
            ) = ParserHelper.collect_until_one_of_characters(
                text_token.token_text, ind + 1, " /<>"
            )
            if collected_text in self.__disallowed_tag_names:
                extra_data = f"Tag Name: {collected_text}"
                text_so_far = text_token.token_text[:ind]
                line_number_delta, column_number_delta = self.__find_delta_column(
                    text_so_far
                )

                if len(self.__container_manager.container_token_stack) > 0:
                    if container_base_column := self.__calculate_base_column(
                        column_number_delta, text_so_far
                    ):
                        column_number_delta -= container_base_column

                self.report_next_token_error(
                    context,
                    text_token,
                    extra_error_information=extra_data,
                    line_number_delta=line_number_delta,
                    column_number_delta=column_number_delta,
                )
            ind = text_token.token_text.find("<", after_text_index)

    def __scan_text_token(
        self, context: PluginScanContext, text_token: RawHtmlMarkdownToken
    ) -> None:
        assert text_token.extra_data is not None
        split_text = text_token.extra_data.split(" ", 1)
        collected_text = split_text[0]
        if collected_text.endswith("/"):
            collected_text = collected_text[:-1]
        if collected_text in self.__disallowed_tag_names:
            extra_data = f"Tag Name: {collected_text}"
            self.report_next_token_error(
                context, text_token, extra_error_information=extra_data
            )

    def __calculate_base_column(
        self, column_number_delta: int, text_so_far: str
    ) -> int:
        container_base_column = 0
        stack_index = len(self.__container_manager.container_token_stack) - 1
        top_one = self.__container_manager.container_token_stack[-1]
        if top_one.is_list_start:
            if column_number_delta < 0:
                list_token = cast(
                    ListStartMarkdownToken,
                    self.__container_manager.container_token_stack[stack_index],
                )
                container_base_column = list_token.indent_level
        else:
            assert top_one.is_block_quote_start
            container_base_column = 0
            count_of_block_quote_characters = text_so_far.count(">")
            if count_of_block_quote_characters > 0:
                bq_index = (
                    self.__container_manager.bq_line_index[stack_index + 1]
                    + count_of_block_quote_characters
                )
                block_quote_token = cast(
                    BlockQuoteMarkdownToken,
                    self.__container_manager.container_token_stack[stack_index],
                )
                assert block_quote_token.bleading_spaces is not None
                split_leading_spaces = block_quote_token.bleading_spaces.split(
                    ParserHelper.newline_character
                )
                container_base_column = len(split_leading_spaces[bq_index])
                assert column_number_delta < 0
                # if column_number_delta >= 0:
                #     container_base_column = -container_base_column

        return container_base_column
