"""
Module to implement a plugin that looks for heading styles that are inconsistent
throughout the document.
"""
from pymarkdown.plugin_details import PluginDetails
from pymarkdown.rule_plugin import RulePlugin


class RuleMd003(RulePlugin):
    """
    Class to implement a plugin that looks for heading styles that are inconsistent
    throughout the document.
    """

    __consistent_style = "consistent"
    __atx_style = "atx"
    __atx_closed_style = "atx_closed"
    __setext_style = "setext"
    __setext_with_atx_style = "setext_with_atx"
    __setext_with_atx_closed_style = "setext_with_atx_closed"

    __simple_styles = [__atx_style, __atx_closed_style, __setext_style]
    __valid_styles = [
        __consistent_style,
        __atx_style,
        __atx_closed_style,
        __setext_style,
        __setext_with_atx_style,
        __setext_with_atx_closed_style,
    ]

    def __init__(self):
        super().__init__()
        self.__style_type = None
        self.__actual_style_type = None
        self.__allow_consistent_setext_update = None

    def get_details(self):
        """
        Get the details for the plugin.
        """
        return PluginDetails(
            plugin_name="heading-style,header-style",
            plugin_id="MD003",
            plugin_enabled_by_default=True,
            plugin_description="Heading style should be consistent throughout the document.",
            plugin_version="0.5.0",
            plugin_interface_version=1,
            plugin_url="https://github.com/jackdewinter/pymarkdown/blob/main/docs/rules/rule_md003.md",
            plugin_configuration="style",
        )

    @classmethod
    def __validate_configuration_style(cls, found_value):
        if found_value not in RuleMd003.__valid_styles:
            raise ValueError(f"Allowable values: {RuleMd003.__valid_styles}")

    def initialize_from_config(self):
        """
        Event to allow the plugin to load configuration information.
        """
        self.__style_type = self.plugin_configuration.get_string_property(
            "style",
            default_value=RuleMd003.__consistent_style,
            valid_value_fn=self.__validate_configuration_style,
        )
        if self.__style_type == RuleMd003.__consistent_style:
            self.__allow_consistent_setext_update = (
                self.plugin_configuration.get_boolean_property(
                    "allow-setext-update", default_value=False
                )
            )
        else:
            self.__allow_consistent_setext_update = False

    def starting_new_file(self):
        """
        Event that the a new file to be scanned is starting.
        """
        self.__actual_style_type = None
        if self.__style_type != RuleMd003.__consistent_style:
            self.__actual_style_type = self.__style_type

    def __handle_simple_styles(self, heading_style_type, is_heading_level_1_or_2):
        is_heading_bad = bool(heading_style_type != self.__actual_style_type)

        if (
            is_heading_bad
            and self.__allow_consistent_setext_update
            and self.__actual_style_type == RuleMd003.__setext_style
            and heading_style_type == RuleMd003.__atx_style
            and not is_heading_level_1_or_2
        ):

            is_heading_bad = False
            self.__actual_style_type = RuleMd003.__setext_with_atx_style

        expected_style_type = self.__actual_style_type
        return is_heading_bad, expected_style_type

    def __handle_complex_styles(self, heading_style_type, is_heading_level_1_or_2):

        is_heading_bad, expected_style_type = False, None
        if self.__actual_style_type == RuleMd003.__setext_with_atx_style:
            base_atx_style = RuleMd003.__atx_style
        else:
            assert self.__actual_style_type == RuleMd003.__setext_with_atx_closed_style
            base_atx_style = RuleMd003.__atx_closed_style
        if not (
            (is_heading_level_1_or_2 and heading_style_type == RuleMd003.__setext_style)
            or (not is_heading_level_1_or_2 and heading_style_type == base_atx_style)
        ):
            is_heading_bad = True
            expected_style_type = (
                RuleMd003.__setext_style if is_heading_level_1_or_2 else base_atx_style
            )
            if (
                expected_style_type == RuleMd003.__setext_style
                and is_heading_level_1_or_2
                and self.__actual_style_type == RuleMd003.__setext_with_atx_style
            ):
                expected_style_type = RuleMd003.__setext_with_atx_style
        return is_heading_bad, expected_style_type

    def next_token(self, context, token):
        """
        Event that a new token is being processed.
        """
        heading_style_type, is_heading_level_1_or_2 = self.__get_heading_properties(
            token
        )

        is_heading_bad = False
        if heading_style_type:
            expected_style_type = None
            if not self.__actual_style_type:
                self.__actual_style_type = heading_style_type
            elif self.__actual_style_type in RuleMd003.__simple_styles:
                is_heading_bad, expected_style_type = self.__handle_simple_styles(
                    heading_style_type, is_heading_level_1_or_2
                )
            else:
                is_heading_bad, expected_style_type = self.__handle_complex_styles(
                    heading_style_type, is_heading_level_1_or_2
                )

            if is_heading_bad:
                extra_data = (
                    f"Expected: {expected_style_type}; Actual: {heading_style_type}"
                )
                self.report_next_token_error(
                    context, token, extra_error_information=extra_data
                )

    @classmethod
    def __get_heading_properties(cls, token):
        """
        Determine the heading properties related to the current token.
        """

        heading_style_type = None
        is_heading_level_1_or_2 = None
        if token.is_atx_heading:
            heading_style_type = (
                RuleMd003.__atx_closed_style
                if token.remove_trailing_count
                else RuleMd003.__atx_style
            )
            is_heading_level_1_or_2 = bool(token.hash_count < 3)
        elif token.is_setext_heading:
            heading_style_type = RuleMd003.__setext_style
            is_heading_level_1_or_2 = True
        return heading_style_type, is_heading_level_1_or_2
