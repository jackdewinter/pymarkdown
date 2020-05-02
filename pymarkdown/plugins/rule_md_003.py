"""
Module to implement a plugin that looks for heading styles that are inconsistent
throughout the document.
"""
from pymarkdown.markdown_token import AtxHeaderMarkdownToken, SetextHeaderMarkdownToken
from pymarkdown.plugin_manager import Plugin, PluginDetails


class RuleMd003(Plugin):
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

    def get_details(self):
        """
        Get the details for the plugin.
        """
        return PluginDetails(
            # headings, headers
            plugin_name="heading-style,header-style",
            plugin_id="MD003",
            plugin_enabled_by_default=True,
            plugin_description="Heading style",
        )  # https://github.com/DavidAnson/markdownlint/blob/master/doc/Rules.md#md003---heading-style
        # Parameters: style ("consistent", "atx", "atx_closed", "setext", "setext_with_atx", "setext_with_atx_closed"; default "consistent")

    def initialize_from_config(self):
        """
        Event to allow the plugin to load configuration information.
        """
        self.__style_type = self.get_configuration_value(
            "style",
            default_value=RuleMd003.__consistent_style,
            valid_values=RuleMd003.__valid_styles,
        )

    def starting_new_file(self):
        """
        Event that the a new file to be scanned is starting.
        """
        self.__actual_style_type = None
        if self.__style_type != RuleMd003.__consistent_style:
            self.__actual_style_type = self.__style_type

    def next_token(self, token):
        """
        Event that a new token is being processed.
        """
        header_style_type, is_header_level_1_or_2 = self.__get_header_properties(token)

        is_header_bad = False
        if header_style_type:
            expected_style_type = None
            if not self.__actual_style_type:
                self.__actual_style_type = header_style_type
            elif self.__actual_style_type in RuleMd003.__simple_styles:
                is_header_bad = bool(header_style_type != self.__actual_style_type)
                expected_style_type = self.__actual_style_type
            else:

                if self.__actual_style_type == RuleMd003.__setext_with_atx_style:
                    base_atx_style = RuleMd003.__atx_style
                else:
                    assert (
                        self.__actual_style_type
                        == RuleMd003.__setext_with_atx_closed_style
                    )
                    base_atx_style = RuleMd003.__atx_closed_style
                if not (
                    (
                        is_header_level_1_or_2
                        and header_style_type == RuleMd003.__setext_style
                    )
                    or (
                        not is_header_level_1_or_2
                        and header_style_type == base_atx_style
                    )
                ):
                    is_header_bad = True

                    if is_header_level_1_or_2:
                        expected_style_type = RuleMd003.__setext_style
                    else:
                        expected_style_type = base_atx_style

            if is_header_bad:
                extra_data = (
                    "Expected: "
                    + str(expected_style_type)
                    + "; Actual: "
                    + str(header_style_type)
                )
                self.report_next_token_error(token, extra_error_information=extra_data)

    @classmethod
    def __get_header_properties(cls, token):
        """
        Determine the header properties related to the current token.
        """

        header_style_type = None
        is_header_level_1_or_2 = None
        if isinstance(token, AtxHeaderMarkdownToken):
            if token.remove_trailing_count:
                header_style_type = RuleMd003.__atx_closed_style
            else:
                header_style_type = RuleMd003.__atx_style
            is_header_level_1_or_2 = bool(token.hash_count < 3)
        elif isinstance(token, SetextHeaderMarkdownToken):
            header_style_type = RuleMd003.__setext_style
            is_header_level_1_or_2 = True
        return header_style_type, is_header_level_1_or_2
