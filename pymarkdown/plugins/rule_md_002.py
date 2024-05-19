"""
Module to implement a plugin that looks to see if the first heading in a file is
a top level heading.
"""

from typing import cast

from pymarkdown.plugin_manager.plugin_details import PluginDetails
from pymarkdown.plugin_manager.plugin_scan_context import PluginScanContext
from pymarkdown.plugin_manager.rule_plugin import RulePlugin
from pymarkdown.tokens.atx_heading_markdown_token import AtxHeadingMarkdownToken
from pymarkdown.tokens.markdown_token import MarkdownToken


class RuleMd002(RulePlugin):
    """
    Class to implement a plugin that looks to see if the first heading in a file is
    a top level heading.
    """

    def __init__(self) -> None:
        super().__init__()
        self.__start_level = 0
        self.__have_seen_first_heading = False

    def get_details(self) -> PluginDetails:
        """
        Get the details for the plugin.
        """
        return PluginDetails(
            plugin_name="first-heading-h1,first-header-h1",
            plugin_id="MD002",
            plugin_enabled_by_default=False,
            plugin_description="First heading of the document should be a top level heading.",
            plugin_version="0.5.0",
            plugin_interface_version=1,
            plugin_url="https://pymarkdown.readthedocs.io/en/latest/plugins/rule_md002.md",
            plugin_configuration="level",
        )

    @classmethod
    def __validate_configuration_other_test_value(cls, found_value: int) -> None:
        if not 1 <= found_value <= 6:
            raise ValueError("Allowable values are between 1 and 6 (inclusive).")

    def initialize_from_config(self) -> None:
        """
        Event to allow the plugin to load configuration information.
        """
        self.__start_level = self.plugin_configuration.get_integer_property(
            "level",
            default_value=1,
            valid_value_fn=self.__validate_configuration_other_test_value,
        )

    def starting_new_file(self) -> None:
        """
        Event that the a new file to be scanned is starting.
        """
        self.__have_seen_first_heading = False

    def next_token(self, context: PluginScanContext, token: MarkdownToken) -> None:
        """
        Event that a new token is being processed.
        """
        if token.is_atx_heading or token.is_setext_heading:
            heading_token = cast(AtxHeadingMarkdownToken, token)
            hash_count = heading_token.hash_count
        else:
            hash_count = None

        if not self.__have_seen_first_heading and hash_count:
            self.__have_seen_first_heading = True
            if hash_count != self.__start_level:
                extra_data = f"Expected: h{self.__start_level}; Actual: h{hash_count}"
                self.report_next_token_error(
                    context, token, extra_error_information=extra_data
                )
