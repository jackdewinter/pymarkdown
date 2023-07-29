"""
Module to implement a plugin that ensures that the style of fenced code blocks is consistent.
"""
from typing import cast

from pymarkdown.plugin_manager.plugin_details import PluginDetails
from pymarkdown.plugin_manager.plugin_scan_context import PluginScanContext
from pymarkdown.plugin_manager.rule_plugin import RulePlugin
from pymarkdown.tokens.fenced_code_block_markdown_token import (
    FencedCodeBlockMarkdownToken,
)
from pymarkdown.tokens.markdown_token import MarkdownToken


class RuleMd048(RulePlugin):
    """
    Class to implement a plugin that ensures that the style of fenced code blocks is consistent.
    """

    __consistent_style = "consistent"
    __tilde_style = "tilde"
    __backtick_style = "backtick"
    __valid_styles = [
        __consistent_style,
        __tilde_style,
        __backtick_style,
    ]

    def __init__(self) -> None:
        super().__init__()
        self.__style_type: str = ""
        self.__actual_style_type: str = ""

    def get_details(self) -> PluginDetails:
        """
        Get the details for the plugin.
        """
        return PluginDetails(
            plugin_name="code-fence-style",
            plugin_id="MD048",
            plugin_enabled_by_default=True,
            plugin_description="Code fence style",
            plugin_version="0.5.0",
            plugin_interface_version=1,
            plugin_url="https://github.com/jackdewinter/pymarkdown/blob/main/docs/rules/rule_md048.md",
            plugin_configuration="style",
        )

    @classmethod
    def __validate_configuration_style(cls, found_value: str) -> None:
        if found_value not in RuleMd048.__valid_styles:
            raise ValueError(f"Allowable values: {RuleMd048.__valid_styles}")

    def initialize_from_config(self) -> None:
        """
        Event to allow the plugin to load configuration information.
        """
        self.__style_type = self.plugin_configuration.get_string_property(
            "style",
            default_value=RuleMd048.__consistent_style,
            valid_value_fn=self.__validate_configuration_style,
        )

    def starting_new_file(self) -> None:
        """
        Event that the a new file to be scanned is starting.
        """
        self.__actual_style_type = ""
        if self.__style_type != RuleMd048.__consistent_style:
            self.__actual_style_type = self.__style_type

    def next_token(self, context: PluginScanContext, token: MarkdownToken) -> None:
        """
        Event that a new token is being processed.
        """
        if token.is_fenced_code_block:
            fence_token = cast(FencedCodeBlockMarkdownToken, token)
            current_style = (
                RuleMd048.__backtick_style
                if fence_token.fence_character == "`"
                else RuleMd048.__tilde_style
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
