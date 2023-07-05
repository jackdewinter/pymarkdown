"""
Module to implement a plugin that looks for unused assets.
"""
import os
import re
from pathlib import Path
from typing import Callable, Pattern, Set, cast

from pymarkdown.inline_markdown_token import ReferenceMarkdownToken
from pymarkdown.markdown_token import MarkdownToken
from pymarkdown.plugin_manager.plugin_details import PluginDetails
from pymarkdown.plugin_manager.plugin_scan_context import PluginScanContext
from pymarkdown.plugin_manager.plugin_scan_failure import PluginScanFailure
from pymarkdown.plugin_manager.rule_plugin import RulePlugin


class RuleMd051(RulePlugin):
    """
    Class to implement a plugin that looks for unused assets.
    """
    ASSET_DEFAULT_REGEX = r".*\.(jpg|jpeg|png|gif)$"

    def __init__(self) -> None:
        super().__init__()
        self.__used_assets: Set[str] = set()
        self.__assets_glob: str = ""
        self.__assets_regex: Pattern[str] = re.compile(self.ASSET_DEFAULT_REGEX)

    def get_details(self) -> PluginDetails:
        """
        Get the details for the plugin.
        """
        return PluginDetails(
            plugin_name="unused-assets",
            plugin_id="MD051",
            plugin_enabled_by_default=True,
            plugin_description="Unused assets found.",
            plugin_version="0.5.0",
            plugin_interface_version=1,
            plugin_url="https://github.com/jackdewinter/pymarkdown/blob/main/docs/rules/rule_md051.md",
            plugin_configuration="assetsglob,assetsregex",
        )

    def initialize_from_config(self) -> None:
        """
        Event to allow the plugin to load configuration information.
        """
        self.__assets_glob = self.plugin_configuration.get_string_property(
            "assetsglob", default_value="**/assets/**/*"
        )
        self.__assets_regex = re.compile(
            self.plugin_configuration.get_string_property(
                "assetsregex", default_value=self.ASSET_DEFAULT_REGEX
            )
        )

    EXTERNAL_LINK_RE = re.compile("^(.+):.*$")

    def next_token(self, context: PluginScanContext, token: MarkdownToken) -> None:
        """
        Event that a new token is being processed.
        """
        if not token.is_inline_image and not token.is_inline_link:
            # Not a reference so nothing to do here
            return

        link_uri = self._extract_link_uri(token)
        if self.EXTERNAL_LINK_RE.match(link_uri):
            # External link so nothing to do here
            return

        filesystem_path = self._resolve_to_filesystem_path(context, link_uri)

        # Check that referenced file exists
        if os.path.exists(filesystem_path):
            self.__used_assets.add(os.path.relpath(filesystem_path))

    def completed_all_files(
        self, log_scan_failure: Callable[[PluginScanFailure], None]
    ) -> None:
        all_assets = set(
            x
            for x in Path(".").glob(self.__assets_glob)
            if self.__assets_regex.match(str(x))
        )
        unused_assets = all_assets - set(Path(x) for x in self.__used_assets)
        for unused_asset in unused_assets:
            log_scan_failure(
                PluginScanFailure(
                    str(unused_asset),
                    0,
                    0,
                    self.get_details().plugin_id,
                    self.get_details().plugin_name,
                    self.get_details().plugin_description,
                    None,
                )
            )

    @staticmethod
    def _resolve_to_filesystem_path(context: PluginScanContext, link_uri: str) -> str:
        if not link_uri:
            path = context.scan_file
        elif link_uri.startswith("/"):
            path = link_uri[1:]
        else:
            path = os.path.join(os.path.dirname(context.scan_file), link_uri)
        return os.path.realpath(path)

    @staticmethod
    def _extract_link_uri(token: MarkdownToken) -> str:
        ref_token = cast(ReferenceMarkdownToken, token)
        return ref_token.link_uri.split("#", 1)[0]
