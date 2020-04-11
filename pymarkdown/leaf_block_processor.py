"""
Module to provide processing for the leaf blocks.
"""
from pymarkdown.inline_helper import InlineHelper
from pymarkdown.markdown_token import (
    AtxHeaderMarkdownToken,
    BlankLineMarkdownToken,
    EndMarkdownToken,
    FencedCodeBlockMarkdownToken,
    IndentedCodeBlockMarkdownToken,
    ParagraphMarkdownToken,
    SetextHeaderEndMarkdownToken,
    SetextHeaderMarkdownToken,
    TextMarkdownToken,
    ThematicBreakMarkdownToken,
)
from pymarkdown.parser_helper import ParserHelper
from pymarkdown.stack_token import (
    BlockQuoteStackToken,
    FencedCodeBlockStackToken,
    IndentedCodeBlockStackToken,
    ParagraphStackToken,
)


class LeafBlockProcessor:
    """
    Class to provide processing for the leaf blocks.
    """

    __fenced_start_tilde = "~"
    __fenced_start_backtick = "`"
    __fenced_code_block_start_characters = (
        __fenced_start_tilde + __fenced_start_backtick
    )
    __thematic_break_characters = "*_-"
    __atx_character = "#"
    __setext_characters = "-="

    @staticmethod
    def is_fenced_code_block(
        line_to_parse, start_index, extracted_whitespace, skip_whitespace_check=False,
    ):
        """
        Determine if we have the start of a fenced code block.
        """

        if (
            ParserHelper.is_length_less_than_or_equal_to(extracted_whitespace, 3)
            or skip_whitespace_check
        ) and ParserHelper.is_character_at_index_one_of(
            line_to_parse,
            start_index,
            LeafBlockProcessor.__fenced_code_block_start_characters,
        ):
            print(
                "ifcb:collected_count>>"
                + line_to_parse
                + "<<"
                + str(start_index)
                + "<<"
            )
            collected_count, new_index = ParserHelper.collect_while_character(
                line_to_parse, start_index, line_to_parse[start_index]
            )
            print("ifcb:collected_count:" + str(collected_count))
            (
                non_whitespace_index,
                extracted_whitespace_before_info_string,
            ) = ParserHelper.extract_whitespace(line_to_parse, new_index)

            if collected_count >= 3:
                print("ifcb:True")
                return (
                    True,
                    non_whitespace_index,
                    extracted_whitespace_before_info_string,
                    collected_count,
                )
        return False, None, None, None

    # pylint: disable=too-many-locals
    @staticmethod
    def parse_fenced_code_block(
        token_stack,
        line_to_parse,
        start_index,
        extracted_whitespace,
        close_open_blocks_fn,
    ):
        """
        Handle the parsing of a fenced code block
        """

        new_tokens = []
        (
            is_fence_start,
            non_whitespace_index,
            extracted_whitespace_before_info_string,
            collected_count,
        ) = LeafBlockProcessor.is_fenced_code_block(
            line_to_parse, start_index, extracted_whitespace
        )
        if is_fence_start and not token_stack[-1].is_html_block:
            if token_stack[-1].is_fenced_code_block:
                print("pfcb->end")

                if (
                    token_stack[-1].code_fence_character == line_to_parse[start_index]
                    and collected_count >= token_stack[-1].fence_character_count
                    and non_whitespace_index >= len(line_to_parse)
                ):
                    new_tokens.append(
                        token_stack[-1].generate_close_token(extracted_whitespace)
                    )
                    del token_stack[-1]
            else:
                print("pfcb->check")
                if (
                    line_to_parse[start_index]
                    == LeafBlockProcessor.__fenced_start_tilde
                    or LeafBlockProcessor.__fenced_start_backtick
                    not in line_to_parse[non_whitespace_index:]
                ):
                    print("pfcb->start")
                    (
                        after_extracted_text_index,
                        extracted_text,
                    ) = ParserHelper.extract_until_whitespace(
                        line_to_parse, non_whitespace_index
                    )
                    text_after_extracted_text = line_to_parse[
                        after_extracted_text_index:
                    ]

                    new_tokens, _, _ = close_open_blocks_fn(
                        only_these_blocks=[ParagraphStackToken],
                    )

                    token_stack.append(
                        FencedCodeBlockStackToken(
                            code_fence_character=line_to_parse[start_index],
                            fence_character_count=collected_count,
                            whitespace_start_count=ParserHelper.calculate_length(
                                extracted_whitespace
                            ),
                        )
                    )
                    extracted_text = InlineHelper.handle_backslashes(extracted_text)
                    text_after_extracted_text = InlineHelper.handle_backslashes(
                        text_after_extracted_text
                    )
                    new_tokens.append(
                        FencedCodeBlockMarkdownToken(
                            line_to_parse[start_index],
                            collected_count,
                            extracted_text,
                            text_after_extracted_text,
                            extracted_whitespace,
                            extracted_whitespace_before_info_string,
                        )
                    )
        elif (
            token_stack[-1].is_fenced_code_block
            and token_stack[-1].whitespace_start_count
            and extracted_whitespace
        ):

            current_whitespace_length = ParserHelper.calculate_length(
                extracted_whitespace
            )
            whitespace_left = max(
                0, current_whitespace_length - token_stack[-1].whitespace_start_count
            )
            extracted_whitespace = "".rjust(whitespace_left, " ")
        return new_tokens, extracted_whitespace

    # pylint: enable=too-many-locals

    @staticmethod
    def parse_indented_code_block(
        token_stack,
        line_to_parse,
        start_index,
        extracted_whitespace,
        removed_chars_at_start,
    ):
        """
        Handle the parsing of an indented code block
        """

        new_tokens = []

        if (
            ParserHelper.is_length_greater_than_or_equal_to(
                extracted_whitespace, 4, start_index=removed_chars_at_start
            )
            and not token_stack[-1].is_paragraph
        ):
            modified_whitespace_count = ParserHelper.calculate_length(
                extracted_whitespace, start_index=removed_chars_at_start
            )

            if not token_stack[-1].is_indented_code_block:
                token_stack.append(IndentedCodeBlockStackToken())
                new_tokens.append(IndentedCodeBlockMarkdownToken("".rjust(4)))
                extracted_whitespace = "".rjust(modified_whitespace_count - 4)
            new_tokens.append(
                TextMarkdownToken(line_to_parse[start_index:], extracted_whitespace)
            )
        return new_tokens

    @staticmethod
    def is_thematic_break(
        line_to_parse, start_index, extracted_whitespace, skip_whitespace_check=False,
    ):
        """
        Determine whether or not we have a thematic break.
        """

        thematic_break_character = None
        end_of_break_index = None
        if (
            ParserHelper.is_length_less_than_or_equal_to(extracted_whitespace, 3)
            or skip_whitespace_check
        ) and ParserHelper.is_character_at_index_one_of(
            line_to_parse, start_index, LeafBlockProcessor.__thematic_break_characters
        ):
            start_char = line_to_parse[start_index]
            index = start_index

            char_count = 0
            while index < len(line_to_parse):
                if ParserHelper.is_character_at_index_whitespace(line_to_parse, index):
                    index += 1
                elif line_to_parse[index] == start_char:
                    index += 1
                    char_count += 1
                else:
                    break

            if char_count >= 3 and index == len(line_to_parse):
                thematic_break_character = start_char
                end_of_break_index = index

        return thematic_break_character, end_of_break_index

    @staticmethod
    # pylint: disable=too-many-arguments
    def parse_thematic_break(
        token_stack,
        line_to_parse,
        start_index,
        extracted_whitespace,
        this_bq_count,
        close_open_blocks_fn,
        stack_bq_count,
    ):
        """
        Handle the parsing of a thematic break.
        """

        new_tokens = []

        start_char, index = LeafBlockProcessor.is_thematic_break(
            line_to_parse, start_index, extracted_whitespace
        )
        if start_char:
            if token_stack[-1].is_paragraph:
                new_tokens.append(token_stack[-1].generate_close_token())
                del token_stack[-1]
            if this_bq_count == 0 and stack_bq_count > 0:
                new_tokens, _, _ = close_open_blocks_fn(
                    destination_array=new_tokens,
                    only_these_blocks=[BlockQuoteStackToken],
                    include_block_quotes=True,
                )
            new_tokens.append(
                ThematicBreakMarkdownToken(
                    start_char,
                    extracted_whitespace.replace("\t", "    "),
                    line_to_parse[start_index:index].replace("\t", "    "),
                )
            )
        return new_tokens

    # pylint: enable=too-many-arguments

    @staticmethod
    def parse_atx_headings(
        line_to_parse, start_index, extracted_whitespace, close_open_blocks_fn
    ):
        """
        Handle the parsing of an atx heading.
        """

        new_tokens = []
        if ParserHelper.is_length_less_than_or_equal_to(
            extracted_whitespace, 3
        ) and ParserHelper.is_character_at_index(
            line_to_parse, start_index, LeafBlockProcessor.__atx_character
        ):
            hash_count, new_index = ParserHelper.collect_while_character(
                line_to_parse, start_index, LeafBlockProcessor.__atx_character
            )
            (
                non_whitespace_index,
                extracted_whitespace_at_start,
            ) = ParserHelper.extract_whitespace(line_to_parse, new_index)

            if hash_count <= 6 and (
                extracted_whitespace_at_start
                or non_whitespace_index == len(line_to_parse)
            ):

                new_tokens, _, _ = close_open_blocks_fn(new_tokens)
                remaining_line = line_to_parse[non_whitespace_index:]
                (
                    end_index,
                    extracted_whitespace_at_end,
                ) = ParserHelper.extract_whitespace_from_end(remaining_line)
                remove_trailing_count = 0
                while (
                    end_index > 0
                    and remaining_line[end_index - 1]
                    == LeafBlockProcessor.__atx_character
                ):
                    end_index -= 1
                    remove_trailing_count += 1
                extracted_whitespace_before_end = ""
                if remove_trailing_count:
                    if end_index > 0:
                        if ParserHelper.is_character_at_index_whitespace(
                            remaining_line, end_index - 1
                        ):
                            remaining_line = remaining_line[:end_index]
                            (
                                end_index,
                                extracted_whitespace_before_end,
                            ) = ParserHelper.extract_whitespace_from_end(remaining_line)
                            remaining_line = remaining_line[:end_index]
                        else:
                            extracted_whitespace_at_end = ""
                            remove_trailing_count = 0
                    else:
                        remaining_line = ""
                else:
                    extracted_whitespace_at_end = remaining_line[end_index:]
                    remaining_line = remaining_line[0:end_index]
                new_tokens.append(
                    AtxHeaderMarkdownToken(
                        hash_count, remove_trailing_count, extracted_whitespace,
                    )
                )
                new_tokens.append(
                    TextMarkdownToken(remaining_line, extracted_whitespace_at_start)
                )
                new_tokens.append(
                    EndMarkdownToken(
                        "atx",
                        extracted_whitespace_at_end,
                        extracted_whitespace_before_end,
                    )
                )
        return new_tokens

    # pylint: disable=too-many-arguments
    @staticmethod
    def parse_setext_headings(
        token_stack,
        token_document,
        line_to_parse,
        start_index,
        extracted_whitespace,
        this_bq_count,
        stack_bq_count,
    ):
        """
        Handle the parsing of an setext heading.
        """

        new_tokens = []
        if (
            ParserHelper.is_length_less_than_or_equal_to(extracted_whitespace, 3)
            and ParserHelper.is_character_at_index_one_of(
                line_to_parse, start_index, LeafBlockProcessor.__setext_characters
            )
            and token_stack[-1].is_paragraph
            and (this_bq_count == stack_bq_count)
        ):
            _, collected_to_index = ParserHelper.collect_while_character(
                line_to_parse, start_index, line_to_parse[start_index]
            )
            (
                after_whitespace_index,
                extra_whitespace_after_setext,
            ) = ParserHelper.extract_whitespace(line_to_parse, collected_to_index)
            if after_whitespace_index == len(line_to_parse):

                # This is unusual.  Normally, close_open_blocks is used to close off
                # blocks based on the stack token.  However, since the setext takes
                # the last paragraph of text (see case 61) and translates it
                # into a header, this has to be done separately, as there is no
                # stack token to close.
                new_tokens.append(
                    SetextHeaderEndMarkdownToken(
                        extracted_whitespace, extra_whitespace_after_setext
                    )
                )
                token_index = len(token_document) - 1
                while not token_document[token_index].is_paragraph:
                    token_index -= 1

                replacement_token = SetextHeaderMarkdownToken(
                    line_to_parse[start_index], token_document[token_index].extra_data,
                )
                token_document[token_index] = replacement_token
                del token_stack[-1]
        return new_tokens

    # pylint: enable=too-many-arguments

    # pylint: disable=too-many-arguments
    @staticmethod
    def parse_paragraph(
        token_stack,
        token_document,
        line_to_parse,
        start_index,
        extracted_whitespace,
        this_bq_count,
        no_para_start_if_empty,
        stack_bq_count,
        close_open_blocks_fn,
    ):
        """
        Handle the parsing of a paragraph.
        """
        new_tokens = []

        if no_para_start_if_empty and start_index >= len(line_to_parse):
            print("Escaping paragraph due to empty w/ blank")
            return [BlankLineMarkdownToken("")]

        print(
            "parse_paragraph>stack_bq_count>"
            + str(stack_bq_count)
            + ">this_bq_count>"
            + str(this_bq_count)
            + "<"
        )

        if (
            len(token_document) >= 2
            and token_document[-1].is_blank_line
            and token_document[-2].is_any_list_token
        ):

            did_find, last_list_index = LeafBlockProcessor.check_for_list_in_process(
                token_stack
            )
            assert did_find
            new_tokens, _, _ = close_open_blocks_fn(until_this_index=last_list_index)
        if stack_bq_count != 0 and this_bq_count == 0:
            new_tokens, _, _ = close_open_blocks_fn(
                only_these_blocks=[BlockQuoteStackToken], include_block_quotes=True,
            )

        if not token_stack[-1].is_paragraph:
            token_stack.append(ParagraphStackToken())
            new_tokens.append(ParagraphMarkdownToken(extracted_whitespace))
            extracted_whitespace = ""

        new_tokens.append(
            TextMarkdownToken(line_to_parse[start_index:], extracted_whitespace)
        )
        return new_tokens
        # pylint: enable=too-many-arguments

    @staticmethod
    def check_for_list_in_process(token_stack):
        """
        From the end of the stack, check to see if there is already a list in progress.
        """

        stack_index = len(token_stack) - 1
        while stack_index >= 0 and not token_stack[stack_index].is_list:
            stack_index -= 1
        return stack_index >= 0, stack_index
