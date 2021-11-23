"""
Module to provide a tokenization of a markdown-encoded string.
"""

from pymarkdown.parser_helper import ParserHelper


class InMemorySourceProvider:
    """
    Class to provide for a source provider that is totally within memory.
    """

    def __init__(self, source_text):
        self.__next_token = source_text.split(ParserHelper.newline_character, 1)

    def is_at_end_of_file(self):
        """
        Whether the provider has reached the end of the input.
        """
        return not self.__next_token

    def get_next_line(self):
        """
        Get the next line from the source provider.
        """
        token_to_use = None
        if not self.is_at_end_of_file():
            token_to_use = self.__next_token[0]
            if len(self.__next_token) == 2:
                self.__next_token = self.__next_token[1].split(
                    ParserHelper.newline_character, 1
                )
            else:
                assert self.__next_token
                self.__next_token = None
        return token_to_use


class FileSourceProvider:
    """
    Class to provide for a source provider that is on media as a file.
    """

    def __init__(self, file_to_open):
        with open(file_to_open, encoding="utf-8") as file_to_parse:
            file_as_lines = file_to_parse.readlines()

        self.read_lines, self.read_index, did_line_end_in_newline = [], 0, True
        for next_line in file_as_lines:
            did_line_end_in_newline = next_line.endswith(ParserHelper.newline_character)
            if did_line_end_in_newline:
                next_line = next_line[0:-1]
            self.read_lines.append(next_line)

        if did_line_end_in_newline:
            self.read_lines.append("")

    def is_at_end_of_file(self):
        """
        Whether the provider has reached the end of the input.
        """
        return self.read_index >= len(self.read_lines)

    def get_next_line(self):
        """
        Get the next line from the source provider.
        """
        token_to_use = None
        if not self.is_at_end_of_file():
            token_to_use = self.read_lines[self.read_index]
            self.read_index += 1
        return token_to_use
