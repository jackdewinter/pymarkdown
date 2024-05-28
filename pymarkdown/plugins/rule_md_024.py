"""
Module to implement a plugin that looks for multiple heading lines with the same
content.
"""

from typing import Dict, List, Optional, cast

from pymarkdown.plugin_manager.plugin_details import (
    PluginDetails,
    PluginDetailsV3,
    QueryConfigItem,
)
from pymarkdown.plugin_manager.plugin_scan_context import PluginScanContext
from pymarkdown.plugin_manager.rule_plugin import RulePlugin
from pymarkdown.tokens.atx_heading_markdown_token import AtxHeadingMarkdownToken
from pymarkdown.tokens.markdown_token import MarkdownToken


class RuleMd024(RulePlugin):
    """
    Class to implement a plugin that looks for multiple heading lines with the same
    content.
    """

    def __init__(self) -> None:
        super().__init__()
        self.__heading_text: Optional[str] = None
        self.__start_token: Optional[MarkdownToken] = None
        self.__hash_count: int = -1
        self.__last_hash_count: int = 0
        self.__siblings_only: bool = False
        self.__heading_content_map: List[Dict[str, str]] = []

    def get_details(self) -> PluginDetails:
        """
        Get the details for the plugin.
        """
        return PluginDetailsV3(
            plugin_name="no-duplicate-heading,no-duplicate-header",
            plugin_id="MD024",
            plugin_enabled_by_default=True,
            plugin_description="Multiple headings cannot contain the same content.",
            plugin_version="0.6.0",
            plugin_url="https://pymarkdown.readthedocs.io/en/latest/plugins/rule_md024.md",
            plugin_configuration="siblings_only, allow_different_nesting",
        )

    def initialize_from_config(self) -> None:
        """
        Event to allow the plugin to load configuration information.
        """
        self.__siblings_only = self.plugin_configuration.get_boolean_property(
            "siblings_only", default_value=False
        ) or self.plugin_configuration.get_boolean_property(
            "allow_different_nesting", default_value=False
        )

    def query_config(self) -> List[QueryConfigItem]:
        """
        Query to find out the configuration that the rule is using.
        """
        return [
            QueryConfigItem("siblings_only", self.__siblings_only),
            QueryConfigItem("allow_different_nesting", self.__siblings_only),
        ]

    def starting_new_file(self) -> None:
        """
        Event that the a new file to be scanned is starting.
        """
        self.__heading_text = None
        self.__start_token = None
        self.__hash_count = -1
        self.__last_hash_count = 0
        self.__heading_content_map = (
            [{}, {}, {}, {}, {}, {}] if self.__siblings_only else [{}]
        )

    def next_token(self, context: PluginScanContext, token: MarkdownToken) -> None:
        """
        Event that a new token is being processed.
        """
        skip_this_token = False
        if token.is_setext_heading or token.is_atx_heading:
            atx_heading_token = cast(AtxHeadingMarkdownToken, token)
            self.handle_heading_start(atx_heading_token)
            skip_this_token = True
        elif token.is_setext_heading_end or token.is_atx_heading_end:
            self.handler_heading_end(context, token)

        if not skip_this_token and self.__heading_text is not None:
            self.__heading_text += token.debug_string(include_column_row_info=False)

    def handle_heading_start(self, token: AtxHeadingMarkdownToken) -> None:
        """
        Process the start heading token, atx or setext
        """
        self.__heading_text = ""
        self.__start_token = token
        self.__hash_count = token.hash_count if self.__siblings_only else 1

    def handler_heading_end(
        self, context: PluginScanContext, token: MarkdownToken
    ) -> None:
        """
        Process the end heading token, atx or setext
        """

        if self.__last_hash_count:
            while self.__last_hash_count < self.__hash_count:
                self.__last_hash_count += 1
                self.__heading_content_map[self.__last_hash_count - 1] = {}
            while self.__last_hash_count > self.__hash_count:
                self.__heading_content_map[self.__last_hash_count - 1] = {}
                self.__last_hash_count -= 1

        past_headings_map = self.__heading_content_map[self.__hash_count - 1]

        assert self.__heading_text is not None
        if self.__heading_text in past_headings_map:
            assert self.__start_token is not None
            self.report_next_token_error(
                context,
                self.__start_token,
                use_original_position=token.is_setext_heading_end,
            )
        else:
            past_headings_map[self.__heading_text] = self.__heading_text
        self.__heading_text = None
        self.__last_hash_count = self.__hash_count
