"""
Module to hold the response from the inline handle_* functions.
"""


# pylint: disable=too-many-instance-attributes
class InlineResponse:
    """
    Class to hold the response from the inline handle_* functions.
    """

    def __init__(self):
        (
            self.__new_string,
            self.__new_index,
            self.__new_tokens,
            self.__new_string_unresolved,
            self.__consume_rest_of_line,
            self.__original_string,
            self.__delta_line_number,
            self.__delta_column_number,
        ) = (None, None, None, None, False, None, 0, 0)
        self.clear_fields()

    @property
    def new_string(self):
        """
        New string that was processed.
        """
        return self.__new_string

    @new_string.setter
    def new_string(self, value):
        self.__new_string = value

    @property
    def new_string_unresolved(self):
        """
        New string that was processed, raw.
        """
        return self.__new_string_unresolved

    @new_string_unresolved.setter
    def new_string_unresolved(self, value):
        self.__new_string_unresolved = value

    @property
    def new_index(self):
        """
        New index resulting from the parsing.
        """
        return self.__new_index

    @new_index.setter
    def new_index(self, value):
        self.__new_index = value

    @property
    def new_tokens(self):
        """
        New tokens produced as part of the parsing.
        """
        return self.__new_tokens

    @new_tokens.setter
    def new_tokens(self, value):
        self.__new_tokens = value

    @property
    def consume_rest_of_line(self):
        """
        Whether to consume the rest of the line.
        """
        return self.__consume_rest_of_line

    @consume_rest_of_line.setter
    def consume_rest_of_line(self, value):
        self.__consume_rest_of_line = value

    @property
    def original_string(self):
        """
        Original string that was interpreted.
        """
        return self.__original_string

    @original_string.setter
    def original_string(self, value):
        self.__original_string = value

    @property
    def delta_line_number(self):
        """
        Change in the line number.
        """
        return self.__delta_line_number

    @delta_line_number.setter
    def delta_line_number(self, value):
        self.__delta_line_number = value

    @property
    def delta_column_number(self):
        """
        Change in the column number.
        """
        return self.__delta_column_number

    @delta_column_number.setter
    def delta_column_number(self, value):
        self.__delta_column_number = value

    def clear_fields(self):
        """
        Clear any of the fields that start with new_*.
        """
        (
            self.__new_string,
            self.__new_index,
            self.__new_tokens,
            self.__new_string_unresolved,
            self.__consume_rest_of_line,
            self.__original_string,
            self.__delta_line_number,
            self.__delta_column_number,
        ) = (None, None, None, None, False, None, 0, 0)


# pylint: enable=too-many-instance-attributes
