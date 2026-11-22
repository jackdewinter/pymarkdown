"""
Module to implement a plugin that ensures that the style of strong emphasis is consistent.
"""

from typing import List, cast

from pymarkdown.plugin_manager.plugin_details import (
    PluginDetailsV2,
    PluginDetailsV3,
    QueryConfigItem,
)
from pymarkdown.plugin_manager.plugin_scan_context import PluginScanContext
from pymarkdown.plugin_manager.rule_plugin import RulePlugin
from pymarkdown.tokens.emphasis_markdown_token import EmphasisMarkdownToken
from pymarkdown.tokens.markdown_token import MarkdownToken


class RuleMd050(RulePlugin):
    """
    Class to implement a plugin that ensures that the style of strong emphasis is consistent.
    """

    __consistent_style = "consistent"
    __asterisk_style = "asterisk"
    __underscore_style = "underscore"
    __valid_styles = [
        __consistent_style,
        __asterisk_style,
        __underscore_style,
    ]

    def __init__(self) -> None:
        """
        Initialize an instance of the RuleMd048 class.
        """
        super().__init__()
        self.__style_type: str = ""
        self.__actual_style_type: str = ""

    def get_details(self) -> PluginDetailsV2:
        """
        Get the details for the plugin.
        """
        return PluginDetailsV3(
            plugin_name="strong-style",
            plugin_id="MD050",
            plugin_enabled_by_default=True,
            plugin_description="Strong style",
            plugin_version="0.5.0",
            plugin_url="https://pymarkdown.readthedocs.io/en/latest/plugins/rule_md050.md",
            plugin_configuration="style",
            # plugin_supports_fix=True,
            # plugin_fix_level=2,
        )

    @classmethod
    def __validate_configuration_style(cls, found_value: str) -> None:
        if found_value not in RuleMd050.__valid_styles:
            raise ValueError(f"Allowable values: {RuleMd050.__valid_styles}")

    def initialize_from_config(self) -> None:
        """
        Event to allow the plugin to load configuration information.
        """
        self.__style_type = self.plugin_configuration.get_string_property_with_default(
            "style",
            RuleMd050.__consistent_style,
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
            if self.__style_type != RuleMd050.__consistent_style
            else ""
        )

    def next_token(self, context: PluginScanContext, token: MarkdownToken) -> None:
        """
        Event that a new token is being processed.
        """
        if not token.is_inline_emphasis:
            return

        emphasis_token = cast(EmphasisMarkdownToken, token)
        if emphasis_token.emphasis_length != 2:
            return

        if emphasis_token.emphasis_character == "*":
            current_style = RuleMd050.__asterisk_style
        elif emphasis_token.emphasis_character == "_":
            current_style = RuleMd050.__underscore_style
        else:
            return

        if not self.__actual_style_type:
            self.__actual_style_type = current_style
        if self.__actual_style_type != current_style:
            #     if context.in_fix_mode:
            #         replace_character = (
            #             "`"
            #             if self.__actual_style_type == RuleMd048.__backtick_style
            #             else "~"
            #         )
            #         self.register_fix_token_request(
            #             context, token, "next_token", "fence_character", replace_character
            #         )
            #     else:
            extra_data = (
                f"Expected: {self.__actual_style_type}; Actual: {current_style}"
            )
            self.report_next_token_error(
                context, token, extra_error_information=extra_data
            )
