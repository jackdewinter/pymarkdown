"""
Emphasis helper
"""

import logging
from typing import List, Optional, Tuple, cast

from pymarkdown.extension_manager.extension_manager import ExtensionManager
from pymarkdown.general.constants import Constants
from pymarkdown.general.parser_helper import ParserHelper
from pymarkdown.general.parser_logger import ParserLogger
from pymarkdown.tokens.emphasis_markdown_token import EmphasisMarkdownToken
from pymarkdown.tokens.markdown_token import MarkdownToken
from pymarkdown.tokens.special_text_markdown_token import SpecialTextMarkdownToken

POGGER = ParserLogger(logging.getLogger(__name__))


class EmphasisHelper:
    """
    Class to helper with the parsing of emphasis for inline elements.
    """

    __simple_emphasis = "*"
    __complex_emphasis = "_"
    __inline_emphasis = ""
    __strikethrough_emphasis = "~"

    @staticmethod
    def initialize(extension_manager: ExtensionManager) -> None:
        """
        Initialize this subsystem.
        """
        EmphasisHelper.__inline_emphasis = (
            f"{EmphasisHelper.__simple_emphasis}{EmphasisHelper.__complex_emphasis}"
        )
        if extension_manager.is_strike_through_enabled:
            EmphasisHelper.__inline_emphasis += EmphasisHelper.__strikethrough_emphasis

    @staticmethod
    def get_inline_emphasis() -> str:
        """
        Get the current string with all inline emphasis characters.
        """
        return EmphasisHelper.__inline_emphasis

    @staticmethod
    def __create_delimiter_stack(
        inline_blocks: List[MarkdownToken],
        is_debug_enabled: bool,
        wall_token: Optional[MarkdownToken],
    ) -> Tuple[List[SpecialTextMarkdownToken], int]:
        delimiter_stack, special_count = [], 0
        for next_block in inline_blocks:
            POGGER.debug(
                "special_count>>$>>$",
                special_count,
                next_block,
            )
            special_count += 1
            if not next_block.is_special_text:
                continue
            special_token = cast(SpecialTextMarkdownToken, next_block)
            if is_debug_enabled:
                POGGER.debug(
                    "i>>>$",
                    special_token.show_process_emphasis(),
                )
            delimiter_stack.append(special_token)

        stack_bottom = EmphasisHelper.__find_token_in_delimiter_stack(
            inline_blocks, delimiter_stack, wall_token
        )
        return delimiter_stack, stack_bottom

    @staticmethod
    def __find_potential_opener(
        delimiter_stack: List[SpecialTextMarkdownToken],
        current_position: int,
        stack_bottom: int,
        openers_bottom: int,
    ) -> Tuple[SpecialTextMarkdownToken, Optional[SpecialTextMarkdownToken]]:
        # POGGER.debug("delimiter_stack-->$",delimiter_stack)
        scan_index = current_position - 1
        found_opener: Optional[SpecialTextMarkdownToken] = None
        close_token = delimiter_stack[current_position]
        # POGGER.debug("potential closer-->$", current_position)
        while (
            scan_index >= 0
            and scan_index > stack_bottom
            and scan_index > openers_bottom
        ):
            # POGGER.debug("potential opener:$", scan_index)
            open_token = delimiter_stack[scan_index]
            if EmphasisHelper.__is_open_close_emphasis_valid(open_token, close_token):
                found_opener = open_token
                break
            scan_index -= 1
            # POGGER.debug(
            #     "scan_index-->$>stack_bottom>$>openers_bottom>$>",
            #     scan_index,
            #     stack_bottom,
            #     openers_bottom,
            # )
        return close_token, found_opener

    @staticmethod
    def __process_this_delimiter_item(
        is_debug_enabled: bool,
        delimiter_stack: List[SpecialTextMarkdownToken],
        current_position: int,
    ) -> bool:
        special_token = delimiter_stack[current_position]

        if is_debug_enabled:
            POGGER.debug(
                "Block($)-->$",
                current_position,
                special_token.show_process_emphasis(),
            )
        continue_processing = False
        if not special_token.is_active:
            POGGER.debug("not active")
        elif special_token.token_text[0] not in EmphasisHelper.get_inline_emphasis():
            POGGER.debug("not emphasis")
        elif not EmphasisHelper.__is_potential_closer(special_token):
            POGGER.debug("not closer")
        else:
            continue_processing = True
        return continue_processing

    @staticmethod
    def resolve_inline_emphasis(
        inline_blocks: List[MarkdownToken], wall_token: Optional[MarkdownToken]
    ) -> None:
        """
        Resolve the inline emphasis by interpreting the special text tokens.
        """
        is_debug_enabled = POGGER.is_debug_enabled
        delimiter_stack, stack_bottom = EmphasisHelper.__create_delimiter_stack(
            inline_blocks, is_debug_enabled, wall_token
        )

        current_position, stack_size = (
            stack_bottom + 1,
            len(delimiter_stack),
        )
        if current_position < stack_size:
            openers_bottom = stack_bottom
            if is_debug_enabled:
                POGGER.debug("BLOCK($) of ($)", current_position, stack_size)
                POGGER.debug(
                    "BLOCK($)-->$",
                    current_position,
                    delimiter_stack[current_position].show_process_emphasis(),
                )

            while current_position < (len(delimiter_stack) - 1):
                current_position += 1
                if not EmphasisHelper.__process_this_delimiter_item(
                    is_debug_enabled, delimiter_stack, current_position
                ):
                    continue

                close_token, found_opener = EmphasisHelper.__find_potential_opener(
                    delimiter_stack, current_position, stack_bottom, openers_bottom
                )

                if found_opener:
                    POGGER.debug("FOUND OPEN")
                    current_position = EmphasisHelper.__process_emphasis_pair(
                        inline_blocks,
                        found_opener,
                        close_token,
                        current_position,
                    )
                else:
                    # openers_bottom = current_position - 1
                    POGGER.debug("NOT FOUND OPEN, openers_bottom=$", openers_bottom)

                POGGER.debug("next->$", current_position)

        EmphasisHelper.__reset_token_text(inline_blocks)
        EmphasisHelper.__clear_remaining_emphasis(delimiter_stack, stack_bottom)

    # pylint: disable=too-many-arguments
    @staticmethod
    def __mark_used_tokens(
        open_token: SpecialTextMarkdownToken,
        close_token: SpecialTextMarkdownToken,
        start_index_in_blocks: int,
        end_index_in_blocks: int,
        emphasis_length: int,
        inline_blocks: List[MarkdownToken],
        current_position: int,
    ) -> int:
        # remove emphasis_length from open and close nodes
        is_debug_enabled = POGGER.is_debug_enabled
        if is_debug_enabled:
            POGGER.debug(
                "$>>close_token>>$<<",
                end_index_in_blocks,
                close_token.show_process_emphasis(),
            )
        close_token.reduce_repeat_count(emphasis_length, adjust_column_number=True)
        if not close_token.repeat_count:
            inline_blocks.remove(close_token)
            POGGER.debug("close_token>>removed")
            end_index_in_blocks -= 1
            close_token.deactivate()
        else:
            current_position -= 1
        if is_debug_enabled:
            POGGER.debug("close_token>>$<<", close_token.show_process_emphasis())
            POGGER.debug(
                "$>>open_token>>$<<",
                start_index_in_blocks,
                open_token.show_process_emphasis(),
            )
        open_token.reduce_repeat_count(emphasis_length)
        if not open_token.repeat_count:
            inline_blocks.remove(open_token)
            POGGER.debug("open_token>>removed")
            end_index_in_blocks -= 1
            open_token.deactivate()
        if is_debug_enabled:
            POGGER.debug("open_token>>$<<", open_token.show_process_emphasis())

        # "remove" between start and end from delimiter_stack
        inline_index = start_index_in_blocks + 1
        while inline_index < end_index_in_blocks:
            POGGER.debug(
                "inline_index>>$>>end>>$>>$",
                inline_index,
                end_index_in_blocks,
                len(inline_blocks),
            )
            if inline_blocks[inline_index].is_special_text:
                special_token = cast(
                    SpecialTextMarkdownToken, inline_blocks[inline_index]
                )
                special_token.deactivate()
            inline_index += 1
        return current_position

    # pylint: enable=too-many-arguments

    @staticmethod
    def __process_emphasis_pair(
        inline_blocks: List[MarkdownToken],
        open_token: SpecialTextMarkdownToken,
        close_token: SpecialTextMarkdownToken,
        current_position: int,
    ) -> int:
        """
        Given that we have found a valid open and close block, process them.
        """

        # Figure out whether we have emphasis or strong emphasis
        emphasis_character, emphasis_length = (
            open_token.token_text[0],
            2 if close_token.repeat_count >= 2 and open_token.repeat_count >= 2 else 1,
        )

        # add emph node in main stream
        POGGER.debug("open_token>>$", open_token)
        POGGER.debug("close_token>>$", close_token)

        POGGER.debug("open_token.repeat_count>>$", open_token.repeat_count)
        POGGER.debug("emphasis_length>>$", emphasis_length)
        open_column_number_delta = (
            open_token.repeat_count - emphasis_length
            if emphasis_length < open_token.repeat_count
            else 0
        )
        POGGER.debug("open_column_number_delta>>$", open_column_number_delta)

        start_index_in_blocks = inline_blocks.index(open_token)
        new_token = EmphasisMarkdownToken(
            emphasis_length,
            emphasis_character,
            line_number=open_token.line_number,
            column_number=open_token.column_number + open_column_number_delta,
        )
        inline_blocks.insert(
            start_index_in_blocks + 1,
            new_token,
        )
        end_index_in_blocks = inline_blocks.index(close_token)
        inline_blocks.insert(
            end_index_in_blocks,
            new_token.generate_close_markdown_token_from_markdown_token(
                "",
                "",
                line_number=close_token.line_number,
                column_number=close_token.column_number,
            ),
        )
        end_index_in_blocks += 1

        return EmphasisHelper.__mark_used_tokens(
            open_token,
            close_token,
            start_index_in_blocks,
            end_index_in_blocks,
            emphasis_length,
            inline_blocks,
            current_position,
        )

    @staticmethod
    def __find_token_in_delimiter_stack(
        inline_blocks: List[MarkdownToken],
        delimiter_stack: List[SpecialTextMarkdownToken],
        wall_token: Optional[MarkdownToken],
    ) -> int:
        """
        Find the specified token in the delimiter stack, based solely on
        position in the inline_blocks.
        """

        if not wall_token:
            return -1
        wall_index_in_inlines = inline_blocks.index(wall_token)
        POGGER.debug(">>wall_index_in_inlines>>$", wall_index_in_inlines)
        while wall_index_in_inlines >= 0:
            if inline_blocks[wall_index_in_inlines].is_special_text:
                special_token = cast(
                    SpecialTextMarkdownToken, inline_blocks[wall_index_in_inlines]
                )
                wall_index_in_inlines = delimiter_stack.index(special_token)
                break
            wall_index_in_inlines -= 1
        POGGER.debug(">>wall_index_in_inlines(mod)>>$", wall_index_in_inlines)
        return wall_index_in_inlines

    @staticmethod
    def __reset_token_text(inline_blocks: List[MarkdownToken]) -> None:
        """
        Once we are completed with any emphasis processing, ensure that any
        special emphasis tokens are limited to the specified lengths.
        """

        for next_block in inline_blocks:
            if next_block.is_special_text:
                special_token = cast(SpecialTextMarkdownToken, next_block)
                special_token.adjust_token_text_by_repeat_count()

    @staticmethod
    def __clear_remaining_emphasis(
        delimiter_stack: List[SpecialTextMarkdownToken], stack_bottom: int
    ) -> None:
        """
        After processing is finished, clear any active states to ensure we don't
        process them in the future.
        """

        clear_index = stack_bottom + 1
        while clear_index < len(delimiter_stack):
            delimiter_stack[clear_index].deactivate()
            clear_index += 1

    @staticmethod
    def __is_right_flanking_delimiter_run(
        current_token: SpecialTextMarkdownToken,
    ) -> bool:
        """
        Is the current token a right flanking delimiter run?
        """

        assert (
            current_token.preceding_two is not None
        ), "Preceeding character string cannot be None."
        assert (
            current_token.following_two is not None
        ), "Following character string cannot be None."
        preceding_two, following_two = (
            current_token.preceding_two.rjust(2, ParserHelper.space_character),
            current_token.following_two.ljust(2, ParserHelper.space_character),
        )

        return not Constants.unicode_whitespace.contains(preceding_two[-1]) and (
            not Constants.punctuation_characters.contains(preceding_two[-1])
            or (
                Constants.punctuation_characters.contains(preceding_two[-1])
                and (
                    Constants.unicode_whitespace.contains(following_two[0])
                    or Constants.punctuation_characters.contains(following_two[0])
                )
            )
        )

    @staticmethod
    def __is_left_flanking_delimiter_run(
        current_token: SpecialTextMarkdownToken,
    ) -> bool:
        """
        Is the current token a left flanking delimiter run?
        """
        assert (
            current_token.preceding_two is not None
        ), "Preceeding character string cannot be None."
        assert (
            current_token.following_two is not None
        ), "Following character string cannot be None."
        preceding_two, following_two = (
            current_token.preceding_two.rjust(2, ParserHelper.space_character),
            current_token.following_two.ljust(2, ParserHelper.space_character),
        )

        return not Constants.unicode_whitespace.contains(following_two[0]) and (
            not Constants.punctuation_characters.contains(following_two[0])
            or (
                Constants.punctuation_characters.contains(following_two[0])
                and (
                    Constants.unicode_whitespace.contains(preceding_two[-1])
                    or Constants.punctuation_characters.contains(preceding_two[-1])
                )
            )
        )

    @staticmethod
    def __is_potential_closer(current_token: SpecialTextMarkdownToken) -> bool:
        """
        Determine if the current token is a potential closer.
        """

        assert (
            current_token.token_text[0] in EmphasisHelper.get_inline_emphasis()
        ), "Must be a valid emphasis character."

        # Rule 3 and 7
        if current_token.token_text[0] == EmphasisHelper.__simple_emphasis:
            is_closer = EmphasisHelper.__is_right_flanking_delimiter_run(current_token)
        elif current_token.token_text[0] == EmphasisHelper.__strikethrough_emphasis:
            is_closer = (
                EmphasisHelper.__is_right_flanking_delimiter_run(current_token)
                if len(current_token.token_text) < 3
                else False
            )
        # Rule 4 and 8
        else:
            assert (
                current_token.token_text[0] == EmphasisHelper.__complex_emphasis
            ), "Must be a valid emphasis character."
            if is_closer := EmphasisHelper.__is_right_flanking_delimiter_run(
                current_token
            ):
                assert (
                    current_token.following_two is not None
                ), "Following character string cannot be None."
                is_left_flanking, following_two = (
                    EmphasisHelper.__is_left_flanking_delimiter_run(current_token),
                    current_token.following_two.ljust(2, ParserHelper.space_character),
                )
                is_closer = not is_left_flanking or (
                    is_left_flanking
                    and Constants.punctuation_characters.contains(following_two[0])
                )
        return is_closer

    @staticmethod
    def __is_potential_opener(current_token: SpecialTextMarkdownToken) -> bool:
        """
        Determine if the current token is a potential opener.
        """

        assert (
            current_token.token_text[0] in EmphasisHelper.get_inline_emphasis()
        ), "Must be a valid emphasis character."

        # Rule 1
        if current_token.token_text[0] == EmphasisHelper.__simple_emphasis:
            is_opener = EmphasisHelper.__is_left_flanking_delimiter_run(current_token)
            # POGGER.debug("is_opener (simple)=$", is_opener)
        elif current_token.token_text[0] == EmphasisHelper.__strikethrough_emphasis:
            is_opener = (
                EmphasisHelper.__is_left_flanking_delimiter_run(current_token)
                if len(current_token.token_text) < 3
                else False
            )
        else:
            assert (
                current_token.token_text[0] == EmphasisHelper.__complex_emphasis
            ), "Must be a valid emphasis character."
            is_opener = EmphasisHelper.__is_left_flanking_delimiter_run(current_token)
            # POGGER.debug("is_opener (complex)=$", is_opener)
            if is_opener:
                assert (
                    current_token.preceding_two is not None
                ), "Preceeding character string cannot be None."
                is_right_flanking, preceding_two = (
                    EmphasisHelper.__is_right_flanking_delimiter_run(current_token),
                    current_token.preceding_two.rjust(2, ParserHelper.space_character),
                )
                # POGGER.debug("is_opener (is_right_flanking)=$", is_right_flanking)
                # POGGER.debug("is_opener (preceding_two)=:$:", current_token.preceding_two)
                # POGGER.debug("is_opener (preceding_two)=:$:", preceding_two)
                is_opener = not is_right_flanking or (
                    is_right_flanking
                    and Constants.punctuation_characters.contains(preceding_two[-1])
                )
        return is_opener

    @staticmethod
    def __is_open_close_emphasis_valid(
        open_token: SpecialTextMarkdownToken, close_token: SpecialTextMarkdownToken
    ) -> bool:
        """
        Determine if these two tokens together make a valid open/close emphasis pair.
        """

        # POGGER.debug("  __is_open_close_emphasis_valid")
        # POGGER.debug("  open_token: token_text=:$:, is_active=$", open_token.token_text, open_token.is_active)
        # POGGER.debug("  close_token: token_text=:$:, is_active=$", close_token.token_text, close_token.is_active)
        is_valid_opener = False
        if not (
            open_token.token_text
            and open_token.token_text[0] == close_token.token_text[0]
        ):
            POGGER.debug("  delimiter mismatch")
        elif not open_token.is_active:
            POGGER.debug("  not active")
        else:
            is_valid_opener = EmphasisHelper.__is_potential_opener(open_token)
            POGGER.debug("is_valid_opener>>$", is_valid_opener)
            if is_valid_opener:
                is_closer_both = EmphasisHelper.__is_potential_closer(
                    close_token
                ) and EmphasisHelper.__is_potential_opener(close_token)
                # POGGER.debug("is_closer_both>>$", is_closer_both)
                is_opener_both = EmphasisHelper.__is_potential_closer(
                    open_token
                ) and EmphasisHelper.__is_potential_opener(open_token)
                # POGGER.debug("is_opener_both>>$", is_opener_both)
                if is_closer_both or is_opener_both:
                    sum_repeat_count = (
                        close_token.repeat_count + open_token.repeat_count
                    )
                    # POGGER.debug("sum_delims>>$", sum_repeat_count)
                    # POGGER.debug("closer_delims>>$", close_token.repeat_count)
                    # POGGER.debug("opener_delims>>$", open_token.repeat_count)

                    if sum_repeat_count % 3 == 0:
                        is_valid_opener = (
                            close_token.repeat_count % 3 == 0
                            and open_token.repeat_count % 3 == 0
                        )

        return is_valid_opener
