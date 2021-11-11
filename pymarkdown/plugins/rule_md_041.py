"""
Module to implement a plugin that ensures that the first line in a file is a top level heading.
"""
from pymarkdown.plugin_manager import Plugin, PluginDetails


class RuleMd041(Plugin):
    """
    Class to implement a plugin that ensures that the first line in a file is a top level heading.
    """

    def __init__(self):
        super().__init__()
        self.__start_level = None
        self.__front_matter_title = None
        self.__have_seen_first_token = None
        self.__seen_html_block_start = None

    def get_details(self):
        """
        Get the details for the plugin.
        """
        return PluginDetails(
            plugin_name="first-line-heading,first-line-h1",
            plugin_id="MD041",
            plugin_enabled_by_default=True,
            plugin_description="First line in file should be a top level heading",
            plugin_version="0.5.0",
            plugin_interface_version=1,
            plugin_url="https://github.com/jackdewinter/pymarkdown/blob/main/docs/rules/rule_md041.md",
            plugin_configuration="level,front_matter_title",
        )

    @classmethod
    def __validate_configuration_level(cls, found_value):
        if found_value < 1 or found_value > 6:
            raise ValueError("Allowable values are between 1 and 6.")

    @classmethod
    def __validate_configuration_title(cls, found_value):
        found_value = found_value.strip()
        if found_value.find(":") != -1:
            raise ValueError("Colons (:) are not allowed in the value.")

    def initialize_from_config(self):
        """
        Event to allow the plugin to load configuration information.
        """
        self.__start_level = self.plugin_configuration.get_integer_property(
            "level",
            default_value=1,
            valid_value_fn=self.__validate_configuration_level,
        )
        self.__front_matter_title = (
            self.plugin_configuration.get_string_property(
                "front_matter_title",
                default_value="title",
                valid_value_fn=self.__validate_configuration_title,
            )
            .lower()
            .strip()
        )

    def starting_new_file(self):
        """
        Event that the a new file to be scanned is starting.
        """
        self.__have_seen_first_token = False
        self.__seen_html_block_start = None

    def next_token(self, context, token):
        """
        Event that a new token is being processed.
        """
        if self.__have_seen_first_token:
            return
        if token.is_atx_heading or token.is_setext_heading:
            self.__have_seen_first_token = True
            if token.hash_count != self.__start_level:
                self.report_next_token_error(context, token)
        elif token.is_front_matter and self.__front_matter_title:
            if self.__front_matter_title in token.matter_map:
                self.__have_seen_first_token = True
        elif token.is_html_block:
            self.__seen_html_block_start = token
        elif self.__seen_html_block_start:
            assert token.is_text
            html_block_contents = token.token_text.strip()
            if not html_block_contents.startswith(
                "<h1 "
            ) and not html_block_contents.startswith("<h1>"):
                self.report_next_token_error(context, self.__seen_html_block_start)
            self.__have_seen_first_token = True
        elif not token.is_blank_line:
            self.report_next_token_error(context, token)
            self.__have_seen_first_token = True
