"""
Module to provide helper functions for parsing html.
"""

import logging
import string
from typing import List, Optional, Tuple, cast

from pymarkdown.block_quotes.block_quote_data import BlockQuoteData
from pymarkdown.container_blocks.container_grab_bag import ContainerGrabBag
from pymarkdown.container_blocks.container_helper import ContainerHelper
from pymarkdown.container_blocks.parse_block_pass_properties import (
    ParseBlockPassProperties,
)
from pymarkdown.general.parser_helper import ParserHelper
from pymarkdown.general.parser_logger import ParserLogger
from pymarkdown.general.parser_state import ParserState
from pymarkdown.general.position_marker import PositionMarker
from pymarkdown.general.tab_helper import TabHelper
from pymarkdown.leaf_blocks.leaf_block_helper import LeafBlockHelper
from pymarkdown.tokens.html_block_markdown_token import HtmlBlockMarkdownToken
from pymarkdown.tokens.markdown_token import MarkdownToken
from pymarkdown.tokens.stack_token import (
    HtmlBlockStackToken,
    ParagraphStackToken,
    StackToken,
)
from pymarkdown.tokens.text_markdown_token import TextMarkdownToken

POGGER = ParserLogger(logging.getLogger(__name__))


class HtmlHelper:
    """
    Class to provide helper functions for parsing html.
    """

    html_block_1 = "1"
    html_block_2 = "2"
    html_block_3 = "3"
    html_block_4 = "4"
    html_block_5 = "5"
    html_block_6 = "6"
    html_block_7 = "7"

    __html_block_start_character = "<"
    __html_tag_start = "/"
    __html_tag_name_end = " >"
    __html_tag_end = ">"
    __html_attribute_value_single = "'"
    __html_attribute_value_double = '"'
    __html_attribute_name_value_separator = "="
    __html_attribute_separator = ParserHelper.space_character
    __valid_tag_name_characters = f"{string.ascii_letters}{string.digits}-"
    __html_block_1_start_tag_prefix = ["script", "pre", "style"]
    __html_tag_attribute_value_terminators = " \"'=<>`"
    __html_block_2_to_5_start = "!"
    __html_block_2_continued_start = "--"
    __html_block_3_continued_start = "?"
    __html_block_4_continued_start = string.ascii_uppercase
    __html_block_5_continued_start = "[CDATA["
    __html_block_1_end_tags = ["</script>", "</pre>", "</style>"]
    __html_block_2_end = "-->"
    __html_block_3_end = "?>"
    __html_block_4_end = __html_tag_end
    __html_block_5_end = "]]>"

    __attribute_start_characters = "abcdefghijklmnopqrstuvwxyz1234567890:_"
    __attribute_other_characters = f"{__attribute_start_characters}.-"

    __html_block_6_start = [
        "address",
        "article",
        "aside",
        "base",
        "basefont",
        "blockquote",
        "body",
        "caption",
        "center",
        "col",
        "colgroup",
        "dd",
        "details",
        "dialog",
        "dir",
        "div",
        "dl",
        "dt",
        "fieldset",
        "figcaption",
        "figure",
        "footer",
        "form",
        "frame",
        "frameset",
        "h1",
        "h2",
        "h3",
        "h4",
        "h5",
        "h6",
        "head",
        "header",
        "hr",
        "html",
        "iframe",
        "legend",
        "li",
        "link",
        "main",
        "menu",
        "menuitem",
        "nav",
        "noframes",
        "ol",
        "optgroup",
        "option",
        "p",
        "param",
        "section",
        "source",
        "summary",
        "table",
        "tbody",
        "td",
        "tfoot",
        "th",
        "thead",
        "title",
        "tr",
        "track",
        "ul",
    ]

    @staticmethod
    def is_valid_tag_name(tag_name: str) -> bool:
        """
        Determine if the html tag name is valid according to the html rules.
        """

        return (
            all(
                next_character in HtmlHelper.__valid_tag_name_characters
                for next_character in tag_name.lower()
            )
            if tag_name
            else False
        )

    @staticmethod
    def extract_html_attribute_name(string_to_parse: str, string_index: int) -> int:
        """
        Attempt to extract the attribute name from the provided string.
        """

        string_to_parse_length = len(string_to_parse)
        if not (
            string_index < string_to_parse_length
            and (
                string_to_parse[string_index] in HtmlHelper.__attribute_start_characters
            )
        ):
            return -1

        new_string_index, __ = ParserHelper.collect_while_one_of_characters_verified(
            string_to_parse, string_index + 1, HtmlHelper.__attribute_other_characters
        )
        if new_string_index < string_to_parse_length and string_to_parse[
            new_string_index
        ] in [
            HtmlHelper.__html_attribute_name_value_separator,
            HtmlHelper.__html_attribute_separator,
            HtmlHelper.__html_tag_start,
            HtmlHelper.__html_tag_end,
        ]:
            return new_string_index
        return -1

    @staticmethod
    def extract_optional_attribute_value(line_to_parse: str, value_index: int) -> int:
        """
        Determine and extract an optional attribute value.
        """

        non_whitespace_index, _ = ParserHelper.extract_spaces_verified(
            line_to_parse, value_index
        )
        line_to_parse_size = len(line_to_parse)
        if (
            non_whitespace_index < line_to_parse_size
            and line_to_parse[non_whitespace_index]
            != HtmlHelper.__html_attribute_name_value_separator
        ) or non_whitespace_index >= line_to_parse_size:
            return non_whitespace_index

        non_whitespace_index, _ = ParserHelper.extract_spaces_verified(
            line_to_parse, non_whitespace_index + 1
        )
        if non_whitespace_index < line_to_parse_size:
            first_character_of_value = line_to_parse[non_whitespace_index]
            extracted_text: Optional[str] = None
            if first_character_of_value == HtmlHelper.__html_attribute_value_double:
                (
                    non_whitespace_index,
                    _,
                ) = ParserHelper.collect_until_character_verified(
                    line_to_parse,
                    non_whitespace_index + 1,
                    HtmlHelper.__html_attribute_value_double,
                )
                if non_whitespace_index == line_to_parse_size:
                    return -1
                non_whitespace_index += 1
            elif first_character_of_value == HtmlHelper.__html_attribute_value_single:
                (
                    non_whitespace_index,
                    _,
                ) = ParserHelper.collect_until_character_verified(
                    line_to_parse,
                    non_whitespace_index + 1,
                    HtmlHelper.__html_attribute_value_single,
                )
                if non_whitespace_index == line_to_parse_size:
                    return -1
                non_whitespace_index += 1
            else:
                (
                    non_whitespace_index,
                    extracted_text,
                ) = ParserHelper.collect_until_one_of_characters_verified(
                    line_to_parse,
                    non_whitespace_index,
                    HtmlHelper.__html_tag_attribute_value_terminators,
                )
                if not extracted_text:
                    non_whitespace_index = -1
        else:
            non_whitespace_index = -1
        return non_whitespace_index

    @staticmethod
    def is_complete_html_end_tag(
        tag_name: str, line_to_parse: str, next_char_index: int
    ) -> Tuple[bool, int]:
        """
        Determine if the supplied information is a completed end of tag specification.
        """

        non_whitespace_index, _ = ParserHelper.extract_spaces_verified(
            line_to_parse, next_char_index
        )
        is_valid = HtmlHelper.is_valid_tag_name(tag_name) and (
            non_whitespace_index < len(line_to_parse)
            and line_to_parse[non_whitespace_index] == HtmlHelper.__html_tag_end
        )
        return is_valid, non_whitespace_index + 1

    @staticmethod
    def __is_valid_block_1_tag_name(tag_name: str) -> bool:
        """
        Determine if the tag name is a valid block-1 html tag name.
        """

        return tag_name in HtmlHelper.__html_block_1_start_tag_prefix

    @staticmethod
    def is_complete_html_start_tag(
        tag_name: str, line_to_parse: str, next_char_index: int
    ) -> Tuple[bool, Optional[int]]:
        """
        Determine if the supplied information is a completed start of tag specification.
        """

        is_tag_valid = HtmlHelper.is_valid_tag_name(
            tag_name
        ) and not HtmlHelper.__is_valid_block_1_tag_name(tag_name)

        non_whitespace_index, extracted_whitespace = (
            ParserHelper.extract_spaces_verified(line_to_parse, next_char_index)
        )
        are_attributes_valid: bool = True
        line_to_parse_size: int = len(line_to_parse)
        while (
            is_tag_valid
            and extracted_whitespace
            and are_attributes_valid
            and 0 <= non_whitespace_index < line_to_parse_size
            and line_to_parse[non_whitespace_index]
            not in [HtmlHelper.__html_tag_end, HtmlHelper.__html_tag_start]
        ):
            non_whitespace_index = HtmlHelper.extract_html_attribute_name(
                line_to_parse, non_whitespace_index
            )
            are_attributes_valid = non_whitespace_index != -1
            if not are_attributes_valid:
                break
            non_whitespace_index = HtmlHelper.extract_optional_attribute_value(
                line_to_parse, non_whitespace_index
            )
            are_attributes_valid = non_whitespace_index != -1
            if not are_attributes_valid:
                break
            (
                non_whitespace_index,
                extracted_whitespace,
            ) = ParserHelper.extract_spaces_verified(
                line_to_parse, non_whitespace_index
            )

        if non_whitespace_index < line_to_parse_size:
            if line_to_parse[non_whitespace_index] == HtmlHelper.__html_tag_start:
                non_whitespace_index += 1
            is_end_of_tag_present = (
                line_to_parse[non_whitespace_index] == HtmlHelper.__html_tag_end
            )
            if is_end_of_tag_present:
                non_whitespace_index += 1
        else:
            is_end_of_tag_present = False

        non_whitespace_indexx, _ = ParserHelper.extract_spaces(
            line_to_parse, non_whitespace_index
        )
        return (
            (
                is_tag_valid
                and is_end_of_tag_present
                and non_whitespace_indexx == line_to_parse_size
                and are_attributes_valid
            ),
            non_whitespace_indexx,
        )

    @staticmethod
    def __check_for_special_html_blocks(
        line_to_parse: str, character_index: int
    ) -> Optional[str]:
        """
        Check for the easy to spot special blocks: 2-5.
        """

        if character_index >= len(line_to_parse):
            return None
        html_block_type = None
        if ParserHelper.is_character_at_index(
            line_to_parse, character_index, HtmlHelper.__html_block_2_to_5_start
        ):
            if ParserHelper.are_characters_at_index(
                line_to_parse,
                character_index + 1,
                HtmlHelper.__html_block_2_continued_start,
            ):
                html_block_type = HtmlHelper.html_block_2
            elif ParserHelper.is_character_at_index_one_of(
                line_to_parse,
                character_index + 1,
                HtmlHelper.__html_block_4_continued_start,
            ):
                html_block_type = HtmlHelper.html_block_4
            elif ParserHelper.are_characters_at_index(
                line_to_parse,
                character_index + 1,
                HtmlHelper.__html_block_5_continued_start,
            ):
                html_block_type = HtmlHelper.html_block_5
        elif ParserHelper.is_character_at_index(
            line_to_parse,
            character_index,
            HtmlHelper.__html_block_3_continued_start,
        ):
            html_block_type = HtmlHelper.html_block_3

        return html_block_type

    @staticmethod
    def __check_for_normal_html_blocks_adjust_tag(
        remaining_html_tag: str, line_to_parse: str, character_index: int
    ) -> Tuple[str, int, bool]:
        adjusted_remaining_html_tag, line_to_parse_size = remaining_html_tag, len(
            line_to_parse
        )
        is_end_tag = (
            bool(adjusted_remaining_html_tag)
            and adjusted_remaining_html_tag[0] == HtmlHelper.__html_tag_start
        )
        if is_end_tag:
            adjusted_remaining_html_tag = adjusted_remaining_html_tag[1:]

        if (
            character_index < line_to_parse_size
            and line_to_parse[character_index] == HtmlHelper.__html_tag_end
            and adjusted_remaining_html_tag
            and adjusted_remaining_html_tag[-1] == HtmlHelper.__html_tag_start
        ):
            adjusted_remaining_html_tag = adjusted_remaining_html_tag[:-1]

        return adjusted_remaining_html_tag, line_to_parse_size, is_end_tag

    @staticmethod
    def __check_for_normal_html_blocks(
        remaining_html_tag: str, line_to_parse: str, character_index: int
    ) -> Optional[str]:
        """
        Check for the the html blocks that are harder to identify: 1, 6-7.
        """

        html_block_type = None

        if HtmlHelper.__is_valid_block_1_tag_name(remaining_html_tag):
            html_block_type = HtmlHelper.html_block_1
        else:
            (
                adjusted_remaining_html_tag,
                line_to_parse_size,
                is_end_tag,
            ) = HtmlHelper.__check_for_normal_html_blocks_adjust_tag(
                remaining_html_tag, line_to_parse, character_index
            )

            complete_parse_index: Optional[int] = 0
            if adjusted_remaining_html_tag in HtmlHelper.__html_block_6_start:
                html_block_type = HtmlHelper.html_block_6
            elif is_end_tag:
                is_complete, complete_parse_index = HtmlHelper.is_complete_html_end_tag(
                    adjusted_remaining_html_tag, line_to_parse, character_index
                )
                if is_complete:
                    html_block_type, character_index = (
                        HtmlHelper.html_block_7,
                        complete_parse_index,
                    )
            else:
                (
                    is_complete,
                    complete_parse_index,
                ) = HtmlHelper.is_complete_html_start_tag(
                    adjusted_remaining_html_tag, line_to_parse, character_index
                )
                if is_complete:
                    assert (
                        complete_parse_index is not None
                    ), "If is_complete is True, this must be set."
                    html_block_type, character_index = (
                        HtmlHelper.html_block_7,
                        complete_parse_index,
                    )
            if html_block_type == HtmlHelper.html_block_7:
                new_index, _ = ParserHelper.extract_ascii_whitespace(
                    line_to_parse, character_index
                )
                if new_index != line_to_parse_size:
                    html_block_type = None
        return html_block_type

    @staticmethod
    def __determine_html_block_type(
        token_stack: List[StackToken],
        line_to_parse: str,
        start_index: int,
        parse_properties: ParseBlockPassProperties,
    ) -> Tuple[Optional[str], Optional[str]]:
        """
        Determine the type of the html block that we are starting.
        """

        character_index = start_index + 1
        html_block_type = HtmlHelper.__check_for_special_html_blocks(
            line_to_parse, character_index
        )
        if html_block_type:
            remaining_html_tag = ""
        else:
            (
                new_character_index,
                new_remaining_html_tag,
            ) = ParserHelper.collect_until_one_of_characters_verified(
                line_to_parse, character_index, HtmlHelper.__html_tag_name_end
            )
            remaining_html_tag = new_remaining_html_tag
            character_index = new_character_index
            remaining_html_tag = remaining_html_tag.lower()

            html_block_type = HtmlHelper.__check_for_normal_html_blocks(
                remaining_html_tag, line_to_parse, character_index
            )

        POGGER.debug("html_block_type=$", html_block_type)
        if not html_block_type:
            return None, None
        if html_block_type == HtmlHelper.html_block_7 and token_stack[-1].is_paragraph:
            POGGER.debug("html_block_type 7 cannot interrupt a paragraph")
            return None, None
        if (
            parse_properties.is_disallow_raw_html_enabled
            and remaining_html_tag
            and parse_properties.disallow_raw_html
            and parse_properties.disallow_raw_html.is_html_tag_disallowed(
                remaining_html_tag
            )
        ):
            POGGER.debug("Tag name '%s' is disallowed.", remaining_html_tag)
            return None, None
        return html_block_type, remaining_html_tag

    # pylint: disable=too-many-arguments
    @staticmethod
    def is_html_block(
        line_to_parse: str,
        start_index: int,
        extracted_whitespace: str,
        token_stack: List[StackToken],
        parse_properties: ParseBlockPassProperties,
        skip_whitespace_check: bool = False,
    ) -> Tuple[Optional[str], Optional[str]]:
        """
        Determine if the current sequence of characters would start a html block element.
        """

        if (
            skip_whitespace_check
            or TabHelper.is_length_less_than_or_equal_to(extracted_whitespace, 3)
        ) and ParserHelper.is_character_at_index(
            line_to_parse,
            start_index,
            HtmlHelper.__html_block_start_character,
        ):
            return HtmlHelper.__determine_html_block_type(
                token_stack, line_to_parse, start_index, parse_properties
            )
        return None, None

    # pylint: enable=too-many-arguments

    @staticmethod
    def __handle_split_tab(
        parser_state: ParserState,
        position_marker: PositionMarker,
        original_line: str,
        orignal_line_end_prefix_index: int,
    ) -> Tuple[Optional[str], Optional[int]]:
        stack_token_index = len(parser_state.token_stack) - 1
        # assert stack_token_index > 0, "Must be a valid stack token."
        # Can omit check as splits only happen with containers, which guarantees one token.

        alternate_list_leading_space = None
        removed_chars_at_start: Optional[int] = None
        # while (
        #     stack_token_index > 0
        #     and not parser_state.token_stack[
        #         stack_token_index
        #     ].is_block_quote
        #     and not parser_state.token_stack[stack_token_index].is_list
        # ):
        #     stack_token_index -= 1
        if parser_state.token_stack[stack_token_index].is_list:
            orignal_line_prefix = original_line[:orignal_line_end_prefix_index]
            stop_index = -1
            if len(orignal_line_prefix) == 1:
                assert (
                    orignal_line_prefix == ParserHelper.tab_character
                ), "Prefix must be a single tab character."
                sdddd = TabHelper.detabify_string(orignal_line_prefix)
                assert (
                    len(sdddd) > position_marker.index_indent
                ), "String length must be larger than the indent."
                stop_index = 1
            else:
                end_index = 1
                keep_going = True
                while keep_going:
                    assert (
                        end_index < len(orignal_line_prefix) + 1
                    ), "End index not in range."
                    sample_slice = TabHelper.detabify_string(
                        orignal_line_prefix[:end_index]
                    )
                    if len(sample_slice) > position_marker.index_indent:
                        stop_index = end_index
                        keep_going = False
                    end_index += 1
                assert stop_index != -1, "Valid slice not found."

            original_prefix = original_line[: stop_index - 1]
            if stack_token_index <= 1:
                alternate_list_leading_space = original_prefix
            removed_chars_at_start = len(original_prefix)
        return alternate_list_leading_space, removed_chars_at_start

    # pylint: disable=too-many-arguments, too-many-locals
    @staticmethod
    def __found_html_block(
        parser_state: ParserState,
        position_marker: PositionMarker,
        new_tokens: List[MarkdownToken],
        original_line: str,
        extracted_whitespace: str,
        block_quote_data: BlockQuoteData,
        html_block_type: str,
        grab_bag: ContainerGrabBag,
    ) -> Tuple[List[MarkdownToken], bool, Optional[int], str]:
        split_tab = False
        alternate_list_leading_space: Optional[str] = None
        removed_chars_at_start: Optional[int] = None
        if ParserHelper.tab_character in original_line:
            token_text = position_marker.text_to_parse[position_marker.index_number :]
            # POGGER.debug("token_text=:$:", token_text)
            (
                _,
                split_tab,
                _,  # split_tab_with_block_quote_suffix,
                _,  # tabified_prefix,
                _,  # tabified_suffix,
                orignal_line_end_prefix_index,
            ) = TabHelper.parse_thematic_break_with_tab(
                original_line, token_text, extracted_whitespace
            )
            # POGGER.debug("split_tab=:$:", split_tab)
            if split_tab:
                (
                    alternate_list_leading_space,
                    removed_chars_at_start,
                ) = HtmlHelper.__handle_split_tab(
                    parser_state,
                    position_marker,
                    original_line,
                    orignal_line_end_prefix_index,
                )

        # POGGER.debug("did_adjust_block_quote=$", did_adjust_block_quote)
        # POGGER.debug("split_tab=$", split_tab)
        old_split_tab = split_tab
        did_adjust_block_quote = False
        split_tab, extracted_whitespace = ContainerHelper.reduce_containers_if_required(
            parser_state,
            position_marker,
            block_quote_data,
            new_tokens,
            split_tab,
            extracted_whitespace,
            grab_bag,
        )
        if split_tab:
            TabHelper.adjust_block_quote_indent_for_tab(
                parser_state,
                extracted_whitespace,
                alternate_list_leading_space,
                original_line=original_line,
            )
            did_adjust_block_quote = True
            POGGER.debug("did_adjust_block_quote=$", did_adjust_block_quote)
        POGGER.debug("split_tab=$", split_tab)
        did_adjust_block_quote = split_tab != old_split_tab or did_adjust_block_quote

        new_token = HtmlBlockMarkdownToken(position_marker, extracted_whitespace)
        new_tokens.append(new_token)
        parser_state.token_stack.append(HtmlBlockStackToken(html_block_type, new_token))
        return (
            new_tokens,
            did_adjust_block_quote,
            removed_chars_at_start,
            extracted_whitespace,
        )

    # pylint: enable=too-many-arguments, too-many-locals

    # pylint: disable=too-many-arguments
    @staticmethod
    def parse_html_block(
        parser_state: ParserState,
        position_marker: PositionMarker,
        extracted_whitespace: str,
        block_quote_data: BlockQuoteData,
        original_line: str,
        grab_bag: ContainerGrabBag,
    ) -> Tuple[List[MarkdownToken], bool, Optional[int], str]:
        """
        Determine if we have the criteria that we need to start an HTML block.
        """

        check_ws = LeafBlockHelper.realize_leading_whitespace(
            parser_state, position_marker, extracted_whitespace, original_line
        )
        html_block_type, _ = HtmlHelper.is_html_block(
            position_marker.text_to_parse,
            position_marker.index_number,
            check_ws,
            parser_state.token_stack,
            parser_state.parse_properties,
        )
        removed_chars_at_start = None
        did_adjust_block_quote = False
        POGGER.debug("did_adjust_block_quote=$", did_adjust_block_quote)
        if html_block_type:
            new_tokens, _ = parser_state.close_open_blocks_fn(
                parser_state,
                only_these_blocks=[ParagraphStackToken],
            )
            POGGER.debug("new_tokens=$", new_tokens)
            POGGER.debug("original_line=:$:", original_line)
            POGGER.debug("extracted_whitespace=:$:", extracted_whitespace)

            (
                new_tokens,
                did_adjust_block_quote,
                removed_chars_at_start,
                extracted_whitespace,
            ) = HtmlHelper.__found_html_block(
                parser_state,
                position_marker,
                new_tokens,
                original_line,
                extracted_whitespace,
                block_quote_data,
                html_block_type,
                grab_bag,
            )
        else:
            new_tokens = []
        POGGER.debug("did_adjust_block_quote=$", did_adjust_block_quote)
        return (
            new_tokens,
            did_adjust_block_quote,
            removed_chars_at_start,
            extracted_whitespace,
        )

    # pylint: enable=too-many-arguments

    @staticmethod
    def check_blank_html_block_end(parser_state: ParserState) -> List[MarkdownToken]:
        """
        Check to see if we have encountered the end of the current HTML block
        via an empty line or BLANK.
        """

        assert parser_state.token_stack[
            -1
        ].is_html_block, "Trailing token on stack must be HTML."
        html_token = cast(HtmlBlockStackToken, parser_state.token_stack[-1])
        if html_token.html_block_type in [
            HtmlHelper.html_block_6,
            HtmlHelper.html_block_7,
        ]:
            new_tokens, _ = parser_state.close_open_blocks_fn(
                parser_state,
                only_these_blocks=[HtmlBlockStackToken],
            )
            POGGER.debug("new_tokens=$", new_tokens)
        else:
            new_tokens = []

        return new_tokens

    @staticmethod
    def __check_normal_html_block_end_with_tab(
        parser_state: ParserState,
        original_line: str,
        extracted_whitespace: str,
        token_text: str,
        did_adjust_block_quote: bool,
    ) -> Tuple[str, str]:
        POGGER.debug("did_adjust_block_quote>:$:<", did_adjust_block_quote)
        POGGER.debug("original_line>:$:<", original_line)
        POGGER.debug("token_text>:$:<", token_text)
        POGGER.debug("extracted_whitespace>:$:<", extracted_whitespace)
        (
            tabified_text,
            split_tab,
            split_tab_with_block_quote_suffix,
            _,
            tabified_whitespace,
            _,
        ) = TabHelper.parse_thematic_break_with_tab(
            original_line, token_text, extracted_whitespace
        )

        POGGER.debug("tabified_text>:$:<", tabified_text)
        POGGER.debug("split_tab>:$:<", split_tab)
        POGGER.debug(
            "split_tab_with_block_quote_suffix>:$:<", split_tab_with_block_quote_suffix
        )
        POGGER.debug("tabified_whitespace>:$:<", tabified_whitespace)

        stack_token_index = len(parser_state.token_stack) - 1
        while (
            stack_token_index > 0
            and not parser_state.token_stack[stack_token_index].is_block_quote
            and not parser_state.token_stack[stack_token_index].is_list
        ):
            stack_token_index -= 1

        if (
            split_tab
            and stack_token_index != 0
            and parser_state.token_stack[stack_token_index].is_block_quote
        ):
            POGGER.debug("extracted_whitespace>:$:<", extracted_whitespace)
            tabified_whitespace = ParserHelper.create_replacement_markers(
                tabified_whitespace, extracted_whitespace
            )
            POGGER.debug("tabified_whitespace>:$:<", tabified_whitespace)
            if not did_adjust_block_quote:
                TabHelper.adjust_block_quote_indent_for_tab(parser_state)
        return tabified_whitespace, tabified_text

    @staticmethod
    def __handle_disallow(parser_state: ParserState, token_text: str) -> str:
        cleaned_up_text_parts: List[str] = []
        new_index, new_index_text = ParserHelper.collect_until_character_verified(
            token_text, 0, HtmlHelper.__html_block_start_character
        )
        x_index: int = new_index
        while x_index < len(token_text):
            cleaned_up_text_parts.append(new_index_text)
            (
                after_text_index,
                collected_text,
            ) = ParserHelper.collect_until_one_of_characters_verified(
                token_text, new_index + 1, " /<>"
            )
            if (
                after_text_index + 1 < len(token_text)
                and token_text[after_text_index] == "<"
            ):
                cleaned_up_text_parts.append(f"<{collected_text}")
                new_index, new_index_text = (
                    ParserHelper.collect_until_character_verified(
                        token_text,
                        after_text_index,
                        HtmlHelper.__html_block_start_character,
                    )
                )
                continue
            assert (
                parser_state.parse_properties is not None
                and parser_state.parse_properties.disallow_raw_html is not None
            ), "Disallow raw html extension must be defined by this point."
            tag_start = (
                ParserHelper.create_replacement_markers(
                    HtmlHelper.__html_block_start_character, "&lt;"
                )
                if parser_state.parse_properties.disallow_raw_html.is_html_tag_disallowed(
                    collected_text
                )
                else HtmlHelper.__html_block_start_character
            )
            cleaned_up_text_parts.append(tag_start + collected_text)
            new_index, new_index_text = ParserHelper.collect_until_character_verified(
                token_text,
                after_text_index,
                HtmlHelper.__html_block_start_character,
            )
            x_index = new_index
        cleaned_up_text_parts.append(new_index_text)
        return "".join(cleaned_up_text_parts)

    # pylint: disable=too-many-arguments
    @staticmethod
    def check_normal_html_block_end(
        parser_state: ParserState,
        line_to_parse: str,
        start_index: int,
        extracted_whitespace: str,
        position_marker: PositionMarker,
        original_line: str,
        did_adjust_block_quote: bool,
    ) -> List[MarkdownToken]:
        """
        Check to see if we have encountered the end of the current HTML block
        via text on a normal line.
        """

        token_text = line_to_parse[start_index:]
        # POGGER.debug("extracted_whitespace=:$:", extracted_whitespace)
        # POGGER.debug("token_text=:$:", token_text)
        # POGGER.debug("original_line=:$:", original_line)
        if ParserHelper.tab_character in original_line:
            (
                extracted_whitespace,
                token_text,
            ) = HtmlHelper.__check_normal_html_block_end_with_tab(
                parser_state,
                original_line,
                extracted_whitespace,
                token_text,
                did_adjust_block_quote,
            )

        if parser_state.parse_properties.is_disallow_raw_html_enabled:
            token_text = HtmlHelper.__handle_disallow(parser_state, token_text)

        new_tokens: List[MarkdownToken] = [
            TextMarkdownToken(
                token_text,
                extracted_whitespace,
                position_marker=position_marker,
            )
        ]

        is_block_terminated, adj_line = False, line_to_parse[start_index:]
        assert parser_state.token_stack[
            -1
        ].is_html_block, "Trailing token must be HTML token."
        html_token = cast(HtmlBlockStackToken, parser_state.token_stack[-1])
        if html_token.html_block_type == HtmlHelper.html_block_1:
            for next_end_tag in HtmlHelper.__html_block_1_end_tags:
                if next_end_tag in adj_line:
                    is_block_terminated = True
        elif html_token.html_block_type == HtmlHelper.html_block_2:
            is_block_terminated = HtmlHelper.__html_block_2_end in adj_line
        elif html_token.html_block_type == HtmlHelper.html_block_3:
            is_block_terminated = HtmlHelper.__html_block_3_end in adj_line
        elif html_token.html_block_type == HtmlHelper.html_block_4:
            is_block_terminated = HtmlHelper.__html_block_4_end in adj_line
        elif html_token.html_block_type == HtmlHelper.html_block_5:
            is_block_terminated = HtmlHelper.__html_block_5_end in adj_line

        if is_block_terminated:
            terminated_block_tokens, _ = parser_state.close_open_blocks_fn(
                parser_state,
                only_these_blocks=[HtmlBlockStackToken],
            )
            # POGGER.debug("terminated_block_tokens=$", terminated_block_tokens)
            assert terminated_block_tokens, "At least one token must be produced."
            new_tokens.extend(terminated_block_tokens)
        return new_tokens

    # pylint: enable=too-many-arguments
