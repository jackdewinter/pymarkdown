"""
Module to provide a tokenization of a markdown-encoded string.
"""


# pylint: disable=too-few-public-methods
class InMemorySourceProvider:
    """
    Class to provide for a source provider that is totally within memory.
    """

    def __init__(self, source_text):
        self.source_text = source_text
        self.next_token = self.source_text.split("\n", 1)

    def get_next_line(self):
        """
        Get the next line from the source provider.
        """
        token_to_use = None
        if self.next_token:
            if len(self.next_token) == 2:
                token_to_use = self.next_token[0]
                self.next_token = self.next_token[1].split("\n", 1)
            else:
                assert self.next_token
                token_to_use = self.next_token[0]
                self.next_token = None
        return token_to_use


# pylint: enable=too-few-public-methods


# pylint: disable=too-few-public-methods
class FileSourceProvider:
    """
    Class to provide for a source provider that is on media as a file.
    """

    def __init__(self, file_to_open):
        with open(file_to_open, encoding="utf-8") as file_to_parse:
            file_as_lines = file_to_parse.readlines()

        self.read_lines = []
        self.read_index = 0
        did_line_end_in_newline = False
        for next_line in file_as_lines:
            did_line_end_in_newline = next_line.endswith("\n")
            if did_line_end_in_newline:
                next_line = next_line[0:-1]
            self.read_lines.append(next_line)

        if did_line_end_in_newline or not self.read_lines:
            self.read_lines.append("")

    def get_next_line(self):
        """
        Get the next line from the source provider.
        """
        token_to_use = None
        if self.read_index < len(self.read_lines):
            token_to_use = self.read_lines[self.read_index]
            self.read_index += 1
        return token_to_use


# pylint: enable=too-few-public-methods
