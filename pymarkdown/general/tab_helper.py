"""
Module to provide helper functions for reintergrating tabs.
"""

import logging
from typing import Optional, Tuple, cast

from pymarkdown.general.parser_helper import ParserHelper
from pymarkdown.general.parser_state import ParserState
from pymarkdown.tokens.block_quote_markdown_token import BlockQuoteMarkdownToken
from pymarkdown.tokens.list_start_markdown_token import ListStartMarkdownToken

LOGGER = logging.getLogger(__name__)


class TabHelper:
    """
    Class to provide helper functions for reintergrating tabs.
    """

    @staticmethod
    def parse_thematic_break_with_tab(
        original_line: str, token_text: str, extracted_whitespace: str
    ) -> Tuple[str, bool, bool, Optional[str], str, int]:
        """
        Generic type of algorithm to deal with tabs, in this case, used by thematic breaks
        and HTML blocks.
        """

        LOGGER.debug(
            "original_line>>:%s:<",
            ParserHelper.make_whitespace_visible((original_line)),
        )
        LOGGER.debug("token_text>>:%s:<", ParserHelper.make_value_visible(token_text))
        LOGGER.debug(
            "extracted_whitespace>>:%s:<",
            ParserHelper.make_value_visible(extracted_whitespace),
        )
        (
            tabified_token_text,
            _,
            tabified_token_text_index,
        ) = TabHelper.find_detabify_string(
            original_line, token_text, use_proper_traverse=True
        )
        LOGGER.debug(
            "tabified_token_text>>:%s:<",
            ParserHelper.make_value_visible(tabified_token_text),
        )
        LOGGER.debug("tabified_token_text_index>>:%d:<", tabified_token_text_index)
        assert tabified_token_text_index != -1, "Detabified string must be found."
        assert tabified_token_text is not None, "Detabified string must be found."

        tabified_leading_spaces = original_line[:tabified_token_text_index]
        LOGGER.debug(
            "tabified_leading_spaces>>:%s:<",
            ParserHelper.make_value_visible(tabified_leading_spaces),
        )
        tabified_suffix = extracted_whitespace
        tabified_prefix = None

        split_tab = False
        split_tab_with_block_quote_suffix = False
        if tabified_leading_spaces:
            (
                tabified_prefix,
                tabified_suffix,
                split_tab,
                split_tab_with_block_quote_suffix,
            ) = TabHelper.match_tabbed_whitespace(
                extracted_whitespace, tabified_leading_spaces
            )
        LOGGER.debug(
            "tabified_token_text>>:%s:<",
            ParserHelper.make_value_visible(tabified_token_text),
        )
        LOGGER.debug(
            "tabified_prefix>>:%s:<", ParserHelper.make_value_visible(tabified_prefix)
        )
        LOGGER.debug(
            "tabified_suffix>>:%s:<", ParserHelper.make_value_visible(tabified_suffix)
        )
        LOGGER.debug("split_tab>>:%s:<", str(split_tab))
        LOGGER.debug(
            "split_tab_with_block_quote_suffix>>:%s:<",
            str(split_tab_with_block_quote_suffix),
        )
        return (
            tabified_token_text,
            split_tab,
            split_tab_with_block_quote_suffix,
            tabified_prefix,
            tabified_suffix,
            tabified_token_text_index,
        )

    @staticmethod
    def match_tabbed_whitespace(
        extracted_whitespace: str, corrected_extracted_whitespace: str
    ) -> Tuple[str, str, bool, bool]:
        """
        Match any tabbed whitespace with its non-tabbed counterpart.
        """
        detabified_suffix = ""
        detabified_prefix = ""
        corrected_prefix = ""
        corrected_suffix = corrected_extracted_whitespace
        index_from_end = len(corrected_extracted_whitespace) - 1
        have_been_inside_loop = False
        while index_from_end >= 0 and len(detabified_suffix) < len(
            extracted_whitespace
        ):
            have_been_inside_loop = True
            corrected_suffix = corrected_extracted_whitespace[index_from_end:]
            corrected_prefix = corrected_extracted_whitespace[:index_from_end]
            LOGGER.debug(
                "index_from_end=:%s: of :%s:",
                index_from_end,
                len(corrected_extracted_whitespace),
            )
            LOGGER.debug("corrected_suffix=:%s:", corrected_suffix)
            LOGGER.debug(
                "corrected_prefix=:%s:",
                ParserHelper.make_whitespace_visible(corrected_prefix),
            )
            detabified_prefix = TabHelper.detabify_string(corrected_prefix)
            LOGGER.debug("detabified_prefix=:%s:", detabified_prefix)
            detabified_suffix = TabHelper.detabify_string(
                corrected_suffix, additional_start_delta=len(detabified_prefix)
            )
            LOGGER.debug("detabified_suffix=:%s:", detabified_suffix)
            if len(detabified_suffix) < len(extracted_whitespace):
                index_from_end -= 1
        assert index_from_end >= 0, "Index must be within the string."

        if not have_been_inside_loop:
            corrected_prefix = corrected_extracted_whitespace
            corrected_suffix = ""

        LOGGER.debug(
            "corrected_prefix=:%s:", ParserHelper.make_value_visible(corrected_prefix)
        )
        LOGGER.debug(
            "corrected_suffix=:%s:", ParserHelper.make_value_visible(corrected_suffix)
        )
        split_tab = detabified_suffix != extracted_whitespace
        LOGGER.debug(
            "detabified_prefix=:%s:", ParserHelper.make_value_visible(detabified_prefix)
        )
        LOGGER.debug(
            "detabified_suffix=:%s:", ParserHelper.make_value_visible(detabified_suffix)
        )
        LOGGER.debug("split_tab=:%s:", str(split_tab))
        split_tab_with_block_quote_suffix = False
        if split_tab:
            split_tab_with_block_quote_suffix = detabified_prefix.endswith(">")
        elif detabified_prefix:
            assert detabified_prefix.endswith(
                " "
            ), "Detabified prefix must end with a space."
        #     assert detabified_suffix[1:] == extracted_whitespace

        return (
            corrected_prefix,
            corrected_suffix,
            split_tab,
            split_tab_with_block_quote_suffix,
        )

    @staticmethod
    def find_detabify_string_ex(
        original_line: str, detabified_line_to_match: str
    ) -> Tuple[str, int]:
        """
        Find a detabified line within the original line, automatically looking at all four tab offsets.
        """

        for initial_offset in range(4):
            (
                adjusted_original_line,
                original_index,
                _,
            ) = TabHelper.find_detabify_string(
                original_line, detabified_line_to_match, initial_offset
            )
            if adjusted_original_line is not None:
                return adjusted_original_line, original_index
        raise AssertionError("A detabbified string must be found.")

    @staticmethod
    def find_detabify_string_verified(
        original_line: str,
        detabified_line_to_match: str,
        initial_offset: int = 0,
        use_proper_traverse: bool = False,
    ) -> Tuple[str, int, int]:
        """
        Find a detabified line within the original line, asserting if the first return value is not defined.
        """
        adjusted_original_line, original_start_index, original_line_index = (
            TabHelper.find_detabify_string(
                original_line,
                detabified_line_to_match,
                initial_offset,
                use_proper_traverse,
            )
        )
        assert (
            adjusted_original_line is not None
        ), "adjusted_original_line must be defined."
        return adjusted_original_line, original_start_index, original_line_index

    @staticmethod
    def find_detabify_string(
        original_line: str,
        detabified_line_to_match: str,
        initial_offset: int = 0,
        use_proper_traverse: bool = False,
    ) -> Tuple[Optional[str], int, int]:
        """
        Find a detabified line within the original line.
        """

        # LOGGER.debug("original_line=:%s:", ParserHelper.make_whitespace_visible(original_line.replace("\t", "\\t")))
        # LOGGER.debug("detabified_line_to_match=:%s:", ParserHelper.make_whitespace_visible(detabified_line_to_match))
        # LOGGER.debug("initial_offset=:%d:", initial_offset)
        original_start_index = 0
        original_line_index = 0
        adjusted_original_line = original_line[original_line_index:]
        adjusted_start_index = original_start_index + initial_offset
        detabified_original_line = TabHelper.detabify_string(
            original_line, additional_start_delta=adjusted_start_index
        )
        # LOGGER.debug("detabified_original_line=:%s:", ParserHelper.make_whitespace_visible(str(detabified_original_line)))
        # LOGGER.debug("len(detabified_original_line)=%s >= len(detabified_line_to_match)=%s ", str(len(detabified_original_line)), str(len(detabified_line_to_match)))
        while (len(detabified_original_line)) >= len(detabified_line_to_match):
            adjusted_original_line = original_line[original_line_index:]
            adjusted_start_index = original_start_index + initial_offset
            # LOGGER.debug("adjusted_original_line=:%s:", adjusted_original_line.replace("\t", "\\t"))
            # LOGGER.debug("adjusted_start_index=:%d:", adjusted_start_index)
            detabified_original_line = TabHelper.detabify_string(
                adjusted_original_line,
                additional_start_delta=adjusted_start_index,
            )
            # LOGGER.debug("detabified_original_line=:%s:", ParserHelper.make_whitespace_visible(str(detabified_original_line)))
            if detabified_line_to_match == detabified_original_line:
                break
            if (
                use_proper_traverse
                and adjusted_original_line[0] == ParserHelper.tab_character
            ):
                original_start_index = (1 + (original_start_index // 4)) * 4
            else:
                original_start_index += 1
            original_line_index += 1
            # LOGGER.debug("len(detabified_original_line)=%s >= len(detabified_line_to_match)=%s ", str(len(detabified_original_line)), str(len(detabified_line_to_match)))
        if detabified_line_to_match == detabified_original_line:
            return adjusted_original_line, original_start_index, original_line_index
        return None, -1, -1

    @staticmethod
    def detabify_string(source_string: str, additional_start_delta: int = 0) -> str:
        """
        Given a string that may have one or more tabstops in it, resolve the
        tabstops into more easily handled space characters.
        """
        if ParserHelper.tab_character not in source_string:
            return source_string

        rebuilt_string = ""
        current_start_index = 0
        next_tab_index = source_string.find(ParserHelper.tab_character)
        # LOGGER.debug("next_tab_index=:%d:", next_tab_index)
        # LOGGER.debug("source_string=:%s:", ParserHelper.make_whitespace_visible(source_string.replace("\t", "\\t")))
        # LOGGER.debug("additional_start_delta=:%d:", additional_start_delta)
        while next_tab_index != -1:
            _, start_index = ParserHelper.collect_backwards_while_spaces_verified(
                source_string, next_tab_index
            )
            # LOGGER.debug("start_index=:%d:", start_index)
            end_index, _ = ParserHelper.collect_while_spaces(
                source_string, next_tab_index
            )
            # LOGGER.debug("end_index=:%d:", end_index)
            whitespace_section = source_string[start_index:end_index]
            # LOGGER.debug("whitespace_section=:%s:", ParserHelper.make_whitespace_visible(whitespace_section.replace("\t", "\\t")))
            if start_index:
                rebuilt_string += source_string[:start_index]
            realized_start_index = (
                current_start_index + start_index + additional_start_delta
            )
            # LOGGER.debug("realized_start_index=:%d:", realized_start_index)
            whitespace_actual_length = TabHelper.calculate_length(
                whitespace_section, realized_start_index
            )
            # LOGGER.debug("whitespace_actual_length=:%d:", whitespace_actual_length)
            rebuilt_string += ParserHelper.repeat_string(
                ParserHelper.space_character, whitespace_actual_length
            )
            current_start_index += start_index + whitespace_actual_length

            source_string = source_string[end_index:]
            next_tab_index = source_string.find(ParserHelper.tab_character)
            # LOGGER.debug("next_tab_index=:%d:", next_tab_index)
        if source_string:
            rebuilt_string += source_string
        return rebuilt_string

    @staticmethod
    def calculate_length(source_string: str, start_index: int = 0) -> int:
        """
        Calculate an adjusted length for the string.
        """

        string_length = start_index
        for source_character in source_string:
            string_length = (
                (int((string_length + 4) / 4) * 4)
                if source_character == ParserHelper.tab_character
                else (string_length + 1)
            )
        return string_length - start_index

    @staticmethod
    def is_length_less_than_or_equal_to(source_string: str, length_limit: int) -> bool:
        """
        Determine if the adjusted length of the string is less than or equal to the
        specified limit.
        """
        return TabHelper.calculate_length(source_string) <= length_limit

    @staticmethod
    def is_length_greater_than_or_equal_to(
        source_string: str, length_limit: int, start_index: int = 0
    ) -> bool:
        """
        Determine if the adjusted length of the string is greater than or equal to the
        specified limit.
        """
        return (
            TabHelper.calculate_length(source_string, start_index=start_index)
            >= length_limit
        )

    # pylint: disable=too-many-arguments
    @staticmethod
    def find_tabified_string(
        original_line: str,
        reconstructed_line: str,
        abc: bool = False,
        use_proper_traverse: bool = False,
        reconstruct_prefix: Optional[str] = None,
        was_indented: bool = False,
    ) -> Tuple[str, int, bool]:
        """
        Find the correct tabified string to represent the line, allowing
        for the possibility that the first character may be split inside
        of a tab character.
        """

        LOGGER.debug(
            "original_line>:%s:<", ParserHelper.make_value_visible(original_line)
        )
        LOGGER.debug(
            "reconstructed_line>:%s:<",
            ParserHelper.make_value_visible(reconstructed_line),
        )
        (
            adj_original,
            adj_original_index,
            adj_traverse_original_index,
        ) = TabHelper.find_detabify_string(
            original_line, reconstructed_line, use_proper_traverse=use_proper_traverse
        )
        LOGGER.debug(">>adj_original>:%s:<", adj_original)
        LOGGER.debug(">>adj_original_index>:%d:<", adj_original_index)
        LOGGER.debug(">>adj_traverse_original_index>:%d:<", adj_traverse_original_index)

        # This is a weird case.
        if adj_original is None and was_indented and original_line[0] == "\t":
            original_line_minus_leading_tab = original_line[1:]
            (
                adj_original,
                adj_original_index,
                adj_traverse_original_index,
            ) = TabHelper.find_detabify_string(
                original_line_minus_leading_tab,
                reconstructed_line,
                use_proper_traverse=use_proper_traverse,
            )
            was_indented = False
        split_tab = adj_original is None
        LOGGER.debug("split_tab>:%s:<", str(split_tab))
        if split_tab:
            (
                adj_original,
                adj_original_index,
                adj_traverse_original_index,
            ) = TabHelper.find_tabified_string_split(
                reconstructed_line,
                reconstruct_prefix,
                original_line,
                use_proper_traverse,
                abc,
            )
        assert (
            adj_original is not None
        ), "Adjusted original line must be defined by now."
        return_index = (
            adj_traverse_original_index if use_proper_traverse else adj_original_index
        )
        LOGGER.debug(
            "adj_original=:%s:",
            ParserHelper.make_whitespace_visible(adj_original.replace("\t", "\\t")),
        )
        LOGGER.debug(">>return_index>:%d:<", return_index)
        LOGGER.debug(">>split_tab>:%s:<", str(split_tab))
        return (
            adj_original,
            return_index,
            split_tab,
        )

    # pylint: enable=too-many-arguments

    @staticmethod
    def find_tabified_string_split(
        reconstructed_line: str,
        reconstruct_prefix: Optional[str],
        original_line: str,
        use_proper_traverse: bool,
        abc: bool,
    ) -> Tuple[Optional[str], int, int]:
        """
        Find a tabified string within a split.
        """
        LOGGER.debug(
            ">>reconstructed_line>:%s:<",
            ParserHelper.make_whitespace_visible(
                reconstructed_line.replace("\t", "\\t")
            ),
        )
        # Need to split this tab between two areas.
        if not reconstruct_prefix:
            reconstruct_prefix = " "
        reconstructed_line = f"{reconstruct_prefix}{reconstructed_line}"
        LOGGER.debug(
            ">>reconstructed_line>:%s:<",
            ParserHelper.make_whitespace_visible(
                reconstructed_line.replace("\t", "\\t")
            ),
        )
        (
            adj_original,
            adj_original_index,
            adj_traverse_original_index,
        ) = TabHelper.find_detabify_string(
            original_line,
            reconstructed_line,
            use_proper_traverse=use_proper_traverse,
        )
        LOGGER.debug(">>adj_original>:%s:<", adj_original)
        LOGGER.debug(">>adj_original_index>:%d:<", adj_original_index)
        LOGGER.debug(">>adj_traverse_original_index>:%d:<", adj_traverse_original_index)
        if abc:
            adj_original_index += 1
            LOGGER.debug(">>adj_original_index>:%d:<", adj_original_index)
        return adj_original, adj_original_index, adj_traverse_original_index

    @staticmethod
    def __adjust_block_quote_indent_for_tab_block_quote(
        parser_state: ParserState, stack_token_index: int
    ) -> None:
        block_quote_token = cast(
            BlockQuoteMarkdownToken,
            parser_state.token_stack[stack_token_index].matching_markdown_token,
        )
        # POGGER.debug(
        #     "parser_state=:$:",
        #     block_quote_token,
        # )
        block_quote_leading_spaces = block_quote_token.bleading_spaces
        assert (
            block_quote_leading_spaces is not None
        ), "Block quote bleading spaces must be defined by now."
        # POGGER.debug("block_quote_leading_spaces=:$:", block_quote_leading_spaces)
        block_quote_leading_spaces_index = block_quote_leading_spaces.rfind("\n")
        last_block_quote_leading_space = block_quote_leading_spaces[
            block_quote_leading_spaces_index + 1 :
        ]
        # POGGER.debug(
        #     "last_block_quote_leading_space=:$:", last_block_quote_leading_space
        # )
        if last_block_quote_leading_space:
            assert last_block_quote_leading_space[-1] in [" ", ">"]
            if last_block_quote_leading_space[-1] != ">":
                last_block_quote_leading_space = last_block_quote_leading_space[:-1]
        # POGGER.debug(
        #     "last_block_quote_leading_space=:$:", last_block_quote_leading_space
        # )
        # POGGER.debug(
        #     "parser_state=:$:",
        #     block_quote_token,
        # )
        block_quote_token.remove_last_bleading_space()
        # POGGER.debug(
        #     "parser_state=:$:",
        #     block_quote_token,
        # )

        LOGGER.debug(
            "__adjust_block_quote_indent_for_tab_block_quote>>block_token>>%s",
            str(block_quote_token),
        )
        block_quote_token.add_bleading_spaces(last_block_quote_leading_space)
        LOGGER.debug(
            "__adjust_block_quote_indent_for_tab_block_quote>>block_token>>%s",
            str(block_quote_token),
        )
        # POGGER.debug(
        #     "parser_state=:$:",
        #     block_quote_token,
        # )

    @staticmethod
    def __adjust_block_quote_indent_for_tab_list_normal(
        last_list_leading_space: str,
        fenced_switch_enabled: bool,
        tab_index: int,
        alternate_list_leading_space: Optional[str],
        extracted_whitespace: str,
    ) -> Tuple[str, str]:
        last_list_leading_space_length = len(last_list_leading_space)
        if fenced_switch_enabled:
            assert tab_index < last_list_leading_space_length or (
                last_list_leading_space_length == 0
            ), "Tab index must be within leading spaces."  # and tab_index == 0)
        else:
            assert (
                tab_index < last_list_leading_space_length
            ), "Tab index must be within leading spaces."
        last_list_leading_space = (
            extracted_whitespace[:tab_index]
            if alternate_list_leading_space is None
            else alternate_list_leading_space
        )
        extracted_whitespace = extracted_whitespace[tab_index:]
        return last_list_leading_space, extracted_whitespace

    # pylint: disable=too-many-arguments
    @staticmethod
    def __adjust_block_quote_indent_for_tab_list(
        parser_state: ParserState,
        stack_token_index: int,
        extracted_whitespace: str,
        fenced_switch_enabled: bool,
        alternate_list_leading_space: Optional[str],
        original_line: Optional[str] = None,
    ) -> str:
        list_start_token = cast(
            ListStartMarkdownToken,
            parser_state.token_stack[stack_token_index].matching_markdown_token,
        )
        LOGGER.debug(
            "list_start_token=:%s:",
            ParserHelper.make_value_visible(list_start_token),
        )
        list_leading_spaces = list_start_token.leading_spaces
        assert list_leading_spaces is not None, "Leading spaces must be defined by now."
        LOGGER.debug(
            "list_leading_spaces=:%s:",
            ParserHelper.make_value_visible(list_leading_spaces),
        )
        list_leading_spaces_index = list_leading_spaces.rfind("\n")
        last_list_leading_space = list_leading_spaces[list_leading_spaces_index + 1 :]
        LOGGER.debug(
            "last_list_leading_space=:%s:",
            ParserHelper.make_value_visible(last_list_leading_space),
        )
        tab_index = extracted_whitespace.find("\t")
        LOGGER.debug("extracted_whitespace=:%s:", extracted_whitespace)
        LOGGER.debug("tab_index=:%d:", tab_index)

        if (
            tab_index == -1
            and extracted_whitespace
            and last_list_leading_space
            and last_list_leading_space != extracted_whitespace
            and original_line is not None
        ):
            last_list_leading_space = (
                TabHelper.__adjust_block_quote_indent_for_tab_list_kludge(
                    original_line, extracted_whitespace, last_list_leading_space
                )
            )
        else:
            (
                last_list_leading_space,
                extracted_whitespace,
            ) = TabHelper.__adjust_block_quote_indent_for_tab_list_normal(
                last_list_leading_space,
                fenced_switch_enabled,
                tab_index,
                alternate_list_leading_space,
                extracted_whitespace,
            )
        LOGGER.debug("last_list_leading_space=:%s:", last_list_leading_space)
        LOGGER.debug("extracted_whitespace=:%s:", extracted_whitespace)

        LOGGER.debug(
            "list_start_token=:%s:",
            ParserHelper.make_value_visible(list_start_token),
        )
        list_start_token.remove_last_leading_space()
        LOGGER.debug(
            "list_start_token=:%s:",
            ParserHelper.make_value_visible(list_start_token),
        )
        list_start_token.add_leading_spaces(last_list_leading_space)
        LOGGER.debug(
            "list_start_token=:%s:",
            ParserHelper.make_value_visible(list_start_token),
        )
        return extracted_whitespace

    # pylint: enable=too-many-arguments
    @staticmethod
    def adjust_block_quote_indent_for_tab_verified(
        parser_state: ParserState,
        extracted_whitespace: Optional[str] = None,
        alternate_list_leading_space: Optional[str] = None,
        fenced_switch_enabled: bool = False,
        original_line: Optional[str] = None,
    ) -> str:
        """
        Adjust the last block quote for a tab, asserting if the returned string is not defined.
        """
        extracted_whitespace = TabHelper.adjust_block_quote_indent_for_tab(
            parser_state,
            extracted_whitespace,
            alternate_list_leading_space,
            fenced_switch_enabled,
            original_line,
        )
        assert (
            extracted_whitespace is not None
        ), "extracted_whitespace must be defined by now."
        return extracted_whitespace

    @staticmethod
    def adjust_block_quote_indent_for_tab(
        parser_state: ParserState,
        extracted_whitespace: Optional[str] = None,
        alternate_list_leading_space: Optional[str] = None,
        fenced_switch_enabled: bool = False,
        original_line: Optional[str] = None,
    ) -> Optional[str]:
        """
        Adjust the last block quote for a tab.
        """
        LOGGER.debug(
            "extracted_whitespace=:%s:",
            ParserHelper.make_value_visible(extracted_whitespace),
        )
        LOGGER.debug(
            "parser_state=:%s:",
            ParserHelper.make_value_visible(parser_state.token_stack),
        )
        stack_token_index = len(parser_state.token_stack) - 1
        while (
            stack_token_index > 0
            and not parser_state.token_stack[stack_token_index].is_block_quote
            and not parser_state.token_stack[stack_token_index].is_list
        ):
            stack_token_index -= 1
        assert stack_token_index != 0, "Must not have gone back to the root index."

        LOGGER.debug(
            "parser_state=:%s:",
            ParserHelper.make_value_visible(
                parser_state.token_stack[stack_token_index]
            ),
        )
        if parser_state.token_stack[stack_token_index].is_block_quote:
            TabHelper.__adjust_block_quote_indent_for_tab_block_quote(
                parser_state, stack_token_index
            )
        else:
            assert (
                extracted_whitespace is not None
            ), "If we are not looking at a block quote, extracted_whitespace must be defined."
            extracted_whitespace = TabHelper.__adjust_block_quote_indent_for_tab_list(
                parser_state,
                stack_token_index,
                extracted_whitespace,
                fenced_switch_enabled,
                alternate_list_leading_space,
                original_line,
            )
        return extracted_whitespace

    @staticmethod
    def __adjust_block_quote_indent_for_tab_list_kludge(
        original_line: str, extracted_whitespace: str, last_list_leading_space: str
    ) -> str:
        orig_end_ws_index, _ = ParserHelper.extract_ascii_whitespace(original_line, 0)
        orig_after_ws = original_line[orig_end_ws_index:]
        recon_line = last_list_leading_space + extracted_whitespace[:-1] + orig_after_ws

        reconstructed_line, _, _ = TabHelper.find_tabified_string_split(
            recon_line, "", original_line, True, False
        )
        assert reconstructed_line is not None, "reconstructed_line must be found."
        text_to_use_count = 1
        keep_going = text_to_use_count < len(reconstructed_line)
        while keep_going:
            detabbified_line = TabHelper.detabify_string(
                reconstructed_line[:text_to_use_count]
            )
            keep_going = text_to_use_count < len(reconstructed_line) and len(
                detabbified_line
            ) < len(last_list_leading_space)
            if keep_going:
                text_to_use_count += 1
        assert (
            reconstructed_line[text_to_use_count - 1] == "\t"
        ), "Last character must be a tab."
        return reconstructed_line[: text_to_use_count - 1]

    @staticmethod
    def search_for_tabbed_prefix(
        extracted_space: str, detabify_index: int, lead_space_len: int
    ) -> Tuple[int, str, str]:
        """
        Look for a specific tabbed prefix length within a given string.
        """
        extra_detabify_index = 0
        indent_used = 0

        search_index = 1
        keep_going = True
        detabbed_ex_part = ex_part = ""
        while keep_going:
            ex_part = extracted_space[indent_used : indent_used + search_index]
            detabbed_ex_part = TabHelper.detabify_string(
                ex_part, detabify_index + extra_detabify_index
            )
            keep_going = (
                search_index < len(extracted_space) + 1
                and len(detabbed_ex_part) < lead_space_len
            )
            if keep_going:
                search_index += 1
        assert (
            len(detabbed_ex_part) >= lead_space_len
        ), "Proper amount of space must be used up."
        return search_index, ex_part, detabbed_ex_part

    @staticmethod
    def search_for_tabbed_prefix2(
        extracted_space: str,
        detabify_index: int,
        extra_detabify_index: int,
        indent_used: int,
        lead_space_len: int,
    ) -> Tuple[int, str, str]:
        """
        Look for a specific tabbed prefix length within a given string.
        """
        search_index = 1
        keep_going = True
        ex_part = detabbed_ex_part = ""
        while keep_going:
            ex_part = extracted_space[indent_used : indent_used + search_index]
            detabbed_ex_part = TabHelper.detabify_string(
                ex_part, detabify_index + extra_detabify_index
            )
            keep_going = (
                len(detabbed_ex_part) < len(extracted_space)
                and len(detabbed_ex_part) < lead_space_len
            )
            if keep_going:
                search_index += 1
        assert (
            len(detabbed_ex_part) >= lead_space_len
        ), "Proper amount of space must be used up."
        return search_index, ex_part, detabbed_ex_part
