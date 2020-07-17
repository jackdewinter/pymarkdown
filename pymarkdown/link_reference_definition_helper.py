"""
Link reference definition helper
"""
import logging

from pymarkdown.link_helper import LinkHelper
from pymarkdown.markdown_token import LinkReferenceDefinitionMarkdownToken
from pymarkdown.parser_helper import ParserHelper
from pymarkdown.stack_token import LinkDefinitionStackToken

LOGGER = logging.getLogger(__name__)


# pylint: disable=too-few-public-methods
class LinkReferenceDefinitionHelper:
    """
    Class to helper with the parsing of link reference definitions.
    """

    __lrd_start_character = "["

    @staticmethod
    def process_link_reference_definition(
        parser_state, position_marker, original_line_to_parse, extracted_whitespace,
    ):
        """
        Process a link deference definition.  Note, this requires a lot of work to
        handle properly because of partial definitions across lines.
        """
        line_to_parse = position_marker.text_to_parse
        start_index = position_marker.index_number

        did_pause_lrd = False
        lines_to_requeue = []
        new_tokens = []
        force_ignore_first_as_lrd = False

        was_started = False
        is_blank_line = not line_to_parse and not start_index
        if parser_state.token_stack[-1].was_link_definition_started:
            was_started = True
            LOGGER.debug(
                ">>continuation_lines>>%s<<",
                str(parser_state.token_stack[-1].continuation_lines),
            )
            line_to_parse = parser_state.token_stack[-1].get_joined_lines(line_to_parse)
            start_index, extracted_whitespace = ParserHelper.extract_whitespace(
                line_to_parse, 0
            )
            LOGGER.debug(">>line_to_parse>>%s<<", line_to_parse.replace("\n", "\\n"))

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
                    parser_state, original_line_to_parse, lines_to_requeue
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
            LinkReferenceDefinitionHelper.__add_line_for_lrd_continuation(
                parser_state,
                position_marker,
                was_started,
                original_line_to_parse,
                extracted_whitespace,
            )
            did_pause_lrd = True
        elif was_started:
            (
                force_ignore_first_as_lrd,
                new_tokens,
            ) = LinkReferenceDefinitionHelper.__stop_lrd_continuation(
                parser_state,
                did_complete_lrd,
                parsed_lrd_tuple,
                end_lrd_index,
                original_line_to_parse,
                is_blank_line,
            )
        else:
            LOGGER.debug(">>parse_link_reference_definition>>other")

        return (
            did_complete_lrd or end_lrd_index != -1,
            did_complete_lrd,
            did_pause_lrd,
            lines_to_requeue,
            force_ignore_first_as_lrd,
            new_tokens,
        )

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
            return True
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
        parser_state, line_to_parse, start_index, extracted_whitespace, is_blank_line,
    ):
        """
        Handle the parsing of what appears to be a link reference definition.
        """
        did_start = LinkReferenceDefinitionHelper.__is_link_reference_definition(
            parser_state, line_to_parse, start_index, extracted_whitespace
        )
        if not did_start:
            return False, -1, None

        LOGGER.debug("\nparse_link_reference_definition")
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
            normalized_destination = LinkHelper.normalize_link_label(
                collected_destination
            )
            if not normalized_destination:
                new_index = -1
                keep_going = False
        if not keep_going:
            return False, new_index, None

        assert new_index != -1

        if not inline_title and line_title_whitespace.endswith("\n"):
            line_title_whitespace = line_title_whitespace[0:-1]
        if end_whitespace and end_whitespace.endswith("\n"):
            end_whitespace = end_whitespace[0:-1]

        LOGGER.debug(
            ">>collected_destination(normalized)>>%s", str(normalized_destination)
        )
        LOGGER.debug(">>inline_link>>%s<<", str(inline_link))
        LOGGER.debug(">>inline_title>>%s<<", str(inline_title))
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

    @staticmethod
    def __add_line_for_lrd_continuation(
        parser_state,
        position_marker,
        was_started,
        original_line_to_parse,
        extracted_whitespace,
    ):
        """
        As part of processing a link reference definition, add a line to the continuation.
        """

        if was_started:
            LOGGER.debug(">>parse_link_reference_definition>>start already marked")
        else:
            LOGGER.debug(">>parse_link_reference_definition>>marking start")
            parser_state.token_stack.append(
                LinkDefinitionStackToken(extracted_whitespace, position_marker)
            )
        parser_state.token_stack[-1].add_continuation_line(original_line_to_parse)

    # pylint: disable=too-many-arguments
    @staticmethod
    def __stop_lrd_continuation(
        parser_state,
        did_complete_lrd,
        parsed_lrd_tuple,
        end_lrd_index,
        original_line_to_parse,
        is_blank_line,
    ):
        """
        As part of processing a link reference definition, stop a continuation.
        """

        force_ignore_first_as_lrd = False
        new_tokens = []
        LOGGER.debug(">>parse_link_reference_definition>>no longer need start")
        if did_complete_lrd:
            assert parsed_lrd_tuple
            did_add_definition = LinkHelper.add_link_definition(
                parsed_lrd_tuple[0], parsed_lrd_tuple[1]
            )
            assert not (end_lrd_index < -1 and original_line_to_parse)
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
        else:
            assert is_blank_line
            force_ignore_first_as_lrd = True
        del parser_state.token_stack[-1]
        return force_ignore_first_as_lrd, new_tokens

    # pylint: enable=too-many-arguments

    @staticmethod
    def __process_lrd_hard_failure(
        parser_state, original_line_to_parse, lines_to_requeue
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
        parser_state.token_stack[-1].add_continuation_line(original_line_to_parse)
        while do_again and parser_state.token_stack[-1].continuation_lines:
            LOGGER.debug(
                "continuation_lines>>%s<<",
                str(parser_state.token_stack[-1].continuation_lines),
            )

            lines_to_requeue.append(parser_state.token_stack[-1].continuation_lines[-1])
            LOGGER.debug(
                ">>continuation_line>>%s",
                str(parser_state.token_stack[-1].continuation_lines[-1]),
            )
            del parser_state.token_stack[-1].continuation_lines[-1]
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
            LOGGER.debug(">>line_to_parse>>%s<<", line_to_parse.replace("\n", "\\n"))
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
