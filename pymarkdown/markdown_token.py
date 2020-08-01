"""
Module to provide for an element that can be added to markdown parsing stream.
"""
import logging
from enum import Enum

from pymarkdown.constants import Constants
from pymarkdown.parser_helper import ParserHelper

LOGGER = logging.getLogger(__name__)

# pylint: disable=too-many-lines


class MarkdownTokenClass(Enum):
    """
    Enumeration to provide guidance on what class of token the token is.
    """

    CONTAINER_BLOCK = 0
    LEAF_BLOCK = 1
    INLINE_BLOCK = 2


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
    token_link_reference_definition = "link-ref-def"
    token_atx_heading = "atx"
    token_setext_heading = "setext"
    token_unordered_list_start = "ulist"
    token_ordered_list_start = "olist"
    token_new_list_item = "li"
    token_html_block = "html-block"
    token_inline_code_span = "icode-span"
    token_inline_hard_break = "hard-break"
    token_inline_uri_autolink = "uri-autolink"
    token_inline_email_autolink = "email-autolink"
    token_inline_raw_html = "raw-html"
    token_inline_emphasis = "emphasis"
    token_inline_link = "link"
    token_inline_image = "image"

    # pylint: disable=too-many-arguments
    def __init__(
        self,
        token_name,
        token_class,
        extra_data=None,
        line_number=0,
        column_number=0,
        position_marker=None,
    ):
        self.token_name = token_name
        self.token_class = token_class
        self.extra_data = extra_data

        if position_marker:
            line_number = position_marker.line_number
            column_number = (
                position_marker.index_number + position_marker.index_indent + 1
            )
        self.line_number = line_number
        self.column_number = column_number

    # pylint: enable=too-many-arguments

    def __str__(self):
        add_extra = ""
        if (
            self.extra_data
            or self.token_name == MarkdownToken.token_paragraph
            or self.token_name == MarkdownToken.token_blank_line
            or self.token_name == MarkdownToken.token_block_quote
        ):
            add_extra = ":" + self.extra_data
        column_row_info = ""
        if self.line_number or self.column_number:
            column_row_info = (
                "(" + str(self.line_number) + "," + str(self.column_number) + ")"
            )
        return "[" + self.token_name + column_row_info + add_extra + "]"

    def __repr__(self):
        return "'" + self.__str__() + "'"

    @property
    def is_block(self):
        """
        Returns whether or not the current token is one of the block tokens.
        """
        # block quotes?
        return (
            self.is_list_start
            or self.token_name == MarkdownToken.token_thematic_break
            or self.is_atx_heading
            or self.is_setext
            or self.is_code_block
            or self.token_name == MarkdownToken.token_html_block
            or self.is_paragraph
        )
        # lrd or \
        # or tables

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
    def is_text(self):
        """
        Returns whether or not the current token is a paragraph element.
        """
        return self.token_name == MarkdownToken.token_text

    @property
    def is_setext(self):
        """
        Returns whether or not the current token is a setext element.
        """
        return self.token_name == MarkdownToken.token_setext_heading

    @property
    def is_atx_heading(self):
        """
        Returns whether or not the current token is an atx element.
        """
        return self.token_name == MarkdownToken.token_atx_heading

    @property
    def is_code_block(self):
        """
        Returns whether or not the current token is a code block element.
        """
        return (
            self.token_name == MarkdownToken.token_fenced_code_block
            or self.token_name == MarkdownToken.token_indented_code_block
        )

    @property
    def is_indented_code_block(self):
        """
        Returns whether or not the current token is an indented code block element.
        """
        return self.token_name == MarkdownToken.token_indented_code_block

    @property
    def is_fenced_code_block(self):
        """
        Returns whether or not the current token is a fenced code block element.
        """
        return self.token_name == MarkdownToken.token_fenced_code_block


# pylint: disable=too-few-public-methods
class BlankLineMarkdownToken(MarkdownToken):
    """
    Class to provide for an encapsulation of the blank line element.
    """

    def __init__(self, extracted_whitespace, position_marker, column_delta=0):
        self.extracted_whitespace = extracted_whitespace

        line_number = 0
        column_number = 0
        if position_marker:
            line_number = position_marker.line_number
            column_number = (
                position_marker.index_number
                + position_marker.index_indent
                + 1
                - column_delta
            )

        MarkdownToken.__init__(
            self,
            MarkdownToken.token_blank_line,
            MarkdownTokenClass.LEAF_BLOCK,
            extracted_whitespace,
            line_number=line_number,
            column_number=column_number,
        )


