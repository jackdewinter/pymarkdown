"""
Module to implement a plugin that prevents different forms of links and images from being used.
"""

from typing import List, Optional, cast

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


class RuleMd054(RulePlugin):
    """
    Class to implement a plugin that prevents different forms of links and images from being used.
    """

    def __init__(self) -> None:
        """
        Initialize an instance of the RuleMd048 class.
        """
        super().__init__()
        self.__allow_autolinks = False
        self.__allow_inline_links = False
        self.__allow_full_links = False
        self.__allow_collapsed_links = False
        self.__allow_shortcut_links = False
        self.__allow_inline_urls = False

    def get_details(self) -> PluginDetailsV2:
        """
        Get the details for the plugin.
        """
        return PluginDetailsV3(
            plugin_name="link-image-style",
            plugin_id="MD054",
            plugin_enabled_by_default=True,
            plugin_description="Link and image style.",
            plugin_version="0.5.0",
            plugin_url="https://pymarkdown.readthedocs.io/en/latest/plugins/rule_md054.md",
            plugin_configuration="autolinks,inline-links,full-links,collapsed-links,shortcut-links,inline-urls",
        )

    def initialize_from_config(self) -> None:
        """
        Event to allow the plugin to load configuration information.
        """
        self.__allow_autolinks = (
            self.plugin_configuration.get_boolean_property_with_default(
                "autolinks", True
            )
        )
        self.__allow_inline_links = (
            self.plugin_configuration.get_boolean_property_with_default(
                "inline-links", True
            )
        )
        self.__allow_full_links = (
            self.plugin_configuration.get_boolean_property_with_default(
                "full-links", True
            )
        )
        self.__allow_collapsed_links = (
            self.plugin_configuration.get_boolean_property_with_default(
                "collapsed-links", True
            )
        )
        self.__allow_shortcut_links = (
            self.plugin_configuration.get_boolean_property_with_default(
                "shortcut-links", True
            )
        )
        self.__allow_inline_urls = (
            self.plugin_configuration.get_boolean_property_with_default(
                "inline-urls", True
            )
        )

    def query_config(self) -> List[QueryConfigItem]:
        """
        Query to find out the configuration that the rule is using.
        """
        return [
            QueryConfigItem("autolinks", self.__allow_autolinks),
            QueryConfigItem("inline-links", self.__allow_inline_links),
            QueryConfigItem("full-links", self.__allow_full_links),
            QueryConfigItem("collapsed-links", self.__allow_collapsed_links),
            QueryConfigItem("shortcut-links", self.__allow_shortcut_links),
            QueryConfigItem("inline-urls", self.__allow_inline_urls),
        ]

    # pylint: disable=too-many-arguments
    def __process_by_label_type(
        self,
        context: PluginScanContext,
        token: MarkdownToken,
        label_type: str,
        link_uri: str,
        text_from_blocks: str,
        link_title: Optional[str],
    ) -> None:
        if label_type == "inline":
            is_allowed = self.__allow_inline_links
            if not self.__allow_inline_urls and (
                link_uri and not link_title and link_uri == text_from_blocks
            ):
                self.report_next_token_error(
                    context,
                    token,
                    extra_error_information="Disallowed Type: Inline Url",
                )
                return
        elif label_type == "full":
            is_allowed = self.__allow_full_links
        elif label_type == "collapsed":
            is_allowed = self.__allow_collapsed_links
        else:
            assert label_type == "shortcut"
            is_allowed = self.__allow_shortcut_links

        if not is_allowed:
            self.report_next_token_error(
                context,
                token,
                extra_error_information=f"Disallowed Type: {label_type.capitalize()}",
            )

    # pylint: enable=too-many-arguments

    def next_token(self, context: PluginScanContext, token: MarkdownToken) -> None:
        """
        Event that a new token is being processed.
        """
        if token.is_inline_autolink or token.is_inline_email_autolink:
            if not self.__allow_autolinks:
                self.report_next_token_error(
                    context, token, extra_error_information="Disallowed Type: Autolink"
                )
        elif token.is_inline_link:
            link_token = cast(LinkStartMarkdownToken, token)
            self.__process_by_label_type(
                context,
                token,
                link_token.label_type,
                link_token.link_uri,
                link_token.text_from_blocks,
                link_token.link_title,
            )
        elif token.is_inline_image:
            image_token = cast(ImageStartMarkdownToken, token)
            self.__process_by_label_type(
                context,
                token,
                image_token.label_type,
                image_token.link_uri,
                image_token.text_from_blocks,
                image_token.link_title,
            )
