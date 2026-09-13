"""
Module to implement a plugin that ensures that visible text for links are not boilerplate.
"""

from typing import List, cast

from pymarkdown.plugin_manager.plugin_details import (
    PluginDetailsV2,
    PluginDetailsV3,
    QueryConfigItem,
)
from pymarkdown.plugin_manager.plugin_scan_context import PluginScanContext
from pymarkdown.plugin_manager.rule_plugin import RulePlugin
from pymarkdown.tokens.image_start_markdown_token import ImageStartMarkdownToken
from pymarkdown.tokens.link_start_markdown_token import LinkStartMarkdownToken
from pymarkdown.tokens.markdown_token import MarkdownToken


class RuleMd059(RulePlugin):
    """
    Class to implement a plugin that ensures that visible text for links are not boilerplate.
    """

    def __init__(self) -> None:
        """
        Initialize an instance of the RuleMd048 class.
        """
        super().__init__()
        self.__prohibited_phrases: List[str] = []

    def get_details(self) -> PluginDetailsV2:
        """
        Get the details for the plugin.
        """
        return PluginDetailsV3(
            plugin_name="descriptive-link-text",
            plugin_id="MD059",
            plugin_enabled_by_default=True,
            plugin_description="Link text should be descriptive.",
            plugin_version="0.5.0",
            plugin_url="https://pymarkdown.readthedocs.io/en/latest/plugins/rule_md059.md",
            plugin_configuration="prohibited-phrases",
        )

    def initialize_from_config(self) -> None:
        """
        Event to allow the plugin to load configuration information.
        """
        prohibited_phrases_source = (
            self.plugin_configuration.get_string_property_with_default(
                "prohibited-phrases", "click here,here,link,more"
            )
        )
        self.__prohibited_phrases = []
        for next_phrase in prohibited_phrases_source.split(","):
            if next_phrase := self.__sanitize(next_phrase):
                self.__prohibited_phrases.append(next_phrase)

    def __sanitize(self, string_to_sanitize: str) -> str:
        sanitized_string = string_to_sanitize.strip().lower()
        while "  " in sanitized_string:
            sanitized_string = sanitized_string.replace("  ", " ")
        return sanitized_string

    def query_config(self) -> List[QueryConfigItem]:
        """
        Query to find out the configuration that the rule is using.
        """
        return [
            QueryConfigItem("prohibited-phrases", str(self.__prohibited_phrases)),
        ]

    def next_token(self, context: PluginScanContext, token: MarkdownToken) -> None:
        """
        Event that a new token is being processed.
        """
        if not token.is_inline_link and not token.is_inline_image:
            return

        if token.is_inline_link:
            link_token = cast(LinkStartMarkdownToken, token)
            token_text = self.__sanitize(link_token.text_from_blocks)
        else:
            image_token = cast(ImageStartMarkdownToken, token)
            token_text = self.__sanitize(image_token.text_from_blocks)
        if token_text in self.__prohibited_phrases:
            self.report_next_token_error(context, token, extra_error_information=None)
