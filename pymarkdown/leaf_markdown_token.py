"""
Module to provide for a leaf element that can be added to markdown parsing stream.
"""
from pymarkdown.markdown_token import MarkdownToken, MarkdownTokenClass
from pymarkdown.parser_helper import ParserHelper


class LeafMarkdownToken(MarkdownToken):
    """
    Class to provide for a leaf element that can be added to markdown parsing stream.
    """

    # pylint: disable=too-many-arguments
    def __init__(
        self,
        token_name,
        extra_data,
        line_number=0,
        column_number=0,
        position_marker=None,
        extracted_whitespace=None,
    ):
        self.__extracted_whitespace = extracted_whitespace
        MarkdownToken.__init__(
            self,
            token_name,
            MarkdownTokenClass.LEAF_BLOCK,
            extra_data,
            line_number=line_number,
            column_number=column_number,
            position_marker=position_marker,
        )

    # pylint: enable=too-many-arguments

    @property
    def extracted_whitespace(self):
        """
        Returns any whitespace that was extracted before the processing of this element occurred.
        """
        return self.__extracted_whitespace


# pylint: disable=too-few-public-methods
class BlankLineMarkdownToken(LeafMarkdownToken):
    """
    Class to provide for an encapsulation of the blank line element.
    """

    def __init__(self, extracted_whitespace, position_marker, column_delta=0):

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

        LeafMarkdownToken.__init__(
            self,
            MarkdownToken._token_blank_line,
            extracted_whitespace,
            line_number=line_number,
            column_number=column_number,
            extracted_whitespace=extracted_whitespace,
        )


# pylint: enable=too-few-public-methods


class ParagraphMarkdownToken(LeafMarkdownToken):
    """
    Class to provide for an encapsulation of the paragraph element.
    """

    def __init__(self, extracted_whitespace, position_marker):
        self.__extracted_whitespace = extracted_whitespace
        self.__final_whitespace = ""
        self.rehydrate_index = 0
        LeafMarkdownToken.__init__(
            self,
            MarkdownToken._token_paragraph,
            "",
            position_marker=position_marker,
        )
        self.__compose_extra_data_field()

    @property
    def extracted_whitespace(self):
        """
        Returns any whitespace that was extracted before the processing of this element occurred.
        """
        return self.__extracted_whitespace

    @property
    def final_whitespace(self):
        """
        Returns any final whitespace at the end of the paragraph that was removed.
        """
        return self.__final_whitespace

    def __compose_extra_data_field(self):
        """
        Compose the object's self.extra_data field from the local object's variables.
        """

        new_extra_data = self.__extracted_whitespace
        if self.final_whitespace:
            new_extra_data += ":" + self.__final_whitespace
        self._set_extra_data(new_extra_data)

    def add_whitespace(self, whitespace_to_add):
        """
        Add extra whitespace to the end of the current paragraph.  Should only be
        used when combining text blocks in a paragraph.
        """

        self.__extracted_whitespace += whitespace_to_add
        self.__compose_extra_data_field()

    def set_final_whitespace(self, whitespace_to_set):
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
        self, start_character, extracted_whitespace, rest_of_line, position_marker
    ):
        self.__rest_of_line = rest_of_line
        LeafMarkdownToken.__init__(
            self,
            MarkdownToken._token_thematic_break,
            start_character + ":" + extracted_whitespace + ":" + self.__rest_of_line,
            position_marker=position_marker,
            extracted_whitespace=extracted_whitespace,
        )

    @property
    def rest_of_line(self):
        """
        Returns any whitespace that was extracted before the processing of this element occurred.
        """
        return self.__rest_of_line


class HtmlBlockMarkdownToken(LeafMarkdownToken):
    """
    Class to provide for an encapsulation of the html block element.
    """

    def __init__(self, position_marker, extracted_whitespace):
        if position_marker:
            line_number = position_marker.line_number
            column_number = (
                position_marker.index_number
                + position_marker.index_indent
                + 1
                - len(extracted_whitespace)
            )
        else:
            line_number = -1
            column_number = -1

        LeafMarkdownToken.__init__(
            self,
            MarkdownToken._token_html_block,
            "",
            line_number=line_number,
            column_number=column_number,
            extracted_whitespace=extracted_whitespace,
        )


