"""
Module to implement a plugin that prevents different forms of links and images from being used.
"""

import re
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Optional, cast

from wcwidth import wcswidth

try:
    from typing import override  # Python 3.12+
except ImportError:
    from typing_extensions import override  # Older versions

from pymarkdown.general.parser_helper import ParserHelper
from pymarkdown.plugin_manager.plugin_details import (
    PluginDetailsV2,
    PluginDetailsV3,
    QueryConfigItem,
)
from pymarkdown.plugin_manager.plugin_scan_context import PluginScanContext
from pymarkdown.plugin_manager.rule_plugin import RulePlugin
from pymarkdown.tokens.emphasis_markdown_token import EmphasisMarkdownToken
from pymarkdown.tokens.image_start_markdown_token import ImageStartMarkdownToken
from pymarkdown.tokens.inline_code_span_markdown_token import (
    InlineCodeSpanMarkdownToken,
)
from pymarkdown.tokens.link_start_markdown_token import LinkStartMarkdownToken
from pymarkdown.tokens.markdown_token import EndMarkdownToken, MarkdownToken
from pymarkdown.tokens.raw_html_markdown_token import RawHtmlMarkdownToken
from pymarkdown.tokens.table_markdown_tokens import (
    TableMarkdownHeaderItemToken,
    TableMarkdownHeaderToken,
    TableMarkdownRowToken,
)
from pymarkdown.tokens.text_markdown_token import TextMarkdownToken
from pymarkdown.tokens.uri_autolink_markdown_token import UriAutolinkMarkdownToken


@dataclass
class CollectedTableHeaderItem:
    """One of the header items for the current table."""

    start_token: TableMarkdownHeaderItemToken
    end_token: EndMarkdownToken
    inner_tokens: List[MarkdownToken]


@dataclass
class CollectedTableHeader:
    """Header for the current table."""

    table_header_token: TableMarkdownHeaderToken
    header_columns: List[CollectedTableHeaderItem]

    def __init__(self, table_header_token: TableMarkdownHeaderToken) -> None:
        self.table_header_token = table_header_token
        self.header_columns = []


@dataclass
class CollectedTableSingleRow:
    """Single row collected as part of the current table."""

    table_row_token: TableMarkdownRowToken
    row_columns: List[CollectedTableHeaderItem]

    def __init__(
        self, table_row_token: TableMarkdownRowToken, did_start_with_separator: bool
    ) -> None:
        self.table_row_token = table_row_token
        self.row_columns = []
        self.did_start_with_separator = did_start_with_separator


@dataclass
class CollectedTableRows:
    """Collected table rows for the current table."""

    table_rows: List[CollectedTableSingleRow]

    def __init__(self) -> None:
        self.table_rows = []


class RuleMd060States(Enum):
    """
    Enumeration to provide guidance on what to look for as the tokens come in.
    """

    LOOK_FOR_TABLE_START = 0
    LOOK_FOR_TABLE_HEADER = 1
    LOOK_FOR_TABLE_HEADER_ITEM_START = 2
    LOOK_FOR_TABLE_HEADER_ITEM_END = 3
    LOOK_FOR_TABLE_ROW_START = 4
    LOOK_FOR_TABLE_ROW_END = 5
    LOOK_FOR_TABLE_ROW_ITEM_START = 6
    LOOK_FOR_TABLE_ROW_ITEM_END = 7
    LOOK_FOR_TABLE_END = 20


@dataclass
class FoundError:
    """Record of an error found by this rule."""

    line_number: int
    column_number: int
    error_reason: str
    is_aligned_override: bool