class ParagraphMarkdownToken(MarkdownToken):
    """
    Class to provide for an encapsulation of the paragraph element.
    """

    def __init__(self, extracted_whitespace, position_marker):
        self.extracted_whitespace = extracted_whitespace
        self.final_whitespace = ""
        self.rehydrate_index = 0
        MarkdownToken.__init__(
            self,
            MarkdownToken.token_paragraph,
            MarkdownTokenClass.LEAF_BLOCK,
            "",
            position_marker=position_marker,
        )
        self.compose_extra_data_field()

    def compose_extra_data_field(self):
        """
        Compose the object's self.extra_data field from the local object's variables.
        """

        self.extra_data = self.extracted_whitespace
        if self.final_whitespace:
            self.extra_data = self.extra_data + ":" + self.final_whitespace

    def add_whitespace(self, whitespace_to_add):
        """
        Add extra whitespace to the end of the current paragraph.  Should only be
        used when combining text blocks in a paragraph.
        """

        self.extracted_whitespace = self.extracted_whitespace + whitespace_to_add
        self.compose_extra_data_field()

    def set_final_whitespace(self, whitespace_to_set):
        """
        Set the final whitespace for the paragraph. That is any whitespace at the very
        end of the paragraph, removed to prevent hard lines at the end.
        """

        self.final_whitespace = whitespace_to_set
        self.compose_extra_data_field()


# pylint: disable=too-many-instance-attributes
class SetextHeadingMarkdownToken(MarkdownToken):
    """
    Class to provide for an encapsulation of the setext heading element.
    """

    # pylint: disable=too-many-arguments
    def __init__(
        self,
        heading_character,
        heading_character_count,
        extracted_whitespace,
        position_marker,
        para_token,
    ):
        self.heading_character = heading_character
        self.heading_character_count = heading_character_count
        self.extracted_whitespace = extracted_whitespace
        self.final_whitespace = ""
        if self.heading_character == "=":
            self.hash_count = 1
        elif self.heading_character == "-":
            self.hash_count = 2
        else:
            self.hash_count = -1
        if para_token:
            self.original_line_number = para_token.line_number
            self.original_column_number = para_token.column_number
        else:
            self.original_line_number = -1
            self.original_column_number = -1
        MarkdownToken.__init__(
            self,
            MarkdownToken.token_setext_heading,
            MarkdownTokenClass.LEAF_BLOCK,
            "",
            position_marker=position_marker,
        )
        self.compose_extra_data_field()

    # pylint: enable=too-many-arguments

    def set_final_whitespace(self, whitespace_to_set):
        """
        Set the final whitespace for the paragraph. That is any whitespace at the very
        end of the paragraph, removed to prevent hard lines at the end.
        """

        self.final_whitespace = whitespace_to_set
        self.compose_extra_data_field()

    def compose_extra_data_field(self):
        """
        Compose the object's self.extra_data field from the local object's variables.
        """

        self.extra_data = (
            self.heading_character
            + ":"
            + str(self.heading_character_count)
            + ":"
            + self.extracted_whitespace
            + ":("
            + str(self.original_line_number)
            + ","
            + str(self.original_column_number)
            + ")"
        )
        if self.final_whitespace:
            self.extra_data = self.extra_data + ":" + self.final_whitespace


# pylint: enable=too-many-instance-attributes


class IndentedCodeBlockMarkdownToken(MarkdownToken):
    """
    Class to provide for an encapsulation of the indented code block element.
    """

    def __init__(self, extracted_whitespace, line_number, column_number):
        self.extracted_whitespace = extracted_whitespace
        self.indented_whitespace = ""
        MarkdownToken.__init__(
            self,
            MarkdownToken.token_indented_code_block,
            MarkdownTokenClass.LEAF_BLOCK,
            extracted_whitespace,
            line_number=line_number,
            column_number=column_number,
        )
        self.compose_extra_data_field()

    def compose_extra_data_field(self):
        """
        Compose the object's self.extra_data field from the local object's variables.
        """
        self.extra_data = self.extracted_whitespace + ":" + self.indented_whitespace

    def add_indented_whitespace(self, indented_whitespace):
        """
        Add the indented whitespace that comes before the text.
        """
        self.indented_whitespace += ParserHelper.newline_character + indented_whitespace
        self.compose_extra_data_field()


