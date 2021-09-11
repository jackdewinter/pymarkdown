"""
Module to provide for an inline element that can be added to markdown parsing stream.
"""
import logging

from pymarkdown.constants import Constants
from pymarkdown.markdown_token import MarkdownToken, MarkdownTokenClass
from pymarkdown.parser_helper import ParserHelper
from pymarkdown.parser_logger import ParserLogger

POGGER = ParserLogger(logging.getLogger(__name__))


# pylint: disable=too-many-arguments
class InlineMarkdownToken(MarkdownToken):
    """
    Class to provide for a leaf element that can be added to markdown parsing stream.
    """

    def __init__(
        self,
        token_name,
        extra_data,
        line_number=0,
        column_number=0,
        position_marker=None,
        requires_end_token=False,
        can_force_close=True,
    ):
        MarkdownToken.__init__(
            self,
            token_name,
            MarkdownTokenClass.INLINE_BLOCK,
            extra_data,
            line_number=line_number,
            column_number=column_number,
            position_marker=position_marker,
            can_force_close=can_force_close,
            requires_end_token=requires_end_token,
        )


# pylint: enable=too-many-arguments


class EmphasisMarkdownToken(InlineMarkdownToken):
    """
    Class to provide for an encapsulation of the inline emphasis element.
    """

    def __init__(
        self, emphasis_length, emphasis_character, line_number=0, column_number=0
    ):
        self.__emphasis_length, self.__emphasis_character = (
            emphasis_length,
            emphasis_character,
        )
        InlineMarkdownToken.__init__(
            self,
            MarkdownToken._token_inline_emphasis,
            MarkdownToken.extra_data_separator.join(
                [str(emphasis_length), emphasis_character]
            ),
            line_number=line_number,
            column_number=column_number,
            requires_end_token=True,
            can_force_close=False,
        )

    @property
    def emphasis_length(self):
        """
        Returns the length of the current emphasis text.
        """
        return self.__emphasis_length

    @property
    def emphasis_character(self):
        """
        Returns the character used for the current emphasis text.
        """
        return self.__emphasis_character


class RawHtmlMarkdownToken(InlineMarkdownToken):
    """
    Class to provide for an encapsulation of the inline raw html element.
    """

    def __init__(self, raw_tag, line_number, column_number):
        self.__raw_tag = raw_tag
        InlineMarkdownToken.__init__(
            self,
            MarkdownToken._token_inline_raw_html,
            self.__raw_tag,
            line_number=line_number,
            column_number=column_number,
        )

    @property
    def raw_tag(self):
        """
        Returns the text that is the raw html tag.
        """
        return self.__raw_tag


class EmailAutolinkMarkdownToken(InlineMarkdownToken):
    """
    Class to provide for an encapsulation of the inline email autolink element.
    """

    def __init__(self, autolink_text, line_number, column_number):
        self.__autolink_text = autolink_text
        InlineMarkdownToken.__init__(
            self,
            MarkdownToken._token_inline_email_autolink,
            self.__autolink_text,
            line_number=line_number,
            column_number=column_number,
        )

    @property
    def autolink_text(self):
        """
        Returns the text that is the autolink.
        """
        return self.__autolink_text


class UriAutolinkMarkdownToken(InlineMarkdownToken):
    """
    Class to provide for an encapsulation of the inline uri autolink element.
    """

    def __init__(self, autolink_text, line_number, column_number):
        self.__autolink_text = autolink_text
        InlineMarkdownToken.__init__(
            self,
            MarkdownToken._token_inline_uri_autolink,
            self.__autolink_text,
            line_number=line_number,
            column_number=column_number,
        )

    @property
    def autolink_text(self):
        """
        Returns the text that is the autolink.
        """
        return self.__autolink_text


