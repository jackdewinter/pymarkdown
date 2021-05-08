"""
Module to implement a plugin that looks to see if the first heading in a file is
a top level heading.
"""
from pymarkdown.plugin_manager import Plugin, PluginDetails


class RuleMd002(Plugin):
    """
    Class to implement a plugin that looks to see if the first heading in a file is
    a top level heading.
    """

    def __init__(self):
        super().__init__()
        self.__start_level = None
        self.__have_seen_first_heading = None
        self.__front_matter_title = None

    def get_details(self):
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
        )

    def initialize_from_config(self):
        """
        Event to allow the plugin to load configuration information.
        """
        self.__start_level = self.plugin_configuration.get_integer_property(
            "level", default_value=1
        )

    def starting_new_file(self):
        """
        Event that the a new file to be scanned is starting.
        """
        self.__have_seen_first_heading = False

    def next_token(self, context, token):
        """
        Event that a new token is being processed.
        """
        hash_count = None
        if token.is_atx_heading or token.is_setext_heading:
            hash_count = token.hash_count

        if not self.__have_seen_first_heading and hash_count:
            self.__have_seen_first_heading = True
            if hash_count != self.__start_level:
                extra_data = (
                    "Expected: h"
                    + str(self.__start_level)
                    + "; Actual: h"
                    + str(hash_count)
                )
                self.report_next_token_error(
                    context, token, extra_error_information=extra_data
                )
