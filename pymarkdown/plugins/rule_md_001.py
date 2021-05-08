"""
Module to implement a plugin that looks for heading that increment more than one
level at a time (going up).
"""
from pymarkdown.plugin_manager import Plugin, PluginDetails


class RuleMd001(Plugin):

    """
    Class to implement a plugin that looks for headings that increment more than one
    level at a time (going up).
    """

    def __init__(self):
        super().__init__()
        self.__last_heading_count = None
        self.__front_matter_title = None

    def get_details(self):
        """
        Get the details for the plugin.
        """
        return PluginDetails(
            plugin_name="heading-increment,header-increment",
            plugin_id="MD001",
            plugin_enabled_by_default=True,
            plugin_description="Heading levels should only increment by one level at a time.",
            plugin_version="0.5.0",
            plugin_interface_version=1,
        )

    def initialize_from_config(self):
        self.__front_matter_title = self.plugin_configuration.get_string_property(
            "front_matter_title", default_value="title"
        ).lower()

    def starting_new_file(self):
        """
        Event that the a new file to be scanned is starting.
        """
        self.__last_heading_count = None

    def next_token(self, context, token):
        """
        Event that a new token is being processed.
        """
        hash_count = None
        if token.is_atx_heading or token.is_setext_heading:
            hash_count = token.hash_count
        elif token.is_front_matter:
            if self.__front_matter_title in token.matter_map:
                hash_count = 1

        if hash_count:
            if self.__last_heading_count and (hash_count > self.__last_heading_count):
                delta = hash_count - self.__last_heading_count
                if delta > 1:
                    extra_data = (
                        "Expected: h"
                        + str(self.__last_heading_count + 1)
                        + "; Actual: h"
                        + str(hash_count)
                    )
                    self.report_next_token_error(
                        context, token, extra_error_information=extra_data
                    )
            self.__last_heading_count = hash_count
