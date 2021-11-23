"""
Module to hold the request information to pass on to the handle_* functions.
"""


# pylint: disable=too-many-instance-attributes
class InlineRequest:
    """
    Class to hold the request information to pass on to the handle_* functions.
    """

    # pylint: disable=too-many-arguments
    def __init__(
        self,
        source_text,
        next_index,
        inline_blocks=None,
        remaining_line=None,
        current_string_unresolved=None,
        line_number=None,
        column_number=None,
        para_owner=None,
    ):
        (
            self.__source_text,
            self.__next_index,
            self.__inline_blocks,
            self.__remaining_line,
            self.__current_string_unresolved,
            self.__line_number,
            self.__column_number,
            self.__para_owner,
        ) = (
            source_text,
            next_index,
            inline_blocks,
            remaining_line,
            current_string_unresolved,
            line_number,
            column_number,
            para_owner,
        )

    # pylint: enable=too-many-arguments
    @property
    def source_text(self):
        """
        Text that is the source of the inline request.
        """
        return self.__source_text

    @property
    def next_index(self):
        """
        Index into the source text.
        """
        return self.__next_index

    @property
    def inline_blocks(self):
        """
        Inline blocks collected up to this point in the processing.
        """
        return self.__inline_blocks

    @property
    def remaining_line(self):
        """
        Remaining part of the line.
        """
        return self.__remaining_line

    @property
    def current_string_unresolved(self):
        """
        Version of the current string before anything is changed.
        """
        return self.__current_string_unresolved

    @property
    def line_number(self):
        """
        Line number where the block of text starts.
        """
        return self.__line_number

    @property
    def column_number(self):
        """
        Column number where the block of text starts.
        """
        return self.__column_number

    @property
    def para_owner(self):
        """
        Paragraph token that owns the current block of text.
        """
        return self.__para_owner


# pylint: enable=too-many-instance-attributes
