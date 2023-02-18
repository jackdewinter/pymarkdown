"""
Link helper
"""
import logging
import urllib
import urllib.parse
from typing import Callable, Dict, List, Optional, Tuple, cast

from pymarkdown.constants import Constants
from pymarkdown.emphasis_helper import EmphasisHelper
from pymarkdown.inline_helper import InlineHelper
from pymarkdown.inline_markdown_token import (
    EmailAutolinkMarkdownToken,
    HardBreakMarkdownToken,
    ImageStartMarkdownToken,
    InlineCodeSpanMarkdownToken,
    LinkStartMarkdownToken,
    RawHtmlMarkdownToken,
    ReferenceMarkdownToken,
    SpecialTextMarkdownToken,
    TextMarkdownToken,
)
from pymarkdown.inline_request import InlineRequest
from pymarkdown.link_reference_titles import LinkReferenceTitles
from pymarkdown.markdown_token import MarkdownToken
from pymarkdown.parser_helper import ParserHelper
from pymarkdown.parser_logger import ParserLogger

POGGER = ParserLogger(logging.getLogger(__name__))


# pylint: disable=too-many-lines
class LinkHelper:
    """
    Class to helper with the parsing of links.
    """

    __link_definitions: Dict[str, LinkReferenceTitles] = {}
    __link_safe_characters = "/#:?=()*!$'+,;@"

    __special_link_destination_characters = "%&"

    __non_angle_link_nest = "("
    __non_angle_link_unnest = ")"
    __non_angle_link_breaks = f"{Constants.ascii_control_characters}()\\"

    link_label_start = "["
    link_label_end = "]"
    __link_label_is_definition_character = ":"
    __link_label_breaks = (
        f"{link_label_start}{link_label_end}{InlineHelper.backslash_character}"
    )

    __angle_link_start = "<"
    __angle_link_end = ">"
    __angle_link_destination_breaks = (
        f"{__angle_link_end}{InlineHelper.backslash_character}"
    )

    __link_title_single = "'"
    __link_title_double = '"'
    __link_title_parenthesis_open = "("
    __link_title_parenthesis_close = ")"

    __link_format_inline_start = "("
    __link_format_inline_end = ")"
    __link_format_reference_start = "["
    __link_format_reference_end = "]"

    __link_start_sequence = "["
    image_start_sequence = "!["
    __valid_link_starts = [__link_start_sequence, image_start_sequence]

    @staticmethod
    def initialize() -> None:
        """
        Initialize the inline subsystem.
        """
        LinkHelper.__link_definitions = {}

    @staticmethod
    def add_link_definition(link_name: str, link_value: LinkReferenceTitles) -> bool:
        """
        Add a link definition to the cache of links.
        """
        POGGER.debug(
            ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>$",
            LinkHelper.__link_definitions,
        )
        POGGER.debug(
            ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>$:$",
            link_name,
            link_value,
        )
        did_add_definition = link_name not in LinkHelper.__link_definitions
        if did_add_definition:
            LinkHelper.__link_definitions[link_name] = link_value
            POGGER.debug(">>added def>>$-->$", link_name, link_value)
        return did_add_definition

    @staticmethod
    def extract_link_label(
        line_to_parse: str, new_index: int, include_reference_colon: bool = True
    ) -> Tuple[bool, int, Optional[str]]:
        """
        Extract the link reference definition's link label.
        """
        label_parts: List[str] = []

        while True:
            newer_index, ert_new = ParserHelper.collect_until_one_of_characters(
                line_to_parse, new_index, LinkHelper.__link_label_breaks
            )
            assert newer_index is not None
            assert ert_new is not None
            new_index = newer_index
            label_parts.append(ert_new)
            if ParserHelper.is_character_at_index(
                line_to_parse, new_index, InlineHelper.backslash_character
            ):
                old_new_index = new_index
                inline_response = InlineHelper.handle_inline_backslash(
                    InlineRequest(line_to_parse, new_index)
                )
                assert inline_response.new_index is not None
                new_index = inline_response.new_index
                label_parts.append(line_to_parse[old_new_index:new_index])
            elif ParserHelper.is_character_at_index(
                line_to_parse, new_index, LinkHelper.link_label_start
            ):
                POGGER.debug(">> unescaped [, bailing")
                return False, -1, None
            else:
                break  # pragma: no cover

        POGGER.debug("look for ]>>$<<", line_to_parse[new_index:])
        if not ParserHelper.is_character_at_index(
            line_to_parse, new_index, LinkHelper.link_label_end
        ):
            POGGER.debug(">> no end ], bailing")
            return False, new_index, None
        new_index += 1

        if include_reference_colon:
            POGGER.debug(
                "look for :>>$<<",
                line_to_parse[new_index:],
            )
            if not ParserHelper.is_character_at_index(
                line_to_parse,
                new_index,
                LinkHelper.__link_label_is_definition_character,
            ):
                POGGER.debug(">> no :, bailing")
                return False, -1, None
            new_index += 1

        return True, new_index, "".join(label_parts)

    @staticmethod
    def extract_link_title(
        line_to_parse: str, new_index: Optional[int], is_blank_line: bool
    ) -> Tuple[
        bool, Optional[int], Optional[str], Optional[str], Optional[str], Optional[str]
    ]:
        """
        Extract the link reference definition's optional link title.
        """
        POGGER.debug("before ws>>$>", line_to_parse[new_index:])
        assert new_index is not None
        new_index, ex_ws = ParserHelper.extract_ascii_whitespace(
            line_to_parse, new_index
        )
        assert new_index is not None
        POGGER.debug(
            "after ws>>$>ex_ws>$",
            line_to_parse[new_index:],
            ex_ws,
        )
        start_index, line_to_parse_size = new_index, len(line_to_parse)
        if new_index == line_to_parse_size and not is_blank_line:
            return False, new_index, None, None, None, None
        if ex_ws and new_index < line_to_parse_size:
            (
                inline_title,
                pre_inline_title,
                new_index,
                _,
            ) = LinkHelper.__parse_link_title(line_to_parse, new_index)
            if new_index == -1 or inline_title is None:
                return False, new_index, None, None, None, None
        else:
            inline_title, pre_inline_title = "", ""
        return (
            True,
            new_index,
            inline_title,
            pre_inline_title,
            ex_ws,
            line_to_parse[start_index:new_index],
        )

    @staticmethod
    def extract_link_destination(
        line_to_parse: str, start_index: int, is_blank_line: bool
    ) -> Tuple[
        bool, Optional[int], Optional[str], Optional[str], Optional[str], Optional[str]
    ]:
        """
        Extract the link reference definition's link destination.
        """
        after_whitespace_index: Optional[int] = None
        (
            after_whitespace_index,
            prefix_whitespace,
        ) = ParserHelper.collect_while_one_of_characters(
            line_to_parse, start_index, Constants.ascii_whitespace
        )
        assert after_whitespace_index is not None
        if after_whitespace_index == len(line_to_parse) and not is_blank_line:
            return False, after_whitespace_index, None, None, None, None

        assert prefix_whitespace is not None
        POGGER.debug(
            "Pre-LD>>$<<", ParserHelper.make_whitespace_visible(prefix_whitespace)
        )
        POGGER.debug("LD>>$<<", line_to_parse[after_whitespace_index:])
        (
            inline_link,
            pre_inline_link,
            after_whitespace_index,
            inline_raw_link,
            _,
        ) = LinkHelper.__parse_link_destination(line_to_parse, after_whitespace_index)
        if after_whitespace_index == -1:
            return False, -1, None, None, None, None
        return (
            True,
            after_whitespace_index,
            inline_link,
            pre_inline_link,
            prefix_whitespace,
            inline_raw_link,
        )

    @staticmethod
    def normalize_link_label(link_label: str) -> str:
        """
        Translate a link label into a normalized form to use for comparisons.
        """

        # Fold all whitespace characters (except for space) into a space character
        link_label = ParserHelper.replace_any_of(
            link_label,
            Constants.non_space_ascii_whitespace,
            ParserHelper.space_character,
        )

        # Fold multiple spaces into a single space character.
        link_label = ParserHelper.space_character.join(link_label.split())

        # Fold the case of any characters to their lower equivalent.
        return link_label.casefold().strip()

    # pylint: disable=too-many-arguments, too-many-locals
    @staticmethod
    def look_for_link_or_image(
        inline_blocks: List[MarkdownToken],
        source_text: str,
        next_index: int,
        remaining_line: str,
        tabified_remaining_line: Optional[str],
        current_string_unresolved: str,
        xx_fn: Callable[[str], str],
        tabified_text: Optional[str],
    ) -> Tuple[int, bool, Optional[MarkdownToken], bool]:
        """
        Given that a link close character has been found, process it to see if
        there is actually enough other text to properly construct the link.
        """

        POGGER.debug(
            ">>look_for_link_or_image>>$<<",
            inline_blocks,
        )
        POGGER.debug(">>source_text>>$<<", source_text)
        POGGER.debug(">>tabified_text>>$<<", tabified_text)
        POGGER.debug(">>next_index>>$<<", next_index)
        POGGER.debug(">>remaining_line>>$<<", remaining_line)
        POGGER.debug(">>tabified_remaining_line>>$<<", tabified_remaining_line)
        POGGER.debug(
            ">>current_string_unresolved>>$<<",
            current_string_unresolved,
        )
        is_valid, consume_rest_of_line, new_index, updated_index = (
            False,
            False,
            next_index + 1,
            -1,
        )
        token_to_append: Optional[MarkdownToken] = None

        POGGER.debug("LOOKING FOR START")
        LinkHelper.__debug_log_specials_in_tokens(inline_blocks)

        valid_special_start_text, search_index = None, len(inline_blocks) - 1
        while search_index >= 0:
            if inline_blocks[search_index].is_special_text:
                (
                    is_done,
                    is_valid,
                    updated_index,
                    token_to_append,
                    consume_rest_of_line,
                    valid_special_start_text,
                ) = LinkHelper.__find_link(
                    inline_blocks,
                    search_index,
                    source_text,
                    new_index,
                    remaining_line,
                    tabified_remaining_line,
                    current_string_unresolved,
                    xx_fn,
                    updated_index,
                    tabified_text,
                )
                if is_done:
                    break
                POGGER.debug("  not link")
            search_index -= 1

        POGGER.debug(
            ">>look_for_link_or_image>>$<<is_valid<<$<<$<<",
            inline_blocks,
            is_valid,
            consume_rest_of_line,
        )
        if is_valid:
            assert valid_special_start_text is not None
            LinkHelper.__deactivate_used_tokens(
                inline_blocks, search_index, valid_special_start_text
            )
            return updated_index, True, token_to_append, consume_rest_of_line
        return new_index, False, token_to_append, consume_rest_of_line

    # pylint: enable=too-many-arguments, too-many-locals

    @staticmethod
    def __deactivate_used_tokens(
        inline_blocks: List[MarkdownToken],
        search_index: int,
        valid_special_start_text: str,
    ) -> None:
        # if link set all [ before to inactive
        POGGER.debug("")
        POGGER.debug("SET TO INACTIVE-->$", valid_special_start_text)
        POGGER.debug("ind-->$", search_index)

        assert (
            inline_blocks[search_index].is_inline_link
            or inline_blocks[search_index].is_inline_image
        )

        POGGER.debug(
            "\nresolve_inline_emphasis>>$",
            inline_blocks,
        )
        EmphasisHelper.resolve_inline_emphasis(
            inline_blocks, inline_blocks[search_index]
        )
        POGGER.debug(
            "resolve_inline_emphasis>>$\n",
            inline_blocks,
        )

        if valid_special_start_text == LinkHelper.__link_start_sequence:
            POGGER.debug("DEACTIVATING")
            LinkHelper.__debug_log_specials_in_tokens(inline_blocks)
            for deactivate_token in inline_blocks:
                if deactivate_token.is_special_text:
                    special_token = cast(SpecialTextMarkdownToken, deactivate_token)
                    POGGER.debug("inline_blocks>>>>>>>>>>>>>>>>>>$", special_token)
                    if special_token.token_text == LinkHelper.__link_start_sequence:
                        special_token.deactivate()
            POGGER.debug("DEACTIVATED")
            LinkHelper.__debug_log_specials_in_tokens(inline_blocks)

    # pylint: disable=too-many-arguments, too-many-locals
    @staticmethod
    def __find_link(
        inline_blocks: List[MarkdownToken],
        search_index: int,
        source_text: str,
        new_index: int,
        remaining_line: str,
        tabified_remaining_line: Optional[str],
        current_string_unresolved: str,
        xx_fn: Callable[[str], str],
        updated_index: int,
        tabified_text: Optional[str],
    ) -> Tuple[bool, bool, int, Optional[MarkdownToken], bool, Optional[str]]:
        special_text_token = cast(SpecialTextMarkdownToken, inline_blocks[search_index])
        # POGGER.debug(
        #     "search_index>>$>>$",
        #     search_index,
        #     special_text_token.show_process_emphasis(),
        # )

        (
            is_done,
            consume_rest_of_line,
            is_valid,
        ) = (False, False, False)
        token_to_append: Optional[MarkdownToken] = None
        if special_text_token.token_text in LinkHelper.__valid_link_starts:
            valid_special_start_text: Optional[str] = special_text_token.token_text
            if special_text_token.is_active:
                # POGGER.debug(">>>>>>$", inline_blocks)
                assert valid_special_start_text is not None
                (
                    updated_index,
                    token_to_append,
                    consume_rest_of_line,
                ) = LinkHelper.__handle_link_types(
                    inline_blocks,
                    search_index,
                    source_text,
                    new_index,
                    valid_special_start_text,
                    remaining_line,
                    tabified_remaining_line,
                    current_string_unresolved,
                    xx_fn,
                    tabified_text,
                )
                if updated_index != -1:
                    is_valid, is_done = True, True

            if not is_done:
                # POGGER.debug("  not active:$", search_index)
                LinkHelper.__revert_token_to_normal_text_token(
                    inline_blocks, search_index
                )
                is_done = True
        else:
            valid_special_start_text = None
        return (
            is_done,
            is_valid,
            updated_index,
            token_to_append,
            consume_rest_of_line,
            valid_special_start_text,
        )

    # pylint: enable=too-many-arguments, too-many-locals

    @staticmethod
    def __revert_token_to_normal_text_token(
        inline_blocks: List[MarkdownToken], search_index: int
    ) -> None:
        """
        Revert this token from a special text token back to a normal text token.
        """

        POGGER.debug("REVERTING")
        LinkHelper.__debug_log_specials_in_tokens(inline_blocks)

        text_token_to_replace = cast(
            SpecialTextMarkdownToken, inline_blocks[search_index]
        )
        inline_blocks.insert(search_index, text_token_to_replace.create_copy())
        del inline_blocks[search_index + 1]

        POGGER.debug("REVERTED")
        LinkHelper.__debug_log_specials_in_tokens(inline_blocks)

    @staticmethod
    def __debug_log_specials_in_tokens(inline_blocks: List[MarkdownToken]) -> None:
        display_parts = []
        for deactivate_token in inline_blocks:
            if deactivate_token.is_special_text:
                special_token = cast(SpecialTextMarkdownToken, deactivate_token)
                display_parts.extend(
                    [
                        f",>>Spec:{special_token.is_active}:{deactivate_token}<<",
                    ]
                )
            else:
                display_parts.extend([",", str(deactivate_token)])

        POGGER.debug("$", "".join(display_parts)[1:])

    @staticmethod
    def __consume_text_for_image_alt_text(
        inline_blocks: List[MarkdownToken],
        ind: int,
        remaining_line: str,
        text_from_blocks_raw: str,
        xx_fn: Callable[[str], str],
    ) -> Tuple[str, str]:
        """
        Consume text from the inline blocks to use as part of the image's alt text.
        """

        inline_blocks_size, ind_plus_one = len(inline_blocks), ind + 1

        POGGER.debug("inline_blocks_size>>$<<", inline_blocks_size)
        POGGER.debug("ind>>$<<", ind)
        POGGER.debug(">>$<<", inline_blocks[ind_plus_one:])
        if inline_blocks_size > (ind_plus_one):

            alt_text_parts: List[str] = []

            while inline_blocks_size > ind_plus_one:

                LinkHelper.__handle_next_alt_text(
                    inline_blocks, ind_plus_one, alt_text_parts
                )

                del inline_blocks[ind_plus_one]
                inline_blocks_size -= 1

            alt_text_parts.append(remaining_line)
            image_alt_text = "".join(alt_text_parts)
            POGGER.debug(">>after>>$>>", image_alt_text)
        else:
            POGGER.debug(">>composing>>$>>", text_from_blocks_raw)
            image_alt_text = xx_fn(text_from_blocks_raw)
            image_alt_text = ParserHelper.resolve_all_from_text(image_alt_text)
            image_alt_text = InlineHelper.append_text(
                "", image_alt_text, add_text_signature=False
            )
            POGGER.debug(">>composed>>$>>", image_alt_text)

        POGGER.debug(">>image_alt_text>>$>>", image_alt_text)
        POGGER.debug(">>text_from_blocks_raw>>$>>", text_from_blocks_raw)
        return image_alt_text, text_from_blocks_raw

    @staticmethod
    def __handle_next_alt_text_special_text(
        next_token: MarkdownToken, alt_text_parts: List[str]
    ) -> None:
        text_token = cast(TextMarkdownToken, (next_token))
        if text_token.token_text == "]":
            alt_text_parts.append(text_token.token_text)

    @staticmethod
    def __handle_next_alt_text_normal_text(
        next_token: MarkdownToken, alt_text_parts: List[str]
    ) -> None:
        text_token = cast(TextMarkdownToken, next_token)
        alt_text_parts.append(ParserHelper.resolve_all_from_text(text_token.token_text))

    @staticmethod
    def __handle_next_alt_text_raw_html(
        next_token: MarkdownToken, alt_text_parts: List[str]
    ) -> None:
        rawhtml_token = cast(RawHtmlMarkdownToken, next_token)
        alt_text_parts.extend(["<", rawhtml_token.raw_tag, ">"])

    @staticmethod
    def __handle_next_alt_text_code_span(
        next_token: MarkdownToken, alt_text_parts: List[str]
    ) -> None:
        codespan_token = cast(InlineCodeSpanMarkdownToken, next_token)
        alt_text_parts.append(
            ParserHelper.resolve_all_from_text(codespan_token.span_text)
        )

    @staticmethod
    def __handle_next_alt_text_auto_link(
        next_token: MarkdownToken, alt_text_parts: List[str]
    ) -> None:
        autolink_token = cast(EmailAutolinkMarkdownToken, next_token)
        alt_text_parts.append(
            ParserHelper.resolve_all_from_text(autolink_token.autolink_text)
        )

    @staticmethod
    def __handle_next_alt_text_hard_break(
        next_token: MarkdownToken, alt_text_parts: List[str]
    ) -> None:
        _ = next_token
        alt_text_parts.append(ParserHelper.newline_character)

    @staticmethod
    def __handle_next_alt_text_else(
        next_token: MarkdownToken, alt_text_parts: List[str]
    ) -> None:
        assert (
            next_token.is_inline_image
        ), f"Not handled: {ParserHelper.make_value_visible(next_token)}"
        image_token = cast(ImageStartMarkdownToken, next_token)
        alt_text_parts.append(image_token.image_alt_text)

    @staticmethod
    def __handle_next_alt_text(
        inline_blocks: List[MarkdownToken], ind_plus_one: int, alt_text_parts: List[str]
    ) -> None:
        if inline_blocks[ind_plus_one].is_special_text:
            LinkHelper.__handle_next_alt_text_special_text(
                inline_blocks[ind_plus_one], alt_text_parts
            )
        elif inline_blocks[ind_plus_one].is_text:
            LinkHelper.__handle_next_alt_text_normal_text(
                inline_blocks[ind_plus_one], alt_text_parts
            )
        elif inline_blocks[ind_plus_one].is_inline_raw_html:
            LinkHelper.__handle_next_alt_text_raw_html(
                inline_blocks[ind_plus_one], alt_text_parts
            )
        elif inline_blocks[ind_plus_one].is_inline_code_span:
            LinkHelper.__handle_next_alt_text_code_span(
                inline_blocks[ind_plus_one], alt_text_parts
            )
        elif inline_blocks[ind_plus_one].is_inline_autolink:
            LinkHelper.__handle_next_alt_text_auto_link(
                inline_blocks[ind_plus_one], alt_text_parts
            )
        elif (
            inline_blocks[ind_plus_one].is_inline_link
            or inline_blocks[ind_plus_one].is_inline_link_end
            or inline_blocks[ind_plus_one].is_inline_emphasis
            or inline_blocks[ind_plus_one].is_inline_emphasis_end
        ):
            pass
        elif inline_blocks[ind_plus_one].is_inline_hard_break:
            LinkHelper.__handle_next_alt_text_hard_break(
                inline_blocks[ind_plus_one], alt_text_parts
            )
        else:
            LinkHelper.__handle_next_alt_text_else(
                inline_blocks[ind_plus_one], alt_text_parts
            )

    @staticmethod
    def __collect_text_from_blocks(
        inline_blocks: List[MarkdownToken], ind: int, suffix_text: str
    ) -> Tuple[str, str]:
        """
        Aggregate the text component of text blocks.
        """

        # POGGER.debug(
        #     ">>collect_text_from_blocks>>$",
        #     inline_blocks,
        # )
        POGGER.debug(
            ">>collect_text_from_blocks>>suffix_text>>$",
            suffix_text,
        )

        (
            collect_index,
            is_inside_of_link,
            inline_blocks_size,
        ) = (ind + 1, False, len(inline_blocks))
        text_parts: List[str] = []
        text_raw_parts: List[str] = []
        POGGER.debug(
            ">>collect_index:$: < inline_blocks_size:$:",
            collect_index,
            inline_blocks_size,
        )
        while collect_index < inline_blocks_size:

            (
                is_inside_of_link,
                collect_index,
            ) = LinkHelper.__collect_text_from_next_block(
                inline_blocks,
                inline_blocks_size,
                collect_index,
                text_raw_parts,
                text_parts,
                is_inside_of_link,
            )

        text_parts.append(suffix_text)
        text_raw_parts.append(suffix_text)

        text_from_blocks = "".join(text_parts)
        POGGER.debug(">>text_from_blocks>:$:<", text_from_blocks)
        text_from_blocks = ParserHelper.resolve_backspaces_from_text(text_from_blocks)
        POGGER.debug(">>text_from_blocks>:$:<", text_from_blocks)
        POGGER.debug(">>text_raw_parts>:$:<", text_raw_parts)
        return text_from_blocks, "".join(text_raw_parts)

    # pylint: disable=too-many-arguments
    @staticmethod
    def __collect_text_from_next_block(
        inline_blocks: List[MarkdownToken],
        inline_blocks_size: int,
        collect_index: int,
        text_raw_parts: List[str],
        text_parts: List[str],
        is_inside_of_link: bool,
    ) -> Tuple[bool, int]:
        POGGER.debug(">>collect_text>>$<<", inline_blocks[collect_index])
        if inline_blocks[collect_index].is_inline_link_end:
            is_inside_of_link = LinkHelper.__collect_text_from_inline_link_end()
        elif inline_blocks[collect_index].is_inline_link:
            is_inside_of_link = LinkHelper.__collect_text_from_inline_link_start(
                inline_blocks, collect_index, text_raw_parts
            )
        elif inline_blocks[collect_index].is_inline_image:
            LinkHelper.__collect_text_from_inline_image(
                inline_blocks, collect_index, text_raw_parts, text_parts
            )
        elif inline_blocks[collect_index].is_inline_code_span:
            LinkHelper.__collect_text_from_inline_code_span(
                inline_blocks,
                collect_index,
                text_raw_parts,
                text_parts,
                is_inside_of_link,
            )
        elif inline_blocks[collect_index].is_inline_raw_html:
            LinkHelper.__collect_text_from_inline_raw_html(
                inline_blocks,
                collect_index,
                text_raw_parts,
                text_parts,
                is_inside_of_link,
            )
        elif inline_blocks[collect_index].is_inline_autolink:
            LinkHelper.__collect_text_from_inline_autolink(
                inline_blocks,
                collect_index,
                text_raw_parts,
                text_parts,
                is_inside_of_link,
            )
        elif inline_blocks[collect_index].is_inline_hard_break:
            LinkHelper.__collect_text_from_inline_hard_break(
                inline_blocks, collect_index, text_raw_parts, text_parts
            )
        elif not is_inside_of_link:
            LinkHelper.__collect_text_from_text(
                inline_blocks, collect_index, text_raw_parts, text_parts
            )
        POGGER.debug(">>collect_text>>$<<$<<", text_parts, inline_blocks[collect_index])
        POGGER.debug(">>collected_text_raw>>$<<", text_raw_parts)
        collect_index += 1
        POGGER.debug(
            ">>collect_index:$: < inline_blocks_size:$:",
            collect_index,
            inline_blocks_size,
        )
        return is_inside_of_link, collect_index

    # pylint: enable=too-many-arguments

    @staticmethod
    def __collect_text_from_inline_link_end() -> bool:
        return False

    @staticmethod
    def __collect_text_from_inline_link_start(
        inline_blocks: List[MarkdownToken],
        collect_index: int,
        text_raw_parts: List[str],
    ) -> bool:
        link_token = cast(LinkStartMarkdownToken, inline_blocks[collect_index])
        raw_text = LinkHelper.rehydrate_inline_link_text_from_token(link_token)
        text_raw_parts.append(raw_text)
        return True

    @staticmethod
    def __collect_text_from_inline_image(
        inline_blocks: List[MarkdownToken],
        collect_index: int,
        text_raw_parts: List[str],
        text_parts: List[str],
    ) -> None:
        image_token = cast(ImageStartMarkdownToken, inline_blocks[collect_index])
        text_raw_parts.append(
            LinkHelper.rehydrate_inline_image_text_from_token(image_token)
        )
        text_parts.append(image_token.image_alt_text)

    @staticmethod
    def __collect_text_from_inline_code_span(
        inline_blocks: List[MarkdownToken],
        collect_index: int,
        text_raw_parts: List[str],
        text_parts: List[str],
        is_inside_of_link: bool,
    ) -> None:
        if not is_inside_of_link:
            codespan_token = cast(
                InlineCodeSpanMarkdownToken, inline_blocks[collect_index]
            )
            POGGER.debug("CODESPAN>>$<<", codespan_token)
            sub_parts = [
                codespan_token.extracted_start_backticks,
                ParserHelper.remove_all_from_text(codespan_token.leading_whitespace),
                ParserHelper.remove_all_from_text(codespan_token.span_text),
                ParserHelper.remove_all_from_text(codespan_token.trailing_whitespace),
                codespan_token.extracted_start_backticks,
            ]
            text_parts.extend(sub_parts)
            text_raw_parts.extend(sub_parts)

    @staticmethod
    def __collect_text_from_inline_raw_html(
        inline_blocks: List[MarkdownToken],
        collect_index: int,
        text_raw_parts: List[str],
        text_parts: List[str],
        is_inside_of_link: bool,
    ) -> None:
        if not is_inside_of_link:
            html_token = cast(RawHtmlMarkdownToken, inline_blocks[collect_index])
            sub_parts = ["<", html_token.raw_tag, ">"]
            text_parts.extend(sub_parts)
            text_raw_parts.extend(sub_parts)

    @staticmethod
    def __collect_text_from_inline_autolink(
        inline_blocks: List[MarkdownToken],
        collect_index: int,
        text_raw_parts: List[str],
        text_parts: List[str],
        is_inside_of_link: bool,
    ) -> None:
        if not is_inside_of_link:
            autolink_token = cast(
                EmailAutolinkMarkdownToken, inline_blocks[collect_index]
            )
            sub_parts = ["<", autolink_token.autolink_text, ">"]
            text_parts.extend(sub_parts)
            text_raw_parts.extend(sub_parts)

    @staticmethod
    def __collect_text_from_inline_hard_break(
        inline_blocks: List[MarkdownToken],
        collect_index: int,
        text_raw_parts: List[str],
        text_parts: List[str],
    ) -> None:
        break_token = cast(HardBreakMarkdownToken, inline_blocks[collect_index])
        POGGER.debug("is_inline_hard_break>>collected_text_raw>>$<<", text_raw_parts)
        converted_text = break_token.line_end
        text_parts.append(converted_text)
        if converted_text == "\\":
            text_parts.append(converted_text)
        text_parts.append(ParserHelper.newline_character)
        text_raw_parts.extend((converted_text, ParserHelper.newline_character))
        POGGER.debug("is_inline_hard_break>>collected_text_raw>>$<<", text_raw_parts)

    @staticmethod
    def __collect_text_from_text(
        inline_blocks: List[MarkdownToken],
        collect_index: int,
        text_raw_parts: List[str],
        text_parts: List[str],
    ) -> None:
        text_token = cast(TextMarkdownToken, inline_blocks[collect_index])
        text_parts.append(text_token.token_text)
        text_raw_parts.append(text_token.token_text)

    @staticmethod
    def __parse_angle_link_destination(
        source_text: str, new_index: int
    ) -> Tuple[int, str]:
        """
        Parse a link destination that is included in angle brackets.
        """

        destination_parts: List[str] = []
        newer_index: Optional[int] = new_index + 1
        while True:
            assert newer_index is not None
            newer_index, ert_new = ParserHelper.collect_until_one_of_characters(
                source_text, newer_index, LinkHelper.__angle_link_destination_breaks
            )
            assert newer_index is not None
            assert ert_new is not None
            destination_parts.append(ert_new)

            if not ParserHelper.is_character_at_index(
                source_text, newer_index, InlineHelper.backslash_character
            ):
                break

            old_new_index = newer_index
            inline_request = InlineRequest(source_text, newer_index)
            inline_response = InlineHelper.handle_inline_backslash(inline_request)
            newer_index = inline_response.new_index
            destination_parts.append(source_text[old_new_index:newer_index])
        if ParserHelper.is_character_at_index(
            source_text, newer_index, LinkHelper.__angle_link_end
        ):
            newer_index += 1
        else:
            newer_index = -1
            destination_parts.clear()
        return newer_index, "".join(destination_parts)

    @staticmethod
    def __parse_non_angle_link_destination(
        source_text: str, new_index: int
    ) -> Tuple[Optional[int], Optional[str]]:
        """
        Parse a link destination that is not included in angle brackets.
        """

        destination_parts: List[str] = []
        keep_collecting, nesting_level = True, 0
        newer_index: Optional[int] = new_index
        while keep_collecting:
            assert newer_index is not None
            POGGER.debug(
                "collected_destination>>$<<source_text<<$>>nesting_level>>$>>",
                destination_parts,
                source_text[newer_index:],
                nesting_level,
            )
            newer_index, before_part = ParserHelper.collect_until_one_of_characters(
                source_text, newer_index, LinkHelper.__non_angle_link_breaks
            )
            assert newer_index is not None
            assert before_part is not None
            destination_parts.append(before_part)
            POGGER.debug(">>>>>>$<<<<<", source_text[newer_index:])
            if ParserHelper.is_character_at_index(
                source_text, newer_index, InlineHelper.backslash_character
            ):
                POGGER.debug("backslash")
                old_new_index = newer_index
                inline_request = InlineRequest(source_text, newer_index)
                inline_response = InlineHelper.handle_inline_backslash(inline_request)
                newer_index = inline_response.new_index
                destination_parts.append(source_text[old_new_index:newer_index])
            elif ParserHelper.is_character_at_index(
                source_text, newer_index, LinkHelper.__non_angle_link_nest
            ):
                POGGER.debug("+1")
                nesting_level += 1
                destination_parts.append(LinkHelper.__non_angle_link_nest)
                newer_index += 1
            elif ParserHelper.is_character_at_index(
                source_text, newer_index, LinkHelper.__non_angle_link_unnest
            ):
                POGGER.debug("-1")
                keep_collecting = bool(nesting_level)
                if keep_collecting:
                    destination_parts.append(LinkHelper.__non_angle_link_unnest)
                    newer_index += 1
                    nesting_level -= 1
            else:
                keep_collecting = False

        if nesting_level:
            return -1, None
        return newer_index, "".join(destination_parts)

    @staticmethod
    def __parse_link_destination(
        source_text: str, new_index: int
    ) -> Tuple[Optional[str], Optional[str], int, Optional[str], Optional[bool]]:
        """
        Parse an inline link's link destination.
        """

        POGGER.debug("parse_link_destination>>new_index>>$>>", source_text[new_index:])
        start_index = new_index
        did_use_angle_start = ParserHelper.is_character_at_index(
            source_text, new_index, LinkHelper.__angle_link_start
        )
        ex_link: Optional[str] = ""
        if did_use_angle_start:
            POGGER.debug(
                ">parse_angle_link_destination>new_index>$>$",
                new_index,
                source_text[new_index:],
            )
            new_index, ex_link = LinkHelper.__parse_angle_link_destination(
                source_text, new_index
            )
            POGGER.debug(
                ">parse_angle_link_destination>new_index>$>ex_link>$>",
                new_index,
                ex_link,
            )
        else:
            POGGER.debug(
                ">parse_non_angle_link_destination>new_index>$>$",
                new_index,
                source_text[new_index:],
            )
            newer_index, ex_link = LinkHelper.__parse_non_angle_link_destination(
                source_text, new_index
            )
            assert newer_index is not None
            new_index = newer_index
            POGGER.debug(
                ">parse_non_angle_link_destination>new_index>$>ex_link>$>",
                new_index,
                ex_link,
            )
            if not ex_link:
                return None, None, -1, None, None

        if new_index != -1 and ParserHelper.newline_character in ex_link:
            return None, None, -1, None, None
        POGGER.debug(
            "handle_backslashes>>new_index>>$>>ex_link>>$>>",
            new_index,
            ex_link,
        )

        pre_handle_link = ex_link
        if new_index != -1 and ex_link:
            ex_link = InlineHelper.handle_backslashes(ex_link)
        POGGER.debug(
            "urllib.parse.quote>>ex_link>>$>>",
            ex_link,
        )

        ex_link = LinkHelper.__encode_link_destination(ex_link)
        POGGER.debug(
            "parse_link_destination>>new_index>>$>>ex_link>>$>>",
            new_index,
            ex_link,
        )
        return (
            ex_link,
            pre_handle_link,
            new_index,
            source_text[start_index:new_index],
            did_use_angle_start,
        )

    @staticmethod
    def __parse_link_title(
        source_text: str, new_index: int
    ) -> Tuple[Optional[str], Optional[str], int, str]:
        """
        Parse an inline link's link title.
        """

        POGGER.debug("parse_link_title>>new_index>>$>>", source_text[new_index:])
        ex_title: Optional[str] = ""
        bounding_character = ""
        newer_index: Optional[int] = new_index
        assert newer_index is not None
        if ParserHelper.is_character_at_index(
            source_text, newer_index, LinkHelper.__link_title_single
        ):
            bounding_character = LinkHelper.__link_title_single
            newer_index, ex_title = InlineHelper.extract_bounded_string(
                source_text, newer_index + 1, LinkHelper.__link_title_single, None
            )
        elif ParserHelper.is_character_at_index(
            source_text, newer_index, LinkHelper.__link_title_double
        ):
            bounding_character = LinkHelper.__link_title_double
            newer_index, ex_title = InlineHelper.extract_bounded_string(
                source_text, newer_index + 1, LinkHelper.__link_title_double, None
            )
        elif ParserHelper.is_character_at_index(
            source_text, newer_index, LinkHelper.__link_title_parenthesis_open
        ):
            bounding_character = LinkHelper.__link_title_parenthesis_open
            newer_index, ex_title = InlineHelper.extract_bounded_string(
                source_text,
                newer_index + 1,
                LinkHelper.__link_title_parenthesis_close,
                LinkHelper.__link_title_parenthesis_open,
            )
        else:
            newer_index = -1
        POGGER.debug(
            "parse_link_title>>new_index>>$>>ex_link>>$>>",
            newer_index,
            ex_title,
        )
        pre_ex_title = ex_title
        if ex_title is not None:
            ex_title = InlineHelper.append_text(
                "",
                InlineHelper.handle_backslashes(ex_title),
                add_text_signature=False,
            )
        POGGER.debug("parse_link_title>>pre>>$>>", pre_ex_title)
        POGGER.debug("parse_link_title>>after>>$>>", ex_title)

        assert newer_index is not None
        return ex_title, pre_ex_title, newer_index, bounding_character

    @staticmethod
    def __process_inline_link_body(
        source_text: str, new_index: int, tabified_text: Optional[str]
    ) -> Tuple[
        Optional[str],
        Optional[str],
        Optional[str],
        Optional[str],
        int,
        bool,
        Optional[str],
        Optional[str],
        Optional[str],
        Optional[str],
    ]:
        """
        Given that an inline link has been identified, process it's body.
        """

        POGGER.debug("process_inline_link_body>:$:<", source_text[new_index:])
        POGGER.debug("source_text>:$:<", source_text)
        POGGER.debug("tabified_text>:$:<", tabified_text)

        text_to_scan = source_text
        if tabified_text:
            text_to_scan = tabified_text
            tabified_new_index = LinkHelper.__translate_between_strings(
                source_text, tabified_text, new_index
            )
            POGGER.debug("tabified_new_index>:$:<", tabified_new_index)
            new_index = tabified_new_index

        new_index += 1

        newer_index: Optional[int] = new_index
        newer_index, before_link_whitespace = ParserHelper.extract_ascii_whitespace(
            text_to_scan, new_index
        )

        POGGER.debug(
            "newer_index>>$>>text_to_scan[]>>$>",
            newer_index,
            text_to_scan[newer_index:],
        )
        assert newer_index is not None
        if not ParserHelper.is_character_at_index(
            text_to_scan, newer_index, LinkHelper.__link_format_inline_end
        ):
            (
                inline_link,
                pre_inline_link,
                newer_index,
                did_use_angle_start,
                before_title_whitespace,
                inline_title,
                pre_inline_title,
                bounding_character,
                after_title_whitespace,
            ) = LinkHelper.__parse_inline_link_properties(text_to_scan, newer_index)
        else:
            (
                inline_link,
                pre_inline_link,
                inline_title,
                pre_inline_title,
                did_use_angle_start,
                bounding_character,
                before_title_whitespace,
                after_title_whitespace,
            ) = ("", "", "", "", False, "", "", "")
        POGGER.debug(
            "inline_link>>$>>inline_title>>$>newer_index>$>",
            inline_link,
            inline_title,
            newer_index,
        )
        assert newer_index is not None
        newer_index, did_use_angle_start = LinkHelper.__process_inline_link_body_final(
            newer_index, source_text, tabified_text, did_use_angle_start
        )
        POGGER.debug(
            "process_inline_link_body>>inline_link>>$>>inline_title>>$>new_index>$>",
            inline_link,
            inline_title,
            newer_index,
        )
        return (
            inline_link,
            pre_inline_link,
            inline_title,
            pre_inline_title,
            newer_index,
            did_use_angle_start,
            bounding_character,
            before_link_whitespace,
            before_title_whitespace,
            after_title_whitespace,
        )

    @staticmethod
    def __process_inline_link_body_final(
        newer_index: int,
        source_text: str,
        tabified_text: Optional[str],
        did_use_angle_start: Optional[bool],
    ) -> Tuple[int, bool]:
        if newer_index != -1:
            if tabified_text:
                untabified_newer_index = LinkHelper.__translate_between_strings(
                    tabified_text, source_text, newer_index
                )
                POGGER.debug("untabified_newer_index>:$:<", untabified_newer_index)
                newer_index = untabified_newer_index

            assert did_use_angle_start is not None
            if ParserHelper.is_character_at_index(
                source_text, newer_index, LinkHelper.__link_format_inline_end
            ):
                newer_index += 1
            else:
                newer_index = -1
        else:
            did_use_angle_start = False
        return newer_index, did_use_angle_start

    @staticmethod
    def __translate_between_strings(
        source_text: str, destination_text: str, next_index: int
    ) -> int:

        stop_character = source_text[next_index]

        POGGER.debug("source_text>:$:<", source_text)
        POGGER.debug("index>:$:< == >:$:<", next_index, stop_character)
        POGGER.debug("destination_text>:$:<", destination_text)

        found_in_source_text_count = 0
        found_in_source_text_index = source_text.find(stop_character)
        POGGER.debug(
            "source_text[$]>:$:<",
            found_in_source_text_index,
            source_text[found_in_source_text_index:],
        )
        while found_in_source_text_index != next_index:
            found_in_source_text_count += 1
            found_in_source_text_index = source_text.find(
                stop_character, found_in_source_text_index + 1
            )
            POGGER.debug(
                "source_text[$]>:$:<",
                found_in_source_text_index,
                source_text[found_in_source_text_index:],
            )
        POGGER.debug("found_in_source_text_count>:$:<", found_in_source_text_count)
        POGGER.debug(
            "source_text[$]>:$:<",
            found_in_source_text_index,
            source_text[found_in_source_text_index:],
        )

        found_in_destination_text_count = 0
        stop_character_in_destination_index = destination_text.find(stop_character)
        POGGER.debug(
            "stop_character_in_destination_index[$]>:$:<",
            stop_character_in_destination_index,
            destination_text[stop_character_in_destination_index:],
        )
        while found_in_destination_text_count != found_in_source_text_count:
            found_in_destination_text_count += 1
            stop_character_in_destination_index = destination_text.find(
                stop_character, stop_character_in_destination_index + 1
            )
            POGGER.debug(
                "adj_tabified_text[$]>:$:<",
                stop_character_in_destination_index,
                destination_text[stop_character_in_destination_index:],
            )
            assert stop_character_in_destination_index != -1
        POGGER.debug(
            "found_in_destination_text_count>:$:<", found_in_destination_text_count
        )
        POGGER.debug(
            "adj_tabified_text[$]>:$:<",
            stop_character_in_destination_index,
            destination_text[stop_character_in_destination_index:],
        )
        assert destination_text[stop_character_in_destination_index] == stop_character
        return stop_character_in_destination_index

    @staticmethod
    def __parse_inline_link_properties(
        source_text: str, new_index: int
    ) -> Tuple[
        Optional[str],
        Optional[str],
        Optional[int],
        Optional[bool],
        Optional[str],
        Optional[str],
        Optional[str],
        Optional[str],
        Optional[str],
    ]:
        inline_title: Optional[str] = ""
        pre_inline_title: Optional[str] = ""
        bounding_character: Optional[str] = ""
        before_title_whitespace: Optional[str] = ""
        after_title_whitespace: Optional[str] = ""
        newer_index: Optional[int] = None
        POGGER.debug(">>search for link destination")
        (
            inline_link,
            pre_inline_link,
            newer_index,
            _,
            did_use_angle_start,
        ) = LinkHelper.__parse_link_destination(source_text, new_index)
        POGGER.debug(
            ">>link destination>>$>>$>>",
            source_text,
            newer_index,
        )
        if newer_index != -1:
            POGGER.debug(
                "before ws>>$<",
                source_text[newer_index:],
            )
            (
                newer_index,
                before_title_whitespace,
            ) = ParserHelper.extract_ascii_whitespace(source_text, newer_index)
            POGGER.debug(
                "after ws>>$>",
                source_text[newer_index:],
            )
            assert newer_index is not None
            if ParserHelper.is_character_at_index_not(
                source_text, newer_index, LinkHelper.__link_format_inline_end
            ):
                (
                    inline_title,
                    pre_inline_title,
                    newer_index,
                    bounding_character,
                ) = LinkHelper.__parse_link_title(source_text, newer_index)
        if newer_index != -1:
            (
                newer_index,
                after_title_whitespace,
            ) = ParserHelper.extract_ascii_whitespace(source_text, newer_index)
        return (
            inline_link,
            pre_inline_link,
            newer_index,
            did_use_angle_start,
            before_title_whitespace,
            inline_title,
            pre_inline_title,
            bounding_character,
            after_title_whitespace,
        )

    @staticmethod
    def __look_up_link(
        link_to_lookup: str, new_index: int, link_type: str
    ) -> Tuple[int, str, str]:
        """
        Look up a link to see if it is present.
        """

        POGGER.debug("pre>>$<<", link_to_lookup)
        link_to_lookup = ParserHelper.remove_all_from_text(link_to_lookup)
        POGGER.debug("mid(pre-norm)>>$<<", link_to_lookup)

        link_label = LinkHelper.normalize_link_label(link_to_lookup)
        POGGER.debug("post>>$<<", link_label)

        POGGER.debug("defs>>$<<", LinkHelper.__link_definitions)
        if not link_label or link_label not in LinkHelper.__link_definitions:
            update_index: int = -1
            inline_link: str = ""
            inline_title: str = ""
        else:
            POGGER.debug(link_type)
            link_titles = LinkHelper.__link_definitions[link_label]
            assert link_titles.inline_link is not None
            assert link_titles.inline_title is not None
            update_index, inline_link, inline_title = (
                new_index,
                link_titles.inline_link,
                link_titles.inline_title,
            )
        return update_index, inline_link, inline_title

    # pylint: disable=too-many-arguments,too-many-locals
    @staticmethod
    def __excavate_link(
        inline_blocks: List[MarkdownToken],
        ind: int,
        source_text: str,
        new_index: int,
        current_string_unresolved: str,
        remaining_line: str,
        tabified_remaining_line: Optional[str],
        tabified_text: Optional[str],
    ) -> Tuple[
        int,
        str,
        str,
        Optional[str],
        Optional[str],
        Optional[str],
        Optional[str],
        Optional[str],
        Optional[str],
        bool,
        Optional[str],
        Optional[str],
        Optional[str],
        Optional[str],
    ]:
        POGGER.debug(
            "handle_link_types>>$<<$<<",
            inline_blocks,
            ind,
        )
        POGGER.debug(
            "handle_link_types>source_text>>$<<",
            source_text,
        )
        POGGER.debug("handle_link_types>>$<<", source_text[new_index:])
        POGGER.debug(
            "handle_link_types>>current_string_unresolved>:$:<remaining_line>:$:<tabified_remaining_line>:$:<",
            current_string_unresolved,
            remaining_line,
            tabified_remaining_line,
        )
        text_to_scan = remaining_line
        if tabified_remaining_line is not None:
            text_to_scan = tabified_remaining_line
        text_from_blocks, text_from_blocks_raw = LinkHelper.__collect_text_from_blocks(
            inline_blocks, ind, f"{current_string_unresolved}{text_to_scan}"
        )
        POGGER.debug(
            "handle_link_types>>text_from_blocks_raw>>$<<",
            text_from_blocks_raw,
        )
        POGGER.debug(
            "handle_link_types>>text_from_blocks>>$<<",
            text_from_blocks,
        )

        POGGER.debug("__look_for_link_formats>>$>>", new_index)
        (
            inline_link,
            pre_inline_link,
            inline_title,
            pre_inline_title,
            update_index,
            tried_full_reference_form,
            ex_label,
            label_type,
            did_use_angle_start,
            inline_title_bounding_character,
            before_link_whitespace,
            before_title_whitespace,
            after_title_whitespace,
        ) = LinkHelper.__look_for_link_formats(
            source_text, new_index, text_from_blocks, tabified_text
        )

        # u != -1 - inline valid
        # tried_full_reference_form - collapsed or full valid
        if update_index == -1 and not tried_full_reference_form:
            (
                ex_label,
                update_index,
                inline_link,
                inline_title,
                label_type,
                pre_inline_link,
            ) = LinkHelper.__look_for_shortcut_link(
                inline_blocks, text_from_blocks, new_index
            )
        return (
            update_index,
            text_from_blocks,
            text_from_blocks_raw,
            inline_link,
            pre_inline_link,
            inline_title,
            pre_inline_title,
            ex_label,
            label_type,
            did_use_angle_start,
            inline_title_bounding_character,
            before_link_whitespace,
            before_title_whitespace,
            after_title_whitespace,
        )

    # pylint: enable=too-many-arguments,too-many-locals

    # pylint: disable=too-many-arguments, too-many-locals
    @staticmethod
    def __handle_link_types(
        inline_blocks: List[MarkdownToken],
        ind: int,
        source_text: str,
        new_index: int,
        start_text: str,
        remaining_line: str,
        tabified_remaining_line: Optional[str],
        current_string_unresolved: str,
        xx_fn: Callable[[str], str],
        tabified_text: Optional[str],
    ) -> Tuple[int, Optional[MarkdownToken], bool]:
        """
        After finding a link specifier, figure out what type of link it is.
        """

        (
            update_index,
            text_from_blocks,
            text_from_blocks_raw,
            inline_link,
            pre_inline_link,
            inline_title,
            pre_inline_title,
            ex_label,
            label_type,
            did_use_angle_start,
            inline_title_bounding_character,
            before_link_whitespace,
            before_title_whitespace,
            after_title_whitespace,
        ) = LinkHelper.__excavate_link(
            inline_blocks,
            ind,
            source_text,
            new_index,
            current_string_unresolved,
            remaining_line,
            tabified_remaining_line,
            tabified_text,
        )

        POGGER.debug("<<<<<<<new_index<<<<<<<$<<", new_index)
        POGGER.debug("<<<<<<<update_index<<<<<<<$<<", update_index)
        POGGER.debug("<<<<<<<text_from_blocks_raw<<<<<<<$<<", text_from_blocks_raw)
        if update_index != -1:
            assert ex_label is not None
            assert before_link_whitespace is not None
            assert inline_link is not None
            assert pre_inline_link is not None
            assert inline_title is not None
            assert pre_inline_title is not None
            assert inline_title_bounding_character is not None
            assert before_title_whitespace is not None
            assert after_title_whitespace is not None
            assert label_type is not None
            consume_rest_of_line, token_to_append = LinkHelper.__create_link_token(
                start_text,
                inline_link,
                pre_inline_link,
                inline_title,
                pre_inline_title,
                text_from_blocks,
                text_from_blocks_raw,
                inline_blocks,
                ind,
                did_use_angle_start,
                inline_title_bounding_character,
                before_link_whitespace,
                before_title_whitespace,
                after_title_whitespace,
                ex_label,
                label_type,
                remaining_line,
                current_string_unresolved,
                xx_fn,
            )
        else:
            consume_rest_of_line, token_to_append = False, None

        POGGER.debug(
            "handle_link_types<update_index<$<<$<<",
            update_index,
            token_to_append,
        )
        return update_index, token_to_append, consume_rest_of_line

    # pylint: enable=too-many-arguments, too-many-locals

    @staticmethod
    def __look_for_shortcut_link(
        inline_blocks: List[MarkdownToken], text_from_blocks: str, new_index: int
    ) -> Tuple[str, int, str, str, str, str]:
        POGGER.debug("shortcut?")
        POGGER.debug(
            ">>$<<",
            inline_blocks,
        )
        POGGER.debug(
            ">>$<<",
            text_from_blocks,
        )

        update_index, inline_link, inline_title = LinkHelper.__look_up_link(
            text_from_blocks, new_index, Constants.link_type__shortcut
        )
        return (
            "",
            update_index,
            inline_link,
            inline_title,
            Constants.link_type__shortcut,
            "",
        )

    # pylint: disable=too-many-arguments, too-many-locals
    @staticmethod
    def __create_link_token(
        start_text: str,
        inline_link: str,
        pre_inline_link: str,
        inline_title: str,
        pre_inline_title: str,
        text_from_blocks: str,
        text_from_blocks_raw: str,
        inline_blocks: List[MarkdownToken],
        ind: int,
        did_use_angle_start: bool,
        inline_title_bounding_character: str,
        before_link_whitespace: str,
        before_title_whitespace: str,
        after_title_whitespace: str,
        ex_label: str,
        label_type: str,
        remaining_line: str,
        current_string_unresolved: str,
        xx_fn: Callable[[str], str],
    ) -> Tuple[bool, Optional[MarkdownToken]]:
        """
        Create the right type of link token.
        """
        (text_from_blocks_raw, line_number, column_number,) = (
            ParserHelper.resolve_backspaces_from_text(text_from_blocks_raw),
            inline_blocks[ind].line_number,
            inline_blocks[ind].column_number,
        )

        # POGGER.debug("<<<<<<<start_text<<<<<<<$<<", start_text)
        # POGGER.debug(">>inline_link>>$>>", inline_link)
        # POGGER.debug(">>pre_inline_link>>$>>", pre_inline_link)
        # POGGER.debug(">>inline_title>>$>>", inline_title)
        # POGGER.debug(">>pre_inline_title>>$>>", pre_inline_title)
        # POGGER.debug(
        #     ">>text_from_blocks>>$>>",
        #     text_from_blocks,
        # )
        _ = text_from_blocks
        if pre_inline_link == inline_link:
            pre_inline_link = ""
        if pre_inline_title == inline_title:
            pre_inline_title = ""
        # POGGER.debug(">>pre_inline_link>>$>>", pre_inline_link)

        # POGGER.debug(">>text_from_blocks_raw>>$>>", text_from_blocks_raw)
        # POGGER.debug(">>inline_blocks[ind]>>$>>", inline_blocks[ind])

        if start_text == LinkHelper.__link_start_sequence:
            consume_rest_of_line = False
            token_to_append = LinkHelper.__add_link_start_token(
                inline_blocks,
                ind,
                inline_link,
                pre_inline_link,
                inline_title,
                pre_inline_title,
                ex_label,
                label_type,
                text_from_blocks_raw,
                did_use_angle_start,
                inline_title_bounding_character,
                before_link_whitespace,
                before_title_whitespace,
                after_title_whitespace,
                line_number,
                column_number,
            )
        else:
            token_to_append = None
            consume_rest_of_line, text_from_blocks_raw = LinkHelper.__add_image_token(
                start_text,
                inline_blocks,
                ind,
                remaining_line,
                text_from_blocks_raw,
                xx_fn,
                inline_link,
                pre_inline_link,
                inline_title,
                pre_inline_title,
                ex_label,
                label_type,
                did_use_angle_start,
                inline_title_bounding_character,
                before_link_whitespace,
                before_title_whitespace,
                after_title_whitespace,
                line_number,
                column_number,
                current_string_unresolved,
            )
        return consume_rest_of_line, token_to_append

    # pylint: enable=too-many-arguments, too-many-locals

    # pylint: disable=too-many-arguments, too-many-locals
    @staticmethod
    def __add_link_start_token(
        inline_blocks: List[MarkdownToken],
        ind: int,
        inline_link: str,
        pre_inline_link: str,
        inline_title: str,
        pre_inline_title: str,
        ex_label: str,
        label_type: str,
        text_from_blocks_raw: str,
        did_use_angle_start: bool,
        inline_title_bounding_character: str,
        before_link_whitespace: str,
        before_title_whitespace: str,
        after_title_whitespace: str,
        line_number: int,
        column_number: int,
    ) -> MarkdownToken:
        inline_blocks[ind] = LinkStartMarkdownToken(
            inline_link,
            pre_inline_link,
            inline_title,
            pre_inline_title,
            ex_label,
            label_type,
            text_from_blocks_raw,
            did_use_angle_start,
            inline_title_bounding_character,
            before_link_whitespace,
            before_title_whitespace,
            after_title_whitespace,
            line_number,
            column_number,
        )
        return inline_blocks[ind].generate_close_markdown_token_from_markdown_token(
            "", ""
        )

    # pylint: enable=too-many-arguments, too-many-locals

    # pylint: disable=too-many-arguments, too-many-locals
    @staticmethod
    def __add_image_token(
        start_text: str,
        inline_blocks: List[MarkdownToken],
        ind: int,
        remaining_line: str,
        text_from_blocks_raw: str,
        xx_fn: Callable[[str], str],
        inline_link: str,
        pre_inline_link: str,
        inline_title: str,
        pre_inline_title: str,
        ex_label: str,
        label_type: str,
        did_use_angle_start: bool,
        inline_title_bounding_character: str,
        before_link_whitespace: str,
        before_title_whitespace: str,
        after_title_whitespace: str,
        line_number: int,
        column_number: int,
        current_string_unresolved: str,
    ) -> Tuple[bool, str]:
        assert start_text == LinkHelper.image_start_sequence
        POGGER.debug("\n>>__consume_text_for_image_alt_text>>$>>", inline_blocks)
        POGGER.debug("\n>>__consume_text_for_image_alt_text>>$>>", ind)
        POGGER.debug("\n>>__consume_text_for_image_alt_text>>$>>", remaining_line)
        (
            image_alt_text,
            text_from_blocks_raw,
        ) = LinkHelper.__consume_text_for_image_alt_text(
            inline_blocks, ind, remaining_line, text_from_blocks_raw, xx_fn
        )
        POGGER.debug("\n>>__consume_text_for_image_alt_text>>$>>", image_alt_text)

        inline_blocks[ind] = ImageStartMarkdownToken(
            inline_link,
            pre_inline_link,
            inline_title,
            pre_inline_title,
            image_alt_text,
            ex_label,
            label_type,
            text_from_blocks_raw,
            did_use_angle_start,
            inline_title_bounding_character,
            before_link_whitespace,
            before_title_whitespace,
            after_title_whitespace,
            line_number,
            column_number,
        )
        POGGER.debug("\n>>Image>>$", inline_blocks)
        POGGER.debug(">>start_text>>$<<", start_text)
        POGGER.debug(">>remaining_line>>$<<", remaining_line)
        POGGER.debug(">>current_string_unresolved>>$<<", current_string_unresolved)
        return True, text_from_blocks_raw

    # pylint: enable=too-many-arguments, too-many-locals

    # pylint: disable=too-many-locals
    @staticmethod
    def __look_for_link_formats(
        source_text: str,
        new_index: int,
        text_from_blocks: str,
        tabified_text: Optional[str],
    ) -> Tuple[
        Optional[str],
        Optional[str],
        Optional[str],
        Optional[str],
        int,
        bool,
        Optional[str],
        Optional[str],
        bool,
        Optional[str],
        Optional[str],
        Optional[str],
        Optional[str],
    ]:
        """
        Look for links in the various formats.
        """
        (
            update_index,
            tried_full_reference_form,
        ) = (-1, False)
        did_use_angle_start: bool = False
        bounding_character: Optional[str] = ""
        label_type: Optional[str] = ""
        inline_link: Optional[str] = ""
        pre_inline_link: Optional[str] = ""
        inline_title: Optional[str] = ""
        pre_inline_title: Optional[str] = ""
        ex_label: Optional[str] = ""
        before_link_whitespace: Optional[str] = ""
        before_title_whitespace: Optional[str] = ""
        after_title_whitespace: Optional[str] = ""
        if ParserHelper.is_character_at_index(
            source_text, new_index, LinkHelper.__link_format_inline_start
        ):
            POGGER.debug("inline reference? >>$>>", new_index)
            (
                inline_link,
                pre_inline_link,
                inline_title,
                pre_inline_title,
                update_index,
                did_use_angle_start,
                bounding_character,
                before_link_whitespace,
                before_title_whitespace,
                after_title_whitespace,
            ) = LinkHelper.__process_inline_link_body(
                source_text, new_index, tabified_text
            )
            label_type = Constants.link_type__inline
        elif ParserHelper.is_character_at_index(
            source_text, new_index, LinkHelper.__link_format_reference_start
        ):
            (
                label_type,
                tried_full_reference_form,
                update_index,
                inline_link,
                inline_title,
                ex_label,
            ) = LinkHelper.__try_to_find_link_match(
                new_index, source_text, text_from_blocks, tabified_text
            )
        POGGER.debug("__look_for_link_formats>>update_index>>$>>", update_index)
        return (
            inline_link,
            pre_inline_link,
            inline_title,
            pre_inline_title,
            update_index,
            tried_full_reference_form,
            ex_label,
            label_type,
            did_use_angle_start,
            bounding_character,
            before_link_whitespace,
            before_title_whitespace,
            after_title_whitespace,
        )

    # pylint: enable=too-many-locals

    # pylint: disable=too-many-locals
    @staticmethod
    def __try_to_find_link_match(
        new_index: int,
        source_text: str,
        text_from_blocks: str,
        tabified_text: Optional[str],
    ) -> Tuple[str, bool, int, str, str, Optional[str]]:
        POGGER.debug("collapsed reference?")

        # TODO label type as Enum?

        text_to_scan = source_text
        if tabified_text:
            assert tabified_text is not None
            text_to_scan = tabified_text
            tabified_new_index = LinkHelper.__translate_between_strings(
                source_text, tabified_text, new_index
            )
            POGGER.debug("tabified_new_index>:$:<", tabified_new_index)
            new_index = tabified_new_index

        after_open_index = new_index + 1
        tried_full_reference_form = ParserHelper.is_character_at_index(
            text_to_scan, after_open_index, LinkHelper.__link_format_reference_end
        )
        if tried_full_reference_form:
            ex_label: Optional[str] = ""

            POGGER.debug("collapsed reference")
            POGGER.debug(">>$>>", text_from_blocks)
            update_index, inline_link, inline_title = LinkHelper.__look_up_link(
                text_from_blocks,
                after_open_index + 1,
                "collapsed reference",
            )
            POGGER.debug("collapsed reference>update_index>$", update_index)
            label_type = Constants.link_type__collapsed
        else:
            POGGER.debug("full reference?")
            POGGER.debug(">>did_extract>>$>", text_to_scan[after_open_index:])
            (did_extract, after_label_index, ex_label,) = LinkHelper.extract_link_label(
                text_to_scan, after_open_index, include_reference_colon=False
            )
            POGGER.debug(
                ">>did_extract>>$>after_label_index>$>ex_label>$>",
                did_extract,
                after_label_index,
                ex_label,
            )
            tried_full_reference_form = did_extract
            if did_extract:
                assert ex_label is not None
                label_type = Constants.link_type__full
                update_index, inline_link, inline_title = LinkHelper.__look_up_link(
                    ex_label, after_label_index, "full reference"
                )
            else:
                label_type, inline_link, inline_title, update_index = "", "", "", -1

        if tabified_text and update_index != -1:

            assert tabified_text is not None

            # Both of the above functions consume the last character of the link.
            # Instead of guessing, we "rewind" the index by one character so that
            # we can have something to sync on that is not an end of line or whitespace.
            assert (
                tabified_text[update_index - 1]
                == LinkHelper.__link_format_reference_end
            )
            untabified_update_index = LinkHelper.__translate_between_strings(
                tabified_text, source_text, update_index - 1
            )
            POGGER.debug("untabified_update_index>:$:<", untabified_update_index)
            update_index = untabified_update_index + 1

        return (
            label_type,
            tried_full_reference_form,
            update_index,
            inline_link,
            inline_title,
            ex_label,
        )

    # pylint: enable=too-many-locals

    @staticmethod
    def __encode_link_destination(link_to_encode: str) -> str:

        percent_index, before_data = ParserHelper.collect_until_one_of_characters(
            link_to_encode, 0, LinkHelper.__special_link_destination_characters
        )
        assert percent_index is not None
        assert before_data is not None
        el_parts, link_to_encode_size = [
            urllib.parse.quote(before_data, safe=LinkHelper.__link_safe_characters)
        ], len(link_to_encode)
        while percent_index < link_to_encode_size:
            special_character = link_to_encode[percent_index]
            percent_index += 1
            if special_character == "%":
                hex_guess_characters = link_to_encode[percent_index : percent_index + 2]
                if len(hex_guess_characters) == 2:
                    try:
                        int(hex_guess_characters, 16)
                        el_parts.extend(["%", hex_guess_characters])
                        percent_index += 2
                    except ValueError:
                        el_parts.append("%25")
                else:
                    el_parts.append("%25")
            else:
                assert special_character == "&"
                el_parts.append("&amp;")

            percent_index, before_data = ParserHelper.collect_until_one_of_characters(
                link_to_encode,
                percent_index,
                LinkHelper.__special_link_destination_characters,
            )
            assert percent_index is not None
            assert before_data is not None
            el_parts.append(
                urllib.parse.quote(before_data, safe=LinkHelper.__link_safe_characters)
            )

        return "".join(el_parts)

    @staticmethod
    def rehydrate_inline_image_text_from_token(
        image_token: ImageStartMarkdownToken,
    ) -> str:
        """
        Given an image token, rehydrate it's original text from the token.
        """
        return f"!{LinkHelper.rehydrate_inline_link_text_from_token(image_token)}"

    @staticmethod
    def __rehydrate_inline_link_text_from_token_type_inline(
        link_token: ReferenceMarkdownToken, link_parts: List[str]
    ) -> None:
        assert link_token.before_title_whitespace is not None
        assert link_token.before_link_whitespace is not None
        link_parts.extend(
            [
                "[",
                ParserHelper.remove_all_from_text(link_token.text_from_blocks),
                "](",
                link_token.before_link_whitespace,
                f"<{link_token.active_link_uri}>"
                if link_token.did_use_angle_start
                else link_token.active_link_uri,
                link_token.before_title_whitespace,
            ]
        )
        if link_token.active_link_title:
            if link_token.inline_title_bounding_character == "'":
                title_prefix = "'"
                title_suffix = "'"
            elif link_token.inline_title_bounding_character == "(":
                title_prefix = "("
                title_suffix = ")"
            else:
                title_prefix = '"'
                title_suffix = '"'

            assert link_token.after_title_whitespace is not None
            link_parts.extend(
                [
                    title_prefix,
                    link_token.active_link_title,
                    title_suffix,
                    link_token.after_title_whitespace,
                ]
            )
        link_parts.append(")")

    @staticmethod
    def rehydrate_inline_link_text_from_token(
        link_token: ReferenceMarkdownToken,
    ) -> str:
        """
        Given a link token, rehydrate it's original text from the token.
        """

        link_parts = []
        if link_token.label_type == Constants.link_type__shortcut:
            link_parts.extend(
                [
                    "[",
                    ParserHelper.remove_all_from_text(link_token.text_from_blocks),
                    "]",
                ]
            )
        elif link_token.label_type == Constants.link_type__full:
            assert link_token.ex_label is not None
            link_parts.extend(
                ["[", link_token.text_from_blocks, "][", link_token.ex_label, "]"]
            )
        elif link_token.label_type == Constants.link_type__collapsed:
            link_parts.extend(["[", link_token.text_from_blocks, "][]"])
        else:
            assert link_token.label_type == Constants.link_type__inline
            LinkHelper.__rehydrate_inline_link_text_from_token_type_inline(
                link_token, link_parts
            )

        return "".join(link_parts)
