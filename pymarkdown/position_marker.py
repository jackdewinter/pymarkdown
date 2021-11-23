"""
Module to provide an encapsulation of the location within the Markdown document.
"""


class PositionMarker:
    """
    Class to provide an encapsulation of the location within the Markdown document.
    """

    def __init__(self, line_number, index_number, text_to_parse, index_indent=0):
        (
            self.__line_number,
            self.__index_number,
            self.__text_to_parse,
            self.__index_indent,
        ) = (line_number, index_number, text_to_parse, index_indent)

    @property
    def line_number(self):
        """
        Gets the line number.
        """
        return self.__line_number

    @property
    def index_number(self):
        """
        Gets the index number.
        """
        return self.__index_number

    @property
    def text_to_parse(self):
        """
        Gets the text being parsed.
        """
        return self.__text_to_parse

    @property
    def index_indent(self):
        """
        Gets the amount that the index is considered indented by.
        """
        return self.__index_indent
