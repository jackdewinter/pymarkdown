"""
Module to implement a plugin that validates uris fo links and images.
"""
import os.path
import re
from typing import cast
from pymarkdown.tokens.reference_markdown_token import ReferenceMarkdownToken

from pymarkdown.tokens.markdown_token import MarkdownToken
from pymarkdown.plugin_manager.plugin_details import PluginDetails
from pymarkdown.plugin_manager.plugin_scan_context import PluginScanContext
from pymarkdown.plugin_manager.rule_plugin import RulePlugin


class RuleMd049(RulePlugin):
    """
    Class to implement a plugin that looks for link and images elements that have a invalid uri.
    """

    EXTERNAL_LINK_REGEX = re.compile("^(.+):.*$")

    def get_details(self) -> PluginDetails:
        """
        Get the details for the plugin.
        """
        return PluginDetails(
            plugin_name="validate-refs",
            plugin_id="MD049",
            plugin_enabled_by_default=False,
            plugin_description="Local URIs should be valid",
            plugin_version="0.0.1",
            plugin_interface_version=1,
            plugin_url="https://github.com/jackdewinter/pymarkdown/blob/main/docs/rules/rule_md049.md",
        )

    def next_token(self, context: PluginScanContext, token: MarkdownToken) -> None:
        """
        Event that a new token is being processed.
        """
        if not token.is_inline_image and not token.is_inline_link:
            return
        link_uri, _ = self._extract_link_uri(token)
        if not link_uri or self.EXTERNAL_LINK_REGEX.match(link_uri):
            return
        link_path = self._resolve_to_absolute_path(context, link_uri)
        if not os.path.exists(link_path):
            self.report_next_token_error(context, token)

    def _resolve_to_absolute_path(self, context, link_uri: str):
        if link_uri.startswith("/"):
            return os.path.join(os.getcwd(), link_uri[1:])

        return os.path.join(os.path.dirname(context.scan_file), link_uri)

    def _extract_link_uri(self, token: MarkdownToken):
        ref_token = cast(ReferenceMarkdownToken, token)
        link_uri_split = ref_token.link_uri.split("#", 1)
        if len(link_uri_split) == 2:
            return link_uri_split

        return link_uri_split[0], None