class TableStyleEvaluator(ABC):
    """Class to provide for independent evaluation of a table's style."""

    def __init__(self) -> None:
        self.__did_start = False
        self.__did_end = False
        self.__title_separator_column_numbers: List[int] = []

    @property
    @abstractmethod
    def name(self) -> str:
        """Name of the style evaluator."""

    @abstractmethod
    def evaluate(
        self,
        headers: CollectedTableHeader,
        table_header_token: CollectedTableRows,
        aligned_delimiter_if_not_aligned: bool,
    ) -> List[FoundError]:
        """Evaluation method to determine what style issues are present with the
        table.
        """

    # Regex to match ANSI escape sequences
    ANSI_ESCAPE_RE = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")

    def __safe_string_length(self, string_to_measure: str) -> int:
        """Implemented as a Python version of NPM's string-width."""

        # Remove ANSI escape sequences and other non-printable control characters. Note that
        # most important control characters will already be escaped or dealt with, leaving
        # what should be a shortened list of characters to deal with.
        cleansed_string = "".join(
            ch
            for ch in TableStyleEvaluator.ANSI_ESCAPE_RE.sub("", string_to_measure)
            if ch.isprintable()
        )

        # If we have missed a printable character, there is a chance that the function will return -1,
        # so handle that gracefully.
        return max(wcswidth(cleansed_string), 0)

    def _skip_over_inline_tokens(self, header_item: CollectedTableHeaderItem) -> int:
        data_length = 0
        for next_inline_token in header_item.inner_tokens:
            if next_inline_token.is_text:
                text_token = cast(TextMarkdownToken, next_inline_token)
                data_length += self.__safe_string_length(
                    ParserHelper.remove_all_from_text(text_token.token_text)
                )
            elif next_inline_token.is_inline_code_span:
                code_span_token = cast(InlineCodeSpanMarkdownToken, next_inline_token)
                data_length += (
                    self.__safe_string_length(code_span_token.span_text)
                    + (2 * len(code_span_token.extracted_start_backticks))
                    + len(code_span_token.leading_whitespace)
                    + len(code_span_token.trailing_whitespace)
                )
            elif next_inline_token.is_inline_emphasis:
                emphasis_start_token = cast(EmphasisMarkdownToken, next_inline_token)
                data_length += len(emphasis_start_token.emphasis_character)
            elif next_inline_token.is_inline_emphasis_end:
                end_token = cast(EndMarkdownToken, next_inline_token)
                emphasis_end_token = cast(
                    EmphasisMarkdownToken, end_token.start_markdown_token
                )
                data_length += len(emphasis_end_token.emphasis_character)
            elif next_inline_token.is_inline_raw_html:
                raw_html_token = cast(RawHtmlMarkdownToken, next_inline_token)
                data_length += len(raw_html_token.raw_tag) + 2
            elif next_inline_token.is_inline_autolink:
                autolink_token = cast(UriAutolinkMarkdownToken, next_inline_token)
                data_length += len(autolink_token.autolink_text) + 2
            elif next_inline_token.is_inline_link:
                data_length += self.__skip_over_inline_link_token(
                    cast(LinkStartMarkdownToken, next_inline_token)
                )
            elif next_inline_token.is_inline_image:
                data_length += self.__skip_over_inline_image_token(
                    cast(ImageStartMarkdownToken, next_inline_token)
                )
            else:
                assert next_inline_token.is_inline_link_end
        return data_length

    def __skip_over_inline_link_token(self, link_token: LinkStartMarkdownToken) -> int:
        data_length = 0
        if link_token.label_type == "full":
            assert link_token.ex_label is not None
            data_length += 4 + len(link_token.ex_label)
        elif link_token.label_type == "collapsed":
            data_length += 4
        elif link_token.label_type == "shortcut":
            data_length += 2
        else:
            assert link_token.label_type == "inline"
            if link_token.active_link_title:
                data_length += 2 + len(link_token.active_link_title)
            assert link_token.after_title_whitespace is not None
            assert link_token.before_link_whitespace is not None
            assert link_token.before_title_whitespace is not None
            data_length += (
                4
                + len(link_token.active_link_uri)
                + len(link_token.after_title_whitespace)
                + len(link_token.before_link_whitespace)
                + len(link_token.before_title_whitespace)
            )
        return data_length

    def __skip_over_inline_image_token(
        self, image_token: ImageStartMarkdownToken
    ) -> int:

        data_length = 0
        if image_token.label_type == "full":
            assert image_token.ex_label is not None
            block_text = ParserHelper.remove_all_from_text(image_token.text_from_blocks)
            data_length += 5 + len(image_token.ex_label) + len(block_text)
        elif image_token.label_type == "collapsed":
            block_text = ParserHelper.remove_all_from_text(image_token.text_from_blocks)
            data_length += 5 + len(block_text)
        elif image_token.label_type == "shortcut":
            block_text = ParserHelper.remove_all_from_text(image_token.text_from_blocks)
            data_length += 3 + len(block_text)
        else:
            assert image_token.label_type == "inline"
            block_text = ParserHelper.remove_all_from_text(image_token.text_from_blocks)
            if image_token.active_link_title:
                data_length += 2 + len(image_token.active_link_title)
            assert image_token.after_title_whitespace is not None
            assert image_token.before_link_whitespace is not None
            assert image_token.before_title_whitespace is not None
            data_length += (
                5
                + len(block_text)
                + len(image_token.active_link_uri)
                + len(image_token.after_title_whitespace)
                + len(image_token.before_link_whitespace)
                + len(image_token.before_title_whitespace)
            )
        return data_length

    def _evaluate_title_row_for_alignment(
        self,
        header_columns: List[CollectedTableHeaderItem],
        table_header_token: TableMarkdownHeaderToken,
    ) -> None:

        did_header_row_start_with_separator = (
            table_header_token.did_header_row_start_with_separator
        )
        header_row_leading_whitespace = table_header_token.header_row_leading_whitespace
        self.__title_separator_column_numbers.clear()
        start_column_number = table_header_token.column_number - len(
            table_header_token.header_row_leading_whitespace
        )
        effective_column_number = len(header_row_leading_whitespace)
        if did_header_row_start_with_separator:
            self.__title_separator_column_numbers.append(
                effective_column_number + start_column_number
            )
            effective_column_number += 1
        did_end_with_separator = False
        for _, column_header_item in enumerate(header_columns):
            effective_column_number += len(
                column_header_item.start_token.extracted_whitespace
            )
            effective_column_number += self._skip_over_inline_tokens(column_header_item)

            end_token_ws = column_header_item.end_token.extracted_whitespace
            did_end_with_separator = end_token_ws.endswith("|")
            if did_end_with_separator:
                end_token_ws = end_token_ws[:-1]
            effective_column_number += len(end_token_ws)
            if did_end_with_separator:
                self.__title_separator_column_numbers.append(
                    effective_column_number + start_column_number
                )
                effective_column_number += 1
        self.__did_start = did_header_row_start_with_separator
        self.__did_end = did_end_with_separator

    def _evaluate_separator_row_for_alignment(
        self,
        errors: List[FoundError],
        table_header_token: TableMarkdownHeaderToken,
        aligned_delimiter_if_not_aligned: bool,
    ) -> None:

        line_split_columns = table_header_token.separator_line.split("|")
        init_column_number = table_header_token.column_number - len(
            table_header_token.header_row_leading_whitespace
        )
        tracking_column_number = init_column_number
        did_start_with_separator = False
        has_end_with_separator = False
        separator_column_numbers: List[int] = []
        for column_index, column_text in enumerate(line_split_columns):
            if (
                column_index == len(line_split_columns) - 1
                and line_split_columns[-1].strip() == ""
            ):
                has_end_with_separator = True
                continue
            if column_index == 0 and line_split_columns[0].strip() == "":
                tracking_column_number += len(line_split_columns[0])
                did_start_with_separator = True
                separator_column_numbers.append(tracking_column_number)
                tracking_column_number += 1
                continue

            tracking_column_number += len(column_text)
            if column_index != len(line_split_columns) - 1:
                separator_column_numbers.append(tracking_column_number)
                tracking_column_number += 1
        self._compare_against_aligned_title_row(
            errors,
            separator_column_numbers,
            did_start_with_separator,
            has_end_with_separator,
            1,
            tracking_column_number,
            init_column_number,
            aligned_delimiter_if_not_aligned,
        )

    # pylint: disable=too-many-arguments
    def _compare_against_aligned_title_row(
        self,
        errors: List[FoundError],
        separator_column_numbers: List[int],
        did_start_with_separator: bool,
        did_end_with_separator: bool,
        row_count: int,
        col_count: int,
        init_col_count: int,
        aligned_delimiter_if_not_aligned: bool,
    ) -> None:

        title_index = 0
        title_end = len(self.__title_separator_column_numbers)
        current_index = 0
        current_end = len(separator_column_numbers)
        if did_start_with_separator != self.__did_start:
            errors.append(
                FoundError(
                    row_count,
                    init_col_count,
                    f"Expected-Leading: {self.__did_start} Actual-Leading: {did_start_with_separator}",
                    aligned_delimiter_if_not_aligned,
                )
            )
            if self.__did_start:
                title_index += 1
            else:
                current_index += 1
        if did_end_with_separator != self.__did_end:
            errors.append(
                FoundError(
                    row_count,
                    col_count,
                    f"Expected-Trailing: {self.__did_end} Actual-Trailing: {did_end_with_separator}",
                    aligned_delimiter_if_not_aligned,
                )
            )
            if did_end_with_separator:
                current_end -= 1
            else:
                title_end -= 1

        while current_index < current_end:
            title_value = self.__title_separator_column_numbers[title_index]
            current_value = separator_column_numbers[current_index]
            if title_value != current_value:
                errors.append(
                    FoundError(
                        row_count,
                        current_value,
                        f"Expected-Column: {title_value} Actual-Column: {current_value}",
                        aligned_delimiter_if_not_aligned,
                    )
                )

            current_index += 1
            title_index += 1
        # assert current_index == current_end
        # assert title_index == title_end

    # pylint: enable=too-many-arguments


