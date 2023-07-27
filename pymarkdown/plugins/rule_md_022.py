"""
Module to implement a plugin that looks for headings that are not surrounded by
blank lines.
"""
from typing import Optional

from pymarkdown.plugin_manager.plugin_details import PluginDetails
from pymarkdown.plugin_manager.plugin_scan_context import PluginScanContext
from pymarkdown.plugin_manager.rule_plugin import RulePlugin
from pymarkdown.tokens.markdown_token import MarkdownToken


class RuleMd022(RulePlugin):
    """
    Class to implement a plugin that looks for headings that are not surrounded by
    blank lines.
    """

    def __init__(self) -> None:
        super().__init__()
        self.__blank_line_count = -1
        self.__did_above_line_count_match = False
        self.__start_heading_token: Optional[MarkdownToken] = None
        self.__did_heading_end = False
        self.__lines_above = 0
        self.__lines_below = 0
        self.__start_heading_blank_line_count = -1

    def get_details(self) -> PluginDetails:
        """
        Get the details for the plugin.
        """
        return PluginDetails(
            plugin_name="blanks-around-headings,blanks-around-headers",
            plugin_id="MD022",
            plugin_enabled_by_default=True,
            plugin_description="Headings should be surrounded by blank lines.",
            plugin_version="0.5.0",
            plugin_interface_version=1,
            plugin_url="https://github.com/jackdewinter/pymarkdown/blob/main/docs/rules/rule_md022.md",
            plugin_configuration="lines_above, lines_below",
        )

    @classmethod
    def __validate_configuration_value(cls, found_value: int) -> None:
        if found_value < 0:
            raise ValueError("Value must not be zero or a positive integer.")

    def initialize_from_config(self) -> None:
        """
        Event to allow the plugin to load configuration information.
        """
        self.__lines_above = self.plugin_configuration.get_integer_property(
            "lines_above",
            default_value=1,
            valid_value_fn=RuleMd022.__validate_configuration_value,
        )
        self.__lines_below = self.plugin_configuration.get_integer_property(
            "lines_below",
            default_value=1,
            valid_value_fn=RuleMd022.__validate_configuration_value,
        )

    def starting_new_file(self) -> None:
        """
        Event that the a new file to be scanned is starting.
        """
        self.__blank_line_count = -1
        self.__did_above_line_count_match = False
        self.__start_heading_token = None
        self.__did_heading_end = False

    def completed_file(self, context: PluginScanContext) -> None:
        """
        Event that the file being currently scanned is now completed.
        """
        if (self.__blank_line_count != -1) and self.__blank_line_count >= 0:
            self.perform_close_check(context, None)

    def __next_token_heading_start(self, token: MarkdownToken) -> None:
        # print(">>token.is_setext_heading or token.is_atx_heading>>")
        self.__did_above_line_count_match = self.__blank_line_count in [
            -1,
            self.__lines_above,
        ]

        self.__start_heading_token = token
        self.__start_heading_blank_line_count = self.__blank_line_count
        self.__did_heading_end = False
        # print("self.__did_above_line_count_match>>" + str(self.__did_above_line_count_match))

    def __next_token_heading_end(self, token: MarkdownToken) -> None:
        # print(">>token.is_end_token>>")
        if not token.is_list_end and not token.is_block_quote_end:
            self.__blank_line_count = (
                0 if token.is_leaf_end_token or token.is_container_end_token else -1
            )
        if token.is_atx_heading_end or token.is_setext_heading_end:
            self.__did_heading_end = True

    def next_token(self, context: PluginScanContext, token: MarkdownToken) -> None:
        """
        Event that a new token is being processed.
        """
        # print("START>>" + str(token).replace(ParserHelper.newline_character, "\\n").replace("\t", "\\t"))
        # print(">>self.__blank_line_count>>" + str(self.__blank_line_count))
        if (self.__blank_line_count != -1) and self.__blank_line_count >= 0:
            self.perform_close_check(context, token)

        if (
            token.is_blank_line
            and (self.__blank_line_count != -1)
            and self.__blank_line_count >= 0
        ):
            self.__blank_line_count += 1
        if token.is_setext_heading or token.is_atx_heading:
            self.__next_token_heading_start(token)
        elif token.is_thematic_break or token.is_link_reference_definition:
            self.__blank_line_count = 0
        elif token.is_end_token:
            self.__next_token_heading_end(token)
        # print(">>self.__blank_line_count>>" + str(self.__blank_line_count))

    def perform_close_check(
        self, context: PluginScanContext, token: Optional[MarkdownToken]
    ) -> None:
        """
        Perform any state checks necessary upon closing the heading context.  Also
        called at the end of a document to make sure the implicit close of the
        document is handled properly.
        """

        if (self.__start_heading_token and self.__did_heading_end) and (
            not token or (not token.is_blank_line and not token.is_block_quote_end)
        ):
            did_end_match = self.__blank_line_count == self.__lines_below
            # print(">>END: did_end_match>>" + str(did_end_match))
            self.report_any_match_failures(context, did_end_match)
            self.__start_heading_token = None

    def report_any_match_failures(
        self, context: PluginScanContext, did_end_match: bool
    ) -> None:
        """
        Take care of reporting any match failures.
        """

        assert self.__start_heading_token is not None
        if not self.__did_above_line_count_match:
            extra_info = f"Expected: {self.__lines_above}; Actual: {self.__start_heading_blank_line_count}; Above"
            # print(">>above>>" + extra_info)
            self.report_next_token_error(
                context,
                self.__start_heading_token,
                extra_error_information=extra_info,
                use_original_position=self.__start_heading_token.is_setext_heading,
            )
        if not did_end_match:
            extra_info = f"Expected: {self.__lines_below}; Actual: {self.__blank_line_count}; Below"
            # print(">>below>>" + extra_info)
            self.report_next_token_error(
                context,
                self.__start_heading_token,
                extra_error_information=extra_info,
                use_original_position=self.__start_heading_token.is_setext_heading,
            )
