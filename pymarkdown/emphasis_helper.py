"""
Emphasis helper
"""
import logging

from pymarkdown.constants import Constants
from pymarkdown.inline_markdown_token import EmphasisMarkdownToken
from pymarkdown.parser_helper import ParserHelper

LOGGER = logging.getLogger(__name__)


# pylint: disable=too-few-public-methods
class EmphasisHelper:
    """
    Class to helper with the parsing of emphasis for inline elements.
    """

    __simple_emphasis = "*"
    __complex_emphasis = "_"
    inline_emphasis = __simple_emphasis + __complex_emphasis

    @staticmethod
    def resolve_inline_emphasis(inline_blocks, wall_token):
        """
        Resolve the inline emphasis by interpreting the special text tokens.
        """
        delimiter_stack = []
        special_count = 0
        for next_block in inline_blocks:
            LOGGER.debug(
                "special_count>>%s>>%s",
                str(special_count),
                ParserHelper.make_value_visible(next_block),
            )
            special_count += 1
            if not next_block.is_special_text:
                continue
            LOGGER.debug(
                "i>>%s>>%s",
                str(len(delimiter_stack)),
                next_block.show_process_emphasis(),
            )
            delimiter_stack.append(next_block)

        stack_bottom = EmphasisHelper.__find_token_in_delimiter_stack(
            inline_blocks, delimiter_stack, wall_token
        )
        current_position = stack_bottom + 1
        openers_bottom = stack_bottom
        if current_position < len(delimiter_stack):
            LOGGER.debug(
                "BLOCK(%s) of (%s)", str(current_position), str(len(delimiter_stack))
            )
            LOGGER.debug(
                "BLOCK(%s)-->%s",
                str(current_position),
                delimiter_stack[current_position].show_process_emphasis(),
            )

            while current_position < (len(delimiter_stack) - 1):
                current_position += 1
                LOGGER.debug(
                    "Block(%s)-->%s",
                    str(current_position),
                    delimiter_stack[current_position].show_process_emphasis(),
                )
                if not delimiter_stack[current_position].is_active:
                    LOGGER.debug("not active")
                    continue
                if (
                    delimiter_stack[current_position].token_text[0]
                    not in EmphasisHelper.inline_emphasis
                ):
                    LOGGER.debug("not emphasis")
                    continue
                if not EmphasisHelper.__is_potential_closer(
                    delimiter_stack[current_position]
                ):
                    LOGGER.debug("not closer")
                    continue

                close_token = delimiter_stack[current_position]
                LOGGER.debug("potential closer-->%s", str(current_position))
                scan_index = current_position - 1
                found_opener = None
                while (
                    scan_index >= 0
                    and scan_index > stack_bottom
                    and scan_index > openers_bottom
                ):
                    LOGGER.debug("potential opener:%s", str(scan_index))
                    open_token = delimiter_stack[scan_index]
                    is_valid_opener = EmphasisHelper.__is_open_close_emphasis_valid(
                        open_token, close_token
                    )
                    if is_valid_opener:
                        found_opener = open_token
                        break
                    scan_index -= 1
                    LOGGER.debug(
                        "scan_index-->%s>stack_bottom>%s>openers_bottom>%s>",
                        str(scan_index),
                        str(stack_bottom),
                        str(openers_bottom),
                    )

                if found_opener:
                    LOGGER.debug("FOUND OPEN")
                    current_position = EmphasisHelper.__process_emphasis_pair(
                        inline_blocks,
                        found_opener,
                        close_token,
                        current_position,
                    )
                else:
                    # openers_bottom = current_position - 1
                    LOGGER.debug(
                        "NOT FOUND OPEN, openers_bottom=%s", str(openers_bottom)
                    )

                LOGGER.debug("next->%s", str(current_position))

        EmphasisHelper.__reset_token_text(inline_blocks)
        EmphasisHelper.__clear_remaining_emphasis(delimiter_stack, stack_bottom)
        return inline_blocks

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
        emphasis_character = open_token.token_text[0]

        # add emph node in main stream
        LOGGER.debug("open_token>>%s", str(open_token))
        LOGGER.debug("close_token>>%s", str(close_token))

        LOGGER.debug("open_token.repeat_count>>%s", str(open_token.repeat_count))
        LOGGER.debug("emphasis_length>>%s", str(emphasis_length))
        open_column_number_delta = 0
        if emphasis_length < open_token.repeat_count:
            open_column_number_delta = open_token.repeat_count - emphasis_length
        LOGGER.debug("open_column_number_delta>>%s", str(open_column_number_delta))

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
                False,
                line_number=close_token.line_number,
                column_number=close_token.column_number,
            ),
        )
        end_index_in_blocks += 1

        # remove emphasis_length from open and close nodes
        LOGGER.debug(
            "%s>>close_token>>%s<<",
            str(end_index_in_blocks),
            close_token.show_process_emphasis(),
        )
        close_token.reduce_repeat_count(emphasis_length, adjust_column_number=True)
        if not close_token.repeat_count:
            inline_blocks.remove(close_token)
            LOGGER.debug("close_token>>removed")
            end_index_in_blocks -= 1
            close_token.deactivate()
        else:
            current_position -= 1
        LOGGER.debug("close_token>>%s<<", close_token.show_process_emphasis())

        LOGGER.debug(
            "%s>>open_token>>%s<<",
            str(start_index_in_blocks),
            open_token.show_process_emphasis(),
        )
        open_token.reduce_repeat_count(emphasis_length)
        if not open_token.repeat_count:
            inline_blocks.remove(open_token)
            LOGGER.debug("open_token>>removed")
            end_index_in_blocks -= 1
            open_token.deactivate()
        LOGGER.debug("open_token>>%s<<", open_token.show_process_emphasis())

        # "remove" between start and end from delimiter_stack
        inline_index = start_index_in_blocks + 1
        while inline_index < end_index_in_blocks:
            LOGGER.debug(
                "inline_index>>%s>>end>>%s>>%s",
                str(inline_index),
                str(end_index_in_blocks),
                str(len(inline_blocks)),
            )
            if inline_blocks[inline_index].is_special_text:
                inline_blocks[inline_index].deactivate()
            inline_index += 1

        return current_position

    @staticmethod
    def __find_token_in_delimiter_stack(inline_blocks, delimiter_stack, wall_token):
        """
        Find the specified token in the delimiter stack, based solely on
        position in the inline_blocks.
        """

        if wall_token:
            wall_index_in_inlines = inline_blocks.index(wall_token)
            LOGGER.debug(">>wall_index_in_inlines>>%s", str(wall_index_in_inlines))
            while wall_index_in_inlines >= 0:
                if inline_blocks[wall_index_in_inlines].is_special_text:
                    wall_index_in_inlines = delimiter_stack.index(
                        inline_blocks[wall_index_in_inlines]
                    )
                    break
                wall_index_in_inlines -= 1
            LOGGER.debug(">>wall_index_in_inlines(mod)>>%s", str(wall_index_in_inlines))
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
            if next_block.is_special_text:
                next_block.adjust_token_text_by_repeat_count()

    @staticmethod
    def __clear_remaining_emphasis(delimiter_stack, stack_bottom):
        """
        After processing is finished, clear any active states to ensure we don't
        process them in the future.
        """

        clear_index = stack_bottom + 1
        while clear_index < len(delimiter_stack):
            delimiter_stack[clear_index].deactivate()
            clear_index += 1

    @staticmethod
    def __is_right_flanking_delimiter_run(current_token):
        """
        Is the current token a right flanking delimiter run?
        """

        preceding_two = current_token.preceding_two.rjust(
            2, ParserHelper.space_character
        )
        following_two = current_token.following_two.ljust(
            2, ParserHelper.space_character
        )

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

        preceding_two = current_token.preceding_two.rjust(
            2, ParserHelper.space_character
        )
        following_two = current_token.following_two.ljust(
            2, ParserHelper.space_character
        )

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

        assert current_token.token_text[0] in EmphasisHelper.inline_emphasis

        # Rule 3 and 7
        if current_token.token_text[0] == EmphasisHelper.__simple_emphasis:
            is_closer = EmphasisHelper.__is_right_flanking_delimiter_run(current_token)
        # Rule 4 and 8
        else:
            assert current_token.token_text[0] == EmphasisHelper.__complex_emphasis
            is_closer = EmphasisHelper.__is_right_flanking_delimiter_run(current_token)
            if is_closer:
                is_left_flanking = EmphasisHelper.__is_left_flanking_delimiter_run(
                    current_token
                )

                following_two = current_token.following_two.ljust(
                    2, ParserHelper.space_character
                )
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

        assert current_token.token_text[0] in EmphasisHelper.inline_emphasis

        # Rule 1
        if current_token.token_text[0] == EmphasisHelper.__simple_emphasis:
            is_opener = EmphasisHelper.__is_left_flanking_delimiter_run(current_token)
        else:
            assert current_token.token_text[0] == EmphasisHelper.__complex_emphasis
            is_opener = EmphasisHelper.__is_left_flanking_delimiter_run(current_token)
            if is_opener:
                is_right_flanking = EmphasisHelper.__is_right_flanking_delimiter_run(
                    current_token
                )
                preceding_two = current_token.preceding_two.ljust(
                    2, ParserHelper.space_character
                )
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
            LOGGER.debug("  delimiter mismatch")
        elif not open_token.is_active:
            LOGGER.debug("  not active")
        elif open_token.is_active and EmphasisHelper.__is_potential_opener(open_token):
            is_valid_opener = True
            is_closer_both = EmphasisHelper.__is_potential_closer(
                close_token
            ) and EmphasisHelper.__is_potential_opener(close_token)
            LOGGER.debug("is_closer_both>>%s", str(is_closer_both))
            is_opener_both = EmphasisHelper.__is_potential_closer(
                open_token
            ) and EmphasisHelper.__is_potential_opener(open_token)
            LOGGER.debug("is_opener_both>>%s", str(is_opener_both))
            if is_closer_both or is_opener_both:
                sum_repeat_count = close_token.repeat_count + open_token.repeat_count
                LOGGER.debug("sum_delims>>%s", str(sum_repeat_count))
                LOGGER.debug("closer_delims>>%s", str(close_token.repeat_count))
                LOGGER.debug("opener_delims>>%s", str(open_token.repeat_count))

                if sum_repeat_count % 3 == 0:
                    is_valid_opener = (
                        close_token.repeat_count % 3 == 0
                        and open_token.repeat_count % 3 == 0
                    )

        return is_valid_opener


# pylint: enable=too-few-public-methods
