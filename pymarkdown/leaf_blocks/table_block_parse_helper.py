from typing import List, Optional, Tuple

from pymarkdown.container_blocks.container_grab_bag import POGGER
from pymarkdown.general.parser_helper import ParserHelper
from pymarkdown.general.parser_state import ParserState
from pymarkdown.general.tab_helper import TabHelper
from pymarkdown.html.html_helper import HtmlHelper
from pymarkdown.leaf_blocks.atx_leaf_block_processor import AtxLeafBlockProcessor
from pymarkdown.leaf_blocks.fenced_leaf_block_processor import FencedLeafBlockProcessor
from pymarkdown.leaf_blocks.table_block_tuple import TableColumn, TableRow, TableTuple
from pymarkdown.leaf_blocks.thematic_leaf_block_processor import (
    ThematicLeafBlockProcessor,
)
from pymarkdown.links.link_reference_definition_parse_helper import (
    LinkReferenceDefinitionParseHelper,
)


class TableParseHelper:
    __table_column_separator_character = "|"

    @staticmethod
    def __parse_table_1(
        parser_state: ParserState, remaining_line_to_parse: str
    ) -> bool:
        remaining_line_start_index, remaining_line_extracted_whitespace = (
            ParserHelper.extract_spaces_verified(remaining_line_to_parse, 0)
        )

        is_atx, _, _, _ = AtxLeafBlockProcessor.is_atx_heading(
            remaining_line_to_parse,
            remaining_line_start_index,
            remaining_line_extracted_whitespace,
        )
        is_leaf_block_start = is_atx
        if not is_leaf_block_start:
            is_thematic_break_start, _ = ThematicLeafBlockProcessor.is_thematic_break(
                remaining_line_to_parse,
                remaining_line_start_index,
                remaining_line_extracted_whitespace,
            )
            is_leaf_block_start = bool(is_thematic_break_start)
        if not is_leaf_block_start:
            # TODO may have to adjust start_index for tabs
            is_indented_code_block_start = TabHelper.is_length_greater_than_or_equal_to(
                remaining_line_extracted_whitespace, 4, start_index=0
            )
            is_leaf_block_start = is_indented_code_block_start
        if not is_leaf_block_start:
            is_fenced_start, _, _, _, _ = FencedLeafBlockProcessor.is_fenced_code_block(
                parser_state,
                remaining_line_to_parse,
                remaining_line_start_index,
                remaining_line_extracted_whitespace,
                "",  # TODO may have issues with this
                0,
            )
            is_leaf_block_start = is_fenced_start
        if not is_leaf_block_start:
            is_html_start, _ = HtmlHelper.is_html_block(
                remaining_line_to_parse,
                remaining_line_start_index,
                remaining_line_extracted_whitespace,
                parser_state.token_stack,
                parser_state.parse_properties,
            )
            is_leaf_block_start = bool(is_html_start)
        if not is_leaf_block_start:
            is_lrd_start = (
                LinkReferenceDefinitionParseHelper.is_link_reference_definition(
                    parser_state,
                    remaining_line_to_parse,
                    remaining_line_start_index,
                    remaining_line_extracted_whitespace,
                )
            )
            is_leaf_block_start = is_lrd_start

        did_start = not is_leaf_block_start
        return did_start

    @staticmethod
    def parse_table(
        parser_state: ParserState,
        line_to_parse: str,
        start_index: int,
        extracted_whitespace: str,
        is_blank_line: bool,
        remaining_line_to_parse: Optional[str],
        was_started: bool,
    ) -> Tuple[bool, int, Optional[TableTuple]]:

        if was_started:
            if remaining_line_to_parse is not None:
                did_start = TableParseHelper.__parse_table_1(
                    parser_state, remaining_line_to_parse
                )
            else:
                did_start = True
        else:
            did_start = TableParseHelper.__is_table_start(
                parser_state, line_to_parse, start_index, extracted_whitespace
            )
        if not did_start:
            POGGER.debug("BAIL")
            return False, -1, None

        xxxx = TableParseHelper.__table_column_separator_character + "\n"
        # multiple lines

        xyz: List[TableRow] = []
        col_as: List[Optional[str]] = []

        while start_index < len(line_to_parse):

            did_start_with_separator = False
            if ParserHelper.is_character_at_index(
                line_to_parse,
                start_index,
                TableParseHelper.__table_column_separator_character,
            ):
                new_index = start_index + 1
                did_start_with_separator = True
            else:
                new_index = start_index

            tr_columns, trailing_whitespace, pre_h, new_index = (
                TableParseHelper.__parse_table_3(line_to_parse, xxxx, new_index)
            )

            tr = TableRow(
                extracted_whitespace,
                trailing_whitespace,
                columns=tr_columns,
                end_of_row=None,
                did_start_with_separator=did_start_with_separator,
            )
            xyz.append(tr)

            start_index = new_index

            (start_index, extracted_whitespace) = ParserHelper.extract_spaces_verified(
                line_to_parse,
                new_index,
            )

            if len(xyz) == 2:
                did_parse_separators = TableParseHelper.__parse_table_2(xyz, col_as)
                if not did_parse_separators:
                    return False, -1, None

        keep_going = is_blank_line and len(xyz) >= 2
        if keep_going:
            return TableParseHelper.__create_table_token(new_index, xyz, col_as)
        else:
            return keep_going, new_index, None

    @staticmethod
    def __parse_table_3(
        line_to_parse: str, xxxx: str, new_index: int
    ) -> Tuple[List[TableColumn], str, str, int]:
        tr_columns = []
        trailing_whitespace = ""
        pre_h = ""
        while new_index < len(line_to_parse):
            g, h = ParserHelper.collect_until_one_of_characters(
                line_to_parse, new_index, xxxx
            )
            assert g is not None
            assert h is not None
            if g >= len(line_to_parse):
                a, _ = ParserHelper.collect_while_spaces(h, 0)
                if a == len(h):
                    trailing_whitespace = h
                else:
                    tr_columns.append(TableColumn(f"{pre_h}{h}", is_last=True))
                new_index = len(line_to_parse)
                continue
            if g > 0 and line_to_parse[g] == "|" and line_to_parse[g - 1] == "\\":
                # f1, f2 = ParserHelper.collect_backwards_while_character(line_to_parse, g, "\\")
                # if f1 % 2 == 1:
                pre_h += f"{h}|"
                new_index = g + 1
                if new_index >= len(line_to_parse):
                    h = f"{pre_h}|"
                    pre_h = ""
                    a, _ = ParserHelper.collect_while_spaces(h, 0)
                    assert a != len(h)
                    tr_columns.append(TableColumn(h, is_last=True))
                continue
            new_index = g + 1
            if line_to_parse[g] == "\n":
                h = f"{pre_h}{h}"
                if h:
                    a, _ = ParserHelper.collect_while_spaces(h, 0)
                    if a == len(h):
                        trailing_whitespace = h
                    else:
                        tr_columns.append(TableColumn(h, is_last=True))
                break
            tr_columns.append(TableColumn(f"{pre_h}{h}|"))
            pre_h = ""
        return tr_columns, trailing_whitespace, pre_h, new_index

    @staticmethod
    def __parse_table_2(xyz: List[TableRow], col_as: List[Optional[str]]) -> bool:
        if len(xyz[0].columns) != len(xyz[1].columns):
            return False
        for ix in xyz[1].columns:
            i = ix.text
            x_index = 0
            x_lead = x_trail = False
            if ParserHelper.is_character_at_index(i, x_index, ":"):
                x_lead = True
                x_index += 1
            ii, ij = ParserHelper.collect_while_character(i, x_index, "-")
            assert ii is not None
            assert ij is not None
            if ii and ij <= len(i):
                if ParserHelper.is_character_at_index(i, ij, ":"):
                    x_trail = True
                    ij += 1
                is_complete = len(i) == ij
                if is_complete:
                    f1 = None
                    if x_lead:
                        f1 = "center" if x_trail else "left"
                    elif x_trail:
                        f1 = "right"
                    col_as.append(f1)
            else:
                is_complete = False
            if not is_complete:
                return False
        return True

    @staticmethod
    def __create_table_token(
        new_index: int,
        xyz: List[TableRow],
        col_as: List[Optional[str]],
    ) -> Tuple[bool, int, Optional[TableTuple]]:
        # POGGER.debug(
        #     ">>collected_destination(normalized)>>$",
        #     normalized_destination,
        # )

        # if (
        #     not inline_title
        #     and line_title_whitespace
        #     and line_title_whitespace[-1] == ParserHelper.newline_character
        # ):
        #     line_title_whitespace = line_title_whitespace[:-1]

        # POGGER.debug(">>inline_link>>$<<", inline_link)
        # POGGER.debug(">>inline_title>>$<<", inline_title)
        parsed_lrd_tuple = TableTuple(
            normalized_destination="",
            xyz=xyz,
            col_as=col_as,
            # LinkReferenceTitles(inline_link, inline_title),
            # LinkReferenceInfo(
            #     collected_destination,
            #     line_destination_whitespace,
            #     inline_raw_link,
            #     line_title_whitespace,
            #     inline_raw_title,
            #     end_whitespace,
            # ),
        )
        return True, new_index, parsed_lrd_tuple

    @staticmethod
    def __is_table_start(
        parser_state: ParserState,
        line_to_parse: str,
        start_index: int,
        extracted_whitespace: str,
    ) -> bool:
        """
        Determine whether or not we have a valid table start.  We can tell this because
        a proper table will have a pipe character `|` at least once in every line.
        """

        # TODO comment out
        # if parser_state.token_stack[-1].is_paragraph:
        #     return False

        POGGER.debug(
            "__is_table_start - extracted_whitespace:>:$:<",
            extracted_whitespace,
        )
        POGGER.debug("__is_table_start - line_to_parse:>:$:<", line_to_parse)
        if (
            TabHelper.is_length_less_than_or_equal_to(extracted_whitespace, 3)
        ) and TableParseHelper.__table_column_separator_character in line_to_parse:
            POGGER.debug("__is_table_start - potential")

            # remaining_line, continue_with_lrd = line_to_parse[start_index + 1 :], True
            # if (
            #     remaining_line
            #     and remaining_line[-1] == InlineBackslashHelper.backslash_character
            # ):
            #     remaining_line_size, start_index, found_index = (
            #         len(remaining_line),
            #         0,
            #         remaining_line.find(
            #             InlineBackslashHelper.backslash_character, start_index
            #         ),
            #     )
            #     POGGER.debug(">>$<<$", remaining_line, remaining_line_size)
            #     POGGER.debug(">>$<<$", remaining_line, start_index)
            #     POGGER.debug(">>$<<", found_index)
            #     while found_index != -1 and found_index < (remaining_line_size - 1):
            #         start_index = found_index + 2
            #         POGGER.debug(">>$<<$", remaining_line, start_index)
            #         found_index = remaining_line.find(
            #             InlineBackslashHelper.backslash_character, start_index
            #         )
            #         POGGER.debug(">>$<<", found_index)
            #     POGGER.debug(">>>>>>>$<<", found_index)
            #     continue_with_lrd = found_index != remaining_line_size - 1
            return True  # continue_with_lrd
        return False