class SimpleStyleEvaluator(TableStyleEvaluator):
    """Base class to handle simple evaluations."""

    def __init__(self, expect_value: int) -> None:
        super().__init__()
        self.__expect_value = expect_value

    def __evaluate_title_row(
        self,
        errors: List[FoundError],
        header_columns: List[CollectedTableHeaderItem],
        did_header_row_start_with_separator: bool,
    ) -> None:

        for column_index, column_header_item in enumerate(header_columns):
            if len(
                column_header_item.start_token.extracted_whitespace
            ) != self.__expect_value and not (
                column_index == 0 and not did_header_row_start_with_separator
            ):
                errors.append(
                    FoundError(
                        0,
                        column_header_item.start_token.column_number
                        - len(column_header_item.start_token.extracted_whitespace),
                        f"Expected-Whitespace: {self.__expect_value} Actual-Whitespace: {len(column_header_item.start_token.extracted_whitespace)}",
                        False,
                    )
                )

            data_length = self._skip_over_inline_tokens(column_header_item)

            end_token_ws = column_header_item.end_token.extracted_whitespace
            did_end_with_separator = end_token_ws.endswith("|")
            if did_end_with_separator:
                end_token_ws = end_token_ws[:-1]
            if len(end_token_ws) != self.__expect_value and did_end_with_separator:
                errors.append(
                    FoundError(
                        0,
                        column_header_item.start_token.column_number + data_length,
                        f"Expected-Whitespace: {self.__expect_value} Actual-Whitespace: {len(end_token_ws)}",
                        False,
                    )
                )

    def __evaluate_separator_row(
        self,
        errors: List[FoundError],
        table_header_token: TableMarkdownHeaderToken,
    ) -> None:

        line_split_columns = table_header_token.separator_line.split("|")
        col_count = table_header_token.column_number - len(
            table_header_token.header_row_leading_whitespace
        )
        for column_index, column_text in enumerate(line_split_columns):
            if (
                column_index == len(line_split_columns) - 1
                and line_split_columns[-1].strip() == ""
            ):
                continue
            if column_index == 0 and line_split_columns[0].strip() == "":
                col_count += len(line_split_columns[0])
                continue
            num_leading_characters, new_index = (
                ParserHelper.collect_while_character_verified(column_text, 0, " ")
            )
            consumed_text_count = 0
            if ParserHelper.is_character_at_index(column_text, new_index, ":"):
                new_index += 1
                consumed_text_count += 1
            num_column_characters, new_index = (
                ParserHelper.collect_while_character_verified(
                    column_text, new_index, "-"
                )
            )
            if ParserHelper.is_character_at_index(column_text, new_index, ":"):
                new_index += 1
                consumed_text_count += 1
            num_column_characters += consumed_text_count
            num_trailing_characters, new_index = (
                ParserHelper.collect_while_character_verified(
                    column_text, new_index, " "
                )
            )
            assert new_index == len(column_text)

            col_count = self.__evaluate_separator_row_find_errors(
                errors,
                line_split_columns,
                column_index,
                col_count,
                num_leading_characters,
                num_column_characters,
                num_trailing_characters,
            )
            col_count += num_trailing_characters

    # pylint: disable=too-many-arguments
    def __evaluate_separator_row_find_errors(
        self,
        errors: List[FoundError],
        line_split_columns: List[str],
        column_index: int,
        col_count: int,
        num_leading_characters: int,
        num_column_characters: int,
        num_trailing_characters: int,
    ) -> int:
        if column_index != 0:
            col_count += 1
        if num_leading_characters != self.__expect_value and column_index != 0:
            errors.append(
                FoundError(
                    1,
                    col_count,
                    f"Expected-Whitespace: {self.__expect_value} Actual-Whitespace: {num_leading_characters}",
                    False,
                )
            )
        col_count += num_leading_characters
        if num_column_characters != 3:
            errors.append(
                FoundError(
                    1,
                    col_count,
                    f"Expected-Delimeters: 3 Actual-Delimeters: {num_column_characters}",
                    False,
                )
            )
        col_count += num_column_characters
        if (
            num_trailing_characters != self.__expect_value
            and column_index != len(line_split_columns) - 1
        ):
            errors.append(
                FoundError(
                    1,
                    col_count,
                    f"Expected-Whitespace: {self.__expect_value} Actual-Whitespace: {num_trailing_characters}",
                    False,
                )
            )
        return col_count

    # pylint: enable=too-many-arguments

    def __evaluate_normal_row(
        self,
        errors: List[FoundError],
        row_index: int,
        collected_row: CollectedTableSingleRow,
    ) -> None:
        for column_index, row_column_item in enumerate(collected_row.row_columns):

            if len(
                row_column_item.start_token.extracted_whitespace
            ) != self.__expect_value and not (
                column_index == 0 and not collected_row.did_start_with_separator
            ):
                errors.append(
                    FoundError(
                        row_index + 2,
                        row_column_item.start_token.column_number
                        - len(row_column_item.start_token.extracted_whitespace),
                        f"Expected-Whitespace: {self.__expect_value} Actual-Whitespace: {len(row_column_item.start_token.extracted_whitespace)}",
                        False,
                    )
                )

            data_length = self._skip_over_inline_tokens(row_column_item)

            end_token_ws = row_column_item.end_token.extracted_whitespace
            did_end_with_separator = end_token_ws.endswith("|")
            if did_end_with_separator:
                end_token_ws = end_token_ws[:-1]
            if len(end_token_ws) != self.__expect_value and did_end_with_separator:
                errors.append(
                    FoundError(
                        row_index + 2,
                        row_column_item.start_token.column_number + data_length,
                        f"Expected-Whitespace: {self.__expect_value} Actual-Whitespace: {len(end_token_ws)}",
                        False,
                    )
                )

    @override
    def evaluate(
        self,
        headers: CollectedTableHeader,
        table_header_token: CollectedTableRows,
        aligned_delimiter_if_not_aligned: bool,
    ) -> List[FoundError]:
        """blah"""
        errors: List[FoundError] = []

        self.__evaluate_title_row(
            errors,
            headers.header_columns,
            headers.table_header_token.did_header_row_start_with_separator,
        )
        self._evaluate_title_row_for_alignment(
            headers.header_columns, headers.table_header_token
        )

        if aligned_delimiter_if_not_aligned:
            self._evaluate_separator_row_for_alignment(
                errors, headers.table_header_token, aligned_delimiter_if_not_aligned
            )
        else:
            self.__evaluate_separator_row(errors, headers.table_header_token)
        for row_index, collected_row in enumerate(table_header_token.table_rows):
            self.__evaluate_normal_row(errors, row_index, collected_row)
        return errors


