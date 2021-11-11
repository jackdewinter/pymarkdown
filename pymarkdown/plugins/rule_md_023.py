"""
Module to implement a plugin that looks for headings that do not start at the
beginning of the line.
"""
from pymarkdown.parser_helper import ParserHelper
from pymarkdown.plugin_details import PluginDetails
from pymarkdown.rule_plugin import RulePlugin


class RuleMd023(RulePlugin):
    """
    Class to implement a plugin that looks for headings that do not start at the
    beginning of the line.
    """

    def __init__(self):
        super().__init__()
        self.__setext_start_token = None
        self.__any_leading_whitespace_detected = None
        self.__seen_first_line_of_setext = None

    def get_details(self):
        """
        Get the details for the plugin.
        """
        return PluginDetails(
            plugin_name="heading-start-left, header-start-left",
            plugin_id="MD023",
            plugin_enabled_by_default=True,
            plugin_description="Headings must start at the beginning of the line.",
            plugin_version="0.5.0",
            plugin_interface_version=1,
            plugin_url="https://github.com/jackdewinter/pymarkdown/blob/main/docs/rules/rule_md023.md",
        )

    def starting_new_file(self):
        """
        Event that the a new file to be scanned is starting.
        """
        self.__setext_start_token = None
        self.__any_leading_whitespace_detected = False
        self.__seen_first_line_of_setext = False

    def next_token(self, context, token):
        """
        Event that a new token is being processed.
        """
        if token.is_atx_heading:
            if token.extracted_whitespace:
                self.report_next_token_error(context, token)
        elif token.is_setext_heading:
            self.__setext_start_token = token
            self.__any_leading_whitespace_detected = bool(token.extracted_whitespace)
            self.__seen_first_line_of_setext = False
        elif token.is_text:
            if (
                self.__setext_start_token
                and not self.__any_leading_whitespace_detected
                and token.end_whitespace
            ):
                split_end_whitespace = token.end_whitespace.split("\n")
                for next_split in split_end_whitespace:
                    if self.__seen_first_line_of_setext:
                        split_next_split = next_split.split(
                            ParserHelper.whitespace_split_character
                        )
                        if len(split_next_split) == 2 and split_next_split[0]:
                            self.__any_leading_whitespace_detected = True
                    else:
                        self.__seen_first_line_of_setext = True
        elif token.is_setext_heading_end:
            if token.extracted_whitespace:
                self.__any_leading_whitespace_detected = True

            if self.__any_leading_whitespace_detected:
                self.report_next_token_error(context, self.__setext_start_token)
            self.__setext_start_token = None
