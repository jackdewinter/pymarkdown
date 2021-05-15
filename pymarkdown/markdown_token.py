"""
Module to provide for an element that can be added to markdown parsing stream.
"""
from enum import Enum


class MarkdownTokenClass(Enum):
    """
    Enumeration to provide guidance on what class of token the token is.
    """

    CONTAINER_BLOCK = 0
    LEAF_BLOCK = 1
    INLINE_BLOCK = 2
    SPECIAL = 3


# pylint: disable=too-many-public-methods,too-many-instance-attributes
class MarkdownToken:
    """
    Class to provide for a base encapsulation of the markdown tokens.
    """

    extra_data_separator = ":"

    _end_token_prefix = "end-"
    _token_pragma = "pragma"

    _token_paragraph = "para"
    _token_blank_line = "BLANK"
    _token_atx_heading = "atx"
    _token_setext_heading = "setext"
    _token_thematic_break = "tbreak"
    _token_link_reference_definition = "link-ref-def"
    _token_html_block = "html-block"
    _token_fenced_code_block = "fcode-block"
    _token_indented_code_block = "icode-block"
    _token_block_quote = "block-quote"
    _token_text = "text"
    _token_front_matter = "front-matter"

    _token_unordered_list_start = "ulist"
    _token_ordered_list_start = "olist"
    _token_new_list_item = "li"

    _token_inline_code_span = "icode-span"
    _token_inline_hard_break = "hard-break"
    _token_inline_uri_autolink = "uri-autolink"
    _token_inline_email_autolink = "email-autolink"
    _token_inline_raw_html = "raw-html"
    _token_inline_emphasis = "emphasis"
    _token_inline_link = "link"
    _token_inline_image = "image"

    # pylint: disable=too-many-arguments
    def __init__(
        self,
        token_name,
        token_class,
        extra_data=None,
        line_number=0,
        column_number=0,
        position_marker=None,
        is_extension=False,
        can_force_close=True,
        requires_end_token=False,
    ):
        if position_marker:
            line_number, column_number = (
                position_marker.line_number,
                position_marker.index_number + position_marker.index_indent + 1,
            )
        (
            self.__token_name,
            self.__token_class,
            self.__extra_data,
            self.__line_number,
            self.__column_number,
            self.__is_extension,
            self.__requires_end_token,
            self.__can_force_close,
        ) = (
            token_name,
            token_class,
            extra_data,
            line_number,
            column_number,
            is_extension,
            requires_end_token,
            can_force_close,
        )

    # pylint: enable=too-many-arguments

    def __str__(self):
        return self.debug_string()

    def debug_string(self, include_column_row_info=True):
        """
        More customizable version of __str__ that allows for options.
        """
        debug_parts = ["[", self.token_name]
        if include_column_row_info and (self.line_number or self.column_number):
            debug_parts.append(f"({self.line_number},{self.column_number})")
        if self.extra_data or self.is_paragraph or self.is_blank_line:
            debug_parts.append(f":{self.extra_data}")
        debug_parts.append("]")
        return "".join(debug_parts)

    def __repr__(self):
        return f"'{self.__str__()}'"

    @property
    def token_name(self):
        """
        Returns the name associated with the token.
        """
        return self.__token_name

    @property
    def is_container(self):
        """
        Returns whether the current token is a container block element.
        """
        return self.__token_class == MarkdownTokenClass.CONTAINER_BLOCK

    @property
    def is_leaf(self):
        """
        Returns whether the current token is a leaf block element.
        """
        return self.__token_class == MarkdownTokenClass.LEAF_BLOCK

    @property
    def is_inline(self):
        """
        Returns whether the current token is an inline block element.
        """
        return self.__token_class == MarkdownTokenClass.INLINE_BLOCK

    @property
    def extra_data(self):
        """
        Returns the extra data associated with the token.
        """
        return self.__extra_data

    def _set_extra_data(self, extra_data):
        self.__extra_data = extra_data

    @property
    def line_number(self):
        """
        Returns the line number associated with the token.
        """
        return self.__line_number

    @property
    def column_number(self):
        """
        Returns the column number associated with the token.
        """
        return self.__column_number

    def _set_column_number(self, column_number):
        self.__column_number = column_number

    @property
    def is_extension(self):
        """
        Returns whether this token is implemented as an extension.
        """
        return self.__is_extension

    @property
    def requires_end_token(self):
        """
        Returns whether this token requires an end token to complete it.
        """
        return self.__requires_end_token

    @property
    def can_force_close(self):
        """
        Returns whether this token can be forceably closed.
        """
        return self.__can_force_close

    @property
    def is_end_token(self):
        """
        Returns whether the current token is an end element.
        """
        return self.token_name.startswith(MarkdownToken._end_token_prefix)

    @property
    def is_block(self):
        """
        Returns whether the current token is one of the block tokens.
        """
        return (
            self.is_block_quote_start
            or self.is_list_start
            or self.is_thematic_break
            or self.is_atx_heading
            or self.is_setext_heading
            or self.is_code_block
            or self.is_html_block
            or self.is_paragraph
        )
        # or tables

    @property
    def is_pragma(self):
        """
        Returns whether the current token is the pragma element.
        """
        return self.token_name == MarkdownToken._token_pragma

    @property
    def is_blank_line(self):
        """
        Returns whether the current token is the blank line element.
        """
        return self.token_name == MarkdownToken._token_blank_line

    @property
    def is_block_quote_start(self):
        """
        Returns whether the current token is a block quote.
        """
        return self.token_name == MarkdownToken._token_block_quote

    @property
    def is_block_quote_end(self):
        """
        Returns whether the current token is a block quote.
        """
        return (
            self.token_name
            == MarkdownToken._end_token_prefix + MarkdownToken._token_block_quote
        )

    @property
    def is_list_start(self):
        """
        Returns whether the current token is a list element.
        """
        return self.is_unordered_list_start or self.is_ordered_list_start

    @property
    def is_list_end(self):
        """
        Returns whether the current token is a list end element.
        """
        return self.is_unordered_list_end or self.is_ordered_list_end

    @property
    def is_unordered_list_start(self):
        """
        Returns whether the current token is a unordered list element.
        """
        return self.token_name == MarkdownToken._token_unordered_list_start

    @property
    def is_ordered_list_start(self):
        """
        Returns whether the current token is a ordered list element.
        """
        return self.token_name == MarkdownToken._token_ordered_list_start

    @property
    def is_unordered_list_end(self):
        """
        Returns whether the current token is a unordered list end element.
        """
        return (
            self.token_name
            == MarkdownToken._end_token_prefix
            + MarkdownToken._token_unordered_list_start
        )

    @property
    def is_ordered_list_end(self):
        """
        Returns whether the current token is a ordered list end element.
        """
        return (
            self.token_name
            == MarkdownToken._end_token_prefix + MarkdownToken._token_ordered_list_start
        )

    @property
    def is_new_list_item(self):
        """
        Returns whether the current token is a list item element.
        """
        return self.token_name == MarkdownToken._token_new_list_item

    @property
    def is_any_list_token(self):
        """
        Returns whether the current token is a list item element or a list element.
        """
        return self.is_new_list_item or self.is_list_start

    @property
    def is_paragraph(self):
        """
        Returns whether the current token is a paragraph element.
        """
        return self.token_name == MarkdownToken._token_paragraph

    @property
    def is_paragraph_end(self):
        """
        Returns whether the current token is a paragraph end element.
        """
        return (
            self.token_name
            == MarkdownToken._end_token_prefix + MarkdownToken._token_paragraph
        )

    @property
    def is_thematic_break(self):
        """
        Returns whether the current token is a thematic break element.
        """
        return self.token_name == MarkdownToken._token_thematic_break

    @property
    def is_front_matter(self):
        """
        Returns whether the current token is the front matter element.
        """
        return self.token_name == MarkdownToken._token_front_matter

    @property
    def is_text(self):
        """
        Returns whether the current token is a text element.
        """
        return self.token_name == MarkdownToken._token_text

    # pylint: disable=no-member
    @property
    def is_special_text(self):
        """
        Returns whether the current token is a special text element.
        """
        return self.is_text and self.is_special

    # pylint: enable=no-member

    @property
    def is_setext_heading(self):
        """
        Returns whether the current token is a setext heading element.
        """
        return self.token_name == MarkdownToken._token_setext_heading

    @property
    def is_setext_heading_end(self):
        """
        Returns whether the current token is a setext heading end element.
        """
        return (
            self.token_name
            == MarkdownToken._end_token_prefix + MarkdownToken._token_setext_heading
        )

    @property
    def is_atx_heading(self):
        """
        Returns whether the current token is an atx element.
        """
        return self.token_name == MarkdownToken._token_atx_heading

    @property
    def is_atx_heading_end(self):
        """
        Returns whether the current token is an atx heading end element.
        """
        return (
            self.token_name
            == MarkdownToken._end_token_prefix + MarkdownToken._token_atx_heading
        )

    @property
    def is_code_block(self):
        """
        Returns whether the current token is a code block element.
        """
        return self.is_indented_code_block or self.is_fenced_code_block

    @property
    def is_indented_code_block(self):
        """
        Returns whether the current token is an indented code block element.
        """
        return self.token_name == MarkdownToken._token_indented_code_block

    @property
    def is_indented_code_block_end(self):
        """
        Returns whether the current token is an indented code block end element.
        """
        return (
            self.token_name
            == MarkdownToken._end_token_prefix
            + MarkdownToken._token_indented_code_block
        )

    @property
    def is_fenced_code_block(self):
        """
        Returns whether the current token is a fenced code block element.
        """
        return self.token_name == MarkdownToken._token_fenced_code_block

    @property
    def is_fenced_code_block_end(self):
        """
        Returns whether the current token is a fenced code block element.
        """
        return (
            self.token_name
            == MarkdownToken._end_token_prefix + MarkdownToken._token_fenced_code_block
        )

    @property
    def is_link_reference_definition(self):
        """
        Returns whether the current token is a link reference definition element.
        """
        return self.token_name == MarkdownToken._token_link_reference_definition

    @property
    def is_html_block(self):
        """
        Returns whether the current token is a html block element.
        """
        return self.token_name == MarkdownToken._token_html_block

    @property
    def is_html_block_end(self):
        """
        Returns whether the current token is a html block element.
        """
        return (
            self.token_name
            == MarkdownToken._end_token_prefix + MarkdownToken._token_html_block
        )

    @property
    def is_inline_code_span(self):
        """
        Returns whether the current token is a code span element.
        """
        return self.token_name == MarkdownToken._token_inline_code_span

    @property
    def is_inline_hard_break(self):
        """
        Returns whether the current token is a hard break element.
        """
        return self.token_name == MarkdownToken._token_inline_hard_break

    @property
    def is_inline_autolink(self):
        """
        Returns whether the current token is an uri autolink or an email autolink element.
        """
        return self.is_inline_uri_autolink or self.is_inline_email_autolink

    @property
    def is_inline_uri_autolink(self):
        """
        Returns whether the current token is an uri autolink element.
        """
        return self.token_name == MarkdownToken._token_inline_uri_autolink

    @property
    def is_inline_email_autolink(self):
        """
        Returns whether the current token is an email autolink element.
        """
        return self.token_name == MarkdownToken._token_inline_email_autolink

    @property
    def is_inline_raw_html(self):
        """
        Returns whether the current token is an email autolink element.
        """
        return self.token_name == MarkdownToken._token_inline_raw_html

    @property
    def is_inline_emphasis(self):
        """
        Returns whether the current token is an emphasis element.
        """
        return self.token_name == MarkdownToken._token_inline_emphasis

    @property
    def is_inline_emphasis_end(self):
        """
        Returns whether the current token is an emphasis end element.
        """
        return (
            self.token_name
            == MarkdownToken._end_token_prefix + MarkdownToken._token_inline_emphasis
        )

    @property
    def is_inline_link(self):
        """
        Returns whether the current token is a link element.
        """
        return self.token_name == MarkdownToken._token_inline_link

    @property
    def is_inline_link_end(self):
        """
        Returns whether the current token is a link end element.
        """
        return (
            self.token_name
            == MarkdownToken._end_token_prefix + MarkdownToken._token_inline_link
        )

    @property
    def is_inline_image(self):
        """
        Returns whether the current token is an image element.
        """
        return self.token_name == MarkdownToken._token_inline_image

    # pylint: disable=too-many-arguments
    def generate_close_markdown_token_from_markdown_token(
        self,
        extracted_whitespace,
        extra_end_data,
        was_forced,
        line_number=0,
        column_number=0,
    ):
        """
        Generate the token emitted to close off the current stack token
        """
        return EndMarkdownToken(
            self.token_name,
            extracted_whitespace,
            extra_end_data,
            self,
            was_forced,
            line_number=line_number,
            column_number=column_number,
        )

    # pylint: enable=too-many-arguments


