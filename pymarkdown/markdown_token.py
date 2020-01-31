"""
Module to provide for an element that can be added to markdown parsing stream.
"""


class MarkdownToken:
    """
    Class to provide for a base encapsulation of the markdown tokens.
    """

    token_blank_line = "BLANK"
    token_paragraph = "para"
    token_text = "text"
    token_indented_code_block = "icode-block"
    token_fenced_code_block = "fcode-block"
    token_thematic_break = "tbreak"
    token_block_quote = "block-quote"
    token_atx_header = "atx"
    token_setext_header = "setext"
    token_unordered_list_start = "ulist"
    token_ordered_list_start = "olist"
    token_new_list_item = "li"
    token_html_block = "html-block"

    def __init__(self, token_name, extra_data=None):
        self.token_name = token_name
        self.extra_data = extra_data

    def __str__(self):
        add_extra = ""
        if (
            self.extra_data
            or self.token_name == MarkdownToken.token_paragraph
            or self.token_name == MarkdownToken.token_blank_line
            or self.token_name == MarkdownToken.token_block_quote
        ):
            add_extra = ":" + self.extra_data
        return "[" + self.token_name + add_extra + "]"

    def __repr__(self):
        return "'" + self.__str__() + "'"

    @property
    def is_blank_line(self):
        """
        Returns whether or not the current token is the blank line element.
        """
        return self.token_name == MarkdownToken.token_blank_line

    @property
    def is_list_start(self):
        """
        Returns whether or not the current token is a list element.
        """
        return (
            self.token_name == MarkdownToken.token_unordered_list_start
            or self.token_name == MarkdownToken.token_ordered_list_start
        )

    @property
    def is_new_list_item(self):
        """
        Returns whether or not the current token is a list item element.
        """
        return self.token_name == MarkdownToken.token_new_list_item

    @property
    def is_any_list_token(self):
        """
        Returns whether or not the current token is a list item element or a list element.
        """
        return self.is_new_list_item or self.is_list_start

    @property
    def is_paragraph(self):
        """
        Returns whether or not the current token is a paragraph element.
        """
        return self.token_name == MarkdownToken.token_paragraph

    @property
    def is_html_block(self):
        """
        Returns whether or not the current token is a html block element.
        """
        return self.token_name == MarkdownToken.token_html_block


# pylint: disable=too-few-public-methods
class BlankLineMarkdownToken(MarkdownToken):
    """
    Class to provide for an encapsulation of the blank line element.
    """

    def __init__(self, extracted_whitespace):
        MarkdownToken.__init__(
            self, MarkdownToken.token_blank_line, extracted_whitespace
        )


class ParagraphMarkdownToken(MarkdownToken):
    """
    Class to provide for an encapsulation of the paragraph element.
    """

    def __init__(self, extracted_whitespace):
        MarkdownToken.__init__(
            self, MarkdownToken.token_paragraph, extracted_whitespace
        )


class IndentedCodeBlockMarkdownToken(MarkdownToken):
    """
    Class to provide for an encapsulation of the indented code block element.
    """

    def __init__(self, extracted_whitespace):
        MarkdownToken.__init__(
            self, MarkdownToken.token_indented_code_block, extracted_whitespace
        )


class FencedCodeBlockMarkdownToken(MarkdownToken):
    """
    Class to provide for an encapsulation of the fenced code block element.
    """

    # pylint: disable=too-many-arguments
    def __init__(
        self,
        fence_character,
        fence_count,
        extracted_text,
        text_after_extracted_text,
        extracted_whitespace,
        extracted_whitespace_before_info_string,
    ):
        MarkdownToken.__init__(
            self,
            MarkdownToken.token_fenced_code_block,
            fence_character
            + ":"
            + str(fence_count)
            + ":"
            + extracted_text
            + ":"
            + text_after_extracted_text
            + ":"
            + extracted_whitespace
            + ":"
            + extracted_whitespace_before_info_string,
        )

    # pylint: enable=too-many-arguments


