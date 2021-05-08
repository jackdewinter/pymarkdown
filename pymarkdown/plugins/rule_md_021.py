"""
Module to implement a plugin that looks for more than one space between either the
opening or closing hashes of an atx heading.
"""
from pymarkdown.plugin_manager import Plugin, PluginDetails


class RuleMd021(Plugin):
    """
    Class to implement a plugin that looks for more than one space between either the
    opening or closing hashes of an atx heading.
    """

    def __init__(self):
        super().__init__()
        self.__atx_heading_token = None
        self.__is_left_in_error = None

    def get_details(self):
        """
        Get the details for the plugin.
        """
        return PluginDetails(
            plugin_name="no-multiple-space-closed-atx",
            plugin_id="MD021",
            plugin_enabled_by_default=True,
            plugin_description="Multiple spaces are present inside hash characters on Atx Closed Heading.",
            plugin_version="0.5.0",
            plugin_interface_version=1,
        )

    def starting_new_file(self):
        """
        Event that the a new file to be scanned is starting.
        """
        self.__atx_heading_token = None
        self.__is_left_in_error = False

    def next_token(self, context, token):
        """
        Event that a new token is being processed.
        """
        if token.is_atx_heading:
            if token.remove_trailing_count:
                self.__atx_heading_token = token
            self.__is_left_in_error = False
        elif token.is_paragraph_end:
            self.__atx_heading_token = None
        elif token.is_atx_heading_end:
            if self.__is_left_in_error or len(token.extra_end_data) > 1:
                self.report_next_token_error(context, self.__atx_heading_token)
        elif token.is_text:
            if self.__atx_heading_token and len(token.extracted_whitespace) > 1:
                self.__is_left_in_error = True
