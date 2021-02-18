"""
Module to implement a plugin that looks for headings that are not surrounded by
blank lines.
"""
from pymarkdown.plugin_manager import Plugin, PluginDetails


class RuleMd022(Plugin):
    """
    Class to implement a plugin that looks for headings that are not surrounded by
    blank lines.
    """

    def __init__(self):
        super().__init__()
        self.__blank_line_count = None
        self.__did_above_line_count_match = None
        self.__start_heading_token = None
        self.__did_heading_end = None
        self.__lines_above = None
        self.__lines_below = None
        self.__start_heading_blank_line_count = None

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
        self.__lines_above = self.get_configuration_value(
            "lines_above", default_value=1
        )
        self.__lines_below = self.get_configuration_value(
            "lines_below", default_value=1
        )

    def starting_new_file(self):
        """
        Event that the a new file to be scanned is starting.
        """
        self.__blank_line_count = -1
        self.__did_above_line_count_match = False
        self.__start_heading_token = None
        self.__did_heading_end = False

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

        if token.is_blank_line:
            if (self.__blank_line_count is not None) and self.__blank_line_count >= 0:
                self.__blank_line_count += 1
        if token.is_setext_heading or token.is_atx_heading:
            self.__did_above_line_count_match = bool(
                self.__blank_line_count == -1
                or self.__blank_line_count == self.__lines_above
            )
            self.__start_heading_token = token
            self.__start_heading_blank_line_count = self.__blank_line_count
            self.__did_heading_end = False
        elif token.is_thematic_break:
            self.__blank_line_count = 0
        elif token.is_end_token:
            self.__blank_line_count = 0 if self.__is_leaf_end_token(token) else None
            if token.is_atx_heading_end or token.is_setext_heading_end:
                self.__did_heading_end = True

    # pylint: disable=too-many-boolean-expressions
    @classmethod
    def __is_leaf_end_token(cls, token):
        if (
            token.is_paragraph_end
            or token.is_atx_heading_end
            or token.is_setext_heading_end
            or token.is_thematic_break
            or token.is_html_block_end
            or token.is_fenced_code_block_end
            or token.is_indented_code_block_end
        ):
            return True
        return False

    # pylint: enable=too-many-boolean-expressions

    def perform_close_check(self, token):
        """
        Perform any state checks necessary upon closing the heading context.  Also
        called at the end of a document to make sure the implicit close of the
        document is handled properly.
        """

        if (
            (self.__start_heading_token and self.__did_heading_end)
        ) and self.__blank_line_count >= 0:
            if not token or not token.is_blank_line:
                did_end_match = bool(self.__blank_line_count == self.__lines_below)
                self.report_any_match_failures(did_end_match)
                self.__start_heading_token = None

    def report_any_match_failures(self, did_end_match):
        """
        Take care of reporting any match failures.
        """

        if not self.__did_above_line_count_match:
            extra_info = (
                "Expected: "
                + str(self.__lines_above)
                + "; Actual: "
                + str(self.__start_heading_blank_line_count)
                + "; Above"
            )
            self.report_next_token_error(
                self.__start_heading_token, extra_error_information=extra_info
            )
        if not did_end_match:
            extra_info = (
                "Expected: "
                + str(self.__lines_below)
                + "; Actual: "
                + str(self.__blank_line_count)
                + "; Below"
            )
            self.report_next_token_error(
                self.__start_heading_token, extra_error_information=extra_info
            )
