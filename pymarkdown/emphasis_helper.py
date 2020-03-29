"""
Emphasis helper
"""
from pymarkdown.constants import Constants
from pymarkdown.markdown_token import (
    EmphasisMarkdownToken,
    EndMarkdownToken,
    MarkdownToken,
    SpecialTextMarkdownToken,
)


# pylint: disable=too-few-public-methods
class EmphasisHelper:
    """
    Class to helper with the parsing of emphasis for inline elements.
    """

    @staticmethod
    def __process_emphasis_pair(
        inline_blocks, open_token, close_token, current_position
    ):
        """
        Given that we have found a valid open and close block, process them.
        """

        # Figure out whether we have emphasis or strong emphasis
        emphasis_length = 1
        if close_token.repeat_count >= 2 and open_token.repeat_count >= 2:
            emphasis_length = 2

        # add emph node in main stream
        start_index_in_blocks = inline_blocks.index(open_token)
        inline_blocks.insert(
            start_index_in_blocks + 1, EmphasisMarkdownToken(emphasis_length),
        )
        end_index_in_blocks = inline_blocks.index(close_token)
        inline_blocks.insert(
            end_index_in_blocks,
            EndMarkdownToken(
                MarkdownToken.token_inline_emphasis, "", str(emphasis_length),
            ),
        )
        end_index_in_blocks = end_index_in_blocks + 1

        # remove emphasis_length from open and close nodes
        print(
            str(end_index_in_blocks)
            + ">>close_token>>"
            + close_token.show_process_emphasis()
            + "<<"
        )
        close_token.reduce_repeat_count(emphasis_length)
        if not close_token.repeat_count:
            inline_blocks.remove(close_token)
            print("close_token>>removed")
            end_index_in_blocks = end_index_in_blocks - 1
            close_token.active = False
        else:
            current_position = current_position - 1
        print("close_token>>" + close_token.show_process_emphasis() + "<<")

        print(
            str(start_index_in_blocks)
            + ">>open_token>>"
            + open_token.show_process_emphasis()
            + "<<"
        )
        open_token.reduce_repeat_count(emphasis_length)
        if not open_token.repeat_count:
            inline_blocks.remove(open_token)
            print("open_token>>removed")
            end_index_in_blocks = end_index_in_blocks - 1
            open_token.active = False
        print("open_token>>" + open_token.show_process_emphasis() + "<<")

        # "remove" between start and end from delimiter_stack
        inline_index = start_index_in_blocks + 1
        while inline_index < end_index_in_blocks:
            print(
                "inline_index>>"
                + str(inline_index)
                + ">>end>>"
                + str(end_index_in_blocks)
                + ">>"
                + str(len(inline_blocks))
            )
            if isinstance(inline_blocks[inline_index], SpecialTextMarkdownToken):
                inline_blocks[inline_index].active = False
            inline_index = inline_index + 1

        return current_position

    @staticmethod
    def __find_token_in_delimiter_stack(inline_blocks, delimiter_stack, wall_token):
        """
        Find the specified token in the delimiter stack, based solely on
        position in the inline_blocks.
        """

        if wall_token:
            wall_index_in_inlines = inline_blocks.index(wall_token)
            print(">>wall_index_in_inlines>>" + str(wall_index_in_inlines))
            while wall_index_in_inlines >= 0:
                if isinstance(
                    inline_blocks[wall_index_in_inlines], SpecialTextMarkdownToken
                ):
                    wall_index_in_inlines = delimiter_stack.index(
                        inline_blocks[wall_index_in_inlines]
                    )
                    break
                wall_index_in_inlines = wall_index_in_inlines - 1
            print(">>wall_index_in_inlines(mod)>>" + str(wall_index_in_inlines))
            stack_bottom = wall_index_in_inlines
        else:
            stack_bottom = -1
        return stack_bottom

    @staticmethod
    def __reset_token_text(inline_blocks):
        """
        Once we are completed with any emphasis processing, ensure that any
        special emphasis tokens are limited to the specified lengths.
        """

        for next_block in inline_blocks:
            if isinstance(next_block, SpecialTextMarkdownToken):
                next_block.token_text = next_block.token_text[
                    0 : next_block.repeat_count
                ]
                next_block.compose_extra_data_field()

    @staticmethod
    def __clear_remaining_emphasis(delimiter_stack, stack_bottom):
        """
        After processing is finished, clear any active states to ensure we don't
        process them in the future.
        """

        clear_index = stack_bottom + 1
        while clear_index < len(delimiter_stack):
            delimiter_stack[clear_index].active = False
            clear_index = clear_index + 1

    @staticmethod
    def __is_right_flanking_delimiter_run(current_token):
        """
        Is the current token a right flanking delimiter run?
        """

        preceding_two = current_token.preceding_two.rjust(2, " ")
        following_two = current_token.following_two.ljust(2, " ")

        return preceding_two[-1] not in Constants.unicode_whitespace and (
            not preceding_two[-1] in Constants.punctuation_characters
            or (
                preceding_two[-1] in Constants.punctuation_characters
                and (
                    following_two[0] in Constants.unicode_whitespace
                    or following_two[0] in Constants.punctuation_characters
                )
            )
        )

    @staticmethod
    def __is_left_flanking_delimiter_run(current_token):
        """
        Is the current token a left flanking delimiter run?
        """

        preceding_two = current_token.preceding_two.rjust(2, " ")
        following_two = current_token.following_two.ljust(2, " ")

        return following_two[0] not in Constants.unicode_whitespace and (
            not following_two[0] in Constants.punctuation_characters
            or (
                following_two[0] in Constants.punctuation_characters
                and (
                    preceding_two[-1] in Constants.unicode_whitespace
                    or preceding_two[-1] in Constants.punctuation_characters
                )
            )
        )

    @staticmethod
    def __is_potential_closer(current_token):
        """
        Determine if the current token is a potential closer.
        """

        assert current_token.token_text[0] in Constants.inline_emphasis

        # Rule 3 and 7
        is_closer = False
        if current_token.token_text[0] == "*":
            is_closer = EmphasisHelper.__is_right_flanking_delimiter_run(current_token)
        # Rule 4 and 8
        else:  # elif current_token.token_text[0] == "_":
            is_closer = EmphasisHelper.__is_right_flanking_delimiter_run(current_token)
            if is_closer:
                is_left_flanking = EmphasisHelper.__is_left_flanking_delimiter_run(
                    current_token
                )

                following_two = current_token.following_two.ljust(2, " ")
                is_closer = not is_left_flanking or (
                    is_left_flanking
                    and following_two[0] in Constants.punctuation_characters
                )
        return is_closer

    @staticmethod
    def __is_potential_opener(current_token):
        """
        Determine if the current token is a potential opener.
        """

        assert current_token.token_text[0] in Constants.inline_emphasis

        # Rule 1
        is_opener = False
        if current_token.token_text[0] == "*":
            is_opener = EmphasisHelper.__is_left_flanking_delimiter_run(current_token)
        else:  # elif current_token.token_text[0] == "_":
            is_opener = EmphasisHelper.__is_left_flanking_delimiter_run(current_token)
            if is_opener:
                is_right_flanking = EmphasisHelper.__is_right_flanking_delimiter_run(
                    current_token
                )
                preceding_two = current_token.preceding_two.ljust(2, " ")
                is_opener = not is_right_flanking or (
                    is_right_flanking
                    and preceding_two[-1] in Constants.punctuation_characters
                )
        return is_opener

    @staticmethod
    def __is_open_close_emphasis_valid(open_token, close_token):
        """
        Determine if these two tokens together make a valid open/close emphasis pair.
        """

        matching_delimiter = close_token.token_text[0]
        is_valid_opener = False

        if not (
            open_token.token_text and open_token.token_text[0] == matching_delimiter
        ):
            print("  delimiter mismatch")
        elif not open_token.active:
            print("  not active")
        elif open_token.active and EmphasisHelper.__is_potential_opener(open_token):
            is_valid_opener = True
            is_closer_both = EmphasisHelper.__is_potential_closer(
                close_token
            ) and EmphasisHelper.__is_potential_opener(close_token)
            print("is_closer_both>>" + str(is_closer_both))
            is_opener_both = EmphasisHelper.__is_potential_closer(
                open_token
            ) and EmphasisHelper.__is_potential_opener(open_token)
            print("is_opener_both>>" + str(is_opener_both))
            if is_closer_both or is_opener_both:
                sum_repeat_count = close_token.repeat_count + open_token.repeat_count
                print("sum_delims>>" + str(sum_repeat_count))
                print("closer_delims>>" + str(close_token.repeat_count))
                print("opener_delims>>" + str(open_token.repeat_count))

                if sum_repeat_count % 3 == 0:
                    is_valid_opener = (
                        close_token.repeat_count % 3 == 0
                        and open_token.repeat_count % 3 == 0
                    )

        return is_valid_opener

    @staticmethod
    def resolve_inline_emphasis(inline_blocks, wall_token):
        """
        Resolve the inline emphasis by interpreting the special text tokens.
        """

        delimiter_stack = []
        special_count = 0
        for next_block in inline_blocks:
            print("special_count>>" + str(special_count) + ">>" + str(next_block))
            special_count = special_count + 1
            if not isinstance(next_block, SpecialTextMarkdownToken):
                continue
            print(
                "i>>"
                + str(len(delimiter_stack))
                + ">>"
                + next_block.show_process_emphasis()
            )
            delimiter_stack.append(next_block)

        stack_bottom = EmphasisHelper.__find_token_in_delimiter_stack(
            inline_blocks, delimiter_stack, wall_token
        )
        current_position = stack_bottom + 1
        openers_bottom = stack_bottom
        if current_position < len(delimiter_stack):
            print(
                "BLOCK("
                + str(current_position)
                + ") of ("
                + str(len(delimiter_stack))
                + ")"
            )
            print(
                "BLOCK("
                + str(current_position)
                + ")-->"
                + delimiter_stack[current_position].show_process_emphasis()
            )

            while current_position < (len(delimiter_stack) - 1):
                current_position = current_position + 1
                print(
                    "Block("
                    + str(current_position)
                    + ")-->"
                    + delimiter_stack[current_position].show_process_emphasis()
                )
                if not delimiter_stack[current_position].active:
                    print("not active")
                    continue
                if (
                    delimiter_stack[current_position].token_text[0]
                    not in Constants.inline_emphasis
                ):
                    print("not emphasis")
                    continue
                if not EmphasisHelper.__is_potential_closer(
                    delimiter_stack[current_position]
                ):
                    print("not closer")
                    continue

                close_token = delimiter_stack[current_position]
                print("potential closer-->" + str(current_position))
                scan_index = current_position - 1
                is_valid_opener = False
                while (
                    scan_index >= 0
                    and scan_index > stack_bottom
                    and scan_index > openers_bottom
                ):
                    print("potential opener:" + str(scan_index))
                    open_token = delimiter_stack[scan_index]
                    is_valid_opener = EmphasisHelper.__is_open_close_emphasis_valid(
                        open_token, close_token
                    )
                    if is_valid_opener:
                        break
                    scan_index = scan_index - 1
                    print(
                        "scan_index-->"
                        + str(scan_index)
                        + ">stack_bottom>"
                        + str(stack_bottom)
                        + ">openers_bottom>"
                        + str(openers_bottom)
                        + ">"
                    )

                if is_valid_opener:
                    print("FOUND OPEN")
                    current_position = EmphasisHelper.__process_emphasis_pair(
                        inline_blocks, open_token, close_token, current_position
                    )
                else:
                    # openers_bottom = current_position - 1
                    print("NOT FOUND OPEN, openers_bottom=" + str(openers_bottom))

                print("next->" + str(current_position))

        EmphasisHelper.__reset_token_text(inline_blocks)
        EmphasisHelper.__clear_remaining_emphasis(delimiter_stack, stack_bottom)
        return inline_blocks


# pylint: enable=too-few-public-methods
