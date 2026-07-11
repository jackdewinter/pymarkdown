"""
Module to implement a custom Rule Plugin for required attributes on Fenced Code Blocks.
"""

import re
from dataclasses import dataclass
from html.parser import HTMLParser
from typing import Any, AnyStr, Dict, Optional, Tuple, Union, cast

from pymarkdown.plugin_manager.plugin_details import PluginDetailsV2, PluginDetailsV3
from pymarkdown.plugin_manager.plugin_scan_context import PluginScanContext
from pymarkdown.plugin_manager.rule_plugin import RulePlugin
from pymarkdown.tokens.fenced_code_block_markdown_token import (
    FencedCodeBlockMarkdownToken,
)
from pymarkdown.tokens.markdown_token import MarkdownToken


class RulePmd001(RulePlugin):
    """
    Class to implement a custom Rule Plugin for required attributes on Fenced Code Blocks.
    """

    def __init__(self) -> None:
        """
        Initialize an instance of the RuleMd001 class.
        """

    def get_details(self) -> PluginDetailsV2:
        """
        Get the details for the plugin.
        """
        return PluginDetailsV3(
            plugin_name="fenced-code-block-required-attributes",
            plugin_id="PMD001",
            plugin_enabled_by_default=True,
            plugin_description="Fenced code block must include required attributes.",
            plugin_version="0.0.1",
            plugin_configuration="front_matter_title",
        )

    @dataclass
    class RequiredAttributes:
        show_lines: bool
        title_regex: Optional[re.Pattern[AnyStr]]

    def initialize_from_config(self) -> None:
        """
        Event to allow the plugin to load configuration information.
        """
        # self.__front_matter_title = (
        #     self.plugin_configuration.get_string_property_with_default(
        #         "front_matter_title", "title"
        #     )
        # )
        self.required_attributes_map: Dict[str, RulePmd001.RequiredAttributes] = {}
        bob = "python;1;.*"
        for next_split_item in bob.split(","):
            next_split_item = next_split_item.strip().split(";", 2)
            code_block_language = next_split_item[0]
            show_lines = len(next_split_item) > 0 and next_split_item[1] == "1"
            match_pattern: Optional[re.Pattern[AnyStr]] = None
            if len(next_split_item) > 1:
                match_pattern = re.compile(next_split_item[2])
            self.required_attributes_map[code_block_language] = (
                RulePmd001.RequiredAttributes(show_lines, match_pattern)
            )

        print(self.required_attributes_map)

    class MyHTMLParser(HTMLParser):
        def __init__(self):
            self.attribute_map: Dict[str, Any] = {}
            super().__init__()

        def handle_starttag(
            self, tag: str, attrs: Tuple[str, Union[str, None]]
        ) -> None:
            for attribute_name, attribute_value in attrs:
                self.attribute_map[attribute_name] = attribute_value

    def __check_for_title_attribute(
        self,
        context: PluginScanContext,
        token: FencedCodeBlockMarkdownToken,
        parser: "RulePmd001.MyHTMLParser",
        ff: RequiredAttributes,
    ):
        attribute_value = parser.attribute_map.get("title", None)
        if not attribute_value:
            self.report_next_token_error(
                context,
                token,
                extra_error_information="Attribute 'title' not present after code block language.",
            )
        else:
            # f = attribute_value.
            pass

    def __check_for_linenums_attribute(
        self,
        context: PluginScanContext,
        token: FencedCodeBlockMarkdownToken,
        code_block_language: str,
        parser: "RulePmd001.MyHTMLParser",
        ff: RequiredAttributes,
    ):
        attribute_value = parser.attribute_map.get("linenums", None)
        if not attribute_value:
            self.report_next_token_error(
                context,
                token,
                extra_error_information="Attribute 'linenums' for code block language '{code_block_language}' not present after code block language.",
            )
        else:
            if not ff.show_lines:
                if attribute_value != "0":
                    self.report_next_token_error(
                        context,
                        token,
                        extra_error_information="Attribute 'linenums' for code block language '{code_block_language}' must have a value of '0'.",
                    )
            else:
                try:
                    dg = int(attribute_value)
                    if dg < 1:
                        self.report_next_token_error(
                            context,
                            token,
                            extra_error_information="Attribute 'linenums' for code block language '{code_block_language}' must be a positive integer, not '{dg}'.",
                        )
                except ValueError:
                    self.report_next_token_error(
                        context,
                        token,
                        extra_error_information="Attribute 'linenums' for code block language '{code_block_language}' must be an integer, not '{attribute_value}'.",
                    )

    def next_token(self, context: PluginScanContext, token: MarkdownToken) -> None:
        """
        Event that a new token is being processed.
        """
        if token.is_fenced_code_block:
            code_block_token = cast(FencedCodeBlockMarkdownToken, token)
            code_block_language = code_block_token.extracted_text.strip()
            if not code_block_language:
                return
            ff = self.required_attributes_map.get(code_block_language, None)
            if not ff:
                self.report_next_token_error(
                    context,
                    token,
                    extra_error_information=f"Code block language '{code_block_language}' not recognized.",
                )
                return
            parser = RulePmd001.MyHTMLParser()
            parser.feed(f"<code {code_block_token.text_after_extracted_text}>")
            self.__check_for_title_attribute(context, code_block_token, parser, ff)
            self.__check_for_linenums_attribute(
                context, code_block_token, code_block_language, parser, ff
            )
            print(">>" + str(parser.attribute_map))
            # title="pyproject.toml" linenums="1"
