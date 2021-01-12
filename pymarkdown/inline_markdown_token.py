"""
Module to provide for an inline element that can be added to markdown parsing stream.
"""
import logging

from pymarkdown.constants import Constants
from pymarkdown.markdown_token import MarkdownToken, MarkdownTokenClass
from pymarkdown.parser_helper import ParserHelper

LOGGER = logging.getLogger(__name__)


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
    ):
        MarkdownToken.__init__(
            self,
            token_name,
            MarkdownTokenClass.INLINE_BLOCK,
            extra_data,
            line_number=line_number,
            column_number=column_number,
            position_marker=position_marker,
        )


# pylint: enable=too-many-arguments


class EmphasisMarkdownToken(InlineMarkdownToken):
    """
    Class to provide for an encapsulation of the inline emphasis element.
    """

    def __init__(
        self, emphasis_length, emphasis_character, line_number=0, column_number=0
    ):
        self.__emphasis_length = emphasis_length
        self.__emphasis_character = emphasis_character
        InlineMarkdownToken.__init__(
            self,
            MarkdownToken._token_inline_emphasis,
            str(emphasis_length) + MarkdownToken.extra_data_separator + emphasis_character,
            line_number=line_number,
            column_number=column_number,
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
        self.__span_text = span_text
        self.__extracted_start_backticks = extracted_start_backticks
        self.__leading_whitespace = leading_whitespace
        self.__trailing_whitespace = trailing_whitespace
        InlineMarkdownToken.__init__(
            self,
            MarkdownToken._token_inline_code_span,
            self.__span_text
            + MarkdownToken.extra_data_separator
            + self.__extracted_start_backticks
            + MarkdownToken.extra_data_separator
            + self.__leading_whitespace
            + MarkdownToken.extra_data_separator
            + self.__trailing_whitespace,
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
            self.__line_end,
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
class LinkStartMarkdownToken(InlineMarkdownToken):
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
        self.__link_uri = link_uri
        self.__link_title = link_title
        self.__pre_link_uri = pre_link_uri
        self.__pre_link_title = pre_link_title
        self.__ex_label = ex_label
        self.__label_type = label_type
        self.__text_from_blocks = text_from_blocks
        self.__did_use_angle_start = did_use_angle_start
        self.__inline_title_bounding_character = inline_title_bounding_character
        self.__before_link_whitespace = before_link_whitespace
        self.__before_title_whitespace = before_title_whitespace
        self.__after_title_whitespace = after_title_whitespace
        InlineMarkdownToken.__init__(
            self,
            MarkdownToken._token_inline_link,
            self.__label_type
            + MarkdownToken.extra_data_separator
            + self.__link_uri
            + MarkdownToken.extra_data_separator
            + self.__link_title
            + MarkdownToken.extra_data_separator
            + self.__pre_link_uri
            + MarkdownToken.extra_data_separator
            + self.__pre_link_title
            + MarkdownToken.extra_data_separator
            + self.__ex_label
            + MarkdownToken.extra_data_separator
            + self.__text_from_blocks
            + MarkdownToken.extra_data_separator
            + str(self.__did_use_angle_start)
            + MarkdownToken.extra_data_separator
            + self.__inline_title_bounding_character
            + MarkdownToken.extra_data_separator
            + self.__before_link_whitespace
            + MarkdownToken.extra_data_separator
            + self.__before_title_whitespace
            + MarkdownToken.extra_data_separator
            + self.__after_title_whitespace,
            line_number=line_number,
            column_number=column_number,
        )

    # pylint: enable=too-many-arguments
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
    def pre_link_uri(self):
        """
        Returns the URI for the link itself, before any mods.
        """
        return self.__pre_link_uri

    @property
    def link_title(self):
        """
        Returns the text associated with the link's title.
        """
        return self.__link_title

    @property
    def pre_link_title(self):
        """
        Returns the text associated with the link's title, before any mods.
        """
        return self.__pre_link_title

    @property
    def text_from_blocks(self):
        """
        Returns the text extracted from the blocks of the link, before processing.
        """
        return self.__text_from_blocks

    @property
    def ex_label(self):
        """
        Returns the text extracted from the blocks of the link, after processing.
        """
        return self.__ex_label

    @property
    def after_title_whitespace(self):
        """
        Returns the whitespace extracted after the title.
        """
        return self.__after_title_whitespace

    @property
    def before_title_whitespace(self):
        """
        Returns the whitespace extracted before the title.
        """
        return self.__before_title_whitespace

    @property
    def before_link_whitespace(self):
        """
        Returns the whitespace extracted before the link.
        """
        return self.__before_link_whitespace

    @property
    def inline_title_bounding_character(self):
        """
        Returns the bounding character used for the title.
        """
        return self.__inline_title_bounding_character

    @property
    def did_use_angle_start(self):
        """
        Returns a value indicating whether an angle start was used around the URI.
        """
        return self.__did_use_angle_start


# pylint: enable=too-many-instance-attributes


# pylint: disable=too-many-instance-attributes
class ImageStartMarkdownToken(InlineMarkdownToken):
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
        self.__image_uri = image_uri
        self.__image_title = image_title
        self.__image_alt_text = image_alt_text
        self.__pre_image_uri = pre_image_uri
        self.__pre_image_title = pre_image_title
        self.__ex_label = ex_label
        self.__label_type = label_type
        self.__text_from_blocks = text_from_blocks
        self.__did_use_angle_start = did_use_angle_start
        self.__inline_title_bounding_character = inline_title_bounding_character
        self.__before_link_whitespace = before_link_whitespace
        self.__before_title_whitespace = before_title_whitespace
        self.__after_title_whitespace = after_title_whitespace
        InlineMarkdownToken.__init__(
            self,
            MarkdownToken._token_inline_image,
            self.__label_type
            + MarkdownToken.extra_data_separator
            + self.__image_uri
            + MarkdownToken.extra_data_separator
            + self.__image_title
            + MarkdownToken.extra_data_separator
            + self.__image_alt_text
            + MarkdownToken.extra_data_separator
            + self.__pre_image_uri
            + MarkdownToken.extra_data_separator
            + self.__pre_image_title
            + MarkdownToken.extra_data_separator
            + self.__ex_label
            + MarkdownToken.extra_data_separator
            + self.__text_from_blocks
            + MarkdownToken.extra_data_separator
            + str(self.__did_use_angle_start)
            + MarkdownToken.extra_data_separator
            + self.__inline_title_bounding_character
            + MarkdownToken.extra_data_separator
            + self.__before_link_whitespace
            + MarkdownToken.extra_data_separator
            + self.__before_title_whitespace
            + MarkdownToken.extra_data_separator
            + self.__after_title_whitespace,
            line_number=line_number,
            column_number=column_number,
        )

    # pylint: enable=too-many-arguments, too-many-locals

    @property
    def label_type(self):
        """
        Returns the type of label that was used.
        """
        return self.__label_type

    @property
    def image_uri(self):
        """
        Returns the URI for the image itself.
        """
        return self.__image_uri

    @property
    def pre_image_uri(self):
        """
        Returns the URI for the image itself, before any mods.
        """
        return self.__pre_image_uri

    @property
    def image_title(self):
        """
        Returns the text associated with the image's title.
        """
        return self.__image_title

    @property
    def pre_image_title(self):
        """
        Returns the text associated with the image's title, before any mods.
        """
        return self.__pre_image_title

    @property
    def text_from_blocks(self):
        """
        Returns the text extracted from the blocks of the link, before processing.
        """
        return self.__text_from_blocks

    @property
    def ex_label(self):
        """
        Returns the text extracted from the blocks of the link, after processing.
        """
        return self.__ex_label

    @property
    def image_alt_text(self):
        """
        Returns the text extracted from the blocks of the link, after processing.
        """
        return self.__image_alt_text

    @property
    def after_title_whitespace(self):
        """
        Returns the whitespace extracted after the title.
        """
        return self.__after_title_whitespace

    @property
    def before_title_whitespace(self):
        """
        Returns the whitespace extracted before the title.
        """
        return self.__before_title_whitespace

    @property
    def before_link_whitespace(self):
        """
        Returns the whitespace extracted before the link.
        """
        return self.__before_link_whitespace

    @property
    def inline_title_bounding_character(self):
        """
        Returns the bounding character used for the title.
        """
        return self.__inline_title_bounding_character

    @property
    def did_use_angle_start(self):
        """
        Returns a value indicating whether an angle start was used around the URI.
        """
        return self.__did_use_angle_start


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
        self.__token_text = token_text
        self.__extracted_whitespace = extracted_whitespace
        self.__end_whitespace = end_whitespace
        self.__is_special = is_special
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

        new_extra_data = self.__token_text + MarkdownToken.extra_data_separator + self.__extracted_whitespace
        if self.end_whitespace:
            new_extra_data += MarkdownToken.extra_data_separator + self.__end_whitespace
        self._set_extra_data(new_extra_data)

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

        blank_line_sequence = ""
        if other_text_token.is_blank_line:
            text_to_combine = ""
            whitespace_present = other_text_token.extra_data
            blank_line_sequence = ParserHelper.replace_noop_character
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
            self.__extracted_whitespace += (
                ParserHelper.newline_character + whitespace_to_append
            )
        self.__token_text += (
            ParserHelper.newline_character
            + blank_line_sequence
            + prefix_whitespace
            + text_to_combine
        )
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
        self.__repeat_count = repeat_count
        self.__is_active = is_active
        self.__preceding_two = preceding_two
        self.__following_two = following_two
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
        Returns the preceeding two characters before this token.
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
        return (
            ">>active="
            + str(self.__is_active)
            + ",repeat="
            + str(self.__repeat_count)
            + ",preceding='"
            + str(self.__preceding_two)
            + "',following='"
            + str(self.__following_two)
            + "':"
            + str(self)
        )
