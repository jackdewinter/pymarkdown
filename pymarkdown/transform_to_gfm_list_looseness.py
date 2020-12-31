"""
Module to handle the calculationof list looseness for the GRM transformer.
"""
import logging

LOGGER = logging.getLogger(__name__)


class TransformToGfmListLooseness:
    """
    Class to handle the calculationof list looseness for the GRM transformer.
    """

    @staticmethod
    def calculate_list_looseness(actual_tokens, actual_token_index, next_token):
        """
        Based on the first token in a list, compute the "looseness" of the list.
        """

        LOGGER.debug("\n\n__calculate_list_looseness>>%s", str(actual_token_index))
        is_loose = False
        current_token_index = actual_token_index + 1
        stack_count = 0
        while True:

            current_token = actual_tokens[current_token_index]
            check_me = False
            stop_me = False
            if current_token.is_list_start:
                LOGGER.debug("cll>>start list>>%s", str(current_token))
                check_me, stack_count = TransformToGfmListLooseness.__handle_list_start(
                    stack_count
                )
            elif current_token.is_new_list_item:
                LOGGER.debug("cll>>new list item>>%s", str(current_token))
                check_me = TransformToGfmListLooseness.__handle_new_list_item(
                    current_token, stack_count
                )
            elif current_token.is_block_quote_start:
                LOGGER.debug("cll>>start block quote>>%s", str(current_token))
                stack_count = TransformToGfmListLooseness.__handle_block_quote_start(
                    stack_count
                )
            elif current_token.is_block_quote_end:
                LOGGER.debug("cll>>end block quote>>%s", str(current_token))
                stack_count = TransformToGfmListLooseness.__handle_block_quote_end(
                    stack_count
                )
            elif current_token.is_list_end:
                LOGGER.debug("cll>>end list>>%s", str(current_token))
                (
                    stop_me,
                    is_loose,
                    stack_count,
                ) = TransformToGfmListLooseness.__handle_list_end(
                    stack_count,
                    is_loose,
                    stop_me,
                    actual_tokens,
                    current_token_index,
                )
            elif actual_tokens[current_token_index - 1].is_blank_line:
                check_me = TransformToGfmListLooseness.__handle_blank_line(
                    current_token, stack_count, actual_tokens, current_token_index
                )

            LOGGER.debug(
                ">>stack_count>>%s>>#%s:%s>>check=%s",
                str(stack_count),
                str(current_token_index),
                str(actual_tokens[current_token_index]),
                str(check_me),
            )
            if check_me:
                LOGGER.debug("check-->?")
                if TransformToGfmListLooseness.__is_token_loose(
                    actual_tokens, current_token_index
                ):
                    is_loose = True
                    stop_me = True
                    LOGGER.debug("check-->Loose")
                else:
                    LOGGER.debug("check-->Normal")
            if stop_me:
                break
            current_token_index += 1

        assert current_token_index != len(actual_tokens)
        next_token.is_loose = is_loose
        LOGGER.debug(
            "__calculate_list_looseness<<%s<<%s\n\n",
            str(actual_token_index),
            str(is_loose),
        )
        return is_loose

    @staticmethod
    def __handle_list_start(stack_count):
        check_me = stack_count == 0
        stack_count += 1
        LOGGER.debug(">>list--new>>%s", str(stack_count))
        return check_me, stack_count

    @staticmethod
    def __handle_new_list_item(current_token, stack_count):
        check_me = stack_count == 0
        assert not current_token.is_block
        LOGGER.debug(">>list--item>>%s", str(stack_count))
        return check_me

    @staticmethod
    def __handle_list_end(
        stack_count,
        is_loose,
        stop_me,
        actual_tokens,
        current_token_index,
    ):
        if stack_count == 0:
            stop_me = True
        else:
            stack_count -= 1
            if TransformToGfmListLooseness.__correct_for_me(
                actual_tokens, current_token_index
            ):
                is_loose = True
                stop_me = True
                LOGGER.debug("!!!latent-LOOSE!!!")
        LOGGER.debug(">>list--end>>%s", str(stack_count))
        return stop_me, is_loose, stack_count

    @staticmethod
    def __handle_block_quote_start(stack_count):
        stack_count += 1
        LOGGER.debug(">>block--new>>%s", str(stack_count))
        return stack_count

    @staticmethod
    def __handle_block_quote_end(stack_count):
        stack_count -= 1
        LOGGER.debug(">>block--end>>%s", str(stack_count))
        return stack_count

    @staticmethod
    def __handle_blank_line(
        current_token, stack_count, actual_tokens, current_token_index
    ):
        search_back_index = current_token_index - 2
        pre_prev_token = actual_tokens[search_back_index]
        LOGGER.debug(">>pre_prev_token>>%s", str(pre_prev_token))

        while pre_prev_token.is_blank_line:
            search_back_index -= 1
            pre_prev_token = actual_tokens[search_back_index]

        if pre_prev_token.is_end_token:
            assert pre_prev_token.start_markdown_token, str(pre_prev_token)
            pre_prev_token = pre_prev_token.start_markdown_token
            LOGGER.debug(">>end_>using_start>>%s", str(pre_prev_token))

        current_check = (
            current_token.is_block and not current_token.is_link_reference_definition
        )
        pre_prev_check = (
            pre_prev_token.is_block and not pre_prev_token.is_link_reference_definition
        )

        LOGGER.debug(">>other--stack_count>>%s", str(stack_count))
        LOGGER.debug(
            ">>other--current_token>>%s>>%s",
            str(current_token),
            str(current_check),
        )
        LOGGER.debug(
            ">>other--current_token-2>>%s>>%s",
            str(pre_prev_token),
            str(pre_prev_check),
        )
        check_me = stack_count == 0 and current_check and pre_prev_check
        return check_me

    @staticmethod
    def __correct_for_me(actual_tokens, current_token_index):
        correct_closure = False
        assert current_token_index > 0

        is_valid = True
        LOGGER.debug(">>prev>>%s", str(actual_tokens[current_token_index - 1]))
        if actual_tokens[current_token_index - 1].is_blank_line:
            search_index = current_token_index + 1
            while (
                search_index < len(actual_tokens)
                and actual_tokens[search_index].is_list_end
            ):
                search_index += 1
            LOGGER.debug(
                ">>ss>>%s>>len>>%s", str(search_index), str(len(actual_tokens))
            )
            is_valid = search_index != len(actual_tokens)
        if is_valid:
            LOGGER.debug(">>current>>%s", str(actual_tokens[current_token_index]))
            LOGGER.debug(">>current-1>>%s", str(actual_tokens[current_token_index - 1]))
            correct_closure = TransformToGfmListLooseness.__is_token_loose(
                actual_tokens, current_token_index
            )
            LOGGER.debug(">>correct_closure>>%s", str(correct_closure))
        return correct_closure

    @staticmethod
    def __is_token_loose(actual_tokens, current_token_index):
        """
        Check to see if this token inspires looseness.
        """

        check_index = current_token_index - 1
        token_to_check = actual_tokens[check_index]
        LOGGER.debug("token_to_check-->%s", str(token_to_check))

        while token_to_check.is_link_reference_definition:
            check_index -= 1
            token_to_check = actual_tokens[check_index]

        LOGGER.debug("token_to_check-->%s", str(token_to_check))
        if token_to_check.is_blank_line:
            LOGGER.debug("before_blank-->%s", str(actual_tokens[check_index - 1]))
            if (
                actual_tokens[check_index - 1].is_new_list_item
                or actual_tokens[check_index - 1].is_list_start
            ):
                LOGGER.debug("!!!Starting Blank!!!")
            else:
                LOGGER.debug("!!!LOOSE!!!")
                return True
        return False

    @staticmethod
    def __find_owning_list_start(actual_tokens, actual_token_index):
        """
        Figure out what the list start for the current token is.
        """

        current_index = actual_token_index
        assert not actual_tokens[current_index].is_list_start

        current_index -= 1
        keep_going = True
        stack_count = 0
        while keep_going and current_index >= 0:
            if actual_tokens[current_index].is_list_start:
                if stack_count == 0:
                    keep_going = False
                else:
                    stack_count -= 1
            elif actual_tokens[current_index].is_list_end:
                stack_count += 1
            if keep_going:
                current_index -= 1
        return current_index

    @staticmethod
    def reset_list_looseness(actual_tokens, actual_token_index):
        """
        Based on where we are within the actual tokens being emitted, figure
        out the correct list looseness to use.
        """

        LOGGER.debug("!!!!!!!!!!!!!!!%s", str(actual_token_index))
        search_index = actual_token_index + 1
        stack_count = 0
        while search_index < len(actual_tokens):
            LOGGER.debug(
                "!!%s::%s::%s",
                str(stack_count),
                str(search_index),
                str(actual_tokens[search_index]),
            )
            if actual_tokens[search_index].is_list_start:
                stack_count += 1
            elif actual_tokens[search_index].is_list_end:
                if not stack_count:
                    break
                stack_count -= 1
            search_index += 1
        LOGGER.debug(
            "!!!!!!!!!!!!!!!%s-of-%s", str(search_index), str(len(actual_tokens))
        )
        # check to see where we are, then grab the matching start to find
        # the loose
        if search_index == len(actual_tokens):
            is_in_loose_list = True
        else:
            LOGGER.debug(">>reset_list_looseness-token_list_start>>")
            new_index = TransformToGfmListLooseness.__find_owning_list_start(
                actual_tokens, search_index
            )
            LOGGER.debug(">>reset_list_looseness>>%s", str(new_index))
            is_in_loose_list = actual_tokens[new_index].is_loose
        LOGGER.debug("           is_in_loose_list=%s", str(is_in_loose_list))
        return is_in_loose_list
