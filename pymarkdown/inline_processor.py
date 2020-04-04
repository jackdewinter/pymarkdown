"""
Inline processing
"""
from pymarkdown.constants import Constants
from pymarkdown.emphasis_helper import EmphasisHelper
from pymarkdown.inline_helper import InlineHelper, InlineRequest, InlineResponse
from pymarkdown.link_helper import LinkHelper
from pymarkdown.markdown_token import SpecialTextMarkdownToken, TextMarkdownToken
from pymarkdown.parser_helper import ParserHelper


# pylint: disable=too-few-public-methods
class InlineProcessor:
    """
    Handle the inline processing of the token stream.
    """

    __valid_inline_text_block_sequence_starts = "`\\&\n<*_[!]"
    __inline_processing_needed = Constants.inline_emphasis + "[]"
    inline_character_handlers = {}

    """
    Class to provide helper functions for parsing html.
    """

    @staticmethod
    def initialize():
        """
        Initialize the inline processor subsystem.
        """
        InlineProcessor.inline_character_handlers = {}
        InlineProcessor.register_handlers("`", InlineHelper.handle_inline_backtick)
        InlineProcessor.register_handlers("\\", InlineHelper.handle_inline_backslash)
        InlineProcessor.register_handlers("&", InlineHelper.handle_character_reference)
        InlineProcessor.register_handlers("<", InlineHelper.handle_angle_brackets)

    @staticmethod
    def register_handlers(inline_character, start_token_handler):
        """
        Register the handlers necessary to deal with token's start and end.
        """
        InlineProcessor.inline_character_handlers[
            inline_character
        ] = start_token_handler

    @staticmethod
    def parse_inline(coalesced_results):
        """
        Parse and resolve any inline elements.
        """

        for next_token in coalesced_results:
            print(">>" + str(next_token) + "<<")
        print("")

        coalesced_list = []
        coalesced_list.extend(coalesced_results[0:1])
        for coalesce_index in range(1, len(coalesced_results)):
            if coalesced_results[coalesce_index].is_text and (
                coalesced_list[-1].is_paragraph
                or coalesced_list[-1].is_setext
                or coalesced_list[-1].is_atx_header
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
                    combined_test = (
                        coalesced_results[coalesce_index].extracted_whitespace
                        + coalesced_results[coalesce_index].token_text
                    )
                    processed_tokens = InlineProcessor.__process_inline_text_block(
                        combined_test.replace("\t", "    ")
                    )
                elif coalesced_list[-1].is_atx_header:
                    processed_tokens = InlineProcessor.__process_inline_text_block(
                        coalesced_results[coalesce_index].token_text.replace(
                            "\t", "    "
                        ),
                        coalesced_results[coalesce_index].extracted_whitespace.replace(
                            "\t", "    "
                        ),
                    )
                else:
                    print(
                        ">>before_add_ws>>"
                        + str(coalesced_list[-1])
                        + ">>add>>"
                        + str(coalesced_results[coalesce_index].extracted_whitespace)
                        + ">>"
                    )
                    coalesced_list[-1].add_whitespace(
                        coalesced_results[coalesce_index].extracted_whitespace.replace(
                            "\t", "    "
                        )
                    )
                    print(">>after_add_ws>>" + str(coalesced_list[-1]))
                    processed_tokens = InlineProcessor.__process_inline_text_block(
                        coalesced_results[coalesce_index].token_text.replace(
                            "\t", "    "
                        )
                    )
                coalesced_list.extend(processed_tokens)
            else:
                coalesced_list.append(coalesced_results[coalesce_index])
        return coalesced_list

    # pylint: disable=too-many-arguments
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

        preceeding_two = None
        following_two = None
        new_token = None
        repeat_count = 1
        is_active = True
        consume_rest_of_line = False
        special_sequence = source_text[next_index : next_index + special_length]
        if special_length == 1 and special_sequence in Constants.inline_emphasis:
            repeat_count, new_index = ParserHelper.collect_while_character(
                source_text, next_index, special_sequence
            )
            special_sequence = source_text[next_index:new_index]

            preceeding_two = source_text[max(0, next_index - 2) : next_index]
            following_two = source_text[
                new_index : min(len(source_text), new_index + 2)
            ]
        else:
            if special_sequence[0] == "]":
                print(
                    "\nPOSSIBLE LINK CLOSE_FOUND>>"
                    + str(special_length)
                    + ">>"
                    + special_sequence
                    + ">>"
                )
                print(">>inline_blocks>>" + str(inline_blocks) + "<<")
                print(">>remaining_line>>" + str(remaining_line) + "<<")
                print(
                    ">>current_string_unresolved>>"
                    + str(current_string_unresolved)
                    + "<<"
                )
                print(">>source_text>>" + source_text[next_index:] + "<<")
                print("")
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
                print(">>inline_blocks>>" + str(inline_blocks) + "<<")
                print(">>new_token>>" + str(new_token) + "<<")
                print(">>source_text>>" + source_text[new_index:] + "<<")
                print(">>consume_rest_of_line>>" + str(consume_rest_of_line) + "<<")
            else:
                repeat_count = special_length
                new_index = next_index + special_length

        if not new_token:
            new_token = SpecialTextMarkdownToken(
                special_sequence, repeat_count, preceeding_two, following_two, is_active
            )

        inline_response = InlineResponse()
        inline_response.new_string = ""
        inline_response.new_index = new_index
        inline_response.new_tokens = [new_token]
        inline_response.consume_rest_of_line = consume_rest_of_line
        return inline_response

    # pylint: enable=too-many-arguments

    @staticmethod
    def __process_inline_text_block(source_text, starting_whitespace=""):
        """
        Process a text block for any inline items.
        """

        inline_blocks = []
        start_index = 0

        current_string = ""
        current_string_unresolved = ""
        end_string = None

        inline_response = InlineResponse()

        next_index = ParserHelper.index_any_of(
            source_text,
            InlineProcessor.__valid_inline_text_block_sequence_starts,
            start_index,
        )
        while next_index != -1:

            inline_response.clear_fields()
            reset_current_string = False
            whitespace_to_add = None

            remaining_line = source_text[start_index:next_index]

            if source_text[next_index] in InlineProcessor.inline_character_handlers:
                proc_fn = InlineProcessor.inline_character_handlers[
                    source_text[next_index]
                ]
                inline_request = InlineRequest(source_text, next_index)
                inline_response = proc_fn(inline_request)
            elif source_text[next_index] in InlineProcessor.__inline_processing_needed:
                inline_response = InlineProcessor.__handle_inline_special(
                    source_text,
                    next_index,
                    inline_blocks,
                    1,
                    remaining_line,
                    current_string_unresolved,
                )
            elif source_text[next_index] == "!":
                if ParserHelper.are_characters_at_index(source_text, next_index, "!["):
                    inline_response = InlineProcessor.__handle_inline_special(
                        source_text, next_index, inline_blocks, 2, remaining_line, "",
                    )
                    assert not inline_response.consume_rest_of_line
                else:
                    inline_response.new_string = "!"
                    inline_response.new_index = next_index + 1
            else:  # if source_text[next_index] == "\n":
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

            if inline_response.consume_rest_of_line:
                inline_response.new_string = ""
                reset_current_string = True
                remaining_line = ""
                inline_response.new_tokens = None
            else:
                current_string = InlineHelper.append_text(
                    current_string, remaining_line
                )
                current_string_unresolved = InlineHelper.append_text(
                    current_string_unresolved, remaining_line
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
            )

        return InlineProcessor.__complete_inline_block_processing(
            inline_blocks,
            source_text,
            start_index,
            current_string,
            end_string,
            starting_whitespace,
        )

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
    ):
        current_string = InlineHelper.append_text(current_string, new_string)

        if new_string_unresolved:
            current_string_unresolved = InlineHelper.append_text(
                current_string_unresolved, new_string_unresolved
            )
        else:
            current_string_unresolved = InlineHelper.append_text(
                current_string_unresolved, new_string
            )

        if whitespace_to_add:
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
    ):
        have_processed_once = len(inline_blocks) != 0 or start_index != 0

        if start_index < len(source_text):
            current_string = InlineHelper.append_text(
                current_string, source_text[start_index:]
            )

        if end_string is not None:
            print("xx-end-lf>" + end_string.replace("\n", "\\n") + "<")
        if current_string or not have_processed_once:
            inline_blocks.append(
                TextMarkdownToken(
                    current_string, starting_whitespace, end_whitespace=end_string
                )
            )
        print(">>" + str(inline_blocks) + "<<")

        return EmphasisHelper.resolve_inline_emphasis(inline_blocks, None)

    # pylint: enable=too-many-arguments


# pylint: enable=too-few-public-methods
