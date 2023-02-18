"""
Module to provide for a leaf element that can be added to markdown parsing stream.
"""
from typing import Optional

from pymarkdown.link_reference_info import LinkReferenceInfo
from pymarkdown.link_reference_titles import LinkReferenceTitles
from pymarkdown.markdown_token import MarkdownToken, MarkdownTokenClass
from pymarkdown.parser_helper import ParserHelper
from pymarkdown.position_marker import PositionMarker


class LeafMarkdownToken(MarkdownToken):
    """
    Class to provide for a leaf element that can be added to markdown parsing stream.
    """

    # pylint: disable=too-many-arguments
    def __init__(
        self,
        token_name: str,
        extra_data: Optional[str],
        line_number: int = 0,
        column_number: int = 0,
        position_marker: Optional[PositionMarker] = None,
        extracted_whitespace: str = "",
        is_extension: bool = False,
        requires_end_token: bool = False,
        can_force_close: bool = True,
    ) -> None:
        self.__extracted_whitespace = extracted_whitespace
        MarkdownToken.__init__(
            self,
            token_name,
            MarkdownTokenClass.LEAF_BLOCK,
            extra_data,
            line_number=line_number,
            column_number=column_number,
            position_marker=position_marker,
            is_extension=is_extension,
            requires_end_token=requires_end_token,
            can_force_close=can_force_close,
        )

    # pylint: enable=too-many-arguments

    @property
    def extracted_whitespace(self) -> str:
        """
        Returns any whitespace that was extracted before the processing of this element occurred.
        """
        return self.__extracted_whitespace


class BlankLineMarkdownToken(LeafMarkdownToken):
    """
    Class to provide for an encapsulation of the blank line element.
    """

    def __init__(
        self,
        extracted_whitespace: str,
        position_marker: Optional[PositionMarker],
        column_delta: int = 0,
    ) -> None:

        if position_marker:
            line_number, column_number = position_marker.line_number, (
                position_marker.index_number
                + position_marker.index_indent
                + 1
                - column_delta
            )
        else:
            line_number, column_number = 0, 0

        LeafMarkdownToken.__init__(
            self,
            MarkdownToken._token_blank_line,
            extracted_whitespace,
            line_number=line_number,
            column_number=column_number,
            extracted_whitespace=extracted_whitespace,
        )


class ParagraphMarkdownToken(LeafMarkdownToken):
    """
    Class to provide for an encapsulation of the paragraph element.
    """

    def __init__(
        self, extracted_whitespace: str, position_marker: PositionMarker
    ) -> None:
        self.__extracted_whitespace: str = extracted_whitespace
        self.__final_whitespace, self.rehydrate_index = (
            "",
            0,
        )
        LeafMarkdownToken.__init__(
            self,
            MarkdownToken._token_paragraph,
            "",
            position_marker=position_marker,
            requires_end_token=True,
        )
        self.__compose_extra_data_field()

    @property
    def extracted_whitespace(self) -> str:
        """
        Returns any whitespace that was extracted before the processing of this element occurred.
        """
        return self.__extracted_whitespace

    @property
    def final_whitespace(self) -> str:
        """
        Returns any final whitespace at the end of the paragraph that was removed.
        """
        return self.__final_whitespace

    def __compose_extra_data_field(self) -> None:
        """
        Compose the object's self.extra_data field from the local object's variables.
        """

        self._set_extra_data(
            f"{self.__extracted_whitespace}{MarkdownToken.extra_data_separator}{self.__final_whitespace}"
            if self.final_whitespace
            else self.__extracted_whitespace
        )

    def add_whitespace(self, whitespace_to_add: str) -> None:
        """
        Add extra whitespace to the end of the current paragraph.  Should only be
        used when combining text blocks in a paragraph.
        """

        self.__extracted_whitespace = (
            f"{self.__extracted_whitespace}{whitespace_to_add}"
        )
        self.__compose_extra_data_field()

    def set_final_whitespace(self, whitespace_to_set: str) -> None:
        """
        Set the final whitespace for the paragraph. That is any whitespace at the very
        end of the paragraph, removed to prevent hard lines at the end.
        """

        self.__final_whitespace = whitespace_to_set
        self.__compose_extra_data_field()


class ThematicBreakMarkdownToken(LeafMarkdownToken):
    """
    Class to provide for an encapsulation of the thematic break element.
    """

    def __init__(
        self,
        start_character: str,
        extracted_whitespace: Optional[str],
        rest_of_line: str,
        position_marker: PositionMarker,
    ) -> None:
        assert extracted_whitespace is not None
        self.__rest_of_line = rest_of_line
        LeafMarkdownToken.__init__(
            self,
            MarkdownToken._token_thematic_break,
            MarkdownToken.extra_data_separator.join(
                [start_character, extracted_whitespace, self.__rest_of_line]
            ),
            position_marker=position_marker,
            extracted_whitespace=extracted_whitespace,
        )

    @property
    def rest_of_line(self) -> str:
        """
        Returns any whitespace that was extracted before the processing of this element occurred.
        """
        return self.__rest_of_line


