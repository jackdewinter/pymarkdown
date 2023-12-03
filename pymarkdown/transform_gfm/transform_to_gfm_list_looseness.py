"""
Module to handle the calculationof list looseness for the GRM transformer.
"""
import logging
from typing import List, Optional, Tuple, cast

from pymarkdown.general.parser_logger import ParserLogger
from pymarkdown.tokens.list_start_markdown_token import ListStartMarkdownToken
from pymarkdown.tokens.markdown_token import EndMarkdownToken, MarkdownToken

POGGER = ParserLogger(logging.getLogger(__name__))


class TransformToGfmListLooseness:
    """
    Class to handle the calculationof list looseness for the GRM transformer.
    """

    @staticmethod
    def calculate_list_looseness(
        actual_tokens: List[MarkdownToken],
        actual_token_index: int,
        next_token: ListStartMarkdownToken,
    ) -> bool:
        """
        Based on the first token in a list, compute the "looseness" of the list.
        """

        POGGER.debug("\n\n__calculate_list_looseness>>$", actual_token_index)
        is_loose, current_token_index, stack_count = False, actual_token_index + 1, 0
        while True:
            current_token = actual_tokens[current_token_index]
            (
                check_me,
                stack_count,
                stop_me,
                is_loose,
            ) = TransformToGfmListLooseness.__calculate_list_looseness_for_containers(
                current_token,
                stack_count,
                is_loose,
                False,
                actual_tokens,
                current_token_index,
            )
            if check_me:
                POGGER.debug("check-->?")
                if TransformToGfmListLooseness.__is_token_loose(
                    actual_tokens, current_token_index
                ):
                    is_loose, stop_me = True, True
                    POGGER.debug("check-->Loose")
                else:
                    POGGER.debug("check-->Normal")
            if stop_me:
                break
            current_token_index += 1

        assert current_token_index != len(actual_tokens)
        POGGER.debug(
            "__calculate_list_looseness<<$<<$\n\n",
            actual_token_index,
            is_loose,
        )
        next_token.is_loose = is_loose
        return is_loose

    # pylint: disable=too-many-arguments
    @staticmethod
    def __calculate_list_looseness_for_containers(
        current_token: MarkdownToken,
        stack_count: int,
        is_loose: bool,
        stop_me: bool,
        actual_tokens: List[MarkdownToken],
        current_token_index: int,
    ) -> Tuple[bool, int, bool, bool]:
        check_me = False
        if current_token.is_list_start:
            POGGER.debug("cll>>start list>>$", current_token)
            check_me, stack_count = TransformToGfmListLooseness.__handle_list_start(
                stack_count
            )
        elif current_token.is_new_list_item:
            POGGER.debug("cll>>new list item>>$", current_token)
            check_me = TransformToGfmListLooseness.__handle_new_list_item(
                current_token, stack_count
            )
        elif current_token.is_block_quote_start:
            POGGER.debug("cll>>start block quote>>$", current_token)
            stack_count = TransformToGfmListLooseness.__handle_block_quote_start(
                stack_count
            )
            check_me = True
        elif current_token.is_block_quote_end:
            POGGER.debug("cll>>end block quote>>$", current_token)
            (
                stop_me,
                is_loose,
                stack_count,
            ) = TransformToGfmListLooseness.__handle_block_quote_end(
                stack_count, actual_tokens, current_token_index, stop_me, is_loose
            )
        elif current_token.is_list_end:
            POGGER.debug("cll>>end list>>$", current_token)
            (
                stop_me,
                is_loose,
                stack_count,
            ) = TransformToGfmListLooseness.__handle_list_end(
                stack_count,
                is_loose,
                actual_tokens,
                current_token_index,
            )
            POGGER.debug("cll>>stop_me>>$", stop_me)
            POGGER.debug("cll>>is_loose>>$", is_loose)
        elif actual_tokens[current_token_index - 1].is_blank_line:
            POGGER.debug("cll>>__handle_blank_line>>")
            check_me = TransformToGfmListLooseness.__handle_blank_line(
                current_token, stack_count, actual_tokens, current_token_index
            )

        POGGER.debug(
            ">>stack_count>>$>>#$:$>>check=$",
            stack_count,
            current_token_index,
            actual_tokens[current_token_index],
            check_me,
        )
        return check_me, stack_count, stop_me, is_loose

    # pylint: enable=too-many-arguments

    @staticmethod
    def __handle_list_start(stack_count: int) -> Tuple[bool, int]:
        POGGER.debug(">>list--new>>$", stack_count)
        return stack_count == 0, stack_count + 1

    @staticmethod
    def __handle_new_list_item(current_token: MarkdownToken, stack_count: int) -> bool:
        assert not current_token.is_block
        POGGER.debug(">>list--item>>$", stack_count)
        return stack_count == 0

    @staticmethod
    def __handle_list_end(
        stack_count: int,
        is_loose: bool,
        actual_tokens: List[MarkdownToken],
        current_token_index: int,
    ) -> Tuple[bool, bool, int]:
        POGGER.debug(">>list--end>>$", stack_count)
        stop_me = not stack_count
        if not stop_me:
            stack_count -= 1
            if not stack_count:
                POGGER.debug("<<check!!")

                check_index = current_token_index + 1
                assert check_index < len(actual_tokens)
                POGGER.debug_with_visible_whitespace(
                    "<<check>>$", actual_tokens[check_index]
                )
                if not actual_tokens[check_index].is_list_end:
                    POGGER.debug("<END OF possibly multiple list ends")
                    search_back_index = current_token_index - 1
                    # while (
                    #     search_back_index >= 0
                    #     and actual_tokens[check_index].is_list_end
                    # ):
                    #     search_back_index -= 1
                    stop_me = TransformToGfmListLooseness.__is_token_loose(
                        actual_tokens, search_back_index + 1
                    )
                    is_loose = stop_me
                    if stop_me:
                        POGGER.debug("!!!latent-LOOSE!!!")
        POGGER.debug("<<list--end>>$", stack_count)
        return stop_me, is_loose, stack_count

    @staticmethod
    def __handle_block_quote_start(stack_count: int) -> int:
        POGGER.debug(">>block--new>>$", stack_count)
        return stack_count + 1

    @staticmethod
    def __handle_block_quote_end_calc(
        actual_tokens: List[MarkdownToken], search_index: int, current_token_index: int
    ) -> Tuple[bool, bool]:
        stop_me = TransformToGfmListLooseness.__is_token_loose(
            actual_tokens, search_index + 1, True
        )
        if stop_me:
            blank_token = actual_tokens[search_index]
            search_index = current_token_index
            next_token = actual_tokens[search_index]
            while search_index >= 0 and not next_token.is_block_quote_start:
                search_index -= 1
                next_token = actual_tokens[search_index]
            block_quote_spaces_count = len(next_token.bleading_spaces.split("\n"))  # type: ignore
            end_block_quote_line = next_token.line_number + block_quote_spaces_count
            stop_me = not blank_token.line_number < end_block_quote_line

        is_loose = stop_me
        if stop_me:
            POGGER.debug("!!!LOOSE-look back at end!!!")
        return is_loose, stop_me

    @staticmethod
    def __handle_block_quote_end(
        stack_count: int,
        actual_tokens: List[MarkdownToken],
        current_token_index: int,
        stop_me: bool,
        is_loose: bool,
    ) -> Tuple[bool, bool, int]:
        POGGER.debug(">>block--end>>$", stack_count)
        old_stack_count = stack_count
        stack_count -= 1
        if old_stack_count and not stack_count:
            search_index = current_token_index - 1
            found_end_token: Optional[MarkdownToken] = actual_tokens[search_index]
            while found_end_token is not None:
                found_end_token = None
                next_token = actual_tokens[search_index]
                if next_token.is_end_token:
                    next_end_token = cast(EndMarkdownToken, next_token)
                    if (
                        next_end_token.start_markdown_token.is_block_quote_start
                        or next_end_token.start_markdown_token.is_list_start
                    ):
                        found_end_token = next_end_token
                        search_index -= 1

            new_index = current_token_index + 1
            keep_checking = (
                new_index < len(actual_tokens) and actual_tokens[new_index].is_end_token
            )
            if keep_checking:
                end_token = cast(EndMarkdownToken, actual_tokens[new_index])
                keep_checking = end_token.start_markdown_token.is_list_start

            if not keep_checking:
                (
                    is_loose,
                    stop_me,
                ) = TransformToGfmListLooseness.__handle_block_quote_end_calc(
                    actual_tokens, search_index, current_token_index
                )
        return stop_me, is_loose, stack_count

    @staticmethod
    def __handle_blank_line(
        current_token: MarkdownToken,
        stack_count: int,
        actual_tokens: List[MarkdownToken],
        current_token_index: int,
    ) -> bool:
        search_back_index = current_token_index - 2
        while actual_tokens[search_back_index].is_blank_line:
            search_back_index -= 1

        pre_prev_token = actual_tokens[search_back_index]
        if pre_prev_token.is_end_token:
            end_token = cast(EndMarkdownToken, pre_prev_token)
            assert end_token.start_markdown_token
            pre_prev_token = end_token.start_markdown_token
            POGGER.debug(">>end_>using_start>>$", pre_prev_token)

        current_check = (
            current_token.is_block and not current_token.is_link_reference_definition
        )
        pre_prev_check = (
            pre_prev_token.is_block and not pre_prev_token.is_link_reference_definition
        )

        POGGER.debug(">>other--stack_count>>$", stack_count)
        POGGER.debug(
            ">>other--current_token>>$>>$",
            current_token,
            current_check,
        )
        POGGER.debug(
            ">>other--current_token-2>>$>>$",
            pre_prev_token,
            pre_prev_check,
        )
        return stack_count == 0 and current_check and pre_prev_check

    @staticmethod
    def __is_token_loose(
        actual_tokens: List[MarkdownToken], current_token_index: int, xx: bool = False
    ) -> bool:
        """
        Check to see if this token inspires looseness.
        """

        check_index = current_token_index - 1
        while actual_tokens[check_index].is_link_reference_definition:
            check_index -= 1
        token_to_check = actual_tokens[check_index]

        POGGER.debug("token_to_check-->$", token_to_check)
        if token_to_check.is_blank_line:
            POGGER.debug("before_blank-->$", actual_tokens[check_index - 1])
            if (
                actual_tokens[check_index - 1].is_new_list_item
                or actual_tokens[check_index - 1].is_list_start
            ):
                POGGER.debug("!!!Starting Blank!!!")
            elif actual_tokens[check_index - 1].is_block_quote_start and xx:
                POGGER.debug("!!!Starting BQ Blank!!!")
            else:
                POGGER.debug("!!!LOOSE!!!")
                return True
        return False

    @staticmethod
    def __find_owning_list_start(
        actual_tokens: List[MarkdownToken], actual_token_index: int
    ) -> int:
        """
        Figure out what the list start for the current token is.
        """

        assert not actual_tokens[actual_token_index].is_list_start
        current_index, stack_count = actual_token_index - 1, 0
        while True:
            assert current_index >= 0
            if actual_tokens[current_index].is_list_start:
                if stack_count == 0:
                    break
                stack_count -= 1
            elif actual_tokens[current_index].is_list_end:
                stack_count += 1
            current_index -= 1
        return current_index

    @staticmethod
    def reset_list_looseness(
        actual_tokens: List[MarkdownToken], actual_token_index: int
    ) -> bool:
        """
        Based on where we are within the actual tokens being emitted, figure
        out the correct list looseness to use.
        """

        POGGER.debug("!!!!!!!!!!!!!!!$", actual_token_index)
        search_index, stack_count, actual_tokens_size = (
            actual_token_index + 1,
            0,
            len(actual_tokens),
        )
        while search_index < actual_tokens_size:
            POGGER.debug(
                "!!$::$::$",
                stack_count,
                search_index,
                actual_tokens[search_index],
            )
            if actual_tokens[search_index].is_list_start:
                stack_count += 1
            elif actual_tokens[search_index].is_list_end:
                if not stack_count:
                    break
                stack_count -= 1
            search_index += 1
        POGGER.debug("!!!!!!!!!!!!!!!$-of-$", search_index, actual_tokens_size)
        # check to see where we are, then grab the matching start to find
        # the loose
        is_in_loose_list = search_index == actual_tokens_size
        if not is_in_loose_list:
            POGGER.debug(">>reset_list_looseness-token_list_start>>")
            new_index = TransformToGfmListLooseness.__find_owning_list_start(
                actual_tokens, search_index
            )
            POGGER.debug(">>reset_list_looseness>>$", new_index)
            list_token = cast(ListStartMarkdownToken, actual_tokens[new_index])
            is_in_loose_list = list_token.is_loose
        POGGER.debug("           is_in_loose_list=$", is_in_loose_list)
        return is_in_loose_list