# pylint: disable=too-many-instance-attributes
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
        pre_extracted_text,
        text_after_extracted_text,
        pre_text_after_extracted_text,
        extracted_whitespace,
        extracted_whitespace_before_info_string,
        position_marker,
    ):
        self.extracted_whitespace = extracted_whitespace
        self.extracted_text = extracted_text
        self.pre_extracted_text = pre_extracted_text
        self.extracted_whitespace_before_info_string = (
            extracted_whitespace_before_info_string
        )
        self.text_after_extracted_text = text_after_extracted_text
        self.pre_text_after_extracted_text = pre_text_after_extracted_text
        self.fence_character = fence_character
        self.fence_count = fence_count
        MarkdownToken.__init__(
            self,
            MarkdownToken.token_fenced_code_block,
            MarkdownTokenClass.LEAF_BLOCK,
            fence_character
            + ":"
            + str(fence_count)
            + ":"
            + extracted_text
            + ":"
            + pre_extracted_text
            + ":"
            + text_after_extracted_text
            + ":"
            + pre_text_after_extracted_text
            + ":"
            + extracted_whitespace
            + ":"
            + extracted_whitespace_before_info_string,
            position_marker=position_marker,
        )

    # pylint: enable=too-many-arguments


# pylint: enable=too-many-instance-attributes


class AtxHeadingMarkdownToken(MarkdownToken):
    """
    Class to provide for an encapsulation of the atx heading element.
    """

    # pylint: disable=too-many-arguments
    def __init__(
        self, hash_count, remove_trailing_count, extracted_whitespace, position_marker,
    ):
        self.hash_count = hash_count
        self.remove_trailing_count = remove_trailing_count
        self.extracted_whitespace = extracted_whitespace

        MarkdownToken.__init__(
            self,
            MarkdownToken.token_atx_heading,
            MarkdownTokenClass.LEAF_BLOCK,
            str(hash_count)
            + ":"
            + str(remove_trailing_count)
            + ":"
            + extracted_whitespace,
            position_marker=position_marker,
        )

    # pylint: enable=too-many-arguments


class EndMarkdownToken(MarkdownToken):
    """
    Class to provide for an encapsulation of the end element to a matching start.
    """

    type_name_prefix = "end-"

    def __init__(
        self, type_name, extracted_whitespace, extra_end_data, start_markdown_token
    ):

        self.type_name = type_name
        self.extracted_whitespace = extracted_whitespace
        self.extra_end_data = extra_end_data
        self.start_markdown_token = start_markdown_token

        MarkdownToken.__init__(
            self,
            EndMarkdownToken.type_name_prefix + type_name,
            MarkdownTokenClass.INLINE_BLOCK,
            "",
        )
        self.compose_data_field()

    def compose_data_field(self):
        """
        Compose the object's self.extra_data field from the local object's variables.
        """
        display_data = self.extracted_whitespace
        if self.extra_end_data is not None:
            display_data = display_data + ":" + self.extra_end_data
        self.extra_data = display_data


