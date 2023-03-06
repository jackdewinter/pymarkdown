"""
Module to provide for the handlers for tokens to allow transformation into HTML.
"""
import inspect
import logging
from typing import Callable, Dict, List, Optional, cast

from pymarkdown.extensions.front_matter_extension import FrontMatterExtension
from pymarkdown.extensions.front_matter_markdown_token import FrontMatterMarkdownToken
from pymarkdown.extensions.pragma_token import PragmaToken
from pymarkdown.inline.inline_helper import InlineHelper
from pymarkdown.inline_markdown_token import (
    EmailAutolinkMarkdownToken,
    EmphasisMarkdownToken,
    HardBreakMarkdownToken,
    ImageStartMarkdownToken,
    InlineCodeSpanMarkdownToken,
    LinkStartMarkdownToken,
    RawHtmlMarkdownToken,
    TextMarkdownToken,
    UriAutolinkMarkdownToken,
)
from pymarkdown.markdown_token import EndMarkdownToken, MarkdownToken
from pymarkdown.parser_helper import ParserHelper
from pymarkdown.parser_logger import ParserLogger
from pymarkdown.transform_gfm.transform_to_gfm_container_token_handlers import (
    TransformToGfmContainerTokenHandlers,
)
from pymarkdown.transform_gfm.transform_to_gfm_leaf_token_handlers import (
    TransformToGfmLeafTokenHandlers,
)
from pymarkdown.transform_state import TransformState

POGGER = ParserLogger(logging.getLogger(__name__))
# pylint: disable=too-few-public-methods


