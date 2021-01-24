"""
Inline processing
"""
import logging

from pymarkdown.emphasis_helper import EmphasisHelper
from pymarkdown.inline_helper import InlineHelper, InlineRequest, InlineResponse
from pymarkdown.inline_markdown_token import SpecialTextMarkdownToken, TextMarkdownToken
from pymarkdown.link_helper import LinkHelper
from pymarkdown.parser_helper import ParserHelper

LOGGER = logging.getLogger(__name__)

# pylint: disable=too-many-lines


# pylint: disable=too-few-public-methods
class InlineProcessor:
    """
    Handle the inline processing of the token stream.
    """

    __valid_inline_text_block_sequence_starts = ""
    __valid_inline_simple_text_block_sequence_starts = ""
    __inline_processing_needed = (
        EmphasisHelper.inline_emphasis
        + LinkHelper.link_label_start
        + LinkHelper.link_label_end
    )
    __inline_character_handlers = {}
    __inline_simple_character_handlers = {}

    """
    Class to provide helper functions for parsing html.
    """

    @staticmethod
    def initialize():
        """
        Initialize the inline processor subsystem.
        """
        InlineProcessor.__inline_character_handlers = {}
        InlineProcessor.__inline_simple_character_handlers = {}
        InlineProcessor.__valid_inline_text_block_sequence_starts = (
            ParserHelper.newline_character
        )
        InlineProcessor.__valid_inline_simple_text_block_sequence_starts = (
            ParserHelper.newline_character
        )

        InlineProcessor.register_handlers(
            InlineHelper.code_span_bounds, InlineHelper.handle_inline_backtick
        )
        InlineProcessor.register_handlers(
            InlineHelper.backslash_character,
            InlineHelper.handle_inline_backslash,
            is_simple_handler=True,
        )
        InlineProcessor.register_handlers(
            InlineHelper.character_reference_start_character,
            InlineHelper.handle_character_reference,
            is_simple_handler=True,
        )
        InlineProcessor.register_handlers(
            InlineHelper.angle_bracket_start, InlineHelper.handle_angle_brackets
        )
        for i in InlineProcessor.__inline_processing_needed:
            InlineProcessor.register_handlers(
                i, InlineProcessor.__handle_inline_special_single_character
            )
        InlineProcessor.register_handlers(
            LinkHelper.image_start_sequence[0],
            InlineProcessor.__handle_inline_image_link_start_character,
        )
        for i in ParserHelper.valid_characters_to_escape():
            InlineProcessor.register_handlers(
                i, InlineProcessor.__handle_inline_control_character
            )

    @staticmethod
    def __handle_inline_control_character(inline_request):
        inline_response = InlineResponse()
        inline_response.new_index = inline_request.next_index + 1
        inline_response.new_string = (
            ParserHelper.escape_character
            + inline_request.source_text[inline_request.next_index]
        )
        inline_response.delta_column_number = 1
        return inline_response

    @staticmethod
    def register_handlers(
        inline_character, start_token_handler, is_simple_handler=False
    ):
        """
        Register the handlers necessary to deal with token's start and end.
        """
        InlineProcessor.__inline_character_handlers[
            inline_character
        ] = start_token_handler
        InlineProcessor.__valid_inline_text_block_sequence_starts += inline_character
        if is_simple_handler:
            InlineProcessor.__inline_simple_character_handlers[
                inline_character
            ] = start_token_handler
            InlineProcessor.__valid_inline_simple_text_block_sequence_starts += (
                inline_character
            )

    @staticmethod
    # pylint: disable=too-many-branches, too-many-statements, too-many-nested-blocks
    def parse_inline(coalesced_results):
        """
        Parse and resolve any inline elements.
        """
        LOGGER.info("coalesced_results")
        LOGGER.info("-----")
        for next_token in coalesced_results:
            LOGGER.info(">>%s<<", ParserHelper.make_value_visible(next_token))
        LOGGER.info("-----")

        coalesced_stack = []

        coalesced_list = []
        coalesced_list.extend(coalesced_results[0:1])

        current_token = coalesced_results[0]
        LOGGER.debug("STACK?:%s", ParserHelper.make_value_visible(current_token))
        if current_token.is_container:
            LOGGER.debug("STACK:%s", ParserHelper.make_value_visible(coalesced_stack))
            coalesced_stack.append(current_token)
            LOGGER.debug("STACK-ADD:%s", ParserHelper.make_value_visible(current_token))
            LOGGER.debug("STACK:%s", ParserHelper.make_value_visible(coalesced_stack))

        for coalesce_index in range(1, len(coalesced_results)):
            if coalesced_results[coalesce_index].is_text and (
                coalesced_list[-1].is_paragraph
                or coalesced_list[-1].is_setext_heading
                or coalesced_list[-1].is_atx_heading
                or coalesced_list[-1].is_code_block
            ):
                LOGGER.info("coalesced_results:%s<", str(coalesced_list[-1]))
                if coalesced_list[-1].is_code_block:
                    encoded_text = InlineHelper.append_text(
                        "", coalesced_results[coalesce_index].token_text
                    )
                    line_number_delta = 0
                    new_column_number = coalesced_list[-1].column_number
                    if coalesced_list[-1].is_fenced_code_block:
                        line_number_delta = 1
                        new_column_number = 1

                        if coalesced_stack:
                            LOGGER.debug(
                                "COAL_STACK:%s",
                                ParserHelper.make_value_visible(coalesced_stack[-1]),
                            )
                            assert coalesced_stack[-1].leading_spaces
                            split_leading_spaces = coalesced_stack[
                                -1
                            ].leading_spaces.split(ParserHelper.newline_character)
                            LOGGER.debug(
                                "COAL_STACK:%s",
                                ParserHelper.make_value_visible(split_leading_spaces),
                            )
                            assert len(split_leading_spaces) >= 2
                            LOGGER.info(
                                "coalesced_stack:%s<",
                                ParserHelper.make_value_visible(split_leading_spaces),
                            )
                            new_column_number += len(split_leading_spaces[1])
                        else:
                            leading_whitespace = coalesced_results[
                                coalesce_index
                            ].extracted_whitespace
                            LOGGER.debug(
                                ">>%s<<",
                                ParserHelper.make_value_visible(
                                    coalesced_results[coalesce_index]
                                ),
                            )
                            assert (
                                ParserHelper.newline_character not in leading_whitespace
                            )
                            LOGGER.info(
                                "leading_whitespace:%s<",
                                ParserHelper.make_value_visible(leading_whitespace),
                            )
                            leading_whitespace = (
                                ParserHelper.resolve_replacement_markers_from_text(
                                    leading_whitespace
                                )
                            )
                            LOGGER.info(
                                "leading_whitespace:%s<",
                                ParserHelper.make_value_visible(leading_whitespace),
                            )
                            new_column_number += len(leading_whitespace)
                    processed_tokens = [
                        TextMarkdownToken(
                            encoded_text,
                            coalesced_results[coalesce_index].extracted_whitespace,
                            line_number=coalesced_list[-1].line_number
                            + line_number_delta,
                            column_number=new_column_number,
                        )
                    ]
                    LOGGER.debug(
                        "new Text>>%s>>",
                        ParserHelper.make_value_visible(processed_tokens),
                    )
                elif coalesced_list[-1].is_setext_heading:
                    combined_text = coalesced_results[coalesce_index].token_text
                    combined_whitespace_text = coalesced_results[
                        coalesce_index
                    ].extracted_whitespace.replace(ParserHelper.tab_character, "    ")
                    LOGGER.debug(
                        "combined_text>>%s",
                        ParserHelper.make_value_visible(combined_text),
                    )
                    LOGGER.debug(
                        "combined_whitespace_text>>%s",
                        ParserHelper.make_value_visible(combined_whitespace_text),
                    )
                    processed_tokens = InlineProcessor.__process_inline_text_block(
                        coalesced_results[coalesce_index].token_text.replace(
                            ParserHelper.tab_character, "    "
                        ),
                        whitespace_to_recombine=combined_whitespace_text,
                        is_setext=True,
                        para_space=coalesced_results[
                            coalesce_index
                        ].extracted_whitespace,
                        line_number=coalesced_results[coalesce_index].line_number,
                        column_number=coalesced_results[coalesce_index].column_number,
                    )
                    LOGGER.debug(
                        "processed_tokens>>%s",
                        ParserHelper.make_value_visible(processed_tokens),
                    )
                elif coalesced_list[-1].is_atx_heading:
                    LOGGER.debug(
                        "atx-block>>%s<<",
                        ParserHelper.make_value_visible(
                            coalesced_results[coalesce_index]
                        ),
                    )
                    LOGGER.debug(
                        "atx-block-text>>%s<<",
                        ParserHelper.make_value_visible(
                            coalesced_results[coalesce_index].token_text
                        ),
                    )
                    LOGGER.debug(
                        "atx-block-ws>>%s<<",
                        ParserHelper.make_value_visible(
                            coalesced_results[coalesce_index].extracted_whitespace
                        ),
                    )
                    processed_tokens = InlineProcessor.__process_inline_text_block(
                        coalesced_results[coalesce_index].token_text.replace(
                            ParserHelper.tab_character, "    "
                        ),
                        coalesced_results[coalesce_index].extracted_whitespace.replace(
                            ParserHelper.tab_character, "    "
                        ),
                        line_number=coalesced_results[coalesce_index].line_number,
                        column_number=coalesced_results[coalesce_index].column_number
                        + len(coalesced_results[coalesce_index].extracted_whitespace)
                        + coalesced_list[-1].hash_count,
                    )
                else:
                    assert coalesced_list[-1].is_paragraph
                    LOGGER.debug(
                        ">>before_add_ws>>%s>>add>>%s>>",
                        ParserHelper.make_value_visible(coalesced_list[-1]),
                        ParserHelper.make_value_visible(
                            coalesced_results[coalesce_index].extracted_whitespace
                        ),
                    )
                    coalesced_list[-1].add_whitespace(
                        coalesced_results[coalesce_index].extracted_whitespace.replace(
                            ParserHelper.tab_character, "    "
                        )
                    )
                    LOGGER.debug(
                        ">>after_add_ws>>%s",
                        ParserHelper.make_value_visible(coalesced_list[-1]),
                    )
                    processed_tokens = InlineProcessor.__process_inline_text_block(
                        coalesced_results[coalesce_index].token_text.replace(
                            ParserHelper.tab_character, "    "
                        ),
                        is_para=True,
                        para_space=coalesced_results[
                            coalesce_index
                        ].extracted_whitespace,
                        line_number=coalesced_results[coalesce_index].line_number,
                        column_number=coalesced_results[coalesce_index].column_number,
                        para_owner=coalesced_list[-1],
                    )
                coalesced_list.extend(processed_tokens)
            else:
                coalesced_list.append(coalesced_results[coalesce_index])

            current_token = coalesced_results[coalesce_index]
            LOGGER.debug("STACK?:%s", ParserHelper.make_value_visible(current_token))
            if current_token.is_container and not current_token.is_new_list_item:
                LOGGER.debug(
                    "STACK:%s", ParserHelper.make_value_visible(coalesced_stack)
                )
                coalesced_stack.append(current_token)
                LOGGER.debug(
                    "STACK-ADD:%s", ParserHelper.make_value_visible(current_token)
                )
                LOGGER.debug(
                    "STACK:%s", ParserHelper.make_value_visible(coalesced_stack)
                )

            elif current_token.is_list_end or current_token.is_block_quote_end:
                LOGGER.debug(
                    "STACK:%s", ParserHelper.make_value_visible(coalesced_stack)
                )
                del coalesced_stack[-1]
                LOGGER.debug(
                    "STACK-REMOVE:%s",
                    ParserHelper.make_value_visible(current_token),
                )
                LOGGER.debug(
                    "STACK:%s", ParserHelper.make_value_visible(coalesced_stack)
                )
        return coalesced_list

    # pylint: enable=too-many-branches, too-many-statements, too-many-nested-blocks

    @staticmethod
    def __handle_inline_special_single_character(inline_request):
        return InlineProcessor.__handle_inline_special(
            inline_request.source_text,
            inline_request.next_index,
            inline_request.inline_blocks,
            1,
            inline_request.remaining_line,
            inline_request.current_string_unresolved,
            inline_request.line_number,
            inline_request.column_number,
            inline_request.para_owner,
        )

    @staticmethod
    def __handle_inline_image_link_start_character(inline_request):
        if ParserHelper.are_characters_at_index(
            inline_request.source_text,
            inline_request.next_index,
            LinkHelper.image_start_sequence,
        ):
            inline_response = InlineProcessor.__handle_inline_special(
                inline_request.source_text,
                inline_request.next_index,
                inline_request.inline_blocks,
                2,
                inline_request.remaining_line,
                inline_request.current_string_unresolved,
                inline_request.line_number,
                inline_request.column_number,
                inline_request.para_owner,
            )
            assert not inline_response.consume_rest_of_line
        else:
            inline_response = InlineResponse()
            inline_response.new_string = LinkHelper.image_start_sequence[0]
            inline_response.new_index = inline_request.next_index + 1
            inline_response.delta_column_number = 1
        return inline_response

    # pylint: disable=too-many-arguments, too-many-locals, too-many-statements, too-many-branches, too-many-nested-blocks
    @staticmethod
    def __handle_inline_special(
        source_text,
        next_index,
        inline_blocks,
        special_length,
        remaining_line,
        current_string_unresolved,
        line_number,
        column_number,
        para_owner,
    ):
        """
        Handle the collection of special inline characters for later processing.
        """
        preceding_two = None
        following_two = None
        new_token = None
        repeat_count = 1
        is_active = True

        delta_line = 0

        consume_rest_of_line = False
        LOGGER.debug(">>column_number>>%s<<", str(column_number))
        LOGGER.debug(
            ">>remaining_line>>%s<<", ParserHelper.make_value_visible(remaining_line)
        )
        column_number += len(remaining_line)
        LOGGER.debug(">>column_number>>%s<<", str(column_number))
        special_sequence = source_text[next_index : next_index + special_length]
        if special_length == 1 and special_sequence in EmphasisHelper.inline_emphasis:
            repeat_count, new_index = ParserHelper.collect_while_character(
                source_text, next_index, special_sequence
            )
            special_sequence = source_text[next_index:new_index]

            preceding_two = source_text[max(0, next_index - 2) : next_index]
            following_two = source_text[
                new_index : min(len(source_text), new_index + 2)
            ]
        else:
            if special_sequence[0] == LinkHelper.link_label_end:
                LOGGER.debug(
                    "POSSIBLE LINK CLOSE_FOUND(%s)>>%s>>",
                    str(special_length),
                    special_sequence,
                )
                LOGGER.debug(
                    ">>inline_blocks>>%s<<",
                    ParserHelper.make_value_visible(inline_blocks),
                )
                LOGGER.debug(
                    ">>remaining_line>>%s<<",
                    ParserHelper.make_value_visible(remaining_line),
                )
                LOGGER.debug(
                    ">>current_string_unresolved>>%s<<",
                    ParserHelper.make_value_visible(current_string_unresolved),
                )
                LOGGER.debug(
                    ">>source_text>>%s<<",
                    ParserHelper.make_value_visible(source_text[next_index:]),
                )
                LOGGER.debug("")
                old_inline_blocks_count = len(inline_blocks)
                old_inline_blocks_last_token = None
                if inline_blocks:
                    old_inline_blocks_last_token = inline_blocks[-1]
                (
                    new_index,
                    is_active,
                    new_token,
                    consume_rest_of_line,
                ) = LinkHelper.look_for_link_or_image(
                    inline_blocks,
                    source_text,
                    next_index,
                    remaining_line,
                    current_string_unresolved,
                    InlineProcessor.__process_simple_inline_fn,
                )
                LOGGER.debug(">>next_index>>%s<<", str(next_index))
                LOGGER.debug(">>new_index>>%s<<", str(new_index))
                LOGGER.debug(
                    ">>inline_blocks>>%s<<",
                    ParserHelper.make_value_visible(inline_blocks),
                )
                LOGGER.debug(
                    ">>new_token>>%s<<", ParserHelper.make_value_visible(new_token)
                )
                LOGGER.debug(
                    ">>source_text>>%s<<",
                    ParserHelper.make_value_visible(source_text[new_index:]),
                )
                LOGGER.debug(">>consume_rest_of_line>>%s<<", str(consume_rest_of_line))
                LOGGER.debug(
                    ">>old_inline_blocks_count>>%s<<", str(old_inline_blocks_count)
                )
                LOGGER.debug(">>len(inline_blocks)>>%s<<", str(len(inline_blocks)))

                if (
                    new_token
                    or old_inline_blocks_count != len(inline_blocks)
                    or (
                        inline_blocks
                        and old_inline_blocks_last_token != inline_blocks[-1]
                    )
                ):
                    if inline_blocks[-1].is_inline_image:
                        repeat_count = (new_index - next_index) + len(remaining_line)
                        (
                            delta_line,
                            repeat_count,
                        ) = InlineProcessor.__calculate_link_and_image_deltas(
                            para_owner, inline_blocks[-1], delta_line, repeat_count
                        )
                        LOGGER.debug(">>delta_line>>%s<<", str(delta_line))
                        LOGGER.debug(">>repeat_count>>%s<<", str(repeat_count))
                    elif new_token and new_token.is_inline_link_end:
                        LOGGER.debug(
                            ">>new_token.start_markdown_token>>%s<<",
                            ParserHelper.make_value_visible(
                                new_token.start_markdown_token
                            ),
                        )
                        assert new_token.start_markdown_token
                        repeat_count = new_index - next_index
                        LOGGER.debug(">>delta_line>>%s<<", str(delta_line))
                        LOGGER.debug(">>repeat_count>>%s<<", str(repeat_count))
                        (
                            delta_line,
                            repeat_count,
                        ) = InlineProcessor.__calculate_link_and_image_deltas(
                            para_owner,
                            new_token.start_markdown_token,
                            delta_line,
                            repeat_count,
                        )
                        LOGGER.debug(">>delta_line>>%s<<", str(delta_line))
                        LOGGER.debug(">>repeat_count>>%s<<", str(repeat_count))
                    else:
                        repeat_count = new_index - next_index
                        LOGGER.debug(">>repeat_count>>%s<<", str(repeat_count))
            else:
                repeat_count = special_length
                new_index = next_index + special_length

        if not new_token:
            LOGGER.debug(">>create>>%s,%s<<", str(line_number), str(column_number))
            new_token = SpecialTextMarkdownToken(
                special_sequence,
                repeat_count,
                preceding_two,
                following_two,
                is_active,
                line_number,
                column_number,
            )

        LOGGER.debug(">>delta_line>>%s<<", str(delta_line))
        LOGGER.debug(">>repeat_count>>%s<<", str(repeat_count))
        inline_response = InlineResponse()
        inline_response.new_string = ""
        inline_response.new_index = new_index
        inline_response.new_tokens = [new_token]
        inline_response.consume_rest_of_line = consume_rest_of_line
        inline_response.delta_line_number = delta_line
        inline_response.delta_column_number = repeat_count
        return inline_response

    # pylint: enable=too-many-arguments, too-many-locals, too-many-statements, too-many-branches, too-many-nested-blocks

    @staticmethod
    def __process_simple_inline_fn(source_text):
        """
        Handle a simple processing of inline text for simple replacements.
        """

        LOGGER.debug(">>source_text>>%s", ParserHelper.make_value_visible(source_text))
        start_index = 0
        processed_line = ""
        LOGGER.debug(
            ">>__valid_inline_simple_text_block_sequence_starts>>%s",
            ParserHelper.make_value_visible(
                InlineProcessor.__valid_inline_simple_text_block_sequence_starts
            ),
        )
        next_index = ParserHelper.index_any_of(
            source_text,
            InlineProcessor.__valid_inline_simple_text_block_sequence_starts,
            start_index,
        )
        LOGGER.debug(">>next_index>>%s", str(next_index))
        while next_index != -1:
            processed_line += source_text[start_index:next_index]
            inline_request = InlineRequest(source_text, next_index)
            if source_text[next_index] in InlineProcessor.__inline_character_handlers:
                LOGGER.debug(
                    "handler(before)>>%s<<",
                    ParserHelper.make_value_visible(source_text[next_index]),
                )
                LOGGER.debug(
                    "current_string_unresolved>>%s<<",
                    ParserHelper.make_value_visible(processed_line),
                )
                proc_fn = InlineProcessor.__inline_character_handlers[
                    source_text[next_index]
                ]
                inline_response = proc_fn(inline_request)
                processed_line += inline_response.new_string
                LOGGER.debug(
                    "handler(after)>>%s<<",
                    ParserHelper.make_value_visible(source_text[next_index]),
                )
                LOGGER.debug(
                    "delta_line_number>>%s<<", str(inline_response.delta_line_number)
                )
                LOGGER.debug(
                    "delta_column>>%s<<", str(inline_response.delta_column_number)
                )
                start_index = inline_response.new_index
            else:
                processed_line += ParserHelper.newline_character
                start_index = next_index + 1
            next_index = ParserHelper.index_any_of(
                source_text,
                InlineProcessor.__valid_inline_simple_text_block_sequence_starts,
                start_index,
            )

        processed_line += source_text[start_index:]
        LOGGER.debug("processed_line>>%s<<", str(processed_line))
        return processed_line

    @staticmethod
    def __calculate_full_deltas(current_token, para_owner, delta_line, repeat_count):
        newline_count = ParserHelper.count_newlines_in_text(
            current_token.text_from_blocks
        )
        if newline_count:
            LOGGER.debug(">>text_from_blocks")
        newline_count = ParserHelper.count_newlines_in_text(current_token.ex_label)
        if newline_count:
            LOGGER.debug(">>ex_label")
            delta_line += newline_count
            if para_owner:
                para_owner.rehydrate_index += newline_count
            LOGGER.debug("full>>ex_label>>newline_count>>%s", str(newline_count))

            split_label = current_token.ex_label.split(ParserHelper.newline_character)
            LOGGER.debug(
                "full>>ex_label>>split_label>>%s",
                ParserHelper.make_value_visible(split_label),
            )

            split_label = split_label[-1]
            LOGGER.debug(
                "full>>ex_label>>split_label>>%s",
                ParserHelper.make_value_visible(split_label),
            )
            repeat_count = -(len(split_label) + 1 + 1)
        return delta_line, repeat_count

    # pylint: disable=too-many-arguments, too-many-branches, too-many-statements
    @staticmethod
    def __calculate_inline_deltas(
        current_token,
        active_link_uri,
        active_link_title,
        para_owner,
        split_paragraph_lines,
        delta_line,
        repeat_count,
    ):
        last_spaces = ""

        link_part_lengths = [0] * 5
        link_part_lengths[0] = len(active_link_uri) + len(
            current_token.before_title_whitespace
        )
        if current_token.inline_title_bounding_character:
            link_part_lengths[1] = 1
            link_part_lengths[2] = len(active_link_title) + 1
            link_part_lengths[3] = len(current_token.after_title_whitespace)
        link_part_lengths[4] = 0

        LOGGER.debug(">>link_part_lengths>>%s<<", str(link_part_lengths))

        link_part_index = -2
        newline_count = ParserHelper.count_newlines_in_text(
            current_token.text_from_blocks
        )
        if newline_count:
            link_part_index = -1
            if para_owner:
                para_owner.rehydrate_index += newline_count
        newline_count = ParserHelper.count_newlines_in_text(
            current_token.before_link_whitespace
        )
        if newline_count:
            LOGGER.debug(">>before_link_whitespace")
            delta_line += newline_count
            if para_owner:
                para_owner.rehydrate_index += newline_count
            last_spaces = current_token.before_link_whitespace[:]

            link_part_index = 0
        newline_count = ParserHelper.count_newlines_in_text(
            current_token.before_title_whitespace
        )
        if newline_count:
            LOGGER.debug(">>before_title_whitespace")
            delta_line += newline_count
            if para_owner:
                para_owner.rehydrate_index += newline_count
            last_spaces = current_token.before_title_whitespace[:]

            link_part_index = 1
        newline_count = ParserHelper.count_newlines_in_text(active_link_title)
        if newline_count:
            LOGGER.debug(">>active_link_title")
            delta_line += newline_count
            if para_owner:
                para_owner.rehydrate_index += newline_count
            last_spaces = ""

            split_active_link_title = active_link_title.split(
                ParserHelper.newline_character
            )
            link_part_lengths[2] = len(split_active_link_title[-1]) + 1
            link_part_index = 2
        newline_count = ParserHelper.count_newlines_in_text(
            current_token.after_title_whitespace
        )
        if newline_count:
            LOGGER.debug(">>after_title_whitespace")
            delta_line += newline_count
            if para_owner:
                para_owner.rehydrate_index += newline_count
            last_spaces = current_token.after_title_whitespace[:]

            link_part_index = 4

        LOGGER.debug(">>link_part_index>>%s<<", str(link_part_index))
        LOGGER.debug(">>delta_line>>%s<<", str(delta_line))

        if link_part_index >= 0:
            if split_paragraph_lines:
                link_part_lengths[4] = len(
                    split_paragraph_lines[para_owner.rehydrate_index]
                )
            else:
                split_last_spaces = last_spaces.split(ParserHelper.newline_character)
                link_part_lengths[4] = len(split_last_spaces[-1])
            link_part_lengths[:link_part_index] = [0] * link_part_index
            repeat_count = -(2 + sum(link_part_lengths))
            LOGGER.debug(">>link_part_lengths>>%s<<", str(link_part_lengths))
            LOGGER.debug(">>repeat_count>>%s<<", str(delta_line))
        return delta_line, repeat_count

    # pylint: enable=too-many-arguments, too-many-branches, too-many-statements

    @staticmethod
    def __calculate_shortcut_collapsed_deltas(current_token, delta_line, repeat_count):
        newline_count = ParserHelper.count_newlines_in_text(
            current_token.text_from_blocks
        )
        if newline_count:
            LOGGER.debug(">>text_from_blocks")
        return delta_line, repeat_count

    @staticmethod
    def __calculate_link_and_image_deltas(
        para_owner, current_token, delta_line, repeat_count
    ):
        LOGGER.debug(">>delta_line>>%s<<", str(delta_line))
        LOGGER.debug(">>repeat_count>>%s<<", str(repeat_count))
        if current_token.is_inline_image:
            active_link_uri = current_token.image_uri
            if current_token.pre_image_uri:
                active_link_uri = current_token.pre_image_uri
            active_link_title = current_token.image_title
            if current_token.pre_image_title:
                active_link_title = current_token.pre_image_title
        else:
            active_link_uri = current_token.link_uri
            if current_token.pre_link_uri:
                active_link_uri = current_token.pre_link_uri

            active_link_title = current_token.link_title
            if current_token.pre_link_title:
                active_link_title = current_token.pre_link_title

        if ParserHelper.newline_character in str(current_token):
            LOGGER.debug(
                ">>para_owner>>%s<<",
                ParserHelper.make_value_visible(para_owner),
            )
            split_paragraph_lines = None
            if para_owner:
                LOGGER.debug(
                    ">>para_owner.rehydrate_index>>%s<<",
                    ParserHelper.make_value_visible(para_owner.rehydrate_index),
                )
                split_paragraph_lines = para_owner.extracted_whitespace.split(
                    ParserHelper.newline_character
                )
                LOGGER.debug(
                    ">>split_paragraph_lines>>%s<<",
                    ParserHelper.make_value_visible(split_paragraph_lines),
                )

            if current_token.label_type == "inline":
                delta_line, repeat_count = InlineProcessor.__calculate_inline_deltas(
                    current_token,
                    active_link_uri,
                    active_link_title,
                    para_owner,
                    split_paragraph_lines,
                    delta_line,
                    repeat_count,
                )
            elif current_token.label_type == "full":
                delta_line, repeat_count = InlineProcessor.__calculate_full_deltas(
                    current_token, para_owner, delta_line, repeat_count
                )
            else:
                assert (
                    current_token.label_type == "shortcut"
                    or current_token.label_type == "collapsed"
                ), ("Label type '" + current_token.label_type + "' not handled.")
                (
                    delta_line,
                    repeat_count,
                ) = InlineProcessor.__calculate_shortcut_collapsed_deltas(
                    current_token, delta_line, repeat_count
                )

        LOGGER.debug(
            ">>delta_line>>%s<<repeat_count>>%s<<", str(delta_line), str(repeat_count)
        )
        return delta_line, repeat_count

    @staticmethod
    def __recombine_with_whitespace(source_text, whitespace_to_recombine):
        split_source_text = source_text.split(ParserHelper.newline_character)
        split_whitespace_to_recombine = whitespace_to_recombine.split(
            ParserHelper.newline_character
        )
        assert len(split_source_text) == len(split_whitespace_to_recombine)
        recombined_text = None
        for split_index, next_split_source in enumerate(split_source_text):
            if recombined_text is None:
                recombined_text = next_split_source
            else:
                recombined_text += (
                    ParserHelper.newline_character
                    + split_whitespace_to_recombine[split_index]
                    + next_split_source
                )
        return recombined_text

    @staticmethod  # noqa: C901
    # pylint: disable=too-many-statements, too-many-locals, too-many-arguments, too-many-branches
    def __process_inline_text_block(
        source_text,
        starting_whitespace="",
        whitespace_to_recombine=None,
        is_setext=False,
        is_para=False,
        para_space=None,
        line_number=0,
        column_number=0,
        para_owner=None,
    ):
        """
        Process a text block for any inline items.
        """

        inline_blocks = []
        start_index = 0
        LOGGER.debug(
            "__process_inline_text_block>>source_text>>%s>",
            ParserHelper.make_value_visible(source_text),
        )
        LOGGER.debug(
            "__process_inline_text_block>>starting_whitespace>>%s>",
            ParserHelper.make_value_visible(starting_whitespace),
        )
        LOGGER.debug(
            "__process_inline_text_block>>whitespace_to_recombine>>%s>",
            ParserHelper.make_value_visible(whitespace_to_recombine),
        )
        LOGGER.debug(
            "__process_inline_text_block>>line_number>>%s>",
            ParserHelper.make_value_visible(line_number),
        )
        LOGGER.debug(
            "__process_inline_text_block>>column_number>>%s>",
            ParserHelper.make_value_visible(column_number),
        )
        if whitespace_to_recombine and " " in whitespace_to_recombine:
            source_text = InlineProcessor.__recombine_with_whitespace(
                source_text, whitespace_to_recombine
            )
        else:
            whitespace_to_recombine = None
        LOGGER.debug(
            "__process_inline_text_block>>source_text>>%s",
            ParserHelper.make_value_visible(source_text),
        )

        last_line_number = line_number
        last_column_number = column_number
        LOGGER.debug(
            ">>Token_start>>%s,%s<<",
            str(last_line_number),
            str(last_column_number),
        )

        current_string = ""
        current_string_unresolved = ""
        end_string = ""
        LOGGER.debug("1<<end_string<<%s<<", ParserHelper.make_value_visible(end_string))

        inline_response = InlineResponse()
        fold_space = None
        LOGGER.debug("__process_inline_text_block>>is_para>>%s", str(is_para))
        if is_para or is_setext:
            fold_space = para_space.split(ParserHelper.newline_character)
        LOGGER.debug("__process_inline_text_block>>fold_space>>%s", str(fold_space))

        LOGGER.debug(
            "starts>%s<",
            ParserHelper.make_value_visible(
                InlineProcessor.__valid_inline_text_block_sequence_starts
            ),
        )
        LOGGER.debug(
            "look>%s<", ParserHelper.make_value_visible(source_text[start_index:])
        )
        next_index = ParserHelper.index_any_of(
            source_text,
            InlineProcessor.__valid_inline_text_block_sequence_starts,
            start_index,
        )
        LOGGER.debug("__process_inline_text_block>>is_setext>>%s", str(is_setext))
        LOGGER.debug(
            "__process_inline_text_block>>%s>>%s",
            ParserHelper.make_value_visible(source_text),
            str(start_index),
        )
        while next_index != -1:

            LOGGER.debug(
                "\n\n>>Token_start>>%s,%s<<",
                str(last_line_number),
                str(last_column_number),
            )
            LOGGER.debug(
                ">>inline_blocks>>%s<<", ParserHelper.make_value_visible(inline_blocks)
            )
            LOGGER.debug(
                ">>current_string>>%s<<",
                ParserHelper.make_value_visible(current_string),
            )
            LOGGER.debug(
                ">>current_string_unresolved>>%s<<",
                ParserHelper.make_value_visible(current_string_unresolved),
            )
            LOGGER.debug(
                ">>current_string_unresolved>>%s<<",
                ParserHelper.make_value_visible(current_string_unresolved),
            )
            LOGGER.debug(
                ">>end_string>>%s<<",
                ParserHelper.make_value_visible(end_string),
            )
            LOGGER.debug(
                ">>source_text[]>>%s<<%s<<",
                ParserHelper.make_value_visible(source_text[next_index]),
                ParserHelper.make_value_visible(source_text[next_index:]),
            )

            inline_response.clear_fields()
            reset_current_string = False
            whitespace_to_add = None

            was_new_line = False
            was_column_number_reset = False

            LOGGER.debug(
                "__process_inline_text_block>>%s>>%s", str(start_index), str(next_index)
            )
            remaining_line = source_text[start_index:next_index]

            old_inline_blocks_count = len(inline_blocks)
            old_inline_blocks_last_token = None
            if inline_blocks:
                old_inline_blocks_last_token = inline_blocks[-1]

            inline_request = InlineRequest(
                source_text,
                next_index,
                inline_blocks,
                remaining_line,
                current_string_unresolved,
                line_number,
                column_number,
                para_owner,
            )
            if source_text[next_index] in InlineProcessor.__inline_character_handlers:
                LOGGER.debug(
                    "handler(before)>>%s<<",
                    ParserHelper.make_value_visible(source_text[next_index]),
                )
                LOGGER.debug(
                    "current_string_unresolved>>%s<<",
                    ParserHelper.make_value_visible(current_string_unresolved),
                )
                LOGGER.debug("remaining_line>>%s<<", str(remaining_line))
                LOGGER.debug("line_number>>%s<<", str(line_number))
                LOGGER.debug("column_number>>%s<<", str(column_number))
                proc_fn = InlineProcessor.__inline_character_handlers[
                    source_text[next_index]
                ]
                inline_response = proc_fn(inline_request)
                LOGGER.debug(
                    "handler(after)>>%s<<",
                    ParserHelper.make_value_visible(source_text[next_index]),
                )
                LOGGER.debug(
                    "delta_line_number>>%s<<", str(inline_response.delta_line_number)
                )
                LOGGER.debug(
                    "delta_column>>%s<<", str(inline_response.delta_column_number)
                )

                line_number += inline_response.delta_line_number
                if inline_response.delta_column_number < 0:
                    column_number = -inline_response.delta_column_number
                    was_column_number_reset = True
                else:
                    column_number += inline_response.delta_column_number
                LOGGER.debug(
                    "handler(after)>>%s,%s<<", str(line_number), str(column_number)
                )
                LOGGER.debug(
                    "handler(after)>>new_tokens>>%s<<",
                    ParserHelper.make_value_visible(inline_response.new_tokens),
                )
            else:
                assert source_text[next_index] == ParserHelper.newline_character
                LOGGER.debug(
                    "end_string(before)>>%s<<",
                    ParserHelper.make_value_visible(end_string),
                )
                (
                    inline_response.new_string,
                    whitespace_to_add,
                    inline_response.new_index,
                    inline_response.new_tokens,
                    remaining_line,
                    end_string,
                    current_string,
                ) = InlineHelper.handle_line_end(
                    next_index,
                    remaining_line,
                    end_string,
                    current_string,
                    line_number,
                    column_number,
                )
                LOGGER.debug(
                    "2<<end_string<<%s<<", ParserHelper.make_value_visible(end_string)
                )
                LOGGER.debug(
                    "handle_line_end>>new_tokens>>%s<<",
                    ParserHelper.make_value_visible(inline_response.new_tokens),
                )
                if not inline_response.new_tokens:
                    LOGGER.debug("ws")
                    end_string = InlineProcessor.__add_recombined_whitespace(
                        bool(whitespace_to_recombine),
                        source_text,
                        inline_response,
                        end_string,
                        is_setext,
                    )
                    LOGGER.debug(
                        "3<<end_string<<%s<<",
                        ParserHelper.make_value_visible(end_string),
                    )
                    LOGGER.debug("ws>%s<", ParserHelper.make_value_visible(end_string))
                LOGGER.debug(
                    "handle_line_end>>%s<<",
                    ParserHelper.make_value_visible(
                        source_text[inline_response.new_index :]
                    ),
                )
                LOGGER.debug(
                    "end_string(after)>>%s<<",
                    ParserHelper.make_value_visible(end_string),
                )
                was_new_line = True
                if para_owner:
                    para_owner.rehydrate_index += 1

            LOGGER.debug(
                "new_string-->%s<--",
                ParserHelper.make_value_visible(inline_response.new_string),
            )
            LOGGER.debug("new_index-->%s<--", str(inline_response.new_index))
            LOGGER.debug(
                "new_tokens-->%s<--",
                ParserHelper.make_value_visible(inline_response.new_tokens),
            )
            LOGGER.debug(
                "new_string_unresolved-->%s<--",
                ParserHelper.make_value_visible(inline_response.new_string_unresolved),
            )
            LOGGER.debug(
                "consume_rest_of_line-->%s<--",
                str(inline_response.consume_rest_of_line),
            )
            LOGGER.debug(
                "original_string-->%s<--",
                ParserHelper.make_value_visible(inline_response.original_string),
            )

            if inline_response.consume_rest_of_line:
                LOGGER.debug("consume_rest_of_line>>%s<", str(remaining_line))
                inline_response.new_string = ""
                reset_current_string = True
                inline_response.new_tokens = None
                remaining_line = ""
                end_string = None
                LOGGER.debug(
                    "9<<end_string<<%s<<",
                    ParserHelper.make_value_visible(end_string),
                )
            else:
                LOGGER.debug("append_rest_of_line>>%s<", str(remaining_line))
                current_string = InlineHelper.append_text(
                    current_string, remaining_line
                )
                current_string_unresolved = InlineHelper.append_text(
                    current_string_unresolved, remaining_line
                )

            LOGGER.debug(
                "current_string>>%s<<",
                ParserHelper.make_value_visible(current_string),
            )
            LOGGER.debug(
                "current_string_unresolved>>%s<<",
                ParserHelper.make_value_visible(current_string_unresolved),
            )
            LOGGER.debug(
                "inline_blocks>>%s<<",
                ParserHelper.make_value_visible(inline_blocks),
            )
            LOGGER.debug(
                "inline_response.new_tokens>>%s<<",
                ParserHelper.make_value_visible(inline_response.new_tokens),
            )
            LOGGER.debug(
                "starting_whitespace>>%s<<",
                ParserHelper.make_value_visible(starting_whitespace),
            )
            if inline_response.new_tokens:
                if current_string:
                    LOGGER.debug(">>>text1")
                    inline_blocks.append(
                        TextMarkdownToken(
                            current_string,
                            starting_whitespace,
                            end_whitespace=end_string,
                            line_number=last_line_number,
                            column_number=last_column_number,
                        )
                    )
                    LOGGER.debug(
                        "new Text>>%s>>", ParserHelper.make_value_visible(inline_blocks)
                    )
                    reset_current_string = True
                    starting_whitespace = ""
                    end_string = None
                    LOGGER.debug(
                        "4<<end_string<<%s<<",
                        ParserHelper.make_value_visible(end_string),
                    )
                elif starting_whitespace:
                    LOGGER.debug(">>>starting whitespace")
                    inline_blocks.append(
                        TextMarkdownToken(
                            "",
                            ParserHelper.create_replace_with_nothing_marker(
                                starting_whitespace
                            ),
                            line_number=last_line_number,
                            column_number=last_column_number,
                        )
                    )
                    LOGGER.debug(
                        "new Text>>%s>>", ParserHelper.make_value_visible(inline_blocks)
                    )
                    starting_whitespace = ""

                inline_blocks.extend(inline_response.new_tokens)

            LOGGER.debug(
                "l/c(before)>>%s,%s<<",
                ParserHelper.make_value_visible(line_number),
                ParserHelper.make_value_visible(column_number),
            )
            if was_new_line:
                LOGGER.debug("l/c(before)>>newline")
                line_number += 1
                column_number = 1
                assert fold_space
                LOGGER.debug("fold_space(before)>>%s<<", str(fold_space))
                fold_space = fold_space[1:]
                LOGGER.debug("fold_space(after)>>%s<<", str(fold_space))
                column_number += len(fold_space[0])

            elif not was_column_number_reset:
                LOGGER.debug(
                    "l/c(remaining_line)>>%s,%s<<",
                    str(len(remaining_line)),
                    ParserHelper.make_value_visible(remaining_line),
                )
                column_number += len(remaining_line)
            LOGGER.debug(
                "l/c(after)>>%s,%s<<",
                ParserHelper.make_value_visible(line_number),
                ParserHelper.make_value_visible(column_number),
            )

            LOGGER.debug(
                "starting_whitespace>>%s<<",
                ParserHelper.make_value_visible(starting_whitespace),
            )
            LOGGER.debug(
                "inline_blocks>>%s<<",
                ParserHelper.make_value_visible(inline_blocks),
            )
            LOGGER.debug(
                "reset_current_string>>%s<<",
                ParserHelper.make_value_visible(reset_current_string),
            )

            if reset_current_string:
                current_string = ""
                current_string_unresolved = ""
            LOGGER.debug("pos>>%s,%s<<", str(line_number), str(column_number))
            LOGGER.debug(
                "last>>%s,%s<<", str(last_line_number), str(last_column_number)
            )
            LOGGER.debug(
                "old>>%s>>now>>%s<<",
                str(old_inline_blocks_count),
                str(len(inline_blocks)),
            )
            if old_inline_blocks_count != len(inline_blocks) or (
                old_inline_blocks_last_token
                and old_inline_blocks_last_token != inline_blocks[-1]
            ):
                last_line_number = line_number
                last_column_number = column_number
            LOGGER.debug(
                "last>>%s,%s<<", str(last_line_number), str(last_column_number)
            )
            LOGGER.debug(
                ">>Token_start>>%s,%s<<",
                str(last_line_number),
                str(last_column_number),
            )

            LOGGER.debug(
                "5<<end_string<<%s<<", ParserHelper.make_value_visible(end_string)
            )
            (
                start_index,
                next_index,
                end_string,
                current_string,
                current_string_unresolved,
            ) = InlineProcessor.__complete_inline_loop(
                source_text,
                inline_response.new_index,
                end_string,
                whitespace_to_add,
                current_string,
                current_string_unresolved,
                inline_response.new_string_unresolved,
                inline_response.new_string,
                inline_response.original_string,
            )
            LOGGER.debug(
                "6<<end_string<<%s<<", ParserHelper.make_value_visible(end_string)
            )
            LOGGER.debug(
                "<<current_string<<%s<<%s<<",
                str(len(current_string)),
                ParserHelper.make_value_visible(current_string),
            )
            LOGGER.debug(
                "<<current_string_unresolved<<%s<<%s<<",
                str(len(current_string_unresolved)),
                ParserHelper.make_value_visible(current_string_unresolved),
            )

        LOGGER.debug("<<__complete_inline_block_processing<<")
        LOGGER.debug(
            "<<__complete_inline_block_processing<<end_string<<%s<<",
            ParserHelper.make_value_visible(end_string),
        )
        return InlineProcessor.__complete_inline_block_processing(
            inline_blocks,
            source_text,
            start_index,
            current_string,
            end_string,
            starting_whitespace,
            is_setext,
            line_number=last_line_number,
            column_number=last_column_number,
        )

    # pylint: enable=too-many-statements, too-many-locals, too-many-arguments, too-many-branches

    @staticmethod
    def __add_recombined_whitespace(
        did_recombine, source_text, inline_response, end_string, is_setext
    ):

        LOGGER.debug("__arw>>did_recombine>>%s>>", str(did_recombine))
        LOGGER.debug(
            "__arw>>end_string>>%s>>",
            ParserHelper.make_value_visible(end_string),
        )
        if did_recombine:
            LOGGER.debug(
                "__arw>>source_text>>%s>>",
                ParserHelper.make_value_visible(source_text),
            )
            new_index, extracted_whitespace = ParserHelper.extract_whitespace(
                source_text, inline_response.new_index
            )
            LOGGER.debug(
                "__arw>>%s>>",
                ParserHelper.make_value_visible(
                    source_text[0 : inline_response.new_index]
                ),
            )
            LOGGER.debug(
                "__arw>>%s>>",
                ParserHelper.make_value_visible(
                    source_text[inline_response.new_index :]
                ),
            )
            LOGGER.debug(
                "__arw>>extracted_whitespace>>%s>>",
                ParserHelper.make_value_visible(extracted_whitespace),
            )
            if extracted_whitespace:
                inline_response.new_index = new_index
                assert end_string is not None
                end_string += extracted_whitespace
                assert is_setext
                end_string += ParserHelper.whitespace_split_character
                LOGGER.debug(
                    "__arw>>end_string>>%s>>",
                    ParserHelper.make_value_visible(end_string),
                )
        return end_string

    @staticmethod
    # pylint: disable=too-many-arguments
    def __complete_inline_loop(
        source_text,
        new_index,
        end_string,
        whitespace_to_add,
        current_string,
        current_string_unresolved,
        new_string_unresolved,
        new_string,
        original_string,
    ):
        LOGGER.debug(
            "__complete_inline_loop--current_string>>%s>>",
            ParserHelper.make_value_visible(current_string),
        )
        LOGGER.debug(
            "__complete_inline_loop--new_string>>%s>>",
            ParserHelper.make_value_visible(new_string),
        )
        LOGGER.debug(
            "__complete_inline_loop--new_string_unresolved>>%s>>",
            ParserHelper.make_value_visible(new_string_unresolved),
        )
        LOGGER.debug(
            "__complete_inline_loop--original_string>>%s>>",
            ParserHelper.make_value_visible(original_string),
        )

        LOGGER.debug(
            "__complete_inline_loop--current_string>>%s>>",
            ParserHelper.make_value_visible(current_string),
        )
        if original_string is not None:
            assert not new_string_unresolved or new_string_unresolved == original_string
            current_string += ParserHelper.create_replacement_markers(
                original_string, InlineHelper.append_text("", new_string)
            )
        else:
            current_string = InlineHelper.append_text(current_string, new_string)
        LOGGER.debug(
            "__complete_inline_loop--current_string>>%s>>",
            ParserHelper.make_value_visible(current_string),
        )

        LOGGER.debug(
            "__complete_inline_loop--current_string>>%s>>",
            ParserHelper.make_value_visible(current_string),
        )

        LOGGER.debug(
            "new_string_unresolved>>%s>>",
            ParserHelper.make_value_visible(new_string_unresolved),
        )
        if new_string_unresolved:
            current_string_unresolved += new_string_unresolved
        else:
            current_string_unresolved = InlineHelper.append_text(
                current_string_unresolved, new_string
            )

        LOGGER.debug(
            "__complete_inline_loop--current_string_unresolved>>%s>>",
            ParserHelper.make_value_visible(current_string_unresolved),
        )

        if whitespace_to_add is not None:
            end_string = InlineHelper.modify_end_string(end_string, whitespace_to_add)

        start_index = new_index
        next_index = ParserHelper.index_any_of(
            source_text,
            InlineProcessor.__valid_inline_text_block_sequence_starts,
            start_index,
        )
        return (
            start_index,
            next_index,
            end_string,
            current_string,
            current_string_unresolved,
        )

    # pylint: enable=too-many-arguments

    @staticmethod
    # pylint: disable=too-many-arguments
    def __complete_inline_block_processing(
        inline_blocks,
        source_text,
        start_index,
        current_string,
        end_string,
        starting_whitespace,
        is_setext,
        line_number,
        column_number,
    ):
        have_processed_once = len(inline_blocks) != 0 or start_index != 0

        LOGGER.debug(
            "__cibp>inline_blocks>%s<", ParserHelper.make_value_visible(inline_blocks)
        )
        LOGGER.debug(
            "__cibp>source_text>%s<", ParserHelper.make_value_visible(source_text)
        )
        LOGGER.debug(
            "__cibp>start_index>%s<", ParserHelper.make_value_visible(start_index)
        )
        LOGGER.debug(
            "__cibp>current_string>%s<", ParserHelper.make_value_visible(current_string)
        )
        LOGGER.debug(
            "__cibp>end_string>%s<", ParserHelper.make_value_visible(end_string)
        )
        LOGGER.debug(
            "__cibp>starting_whitespace>%s<",
            ParserHelper.make_value_visible(starting_whitespace),
        )
        LOGGER.debug("__cibp>is_setext>%s<", ParserHelper.make_value_visible(is_setext))
        LOGGER.debug(
            "__cibp>line_number>%s<", ParserHelper.make_value_visible(line_number)
        )
        LOGGER.debug(
            "__cibp>column_number>%s<", ParserHelper.make_value_visible(column_number)
        )

        if inline_blocks and inline_blocks[-1].is_inline_hard_break:
            start_index, extracted_whitespace = ParserHelper.extract_whitespace(
                source_text, start_index
            )
            assert end_string
            end_string += extracted_whitespace

        if start_index < len(source_text):
            current_string = InlineHelper.append_text(
                current_string, source_text[start_index:]
            )

        if end_string is not None:
            LOGGER.debug("xx-end-lf>%s<", ParserHelper.make_value_visible(end_string))
        if current_string or not have_processed_once:
            inline_blocks.append(
                TextMarkdownToken(
                    current_string,
                    starting_whitespace,
                    end_whitespace=end_string,
                    line_number=line_number,
                    column_number=column_number,
                )
            )
        LOGGER.debug(">>%s<<", ParserHelper.make_value_visible(inline_blocks))

        return EmphasisHelper.resolve_inline_emphasis(inline_blocks, None)

    # pylint: enable=too-many-arguments


# pylint: enable=too-few-public-methods
