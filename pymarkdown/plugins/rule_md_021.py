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
        self.__in_atx_heading = None
        self.__is_left_in_error = None

    def get_details(self):
        """
        Get the details for the plugin.
        """
        return PluginDetails(
            # headings, headers, atx_closed, spaces
            plugin_name="no-multiple-space-closed-atx",
            plugin_id="MD021",
            plugin_enabled_by_default=True,
            plugin_description="Multiple spaces inside hashes on closed atx style heading",
        )  # https://github.com/DavidAnson/markdownlint/blob/master/doc/Rules.md#md021---multiple-spaces-inside-hashes-on-closed-atx-style-heading

    def starting_new_file(self):
        """
        Event that the a new file to be scanned is starting.
        """
        self.__in_atx_heading = None
        self.__is_left_in_error = False

    def next_token(self, context, token):
        """
        Event that a new token is being processed.
        """
        if token.is_atx_heading:
            self.__in_atx_heading = token.remove_trailing_count
            self.__is_left_in_error = False
        elif token.is_paragraph_end:
            self.__in_atx_heading = False
        elif token.is_atx_heading_end:
            if self.__is_left_in_error or len(token.extra_end_data) > 1:
                self.report_next_token_error(context, token)
        elif token.is_text:
            if self.__in_atx_heading and len(token.extracted_whitespace) > 1:
                self.__is_left_in_error = True