class HtmlBlockMarkdownToken(LeafMarkdownToken):
    """
    Class to provide for an encapsulation of the html block element.
    """

    def __init__(
        self, position_marker: PositionMarker, extracted_whitespace: str
    ) -> None:
        if position_marker:
            line_number, column_number = position_marker.line_number, (
                position_marker.index_number
                + position_marker.index_indent
                + 1
                - len(extracted_whitespace)
            )
        else:
            line_number, column_number = -1, -1

        LeafMarkdownToken.__init__(
            self,
            MarkdownToken._token_html_block,
            "",
            line_number=line_number,
            column_number=column_number,
            extracted_whitespace=extracted_whitespace,
            requires_end_token=True,
        )


# pylint: disable=too-many-instance-attributes
class LinkReferenceDefinitionMarkdownToken(LeafMarkdownToken):
    """
    Class to provide for an encapsulation of the link reference definition element.
    """

    # pylint: disable=too-many-arguments
    def __init__(
        self,
        did_add_definition: bool,
        extracted_whitespace: str,
        link_name: str,
        link_value: LinkReferenceTitles,
        link_debug: Optional[LinkReferenceInfo],
        position_marker: PositionMarker,
    ) -> None:
        self.__did_add_definition = did_add_definition
        self.__link_name = link_name

        if link_value:
            self.__link_destination, self.__link_title = (
                link_value.inline_link,
                link_value.inline_title,
            )
        else:
            self.__link_destination, self.__link_title = "", ""

        if link_debug:
            (
                self.__link_name_debug,
                self.__link_destination_whitespace,
                self.__link_destination_raw,
                self.__link_title_whitespace,
                self.__link_title_raw,
                self.__end_whitespace,
            ) = (
                ""
                if link_debug.collected_destination == self.__link_name
                else link_debug.collected_destination,
                link_debug.line_destination_whitespace,
                ""
                if link_debug.inline_raw_link == self.__link_destination
                else link_debug.inline_raw_link,
                link_debug.line_title_whitespace,
                ""
                if link_debug.inline_raw_title == self.__link_title
                else link_debug.inline_raw_title,
                link_debug.end_whitespace,
            )
        else:
            (
                self.__link_name_debug,
                self.__link_destination_whitespace,
                self.__link_destination_raw,
                self.__link_title_whitespace,
                self.__link_title_raw,
                self.__end_whitespace,
            ) = ("", "", "", "", "", "")

        extra_data = self.__validate_proper_fields_are_valid(extracted_whitespace)
        LeafMarkdownToken.__init__(
            self,
            MarkdownToken._token_link_reference_definition,
            extra_data,
            position_marker=position_marker,
            extracted_whitespace=extracted_whitespace,
        )

    def __validate_proper_fields_are_valid(self, extracted_whitespace: str) -> str:
        assert self.__end_whitespace is not None
        assert self.__link_title_raw is not None
        assert self.__link_title is not None
        assert self.__link_title_whitespace is not None
        assert self.__link_destination_raw is not None
        assert self.__link_destination is not None
        assert self.__link_destination_whitespace is not None
        assert self.__link_name_debug is not None
        return MarkdownToken.extra_data_separator.join(
            [
                str(self.did_add_definition),
                extracted_whitespace,
                self.__link_name,
                self.__link_name_debug,
                self.__link_destination_whitespace,
                self.__link_destination,
                self.__link_destination_raw,
                self.__link_title_whitespace,
                self.__link_title,
                self.__link_title_raw,
                self.__end_whitespace,
            ]
        )

    # pylint: enable=too-many-arguments
    @property
    def did_add_definition(self) -> bool:
        """
        Returns an indication of whether the definition was actually added.
        """
        return self.__did_add_definition

    @property
    def end_whitespace(self) -> Optional[str]:
        """
        Returns any whitespace that was extracted after the processing of this element occurred.
        """
        return self.__end_whitespace

    @property
    def link_name(self) -> str:
        """
        Returns the name of the link that was defined.
        """
        return self.__link_name

    @property
    def link_name_debug(self) -> Optional[str]:
        """
        Returns the name of the link that was defined, in debug form.
        """
        return self.__link_name_debug

    @property
    def link_destination_whitespace(self) -> Optional[str]:
        """
        Returns the whitespace that occurs before the link destination.
        """
        return self.__link_destination_whitespace

    @property
    def link_destination(self) -> Optional[str]:
        """
        Returns the destination (URI) of the link that was defined.
        """
        return self.__link_destination

    @property
    def link_destination_raw(self) -> Optional[str]:
        """
        Returns the destination (URI) of the link that was defined, in raw form.
        """
        return self.__link_destination_raw

    @property
    def link_title(self) -> Optional[str]:
        """
        Returns the title of the link that was defined.
        """
        return self.__link_title

    @property
    def link_title_raw(self) -> Optional[str]:
        """
        Returns the title of the link that was defined, in raw form.
        """
        return self.__link_title_raw

    @property
    def link_title_whitespace(self) -> Optional[str]:
        """
        Returns the whitespace that occurs after the link title.
        """
        return self.__link_title_whitespace


