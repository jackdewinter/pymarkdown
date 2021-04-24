"""
Module to implement a plugin that looks for text in a paragraph where a line starts
with what could be an atx heading, except there is no spaces between the hashes and
the text of the heading.
"""
import re

from pymarkdown.plugin_manager import Plugin, PluginDetails


class RuleMd018(Plugin):
    """
    Class to implement a plugin that looks for text in a paragraph where a line starts
    with what could be an atx heading, except there is no spaces between the hashes and
    the text of the heading.
    """

    def __init__(self):
        super().__init__()
        self.__last_paragraph_token = None
        self.__paragraph_index = None
        self.__first_line_after_other_token = None
        self.__paragraph_column_number = None

    def get_details(self):
        """
        Get the details for the plugin.
        """
        return PluginDetails(
            # headings, headers, atx, spaces
            plugin_name="no-missing-space-atx",
            plugin_id="MD018",
            plugin_enabled_by_default=True,
            plugin_description="No space after hash on atx style heading",
            plugin_version="0.5.0",
            plugin_interface_version=1,
        )  # https://github.com/DavidAnson/markdownlint/blob/master/doc/Rules.md#md018---no-space-after-hash-on-atx-style-heading

    def starting_new_file(self):
        """
        Event that the a new file to be scanned is starting.
        """
        self.__last_paragraph_token = None
        self.__paragraph_index = None
        self.__first_line_after_other_token = None
        self.__paragraph_column_number = None

    def next_token(self, context, token):
        """
        Event that a new token is being processed.
        """
        if token.is_paragraph:
            self.__last_paragraph_token = token
            self.__paragraph_index = 0
            self.__first_line_after_other_token = True
            self.__first_line_after_hard_break = False
            self.__inside_of_link = False
            self.__paragraph_column_number = token.column_number
        elif token.is_paragraph_end:
            self.__last_paragraph_token = None
        elif self.__last_paragraph_token:
            if self.__inside_of_link:
                if token.is_inline_link_end:
                    self.__inside_of_link = False
            elif token.is_text:
                split_whitespace = (
                    self.__last_paragraph_token.extracted_whitespace.split("\n")
                )
                split_text = token.token_text.split("\n")

                for split_index, next_text in enumerate(split_text):
                    combined_text = (
                        split_whitespace[split_index + self.__paragraph_index]
                        + next_text
                    )
                    if (
                        self.__first_line_after_hard_break
                        or self.__first_line_after_other_token
                    ) or split_index:
                        if self.__first_line_after_other_token:
                            adjusted_column_number = self.__paragraph_column_number
                        else:
                            adjusted_column_number = (
                                self.__paragraph_column_number
                                + len(
                                    split_whitespace[
                                        split_index + self.__paragraph_index
                                    ]
                                )
                            )
                        if re.search(
                            r"^\s{0,3}#{1,6}\S", combined_text
                        ) and not re.search(r"#\s*$", combined_text):
                            self.report_next_token_error(
                                context,
                                token,
                                line_number_delta=split_index,
                                column_number_delta=-adjusted_column_number,
                            )
                    self.__first_line_after_other_token = False
                    self.__first_line_after_hard_break = False
                self.__paragraph_index += token.token_text.count("\n")
            elif token.is_inline_code_span:
                self.__paragraph_index += (
                    token.leading_whitespace.count("\n")
                    + token.span_text.count("\n")
                    + token.trailing_whitespace.count("\n")
                )
            elif token.is_inline_raw_html:
                self.__paragraph_index += token.raw_tag.count("\n")
            elif token.is_inline_image or token.is_inline_link:
                self.__paragraph_index += token.text_from_blocks.count("\n")
                if token.label_type == "inline":
                    self.__paragraph_index += token.before_link_whitespace.count("\n")
                    self.__paragraph_index += token.before_title_whitespace.count("\n")
                    self.__paragraph_index += token.after_title_whitespace.count("\n")
                    self.__paragraph_index += token.active_link_title.count("\n")
                if token.label_type == "full":
                    self.__paragraph_index += token.ex_label.count("\n")
                self.__inside_of_link = token.is_inline_link
            elif token.is_inline_hard_break:
                self.__paragraph_index += 1
                self.__first_line_after_hard_break = True
