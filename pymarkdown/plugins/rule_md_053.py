"""
Module to implement a plugin that ensures that any provided LRDs are required.
"""

from typing import List, Set, cast

from pymarkdown.general.parser_helper import ParserHelper
from pymarkdown.links.link_parse_helper import LinkParseHelper
from pymarkdown.plugin_manager.plugin_details import (
    PluginDetailsV2,
    PluginDetailsV3,
    QueryConfigItem,
)
from pymarkdown.plugin_manager.plugin_scan_context import PluginScanContext
from pymarkdown.plugin_manager.rule_plugin import RulePlugin
from pymarkdown.tokens.image_start_markdown_token import ImageStartMarkdownToken
from pymarkdown.tokens.link_reference_definition_markdown_token import (
    LinkReferenceDefinitionMarkdownToken,
)
from pymarkdown.tokens.link_start_markdown_token import LinkStartMarkdownToken
from pymarkdown.tokens.markdown_token import MarkdownToken


class RuleMd053(RulePlugin):
    """
    Class to implement a plugin that ensures that any provided LRDs are required.
    """

    def __init__(self) -> None:
        """
        Initialize an instance of the RuleMd048 class.
        """
        super().__init__()
        self.__ignored_definitions: List[str] = []
        self.__lrd_tokens: List[LinkReferenceDefinitionMarkdownToken] = []
        self.__link_tokens: List[LinkStartMarkdownToken] = []
        self.__image_tokens: List[ImageStartMarkdownToken] = []

    def get_details(self) -> PluginDetailsV2:
        """
        Get the details for the plugin.
        """
        return PluginDetailsV3(
            plugin_name="link-image-reference-definitions",
            plugin_id="MD053",
            plugin_enabled_by_default=True,
            plugin_description="Link and image reference definitions should be needed.",
            plugin_version="0.5.0",
            plugin_url="https://pymarkdown.readthedocs.io/en/latest/plugins/rule_md053.md",
            plugin_configuration="ignored-definitions",
        )

    def initialize_from_config(self) -> None:
        """
        Event to allow the plugin to load configuration information.
        """
        ignored_definitions_source = (
            self.plugin_configuration.get_string_property_with_default(
                "ignored-definitions", "//"
            )
        )
        self.__ignored_definitions = []
        for next_phrase in ignored_definitions_source.split(","):
            if next_phrase := LinkParseHelper.normalize_link_label(next_phrase):
                self.__ignored_definitions.append(next_phrase)

    def query_config(self) -> List[QueryConfigItem]:
        """
        Query to find out the configuration that the rule is using.
        """
        return [
            QueryConfigItem("ignored-definitions", str(self.__ignored_definitions)),
        ]

    def starting_new_file(self) -> None:
        """
        Event that the a new file to be scanned is starting.
        """
        self.__lrd_tokens = []
        self.__link_tokens = []
        self.__image_tokens = []

    def completed_file(self, context: PluginScanContext) -> None:
        """
        Event that the file being currently scanned is now completed.
        """
        link_text_set: Set[str] = set()
        for next_link_token in self.__link_tokens:
            if next_link_token.label_type == "full":
                assert next_link_token.ex_label is not None
                link_text = LinkParseHelper.normalize_link_label(
                    next_link_token.ex_label
                )
            else:
                assert next_link_token.text_from_blocks is not None
                original_text_from_blocks = ParserHelper.remove_all_from_text(
                    next_link_token.text_from_blocks
                )
                link_text = LinkParseHelper.normalize_link_label(
                    original_text_from_blocks
                )
            link_text_set.add(link_text)
        for next_image_token in self.__image_tokens:
            if next_image_token.label_type == "full":
                assert next_image_token.ex_label is not None
                image_text = LinkParseHelper.normalize_link_label(
                    next_image_token.ex_label
                )
            else:
                assert next_image_token.text_from_blocks is not None
                original_text_from_blocks = ParserHelper.remove_all_from_text(
                    next_image_token.text_from_blocks
                )
                image_text = LinkParseHelper.normalize_link_label(
                    original_text_from_blocks
                )
            link_text_set.add(image_text)

        lrd_link_texts: Set[str] = set()
        for next_lrd_token in self.__lrd_tokens:
            lrd_text = LinkParseHelper.normalize_link_label(next_lrd_token.link_name)
            if (
                lrd_text not in link_text_set or lrd_text in lrd_link_texts
            ) and lrd_text not in self.__ignored_definitions:
                self.report_next_token_error(
                    context, next_lrd_token, extra_error_information=None
                )
            lrd_link_texts.add(lrd_text)

    def next_token(self, context: PluginScanContext, token: MarkdownToken) -> None:
        """
        Event that a new token is being processed.
        """
        if token.is_inline_link:
            link_token = cast(LinkStartMarkdownToken, token)
            if link_token.label_type != "inline":
                self.__link_tokens.append(link_token)
        elif token.is_inline_image:
            image_token = cast(ImageStartMarkdownToken, token)
            if image_token.label_type != "inline":
                self.__image_tokens.append(image_token)
        elif token.is_link_reference_definition:
            lrd_token = cast(LinkReferenceDefinitionMarkdownToken, token)
            self.__lrd_tokens.append(lrd_token)
