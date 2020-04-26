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


# pylint: disable=too-many-instance-attributes
class RuleMd022(Plugin):
    """
    Class to implement a plugin that looks for hard tabs in the files.
    """

    def __init__(self):
        super().__init__()
        self.blank_line_count = None
        self.did_start_match = None
        self.did_atx = None
        self.did_setext = None
        self.did_atx_terminate = None
        self.did_setext_terminate = None
        self.lines_above = None
        self.lines_below = None

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
        self.did_start_match = False
        self.did_atx = None
        self.did_setext = None
        self.did_atx_terminate = False
        self.did_setext_terminate = False

    def completed_file(self):
        """
        Event that the file being currently scanned is now completed.
        """
        self.perform_close_check(None)

    def next_token(self, token):
        """
        Event that a new token is being processed.
        """
        # print("token>" +str(token) + ">blc>" + str(self.blank_line_count))
        self.perform_close_check(token)

        if isinstance(token, BlankLineMarkdownToken):
            if (self.blank_line_count is not None) and self.blank_line_count >= 0:
                self.blank_line_count += 1
        if isinstance(token, AtxHeaderMarkdownToken):
            self.did_start_match = bool(
                self.blank_line_count == -1 or self.blank_line_count == self.lines_above
            )
            # print("self.did_start_match>>" + str(self.did_start_match))
            self.did_atx = token
            self.did_atx_terminate = False
        elif isinstance(token, SetextHeaderMarkdownToken):
            self.did_start_match = bool(
                self.blank_line_count == -1 or self.blank_line_count == self.lines_above
            )
            # print("self.did_start_match>>" + str(self.did_start_match))
            self.did_setext = token
            self.did_setext_terminate = False
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
            if token.type_name == MarkdownToken.token_atx_header:
                self.did_atx_terminate = True
            elif token.type_name == MarkdownToken.token_setext_header:
                self.did_setext_terminate = True

    def perform_close_check(self, token):
        """
        Perform any state checks necessary upon closing the header context.  Also
        called at the end of a document to make sure the implicit close of the
        document is handled properly.
        """

        if (
            (self.did_atx and self.did_atx_terminate)
            or (self.did_setext and self.did_setext_terminate)
        ) and self.blank_line_count >= 0:
            if not isinstance(token, BlankLineMarkdownToken):
                did_end_match = bool(self.blank_line_count == self.lines_below)
                # print("did_end_match>>" + str(did_end_match))
                # print("did_start_match>>" + str(self.did_start_match))
                if not did_end_match or not self.did_start_match:
                    if self.did_atx:
                        self.report_next_token_error(self.did_atx)
                    else:
                        self.report_next_token_error(self.did_setext)
                self.did_atx = None
                self.did_setext = None


# pylint: enable=too-many-instance-attributes