# pylint: enable=too-many-public-methods,too-many-instance-attributes


class EndMarkdownToken(MarkdownToken):
    """
    Class to provide for an encapsulation of the end element to a matching start.
    """

    # pylint: disable=too-many-arguments
    def __init__(
        self,
        type_name,
        extracted_whitespace,
        extra_end_data,
        start_markdown_token,
        was_forced,
        line_number=0,
        column_number=0,
    ):
        assert start_markdown_token
        if isinstance(start_markdown_token, MarkdownToken):
            assert (
                start_markdown_token.requires_end_token
            ), f"Token '{start_markdown_token} does not require end token."
            if not start_markdown_token.can_force_close:
                assert (
                    not was_forced
                ), f"Token '{start_markdown_token}'s end token cannot be forced."
        (
            self.__type_name,
            self.__extracted_whitespace,
            self.__extra_end_data,
            self.__start_markdown_token,
            self.__was_forced,
        ) = (
            type_name,
            extracted_whitespace,
            extra_end_data,
            start_markdown_token,
            was_forced,
        )

        MarkdownToken.__init__(
            self,
            f"{MarkdownToken._end_token_prefix}{type_name}",
            MarkdownTokenClass.INLINE_BLOCK,
            "",
            line_number=line_number,
            column_number=column_number,
        )
        self.__compose_data_field()

    # pylint: enable=too-many-arguments

    @property
    def type_name(self):
        """
        Returns the type of markdown element related to this end element.
        """
        return self.__type_name

    @property
    def extracted_whitespace(self):
        """
        Returns any whitespace that was extracted before the processing of this element occurred.
        """
        return self.__extracted_whitespace

    @property
    def extra_end_data(self):
        """
        Returns any extra data specificially tied to the end element.
        """
        return self.__extra_end_data

    @property
    def start_markdown_token(self):
        """
        Returns the start markdown token that this end token is the end for.
        """
        return self.__start_markdown_token

    @property
    def was_forced(self):
        """
        Returns a value indicating whether the end element was forced.
        """
        return self.__was_forced

    def __compose_data_field(self):
        """
        Compose the object's self.extra_data field from the local object's variables.
        """
        field_parts = []
        if self.extra_end_data is not None:
            field_parts.append(self.extracted_whitespace)
        else:
            field_parts.append("")
        if self.extra_end_data is not None:
            field_parts.append(self.extra_end_data)
        else:
            field_parts.append("")
        if (
            isinstance(self.__start_markdown_token, MarkdownToken)
            and self.__start_markdown_token.can_force_close
        ):
            field_parts.append(str(self.was_forced))

        self._set_extra_data(MarkdownToken.extra_data_separator.join(field_parts))
