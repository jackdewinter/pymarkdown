"""
Module to implement a plugin that looks for inconsistencies in the
style used for Unordered List elements.
"""
from pymarkdown.plugin_manager import Plugin, PluginDetails


class RuleMd004(Plugin):
    """
    Class to implement a plugin that looks for inconsistencies in the
    style used for Unordered List elements.
    """

    __consistent_style = "consistent"
    __asterisk_style = "asterisk"
    __plus_style = "plus"
    __dash_style = "dash"
    __sublist_style = "sublist"

    __valid_styles = [
        __consistent_style,
        __asterisk_style,
        __plus_style,
        __dash_style,
        __sublist_style,
    ]

    def __init__(self):
        super().__init__()
        self.__style_type = None
        self.__actual_style_type = None
        self.__current_list_level = None

    def get_details(self):
        """
        Get the details for the plugin.
        """
        return PluginDetails(
            # bullet, ul
            plugin_name="ul-style",
            plugin_id="MD004",
            plugin_enabled_by_default=True,
            plugin_description="Inconsistent Unordered List Start style",
            plugin_version="0.5.0",
            plugin_interface_version=1,
            plugin_url="https://github.com/jackdewinter/pymarkdown/blob/main/docs/rules/rule_md004.md",
            plugin_configuration="style",
        )

    @classmethod
    def __validate_configuration_style(cls, found_value):
        if found_value not in RuleMd004.__valid_styles:
            raise ValueError(f"Allowable values: {RuleMd004.__valid_styles}")

    def initialize_from_config(self):
        """
        Event to allow the plugin to load configuration information.
        """
        self.__style_type = self.plugin_configuration.get_string_property(
            "style",
            default_value=RuleMd004.__consistent_style,
            valid_value_fn=self.__validate_configuration_style,
        )

    def starting_new_file(self):
        """
        Event that the a new file to be scanned is starting.
        """
        self.__actual_style_type = {}
        self.__current_list_level = 0
        if self.__style_type not in (
            RuleMd004.__consistent_style,
            RuleMd004.__sublist_style,
        ):
            self.__actual_style_type[0] = self.__style_type

    @classmethod
    def __get_sequence_type(cls, token):
        if token.list_start_sequence == "*":
            return RuleMd004.__asterisk_style
        if token.list_start_sequence == "+":
            return RuleMd004.__plus_style
        assert token.list_start_sequence == "-"
        return RuleMd004.__dash_style

    def next_token(self, context, token):
        """
        Event that a new token is being processed.
        """
        if token.is_unordered_list_start:
            if self.__current_list_level not in self.__actual_style_type:
                if self.__style_type in (RuleMd004.__sublist_style,) or (
                    self.__style_type in (RuleMd004.__consistent_style)
                    and not self.__actual_style_type
                ):
                    self.__actual_style_type[
                        self.__current_list_level
                    ] = self.__get_sequence_type(token)
                else:
                    self.__actual_style_type[
                        self.__current_list_level
                    ] = self.__actual_style_type[0]

            this_start_style = self.__get_sequence_type(token)
            if self.__actual_style_type[self.__current_list_level] != this_start_style:
                extra_data = f"Expected: {self.__actual_style_type[self.__current_list_level]}; Actual: {this_start_style}"
                self.report_next_token_error(context, token, extra_data)
            self.__current_list_level += 1
        elif token.is_unordered_list_end:
            self.__current_list_level -= 1
