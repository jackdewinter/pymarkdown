"""
Module to implement a plugin that looks to see if the first heading in a file is
a top level heading.
"""
from pymarkdown.markdown_token import AtxHeaderMarkdownToken, SetextHeaderMarkdownToken
from pymarkdown.plugin_manager import Plugin, PluginDetails


class RuleMd002(Plugin):
    """
    Class to implement a plugin that looks to see if the first heading in a file is
    a top level heading.
    """

    def __init__(self):
        super().__init__()
        self.__start_level = None
        self.__have_seen_first_header = None

    def get_details(self):
        """
        Get the details for the plugin.
        """
        return PluginDetails(
            # headings, headers
            plugin_name="first-heading-h1,first-header-h1",
            plugin_id="MD002",
            plugin_enabled_by_default=False,
            plugin_description="First heading should be a top level heading",
        )  # https://github.com/DavidAnson/markdownlint/blob/master/doc/Rules.md#md002---first-heading-should-be-a-top-level-heading
        # Parameters: level (number; default 1)

    def initialize_from_config(self):
        """
        Event to allow the plugin to load configuration information.
        """
        self.__start_level = self.get_configuration_value("level", default_value=1)

    def starting_new_file(self):
        """
        Event that the a new file to be scanned is starting.
        """
        self.__have_seen_first_header = False

    def next_token(self, token):
        """
        Event that a new token is being processed.
        """
        hash_count = None
        if isinstance(token, AtxHeaderMarkdownToken):
            hash_count = token.hash_count
        elif isinstance(token, SetextHeaderMarkdownToken):
            hash_count = token.hash_count
        if not self.__have_seen_first_header and hash_count:
            self.__have_seen_first_header = True
            if hash_count != self.__start_level:
                extra_data = (
                    "Expected: h"
                    + str(self.__start_level)
                    + "; Actual: h"
                    + str(hash_count)
                )
                self.report_next_token_error(token, extra_error_information=extra_data)