# pylint: disable=too-many-instance-attributes
class LinkReferenceDefinitionMarkdownToken(LeafMarkdownToken):
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
        self.__did_add_definition = did_add_definition
        self.__link_name = link_name

        if link_value:
            self.__link_destination = link_value[0]
            self.__link_title = link_value[1]
        else:
            self.__link_destination = ""
            self.__link_title = ""

        if link_debug:
            self.__link_name_debug = link_debug[0]
            if self.__link_name_debug == self.__link_name:
                self.__link_name_debug = ""
            self.__link_destination_whitespace = link_debug[1]
            self.__link_destination_raw = link_debug[2]
            if self.__link_destination_raw == self.__link_destination:
                self.__link_destination_raw = ""
            self.__link_title_whitespace = link_debug[3]
            self.__link_title_raw = link_debug[4]
            if self.__link_title_raw == self.__link_title:
                self.__link_title_raw = ""
            self.__end_whitespace = link_debug[5]
        else:
            self.__link_name_debug = ""
            self.__link_destination_whitespace = ""
            self.__link_destination_raw = ""
            self.__link_title_whitespace = ""
            self.__link_title_raw = ""
            self.__end_whitespace = ""
        extra_data = (
            str(self.did_add_definition)
            + ":"
            + extracted_whitespace
            + ":"
            + self.__link_name
            + ":"
            + self.__link_name_debug
            + ":"
            + self.__link_destination_whitespace
            + ":"
            + self.__link_destination
            + ":"
            + self.__link_destination_raw
            + ":"
            + self.__link_title_whitespace
            + ":"
            + self.__link_title
            + ":"
            + self.__link_title_raw
            + ":"
            + self.__end_whitespace
        )
        LeafMarkdownToken.__init__(
            self,
            MarkdownToken._token_link_reference_definition,
            extra_data,
            position_marker=position_marker,
            extracted_whitespace=extracted_whitespace,
        )

    # pylint: enable=too-many-arguments
    @property
    def did_add_definition(self):
        """
        Returns an indication of whether the definition was actually added.
        """
        return self.__did_add_definition

    @property
    def end_whitespace(self):
        """
        Returns any whitespace that was extracted after the processing of this element occurred.
        """
        return self.__end_whitespace

    @property
    def link_name(self):
        """
        Returns the name of the link that was defined.
        """
        return self.__link_name

    @property
    def link_name_debug(self):
        """
        Returns the name of the link that was defined, in debug form.
        """
        return self.__link_name_debug

    @property
    def link_destination_whitespace(self):
        """
        Returns the whitespace that occurs before the link destination.
        """
        return self.__link_destination_whitespace

    @property
    def link_destination(self):
        """
        Returns the destination (URI) of the link that was defined.
        """
        return self.__link_destination

    @property
    def link_destination_raw(self):
        """
        Returns the destination (URI) of the link that was defined, in raw form.
        """
        return self.__link_destination_raw

    @property
    def link_title(self):
        """
        Returns the title of the link that was defined.
        """
        return self.__link_title

    @property
    def link_title_raw(self):
        """
        Returns the title of the link that was defined, in raw form.
        """
        return self.__link_title_raw

    @property
    def link_title_whitespace(self):
        """
        Returns the whitespace that occurs after the link title.
        """
        return self.__link_title_whitespace


# pylint: enable=too-many-instance-attributes


class AtxHeadingMarkdownToken(LeafMarkdownToken):
    """
    Class to provide for an encapsulation of the atx heading element.
    """

    # pylint: disable=too-many-arguments
    def __init__(
        self,
        hash_count,
        remove_trailing_count,
        extracted_whitespace,
        position_marker,
    ):
        self.__hash_count = hash_count
        self.__remove_trailing_count = remove_trailing_count

        LeafMarkdownToken.__init__(
            self,
            MarkdownToken._token_atx_heading,
            "",
            position_marker=position_marker,
            extracted_whitespace=extracted_whitespace,
        )
        self.__compose_extra_data_field()

    # pylint: enable=too-many-arguments

    @property
    def hash_count(self):
        """
        Returns the number of hash marks specified at the start of the line.
        """
        return self.__hash_count

    @property
    def remove_trailing_count(self):
        """
        Returns the number of hash marks specified at the end of the line.
        """
        return self.__remove_trailing_count

    def __compose_extra_data_field(self):
        """
        Compose the object's self.extra_data field from the local object's variables.
        """
        new_extra_data = (
            str(self.__hash_count)
            + ":"
            + str(self.__remove_trailing_count)
            + ":"
            + self.extracted_whitespace
        )
        self._set_extra_data(new_extra_data)


