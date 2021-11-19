"""
Module to implement a plugin that looks for text in a paragraph where a line starts
with what could be an atx heading, except there is no spaces between the hashes and
the text of the heading.
"""
import re

from pymarkdown.plugin_details import PluginDetails
from pymarkdown.rule_plugin import RulePlugin


class StartOfLineTokenParser:
    """
    Token parser that activates a check only on valid newlines within
    a paragraph.
    """

    def __init__(self):
        self.__last_paragraph_token = None
        self.__paragraph_index = None
        self.__first_line_after_other_token = None
        self.__paragraph_column_number = None
        self.__inside_of_link = None
        self.__first_line_after_hard_break = None
        self.__delayed_line = None

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
            self.__next_token_paragraph_start(token)
        elif token.is_paragraph_end:
            self.__next_token_paragraph_end()
        elif self.__last_paragraph_token:
            if self.__inside_of_link:
                if token.is_inline_link_end:
                    self.__inside_of_link = False
            elif token.is_text:
                self.__next_token_paragraph_text_inline(token, context)
            else:
                self.__next_token_paragraph_non_text_inline(token)

    def __next_token_paragraph_start(self, token):
        self.__last_paragraph_token = token
        self.__paragraph_index = 0
        self.__first_line_after_other_token = True
        self.__first_line_after_hard_break = False
        self.__inside_of_link = False
        self.__paragraph_column_number = token.column_number
        self.__delayed_line = None

    def __next_token_paragraph_end(self):
        if self.__delayed_line:
            self.check_start_of_line(
                self.__delayed_line[0],
                self.__delayed_line[1],
                self.__delayed_line[2],
                self.__delayed_line[3],
                self.__delayed_line[4],
            )
            self.__delayed_line = None
        self.__last_paragraph_token = None

    def __next_token_paragraph_non_text_inline(self, token):
        if token.is_inline_code_span:
            self.__delayed_line = None
            self.__paragraph_index += (
                token.leading_whitespace.count("\n")
                + token.span_text.count("\n")
                + token.trailing_whitespace.count("\n")
            )
        elif token.is_inline_raw_html:
            self.__delayed_line = None
            self.__paragraph_index += token.raw_tag.count("\n")
        elif token.is_inline_image or token.is_inline_link:
            self.__delayed_line = None
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
            self.__delayed_line = None
            self.__paragraph_index += 1
            self.__first_line_after_hard_break = True
        else:
            assert (
                token.is_inline_emphasis
                or token.is_inline_emphasis_end
                or token.is_inline_autolink
            )
            self.__delayed_line = None

    def __next_token_paragraph_text_inline(self, token, context):
        split_whitespace = self.__last_paragraph_token.extracted_whitespace.split("\n")
        split_text = token.token_text.split("\n")

        for split_index, next_text in enumerate(split_text):
            combined_text = (
                f"{split_whitespace[split_index + self.__paragraph_index]}{next_text}"
            )
            if (
                self.__first_line_after_hard_break
                or self.__first_line_after_other_token
            ) or split_index:
                if self.__first_line_after_other_token:
                    adjusted_column_number = self.__paragraph_column_number
                else:
                    adjusted_column_number = self.__paragraph_column_number + len(
                        split_whitespace[split_index + self.__paragraph_index]
                    )
                # pylint: disable=invalid-unary-operand-type
                # See https://github.com/PyCQA/pylint/issues/1472
                if split_index == len(split_text) - 1:
                    self.__delayed_line = (
                        combined_text,
                        context,
                        token,
                        split_index,
                        -adjusted_column_number,
                    )
                else:
                    self.check_start_of_line(
                        combined_text,
                        context,
                        token,
                        split_index,
                        -adjusted_column_number,
                    )
                # pylint: enable=invalid-unary-operand-type
            self.__first_line_after_other_token = False
            self.__first_line_after_hard_break = False
        self.__paragraph_index += token.token_text.count("\n")

    # pylint: disable=too-many-arguments
    def check_start_of_line(
        self, combined_text, context, token, line_number_delta, column_number_delta
    ):
        """
        Check for a pattern at the start of the line.
        """

    # pylint: enable=too-many-arguments


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

        Note that the logic here is a bit weird for the `\\S` at the end of the
        regular expression.  If everything else is good except for that `\\S`,
        which is equivalent to any whitespace character, and it was a space character,
        it would match the Atx code in the leaf processor and be an Atx Heading token
        already.  Hence, what is left is any other whitespace character which is not
        the space character, which should still trigger the rule.
        """
        if re.search(r"^\s{0,3}#{1,6}\S", combined_text) and not re.search(
            r"#\s*$", combined_text
        ):
            self.__owner.report_next_token_error(
                context,
                token,
                line_number_delta=line_number_delta,
                column_number_delta=column_number_delta,
            )

    # pylint: enable=too-many-arguments


class RuleMd018(RulePlugin):
    """
    Class to implement a plugin that looks for text in a paragraph where a line starts
    with what could be an atx heading, except there is no spaces between the hashes and
    the text of the heading.
    """

    def __init__(self):
        super().__init__()
        self.__token_parser = MyStartOfLineTokenParser(self)

    def get_details(self):
        """
        Get the details for the plugin.
        """
        return PluginDetails(
            plugin_name="no-missing-space-atx",
            plugin_id="MD018",
            plugin_enabled_by_default=True,
            plugin_description="No space present after the hash character on a possible Atx Heading.",
            plugin_version="0.5.0",
            plugin_interface_version=1,
            plugin_url="https://github.com/jackdewinter/pymarkdown/blob/main/docs/rules/rule_md018.md",
        )

    def starting_new_file(self):
        """
        Event that the a new file to be scanned is starting.
        """
        self.__token_parser.starting_new_file()

    def next_token(self, context, token):
        """
        Event that a new token is being processed.
        """
        self.__token_parser.next_token(context, token)
