"""
Module to provide structure to scan through a file.
"""

from abc import ABC, abstractmethod
from typing import Optional, cast

from application_properties import ApplicationPropertiesFacade

from pymarkdown.leaf_markdown_token import SetextHeadingMarkdownToken
from pymarkdown.markdown_token import MarkdownToken
from pymarkdown.plugin_manager.plugin_details import PluginDetails
from pymarkdown.plugin_manager.plugin_scan_context import PluginScanContext


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
        ) = (True, True, True, True)
        self.__plugin_specific_facade: Optional[ApplicationPropertiesFacade] = None

    @abstractmethod
    def get_details(self) -> PluginDetails:
        """
        Get the details for the plugin.
        """

    @property
    def plugin_configuration(self) -> ApplicationPropertiesFacade:
        """
        Get the configuration facade associated with this plugin.
        """
        assert self.__plugin_specific_facade
        return self.__plugin_specific_facade

    def set_configuration_map(
        self, plugin_specific_facade: ApplicationPropertiesFacade
    ):
        """
        Set the configuration map with values for the plugin.
        """
        self.__plugin_specific_facade = plugin_specific_facade

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

    def report_next_line_error(
        self,
        context: PluginScanContext,
        column_number: int,
        line_number_delta=0,
        extra_error_information: Optional[str] = None,
    ) -> None:
        """
        Report an error with the current line being processed.
        """
        context.add_triggered_rule(
            context.scan_file,
            context.line_number + line_number_delta,
            column_number,
            self.get_details().plugin_id,
            self.get_details().plugin_name,
            self.get_details().plugin_description,
            extra_error_information,
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
    ):
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

        context.add_triggered_rule(
            context.scan_file,
            line_number + line_number_delta,
            column_number + column_number_delta
            if column_number_delta >= 0
            else -column_number_delta,
            self.get_details().plugin_id,
            self.get_details().plugin_name,
            self.get_details().plugin_description,
            extra_error_information,
        )

    # pylint: enable=too-many-arguments

    def initialize_from_config(self) -> None:
        """
        Event to allow the plugin to load configuration information.
        """

    def starting_new_file(self) -> None:
        """
        Event that the a new file to be scanned is starting.
        """

    def completed_file(self, context: PluginScanContext) -> None:
        """
        Event that the file being currently scanned is now completed.
        """

    def next_line(self, context: PluginScanContext, line: str) -> None:
        """
        Event that a new line is being processed.
        """

    def next_token(self, context: PluginScanContext, token: MarkdownToken) -> None:
        """
        Event that a new token is being processed.
        """
