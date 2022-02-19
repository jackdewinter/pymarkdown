"""
Module to implement a plugin that looks for multiple top level headings.
"""
from pymarkdown.plugin_manager.plugin_details import PluginDetails
from pymarkdown.plugin_manager.rule_plugin import RulePlugin


class RuleMd025(RulePlugin):
    """
    Class to implement a plugin that looks for multiple top level headings.
    """

    def __init__(self):
        super().__init__()
        self.__have_top_level = None
        self.__front_matter_title = None
        self.__level = None

    def get_details(self):
        """
        Get the details for the plugin.
        """
        return PluginDetails(
            plugin_name="single-title,single-h1",
            plugin_id="MD025",
            plugin_enabled_by_default=True,
            plugin_description="Multiple top-level headings in the same document",
            plugin_version="0.5.0",
            plugin_interface_version=1,
            plugin_url="https://github.com/jackdewinter/pymarkdown/blob/main/docs/rules/rule_md025.md",
            plugin_configuration="level, front_matter_title",
        )

    @classmethod
    def __validate_configuration_level(cls, found_value):
        if found_value < 1 or found_value > 6:
            raise ValueError("Allowable values are between 1 and 6.")

    @classmethod
    def __validate_configuration_title(cls, found_value):
        found_value = found_value.strip()
        if not found_value:
            raise ValueError("Empty strings are not allowable values.")
        if found_value.find(":") != -1:
            raise ValueError("Colons (:) are not allowed in the value.")

    def initialize_from_config(self):
        """
        Event to allow the plugin to load configuration information.
        """
        self.__level = self.plugin_configuration.get_integer_property(
            "level",
            default_value=1,
            valid_value_fn=self.__validate_configuration_level,
        )
        self.__front_matter_title = self.plugin_configuration.get_string_property(
            "front_matter_title",
            default_value="title",
            valid_value_fn=self.__validate_configuration_title,
        ).lower()

    def starting_new_file(self):
        """
        Event that the a new file to be scanned is starting.
        """
        self.__have_top_level = False

    def next_token(self, context, token):
        """
        Event that a new token is being processed.
        """
        # print(">>>" + str(token).replace(ParserHelper.newline_character, "\\n"))
        is_token_heading = token.is_atx_heading or token.is_setext_heading
        if (
            is_token_heading
            and token.hash_count == self.__level
            and self.__have_top_level
        ):
            self.report_next_token_error(context, token)
        elif (is_token_heading and token.hash_count == self.__level) or (
            not is_token_heading
            and token.is_front_matter
            and self.__front_matter_title in token.matter_map
        ):
            self.__have_top_level = True
