"""
Module to implement a plugin that looks for inconsistencies in the
style used for Unordered List elements.
"""

from typing import Dict, cast

from pymarkdown.plugin_manager.plugin_details import PluginDetailsV2
from pymarkdown.plugin_manager.plugin_scan_context import PluginScanContext
from pymarkdown.plugin_manager.rule_plugin import RulePlugin
from pymarkdown.tokens.markdown_token import MarkdownToken
from pymarkdown.tokens.unordered_list_start_markdown_token import (
    UnorderedListStartMarkdownToken,
)


class RuleMd004(RulePlugin):
    """
    Class to implement a plugin that looks for inconsistencies in the
    style used for Unordered List elements.
    """

    __consistent_style = "consistent"
    __asterisk_style = "asterisk"
    __plus_style = "plus"
    __dash_style = "dash"
    __sublist_style = "sublist"

    __valid_styles = [
        __consistent_style,
        __asterisk_style,
        __plus_style,
        __dash_style,
        __sublist_style,
    ]

    def __init__(self) -> None:
        super().__init__()
        self.__style_type = ""
        self.__actual_style_type: Dict[int, str] = {}
        self.__current_list_level = 0

    def get_details(self) -> PluginDetailsV2:
        """
        Get the details for the plugin.
        """
        return PluginDetailsV2(
            # bullet, ul
            plugin_name="ul-style",
            plugin_id="MD004",
            plugin_enabled_by_default=True,
            plugin_description="Inconsistent Unordered List Start style",
            plugin_version="0.5.1",
            plugin_url="https://github.com/jackdewinter/pymarkdown/blob/main/docs/rules/rule_md004.md",
            plugin_configuration="style",
            plugin_supports_fix=True,
        )

    @classmethod
    def __validate_configuration_style(cls, found_value: str) -> None:
        if found_value not in RuleMd004.__valid_styles:
            raise ValueError(f"Allowable values: {RuleMd004.__valid_styles}")

    def initialize_from_config(self) -> None:
        """
        Event to allow the plugin to load configuration information.
        """
        self.__style_type = self.plugin_configuration.get_string_property(
            "style",
            default_value=RuleMd004.__consistent_style,
            valid_value_fn=self.__validate_configuration_style,
        )

    def starting_new_file(self) -> None:
        """
        Event that the a new file to be scanned is starting.
        """
        self.__actual_style_type = {}
        self.__current_list_level = 0
        if self.__style_type not in (
            RuleMd004.__consistent_style,
            RuleMd004.__sublist_style,
        ):
            self.__actual_style_type[0] = self.__style_type

    @classmethod
    def __get_sequence_type(cls, token: UnorderedListStartMarkdownToken) -> str:
        if token.list_start_sequence == "*":
            return RuleMd004.__asterisk_style
        if token.list_start_sequence == "+":
            return RuleMd004.__plus_style
        assert token.list_start_sequence == "-"
        return RuleMd004.__dash_style

    def __next_token_triggered(
        self, context: PluginScanContext, token: MarkdownToken, this_start_style: str
    ) -> None:
        if context.in_fix_mode:
            if (
                self.__actual_style_type[self.__current_list_level]
                == RuleMd004.__plus_style
            ):
                new_start_sequence = "+"
            elif (
                self.__actual_style_type[self.__current_list_level]
                == RuleMd004.__dash_style
            ):
                new_start_sequence = "-"
            else:
                new_start_sequence = "*"
            self.register_fix_token_request(
                context, token, "next_token", "list_start_sequence", new_start_sequence
            )
        else:
            extra_data = (
                f"Expected: {self.__actual_style_type[self.__current_list_level]}; "
                + f"Actual: {this_start_style}"
            )
            self.report_next_token_error(context, token, extra_data)

    def next_token(self, context: PluginScanContext, token: MarkdownToken) -> None:
        """
        Event that a new token is being processed.
        """
        if token.is_unordered_list_start:
            list_token = cast(UnorderedListStartMarkdownToken, token)
            if self.__current_list_level not in self.__actual_style_type:
                if self.__style_type in (RuleMd004.__sublist_style,) or (
                    self.__style_type in (RuleMd004.__consistent_style)
                    and not self.__actual_style_type
                ):
                    self.__actual_style_type[self.__current_list_level] = (
                        self.__get_sequence_type(list_token)
                    )
                else:
                    self.__actual_style_type[self.__current_list_level] = (
                        self.__actual_style_type[0]
                    )

            this_start_style = self.__get_sequence_type(list_token)
            if self.__actual_style_type[self.__current_list_level] != this_start_style:
                self.__next_token_triggered(context, token, this_start_style)
            self.__current_list_level += 1
        elif token.is_unordered_list_end:
            self.__current_list_level -= 1
