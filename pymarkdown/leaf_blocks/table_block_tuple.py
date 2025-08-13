from dataclasses import dataclass
from typing import List, Optional

from pymarkdown.general.parser_helper import ParserHelper


@dataclass
class TableColumn:
    text: str
    leading_whitespace: str
    trailing_whitespace: str

    def __init__(self, text: str, is_last: bool = False):
        new_start_index, leading_whitespace = ParserHelper.collect_while_spaces(text, 0)
        assert new_start_index is not None
        assert leading_whitespace is not None
        self.leading_whitespace = leading_whitespace
        d = len(text) - 1 if (text[-1] == "|" and not is_last) else len(text)
        _, new_end_index = ParserHelper.collect_backwards_while_spaces(text, d)
        assert new_end_index is not None
        self.trailing_whitespace = text[new_end_index:]
        self.text = text[new_start_index:new_end_index]


@dataclass
class TableRow:
    extracted_whitespace: str
    trailing_whitespace: str
    columns: List[TableColumn]
    end_of_row: Optional[str]
    did_start_with_separator: bool


@dataclass(frozen=True)
class TableTuple:
    """
    Class to hold the tuple of information for creating a Table.
    """

    normalized_destination: Optional[str]
    xyz: List[TableRow]
    col_as: List[Optional[str]]