class CompactStyleEvaluator(SimpleStyleEvaluator):
    """Class to implement a the evaluator for the 'compact' style."""

    def __init__(self) -> None:
        super().__init__(1)

    @property
    @override
    def name(self) -> str:
        return "compact"


class TightStyleEvaluator(SimpleStyleEvaluator):
    """Class to implement a the evaluator for the 'tight' style."""

    def __init__(self) -> None:
        super().__init__(0)

    @property
    @override
    def name(self) -> str:
        return "tight"


class AlignedStyleEvaluator(TableStyleEvaluator):
    """Class to implement a the evaluator for the 'aligned' style."""

    @property
    @override
    def name(self) -> str:
        return "aligned"

    def __evaluate_normal_row(
        self,
        errors: List[FoundError],
        row_index: int,
        collected_row: CollectedTableSingleRow,
    ) -> None:

        did_start_with_separator = False
        did_end_with_separator = False
        separator_column_numbers: List[int] = []
        tracking_column_number = collected_row.table_row_token.column_number
        init_column_number = tracking_column_number
        for column_index, row_column_item in enumerate(collected_row.row_columns):

            if column_index == 0:
                did_start_with_separator = collected_row.did_start_with_separator
                if did_start_with_separator:
                    separator_column_numbers.append(tracking_column_number)
                    tracking_column_number += 1

            tracking_column_number += len(
                row_column_item.start_token.extracted_whitespace
            )
            tracking_column_number += self._skip_over_inline_tokens(row_column_item)
            tracking_column_number += len(
                row_column_item.end_token.extracted_whitespace
            )

            if row_column_item.end_token.extracted_whitespace.endswith("|"):
                separator_column_numbers.append(tracking_column_number - 1)
                if column_index == len(collected_row.row_columns) - 1:
                    did_end_with_separator = True
        self._compare_against_aligned_title_row(
            errors,
            separator_column_numbers,
            did_start_with_separator,
            did_end_with_separator,
            row_index + 2,
            tracking_column_number,
            init_column_number,
            False,
        )

    @override
    def evaluate(
        self,
        headers: CollectedTableHeader,
        table_header_token: CollectedTableRows,
        aligned_delimiter_if_not_aligned: bool,
    ) -> List[FoundError]:
        errors: List[FoundError] = []
        self._evaluate_title_row_for_alignment(
            headers.header_columns, headers.table_header_token
        )
        self._evaluate_separator_row_for_alignment(
            errors, headers.table_header_token, False
        )
        for row_index, collected_row in enumerate(table_header_token.table_rows):
            self.__evaluate_normal_row(errors, row_index, collected_row)
        return errors


