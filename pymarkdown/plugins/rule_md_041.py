"""
Module to implement a plugin that ensures that the first line in a file is a top level heading.
"""

import re
from typing import List, Optional, cast

from pymarkdown.extensions.front_matter_markdown_token import FrontMatterMarkdownToken
from pymarkdown.plugin_manager.plugin_details import (
    PluginDetails,
    PluginDetailsV3,
    QueryConfigItem,
)
from pymarkdown.plugin_manager.plugin_scan_context import PluginScanContext
from pymarkdown.plugin_manager.rule_plugin import RulePlugin
from pymarkdown.tokens.atx_heading_markdown_token import AtxHeadingMarkdownToken
from pymarkdown.tokens.markdown_token import MarkdownToken
from pymarkdown.tokens.text_markdown_token import TextMarkdownToken


class RuleMd041(RulePlugin):
    """
    Class to implement a plugin that ensures that the first line in a file is a top level heading.
    """

    def __init__(self) -> None:
        super().__init__()
        self.__start_level: int = -1
        self.__front_matter_title: str = ""
        self.__have_seen_first_token: bool = False
        self.__seen_html_block_start: Optional[MarkdownToken] = None
        self.__wait_for_html_end = False
        self.__html_tags_to_skip: List[str] = []

    def get_details(self) -> PluginDetails:
        """
        Get the details for the plugin.
        """
        return PluginDetailsV3(
            plugin_name="first-line-heading,first-line-h1",
            plugin_id="MD041",
            plugin_enabled_by_default=True,
            plugin_description="First line in file should be a top level heading",
            plugin_version="0.7.1",
            plugin_url="https://pymarkdown.readthedocs.io/en/latest/plugins/rule_md041.md",
            plugin_configuration="level,front_matter_title",
        )

    @classmethod
    def __validate_configuration_level(cls, found_value: int) -> None:
        if found_value < 1 or found_value > 6:
            raise ValueError("Allowable values are between 1 and 6.")

    @classmethod
    def __validate_configuration_title(cls, found_value: str) -> None:
        found_value = found_value.strip(" ")
        if ":" in found_value:
            raise ValueError("Colons (:) are not allowed in the value.")

    def initialize_from_config(self) -> None:
        """
        Event to allow the plugin to load configuration information.
        """
        self.__start_level = (
            self.plugin_configuration.get_integer_property_with_default(
                "level",
                1,
                valid_value_fn=self.__validate_configuration_level,
            )
        )
        self.__front_matter_title = (
            self.plugin_configuration.get_string_property_with_default(
                "front_matter_title",
                "title",
                valid_value_fn=self.__validate_configuration_title,
            )
            .lower()
            .strip(" ")
        )

        self.__html_tags_to_skip = ["<!--"]
        eligible_tags = self.plugin_configuration.get_string_property_with_default(
            "invisible_tags",
            "link",
            valid_value_fn=self.__validate_configuration_title,
        )

        for next_tag in eligible_tags.split(","):
            next_tag = next_tag.strip(" ")
            if next_tag == "":
                raise ValueError("Empty tag name found in between commas.")
            if re.match(r"^[a-zA-Z][a-zA-Z0-9]*$", next_tag) is None:
                raise ValueError(f"Invalid tag name '{next_tag}' found between commas.")
            self.__html_tags_to_skip.append(f"<{next_tag}")

    def query_config(self) -> List[QueryConfigItem]:
        """
        Query to find out the configuration that the rule is using.
        """
        return [
            QueryConfigItem("level", self.__start_level),
            QueryConfigItem("front_matter_title", self.__front_matter_title),
            QueryConfigItem("invisible_tags", ",".join(self.__html_tags_to_skip)),
        ]

    def starting_new_file(self) -> None:
        """
        Event that the a new file to be scanned is starting.
        """
        self.__have_seen_first_token = False
        self.__seen_html_block_start = None
        self.__wait_for_html_end = False
        self.__wait_for_html_end = False

    def __handle_heading_start(
        self, context: PluginScanContext, token: MarkdownToken
    ) -> None:
        atx_token = cast(AtxHeadingMarkdownToken, token)
        self.__have_seen_first_token = True
        if atx_token.hash_count != self.__start_level:
            self.report_next_token_error(
                context, token, use_original_position=token.is_setext_heading
            )
        self.__have_seen_first_token = True

    def __handle_front_matter(self, token: MarkdownToken) -> None:
        front_token = cast(FrontMatterMarkdownToken, token)
        if self.__front_matter_title in front_token.matter_map:
            self.__have_seen_first_token = True

    def __handle_html_block_started(
        self, context: PluginScanContext, token: MarkdownToken
    ) -> None:
        assert token.is_text
        text_token = cast(TextMarkdownToken, token)
        html_block_contents = text_token.token_text.strip(" ")

        tag_name = re.split(r"[ \n\>]", html_block_contents)[0].lower()
        if tag_name in self.__html_tags_to_skip:
            self.__wait_for_html_end = True
            return

        if not html_block_contents.startswith(
            "<h1 "
        ) and not html_block_contents.startswith("<h1>"):
            assert self.__seen_html_block_start is not None
            self.report_next_token_error(context, self.__seen_html_block_start)
        self.__have_seen_first_token = True

    def next_token(self, context: PluginScanContext, token: MarkdownToken) -> None:
        """
        Event that a new token is being processed.
        """
        if self.__have_seen_first_token:
            return
        if self.__wait_for_html_end:
            if token.is_html_block_end:
                self.__wait_for_html_end = False
                self.__seen_html_block_start = None
            return
        if token.is_atx_heading or token.is_setext_heading:
            self.__handle_heading_start(context, token)
        elif token.is_front_matter and self.__front_matter_title:
            self.__handle_front_matter(token)
        elif token.is_html_block:
            self.__seen_html_block_start = token
        elif self.__seen_html_block_start:
            self.__handle_html_block_started(context, token)
        elif not token.is_blank_line and not token.is_end_of_stream:
            self.report_next_token_error(context, token)
            self.__have_seen_first_token = True