class InlineCodeSpanMarkdownToken(InlineMarkdownToken):
    """
    Class to provide for an encapsulation of the inline code span element.
    """

    # pylint: disable=too-many-arguments
    def __init__(
        self,
        span_text,
        extracted_start_backticks,
        leading_whitespace,
        trailing_whitespace,
        line_number,
        column_number,
    ):
        (
            self.__span_text,
            self.__extracted_start_backticks,
            self.__leading_whitespace,
            self.__trailing_whitespace,
        ) = (
            span_text,
            extracted_start_backticks,
            leading_whitespace,
            trailing_whitespace,
        )
        InlineMarkdownToken.__init__(
            self,
            MarkdownToken._token_inline_code_span,
            MarkdownToken.extra_data_separator.join(
                [
                    self.__span_text,
                    self.__extracted_start_backticks,
                    self.__leading_whitespace,
                    self.__trailing_whitespace,
                ]
            ),
            line_number=line_number,
            column_number=column_number,
        )

    # pylint: enable=too-many-arguments
    @property
    def span_text(self):
        """
        Returns the text that is within the span.
        """
        return self.__span_text

    @property
    def extracted_start_backticks(self):
        """
        Returns the backticks that started the code span.
        """
        return self.__extracted_start_backticks

    @property
    def leading_whitespace(self):
        """
        Returns the whitespace at the start of the code span.
        """
        return self.__leading_whitespace

    @property
    def trailing_whitespace(self):
        """
        Returns the whitespace at the end of the code span.
        """
        return self.__trailing_whitespace


class HardBreakMarkdownToken(InlineMarkdownToken):
    """
    Class to provide for an encapsulation of the inline hard line break element.
    """

    def __init__(self, line_end, line_number, column_number):
        self.__line_end = line_end
        InlineMarkdownToken.__init__(
            self,
            MarkdownToken._token_inline_hard_break,
            MarkdownToken.extra_data_separator.join(
                [
                    self.__line_end,
                    ParserHelper.newline_character,
                ]
            ),
            line_number=line_number,
            column_number=column_number,
        )

    @property
    def line_end(self):
        """
        Returns the text at the end of the line.
        """
        return self.__line_end


# pylint: disable=too-many-instance-attributes
class ReferenceMarkdownToken(InlineMarkdownToken):
    """
    Base class for images and links.
    """

    # pylint: disable=too-many-arguments, too-many-locals
    def __init__(
        self,
        token_name,
        label_type,
        link_uri,
        link_title,
        extra_data,
        pre_link_uri,
        pre_link_title,
        ex_label,
        text_from_blocks,
        did_use_angle_start,
        inline_title_bounding_character,
        before_link_whitespace,
        before_title_whitespace,
        after_title_whitespace,
        line_number=0,
        column_number=0,
        requires_end_token=False,
        can_force_close=True,
    ):
        (
            self.__label_type,
            self.__link_uri,
            self.__link_title,
            self.__pre_link_uri,
            self.__pre_link_title,
            self.__ex_label,
            self.__text_from_blocks,
            self.__did_use_angle_start,
            self.__inline_title_bounding_character,
            self.__before_link_whitespace,
            self.__before_title_whitespace,
            self.__after_title_whitespace,
        ) = (
            label_type,
            link_uri,
            link_title,
            pre_link_uri,
            pre_link_title,
            ex_label,
            text_from_blocks,
            did_use_angle_start,
            inline_title_bounding_character,
            before_link_whitespace,
            before_title_whitespace,
            after_title_whitespace,
        )

        if token_name == MarkdownToken._token_inline_image:
            extra_data = f"{extra_data}{MarkdownToken.extra_data_separator}"

        # Purposefully split this way to accommodate the extra data
        part_1 = MarkdownToken.extra_data_separator.join(
            [label_type, self.__link_uri, self.__link_title, extra_data]
        )
        part_2 = MarkdownToken.extra_data_separator.join(
            [
                self.__pre_link_uri,
                self.__pre_link_title,
                self.__ex_label,
                self.__text_from_blocks,
                str(self.__did_use_angle_start),
                self.__inline_title_bounding_character,
                self.__before_link_whitespace,
                self.__before_title_whitespace,
                self.__after_title_whitespace,
            ]
        )

        InlineMarkdownToken.__init__(
            self,
            token_name,
            f"{part_1}{part_2}",
            line_number=line_number,
            column_number=column_number,
            requires_end_token=requires_end_token,
            can_force_close=can_force_close,
        )

    # pylint: enable=too-many-arguments, too-many-locals

    @property
    def label_type(self):
        """
        Returns the type of label that was used.
        """
        return self.__label_type

    @property
    def link_uri(self):
        """
        Returns the URI for the link itself.
        """
        return self.__link_uri

    @property
    def active_link_uri(self):
        """
        Returns the active URI for the link, preferring the __pre_link_uri over the __link_uri.
        """
        return self.__pre_link_uri if self.__pre_link_uri else self.__link_uri

    @property
    def link_title(self):
        """
        Returns the text associated with the link's title.
        """
        return self.__link_title

    @property
    def active_link_title(self):
        """
        Returns the active text associated with the link's title, preferring the __pre_link_title over the __link_title.
        """
        return self.__pre_link_title if self.__pre_link_title else self.__link_title

    @property
    def ex_label(self):
        """
        Returns the text extracted from the blocks of the link, after processing.
        """
        return self.__ex_label

    @property
    def text_from_blocks(self):
        """
        Returns the text extracted from the blocks of the link, before processing.
        """
        return self.__text_from_blocks

    @property
    def did_use_angle_start(self):
        """
        Returns a value indicating whether an angle start was used around the URI.
        """
        return self.__did_use_angle_start

    @property
    def inline_title_bounding_character(self):
        """
        Returns the bounding character used for the title.
        """
        return self.__inline_title_bounding_character

    @property
    def before_link_whitespace(self):
        """
        Returns the whitespace extracted before the link.
        """
        return self.__before_link_whitespace

    @property
    def before_title_whitespace(self):
        """
        Returns the whitespace extracted before the title.
        """
        return self.__before_title_whitespace

    @property
    def after_title_whitespace(self):
        """
        Returns the whitespace extracted after the title.
        """
        return self.__after_title_whitespace