class TextMarkdownToken(MarkdownToken):
    """
    Class to provide for an encapsulation of the text element.
    """

    def __init__(self, token_text, extracted_whitespace, end_whitespace=None):
        self.token_text = token_text
        self.extracted_whitespace = extracted_whitespace
        self.end_whitespace = end_whitespace
        MarkdownToken.__init__(
            self, MarkdownToken.token_text, MarkdownTokenClass.INLINE_BLOCK, ""
        )
        self.compose_extra_data_field()

    def compose_extra_data_field(self):
        """
        Compose the object's self.extra_data field from the local object's variables.
        """

        self.extra_data = self.token_text + ":" + self.extracted_whitespace
        if self.end_whitespace:
            self.extra_data = self.extra_data + ":" + self.end_whitespace

    def remove_final_whitespace(self):
        """
        Remove any final whitespace.  Used by paragraph blocks so that they do not
        end with a hard break.
        """

        removed_whitespace = ""
        (
            collected_whitespace_length,
            first_non_whitespace_index,
        ) = ParserHelper.collect_backwards_while_one_of_characters(
            self.token_text, -1, Constants.whitespace
        )
        if collected_whitespace_length:
            removed_whitespace = self.token_text[
                first_non_whitespace_index : first_non_whitespace_index
                + collected_whitespace_length
            ]
            self.token_text = self.token_text[0:first_non_whitespace_index]
        return removed_whitespace

    def combine(self, other_text_token, remove_leading_spaces):
        """
        Combine the two text tokens together with a line feed between.
        If remove_leading_spaces > 0, then that many leading spaces will be
        removed from each line, if present.
        If remove_leading_spaces == -1, then.
        If remove_leading_spaces == 0, then.
        """

        if other_text_token.is_blank_line:
            text_to_combine = ""
            whitespace_present = other_text_token.extra_data
        else:
            assert other_text_token.is_text
            text_to_combine = other_text_token.token_text
            whitespace_present = other_text_token.extracted_whitespace

        whitespace_to_append = None
        removed_whitespace = ""
        if not remove_leading_spaces:
            prefix_whitespace = whitespace_present
        elif remove_leading_spaces == -1:
            whitespace_to_append = whitespace_present
            prefix_whitespace = ""
        else:
            LOGGER.debug(
                "whitespace_present>>%s>>%s<<",
                str(len(whitespace_present)),
                str(whitespace_present),
            )
            LOGGER.debug("remove_leading_spaces>>%s<<", str(remove_leading_spaces))
            if len(whitespace_present) < remove_leading_spaces:
                removed_whitespace = whitespace_present
                prefix_whitespace = ""
            else:
                removed_whitespace = whitespace_present[0:remove_leading_spaces]
                prefix_whitespace = whitespace_present[remove_leading_spaces:]

        if whitespace_to_append is not None:
            self.extracted_whitespace = (
                self.extracted_whitespace
                + ParserHelper.newline_character
                + whitespace_to_append
            )
        self.token_text = (
            self.token_text
            + ParserHelper.newline_character
            + prefix_whitespace
            + text_to_combine
        )
        self.compose_extra_data_field()
        return removed_whitespace


class SpecialTextMarkdownToken(TextMarkdownToken):
    """
    Class to provide for special tokens that represent exceptional inline elements.
    """

    # pylint: disable=too-many-arguments
    def __init__(
        self, token_text, repeat_count, preceding_two, following_two, is_active=True
    ):
        self.repeat_count = repeat_count
        self.active = is_active
        self.preceding_two = preceding_two
        self.following_two = following_two
        TextMarkdownToken.__init__(self, token_text, "", "")

    # pylint: enable=too-many-arguments

    def reduce_repeat_count(self, emphasis_length):
        """
        Reduce the repeat count by the specified amount.
        """
        self.repeat_count = self.repeat_count - emphasis_length

    def show_process_emphasis(self):
        """
        Independent of the __str__ function, provide extra information.
        """
        return (
            ">>active="
            + str(self.active)
            + ",repeat="
            + str(self.repeat_count)
            + ",preceding='"
            + str(self.preceding_two)
            + "',following='"
            + str(self.following_two)
            + "':"
            + str(self)
        )