# pylint: disable=too-many-instance-attributes
class RuleMd060(RulePlugin):
    """
    Class to implement a plugin that prevents different forms of links and images from being used.
    """

    __any_style = "any"
    __valid_styles: Dict[str, TableStyleEvaluator] = {
        TightStyleEvaluator().name: TightStyleEvaluator(),
        CompactStyleEvaluator().name: CompactStyleEvaluator(),
        AlignedStyleEvaluator().name: AlignedStyleEvaluator(),
    }

    def __init__(self) -> None:
        """
        Initialize an instance of the RuleMd048 class.
        """
        super().__init__()
        self.__style_type = TightStyleEvaluator().name
        self.__actual_style = ""
        self.__state = RuleMd060States.LOOK_FOR_TABLE_START
        self.__start_token: Optional[MarkdownToken] = None
        self.__end_token: Optional[MarkdownToken] = None
        self.__header: Optional[CollectedTableHeader] = None
        self.__inner_tokens: List[MarkdownToken] = []
        self.__current_row: Optional[CollectedTableSingleRow] = None
        self.__table_rows: Optional[CollectedTableRows] = None
        self.__aligned_delimiter_if_not_aligned = False

    def get_details(self) -> PluginDetailsV2:
        """
        Get the details for the plugin.
        """
        return PluginDetailsV3(
            plugin_name="table-column-style",
            plugin_id="MD060",
            plugin_enabled_by_default=True,
            plugin_description="Table column style.",
            plugin_version="0.5.0",
            plugin_url="https://pymarkdown.readthedocs.io/en/latest/plugins/rule_md060.md",
            plugin_configuration="style",
        )

    @classmethod
    def __validate_configuration_style(cls, found_value: str) -> None:
        if (
            found_value != RuleMd060.__any_style
            and found_value not in RuleMd060.__valid_styles
        ):
            allowed_keys: List[str] = [RuleMd060.__any_style]
            allowed_keys.extend(RuleMd060.__valid_styles.keys())
            raise ValueError(f"Allowable values: {allowed_keys}.")

    def initialize_from_config(self) -> None:
        """
        Event to allow the plugin to load configuration information.
        """
        self.__style_type = self.plugin_configuration.get_string_property_with_default(
            "style",
            RuleMd060.__any_style,
            valid_value_fn=self.__validate_configuration_style,
        )
        self.__aligned_delimiter_if_not_aligned = (
            self.plugin_configuration.get_boolean_property_with_default(
                "aligned_delimiter", False
            )
        )

    def query_config(self) -> List[QueryConfigItem]:
        """
        Query to find out the configuration that the rule is using.
        """
        return [
            QueryConfigItem("style", self.__style_type),
            QueryConfigItem(
                "aligned_delimiter", self.__aligned_delimiter_if_not_aligned
            ),
        ]

    def starting_new_file(self) -> None:
        """
        Event that the a new file to be scanned is starting.
        """
        self.__state = RuleMd060States.LOOK_FOR_TABLE_START
        self.__start_token = None
        self.__end_token = None

        self.__table_rows = CollectedTableRows()
        self.__header = None
        self.__inner_tokens = []
        self.__current_row = None

        self.__actual_style = self.__style_type
        # TODO if implementing consistent style, use this
        # self.__actual_style_type = (
        #     self.__style_type
        #     if self.__style_type != RuleMd050.__consistent_style
        #     else ""
        # )

    def __process_header_item(self) -> None:
        assert self.__start_token is not None
        assert self.__end_token is not None
        assert self.__header is not None
        header_item_start_token = cast(TableMarkdownHeaderItemToken, self.__start_token)
        header_item_end_token = cast(EndMarkdownToken, self.__end_token)
        self.__header.header_columns.append(
            CollectedTableHeaderItem(
                header_item_start_token, header_item_end_token, self.__inner_tokens[:]
            )
        )

    def __process_column_item(self) -> None:
        assert self.__start_token is not None
        assert self.__end_token is not None
        assert self.__current_row is not None

        header_item_start_token = cast(TableMarkdownHeaderItemToken, self.__start_token)
        header_item_end_token = cast(EndMarkdownToken, self.__end_token)
        self.__current_row.row_columns.append(
            CollectedTableHeaderItem(
                header_item_start_token, header_item_end_token, self.__inner_tokens[:]
            )
        )

    def __process_row_columns(self) -> None:
        assert self.__current_row is not None
        assert self.__table_rows is not None
        self.__table_rows.table_rows.append(self.__current_row)
        self.__current_row = None

    def __generate_rule_failures_from_style_errors(
        self,
        context: PluginScanContext,
        token: MarkdownToken,
        style_errors: List[FoundError],
        initial_line_number: int,
        reported_style: str,
    ) -> None:
        for next_style_error in style_errors:
            effective_style = (
                "aligned-delimiter"
                if next_style_error.is_aligned_override
                else reported_style
            )
            self.report_next_token_error(
                context,
                token,
                line_number_delta=initial_line_number + next_style_error.line_number,
                column_number_delta=-next_style_error.column_number,
                extra_error_information=f"Style: {effective_style} {next_style_error.error_reason}",
            )

    def __process_entire_table(
        self, context: PluginScanContext, token: MarkdownToken
    ) -> None:
        # sourcery skip: extract-method
        assert self.__header is not None
        assert self.__table_rows is not None
        initial_line_number = self.__header.table_header_token.line_number
        if self.__actual_style == RuleMd060.__any_style:
            style_errors = []
            min_found = -1
            max_errors = []
            max_name = ""
            for style_name, style_evaluator in RuleMd060.__valid_styles.items():
                style_errors = style_evaluator.evaluate(
                    self.__header,
                    self.__table_rows,
                    self.__aligned_delimiter_if_not_aligned,
                )
                if min_found == -1 or len(style_errors) < min_found:
                    min_found = len(style_errors)
                    max_name = style_name
                    max_errors = style_errors
            self.__generate_rule_failures_from_style_errors(
                context, token, max_errors, initial_line_number, max_name
            )
        else:
            style_evaluator = RuleMd060.__valid_styles[self.__actual_style]
            style_errors = style_evaluator.evaluate(
                self.__header,
                self.__table_rows,
                self.__aligned_delimiter_if_not_aligned,
            )
            self.__generate_rule_failures_from_style_errors(
                context, token, style_errors, initial_line_number, self.__actual_style
            )

    def __handle_state_look_for_table_start(self, token: MarkdownToken) -> None:
        if token.is_table:
            self.__table_rows = CollectedTableRows()
            self.__header = None
            self.__current_row = None
            self.__start_token = None
            self.__inner_tokens = []
            self.__end_token = None
            self.__state = RuleMd060States.LOOK_FOR_TABLE_HEADER

    def __handle_state_look_for_table_header(self, token: MarkdownToken) -> None:
        assert token.is_table_header
        self.__header = CollectedTableHeader(cast(TableMarkdownHeaderToken, token))
        self.__state = RuleMd060States.LOOK_FOR_TABLE_HEADER_ITEM_START

    def __handle_state_look_for_table_header_item_start(
        self, token: MarkdownToken
    ) -> None:
        if token.is_table_header_item:
            self.__start_token = token
            self.__inner_tokens.clear()
            self.__end_token = None
            self.__state = RuleMd060States.LOOK_FOR_TABLE_HEADER_ITEM_END
        else:
            assert token.is_table_header_end
            self.__state = RuleMd060States.LOOK_FOR_TABLE_ROW_START

    def __handle_state_look_for_table_header_item_end(
        self, token: MarkdownToken
    ) -> None:
        if token.is_table_header_item_end:
            self.__state = RuleMd060States.LOOK_FOR_TABLE_HEADER_ITEM_START
            self.__end_token = token
            self.__process_header_item()
        else:
            self.__inner_tokens.append(token)

    def __handle_state_look_for_table_row_start(
        self, context: PluginScanContext, token: MarkdownToken
    ) -> None:
        if token.is_table_row:
            table_row_token = cast(TableMarkdownRowToken, token)
            self.__current_row = CollectedTableSingleRow(
                table_row_token, table_row_token.did_start_with_separator
            )
            self.__state = RuleMd060States.LOOK_FOR_TABLE_ROW_END
        elif token.is_table_end:
            self.__state = RuleMd060States.LOOK_FOR_TABLE_START
            self.__process_entire_table(context, token)

    def __handle_state_look_for_table_row_end(self, token: MarkdownToken) -> None:
        if token.is_table_row_item:
            self.__start_token = token
            self.__inner_tokens.clear()
            self.__end_token = None
            self.__state = RuleMd060States.LOOK_FOR_TABLE_ROW_ITEM_END
        else:
            assert token.is_table_row_end
            self.__process_row_columns()
            self.__state = RuleMd060States.LOOK_FOR_TABLE_ROW_START

    def __handle_state_look_for_table_row_item_end(self, token: MarkdownToken) -> None:
        if token.is_table_row_item_end:
            self.__end_token = token
            self.__process_column_item()
            self.__state = RuleMd060States.LOOK_FOR_TABLE_ROW_END
        else:
            self.__inner_tokens.append(token)

    def next_token(self, context: PluginScanContext, token: MarkdownToken) -> None:
        """
        Event that a new token is being processed.
        """
        if self.__state == RuleMd060States.LOOK_FOR_TABLE_START:
            self.__handle_state_look_for_table_start(token)
        elif self.__state == RuleMd060States.LOOK_FOR_TABLE_HEADER:
            self.__handle_state_look_for_table_header(token)
        elif self.__state == RuleMd060States.LOOK_FOR_TABLE_HEADER_ITEM_START:
            self.__handle_state_look_for_table_header_item_start(token)
        elif self.__state == RuleMd060States.LOOK_FOR_TABLE_HEADER_ITEM_END:
            self.__handle_state_look_for_table_header_item_end(token)
        elif self.__state == RuleMd060States.LOOK_FOR_TABLE_ROW_START:
            self.__handle_state_look_for_table_row_start(context, token)
        elif self.__state == RuleMd060States.LOOK_FOR_TABLE_ROW_END:
            self.__handle_state_look_for_table_row_end(token)
        else:
            assert self.__state == RuleMd060States.LOOK_FOR_TABLE_ROW_ITEM_END
            self.__handle_state_look_for_table_row_item_end(token)


# pylint: enable=too-many-instance-attributes
