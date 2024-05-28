"""
Module to implement a plugin that ensures the code blocks maintain a consistent style.
"""

from typing import List

from pymarkdown.plugin_manager.plugin_details import (
    PluginDetails,
    PluginDetailsV3,
    QueryConfigItem,
)
from pymarkdown.plugin_manager.plugin_scan_context import PluginScanContext
from pymarkdown.plugin_manager.rule_plugin import RulePlugin
from pymarkdown.tokens.markdown_token import MarkdownToken


class RuleMd046(RulePlugin):
    """
    Class to implement a plugin that ensures the code blocks maintain a consistent style.
    """

    __consistent_style = "consistent"
    __fenced_style = "fenced"
    __indented_style = "indented"
    __valid_styles = [
        __consistent_style,
        __fenced_style,
        __indented_style,
    ]

    def __init__(self) -> None:
        super().__init__()
        self.__style_type: str = ""
        self.__actual_style_type: str = ""

    def get_details(self) -> PluginDetails:
        """
        Get the details for the plugin.
        """
        return PluginDetailsV3(
            plugin_name="code-block-style",
            plugin_id="MD046",
            plugin_enabled_by_default=True,
            plugin_description="Code block style",
            plugin_version="0.6.0",
            plugin_url="https://pymarkdown.readthedocs.io/en/latest/plugins/rule_md046.md",
            plugin_configuration="style",
        )

    @classmethod
    def __validate_configuration_style(cls, found_value: str) -> None:
        if found_value not in RuleMd046.__valid_styles:
            raise ValueError(f"Allowable values: {RuleMd046.__valid_styles}")

    def initialize_from_config(self) -> None:
        """
        Event to allow the plugin to load configuration information.
        """
        self.__style_type = self.plugin_configuration.get_string_property(
            "style",
            default_value=RuleMd046.__consistent_style,
            valid_value_fn=self.__validate_configuration_style,
        )

    def query_config(self) -> List[QueryConfigItem]:
        """
        Query to find out the configuration that the rule is using.
        """
        return [
            QueryConfigItem("style", self.__style_type),
        ]

    def starting_new_file(self) -> None:
        """
        Event that the a new file to be scanned is starting.
        """
        self.__actual_style_type = (
            self.__style_type
            if self.__style_type != RuleMd046.__consistent_style
            else ""
        )

    def next_token(self, context: PluginScanContext, token: MarkdownToken) -> None:
        """
        Event that a new token is being processed.
        """
        if token.is_code_block:
            current_style = (
                RuleMd046.__fenced_style
                if token.is_fenced_code_block
                else RuleMd046.__indented_style
            )
            if not self.__actual_style_type:
                self.__actual_style_type = current_style
            if self.__actual_style_type != current_style:
                extra_data = (
                    f"Expected: {self.__actual_style_type}; Actual: {current_style}"
                )
                self.report_next_token_error(
                    context, token, extra_error_information=extra_data
                )
