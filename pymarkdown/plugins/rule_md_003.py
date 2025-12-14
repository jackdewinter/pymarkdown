"""
Module to implement a plugin that looks for heading styles that are inconsistent
throughout the document.
"""

from typing import List, Tuple, cast

from pymarkdown.plugin_manager.plugin_details import (
    PluginDetails,
    PluginDetailsV3,
    QueryConfigItem,
)
from pymarkdown.plugin_manager.plugin_scan_context import PluginScanContext
from pymarkdown.plugin_manager.rule_plugin import RulePlugin
from pymarkdown.tokens.atx_heading_markdown_token import AtxHeadingMarkdownToken
from pymarkdown.tokens.markdown_token import MarkdownToken


class RuleMd003(RulePlugin):
    """
    Class to implement a plugin that looks for heading styles that are inconsistent
    throughout the document.
    """

    __consistent_style = "consistent"
    __atx_style = "atx"
    __atx_closed_style = "atx_closed"
    __setext_style = "setext"
    __setext_with_atx_style = "setext_with_atx"
    __setext_with_atx_closed_style = "setext_with_atx_closed"

    __simple_styles = [__atx_style, __atx_closed_style, __setext_style]
    __valid_styles = [
        __consistent_style,
        __atx_style,
        __atx_closed_style,
        __setext_style,
        __setext_with_atx_style,
        __setext_with_atx_closed_style,
    ]

    def __init__(self) -> None:
        super().__init__()
        self.__style_type: str = ""
        self.__actual_style_type: str = ""
        self.__allow_consistent_setext_update = False

    def get_details(self) -> PluginDetails:
        """
        Get the details for the plugin.
        """
        return PluginDetailsV3(
            plugin_name="heading-style,header-style",
            plugin_id="MD003",
            plugin_enabled_by_default=True,
            plugin_description="Heading style should be consistent throughout the document.",
            plugin_version="0.6.1",
            plugin_url="https://pymarkdown.readthedocs.io/en/latest/plugins/rule_md003.md",
            plugin_configuration="style",
        )

    @classmethod
    def __validate_configuration_style(cls, found_value: str) -> None:
        if found_value not in RuleMd003.__valid_styles:
            raise ValueError(f"Allowable values: {RuleMd003.__valid_styles}")

    def initialize_from_config(self) -> None:
        """
        Event to allow the plugin to load configuration information.
        """
        self.__style_type = self.plugin_configuration.get_string_property_with_default(
            "style",
            RuleMd003.__consistent_style,
            valid_value_fn=self.__validate_configuration_style,
        )
        self.__allow_consistent_setext_update = (
            self.plugin_configuration.get_boolean_property_with_default(
                "allow-setext-update", False
            )
            if self.__style_type == RuleMd003.__consistent_style
            else False
        )

    def query_config(self) -> List[QueryConfigItem]:
        """
        Query to find out the configuration that the rule is using.
        """
        return [
            QueryConfigItem("style", self.__style_type),
            QueryConfigItem(
                "allow-setext-update", self.__allow_consistent_setext_update
            ),
        ]

    def starting_new_file(self) -> None:
        """
        Event that the a new file to be scanned is starting.
        """
        self.__actual_style_type = (
            self.__style_type
            if self.__style_type != RuleMd003.__consistent_style
            else ""
        )

    def __handle_simple_styles(
        self, heading_style_type: str, is_heading_level_1_or_2: bool
    ) -> Tuple[bool, str]:
        is_heading_bad = heading_style_type != self.__actual_style_type

        if (
            is_heading_bad
            and self.__allow_consistent_setext_update
            and self.__actual_style_type == RuleMd003.__setext_style
            and heading_style_type == RuleMd003.__atx_style
            and not is_heading_level_1_or_2
        ):
            is_heading_bad = False
            self.__actual_style_type = RuleMd003.__setext_with_atx_style

        expected_style_type = self.__actual_style_type
        return is_heading_bad, expected_style_type

    def __handle_complex_styles(
        self, heading_style_type: str, is_heading_level_1_or_2: bool
    ) -> Tuple[bool, str]:
        is_heading_bad, expected_style_type = False, ""
        if self.__actual_style_type == RuleMd003.__setext_with_atx_style:
            base_atx_style = RuleMd003.__atx_style
        else:
            assert self.__actual_style_type == RuleMd003.__setext_with_atx_closed_style
            base_atx_style = RuleMd003.__atx_closed_style
        if not (
            (is_heading_level_1_or_2 and heading_style_type == RuleMd003.__setext_style)
            or (not is_heading_level_1_or_2 and heading_style_type == base_atx_style)
        ):
            is_heading_bad = True
            expected_style_type = (
                RuleMd003.__setext_style if is_heading_level_1_or_2 else base_atx_style
            )
            if (
                expected_style_type == RuleMd003.__setext_style
                and is_heading_level_1_or_2
                and self.__actual_style_type == RuleMd003.__setext_with_atx_style
            ):
                expected_style_type = RuleMd003.__setext_with_atx_style
        return is_heading_bad, expected_style_type

    def next_token(self, context: PluginScanContext, token: MarkdownToken) -> None:
        """
        Event that a new token is being processed.
        """
        heading_style_type, is_heading_level_1_or_2 = self.__get_heading_properties(
            token
        )

        is_heading_bad = False
        if heading_style_type:
            expected_style_type = None
            if not self.__actual_style_type:
                self.__actual_style_type = heading_style_type
            elif self.__actual_style_type in RuleMd003.__simple_styles:
                is_heading_bad, expected_style_type = self.__handle_simple_styles(
                    heading_style_type, is_heading_level_1_or_2
                )
            else:
                is_heading_bad, expected_style_type = self.__handle_complex_styles(
                    heading_style_type, is_heading_level_1_or_2
                )

            if is_heading_bad:
                extra_data = (
                    f"Expected: {expected_style_type}; Actual: {heading_style_type}"
                )
                self.report_next_token_error(
                    context,
                    token,
                    extra_error_information=extra_data,
                    use_original_position=token.is_setext_heading,
                )

    @classmethod
    def __get_heading_properties(cls, token: MarkdownToken) -> Tuple[str, bool]:
        """
        Determine the heading properties related to the current token.
        """

        heading_style_type = ""
        is_heading_level_1_or_2 = False
        if token.is_atx_heading:
            atx_token = cast(AtxHeadingMarkdownToken, token)
            heading_style_type = (
                RuleMd003.__atx_closed_style
                if atx_token.remove_trailing_count
                else RuleMd003.__atx_style
            )
            is_heading_level_1_or_2 = atx_token.hash_count < 3
        elif token.is_setext_heading:
            heading_style_type = RuleMd003.__setext_style
            is_heading_level_1_or_2 = True
        return heading_style_type, is_heading_level_1_or_2
