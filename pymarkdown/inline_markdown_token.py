"""
Module to provide for an inline element that can be added to markdown parsing stream.
"""
import logging
from typing import Optional, Tuple, cast

from pymarkdown.constants import Constants
from pymarkdown.links.link_helper_properties import LinkHelperProperties
from pymarkdown.markdown_token import MarkdownToken, MarkdownTokenClass
from pymarkdown.parser_helper import ParserHelper
from pymarkdown.parser_logger import ParserLogger
from pymarkdown.position_marker import PositionMarker

POGGER = ParserLogger(logging.getLogger(__name__))


# pylint: disable=too-many-arguments
class InlineMarkdownToken(MarkdownToken):
    """
    Class to provide for a leaf element that can be added to markdown parsing stream.
    """

    def __init__(
        self,
        token_name: str,
        extra_data: Optional[str],
        line_number: int = 0,
        column_number: int = 0,
        position_marker: Optional[PositionMarker] = None,
        requires_end_token: bool = False,
        can_force_close: bool = True,
        is_special: bool = False,
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
            is_special=is_special,
        )


# pylint: enable=too-many-arguments


class EmphasisMarkdownToken(InlineMarkdownToken):
    """
    Class to provide for an encapsulation of the inline emphasis element.
    """

    def __init__(
        self,
        emphasis_length: int,
        emphasis_character: str,
        line_number: int = 0,
        column_number: int = 0,
    ) -> None:
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
    def emphasis_length(self) -> int:
        """
        Returns the length of the current emphasis text.
        """
        return self.__emphasis_length

    @property
    def emphasis_character(self) -> str:
        """
        Returns the character used for the current emphasis text.
        """
        return self.__emphasis_character


class RawHtmlMarkdownToken(InlineMarkdownToken):
    """
    Class to provide for an encapsulation of the inline raw html element.
    """

    def __init__(self, raw_tag: str, line_number: int, column_number: int) -> None:
        self.__raw_tag = raw_tag
        InlineMarkdownToken.__init__(
            self,
            MarkdownToken._token_inline_raw_html,
            self.__raw_tag,
            line_number=line_number,
            column_number=column_number,
        )

    @property
    def raw_tag(self) -> str:
        """
        Returns the text that is the raw html tag.
        """
        return self.__raw_tag


class EmailAutolinkMarkdownToken(InlineMarkdownToken):
    """
    Class to provide for an encapsulation of the inline email autolink element.
    """

    def __init__(
        self, autolink_text: str, line_number: int, column_number: int
    ) -> None:
        self.__autolink_text = autolink_text
        InlineMarkdownToken.__init__(
            self,
            MarkdownToken._token_inline_email_autolink,
            self.__autolink_text,
            line_number=line_number,
            column_number=column_number,
        )

    @property
    def autolink_text(self) -> str:
        """
        Returns the text that is the autolink.
        """
        return self.__autolink_text


class UriAutolinkMarkdownToken(InlineMarkdownToken):
    """
    Class to provide for an encapsulation of the inline uri autolink element.
    """

    def __init__(
        self, autolink_text: str, line_number: int, column_number: int
    ) -> None:
        self.__autolink_text = autolink_text
        InlineMarkdownToken.__init__(
            self,
            MarkdownToken._token_inline_uri_autolink,
            self.__autolink_text,
            line_number=line_number,
            column_number=column_number,
        )

    @property
    def autolink_text(self) -> str:
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
        span_text: str,
        extracted_start_backticks: str,
        leading_whitespace: str,
        trailing_whitespace: str,
        line_number: int,
        column_number: int,
    ) -> None:
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
    def span_text(self) -> str:
        """
        Returns the text that is within the span.
        """
        return self.__span_text

    @property
    def extracted_start_backticks(self) -> str:
        """
        Returns the backticks that started the code span.
        """
        return self.__extracted_start_backticks

    @property
    def leading_whitespace(self) -> str:
        """
        Returns the whitespace at the start of the code span.
        """
        return self.__leading_whitespace

    @property
    def trailing_whitespace(self) -> str:
        """
        Returns the whitespace at the end of the code span.
        """
        return self.__trailing_whitespace


