"""
Module to provide structure to scan through a file.
"""

from abc import ABC, abstractmethod


class RulePlugin(ABC):
    """
    Class to provide structure to scan through a file.
    Based off of concepts from https://github.com/hiddenillusion/example-code/commit/3e2daada652fe9b487574c784e0924bd5fcfe667
    """

    def __init__(self):
        (
            self.__plugin_specific_facade,
            self.__is_next_token_implemented_in_plugin,
            self.__is_next_line_implemented_in_plugin,
            self.__is_starting_new_file_implemented_in_plugin,
            self.__is_completed_file_implemented_in_plugin,
        ) = (None, True, True, True, True)

    @abstractmethod
    def get_details(self):
        """
        Get the details for the plugin.
        """

    @property
    def plugin_configuration(self):
        """
        Get the configuration facade associated with this plugin.
        """
        return self.__plugin_specific_facade

    def set_configuration_map(self, plugin_specific_facade):
        """
        Set the configuration map with values for the plugin.
        """
        self.__plugin_specific_facade = plugin_specific_facade

        self.__is_next_token_implemented_in_plugin = (
            "next_token" in self.__class__.__dict__.keys()
        )
        self.__is_next_line_implemented_in_plugin = (
            "next_line" in self.__class__.__dict__.keys()
        )
        self.__is_starting_new_file_implemented_in_plugin = (
            "starting_new_file" in self.__class__.__dict__.keys()
        )
        self.__is_completed_file_implemented_in_plugin = (
            "completed_file" in self.__class__.__dict__.keys()
        )

    @property
    def is_starting_new_file_implemented_in_plugin(self):
        """
        Return whether the starting_new_file function is implemented in the plugin.
        """
        return self.__is_starting_new_file_implemented_in_plugin

    @property
    def is_next_line_implemented_in_plugin(self):
        """
        Return whether the next_line function is implemented in the plugin.
        """
        return self.__is_next_line_implemented_in_plugin

    @property
    def is_next_token_implemented_in_plugin(self):
        """
        Return whether the next_token function is implemented in the plugin.
        """
        return self.__is_next_token_implemented_in_plugin

    @property
    def is_completed_file_implemented_in_plugin(self):
        """
        Return whether the completed_file function is implemented in the plugin.
        """
        return self.__is_completed_file_implemented_in_plugin

    def report_next_line_error(
        self, context, column_number, line_number_delta=0, extra_error_information=None
    ):
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
        context,
        token,
        extra_error_information=None,
        line_number_delta=0,
        column_number_delta=0,
        use_original_position=False,
    ):
        """
        Report an error with the current token being processed.
        """
        context.add_triggered_rule(
            context.scan_file,
            (token.original_line_number if use_original_position else token.line_number)
            + line_number_delta,
            (
                token.original_column_number
                if use_original_position
                else token.column_number
            )
            + column_number_delta
            if column_number_delta >= 0
            else -column_number_delta,
            self.get_details().plugin_id,
            self.get_details().plugin_name,
            self.get_details().plugin_description,
            extra_error_information,
        )

    # pylint: enable=too-many-arguments

    def initialize_from_config(self):
        """
        Event to allow the plugin to load configuration information.
        """

    def starting_new_file(self):
        """
        Event that the a new file to be scanned is starting.
        """

    def completed_file(self, context):
        """
        Event that the file being currently scanned is now completed.
        """

    def next_line(self, context, line):
        """
        Event that a new line is being processed.
        """

    def next_token(self, context, token):
        """
        Event that a new token is being processed.
        """