# pylint: enable=too-many-instance-attributes


# pylint: disable=too-many-instance-attributes
class LinkStartMarkdownToken(ReferenceMarkdownToken):
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
        line_number,
        column_number,
    ):
        ReferenceMarkdownToken.__init__(
            self,
            MarkdownToken._token_inline_link,
            label_type,
            link_uri,
            link_title,
            "",
            pre_link_uri,
            pre_link_title,
            ex_label,
            text_from_blocks,
            did_use_angle_start,
            inline_title_bounding_character,
            before_link_whitespace,
            before_title_whitespace,
            after_title_whitespace,
            line_number=line_number,
            column_number=column_number,
            requires_end_token=True,
            can_force_close=False,
        )

    # pylint: enable=too-many-arguments


# pylint: enable=too-many-instance-attributes


# pylint: disable=too-many-instance-attributes
class ImageStartMarkdownToken(ReferenceMarkdownToken):
    """
    Class to provide for an encapsulation of the image element.
    """

    # pylint: disable=too-many-arguments, too-many-locals
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
        line_number,
        column_number,
    ):
        self.__image_alt_text = image_alt_text
        ReferenceMarkdownToken.__init__(
            self,
            MarkdownToken._token_inline_image,
            label_type,
            image_uri,
            image_title,
            self.__image_alt_text,
            pre_image_uri,
            pre_image_title,
            ex_label,
            text_from_blocks,
            did_use_angle_start,
            inline_title_bounding_character,
            before_link_whitespace,
            before_title_whitespace,
            after_title_whitespace,
            line_number=line_number,
            column_number=column_number,
        )

    # pylint: enable=too-many-arguments, too-many-locals

    @property
    def image_alt_text(self):
        """
        Returns the text extracted from the blocks of the link, after processing.
        """
        return self.__image_alt_text


# pylint: enable=too-many-instance-attributes