class HardBreakMarkdownToken(InlineMarkdownToken):
    """
    Class to provide for an encapsulation of the inline hard line break element.
    """

    def __init__(self, line_end: str, line_number: int, column_number: int) -> None:
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
    def line_end(self) -> str:
        """
        Returns the text at the end of the line.
        """
        return self.__line_end


# pylint: disable=too-many-instance-attributes
class ReferenceMarkdownToken(InlineMarkdownToken):
    """
    Base class for images and links.
    """

    # pylint: disable=too-many-arguments
    def __init__(
        self,
        lhp: LinkHelperProperties,
        token_name: str,
        extra_data: Optional[str],
        text_from_blocks: str,
        line_number: int = 0,
        column_number: int = 0,
        requires_end_token: bool = False,
        can_force_close: bool = True,
    ):
        assert lhp.inline_link is not None
        assert lhp.label_type is not None
        assert lhp.pre_inline_link is not None
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
            lhp.label_type,
            lhp.inline_link,
            lhp.inline_title,
            lhp.pre_inline_link,
            lhp.pre_inline_title,
            lhp.ex_label,
            text_from_blocks,
            lhp.did_use_angle_start,
            lhp.bounding_character,
            lhp.before_link_whitespace,
            lhp.before_title_whitespace,
            lhp.after_title_whitespace,
        )

        if token_name == MarkdownToken._token_inline_image:
            extra_data = f"{extra_data}{MarkdownToken.extra_data_separator}"

        # Purposefully split this way to accommodate the extra data
        part_1, part_2 = self.__build_extra_data(extra_data, lhp.label_type)

        InlineMarkdownToken.__init__(
            self,
            token_name,
            f"{part_1}{part_2}",
            line_number=line_number,
            column_number=column_number,
            requires_end_token=requires_end_token,
            can_force_close=can_force_close,
        )

    # pylint: enable=too-many-arguments

    def __build_extra_data(
        self, extra_data: Optional[str], label_type: str
    ) -> Tuple[str, str]:
        assert self.__link_title is not None
        assert extra_data is not None
        part_1 = MarkdownToken.extra_data_separator.join(
            [label_type, self.__link_uri, self.__link_title, extra_data]
        )
        assert self.__inline_title_bounding_character is not None
        assert self.__before_link_whitespace is not None
        assert self.__before_title_whitespace is not None
        assert self.__after_title_whitespace is not None
        assert self.__pre_link_title is not None
        assert self.__ex_label is not None
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
        return part_1, part_2

    @property
    def label_type(self) -> str:
        """
        Returns the type of label that was used.
        """
        return self.__label_type

    @property
    def link_uri(self) -> str:
        """
        Returns the URI for the link itself.
        """
        return self.__link_uri

    @property
    def active_link_uri(self) -> str:
        """
        Returns the active URI for the link, preferring the __pre_link_uri over the __link_uri.
        """
        return self.__pre_link_uri or self.__link_uri

    @property
    def link_title(self) -> Optional[str]:
        """
        Returns the text associated with the link's title.
        """
        return self.__link_title

    @property
    def active_link_title(self) -> Optional[str]:
        """
        Returns the active text associated with the link's title, preferring the __pre_link_title over the __link_title.
        """
        return self.__pre_link_title or self.__link_title

    @property
    def ex_label(self) -> Optional[str]:
        """
        Returns the text extracted from the blocks of the link, after processing.
        """
        return self.__ex_label

    @property
    def text_from_blocks(self) -> str:
        """
        Returns the text extracted from the blocks of the link, before processing.
        """
        return self.__text_from_blocks

    @property
    def did_use_angle_start(self) -> Optional[bool]:
        """
        Returns a value indicating whether an angle start was used around the URI.
        """
        return self.__did_use_angle_start

    @property
    def inline_title_bounding_character(self) -> Optional[str]:
        """
        Returns the bounding character used for the title.
        """
        return self.__inline_title_bounding_character

    @property
    def before_link_whitespace(self) -> Optional[str]:
        """
        Returns the whitespace extracted before the link.
        """
        return self.__before_link_whitespace

    @property
    def before_title_whitespace(self) -> Optional[str]:
        """
        Returns the whitespace extracted before the title.
        """
        return self.__before_title_whitespace

    @property
    def after_title_whitespace(self) -> Optional[str]:
        """
        Returns the whitespace extracted after the title.
        """
        return self.__after_title_whitespace