# pylint: enable=too-many-instance-attributes


class AtxHeadingMarkdownToken(LeafMarkdownToken):
    """
    Class to provide for an encapsulation of the atx heading element.
    """

    def __init__(
        self,
        hash_count: int,
        remove_trailing_count: int,
        extracted_whitespace: str,
        position_marker: PositionMarker,
    ) -> None:
        self.__hash_count, self.__remove_trailing_count = (
            hash_count,
            remove_trailing_count,
        )

        LeafMarkdownToken.__init__(
            self,
            MarkdownToken._token_atx_heading,
            "",
            position_marker=position_marker,
            extracted_whitespace=extracted_whitespace,
            requires_end_token=True,
            can_force_close=False,
        )
        self.__compose_extra_data_field()

    @property
    def hash_count(self) -> int:
        """
        Returns the number of hash marks specified at the start of the line.
        """
        return self.__hash_count

    @property
    def remove_trailing_count(self) -> int:
        """
        Returns the number of hash marks specified at the end of the line.
        """
        return self.__remove_trailing_count

    def __compose_extra_data_field(self) -> None:
        """
        Compose the object's self.extra_data field from the local object's variables.
        """
        self._set_extra_data(
            MarkdownToken.extra_data_separator.join(
                [
                    str(self.__hash_count),
                    str(self.__remove_trailing_count),
                    self.extracted_whitespace,
                ]
            )
        )


class SetextHeadingMarkdownToken(LeafMarkdownToken):
    """
    Class to provide for an encapsulation of the setext heading element.
    """

    # pylint: disable=too-many-arguments
    def __init__(
        self,
        heading_character: str,
        heading_character_count: int,
        extracted_whitespace: str,
        position_marker: PositionMarker,
        para_token: ParagraphMarkdownToken,
    ) -> None:
        (
            self.__heading_character,
            self.__heading_character_count,
            self.__final_whitespace,
            self.__original_line_number,
            self.__original_column_number,
        ) = (
            heading_character,
            heading_character_count,
            "",
            para_token.line_number if para_token else -1,
            para_token.column_number if para_token else -1,
        )

        if self.__heading_character == "=":
            self.__hash_count = 1
        elif self.__heading_character == "-":
            self.__hash_count = 2
        else:
            self.__hash_count = -1

        LeafMarkdownToken.__init__(
            self,
            MarkdownToken._token_setext_heading,
            "",
            position_marker=position_marker,
            extracted_whitespace=extracted_whitespace,
            requires_end_token=True,
            can_force_close=False,
        )
        self.__compose_extra_data_field()

    # pylint: enable=too-many-arguments

    @property
    def final_whitespace(self) -> str:
        """
        Returns any final whitespace at the end of the heading that was removed.
        """
        return self.__final_whitespace

    @property
    def heading_character(self) -> str:
        """
        Returns the character associated with the heading start.
        """
        return self.__heading_character

    @property
    def hash_count(self) -> int:
        """
        Returns the count in equivalence of "Atx Hash" counts.
        """
        return self.__hash_count

    @property
    def heading_character_count(self) -> int:
        """
        Returns the count of characters associated with the heading start.
        """
        return self.__heading_character_count

    @property
    def original_line_number(self) -> int:
        """
        Returns the line number where this element actually started.
        """
        return self.__original_line_number

    @property
    def original_column_number(self) -> int:
        """
        Returns the column number where this element actually started.
        """
        return self.__original_column_number

    def set_final_whitespace(self, whitespace_to_set: str) -> None:
        """
        Set the final whitespace for the paragraph. That is any whitespace at the very
        end of the paragraph, removed to prevent hard lines at the end.
        """

        self.__final_whitespace = whitespace_to_set
        self.__compose_extra_data_field()

    def __compose_extra_data_field(self) -> None:
        """
        Compose the object's self.extra_data field from the local object's variables.
        """

        original_location = (
            f"({self.original_line_number},{self.original_column_number})"
        )
        field_parts = [
            self.__heading_character,
            str(self.__heading_character_count),
            self.extracted_whitespace,
            original_location,
        ]
        if self.final_whitespace:
            field_parts.append(self.final_whitespace)
        self._set_extra_data(MarkdownToken.extra_data_separator.join(field_parts))


