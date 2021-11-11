"""
Module to implement a plugin that looks for bare URLs in the files.
"""
from pymarkdown.parser_helper import ParserHelper
from pymarkdown.plugin_details import PluginDetails
from pymarkdown.rule_plugin import RulePlugin


class RuleMd034(RulePlugin):
    """
    Class to implement a plugin that looks for bare URLs in the files.
    """

    __valid_uri_types = ["http:", "https:", "ftp:", "ftps:"]

    def __init__(self):
        super().__init__()
        self.__in_code_block = None
        self.__in_html_block = None
        self.__in_link = None

    def get_details(self):
        """
        Get the details for the plugin.
        """
        return PluginDetails(
            plugin_name="no-bare-urls",
            plugin_id="MD034",
            plugin_enabled_by_default=True,
            plugin_description="Bare URL used",
            plugin_version="0.5.0",
            plugin_interface_version=1,
            plugin_url="https://github.com/jackdewinter/pymarkdown/blob/main/docs/rules/rule_md034.md",
        )

    def starting_new_file(self):
        """
        Event that the a new file to be scanned is starting.
        """
        self.__in_code_block = False
        self.__in_html_block = False
        self.__in_link = False

    # pylint: disable=too-many-arguments
    def __evaluate_possible_url(
        self, source_text, url_prefix, found_index, context, token
    ):
        if found_index == 0 or source_text[found_index - 1] in (" ", "\n"):
            url_start_sequence = source_text[found_index + len(url_prefix) :]
            if (
                len(url_start_sequence) >= 3
                and url_start_sequence.startswith("//")
                and url_start_sequence[2] not in (" ", "\n")
            ):
                (
                    column_number_delta,
                    line_number_delta,
                ) = ParserHelper.adjust_for_newlines(source_text, 0, found_index)
                self.report_next_token_error(
                    context,
                    token,
                    line_number_delta=line_number_delta,
                    column_number_delta=column_number_delta,
                )

    # pylint: enable=too-many-arguments

    def next_token(self, context, token):
        """
        Event that a new token is being processed.
        """
        if (
            token.is_text
            and not self.__in_code_block
            and not self.__in_html_block
            and not self.__in_link
        ):
            for url_prefix in RuleMd034.__valid_uri_types:
                start_index = 0
                found_index = token.token_text.find(url_prefix, start_index)
                while found_index != -1:
                    self.__evaluate_possible_url(
                        token.token_text, url_prefix, found_index, context, token
                    )
                    start_index = found_index + len(url_prefix)
                    found_index = token.token_text.find(url_prefix, start_index)

        elif token.is_code_block:
            self.__in_code_block = True
        elif token.is_code_block_end:
            self.__in_code_block = False
        elif token.is_html_block:
            self.__in_html_block = True
        elif token.is_html_block_end:
            self.__in_html_block = False
        elif token.is_inline_link:
            self.__in_link = True
        elif token.is_inline_link_end:
            self.__in_link = False