# pylint: enable=too-many-instance-attributes


class LinkStartMarkdownToken(ReferenceMarkdownToken):
    """
    Class to provide for an encapsulation of the link element.
    """

    def __init__(
        self,
        text_from_blocks: str,
        line_number: int,
        column_number: int,
        lhp: LinkHelperProperties,
    ) -> None:
        assert lhp.pre_inline_link is not None
        assert lhp.label_type is not None
        assert lhp.inline_link is not None
        ReferenceMarkdownToken.__init__(
            self,
            lhp,
            LinkStartMarkdownToken.get_markdown_token_type(),
            "",
            text_from_blocks,
            line_number=line_number,
            column_number=column_number,
            requires_end_token=True,
            can_force_close=False,
        )

    # pylint: disable=protected-access
    @staticmethod
    def get_markdown_token_type() -> str:
        """
        Get the type of markdown token for rehydration purposes.
        """
        return MarkdownToken._token_inline_link

    # pylint: enable=protected-access


class ImageStartMarkdownToken(ReferenceMarkdownToken):
    """
    Class to provide for an encapsulation of the image element.
    """

    # pylint: disable=too-many-arguments
    def __init__(
        self,
        image_alt_text: str,
        text_from_blocks: str,
        line_number: int,
        column_number: int,
        lhp: LinkHelperProperties,
    ) -> None:
        assert lhp.label_type is not None
        assert lhp.pre_inline_link is not None
        assert lhp.inline_link is not None

        self.__image_alt_text = image_alt_text
        ReferenceMarkdownToken.__init__(
            self,
            lhp,
            ImageStartMarkdownToken.get_markdown_token_type(),
            self.__image_alt_text,
            text_from_blocks,
            line_number=line_number,
            column_number=column_number,
        )

    # pylint: enable=too-many-arguments

    # pylint: disable=protected-access
    @staticmethod
    def get_markdown_token_type() -> str:
        """
        Get the type of markdown token for rehydration purposes.
        """
        return MarkdownToken._token_inline_image

    # pylint: enable=protected-access

    @property
    def image_alt_text(self) -> str:
        """
        Returns the text extracted from the blocks of the link, after processing.
        """
        return self.__image_alt_text


