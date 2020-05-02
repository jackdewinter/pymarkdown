"""
Module to implement a plugin that looks for multiple header lines with the same
content.
"""
from pymarkdown.markdown_token import (
    AtxHeaderMarkdownToken,
    EndMarkdownToken,
    MarkdownToken,
    SetextHeaderMarkdownToken,
)
from pymarkdown.plugin_manager import Plugin, PluginDetails


class RuleMd024(Plugin):
    """
    Class to implement a plugin that looks for multiple header lines with the same
    content.
    """

    def __init__(self):
        super().__init__()
        self.__header_text = None
        self.__start_token = None
        self.__hash_count = None
        self.__last_hash_count = None
        self.__siblings_only = None
        self.__header_content_map = None

    def get_details(self):
        """
        Get the details for the plugin.
        """
        return PluginDetails(
            # headings, headers
            plugin_name="no-duplicate-heading,no-duplicate-header",
            plugin_id="MD024",
            plugin_enabled_by_default=True,
            plugin_description="Multiple headings with the same content",
        )  # https://github.com/DavidAnson/markdownlint/blob/master/doc/Rules.md#md024---multiple-headings-with-the-same-content
        # Parameters: siblings_only, allow_different_nesting (boolean; default false)

    def initialize_from_config(self):
        """
        Event to allow the plugin to load configuration information.
        """
        self.__siblings_only = self.get_configuration_value(
            "siblings_only", default_value=False
        ) or self.get_configuration_value(
            "allow_different_nesting", default_value=False
        )

    def starting_new_file(self):
        """
        Event that the a new file to be scanned is starting.
        """
        self.__header_text = None
        self.__start_token = None
        self.__hash_count = None
        self.__last_hash_count = None
        if self.__siblings_only:
            self.__header_content_map = [{}, {}, {}, {}, {}, {}]
        else:
            self.__header_content_map = [{}]

    def next_token(self, token):
        """
        Event that a new token is being processed.
        """
        skip_this_token = False
        if isinstance(token, (AtxHeaderMarkdownToken, SetextHeaderMarkdownToken)):
            self.handle_header_start(token)
            skip_this_token = True
        elif isinstance(token, EndMarkdownToken):
            if token.type_name in (
                MarkdownToken.token_atx_header,
                MarkdownToken.token_setext_header,
            ):
                self.handler_header_end()

        if not skip_this_token and self.__header_text is not None:
            self.__header_text += str(token)

    def handle_header_start(self, token):
        """
        Process the start header token, atx or setext
        """

        self.__header_text = ""
        self.__start_token = token
        if self.__siblings_only:
            self.__hash_count = token.hash_count
        else:
            self.__hash_count = 1

    def handler_header_end(self):
        """
        Process the end header token, atx or setext
        """

        if self.__last_hash_count:
            while self.__last_hash_count < self.__hash_count:
                self.__last_hash_count += 1
                self.__header_content_map[self.__last_hash_count - 1] = {}
            while self.__last_hash_count > self.__hash_count:
                self.__header_content_map[self.__last_hash_count - 1] = {}
                self.__last_hash_count -= 1

        past_headers_map = self.__header_content_map[self.__hash_count - 1]

        if self.__header_text in past_headers_map:
            self.report_next_token_error(self.__start_token)
        else:
            past_headers_map[self.__header_text] = self.__header_text
        self.__header_text = None
        self.__last_hash_count = self.__hash_count
