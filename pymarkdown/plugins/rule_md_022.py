"""
Module to implement a plugin that looks for hard tabs in the files.
"""
from pymarkdown.markdown_token import (
    AtxHeaderMarkdownToken,
    BlankLineMarkdownToken,
    EndMarkdownToken,
    MarkdownToken,
    SetextHeaderMarkdownToken,
    ThematicBreakMarkdownToken,
)
from pymarkdown.plugin_manager import Plugin, PluginDetails


class RuleMd022(Plugin):
    """
    Class to implement a plugin that looks for hard tabs in the files.
    """

    def __init__(self):
        super().__init__()
        self.blank_line_count = None
        self.did_above_line_count_match = None
        self.start_header_token = None
        self.did_header_end = None
        self.lines_above = None
        self.lines_below = None
        self.start_header_blank_line_count = None

    def get_details(self):
        """
        Get the details for the plugin.
        """
        return PluginDetails(
            # headings, headers, blank_lines
            plugin_name="blanks-around-headings,blanks-around-headers",
            plugin_id="MD022",
            plugin_enabled_by_default=True,
            plugin_description="Headings should be surrounded by blank lines",
        )  # https://github.com/DavidAnson/markdownlint/blob/master/doc/Rules.md#md022---headings-should-be-surrounded-by-blank-lines
        # Parameters: lines_above, lines_below (number; default 1)

    def initialize_from_config(self):
        """
        Event to allow the plugin to load configuration information.
        """
        self.lines_above = self.get_configuration_value("lines_above", default_value=1)
        self.lines_below = self.get_configuration_value("lines_below", default_value=1)

    def starting_new_file(self):
        """
        Event that the a new file to be scanned is starting.
        """
        self.blank_line_count = -1
        self.did_above_line_count_match = False
        self.start_header_token = None
        self.did_header_end = False

    def completed_file(self):
        """
        Event that the file being currently scanned is now completed.
        """
        self.perform_close_check(None)

    def next_token(self, token):
        """
        Event that a new token is being processed.
        """
        self.perform_close_check(token)

        if isinstance(token, BlankLineMarkdownToken):
            if (self.blank_line_count is not None) and self.blank_line_count >= 0:
                self.blank_line_count += 1
        if isinstance(token, (AtxHeaderMarkdownToken, SetextHeaderMarkdownToken)):
            self.did_above_line_count_match = bool(
                self.blank_line_count == -1 or self.blank_line_count == self.lines_above
            )
            self.start_header_token = token
            self.start_header_blank_line_count = self.blank_line_count
            self.did_header_end = False
        elif isinstance(token, ThematicBreakMarkdownToken):
            self.blank_line_count = 0
        elif isinstance(token, EndMarkdownToken):
            if token.type_name in (
                MarkdownToken.token_paragraph,
                MarkdownToken.token_atx_header,
                MarkdownToken.token_html_block,
                MarkdownToken.token_fenced_code_block,
                MarkdownToken.token_indented_code_block,
                MarkdownToken.token_thematic_break,
                MarkdownToken.token_setext_header,
            ):
                self.blank_line_count = 0
            else:
                self.blank_line_count = None
            if (
                token.type_name == MarkdownToken.token_atx_header
                or token.type_name == MarkdownToken.token_setext_header
            ):
                self.did_header_end = True

    def perform_close_check(self, token):
        """
        Perform any state checks necessary upon closing the header context.  Also
        called at the end of a document to make sure the implicit close of the
        document is handled properly.
        """

        if (
            (self.start_header_token and self.did_header_end)
        ) and self.blank_line_count >= 0:
            if not isinstance(token, BlankLineMarkdownToken):
                did_end_match = bool(self.blank_line_count == self.lines_below)
                self.report_any_match_failures(did_end_match)
                self.start_header_token = None

    def report_any_match_failures(self, did_end_match):
        """
        Take care of reporting any match failures.
        """

        if not self.did_above_line_count_match:
            extra_info = (
                "Expected: "
                + str(self.lines_above)
                + "; Actual: "
                + str(self.start_header_blank_line_count)
                + "; Above"
            )
            self.report_next_token_error(
                self.start_header_token, extra_error_information=extra_info
            )
        if not did_end_match:
            extra_info = (
                "Expected: "
                + str(self.lines_below)
                + "; Actual: "
                + str(self.blank_line_count)
                + "; Below"
            )
            self.report_next_token_error(
                self.start_header_token, extra_error_information=extra_info
            )