# pylint: disable=too-many-instance-attributes
class LinkReferenceDefinitionMarkdownToken(MarkdownToken):
    """
    Class to provide for an encapsulation of the link reference definition element.
    """

    # pylint: disable=too-many-arguments
    def __init__(
        self,
        did_add_definition,
        extracted_whitespace,
        link_name,
        link_value,
        link_debug,
        position_marker,
    ):
        self.did_add_definition = did_add_definition
        self.extracted_whitespace = extracted_whitespace
        self.link_name = link_name

        if link_value:
            self.link_destination = link_value[0]
            self.link_title = link_value[1]
        else:
            self.link_destination = ""
            self.link_title = ""

        if link_debug:
            self.link_name_debug = link_debug[0]
            if self.link_name_debug == self.link_name:
                self.link_name_debug = ""
            self.link_destination_whitespace = link_debug[1]
            self.link_destination_raw = link_debug[2]
            if self.link_destination_raw == self.link_destination:
                self.link_destination_raw = ""
            self.link_title_whitespace = link_debug[3]
            self.link_title_raw = link_debug[4]
            if self.link_title_raw == self.link_title:
                self.link_title_raw = ""
            self.end_whitespace = link_debug[5]
        else:
            self.link_name_debug = ""
            self.link_destination_whitespace = ""
            self.link_destination_raw = ""
            self.link_title_whitespace = ""
            self.link_title_raw = ""
            self.end_whitespace = ""
        extra_data = (
            str(did_add_definition)
            + ":"
            + extracted_whitespace
            + ":"
            + link_name
            + ":"
            + self.link_name_debug
            + ":"
            + self.link_destination_whitespace
            + ":"
            + self.link_destination
            + ":"
            + self.link_destination_raw
            + ":"
            + self.link_title_whitespace
            + ":"
            + self.link_title
            + ":"
            + self.link_title_raw
            + ":"
            + self.end_whitespace
        )
        MarkdownToken.__init__(
            self,
            MarkdownToken.token_link_reference_definition,
            MarkdownTokenClass.LEAF_BLOCK,
            extra_data,
            position_marker=position_marker,
        )

    # pylint: enable=too-many-arguments


# pylint: enable=too-many-instance-attributes


class BlockQuoteMarkdownToken(MarkdownToken):
    """
    Class to provide for an encapsulation of the block quote element.
    """

    def __init__(self, extracted_whitespace, position_marker):
        self.extracted_whitespace = extracted_whitespace
        MarkdownToken.__init__(
            self,
            MarkdownToken.token_block_quote,
            MarkdownTokenClass.CONTAINER_BLOCK,
            extracted_whitespace,
            position_marker=position_marker,
        )


class UnorderedListStartMarkdownToken(MarkdownToken):
    """
    Class to provide for an encapsulation of the unordered list start element.
    """

    def __init__(
        self, list_start_sequence, indent_level, extracted_whitespace, position_marker
    ):
        self.list_start_sequence = list_start_sequence
        self.indent_level = indent_level
        self.is_loose = True
        self.extracted_whitespace = extracted_whitespace
        self.leading_spaces = None
        MarkdownToken.__init__(
            self,
            MarkdownToken.token_unordered_list_start,
            MarkdownTokenClass.CONTAINER_BLOCK,
            "",
            position_marker=position_marker,
        )
        self.compose_extra_data_field()

    def compose_extra_data_field(self):
        """
        Compose the object's self.extra_data field from the local object's variables.
        """

        self.extra_data = (
            self.list_start_sequence
            + "::"
            + str(self.indent_level)
            + ":"
            + self.extracted_whitespace
        )
        if self.leading_spaces is not None:
            self.extra_data += ":" + self.leading_spaces

    def add_leading_spaces(self, ws_add):
        """
        Add any leading spaces to the token, separating them with line feeds.
        """
        if self.leading_spaces is None:
            self.leading_spaces = ws_add
        else:
            self.leading_spaces += ParserHelper.newline_character + ws_add
        self.compose_extra_data_field()


class OrderedListStartMarkdownToken(MarkdownToken):
    """
    Class to provide for an encapsulation of the ordered list start element.
    """

    # pylint: disable=too-many-arguments
    def __init__(
        self,
        list_start_sequence,
        list_start_content,
        indent_level,
        extracted_whitespace,
        position_marker,
    ):
        self.list_start_sequence = list_start_sequence
        self.list_start_content = list_start_content
        self.indent_level = indent_level
        self.is_loose = True
        self.extracted_whitespace = extracted_whitespace
        self.leading_spaces = None
        MarkdownToken.__init__(
            self,
            MarkdownToken.token_ordered_list_start,
            MarkdownTokenClass.CONTAINER_BLOCK,
            "",
            position_marker=position_marker,
        )
        self.compose_extra_data_field()

    # pylint: enable=too-many-arguments

    def compose_extra_data_field(self):
        """
        Compose the object's self.extra_data field from the local object's variables.
        """

        self.extra_data = (
            self.list_start_sequence
            + ":"
            + self.list_start_content
            + ":"
            + str(self.indent_level)
            + ":"
            + self.extracted_whitespace
        )
        if self.leading_spaces is not None:
            self.extra_data += ":" + self.leading_spaces

    def add_leading_spaces(self, ws_add):
        """
        Add any leading spaces to the token, separating them with line feeds.
        """
        if self.leading_spaces is None:
            self.leading_spaces = ws_add
        else:
            self.leading_spaces += ParserHelper.newline_character + ws_add
        self.compose_extra_data_field()


