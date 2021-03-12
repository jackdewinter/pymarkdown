"""
Module to implement a plugin that looks for multiple heading lines with the same
content.
"""
from pymarkdown.plugin_manager import Plugin, PluginDetails


class RuleMd024(Plugin):
    """
    Class to implement a plugin that looks for multiple heading lines with the same
    content.
    """

    def __init__(self):
        super().__init__()
        self.__heading_text = None
        self.__start_token = None
        self.__hash_count = None
        self.__last_hash_count = None
        self.__siblings_only = None
        self.__heading_content_map = None

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
        self.__siblings_only = self.plugin_configuration.get_boolean_property(
            "siblings_only", default_value=False
        ) or self.plugin_configuration.get_boolean_property(
            "allow_different_nesting", default_value=False
        )

    def starting_new_file(self):
        """
        Event that the a new file to be scanned is starting.
        """
        self.__heading_text = None
        self.__start_token = None
        self.__hash_count = None
        self.__last_hash_count = None
        if self.__siblings_only:
            self.__heading_content_map = [{}, {}, {}, {}, {}, {}]
        else:
            self.__heading_content_map = [{}]

    def next_token(self, context, token):
        """
        Event that a new token is being processed.
        """
        skip_this_token = False
        if token.is_setext_heading or token.is_atx_heading:
            self.handle_heading_start(token)
            skip_this_token = True
        elif token.is_setext_heading_end or token.is_atx_heading_end:
            self.handler_heading_end(context)

        if not skip_this_token and self.__heading_text is not None:
            self.__heading_text += token.debug_string(include_column_row_info=False)

    def handle_heading_start(self, token):
        """
        Process the start heading token, atx or setext
        """
        self.__heading_text = ""
        self.__start_token = token
        if self.__siblings_only:
            self.__hash_count = token.hash_count
        else:
            self.__hash_count = 1

    def handler_heading_end(self, context):
        """
        Process the end heading token, atx or setext
        """

        if self.__last_hash_count:
            while self.__last_hash_count < self.__hash_count:
                self.__last_hash_count += 1
                self.__heading_content_map[self.__last_hash_count - 1] = {}
            while self.__last_hash_count > self.__hash_count:
                self.__heading_content_map[self.__last_hash_count - 1] = {}
                self.__last_hash_count -= 1

        past_headings_map = self.__heading_content_map[self.__hash_count - 1]

        if self.__heading_text in past_headings_map:
            self.report_next_token_error(context, self.__start_token)
        else:
            past_headings_map[self.__heading_text] = self.__heading_text
        self.__heading_text = None
        self.__last_hash_count = self.__hash_count