# pylint: disable=too-many-instance-attributes
class SetextHeadingMarkdownToken(LeafMarkdownToken):
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
        self.__heading_character = heading_character
        self.__heading_character_count = heading_character_count
        self.__final_whitespace = ""
        if self.__heading_character == "=":
            self.__hash_count = 1
        elif self.__heading_character == "-":
            self.__hash_count = 2
        else:
            self.__hash_count = -1
        if para_token:
            self.__original_line_number = para_token.line_number
            self.__original_column_number = para_token.column_number
        else:
            self.__original_line_number = -1
            self.__original_column_number = -1
        LeafMarkdownToken.__init__(
            self,
            MarkdownToken._token_setext_heading,
            "",
            position_marker=position_marker,
            extracted_whitespace=extracted_whitespace,
        )
        self.__compose_extra_data_field()

    # pylint: enable=too-many-arguments

    @property
    def final_whitespace(self):
        """
        Returns any final whitespace at the end of the heading that was removed.
        """
        return self.__final_whitespace

    @property
    def heading_character(self):
        """
        Returns the character associated with the heading start.
        """
        return self.__heading_character

    @property
    def hash_count(self):
        """
        Returns the count in equivalence of "Atx Hash" counts.
        """
        return self.__hash_count

    @property
    def heading_character_count(self):
        """
        Returns the count of characters associated with the heading start.
        """
        return self.__heading_character_count

    @property
    def original_line_number(self):
        """
        Returns the line number where this element actually started.
        """
        return self.__original_line_number

    @property
    def original_column_number(self):
        """
        Returns the column number where this element actually started.
        """
        return self.__original_column_number

    def set_final_whitespace(self, whitespace_to_set):
        """
        Set the final whitespace for the paragraph. That is any whitespace at the very
        end of the paragraph, removed to prevent hard lines at the end.
        """

        self.__final_whitespace = whitespace_to_set
        self.__compose_extra_data_field()

    def __compose_extra_data_field(self):
        """
        Compose the object's self.extra_data field from the local object's variables.
        """

        new_extra_data = (
            self.__heading_character
            + ":"
            + str(self.__heading_character_count)
            + ":"
            + self.extracted_whitespace
            + ":("
            + str(self.original_line_number)
            + ","
            + str(self.original_column_number)
            + ")"
        )
        if self.final_whitespace:
            new_extra_data += ":" + self.final_whitespace
        self._set_extra_data(new_extra_data)


# pylint: enable=too-many-instance-attributes


class IndentedCodeBlockMarkdownToken(LeafMarkdownToken):
    """
    Class to provide for an encapsulation of the indented code block element.
    """

    def __init__(self, extracted_whitespace, line_number, column_number):
        self.__indented_whitespace = ""
        LeafMarkdownToken.__init__(
            self,
            MarkdownToken._token_indented_code_block,
            extracted_whitespace,
            line_number=line_number,
            column_number=column_number,
            extracted_whitespace=extracted_whitespace,
        )
        self.__compose_extra_data_field()

    @property
    def indented_whitespace(self):
        """
        Returns any indented whitespace that comes before the text.
        """
        return self.__indented_whitespace

    def __compose_extra_data_field(self):
        """
        Compose the object's self.extra_data field from the local object's variables.
        """
        self._set_extra_data(self.extracted_whitespace + ":" + self.indented_whitespace)

    def add_indented_whitespace(self, indented_whitespace):
        """
        Add the indented whitespace that comes before the text.
        """
        self.__indented_whitespace += (
            ParserHelper.newline_character + indented_whitespace
        )
        self.__compose_extra_data_field()


# pylint: disable=too-many-instance-attributes
class FencedCodeBlockMarkdownToken(LeafMarkdownToken):
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
        self.__extracted_text = extracted_text
        self.__pre_extracted_text = pre_extracted_text
        self.__extracted_whitespace_before_info_string = (
            extracted_whitespace_before_info_string
        )
        self.__text_after_extracted_text = text_after_extracted_text
        self.__pre_text_after_extracted_text = pre_text_after_extracted_text
        self.__fence_character = fence_character
        self.__fence_count = fence_count
        LeafMarkdownToken.__init__(
            self,
            MarkdownToken._token_fenced_code_block,
            "",
            position_marker=position_marker,
            extracted_whitespace=extracted_whitespace,
        )
        self.__compose_extra_data_field()

    # pylint: enable=too-many-arguments

    @property
    def fence_character(self):
        """
        Returns the character used for the fence.
        """
        return self.__fence_character

    @property
    def fence_count(self):
        """
        Returns the number of fence characters used for the fence.
        """
        return self.__fence_count

    @property
    def extracted_text(self):
        """
        Returns the text extracted from the info string.
        """
        return self.__extracted_text

    @property
    def pre_extracted_text(self):
        """
        Returns the text extracted from the info string.
        """
        return self.__pre_extracted_text

    @property
    def text_after_extracted_text(self):
        """
        Returns the text extracted after the info string.
        """
        return self.__text_after_extracted_text

    @property
    def pre_text_after_extracted_text(self):
        """
        Returns the text extracted after after the info string.
        """
        return self.__pre_text_after_extracted_text

    @property
    def extracted_whitespace_before_info_string(self):
        """
        Returns any whitespace that was extracted before the info string was processed.
        """
        return self.__extracted_whitespace_before_info_string

    def __compose_extra_data_field(self):
        """
        Compose the object's self.extra_data field from the local object's variables.
        """
        new_extra_data = (
            self.__fence_character
            + ":"
            + str(self.__fence_count)
            + ":"
            + self.__extracted_text
            + ":"
            + self.__pre_extracted_text
            + ":"
            + self.__text_after_extracted_text
            + ":"
            + self.__pre_text_after_extracted_text
            + ":"
            + self.extracted_whitespace
            + ":"
            + self.__extracted_whitespace_before_info_string
        )
        self._set_extra_data(new_extra_data)


# pylint: enable=too-many-instance-attributes