class NewListItemMarkdownToken(MarkdownToken):
    """
    Class to provide for an encapsulation of the new list item element.
    """

    def __init__(self, indent_level, position_marker, extracted_whitespace):
        self.indent_level = indent_level
        self.extracted_whitespace = ""
        MarkdownToken.__init__(
            self,
            MarkdownToken.token_new_list_item,
            MarkdownTokenClass.CONTAINER_BLOCK,
            str(indent_level) + ":" + extracted_whitespace,
            position_marker=position_marker,
        )


class HtmlBlockMarkdownToken(MarkdownToken):
    """
    Class to provide for an encapsulation of the html block element.
    """

    def __init__(self, position_marker, extracted_whitespace):
        extra_indent = len(extracted_whitespace)

        if position_marker:
            line_number = position_marker.line_number
            column_number = (
                position_marker.index_number
                + position_marker.index_indent
                + 1
                - extra_indent
            )
        else:
            line_number = -1
            column_number = -1

        MarkdownToken.__init__(
            self,
            MarkdownToken.token_html_block,
            MarkdownTokenClass.LEAF_BLOCK,
            "",
            line_number=line_number,
            column_number=column_number,
        )


class ThematicBreakMarkdownToken(MarkdownToken):
    """
    Class to provide for an encapsulation of the thematic break element.
    """

    def __init__(
        self, start_character, extracted_whitespace, rest_of_line, position_marker
    ):
        self.extracted_whitespace = extracted_whitespace
        self.rest_of_line = rest_of_line
        MarkdownToken.__init__(
            self,
            MarkdownToken.token_thematic_break,
            MarkdownTokenClass.LEAF_BLOCK,
            start_character + ":" + extracted_whitespace + ":" + rest_of_line,
            position_marker=position_marker,
        )


class InlineCodeSpanMarkdownToken(MarkdownToken):
    """
    Class to provide for an encapsulation of the inline code span element.
    """

    def __init__(
        self,
        span_text,
        extracted_start_backticks,
        leading_whitespace,
        trailing_whitespace,
    ):
        self.span_text = span_text
        self.extracted_start_backticks = extracted_start_backticks
        self.leading_whitespace = leading_whitespace
        self.trailing_whitespace = trailing_whitespace
        MarkdownToken.__init__(
            self,
            MarkdownToken.token_inline_code_span,
            MarkdownTokenClass.INLINE_BLOCK,
            span_text
            + ":"
            + extracted_start_backticks
            + ":"
            + leading_whitespace
            + ":"
            + trailing_whitespace,
        )


class HardBreakMarkdownToken(MarkdownToken):
    """
    Class to provide for an encapsulation of the inline hard line break element.
    """

    def __init__(self, line_end):
        self.line_end = line_end
        MarkdownToken.__init__(
            self,
            MarkdownToken.token_inline_hard_break,
            MarkdownTokenClass.INLINE_BLOCK,
            line_end,
        )


class UriAutolinkMarkdownToken(MarkdownToken):
    """
    Class to provide for an encapsulation of the inline uri autolink element.
    """

    def __init__(self, autolink_text):
        self.autolink_text = autolink_text
        MarkdownToken.__init__(
            self,
            MarkdownToken.token_inline_uri_autolink,
            MarkdownTokenClass.INLINE_BLOCK,
            autolink_text,
        )