class TextMarkdownToken(InlineMarkdownToken):
    """
    Class to provide for an encapsulation of the text element.
    """

    # pylint: disable=too-many-arguments
    def __init__(
        self,
        token_text,
        extracted_whitespace,
        end_whitespace=None,
        position_marker=None,
        line_number=0,
        column_number=0,
        is_special=False,
    ):
        (
            self.__token_text,
            self.__extracted_whitespace,
            self.__end_whitespace,
            self.__is_special,
        ) = (token_text, extracted_whitespace, end_whitespace, is_special)
        InlineMarkdownToken.__init__(
            self,
            MarkdownToken._token_text,
            "",
            position_marker=position_marker,
            line_number=line_number,
            column_number=column_number,
        )
        self.__compose_extra_data_field()

    # pylint: enable=too-many-arguments

    def _set_token_text(self, new_text):
        self.__token_text = new_text
        self.__compose_extra_data_field()

    @property
    def is_special(self):
        """
        Returns whether the current token is actually a special subclass.

        This resolves issues above the base class being able to have helper
        methods to identify the type of token.
        """
        return self.__is_special

    @property
    def token_text(self):
        """
        Returns the text associated with the token.
        """
        return self.__token_text

    @property
    def extracted_whitespace(self):
        """
        Returns any whitespace that was extracted before the processing of this element occurred.
        """
        return self.__extracted_whitespace

    @property
    def end_whitespace(self):
        """
        Returns any whitespace that was extracted after the processing of this element occurred.
        """
        return self.__end_whitespace

    def create_copy(self):
        """
        Create a copy of this token.
        """
        new_token = TextMarkdownToken(
            self.__token_text,
            self.__extracted_whitespace,
            self.__end_whitespace,
            line_number=self.line_number,
            column_number=self.column_number,
        )
        return new_token

    def __compose_extra_data_field(self):
        """
        Compose the object's self.extra_data field from the local object's variables.
        """

        data_field_parts = [self.__token_text, self.__extracted_whitespace]
        if self.end_whitespace:
            data_field_parts.append(self.__end_whitespace)
        self._set_extra_data(MarkdownToken.extra_data_separator.join(data_field_parts))

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
            self.__token_text, -1, Constants.whitespace
        )
        if collected_whitespace_length:
            removed_whitespace = self.__token_text[
                first_non_whitespace_index : first_non_whitespace_index
                + collected_whitespace_length
            ]
            self.__token_text = self.__token_text[0:first_non_whitespace_index]
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
            text_to_combine, whitespace_present, blank_line_sequence = (
                "",
                other_text_token.extra_data,
                ParserHelper.replace_noop_character,
            )
        else:
            assert other_text_token.is_text
            text_to_combine, whitespace_present, blank_line_sequence = (
                other_text_token.token_text,
                other_text_token.extracted_whitespace,
                "",
            )

        whitespace_to_append, removed_whitespace = None, ""
        if not remove_leading_spaces:
            prefix_whitespace = whitespace_present
        elif remove_leading_spaces == -1:
            whitespace_to_append, prefix_whitespace = whitespace_present, ""
        else:
            whitespace_present_size = len(whitespace_present)
            POGGER.debug(
                "whitespace_present>>$>>$<<",
                whitespace_present_size,
                whitespace_present,
            )
            POGGER.debug("remove_leading_spaces>>$<<", remove_leading_spaces)
            if whitespace_present_size < remove_leading_spaces:
                removed_whitespace, prefix_whitespace = whitespace_present, ""
            else:
                removed_whitespace, prefix_whitespace = (
                    whitespace_present[0:remove_leading_spaces],
                    whitespace_present[remove_leading_spaces:],
                )

        if whitespace_to_append is not None:
            self.__extracted_whitespace = f"{self.__extracted_whitespace}{ParserHelper.newline_character}{whitespace_to_append}"
        self.__token_text = f"{self.__token_text}{ParserHelper.newline_character}{blank_line_sequence}{prefix_whitespace}{text_to_combine}"
        self.__compose_extra_data_field()
        return removed_whitespace


class SpecialTextMarkdownToken(TextMarkdownToken):
    """
    Class to provide for special tokens that represent exceptional inline elements.
    """

    # pylint: disable=too-many-arguments
    def __init__(
        self,
        token_text,
        repeat_count,
        preceding_two,
        following_two,
        is_active=True,
        line_number=0,
        column_number=0,
    ):
        (
            self.__repeat_count,
            self.__is_active,
            self.__preceding_two,
            self.__following_two,
        ) = (repeat_count, is_active, preceding_two, following_two)
        TextMarkdownToken.__init__(
            self,
            token_text,
            "",
            "",
            line_number=line_number,
            column_number=column_number,
            is_special=True,
        )

    # pylint: enable=too-many-arguments

    @property
    def is_active(self):
        """
        Returns a value indicating whether this special text is still active.
        """
        return self.__is_active

    @property
    def repeat_count(self):
        """
        Returns the repeat count for the special text element.
        """
        return self.__repeat_count

    @property
    def preceding_two(self):
        """
        Returns the preceding two characters before this token.
        """
        return self.__preceding_two

    @property
    def following_two(self):
        """
        Returns the following two characters before this token.
        """
        return self.__following_two

    def deactivate(self):
        """
        Mark this special token as deactivated.
        """
        self.__is_active = False

    def adjust_token_text_by_repeat_count(self):
        """
        Adjust the token's text by the repeat count.
        """
        self._set_token_text(self.token_text[0 : self.repeat_count])

    def reduce_repeat_count(self, emphasis_length, adjust_column_number=False):
        """
        Reduce the repeat count by the specified amount.
        """
        self.__repeat_count -= emphasis_length
        if adjust_column_number:
            self._set_column_number(self.column_number + emphasis_length)

    def show_process_emphasis(self):
        """
        Independent of the __str__ function, provide extra information.
        """
        return f">>active={str(self.__is_active)},repeat={str(self.__repeat_count)},preceding='{str(self.__preceding_two)}',following='{str(self.__following_two)}':{str(self)}"
