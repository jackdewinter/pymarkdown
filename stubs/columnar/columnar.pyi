import io
import re
from typing import Any, List, Sequence, Tuple, Union

from wcwidth import wcwidth as wcwidth

from .exceptions import TableOverflowError as TableOverflowError

NonWrappedCell = str
WrappedCellLine = str
Data = List[List[NonWrappedCell]]
Headers = List[str]
LogicalRow = List[List[WrappedCellLine]]

class Columnar:
    wrap_max: Any
    max_column_width: Any
    min_column_width: Any
    justify: Any
    head: Any
    terminal_width: Any
    row_sep: Any
    column_sep: Any
    header_sep: str
    patterns: Any
    ansi_color_pattern: Any
    color_reset: str
    color_grid: Any
    drop: Any
    select: Any
    no_borders: Any
    no_headers: Any
    def __call__(
        self,
        data: Sequence[Sequence[Any]],
        headers: Union[None, Sequence[Any]] = ...,
        head: int = ...,
        justify: Union[str, List[str]] = ...,
        wrap_max: int = ...,
        max_column_width: Union[None, int] = ...,
        min_column_width: int = ...,
        row_sep: str = ...,
        column_sep: str = ...,
        patterns: Sequence[str] = ...,
        drop: Sequence[str] = ...,
        select: Sequence[str] = ...,
        no_borders: bool = ...,
        terminal_width: Union[None, int] = ...,
        preformatted_headers: bool = ...,
    ) -> str: ...
    def write_row_separators(
        self, out_stream: io.StringIO, column_widths: Sequence[int]
    ) -> None: ...
    def compile_patterns(self, patterns: List[Any]) -> List[Tuple[re.Pattern, Any]]: ...  # type: ignore
    def colorize(self, text: str, code: str) -> str: ...
    def clean_data(self, data: Sequence[Sequence[Any]]) -> Data: ...
    def filter_columns(self, data: Data, headers: Headers) -> Tuple[Data, Headers]: ...
    def convert_data_to_logical_rows(self, full_data: Data) -> List[LogicalRow]: ...
    def apply_patterns(self, cell_text: str) -> str: ...
    def strip_color(self, cell_text: str) -> str: ...
    def distribute_between(
        self, diff: int, columns: List[dict], n: int  # type: ignore
    ) -> List[dict]: ...  # type: ignore
    def widths_sorted_by(self, columns: List[dict], key: str) -> List[int]: ...  # type: ignore
    def current_table_width(self, columns: List[dict]) -> int: ...  # type: ignore
    def get_column_widths(self, logical_rows: List[LogicalRow]) -> List[int]: ...
    def wrap_and_truncate_logical_cells(
        self, logical_rows: List[LogicalRow], column_widths: List[int]
    ) -> List[LogicalRow]: ...
    def visual_justify(self, text: str, width: int, alignment: str) -> str: ...
