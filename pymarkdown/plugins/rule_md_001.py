"""
Module to implement a plugin that looks for hard tabs in the files.
"""
from pymarkdown.markdown_token import AtxHeaderMarkdownToken, SetextHeaderMarkdownToken
from pymarkdown.plugin_manager import Plugin, PluginDetails


class RuleMd001(Plugin):
    """
    Class to implement a plugin that looks for hard tabs in the files.
    """

    def __init__(self):
        super().__init__()
        self.last_header_count = None

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
        self.last_header_count = None

    def next_token(self, token):
        """
        Event that a new token is being processed.
        """
        hash_count = None
        if isinstance(token, AtxHeaderMarkdownToken):
            hash_count = token.hash_count
        elif isinstance(token, SetextHeaderMarkdownToken):
            if token.header_character == "=":
                hash_count = 1
            else:
                assert token.header_character == "-"
                hash_count = 2
        if hash_count:
            if self.last_header_count and (hash_count > self.last_header_count):
                delta = hash_count - self.last_header_count
                if delta > 1:
                    extra_data = (
                        "Expected: h"
                        + str(self.last_header_count + 1)
                        + "; Actual: h"
                        + str(hash_count)
                    )
                    self.report_next_token_error(
                        token, extra_error_information=extra_data
                    )
            self.last_header_count = hash_count

    def completed_file(self):
        """
        Event that the file being currently scanned is now completed.
        """
