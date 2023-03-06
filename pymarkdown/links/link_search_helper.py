"""
Module to provide for the ability to search the text for a link.
"""
import logging
from typing import Callable, List, Optional, Tuple, cast

from pymarkdown.constants import Constants
from pymarkdown.emphasis_helper import EmphasisHelper
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
from pymarkdown.links.link_create_helper import LinkCreateHelper
from pymarkdown.links.link_helper_properties import LinkHelperProperties
from pymarkdown.links.link_parse_helper import LinkParseHelper
from pymarkdown.markdown_token import MarkdownToken
from pymarkdown.parser_helper import ParserHelper
from pymarkdown.parser_logger import ParserLogger

POGGER = ParserLogger(logging.getLogger(__name__))


class LinkSearchHelper:
    """
    Class to provide for the ability to search the text for a link.
    """

    __link_start_sequence = "["
    image_start_sequence = "!["
    __valid_link_starts = [__link_start_sequence, image_start_sequence]

    # pylint: disable=too-many-arguments
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
        is_valid, consume_rest_of_line, next_index, updated_index = (
            False,
            False,
            next_index + 1,
            -1,
        )
        token_to_append: Optional[MarkdownToken] = None

        POGGER.debug("LOOKING FOR START")
        LinkSearchHelper.__debug_log_specials_in_tokens(inline_blocks)

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
                ) = LinkSearchHelper.__find_link(
                    inline_blocks,
                    search_index,
                    source_text,
                    next_index,
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
            LinkSearchHelper.__deactivate_used_tokens(
                inline_blocks, search_index, valid_special_start_text
            )
            return updated_index, True, token_to_append, consume_rest_of_line
        return next_index, False, token_to_append, consume_rest_of_line

    # pylint: enable=too-many-arguments

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
        if special_text_token.token_text in LinkSearchHelper.__valid_link_starts:
            valid_special_start_text: Optional[str] = special_text_token.token_text
            if special_text_token.is_active:
                # POGGER.debug(">>>>>>$", inline_blocks)
                assert valid_special_start_text is not None
                (
                    updated_index,
                    token_to_append,
                    consume_rest_of_line,
                ) = LinkSearchHelper.__handle_link_types(
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
                LinkSearchHelper.__revert_token_to_normal_text_token(
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
    def __revert_token_to_normal_text_token(
        inline_blocks: List[MarkdownToken], search_index: int
    ) -> None:
        """
        Revert this token from a special text token back to a normal text token.
        """

        POGGER.debug("REVERTING")
        LinkSearchHelper.__debug_log_specials_in_tokens(inline_blocks)

        text_token_to_replace = cast(
            SpecialTextMarkdownToken, inline_blocks[search_index]
        )
        inline_blocks.insert(search_index, text_token_to_replace.create_copy())
        del inline_blocks[search_index + 1]

        POGGER.debug("REVERTED")
        LinkSearchHelper.__debug_log_specials_in_tokens(inline_blocks)

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

        if valid_special_start_text == LinkSearchHelper.__link_start_sequence:
            POGGER.debug("DEACTIVATING")
            LinkSearchHelper.__debug_log_specials_in_tokens(inline_blocks)
            for deactivate_token in inline_blocks:
                if deactivate_token.is_special_text:
                    special_token = cast(SpecialTextMarkdownToken, deactivate_token)
                    POGGER.debug("inline_blocks>>>>>>>>>>>>>>>>>>$", special_token)
                    if (
                        special_token.token_text
                        == LinkSearchHelper.__link_start_sequence
                    ):
                        special_token.deactivate()
            POGGER.debug("DEACTIVATED")
            LinkSearchHelper.__debug_log_specials_in_tokens(inline_blocks)

    # pylint: disable=too-many-arguments
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
            lhp,
        ) = LinkSearchHelper.__excavate_link(
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
            assert lhp.ex_label is not None
            assert lhp.inline_link is not None
            assert lhp.pre_inline_link is not None
            assert lhp.inline_title is not None
            assert lhp.pre_inline_title is not None
            assert lhp.bounding_character is not None
            assert lhp.before_title_whitespace is not None
            assert lhp.after_title_whitespace is not None
            assert lhp.before_link_whitespace is not None
            assert lhp.label_type is not None
            return LinkCreateHelper.create_link_token(
                start_text,
                text_from_blocks,
                text_from_blocks_raw,
                inline_blocks,
                ind,
                remaining_line,
                current_string_unresolved,
                xx_fn,
                lhp,
                update_index,
            )
        return update_index, None, False

    # pylint: enable=too-many-arguments

    # pylint: disable=too-many-arguments
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
    ) -> Tuple[int, str, str, LinkHelperProperties,]:
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
        (
            text_from_blocks,
            text_from_blocks_raw,
        ) = LinkSearchHelper.__collect_text_from_blocks(
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
            update_index,
            tried_full_reference_form,
            lhp,
        ) = LinkParseHelper.look_for_link_formats(
            source_text, new_index, text_from_blocks, tabified_text
        )

        # u != -1 - inline valid
        # tried_full_reference_form - collapsed or full valid
        if update_index == -1 and not tried_full_reference_form:
            (
                lhp.ex_label,
                update_index,
                lhp.inline_link,
                lhp.inline_title,
                lhp.label_type,
                lhp.pre_inline_link,
            ) = LinkSearchHelper.__look_for_shortcut_link(
                inline_blocks, text_from_blocks, new_index
            )
        return (
            update_index,
            text_from_blocks,
            text_from_blocks_raw,
            lhp,
        )

    # pylint: enable=too-many-arguments
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

        update_index, inline_link, inline_title = LinkParseHelper.look_up_link(
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
            ) = LinkSearchHelper.__collect_text_from_next_block(
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
            is_inside_of_link = LinkSearchHelper.__collect_text_from_inline_link_end()
        elif inline_blocks[collect_index].is_inline_link:
            is_inside_of_link = LinkSearchHelper.__collect_text_from_inline_link_start(
                inline_blocks, collect_index, text_raw_parts
            )
        elif inline_blocks[collect_index].is_inline_image:
            LinkSearchHelper.__collect_text_from_inline_image(
                inline_blocks, collect_index, text_raw_parts, text_parts
            )
        elif inline_blocks[collect_index].is_inline_code_span:
            LinkSearchHelper.__collect_text_from_inline_code_span(
                inline_blocks,
                collect_index,
                text_raw_parts,
                text_parts,
                is_inside_of_link,
            )
        elif inline_blocks[collect_index].is_inline_raw_html:
            LinkSearchHelper.__collect_text_from_inline_raw_html(
                inline_blocks,
                collect_index,
                text_raw_parts,
                text_parts,
                is_inside_of_link,
            )
        elif inline_blocks[collect_index].is_inline_autolink:
            LinkSearchHelper.__collect_text_from_inline_autolink(
                inline_blocks,
                collect_index,
                text_raw_parts,
                text_parts,
                is_inside_of_link,
            )
        elif inline_blocks[collect_index].is_inline_hard_break:
            LinkSearchHelper.__collect_text_from_inline_hard_break(
                inline_blocks, collect_index, text_raw_parts, text_parts
            )
        elif not is_inside_of_link:
            LinkSearchHelper.__collect_text_from_text(
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
        raw_text = LinkSearchHelper.rehydrate_inline_link_text_from_token(link_token)
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
            LinkSearchHelper.rehydrate_inline_image_text_from_token(image_token)
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
    def rehydrate_inline_image_text_from_token(
        image_token: ImageStartMarkdownToken,
    ) -> str:
        """
        Given an image token, rehydrate it's original text from the token.
        """
        return f"!{LinkSearchHelper.rehydrate_inline_link_text_from_token(image_token)}"

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
            LinkSearchHelper.__rehydrate_inline_link_text_from_token_type_inline(
                link_token, link_parts
            )

        return "".join(link_parts)