# pylint: disable=too-many-instance-attributes
class LinkStartMarkdownToken(MarkdownToken):
    """
    Class to provide for an encapsulation of the link element.
    """

    # pylint: disable=too-many-arguments
    def __init__(
        self,
        link_uri,
        pre_link_uri,
        link_title,
        pre_link_title,
        ex_label,
        label_type,
        text_from_blocks,
        did_use_angle_start,
        inline_title_bounding_character,
        before_link_whitespace,
        before_title_whitespace,
        after_title_whitespace,
    ):
        self.link_uri = link_uri
        self.link_title = link_title
        self.pre_link_uri = pre_link_uri
        self.pre_link_title = pre_link_title
        self.ex_label = ex_label
        self.label_type = label_type
        self.text_from_blocks = text_from_blocks
        self.did_use_angle_start = did_use_angle_start
        self.inline_title_bounding_character = inline_title_bounding_character
        self.before_link_whitespace = before_link_whitespace
        self.before_title_whitespace = before_title_whitespace
        self.after_title_whitespace = after_title_whitespace
        MarkdownToken.__init__(
            self,
            MarkdownToken.token_inline_link,
            MarkdownTokenClass.INLINE_BLOCK,
            label_type
            + ":"
            + link_uri
            + ":"
            + link_title
            + ":"
            + pre_link_uri
            + ":"
            + pre_link_title
            + ":"
            + ex_label
            + ":"
            + text_from_blocks
            + ":"
            + str(did_use_angle_start)
            + ":"
            + inline_title_bounding_character
            + ":"
            + before_link_whitespace
            + ":"
            + before_title_whitespace
            + ":"
            + after_title_whitespace,
        )

    # pylint: enable=too-many-arguments


# pylint: enable=too-many-instance-attributes


# pylint: disable=too-many-instance-attributes
class ImageStartMarkdownToken(MarkdownToken):
    """
    Class to provide for an encapsulation of the image element.
    """

    # pylint: disable=too-many-arguments
    def __init__(
        self,
        image_uri,
        pre_image_uri,
        image_title,
        pre_image_title,
        image_alt_text,
        ex_label,
        label_type,
        text_from_blocks,
        did_use_angle_start,
        inline_title_bounding_character,
        before_link_whitespace,
        before_title_whitespace,
        after_title_whitespace,
    ):
        self.image_uri = image_uri
        self.image_title = image_title
        self.image_alt_text = image_alt_text
        self.pre_image_uri = pre_image_uri
        self.pre_image_title = pre_image_title
        self.ex_label = ex_label
        self.label_type = label_type
        self.text_from_blocks = text_from_blocks
        self.did_use_angle_start = did_use_angle_start
        self.inline_title_bounding_character = inline_title_bounding_character
        self.before_link_whitespace = before_link_whitespace
        self.before_title_whitespace = before_title_whitespace
        self.after_title_whitespace = after_title_whitespace
        MarkdownToken.__init__(
            self,
            MarkdownToken.token_inline_image,
            MarkdownTokenClass.INLINE_BLOCK,
            label_type
            + ":"
            + image_uri
            + ":"
            + image_title
            + ":"
            + image_alt_text
            + ":"
            + pre_image_uri
            + ":"
            + pre_image_title
            + ":"
            + ex_label
            + ":"
            + text_from_blocks
            + ":"
            + str(did_use_angle_start)
            + ":"
            + inline_title_bounding_character
            + ":"
            + before_link_whitespace
            + ":"
            + before_title_whitespace
            + ":"
            + after_title_whitespace,
        )

    # pylint: enable=too-many-arguments


# pylint: enable=too-many-instance-attributes


class EmailAutolinkMarkdownToken(MarkdownToken):
    """
    Class to provide for an encapsulation of the inline email autolink element.
    """

    def __init__(self, autolink_text):
        self.autolink_text = autolink_text
        MarkdownToken.__init__(
            self,
            MarkdownToken.token_inline_email_autolink,
            MarkdownTokenClass.INLINE_BLOCK,
            autolink_text,
        )


class RawHtmlMarkdownToken(MarkdownToken):
    """
    Class to provide for an encapsulation of the inline raw html element.
    """

    def __init__(self, raw_tag):
        self.raw_tag = raw_tag
        MarkdownToken.__init__(
            self,
            MarkdownToken.token_inline_raw_html,
            MarkdownTokenClass.INLINE_BLOCK,
            raw_tag,
        )


class EmphasisMarkdownToken(MarkdownToken):
    """
    Class to provide for an encapsulation of the inline emphasis element.
    """

    def __init__(self, emphasis_length, emphasis_character):
        self.emphasis_length = emphasis_length
        self.emphasis_character = emphasis_character
        MarkdownToken.__init__(
            self,
            MarkdownToken.token_inline_emphasis,
            MarkdownTokenClass.INLINE_BLOCK,
            str(emphasis_length) + ":" + emphasis_character,
        )


# pylint: enable=too-few-public-methods
