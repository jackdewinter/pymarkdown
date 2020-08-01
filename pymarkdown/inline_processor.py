"""
Inline processing
"""
import logging

from pymarkdown.emphasis_helper import EmphasisHelper
from pymarkdown.inline_helper import InlineHelper, InlineRequest, InlineResponse
from pymarkdown.link_helper import LinkHelper
from pymarkdown.markdown_token import (
    MarkdownToken,
    SpecialTextMarkdownToken,
    TextMarkdownToken,
)
from pymarkdown.parser_helper import ParserHelper

LOGGER = logging.getLogger(__name__)


# pylint: disable=too-few-public-methods
class InlineProcessor:
    """
    Handle the inline processing of the token stream.
    """

    __valid_inline_text_block_sequence_starts = ""
    __inline_processing_needed = (
        EmphasisHelper.inline_emphasis
        + LinkHelper.link_label_start
        + LinkHelper.link_label_end
    )
    __inline_character_handlers = {}

    """
    Class to provide helper functions for parsing html.
    """

    @staticmethod
    def initialize():
        """
        Initialize the inline processor subsystem.
        """
        InlineProcessor.__inline_character_handlers = {}
        InlineProcessor.__valid_inline_text_block_sequence_starts = (
            ParserHelper.newline_character
        )
        InlineProcessor.register_handlers(
            InlineHelper.code_span_bounds, InlineHelper.handle_inline_backtick
        )
        InlineProcessor.register_handlers(
            InlineHelper.backslash_character, InlineHelper.handle_inline_backslash
        )
        InlineProcessor.register_handlers(
            InlineHelper.character_reference_start_character,
            InlineHelper.handle_character_reference,
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

    @staticmethod
    def register_handlers(inline_character, start_token_handler):
        """
        Register the handlers necessary to deal with token's start and end.
        """
        InlineProcessor.__inline_character_handlers[
            inline_character
        ] = start_token_handler
        InlineProcessor.__valid_inline_text_block_sequence_starts = (
            InlineProcessor.__valid_inline_text_block_sequence_starts + inline_character
        )

    @staticmethod
    def parse_inline(coalesced_results):
        """
        Parse and resolve any inline elements.
        """
        LOGGER.info("coalesced_results")
        LOGGER.info("-----")
        for next_token in coalesced_results:
            LOGGER.info(">>%s<<", ParserHelper.make_value_visible(next_token))
        LOGGER.info("-----")

        coalesced_list = []
        coalesced_list.extend(coalesced_results[0:1])
        for coalesce_index in range(1, len(coalesced_results)):
            if coalesced_results[coalesce_index].is_text and (
                coalesced_list[-1].is_paragraph
                or coalesced_list[-1].is_setext
                or coalesced_list[-1].is_atx_heading
                or coalesced_list[-1].is_code_block
            ):
                if coalesced_list[-1].is_code_block:
                    encoded_text = InlineHelper.append_text(
                        "", coalesced_results[coalesce_index].token_text
                    )
                    processed_tokens = [
                        TextMarkdownToken(
                            encoded_text,
                            coalesced_results[coalesce_index].extracted_whitespace,
                        )
                    ]
                elif coalesced_list[-1].is_setext:
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
                    )
                    LOGGER.debug(
                        "processed_tokens>>%s",
                        ParserHelper.make_value_visible(processed_tokens),
                    )
                elif coalesced_list[-1].is_atx_heading:
                    processed_tokens = InlineProcessor.__process_inline_text_block(
                        coalesced_results[coalesce_index].token_text.replace(
                            ParserHelper.tab_character, "    "
                        ),
                        coalesced_results[coalesce_index].extracted_whitespace.replace(
                            ParserHelper.tab_character, "    "
                        ),
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
                    )
                coalesced_list.extend(processed_tokens)
            else:
                coalesced_list.append(coalesced_results[coalesce_index])
        return coalesced_list

    @staticmethod
    def __handle_inline_special_single_character(inline_request):
        return InlineProcessor.__handle_inline_special(
            inline_request.source_text,
            inline_request.next_index,
            inline_request.inline_blocks,
            1,
            inline_request.remaining_line,
            inline_request.current_string_unresolved,
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
            )
            assert not inline_response.consume_rest_of_line
        else:
            inline_response = InlineResponse()
            inline_response.new_string = LinkHelper.image_start_sequence[0]
            inline_response.new_index = inline_request.next_index + 1
        return inline_response

    # pylint: disable=too-many-arguments
    # pylint: disable=too-many-locals
    @staticmethod
    def __handle_inline_special(
        source_text,
        next_index,
        inline_blocks,
        special_length,
        remaining_line,
        current_string_unresolved,
    ):
        """
        Handle the collection of special inline characters for later processing.
        """
        preceding_two = None
        following_two = None
        new_token = None
        repeat_count = 1
        is_active = True
        consume_rest_of_line = False
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
                LOGGER.debug(">>inline_blocks>>%s<<", str(inline_blocks))
                LOGGER.debug(">>remaining_line>>%s<<", str(remaining_line))
                LOGGER.debug(
                    ">>current_string_unresolved>>%s<<", str(current_string_unresolved)
                )
                LOGGER.debug(">>source_text>>%s<<", source_text[next_index:])
                LOGGER.debug("")
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
                )
                LOGGER.debug(">>inline_blocks>>%s<<", str(inline_blocks))
                LOGGER.debug(">>new_token>>%s<<", str(new_token))
                LOGGER.debug(">>source_text>>%s<<", source_text[new_index:])
                LOGGER.debug(">>consume_rest_of_line>>%s<<", str(consume_rest_of_line))
            else:
                repeat_count = special_length
                new_index = next_index + special_length

        if not new_token:
            new_token = SpecialTextMarkdownToken(
                special_sequence, repeat_count, preceding_two, following_two, is_active
            )

        inline_response = InlineResponse()
        inline_response.new_string = ""
        inline_response.new_index = new_index
        inline_response.new_tokens = [new_token]
        inline_response.consume_rest_of_line = consume_rest_of_line
        return inline_response

    # pylint: enable=too-many-arguments
    # pylint: enable=too-many-locals

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

    @staticmethod
    # pylint: disable=too-many-statements
    # pylint: disable=too-many-locals
    def __process_inline_text_block(
        source_text,
        starting_whitespace="",
        whitespace_to_recombine=None,
        is_setext=False,
    ):
        """
        Process a text block for any inline items.
        """

        inline_blocks = []
        start_index = 0
        LOGGER.debug(
            "__process_inline_text_block>>source_text>>%s",
            ParserHelper.make_value_visible(source_text),
        )
        LOGGER.debug(
            "__process_inline_text_block>>whitespace_to_recombine>>%s",
            ParserHelper.make_value_visible(whitespace_to_recombine),
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

        current_string = ""
        current_string_unresolved = ""
        end_string = ""

        inline_response = InlineResponse()

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

            inline_response.clear_fields()
            reset_current_string = False
            whitespace_to_add = None

            LOGGER.debug(
                "__process_inline_text_block>>%s>>%s", str(start_index), str(next_index)
            )
            remaining_line = source_text[start_index:next_index]

            inline_request = InlineRequest(
                source_text,
                next_index,
                inline_blocks,
                remaining_line,
                current_string_unresolved,
            )
            if source_text[next_index] in InlineProcessor.__inline_character_handlers:
                LOGGER.debug("handler(before)>>%s<<", source_text[next_index])
                proc_fn = InlineProcessor.__inline_character_handlers[
                    source_text[next_index]
                ]
                inline_response = proc_fn(inline_request)
                LOGGER.debug("handler(after)>>%s<<", source_text[next_index])
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
                    next_index, remaining_line, end_string, current_string
                )
                LOGGER.debug(
                    "handle_line_end>>new_tokens>>%s<<",
                    ParserHelper.make_value_visible(inline_response.new_tokens),
                )
                if not inline_response.new_tokens:
                    end_string = InlineProcessor.__add_recombined_whitespace(
                        bool(whitespace_to_recombine),
                        source_text,
                        inline_response,
                        end_string,
                        is_setext,
                    )
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
                inline_response.new_string = ""
                reset_current_string = True
                inline_response.new_tokens = None
            else:
                current_string = InlineHelper.append_text(
                    current_string, remaining_line
                )
                current_string_unresolved = InlineHelper.append_text(
                    current_string_unresolved, remaining_line
                )

            LOGGER.debug(
                "current_string>>%s<<", ParserHelper.make_value_visible(current_string),
            )
            LOGGER.debug(
                "current_string_unresolved>>%s<<",
                ParserHelper.make_value_visible(current_string_unresolved),
            )
            if inline_response.new_tokens:
                if current_string:
                    # assert end_string is None
                    inline_blocks.append(
                        TextMarkdownToken(
                            current_string,
                            starting_whitespace,
                            end_whitespace=end_string,
                        )
                    )
                    reset_current_string = True
                    starting_whitespace = ""
                    end_string = None

                inline_blocks.extend(inline_response.new_tokens)

            if reset_current_string:
                current_string = ""
                current_string_unresolved = ""

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
        return InlineProcessor.__complete_inline_block_processing(
            inline_blocks,
            source_text,
            start_index,
            current_string,
            end_string,
            starting_whitespace,
            is_setext,
        )

    # pylint: enable=too-many-statements
    # pylint: enable=too-many-locals

    @staticmethod
    def __add_recombined_whitespace(
        did_recombine, source_text, inline_response, end_string, is_setext
    ):

        LOGGER.debug("__arw>>did_recombine>>%s>>", str(did_recombine))
        LOGGER.debug(
            "__arw>>end_string>>%s>>", ParserHelper.make_value_visible(end_string),
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

        if (
            inline_blocks
            and inline_blocks[-1].token_name == MarkdownToken.token_inline_hard_break
        ):
            start_index, extracted_whitespace = ParserHelper.extract_whitespace(
                source_text, start_index
            )
            if end_string is None:
                end_string = extracted_whitespace
            else:
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
                    current_string, starting_whitespace, end_whitespace=end_string
                )
            )
        LOGGER.debug(">>%s<<", ParserHelper.make_value_visible(inline_blocks))

        return EmphasisHelper.resolve_inline_emphasis(inline_blocks, None)

    # pylint: enable=too-many-arguments


# pylint: enable=too-few-public-methods
