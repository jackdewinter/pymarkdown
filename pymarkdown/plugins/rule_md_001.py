"""
Module to implement a plugin that looks for heading that increment more than one
level at a time (going up).
"""
from pymarkdown.markdown_token import AtxHeadingMarkdownToken, SetextHeadingMarkdownToken
from pymarkdown.plugin_manager import Plugin, PluginDetails


class RuleMd001(Plugin):
    """
    Class to implement a plugin that looks for headings that increment more than one
    level at a time (going up).
    """

    def __init__(self):
        super().__init__()
        self.__last_heading_count = None

    def get_details(self):
        """
        Get the details for the plugin.
        """
        return PluginDetails(
            # headings, headers
            plugin_name="heading-increment,header-increment",
            plugin_id="MD001",
            plugin_enabled_by_default=True,
            plugin_description="Heading levels should only increment by one level at a time",
        )  # https://github.com/DavidAnson/markdownlint/blob/master/doc/Rules.md#md001---heading-levels-should-only-increment-by-one-level-at-a-time

    def starting_new_file(self):
        """
        Event that the a new file to be scanned is starting.
        """
        self.__last_heading_count = None

    def next_token(self, token):
        """
        Event that a new token is being processed.
        """
        hash_count = None
        if isinstance(token, AtxHeadingMarkdownToken):
            hash_count = token.hash_count
        elif isinstance(token, SetextHeadingMarkdownToken):
            hash_count = token.hash_count
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
                        token, extra_error_information=extra_data
                    )
            self.__last_heading_count = hash_count
