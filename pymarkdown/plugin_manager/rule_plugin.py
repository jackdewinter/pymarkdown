"""
Module to provide structure to scan through a file.
"""

from abc import ABC, abstractmethod
from typing import List, Optional, Union, cast

from application_properties import ApplicationPropertiesFacade

from pymarkdown.my_application_properties_facade import MyApplicationPropertiesFacade
from pymarkdown.plugin_manager.plugin_details import (
    PluginDetails,
    PluginDetailsV2,
    QueryConfigItem,
)
from pymarkdown.plugin_manager.plugin_scan_context import PluginScanContext
from pymarkdown.tokens.markdown_token import MarkdownToken
from pymarkdown.tokens.setext_heading_markdown_token import SetextHeadingMarkdownToken


class RulePlugin(ABC):
    """
    Class to provide structure to scan through a file.
    Based off of concepts from
    https://github.com/hiddenillusion/example-code/commit/3e2daada652fe9b487574c784e0924bd5fcfe667
    """

    def __init__(self) -> None:
        (
            self.__is_next_token_implemented_in_plugin,
            self.__is_next_line_implemented_in_plugin,
            self.__is_starting_new_file_implemented_in_plugin,
            self.__is_completed_file_implemented_in_plugin,
            self.__is_query_config_implemented_in_plugin,
        ) = (True, True, True, True, False)
        self.__plugin_specific_facade: Optional[MyApplicationPropertiesFacade] = None

    @abstractmethod
    def get_details(self) -> PluginDetails:
        """
        Get the details for the plugin.
        """

    @property
    def plugin_configuration(self) -> MyApplicationPropertiesFacade:
        """
        Get the configuration facade associated with this plugin.
        """
        assert self.__plugin_specific_facade
        return self.__plugin_specific_facade

    def set_configuration_map(
        self, plugin_specific_facade: ApplicationPropertiesFacade
    ) -> None:
        """
        Set the configuration map with values for the plugin.
        """
        self.__plugin_specific_facade = MyApplicationPropertiesFacade(
            plugin_specific_facade
        )

        self.__is_query_config_implemented_in_plugin = (
            "query_config" in self.__class__.__dict__
        )
        self.__is_next_token_implemented_in_plugin = (
            "next_token" in self.__class__.__dict__
        )
        self.__is_next_line_implemented_in_plugin = (
            "next_line" in self.__class__.__dict__
        )
        self.__is_starting_new_file_implemented_in_plugin = (
            "starting_new_file" in self.__class__.__dict__
        )
        self.__is_completed_file_implemented_in_plugin = (
            "completed_file" in self.__class__.__dict__
        )

    @property
    def is_query_config_implemented_in_plugin(self) -> bool:
        """
        Return whether the query_config function is implemented in the plugin.
        """
        return self.__is_query_config_implemented_in_plugin

    @property
    def is_starting_new_file_implemented_in_plugin(self) -> bool:
        """
        Return whether the starting_new_file function is implemented in the plugin.
        """
        return self.__is_starting_new_file_implemented_in_plugin

    @property
    def is_next_line_implemented_in_plugin(self) -> bool:
        """
        Return whether the next_line function is implemented in the plugin.
        """
        return self.__is_next_line_implemented_in_plugin

    @property
    def is_next_token_implemented_in_plugin(self) -> bool:
        """
        Return whether the next_token function is implemented in the plugin.
        """
        return self.__is_next_token_implemented_in_plugin

    @property
    def is_completed_file_implemented_in_plugin(self) -> bool:
        """
        Return whether the completed_file function is implemented in the plugin.
        """
        return self.__is_completed_file_implemented_in_plugin

    # pylint: disable=too-many-arguments
    def register_fix_token_request(
        self,
        context: PluginScanContext,
        token: MarkdownToken,
        plugin_action: str,
        field_name: str,
        field_value: Union[str, int],
    ) -> None:
        """
        Register a request to fix a token.
        """
        context.register_fix_token_request(
            token, self.get_details().plugin_id, plugin_action, field_name, field_value
        )

    def register_replace_tokens_request(
        self,
        context: PluginScanContext,
        start_token: MarkdownToken,
        end_token: MarkdownToken,
        replacement_tokens: List[MarkdownToken],
    ) -> None:
        """
        Register a request to replace a sequence of tokens.
        """
        context.register_replace_tokens_request(
            self.get_details().plugin_id, start_token, end_token, replacement_tokens
        )

    # pylint: enable=too-many-arguments

    def report_next_line_error(
        self,
        context: PluginScanContext,
        column_number: int,
        line_number_delta: int = 0,
        extra_error_information: Optional[str] = None,
    ) -> None:
        """
        Report an error with the current line being processed.
        """
        does_support_fix = False
        plugin_details = self.get_details()
        if isinstance(plugin_details, PluginDetailsV2):
            does_support_fix = plugin_details.plugin_supports_fix

        context.add_triggered_rule(
            context.scan_file,
            context.line_number + line_number_delta,
            column_number,
            plugin_details.plugin_id,
            plugin_details.plugin_name,
            plugin_details.plugin_description,
            extra_error_information,
            does_support_fix,
        )

    # pylint: disable=too-many-arguments
    def report_next_token_error(
        self,
        context: PluginScanContext,
        token: MarkdownToken,
        extra_error_information: Optional[str] = None,
        line_number_delta: int = 0,
        column_number_delta: int = 0,
        use_original_position: bool = False,
    ) -> None:
        """
        Report an error with the current token being processed.
        """
        if use_original_position:
            leaf_token = cast(SetextHeadingMarkdownToken, token)
            line_number = leaf_token.original_line_number
            column_number = leaf_token.original_column_number
        else:
            line_number = token.line_number
            column_number = token.column_number

        does_support_fix = False
        plugin_details = self.get_details()
        # if isinstance(xx, PluginDetailsV2):
        #     xy = cast(PluginDetailsV2, xx)
        #     does_support_fix = xy.plugin_supports_fix

        context.add_triggered_rule(
            context.scan_file,
            line_number + line_number_delta,
            (
                column_number + column_number_delta
                if column_number_delta >= 0
                else -column_number_delta
            ),
            plugin_details.plugin_id,
            plugin_details.plugin_name,
            plugin_details.plugin_description,
            extra_error_information,
            does_support_fix,
        )

    # pylint: enable=too-many-arguments

    def initialize_from_config(self) -> None:  # noqa: B027
        """
        Event to allow the plugin to load configuration information.
        """

    def query_config(self) -> List[QueryConfigItem]:  # noqa: B027
        """
        Query to find out the configuration that the rule is using.
        """
        return []  # pragma: no cover

    def starting_new_file(self) -> None:  # noqa: B027
        """
        Event that the a new file to be scanned is starting.
        """

    def completed_file(self, context: PluginScanContext) -> None:  # noqa: B027
        """
        Event that the file being currently scanned is now completed.
        """

    def next_line(self, context: PluginScanContext, line: str) -> None:  # noqa: B027
        """
        Event that a new line is being processed.
        """

    def next_token(  # noqa: B027
        self, context: PluginScanContext, token: MarkdownToken
    ) -> None:
        """
        Event that a new token is being processed.
        """
