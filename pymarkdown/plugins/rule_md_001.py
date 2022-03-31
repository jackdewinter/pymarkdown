"""
Module to implement a plugin that looks for heading that increment more than one
level at a time (going up).
"""
from typing import cast

from pymarkdown.extensions.front_matter_markdown_token import FrontMatterMarkdownToken
from pymarkdown.leaf_markdown_token import SetextHeadingMarkdownToken
from pymarkdown.markdown_token import MarkdownToken
from pymarkdown.plugin_manager.plugin_details import PluginDetails
from pymarkdown.plugin_manager.plugin_scan_context import PluginScanContext
from pymarkdown.plugin_manager.rule_plugin import RulePlugin


class RuleMd001(RulePlugin):
    """
    Class to implement a plugin that looks for headings that increment more than one
    level at a time (going up).
    """

    def __init__(self) -> None:
        super().__init__()
        self.__last_heading_count: int = 0
        self.__front_matter_title = None

    def get_details(self) -> PluginDetails:
        """
        Get the details for the plugin.
        """
        return PluginDetails(
            plugin_name="heading-increment,header-increment",
            plugin_id="MD001",
            plugin_enabled_by_default=True,
            plugin_description="Heading levels should only increment by one level at a time.",
            plugin_version="0.5.0",
            plugin_interface_version=1,
            plugin_url="https://github.com/jackdewinter/pymarkdown/blob/main/docs/rules/rule_md001.md",
            plugin_configuration="front_matter_title",
        )

    def initialize_from_config(self) -> None:
        self.__front_matter_title = self.plugin_configuration.get_string_property(
            "front_matter_title", default_value="title"
        ).lower()

    def starting_new_file(self) -> None:
        """
        Event that the a new file to be scanned is starting.
        """
        self.__last_heading_count = 0

    def next_token(self, context: PluginScanContext, token: MarkdownToken) -> None:
        """
        Event that a new token is being processed.
        """
        hash_count = None
        if token.is_atx_heading or token.is_setext_heading:
            setext_token = cast(SetextHeadingMarkdownToken, token)
            hash_count = setext_token.hash_count
        elif token.is_front_matter:
            front_matter_token = cast(FrontMatterMarkdownToken, token)
            if self.__front_matter_title in front_matter_token.matter_map:
                hash_count = 1

        if hash_count:
            if self.__last_heading_count and (hash_count > self.__last_heading_count):
                delta = hash_count - self.__last_heading_count
                if delta > 1:
                    extra_data = f"Expected: h{self.__last_heading_count + 1}; Actual: h{hash_count}"
                    self.report_next_token_error(
                        context, token, extra_error_information=extra_data
                    )
            self.__last_heading_count = hash_count