class TextMarkdownToken(InlineMarkdownToken):
    """
    Class to provide for an encapsulation of the text element.
    """

    # pylint: disable=too-many-arguments
    def __init__(
        self,
        token_text: str,
        extracted_whitespace: str,
        end_whitespace: Optional[str] = None,
        position_marker: Optional[PositionMarker] = None,
        line_number: int = 0,
        column_number: int = 0,
        is_special: bool = False,
        tabified_text: Optional[str] = None,
    ):
        (
            self.__token_text,
            self.__extracted_whitespace,
            self.__end_whitespace,
            self.__tabified_text,
        ) = (token_text, extracted_whitespace, end_whitespace, tabified_text)
        InlineMarkdownToken.__init__(
            self,
            MarkdownToken._token_text,
            "",
            position_marker=position_marker,
            line_number=line_number,
            column_number=column_number,
            is_special=is_special,
        )
        self.__compose_extra_data_field()

    # pylint: enable=too-many-arguments

    def _set_token_text(self, new_text: str) -> None:
        self.__token_text = new_text
        self.__compose_extra_data_field()

    @property
    def token_text(self) -> str:
        """
        Returns the text associated with the token.
        """
        return self.__token_text

    @property
    def extracted_whitespace(self) -> str:
        """
        Returns any whitespace that was extracted before the processing of this element occurred.
        """
        return self.__extracted_whitespace

    @property
    def end_whitespace(self) -> Optional[str]:
        """
        Returns any whitespace that was extracted after the processing of this element occurred.
        """
        return self.__end_whitespace

    @property
    def tabified_text(self) -> Optional[str]:
        """
        Returns any text that had a tab character in it.
        """
        return self.__tabified_text

    def create_copy(self) -> "TextMarkdownToken":
        """
        Create a copy of this token.
        """
        return TextMarkdownToken(
            self.__token_text,
            self.__extracted_whitespace,
            self.__end_whitespace,
            line_number=self.line_number,
            column_number=self.column_number,
        )

    def __compose_extra_data_field(self) -> None:
        """
        Compose the object's self.extra_data field from the local object's variables.
        """

        data_field_parts = [self.__token_text, self.__extracted_whitespace]
        if self.__end_whitespace:
            data_field_parts.append(self.__end_whitespace)
            assert not self.__tabified_text
        elif self.__tabified_text:
            data_field_parts.extend(("", self.__tabified_text))
        self._set_extra_data(MarkdownToken.extra_data_separator.join(data_field_parts))

    def remove_final_whitespace(self) -> str:
        """
        Remove any final whitespace.  Used by paragraph blocks so that they do not
        end with a hard break.
        """

        removed_whitespace = ""
        # POGGER.debug("self.__tabified_text=:$:", self.__tabified_text)
        # POGGER.debug("self.__token_text=:$:", self.__token_text)
        (
            collected_whitespace_length,
            first_non_whitespace_index,
        ) = ParserHelper.collect_backwards_while_one_of_characters(
            self.__token_text, -1, Constants.ascii_whitespace
        )
        # POGGER.debug("collected_whitespace_length=:$:", collected_whitespace_length)
        # POGGER.debug("first_non_whitespace_index=:$:", first_non_whitespace_index)

        assert first_non_whitespace_index is not None
        if collected_whitespace_length:
            removed_whitespace = self.__token_text[
                first_non_whitespace_index : first_non_whitespace_index
                + collected_whitespace_length
            ]
            self.__token_text = self.__token_text[:first_non_whitespace_index]
            if self.__tabified_text:
                (
                    collected_whitespace_length,
                    first_non_whitespace_index,
                ) = ParserHelper.collect_backwards_while_one_of_characters(
                    self.__tabified_text, -1, Constants.ascii_whitespace
                )
                # POGGER.debug("collected_whitespace_length=:$:", collected_whitespace_length)
                # POGGER.debug("first_non_whitespace_index=:$:", first_non_whitespace_index)
                assert collected_whitespace_length is not None
                assert first_non_whitespace_index is not None
                removed_whitespace = self.__tabified_text[
                    first_non_whitespace_index : first_non_whitespace_index
                    + collected_whitespace_length
                ]
                self.__tabified_text = self.__tabified_text[:first_non_whitespace_index]
        self.__compose_extra_data_field()
        return removed_whitespace

    def combine(
        self, other_text_token: MarkdownToken, remove_leading_spaces: int
    ) -> str:
        """
        Combine the two text tokens together with a line feed between.
        If remove_leading_spaces > 0, then that many leading spaces will be
        removed from each line, if present.
        If remove_leading_spaces == -1, then.
        If remove_leading_spaces == 0, then.
        """

        if other_text_token.is_blank_line:
            text_to_combine = ""
            tabified_text_to_combine: Optional[str] = ""
            (
                whitespace_present,
                blank_line_sequence,
            ) = (
                other_text_token.extra_data,
                ParserHelper.replace_noop_character,
            )
        else:
            assert other_text_token.is_text
            text_other_token = cast(TextMarkdownToken, other_text_token)

            text_to_combine = text_other_token.token_text
            tabified_text_to_combine = text_other_token.tabified_text
            (
                whitespace_present,
                blank_line_sequence,
            ) = (
                text_other_token.extracted_whitespace,
                "",
            )

        removed_whitespace, prefix_whitespace = self.__combine_handle_whitespace(
            remove_leading_spaces, whitespace_present
        )

        if self.__tabified_text or tabified_text_to_combine:
            other_token_text = tabified_text_to_combine or text_to_combine

            this_token_text = self.__tabified_text or self.__token_text
            # POGGER.debug("this_token_text>:$:<", this_token_text)
            # POGGER.debug("blank_line_sequence>:$:<", blank_line_sequence)
            # POGGER.debug("prefix_whitespace>:$:<", prefix_whitespace)
            # POGGER.debug("other_token_text>:$:<", other_token_text)

            self.__tabified_text = (
                f"{this_token_text}{ParserHelper.newline_character}{blank_line_sequence}"
                + f"{prefix_whitespace}{other_token_text}"
            )
        self.__token_text = (
            f"{self.__token_text}{ParserHelper.newline_character}{blank_line_sequence}"
            + f"{prefix_whitespace}{text_to_combine}"
        )
        self.__compose_extra_data_field()
        return removed_whitespace

    def __combine_handle_whitespace(
        self, remove_leading_spaces: int, whitespace_present: Optional[str]
    ) -> Tuple[str, str]:
        prefix_whitespace = ""
        whitespace_to_append, removed_whitespace = None, ""
        if not remove_leading_spaces:
            assert whitespace_present is not None
            prefix_whitespace = whitespace_present
        elif remove_leading_spaces == -1:
            whitespace_to_append, prefix_whitespace = whitespace_present, ""
        else:
            assert whitespace_present is not None
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
                    whitespace_present[:remove_leading_spaces],
                    whitespace_present[remove_leading_spaces:],
                )

        if whitespace_to_append is not None:
            self.__extracted_whitespace = (
                f"{self.__extracted_whitespace}"
                + f"{ParserHelper.newline_character}{whitespace_to_append}"
            )
        return removed_whitespace, prefix_whitespace


