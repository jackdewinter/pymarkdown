"""
Module to provide a tokenization of a markdown-encoded string.
"""

from abc import ABC, abstractmethod
from typing import List, Optional

from pymarkdown.general.parser_helper import ParserHelper


class SourceProvider(ABC):
    """
    Class to provide for an abstract definition of an instance that provides
    information about the input source.
    """

    @abstractmethod
    def is_at_end_of_file(self) -> bool:
        """
        Whether the provider has reached the end of the input.
        """

    @abstractmethod
    def get_next_line(self) -> Optional[str]:
        """
        Get the next line from the source provider.
        """


class InMemorySourceProvider(SourceProvider):
    """
    Class to provide for a source provider that is totally within memory.
    """

    def __init__(self, source_text: str) -> None:
        self.__next_line_tuple: List[str] = source_text.split(
            ParserHelper.newline_character, 1
        )

    def is_at_end_of_file(self) -> bool:
        """
        Whether the provider has reached the end of the input.
        """
        return not self.__next_line_tuple

    def get_next_line(self) -> Optional[str]:
        """
        Get the next line from the source provider.
        """
        token_to_use = None
        if not self.is_at_end_of_file():
            token_to_use = self.__next_line_tuple[0]
            if len(self.__next_line_tuple) == 2:
                self.__next_line_tuple = self.__next_line_tuple[1].split(
                    ParserHelper.newline_character, 1
                )
            else:
                assert self.__next_line_tuple
                self.__next_line_tuple = []
        return token_to_use


class FileSourceProvider(SourceProvider):
    """
    Class to provide for a source provider that is on media as a file.
    """

    def __init__(self, file_to_open: str) -> None:
        with open(file_to_open, encoding="utf-8") as file_to_parse:
            file_as_lines = file_to_parse.readlines()

        self.__read_lines, self.__read_index, did_line_end_in_newline = [], 0, True
        for next_line in file_as_lines:
            did_line_end_in_newline = next_line.endswith(ParserHelper.newline_character)
            if did_line_end_in_newline:
                next_line = next_line[:-1]
            self.__read_lines.append(next_line)

        if did_line_end_in_newline:
            self.__read_lines.append("")

    def is_at_end_of_file(self) -> bool:
        """
        Whether the provider has reached the end of the input.
        """
        return self.__read_index >= len(self.__read_lines)

    def get_next_line(self) -> Optional[str]:
        """
        Get the next line from the source provider.
        """
        token_to_use = None
        if not self.is_at_end_of_file():
            token_to_use = self.__read_lines[self.__read_index]
            self.__read_index += 1
        return token_to_use

    def reset_to_start(self) -> None:
        """
        Reset the provider to the start of the stream.
        """
        self.__read_index = 0
