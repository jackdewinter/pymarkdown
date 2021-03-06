"""
Link reference definition helper
"""
import logging

from pymarkdown.inline_helper import InlineHelper
from pymarkdown.leaf_markdown_token import LinkReferenceDefinitionMarkdownToken
from pymarkdown.link_helper import LinkHelper
from pymarkdown.parser_helper import ParserHelper
from pymarkdown.requeue_line_info import RequeueLineInfo
from pymarkdown.stack_token import LinkDefinitionStackToken

LOGGER = logging.getLogger(__name__)


# pylint: disable=too-few-public-methods
class LinkReferenceDefinitionHelper:
    """
    Class to helper with the parsing of link reference definitions.
    """

    __lrd_start_character = "["

    # pylint: disable=too-many-locals, too-many-arguments, too-many-statements, too-many-branches
    @staticmethod
    def process_link_reference_definition(
        parser_state,
        position_marker,
        remaining_line_to_parse,
        extracted_whitespace,
        unmodified_line_to_parse,
        original_stack_depth,
        original_document_depth,
    ):
        """
        Process a link deference definition.  Note, this requires a lot of work to
        handle properly because of partial definitions across lines.
        """
        line_to_parse = position_marker.text_to_parse
        start_index = position_marker.index_number

        did_pause_lrd = False
        new_tokens = []

        lines_to_requeue = []
        force_ignore_first_as_lrd = False

        was_started = False
        is_blank_line = not line_to_parse and not start_index
        lrd_stack_token = None
        if parser_state.token_stack[-1].was_link_definition_started:
            was_started = True
            lrd_stack_token = parser_state.token_stack[-1]
            original_stack_depth = lrd_stack_token.original_stack_depth
            original_document_depth = lrd_stack_token.original_document_depth
            LOGGER.debug(
                ">>continuation_lines>>%s<<",
                str(lrd_stack_token.continuation_lines),
            )
            line_to_parse = lrd_stack_token.get_joined_lines(line_to_parse)
            start_index, extracted_whitespace = ParserHelper.extract_whitespace(
                line_to_parse, 0
            )
            LOGGER.debug(
                ">>line_to_parse>>%s<<", ParserHelper.make_value_visible(line_to_parse)
            )

        if was_started:
            LOGGER.debug(">>parse_link_reference_definition>>was_started")
            (
                did_complete_lrd,
                end_lrd_index,
                parsed_lrd_tuple,
            ) = LinkReferenceDefinitionHelper.__parse_link_reference_definition(
                parser_state,
                line_to_parse,
                start_index,
                extracted_whitespace,
                is_blank_line,
            )
            LOGGER.debug(
                ">>parse_link_reference_definition>>was_started>>did_complete_lrd>>%s>>end_lrd_index>>%s>>len(line_to_parse)>>%s",
                str(did_complete_lrd),
                str(end_lrd_index),
                str(len(line_to_parse)),
            )

            if not (
                did_complete_lrd
                or (
                    not is_blank_line
                    and not did_complete_lrd
                    and (end_lrd_index == len(line_to_parse))
                )
            ):
                LOGGER.debug(
                    ">>parse_link_reference_definition>>was_started>>GOT HARD FAILURE"
                )
                (
                    is_blank_line,
                    line_to_parse,
                    did_complete_lrd,
                    end_lrd_index,
                    parsed_lrd_tuple,
                ) = LinkReferenceDefinitionHelper.__process_lrd_hard_failure(
                    parser_state,
                    remaining_line_to_parse,
                    lines_to_requeue,
                    unmodified_line_to_parse,
                )
        else:
            (
                did_complete_lrd,
                end_lrd_index,
                parsed_lrd_tuple,
            ) = LinkReferenceDefinitionHelper.__parse_link_reference_definition(
                parser_state,
                line_to_parse,
                start_index,
                extracted_whitespace,
                is_blank_line,
            )
            LOGGER.debug(
                ">>parse_link_reference_definition>>did_complete_lrd>>%s>>end_lrd_index>>%s>>len(line_to_parse)>>%s",
                str(did_complete_lrd),
                str(end_lrd_index),
                str(len(line_to_parse)),
            )
        if (
            end_lrd_index >= 0
            and end_lrd_index == len(line_to_parse)
            and not is_blank_line
        ):
            LOGGER.debug(">>parse_link_reference_definition>>continuation")
            LinkReferenceDefinitionHelper.__add_line_for_lrd_continuation(
                parser_state,
                position_marker,
                was_started,
                remaining_line_to_parse,
                extracted_whitespace,
                unmodified_line_to_parse,
                original_stack_depth,
                original_document_depth,
            )
            did_pause_lrd = True
        if (not did_pause_lrd and was_started) or did_complete_lrd:
            LOGGER.debug(">>parse_link_reference_definition>>was_started")
            (
                force_ignore_first_as_lrd,
                new_tokens,
            ) = LinkReferenceDefinitionHelper.__stop_lrd_continuation(
                parser_state,
                did_complete_lrd,
                parsed_lrd_tuple,
                end_lrd_index,
                remaining_line_to_parse,
                is_blank_line,
                lines_to_requeue,
            )
        else:
            LOGGER.debug(">>parse_link_reference_definition>>other")

        LOGGER.debug(">>XXXXXX>>requeue:%s:", str(lines_to_requeue))
        LOGGER.debug(">>XXXXXX>>did_complete_lrd:%s:", str(did_complete_lrd))
        if lines_to_requeue:

            # This works because in most cases, we add things.  However, in cases like
            # an indented code block, we process the "is it indented enough" and close
            # that block before hitting this.  As such, we have a special case to take
            # care of that.  In the future, will possibly want to do something instead of
            # original_document_depth and stack, such as passing in a copy of the both
            # elements so they can be reset on the rewind.
            # i.e. icode would go back on stack, end-icode would not be in document.
            LOGGER.debug(
                ">>XXXXXX>>copy_of_last_block_quote_markdown_token:%s:",
                ParserHelper.make_value_visible(
                    lrd_stack_token.copy_of_last_block_quote_markdown_token
                ),
            )
            if lrd_stack_token.copy_of_last_block_quote_markdown_token:
                LOGGER.debug(
                    ">>XXXXXX>>last_block_quote_markdown_token_index:%s:",
                    str(lrd_stack_token.last_block_quote_markdown_token_index),
                )
                LOGGER.debug(
                    ">>XXXXXX>>st-now:%s:",
                    ParserHelper.make_value_visible(
                        parser_state.token_document[
                            lrd_stack_token.last_block_quote_markdown_token_index
                        ]
                    ),
                )

                del parser_state.token_document[
                    lrd_stack_token.last_block_quote_markdown_token_index
                ]
                parser_state.token_document.insert(
                    lrd_stack_token.last_block_quote_markdown_token_index,
                    lrd_stack_token.copy_of_last_block_quote_markdown_token,
                )
                lrd_stack_token.last_block_quote_stack_token.reset_matching_markdown_token(
                    lrd_stack_token.copy_of_last_block_quote_markdown_token
                )

            LOGGER.debug(
                ">>XXXXXX>>original_stack_depth:%s:", str(original_stack_depth)
            )
            LOGGER.debug(
                ">>XXXXXX>>token_stack_depth:%s:", str(len(parser_state.token_stack))
            )
            while len(parser_state.token_stack) > original_stack_depth:
                del parser_state.token_stack[-1]

            LOGGER.debug(
                ">>XXXXXX>>original_document_depth:%s:", str(original_document_depth)
            )
            LOGGER.debug(
                ">>XXXXXX>>token_document_depth:%s:",
                str(len(parser_state.token_document)),
            )
            while len(parser_state.token_document) > original_document_depth:
                # if parser_state.token_document[-1].is_indented_code_block_end:
                #    break
                del parser_state.token_document[-1]

        if lines_to_requeue:
            requeue_line_info = RequeueLineInfo(
                lines_to_requeue, force_ignore_first_as_lrd
            )
        else:
            requeue_line_info = None
        return (
            did_complete_lrd or end_lrd_index != -1,
            did_complete_lrd,
            did_pause_lrd,
            requeue_line_info,
            new_tokens,
        )

    # pylint: enable=too-many-locals, too-many-arguments, too-many-statements, too-many-branches

    @staticmethod
    def __is_link_reference_definition(
        position_marker, line_to_parse, start_index, extracted_whitespace
    ):
        """
        Determine whether or not we have the start of a link reference definition.
        """

        if position_marker.token_stack[-1].is_paragraph:
            return False

        if (
            ParserHelper.is_length_less_than_or_equal_to(extracted_whitespace, 3)
        ) and ParserHelper.is_character_at_index_one_of(
            line_to_parse,
            start_index,
            LinkReferenceDefinitionHelper.__lrd_start_character,
        ):
            remaining_line = line_to_parse[start_index + 1 :]
            continue_with_lrd = True
            if (
                InlineHelper.backslash_character in remaining_line
                and remaining_line.endswith(InlineHelper.backslash_character)
            ):
                LOGGER.debug(">>%s<<%s", remaining_line, len(remaining_line))
                start_index = 0
                LOGGER.debug(">>%s<<%s", remaining_line, str(start_index))
                found_index = remaining_line.find(
                    InlineHelper.backslash_character, start_index
                )
                LOGGER.debug(">>%s<<", str(found_index))
                while found_index != -1 and found_index < (len(remaining_line) - 1):
                    start_index = found_index + 2
                    LOGGER.debug(">>%s<<%s", remaining_line, str(start_index))
                    found_index = remaining_line.find(
                        InlineHelper.backslash_character, start_index
                    )
                    LOGGER.debug(">>%s<<", str(found_index))
                LOGGER.debug(">>>>>>>%s<<", str(found_index))
                continue_with_lrd = found_index != len(remaining_line) - 1
            return continue_with_lrd
        return False

    @staticmethod
    def __verify_link_definition_end(line_to_parse, new_index):
        """
        Verify that the link reference definition's ends properly.
        """

        LOGGER.debug("look for EOL-ws>>%s<<", line_to_parse[new_index:])
        new_index, ex_ws = ParserHelper.extract_any_whitespace(line_to_parse, new_index)
        LOGGER.debug("look for EOL>>%s<<", line_to_parse[new_index:])
        if new_index < len(line_to_parse):
            LOGGER.debug(">> characters left at EOL, bailing")
            return False, -1, None
        return True, new_index, ex_ws

    # pylint: disable=too-many-locals
    @staticmethod
    def __parse_link_reference_definition(
        parser_state,
        line_to_parse,
        start_index,
        extracted_whitespace,
        is_blank_line,
    ):
        """
        Handle the parsing of what appears to be a link reference definition.
        """
        LOGGER.debug(
            "parse_link_reference_definition:%s:",
            ParserHelper.make_value_visible(line_to_parse),
        )
        LOGGER.debug("start_index:%s:", str(start_index))
        LOGGER.debug("start_index:%s:", str(extracted_whitespace))
        did_start = LinkReferenceDefinitionHelper.__is_link_reference_definition(
            parser_state, line_to_parse, start_index, extracted_whitespace
        )
        if not did_start:
            LOGGER.debug("BAIL")
            return False, -1, None

        LOGGER.debug("parse_link_reference_definition")
        inline_title = ""
        inline_link = None
        keep_going, new_index, collected_destination = LinkHelper.extract_link_label(
            line_to_parse, start_index + 1
        )
        line_destination_whitespace = ""
        inline_raw_link = ""
        if keep_going:
            (
                keep_going,
                new_index,
                inline_link,
                _,
                line_destination_whitespace,
                inline_raw_link,
            ) = LinkHelper.extract_link_destination(
                line_to_parse, new_index, is_blank_line
            )
        line_title_whitespace = ""
        inline_raw_title = ""
        if keep_going:
            (
                keep_going,
                new_index,
                inline_title,
                _,
                line_title_whitespace,
                inline_raw_title,
            ) = LinkHelper.extract_link_title(line_to_parse, new_index, is_blank_line)
        end_whitespace = ""
        if keep_going:
            (
                keep_going,
                new_index,
                end_whitespace,
            ) = LinkReferenceDefinitionHelper.__verify_link_definition_end(
                line_to_parse, new_index
            )
        normalized_destination = ""
        if keep_going:
            LOGGER.debug(
                ">>collected_destination(not normalized)>>%s",
                ParserHelper.make_value_visible(collected_destination),
            )
            normalized_destination = LinkHelper.normalize_link_label(
                collected_destination
            )
            if not normalized_destination:
                new_index = -1
                keep_going = False
        if not keep_going:
            return False, new_index, None

        assert new_index != -1

        LOGGER.debug(
            ">>collected_destination(normalized)>>%s",
            ParserHelper.make_value_visible(normalized_destination),
        )

        if not inline_title and line_title_whitespace.endswith(
            ParserHelper.newline_character
        ):
            line_title_whitespace = line_title_whitespace[0:-1]

        LOGGER.debug(
            ">>inline_link>>%s<<", ParserHelper.make_value_visible(inline_link)
        )
        LOGGER.debug(
            ">>inline_title>>%s<<", ParserHelper.make_value_visible(inline_title)
        )
        parsed_lrd_tuple = (
            normalized_destination,
            (inline_link, inline_title),
            (
                collected_destination,
                line_destination_whitespace,
                inline_raw_link,
                line_title_whitespace,
                inline_raw_title,
                end_whitespace,
            ),
        )
        return True, new_index, parsed_lrd_tuple

    # pylint: enable=too-many-locals

    # pylint: disable=too-many-arguments
    @staticmethod
    def __add_line_for_lrd_continuation(
        parser_state,
        position_marker,
        was_started,
        remaining_line_to_parse,
        extracted_whitespace,
        unmodified_line_to_parse,
        original_stack_depth,
        original_document_depth,
    ):
        """
        As part of processing a link reference definition, add a line to the continuation.
        """

        line_to_store = remaining_line_to_parse
        if was_started:
            LOGGER.debug(">>parse_link_reference_definition>>start already marked")
        else:
            LOGGER.debug(">>parse_link_reference_definition>>marking start")
            parser_state.token_stack.append(
                LinkDefinitionStackToken(extracted_whitespace, position_marker)
            )
            parser_state.token_stack[-1].original_stack_depth = original_stack_depth
            parser_state.token_stack[
                -1
            ].original_document_depth = original_document_depth
            parser_state.token_stack[
                -1
            ].last_block_quote_stack_token = parser_state.last_block_quote_stack_token
            parser_state.token_stack[
                -1
            ].last_block_quote_markdown_token_index = (
                parser_state.last_block_quote_markdown_token_index
            )
            parser_state.token_stack[
                -1
            ].copy_of_last_block_quote_markdown_token = (
                parser_state.copy_of_last_block_quote_markdown_token
            )
        LOGGER.debug(">>parse_link_reference_definition>>add>:%s<<", str(line_to_store))
        parser_state.token_stack[-1].add_continuation_line(line_to_store)
        parser_state.token_stack[-1].add_unmodified_line(unmodified_line_to_parse)

    # pylint: enable=too-many-arguments

    # pylint: disable=too-many-arguments
    @staticmethod
    def __stop_lrd_continuation(
        parser_state,
        did_complete_lrd,
        parsed_lrd_tuple,
        end_lrd_index,
        remaining_line_to_parse,
        is_blank_line,
        lines_to_requeue,
    ):
        """
        As part of processing a link reference definition, stop a continuation.
        """

        new_tokens = []
        LOGGER.debug(">>parse_link_reference_definition>>no longer need start")
        if did_complete_lrd:
            assert parsed_lrd_tuple
            did_add_definition = LinkHelper.add_link_definition(
                parsed_lrd_tuple[0], parsed_lrd_tuple[1]
            )
            assert not (end_lrd_index < -1 and remaining_line_to_parse)
            new_tokens = [
                LinkReferenceDefinitionMarkdownToken(
                    did_add_definition,
                    parser_state.token_stack[-1].extracted_whitespace,
                    parsed_lrd_tuple[0],
                    parsed_lrd_tuple[1],
                    parsed_lrd_tuple[2],
                    position_marker=parser_state.token_stack[-1].start_position_marker,
                )
            ]
            force_ignore_first_as_lrd = len(lines_to_requeue) > 1
        else:
            assert is_blank_line
            force_ignore_first_as_lrd = True
        del parser_state.token_stack[-1]
        return force_ignore_first_as_lrd, new_tokens

    # pylint: enable=too-many-arguments

    @staticmethod
    def __process_lrd_hard_failure(
        parser_state,
        remaining_line_to_parse,
        lines_to_requeue,
        unmodified_line_to_parse,
    ):
        """
        In cases of a hard failure, we have had continuations to the original line
        that make it a bit more difficult to figure out if we have an actual good
        LRD in the mix somehow.  So take lines off the end while we have lines.
        """
        is_blank_line = None
        line_to_parse = None
        did_complete_lrd = None
        end_lrd_index = None
        parsed_lrd_tuple = None

        do_again = True
        parser_state.token_stack[-1].add_continuation_line(remaining_line_to_parse)
        parser_state.token_stack[-1].add_unmodified_line(unmodified_line_to_parse)
        while do_again and parser_state.token_stack[-1].continuation_lines:
            LOGGER.debug(
                "continuation_lines>>%s<<",
                str(parser_state.token_stack[-1].continuation_lines),
            )

            lines_to_requeue.append(parser_state.token_stack[-1].unmodified_lines[-1])
            LOGGER.debug(
                ">>continuation_line>>%s",
                str(parser_state.token_stack[-1].continuation_lines[-1]),
            )
            LOGGER.debug(
                ">>unmodified_line>>%s",
                str(parser_state.token_stack[-1].unmodified_lines[-1]),
            )
            del parser_state.token_stack[-1].continuation_lines[-1]
            del parser_state.token_stack[-1].unmodified_lines[-1]
            LOGGER.debug(
                ">>lines_to_requeue>>%s>>%s",
                str(lines_to_requeue),
                str(len(lines_to_requeue)),
            )
            LOGGER.debug(
                ">>continuation_lines>>%s<<",
                str(parser_state.token_stack[-1].continuation_lines),
            )
            is_blank_line = True
            line_to_parse = parser_state.token_stack[-1].get_joined_lines("")
            line_to_parse = line_to_parse[0:-1]
            start_index, extracted_whitespace = ParserHelper.extract_whitespace(
                line_to_parse, 0
            )
            LOGGER.debug(
                ">>line_to_parse>>%s<<", ParserHelper.make_value_visible(line_to_parse)
            )
            (
                did_complete_lrd,
                end_lrd_index,
                parsed_lrd_tuple,
            ) = LinkReferenceDefinitionHelper.__parse_link_reference_definition(
                parser_state,
                line_to_parse,
                start_index,
                extracted_whitespace,
                is_blank_line,
            )
            LOGGER.debug(
                ">>parse_link_reference_definition>>was_started>>did_complete_lrd>>%s>>end_lrd_index>>%s>>len(line_to_parse)>>%s",
                str(did_complete_lrd),
                str(end_lrd_index),
                str(len(line_to_parse)),
            )
            do_again = not did_complete_lrd
        return (
            is_blank_line,
            line_to_parse,
            did_complete_lrd,
            end_lrd_index,
            parsed_lrd_tuple,
        )


# pylint: enable=too-few-public-methods