class TransformToGfmTokenHandlers:
    """
    Class to provide for the handlers for tokens to allow transformation into HTML.
    """

    __uri_autolink_html_character_escape_map = {
        "<": "&lt;",
        ">": "&gt;",
        "&": "&amp;",
    }

    __raw_html_percent_escape_ascii_chars = '"%[\\]^`{}|'

    def __init__(self) -> None:
        self.__start_token_handlers: Dict[
            str, Callable[[str, MarkdownToken, TransformState], str]
        ] = {}
        self.__end_token_handlers: Dict[
            str, Callable[[str, MarkdownToken, TransformState], str]
        ] = {}

        TransformToGfmLeafTokenHandlers.register_handlers(self.__register_handlers)
        TransformToGfmContainerTokenHandlers.register_handlers(self.__register_handlers)

        self.__register_handlers(
            FrontMatterMarkdownToken, FrontMatterExtension.handle_front_matter_token
        )
        self.__register_handlers(HardBreakMarkdownToken, self.__handle_hard_break_token)
        self.__register_handlers(
            LinkStartMarkdownToken,
            self.__handle_start_link_token,
            self.__handle_end_link_token,
        )
        self.__register_handlers(ImageStartMarkdownToken, self.__handle_image_token)
        self.__register_handlers(
            InlineCodeSpanMarkdownToken, self.__handle_inline_code_span_token
        )
        self.__register_handlers(RawHtmlMarkdownToken, self.__handle_raw_html_token)
        self.__register_handlers(
            EmailAutolinkMarkdownToken, self.__handle_email_autolink_token
        )
        self.__register_handlers(UriAutolinkMarkdownToken, self.__handle_uri_autolink)
        self.__register_handlers(
            EmphasisMarkdownToken,
            self.__handle_start_emphasis_token,
            self.__handle_end_emphasis_token,
        )
        self.__register_handlers(TextMarkdownToken, self.__handle_text_token)
        self.__register_handlers(
            PragmaToken,
            self.__handle_pragma_token,
        )

    def __register_handlers(
        self,
        token_type: type,
        start_token_handler: Callable[[str, MarkdownToken, TransformState], str],
        end_token_handler: Optional[
            Callable[[str, MarkdownToken, TransformState], str]
        ] = None,
    ) -> None:
        """
        Register the handlers necessary to deal with token's start and end.
        """
        assert issubclass(
            token_type, MarkdownToken
        ), f"Token class '{token_type}' must be descended from the 'MarkdownToken' class."

        # This is being done to create a rough "default" instance of the type in
        # question.  Because it is a rough creation and we have no intentions of
        # using it, each parameter is an empty string.  Therefore, we expect that
        # mypy will have issues when we create the instance, hence ignoring them.
        #
        # That was the old way, and had problems.  The new way is to call a new
        # static method directly.  Both are here until that is completed.

        if "get_markdown_token_type" in token_type.__dict__:
            token_name = token_type.__dict__["get_markdown_token_type"].__func__()
        else:
            token_init_fn = token_type.__dict__["__init__"]
            init_parameters = {
                i: "" for i in inspect.getfullargspec(token_init_fn)[0] if i != "self"
            }
            handler_instance = token_type(**init_parameters)  # type: ignore
            token_name = handler_instance.token_name

        assert token_name
        self.__start_token_handlers[token_name] = start_token_handler
        if end_token_handler:
            self.__end_token_handlers[token_name] = end_token_handler

    # pylint: disable=too-many-arguments
    def apply_transformation(
        self,
        transform_state: TransformState,
        actual_tokens: List[MarkdownToken],
        actual_tokens_size: int,
        next_token: MarkdownToken,
        output_html: str,
    ) -> str:
        """
        Apply the required tranformation for the current token.
        """
        transform_state.add_trailing_text = None
        transform_state.add_leading_text = None
        transform_state.next_token = None

        if (transform_state.actual_token_index + 1) < actual_tokens_size:
            transform_state.next_token = actual_tokens[
                transform_state.actual_token_index + 1
            ]
        if next_token.token_name in self.__start_token_handlers:
            start_handler_fn = self.__start_token_handlers[next_token.token_name]
            POGGER.debug("next_token>:$:<", next_token)
            POGGER.debug("output_html>:$:<", output_html)
            output_html = start_handler_fn(output_html, next_token, transform_state)
            POGGER.debug("output_html>:$:<", output_html)

        elif next_token.is_end_token:
            end_token = cast(EndMarkdownToken, next_token)
            if end_token.type_name not in self.__end_token_handlers:
                raise AssertionError(
                    f"Markdown token end type {end_token.type_name} not supported."
                )
            end_handler_fn = self.__end_token_handlers[end_token.type_name]
            POGGER.debug("end_token>:$:<", end_token)
            POGGER.debug("output_html>:$:<", output_html)
            output_html = end_handler_fn(output_html, end_token, transform_state)
            POGGER.debug("output_html>:$:<", output_html)
        else:
            raise AssertionError(
                f"Markdown token type {type(next_token)} not supported."
            )
        return output_html

    # pylint: enable=too-many-arguments

    @classmethod
    def __handle_hard_break_token(
        cls,
        output_html: str,
        next_token: MarkdownToken,
        transform_state: TransformState,
    ) -> str:
        _ = (next_token, transform_state)

        return "".join([output_html, "<br />", ParserHelper.newline_character])

    @classmethod
    def __handle_inline_code_span_token(
        cls,
        output_html: str,
        next_token: MarkdownToken,
        transform_state: TransformState,
    ) -> str:
        _ = transform_state

        code_span_token = cast(InlineCodeSpanMarkdownToken, next_token)
        return "".join(
            [
                output_html,
                "<code>",
                ParserHelper.resolve_all_from_text(code_span_token.span_text),
                "</code>",
            ]
        )

    @classmethod
    def __handle_raw_html_token(
        cls,
        output_html: str,
        next_token: MarkdownToken,
        transform_state: TransformState,
    ) -> str:
        _ = transform_state

        raw_html_token = cast(RawHtmlMarkdownToken, next_token)
        return "".join(
            [
                output_html,
                "<",
                ParserHelper.resolve_all_from_text(raw_html_token.raw_tag),
                ">",
            ]
        )

    @classmethod
    def __handle_pragma_token(
        cls,
        output_html: str,
        next_token: MarkdownToken,
        transform_state: TransformState,
    ) -> str:
        _ = (transform_state, next_token)

        return output_html

    @classmethod
    def __handle_email_autolink_token(
        cls,
        output_html: str,
        next_token: MarkdownToken,
        transform_state: TransformState,
    ) -> str:
        _ = transform_state

        email_token = cast(EmailAutolinkMarkdownToken, next_token)
        return "".join(
            [
                output_html,
                '<a href="mailto:',
                email_token.autolink_text,
                '">',
                email_token.autolink_text,
                "</a>",
            ]
        )

    @classmethod
    def __handle_uri_autolink(
        cls,
        output_html: str,
        next_token: MarkdownToken,
        transform_state: TransformState,
    ) -> str:
        _ = transform_state

        autolink_token = cast(UriAutolinkMarkdownToken, next_token)
        in_tag_pretext = InlineHelper.append_text(
            "",
            autolink_token.autolink_text,
            alternate_escape_map=TransformToGfmTokenHandlers.__uri_autolink_html_character_escape_map,
            add_text_signature=False,
        )

        tag_text_parts = []
        for next_character in in_tag_pretext:
            if (
                next_character
                in TransformToGfmTokenHandlers.__raw_html_percent_escape_ascii_chars
            ):
                tag_text_parts.extend(["%", (hex(ord(next_character))[2:]).upper()])
            elif ord(next_character) >= 128:
                encoded_data = next_character.encode("utf8")
                for encoded_byte in encoded_data:
                    tag_text_parts.extend(["%", (hex(encoded_byte)[2:]).upper()])
            else:
                tag_text_parts.append(next_character)

        return "".join(
            [
                output_html,
                '<a href="',
                "".join(tag_text_parts),
                '">',
                InlineHelper.append_text(
                    "", autolink_token.autolink_text, add_text_signature=False
                ),
                "</a>",
            ]
        )

    @classmethod
    def __handle_start_emphasis_token(
        cls,
        output_html: str,
        next_token: MarkdownToken,
        transform_state: TransformState,
    ) -> str:
        _ = transform_state

        emphasis_token = cast(EmphasisMarkdownToken, next_token)
        return "".join(
            [output_html, "<em>" if emphasis_token.emphasis_length == 1 else "<strong>"]
        )

    @classmethod
    def __handle_end_emphasis_token(
        cls,
        output_html: str,
        next_token: MarkdownToken,
        transform_state: TransformState,
    ) -> str:
        _ = transform_state

        end_token = cast(EndMarkdownToken, next_token)
        emphasis_token = cast(EmphasisMarkdownToken, end_token.start_markdown_token)

        return "".join(
            [
                output_html,
                "</em>" if emphasis_token.emphasis_length == 1 else "</strong>",
            ]
        )

    @classmethod
    def __handle_start_link_token(
        cls,
        output_html: str,
        next_token: MarkdownToken,
        transform_state: TransformState,
    ) -> str:
        _ = transform_state

        link_token = cast(LinkStartMarkdownToken, next_token)
        return "".join(
            [
                output_html,
                '<a href="',
                link_token.link_uri,
                f'" title="{link_token.link_title}' if link_token.link_title else "",
                '">',
            ]
        )

    @classmethod
    def __handle_end_link_token(
        cls,
        output_html: str,
        next_token: MarkdownToken,
        transform_state: TransformState,
    ) -> str:
        _ = (next_token, transform_state)

        return f"{output_html}</a>"

    @classmethod
    def __handle_image_token(
        cls,
        output_html: str,
        next_token: MarkdownToken,
        transform_state: TransformState,
    ) -> str:
        _ = transform_state

        image_token = cast(ImageStartMarkdownToken, next_token)
        return "".join(
            [
                output_html,
                '<img src="',
                image_token.link_uri,
                '" alt="',
                image_token.image_alt_text,
                '" ',
                (
                    f'title="{image_token.link_title}" '
                    if image_token.link_title
                    else ""
                ),
                "/>",
            ]
        )

    @classmethod
    def __handle_text_token(
        cls,
        output_html: str,
        next_token: MarkdownToken,
        transform_state: TransformState,
    ) -> str:
        """
        Handle the text token.
        """
        text_token = cast(TextMarkdownToken, next_token)
        adjusted_text_token = ParserHelper.resolve_all_from_text(text_token.token_text)

        token_parts: List[str] = []
        if transform_state.is_in_code_block:
            POGGER.debug(
                "text_token.extracted_whitespace>:$:<", text_token.extracted_whitespace
            )
            leading_space = ParserHelper.resolve_all_from_text(
                text_token.extracted_whitespace
            )

            POGGER.debug("leading_space>:$:<", leading_space)
            POGGER.debug("adjusted_text_token>:$:<", adjusted_text_token)
            token_parts.extend(
                [
                    leading_space,
                    adjusted_text_token,
                ]
            )
        elif transform_state.is_in_html_block:
            POGGER.debug(
                "text_token.extracted_whitespace>:$:<", text_token.extracted_whitespace
            )
            leading_space = ParserHelper.resolve_all_from_text(
                text_token.extracted_whitespace
            )

            POGGER.debug("leading_space>:$:<", leading_space)
            POGGER.debug("adjusted_text_token>:$:<", adjusted_text_token)
            POGGER.debug("newline_character>:$:<", ParserHelper.newline_character)
            token_parts.extend(
                [
                    leading_space,
                    adjusted_text_token,
                    ParserHelper.newline_character,
                ]
            )
        elif transform_state.is_in_setext_block:
            token_parts.append(adjusted_text_token)
        else:
            cls.__handle_text_token_normal(token_parts, text_token, adjusted_text_token)

        token_parts.insert(0, output_html)
        return "".join(token_parts)

    @classmethod
    def __handle_text_token_normal(
        cls,
        token_parts: List[str],
        text_token: TextMarkdownToken,
        adjusted_text_token: str,
    ) -> None:
        POGGER.debug("adjusted_text_token>:$:<", adjusted_text_token)
        POGGER.debug("text_token.end_whitespace>:$:<", text_token.end_whitespace)
        if text_token.end_whitespace is not None:
            newlines_in_adjusted = ParserHelper.count_newlines_in_text(
                adjusted_text_token
            )

            resolved_whitespace = ParserHelper.resolve_all_from_text(
                text_token.end_whitespace
            )
            POGGER.debug("resolved_whitespace>:$:<", resolved_whitespace)
            newlines_in_whitespace = ParserHelper.count_newlines_in_text(
                resolved_whitespace
            )
            arrays_to_combine: List[List[str]] = []
            if newlines_in_adjusted == newlines_in_whitespace:
                arrays_to_combine.append(adjusted_text_token.split("\n"))
            else:
                cls.__handle_text_token_normal_enhanced(arrays_to_combine, text_token)

            arrays_to_combine.append(resolved_whitespace.split("\n"))
            assert len(arrays_to_combine[0]) == len(arrays_to_combine[1])
            POGGER.debug("arrays_to_combine>:$:<", arrays_to_combine)
            final_parts: List[str] = []
            for loop_index in range(len(arrays_to_combine[0]) * 2):
                loop_index_mod = loop_index % 2
                loop_index_div = loop_index // 2
                if loop_index_mod == 0 and final_parts:
                    final_parts.append("\n")
                POGGER.debug(
                    "$-->final_parts>:$:<...$,$",
                    loop_index,
                    final_parts,
                    loop_index_mod,
                    loop_index_div,
                )
                final_parts.append(arrays_to_combine[loop_index_mod][loop_index_div])
                POGGER.debug("final_parts>:$:<", final_parts)
            adjusted_text_token = "".join(final_parts)
        token_parts.append(adjusted_text_token)

    @classmethod
    def __handle_text_token_normal_enhanced(
        cls, arrays_to_combine: List[List[str]], text_token: TextMarkdownToken
    ) -> None:
        """
        This should only happen in the case where there are replacement characters that
        include replacing a character sequence with a newline.  Specifically target that.
        """

        assert "\a" in text_token.token_text
        replace_character_count = ParserHelper.count_characters_in_text(
            text_token.token_text, "\a"
        )
        assert replace_character_count % 3 == 0

        start_index = 0
        current_line = ""
        processed_lines: List[str] = []
        next_index, found_prefix = ParserHelper.collect_until_one_of_characters(
            text_token.token_text, start_index, "\a\n"
        )
        assert next_index is not None
        assert found_prefix is not None
        # POGGER.debug("next_index>:$:<", next_index)
        # POGGER.debug("found_prefix>:$:<", found_prefix)
        while next_index < len(text_token.token_text):
            current_line += found_prefix
            if text_token.token_text[next_index] == "\a":
                # POGGER.debug("before>:$:<", text_token.token_text[start_index:next_index])
                middle_index = text_token.token_text.find("\a", next_index + 1)
                # POGGER.debug("replace>:$:<", text_token.token_text[next_index+1:middle_index])
                start_index = text_token.token_text.find("\a", middle_index + 1)
                # POGGER.debug("with>:$:<", text_token.token_text[middle_index+1:start_index])
                current_line += text_token.token_text[middle_index + 1 : start_index]
            else:
                processed_lines.append(current_line)
                current_line = ""
                start_index = next_index
            next_index, found_prefix = ParserHelper.collect_until_one_of_characters(
                text_token.token_text, start_index + 1, "\a\n"
            )
            assert next_index is not None
            assert found_prefix is not None
            # POGGER.debug("next_index>:$:<", next_index)
            # POGGER.debug("found_prefix>:$:<", found_prefix)
        current_line += found_prefix

        # POGGER.debug("currernt_line>:$:<", current_line)
        assert len(current_line)
        processed_lines.append(current_line)

        arrays_to_combine.append(processed_lines)


# pylint: enable=too-few-public-methods