class AtxHeaderMarkdownToken(MarkdownToken):
    """
    Class to provide for an encapsulation of the atx header element.
    """

    # pylint: disable=too-many-arguments
    def __init__(
        self,
        hash_count,
        remaining_line,
        extracted_whitespace,
        extracted_whitespace_at_start,
        extracted_whitespace_at_end,
        extracted_whitespace_before_end,
    ):
        MarkdownToken.__init__(
            self,
            MarkdownToken.token_atx_header,
            str(hash_count)
            + ":"
            + remaining_line
            + ":"
            + extracted_whitespace
            + ":"
            + extracted_whitespace_at_start
            + ":"
            + extracted_whitespace_at_end
            + ":"
            + extracted_whitespace_before_end,
        )

    # pylint: enable=too-many-arguments


class SetextHeaderMarkdownToken(MarkdownToken):
    """
    Class to provide for an encapsulation of the setext header element.
    """

    def __init__(self, header_character, remaining_line):
        MarkdownToken.__init__(
            self,
            MarkdownToken.token_setext_header,
            header_character + ":" + remaining_line,
        )


class EndMarkdownToken(MarkdownToken):
    """
    Class to provide for an encapsulation of the end element to a matching start.
    """

    def __init__(self, type_name, extracted_whitespace, extra_data):

        display_data = extracted_whitespace
        if extra_data is not None:
            display_data = display_data + ":" + extra_data

        MarkdownToken.__init__(
            self, "end-" + type_name, display_data,
        )


class SetextHeaderEndMarkdownToken(EndMarkdownToken):
    """
    Class to provide for an encapsulation of the end of a setext header element.
    """

    def __init__(self, extracted_whitespace, extra_whitespace_after_setext):
        super().__init__(
            MarkdownToken.token_setext_header,
            extracted_whitespace,
            extra_whitespace_after_setext,
        )


class TextMarkdownToken(MarkdownToken):
    """
    Class to provide for an encapsulation of the text element.
    """

    def __init__(self, token_text, extracted_whitespace):
        MarkdownToken.__init__(
            self, MarkdownToken.token_text, token_text + ":" + extracted_whitespace
        )


class BlockQuoteMarkdownToken(MarkdownToken):
    """
    Class to provide for an encapsulation of the block quote element.
    """

    def __init__(self, extracted_whitespace):
        MarkdownToken.__init__(
            self, MarkdownToken.token_block_quote, extracted_whitespace
        )


class UnorderedListStartMarkdownToken(MarkdownToken):
    """
    Class to provide for an encapsulation of the unordered list start element.
    """

    def __init__(self, list_start_sequence, indent_level, extracted_whitespace):
        self.indent_level = indent_level
        MarkdownToken.__init__(
            self,
            MarkdownToken.token_unordered_list_start,
            list_start_sequence + "::" + str(indent_level) + ":" + extracted_whitespace,
        )


class OrderedListStartMarkdownToken(MarkdownToken):
    """
    Class to provide for an encapsulation of the ordered list start element.
    """

    def __init__(
        self,
        list_start_sequence,
        list_start_content,
        indent_level,
        extracted_whitespace,
    ):
        self.indent_level = indent_level
        MarkdownToken.__init__(
            self,
            MarkdownToken.token_ordered_list_start,
            list_start_sequence
            + ":"
            + list_start_content
            + ":"
            + str(indent_level)
            + ":"
            + extracted_whitespace,
        )


class NewListItemMarkdownToken(MarkdownToken):
    """
    Class to provide for an encapsulation of the new list item element.
    """

    def __init__(self, indent_level):
        self.indent_level = indent_level
        MarkdownToken.__init__(
            self, MarkdownToken.token_new_list_item, str(indent_level)
        )


class HtmlBlockMarkdownToken(MarkdownToken):
    """
    Class to provide for an encapsulation of the html block element.
    """

    def __init__(self):
        MarkdownToken.__init__(self, MarkdownToken.token_html_block, "")


class ThematicBreakMarkdownToken(MarkdownToken):
    """
    Class to provide for an encapsulation of the thematic break element.
    """

    def __init__(self, start_character, extracted_whitespace, rest_of_line):
        MarkdownToken.__init__(
            self,
            MarkdownToken.token_thematic_break,
            start_character + ":" + extracted_whitespace + ":" + rest_of_line,
        )


# pylint: enable=too-few-public-methods
