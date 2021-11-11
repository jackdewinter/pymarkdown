"""
Module to implement a plugin that looks for text in a paragraph where a line starts
with what could be a closed atx heading, except there is no spaces between the hashes
and the text of the heading, either at the start, end, or both.
"""
import re

from pymarkdown.plugin_details import PluginDetails
from pymarkdown.plugins.rule_md_018 import StartOfLineTokenParser
from pymarkdown.rule_plugin import RulePlugin


class MyStartOfLineTokenParser(StartOfLineTokenParser):
    """
    Local implementation of the token parser.
    """

    def __init__(self, owner):
        super().__init__()
        self.__owner = owner

    # pylint: disable=too-many-arguments
    def check_start_of_line(
        self, combined_text, context, token, line_number_delta, column_number_delta
    ):
        """
        Check for a pattern at the start of the line.
        """
        if re.search(r"^\s{0,3}#{1,6}.*#+\s*$", combined_text):
            self.__owner.report_next_token_error(
                context,
                token,
                line_number_delta=line_number_delta,
                column_number_delta=column_number_delta,
            )

    # pylint: enable=too-many-arguments


class RuleMd020(RulePlugin):
    """
    Class to implement a plugin that looks for text in a paragraph where a line starts
    with what could be a closed atx heading, except there is no spaces between the hashes
    and the text of the heading, either at the start, end, or both.
    """

    def __init__(self):
        super().__init__()
        self.__token_parser = MyStartOfLineTokenParser(self)
        self.__is_in_normal_atx = None
        self.__last_atx_token = None

    def get_details(self):
        """
        Get the details for the plugin.
        """
        return PluginDetails(
            plugin_name="no-missing-space-closed-atx",
            plugin_id="MD020",
            plugin_enabled_by_default=True,
            plugin_description="No space present inside of the hashes on a possible Atx Closed Heading.",
            plugin_version="0.5.0",
            plugin_interface_version=1,
            plugin_url="https://github.com/jackdewinter/pymarkdown/blob/main/docs/rules/rule_md020.md",
        )

    def starting_new_file(self):
        """
        Event that the a new file to be scanned is starting.
        """
        self.__token_parser.starting_new_file()
        self.__is_in_normal_atx = False
        self.__last_atx_token = None

    def next_token(self, context, token):
        """
        Event that a new token is being processed.
        """
        self.__token_parser.next_token(context, token)
        if not token.is_atx_heading_end and self.__is_in_normal_atx:
            self.__last_atx_token = token

        if token.is_atx_heading:
            self.__is_in_normal_atx = True
        elif token.is_atx_heading_end:
            if (
                self.__is_in_normal_atx
                and self.__last_atx_token.is_text
                and self.__last_atx_token.token_text.endswith("#")
            ):
                regex_match = re.search(r"\#+$", self.__last_atx_token.token_text)
                self.report_next_token_error(
                    context,
                    self.__last_atx_token,
                    column_number_delta=regex_match.start(),
                )
            self.__is_in_normal_atx = False