class IndentedCodeBlockMarkdownToken(LeafMarkdownToken):
    """
    Class to provide for an encapsulation of the indented code block element.
    """

    def __init__(
        self, extracted_whitespace: str, line_number: int, column_number: int
    ) -> None:
        self.__indented_whitespace = ""
        LeafMarkdownToken.__init__(
            self,
            MarkdownToken._token_indented_code_block,
            extracted_whitespace,
            line_number=line_number,
            column_number=column_number,
            extracted_whitespace=extracted_whitespace,
            requires_end_token=True,
        )
        self.__compose_extra_data_field()

    @property
    def indented_whitespace(self) -> str:
        """
        Returns any indented whitespace that comes before the text.
        """
        return self.__indented_whitespace

    def __compose_extra_data_field(self) -> None:
        """
        Compose the object's self.extra_data field from the local object's variables.
        """
        self._set_extra_data(
            MarkdownToken.extra_data_separator.join(
                [self.extracted_whitespace, self.indented_whitespace]
            )
        )

    def add_indented_whitespace(self, indented_whitespace: str) -> None:
        """
        Add the indented whitespace that comes before the text.
        """
        self.__indented_whitespace = (
            f"{self.__indented_whitespace}{ParserHelper.newline_character}"
            + f"{indented_whitespace}"
        )
        self.__compose_extra_data_field()


class FencedCodeBlockMarkdownToken(LeafMarkdownToken):
    """
    Class to provide for an encapsulation of the fenced code block element.
    """

    # pylint: disable=too-many-arguments
    def __init__(
        self,
        fence_character: str,
        fence_count: int,
        extracted_text: str,
        pre_extracted_text: str,
        text_after_extracted_text: str,
        pre_text_after_extracted_text: str,
        extracted_whitespace: str,
        extracted_whitespace_before_info_string: str,
        position_marker: PositionMarker,
    ) -> None:
        (
            self.__extracted_text,
            self.__pre_extracted_text,
            self.__extracted_whitespace_before_info_string,
            self.__text_after_extracted_text,
            self.__pre_text_after_extracted_text,
            self.__fence_character,
            self.__fence_count,
        ) = (
            extracted_text,
            pre_extracted_text,
            extracted_whitespace_before_info_string,
            text_after_extracted_text,
            pre_text_after_extracted_text,
            fence_character,
            fence_count,
        )
        LeafMarkdownToken.__init__(
            self,
            MarkdownToken._token_fenced_code_block,
            "",
            position_marker=position_marker,
            extracted_whitespace=extracted_whitespace,
            requires_end_token=True,
        )
        self.__compose_extra_data_field()

    # pylint: enable=too-many-arguments

    @property
    def fence_character(self) -> str:
        """
        Returns the character used for the fence.
        """
        return self.__fence_character

    @property
    def fence_count(self) -> int:
        """
        Returns the number of fence characters used for the fence.
        """
        return self.__fence_count

    @property
    def extracted_text(self) -> str:
        """
        Returns the text extracted from the info string.
        """
        return self.__extracted_text

    @property
    def pre_extracted_text(self) -> str:
        """
        Returns the text extracted from the info string.
        """
        return self.__pre_extracted_text

    @property
    def text_after_extracted_text(self) -> str:
        """
        Returns the text extracted after the info string.
        """
        return self.__text_after_extracted_text

    @property
    def pre_text_after_extracted_text(self) -> str:
        """
        Returns the text extracted after after the info string.
        """
        return self.__pre_text_after_extracted_text

    @property
    def extracted_whitespace_before_info_string(self) -> str:
        """
        Returns any whitespace that was extracted before the info string was processed.
        """
        return self.__extracted_whitespace_before_info_string

    def __compose_extra_data_field(self) -> None:
        """
        Compose the object's self.extra_data field from the local object's variables.
        """
        self._set_extra_data(
            MarkdownToken.extra_data_separator.join(
                [
                    self.__fence_character,
                    str(self.__fence_count),
                    self.__extracted_text,
                    self.__pre_extracted_text,
                    self.__text_after_extracted_text,
                    self.__pre_text_after_extracted_text,
                    self.extracted_whitespace,
                    self.__extracted_whitespace_before_info_string,
                ]
            )
        )