class SpecialTextMarkdownToken(TextMarkdownToken):
    """
    Class to provide for special tokens that represent exceptional inline elements.
    """

    # pylint: disable=too-many-arguments
    def __init__(
        self,
        token_text: str,
        repeat_count: int,
        preceding_two: Optional[str],
        following_two: Optional[str],
        is_active: bool = True,
        line_number: int = 0,
        column_number: int = 0,
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
    def is_active(self) -> bool:
        """
        Returns a value indicating whether this special text is still active.
        """
        return self.__is_active

    @property
    def repeat_count(self) -> int:
        """
        Returns the repeat count for the special text element.
        """
        return self.__repeat_count

    @property
    def preceding_two(self) -> Optional[str]:
        """
        Returns the preceding two characters before this token.
        """
        return self.__preceding_two

    @property
    def following_two(self) -> Optional[str]:
        """
        Returns the following two characters before this token.
        """
        return self.__following_two

    def deactivate(self) -> None:
        """
        Mark this special token as deactivated.
        """
        self.__is_active = False

    def adjust_token_text_by_repeat_count(self) -> None:
        """
        Adjust the token's text by the repeat count.
        """
        self._set_token_text(self.token_text[: self.repeat_count])

    def reduce_repeat_count(
        self, emphasis_length: int, adjust_column_number: bool = False
    ) -> None:
        """
        Reduce the repeat count by the specified amount.
        """
        self.__repeat_count -= emphasis_length
        if adjust_column_number:
            self._set_column_number(self.column_number + emphasis_length)

    def show_process_emphasis(self) -> str:
        """
        Independent of the __str__ function, provide extra information.
        """
        return (
            f">>active={self.__is_active},repeat={self.__repeat_count},preceding='{self.__preceding_two}',"
            + f"following='{self.__following_two}':{self}"
        )
