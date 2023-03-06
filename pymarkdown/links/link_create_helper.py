"""
Module to provide for the creation of a new link.
"""
import logging
from typing import Callable, List, Optional, Tuple, cast

from pymarkdown.inline.inline_helper import InlineHelper
from pymarkdown.inline_markdown_token import (
    EmailAutolinkMarkdownToken,
    ImageStartMarkdownToken,
    InlineCodeSpanMarkdownToken,
    LinkStartMarkdownToken,
    RawHtmlMarkdownToken,
    TextMarkdownToken,
)
from pymarkdown.links.link_helper_properties import LinkHelperProperties
from pymarkdown.markdown_token import MarkdownToken
from pymarkdown.parser_helper import ParserHelper
from pymarkdown.parser_logger import ParserLogger

POGGER = ParserLogger(logging.getLogger(__name__))

# pylint: disable=too-few-public-methods


class LinkCreateHelper:
    """
    Class to provide for the creation of a new link.
    """

    __link_start_sequence = "["
    image_start_sequence = "!["

    # pylint: disable=too-many-arguments
    @staticmethod
    def create_link_token(
        start_text: str,
        text_from_blocks: str,
        text_from_blocks_raw: str,
        inline_blocks: List[MarkdownToken],
        ind: int,
        remaining_line: str,
        current_string_unresolved: str,
        xx_fn: Callable[[str], str],
        lhp: LinkHelperProperties,
        update_index: int,
    ) -> Tuple[int, Optional[MarkdownToken], bool]:
        """
        Create the right type of link token.
        """
        (
            text_from_blocks_raw,
            line_number,
            column_number,
        ) = (
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
        if lhp.pre_inline_link == lhp.inline_link:
            lhp.pre_inline_link = ""
        if lhp.pre_inline_title == lhp.inline_title:
            lhp.pre_inline_title = ""
        # POGGER.debug(">>pre_inline_link>>$>>", pre_inline_link)

        # POGGER.debug(">>text_from_blocks_raw>>$>>", text_from_blocks_raw)
        # POGGER.debug(">>inline_blocks[ind]>>$>>", inline_blocks[ind])

        if start_text == LinkCreateHelper.__link_start_sequence:
            consume_rest_of_line = False
            token_to_append = LinkCreateHelper.__add_link_start_token(
                inline_blocks,
                ind,
                text_from_blocks_raw,
                line_number,
                column_number,
                lhp,
            )
        else:
            token_to_append = None
            (
                consume_rest_of_line,
                text_from_blocks_raw,
            ) = LinkCreateHelper.__add_image_token(
                start_text,
                inline_blocks,
                ind,
                remaining_line,
                text_from_blocks_raw,
                xx_fn,
                line_number,
                column_number,
                current_string_unresolved,
                lhp,
            )
        return update_index, token_to_append, consume_rest_of_line

    # pylint: enable=too-many-arguments

    # pylint: disable=too-many-arguments
    @staticmethod
    def __add_link_start_token(
        inline_blocks: List[MarkdownToken],
        ind: int,
        text_from_blocks_raw: str,
        line_number: int,
        column_number: int,
        lhp: LinkHelperProperties,
    ) -> MarkdownToken:
        inline_blocks[ind] = LinkStartMarkdownToken(
            text_from_blocks_raw, line_number, column_number, lhp
        )
        return inline_blocks[ind].generate_close_markdown_token_from_markdown_token(
            "", ""
        )

    # pylint: enable=too-many-arguments

    # pylint: disable=too-many-arguments
    @staticmethod
    def __add_image_token(
        start_text: str,
        inline_blocks: List[MarkdownToken],
        ind: int,
        remaining_line: str,
        text_from_blocks_raw: str,
        xx_fn: Callable[[str], str],
        line_number: int,
        column_number: int,
        current_string_unresolved: str,
        lhp: LinkHelperProperties,
    ) -> Tuple[bool, str]:
        assert start_text == LinkCreateHelper.image_start_sequence
        POGGER.debug("\n>>__consume_text_for_image_alt_text>>$>>", inline_blocks)
        POGGER.debug("\n>>__consume_text_for_image_alt_text>>$>>", ind)
        POGGER.debug("\n>>__consume_text_for_image_alt_text>>$>>", remaining_line)
        (
            image_alt_text,
            text_from_blocks_raw,
        ) = LinkCreateHelper.__consume_text_for_image_alt_text(
            inline_blocks, ind, remaining_line, text_from_blocks_raw, xx_fn
        )
        POGGER.debug("\n>>__consume_text_for_image_alt_text>>$>>", image_alt_text)

        inline_blocks[ind] = ImageStartMarkdownToken(
            image_alt_text,
            text_from_blocks_raw,
            line_number,
            column_number,
            lhp,
        )
        POGGER.debug("\n>>Image>>$", inline_blocks)
        POGGER.debug(">>start_text>>$<<", start_text)
        POGGER.debug(">>remaining_line>>$<<", remaining_line)
        POGGER.debug(">>current_string_unresolved>>$<<", current_string_unresolved)
        return True, text_from_blocks_raw

    # pylint: enable=too-many-arguments

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
                LinkCreateHelper.__handle_next_alt_text(
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
            LinkCreateHelper.__handle_next_alt_text_special_text(
                inline_blocks[ind_plus_one], alt_text_parts
            )
        elif inline_blocks[ind_plus_one].is_text:
            LinkCreateHelper.__handle_next_alt_text_normal_text(
                inline_blocks[ind_plus_one], alt_text_parts
            )
        elif inline_blocks[ind_plus_one].is_inline_raw_html:
            LinkCreateHelper.__handle_next_alt_text_raw_html(
                inline_blocks[ind_plus_one], alt_text_parts
            )
        elif inline_blocks[ind_plus_one].is_inline_code_span:
            LinkCreateHelper.__handle_next_alt_text_code_span(
                inline_blocks[ind_plus_one], alt_text_parts
            )
        elif inline_blocks[ind_plus_one].is_inline_autolink:
            LinkCreateHelper.__handle_next_alt_text_auto_link(
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
            LinkCreateHelper.__handle_next_alt_text_hard_break(
                inline_blocks[ind_plus_one], alt_text_parts
            )
        else:
            LinkCreateHelper.__handle_next_alt_text_else(
                inline_blocks[ind_plus_one], alt_text_parts
            )


# pylint: enable=too-few-public-methods
