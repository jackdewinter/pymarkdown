"""
Module to provide for a transformation from markdown tokens to html for GFM.
"""
import inspect
import logging
from typing import Callable, Dict, List, Optional, cast

from pymarkdown.container_markdown_token import (
    BlockQuoteMarkdownToken,
    ListStartMarkdownToken,
    NewListItemMarkdownToken,
    OrderedListStartMarkdownToken,
    UnorderedListStartMarkdownToken,
)
from pymarkdown.extensions.front_matter_extension import FrontMatterExtension
from pymarkdown.extensions.front_matter_markdown_token import FrontMatterMarkdownToken
from pymarkdown.extensions.pragma_token import PragmaToken
from pymarkdown.inline_helper import InlineHelper
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
from pymarkdown.leaf_markdown_token import (
    AtxHeadingMarkdownToken,
    BlankLineMarkdownToken,
    FencedCodeBlockMarkdownToken,
    HtmlBlockMarkdownToken,
    IndentedCodeBlockMarkdownToken,
    LinkReferenceDefinitionMarkdownToken,
    ParagraphMarkdownToken,
    SetextHeadingMarkdownToken,
    ThematicBreakMarkdownToken,
)
from pymarkdown.markdown_token import EndMarkdownToken, MarkdownToken
from pymarkdown.parser_helper import ParserHelper
from pymarkdown.parser_logger import ParserLogger
from pymarkdown.transform_state import TransformState
from pymarkdown.transform_to_gfm_list_looseness import TransformToGfmListLooseness

POGGER = ParserLogger(logging.getLogger(__name__))

# pylint: disable=too-many-lines


class TransformToGfm:
    """
    Class to provide for a transformation from markdown tokens to html for GFM.
    """

    add_trailing_text_tokens = [
        "<hr />",
        "<p>",
        "<h1>",
        "<h2>",
        "<h3>",
        "<h4>",
        "<h5>",
        "<h6>",
        "<pre>",
        "<ul>",
        "<ol>",
        '<ol start="',
    ]
    uri_autolink_html_character_escape_map = {
        "<": "&lt;",
        ">": "&gt;",
        "&": "&amp;",
    }
    raw_html_percent_escape_ascii_chars = '"%[\\]^`{}|'

    def __init__(self) -> None:
        self.start_token_handlers: Dict[
            str, Callable[[str, MarkdownToken, TransformState], str]
        ] = {}
        self.end_token_handlers: Dict[
            str, Callable[[str, MarkdownToken, TransformState], str]
        ] = {}

        self.register_handlers(
            ThematicBreakMarkdownToken, self.__handle_thematic_break_token
        )
        self.register_handlers(
            FrontMatterMarkdownToken, FrontMatterExtension.handle_front_matter_token
        )
        self.register_handlers(HardBreakMarkdownToken, self.__handle_hard_break_token)
        self.register_handlers(
            AtxHeadingMarkdownToken,
            self.__handle_start_atx_heading_token,
            self.__handle_end_atx_heading_token,
        )
        self.register_handlers(
            LinkStartMarkdownToken,
            self.__handle_start_link_token,
            self.__handle_end_link_token,
        )
        self.register_handlers(ImageStartMarkdownToken, self.__handle_image_token)
        self.register_handlers(
            InlineCodeSpanMarkdownToken, self.__handle_inline_code_span_token
        )
        self.register_handlers(RawHtmlMarkdownToken, self.__handle_raw_html_token)
        self.register_handlers(
            EmailAutolinkMarkdownToken, self.__handle_email_autolink_token
        )
        self.register_handlers(UriAutolinkMarkdownToken, self.__handle_uri_autolink)
        self.register_handlers(
            SetextHeadingMarkdownToken,
            self.__handle_start_setext_heading_token,
            self.__handle_end_setext_heading_token,
        )
        self.register_handlers(
            EmphasisMarkdownToken,
            self.__handle_start_emphasis_token,
            self.__handle_end_emphasis_token,
        )
        self.register_handlers(TextMarkdownToken, self.__handle_text_token)
        self.register_handlers(
            ParagraphMarkdownToken,
            self.__handle_start_paragraph_token,
            self.__handle_end_paragraph_token,
        )
        self.register_handlers(BlankLineMarkdownToken, self.__handle_blank_line_token)
        self.register_handlers(
            BlockQuoteMarkdownToken,
            self.__handle_start_block_quote_token,
            self.__handle_end_block_quote_token,
        )
        self.register_handlers(
            IndentedCodeBlockMarkdownToken,
            self.__handle_start_indented_code_block_token,
            self.__handle_end_indented_code_block_token,
        )
        self.register_handlers(
            FencedCodeBlockMarkdownToken,
            self.__handle_start_fenced_code_block_token,
            self.__handle_end_fenced_code_block_token,
        )
        self.register_handlers(
            NewListItemMarkdownToken, self.__handle_new_list_item_token
        )
        self.register_handlers(
            OrderedListStartMarkdownToken,
            self.__handle_start_list_token,
            self.__handle_end_list_token,
        )
        self.register_handlers(
            UnorderedListStartMarkdownToken,
            self.__handle_start_list_token,
            self.__handle_end_list_token,
        )
        self.register_handlers(
            HtmlBlockMarkdownToken,
            self.__handle_start_html_block_token,
            self.__handle_end_html_block_token,
        )
        self.register_handlers(
            LinkReferenceDefinitionMarkdownToken,
            self.__handle_link_reference_definition_token,
        )
        self.register_handlers(
            PragmaToken,
            self.__handle_pragma_token,
        )

    def register_handlers(
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
        token_init_fn = token_type.__dict__["__init__"]
        init_parameters = {
            i: "" for i in inspect.getfullargspec(token_init_fn)[0] if i != "self"
        }
        handler_instance = token_type(**init_parameters)  # type: ignore

        self.start_token_handlers[handler_instance.token_name] = start_token_handler
        if end_token_handler:
            self.end_token_handlers[handler_instance.token_name] = end_token_handler

    def transform(self, actual_tokens: List[MarkdownToken]) -> str:
        """
        Transform the tokens into html.
        """
        POGGER.debug("\n\n---\n")
        transform_state, output_html, actual_tokens_size = (
            TransformState(actual_tokens),
            "",
            len(actual_tokens),
        )

        # This is the easiest way to finish covering the missing items.
        assert transform_state.next_token is None
        assert not transform_state.is_in_fenced_code_block

        for next_token in transform_state.actual_tokens:

            output_html = self.__apply_transformation(
                transform_state,
                actual_tokens,
                actual_tokens_size,
                next_token,
                output_html,
            )

            POGGER.debug("======")
            POGGER.debug(
                "add_trailing_text-->$<--",
                transform_state.add_trailing_text,
            )
            POGGER.debug("add_leading_text -->$<--", transform_state.add_leading_text)
            POGGER.debug("output_html    -->$<--", output_html)

            if transform_state.add_trailing_text:
                output_html = self.__apply_trailing_text(output_html, transform_state)

            if transform_state.add_leading_text:
                output_html = self.__apply_leading_text(output_html, transform_state)

            POGGER.debug("------")
            POGGER.debug("next_token     -->$<--", next_token)
            POGGER.debug("output_html    -->$<--", output_html)
            POGGER.debug("transform_stack-->$<--", transform_state.transform_stack)

            transform_state.last_token = next_token
            transform_state.actual_token_index += 1
        if output_html and output_html[-1] == ParserHelper.newline_character:
            output_html = output_html[:-1]
        POGGER.debug("output_html    -->$<--", output_html)
        return output_html

    # pylint: disable=too-many-arguments
    def __apply_transformation(
        self,
        transform_state: TransformState,
        actual_tokens: List[MarkdownToken],
        actual_tokens_size: int,
        next_token: MarkdownToken,
        output_html: str,
    ) -> str:
        transform_state.add_trailing_text = None
        transform_state.add_leading_text = None
        transform_state.next_token = None

        if (transform_state.actual_token_index + 1) < actual_tokens_size:
            transform_state.next_token = actual_tokens[
                transform_state.actual_token_index + 1
            ]
        if next_token.token_name in self.start_token_handlers:
            start_handler_fn = self.start_token_handlers[next_token.token_name]
            output_html = start_handler_fn(output_html, next_token, transform_state)

        elif next_token.is_end_token:
            end_token = cast(EndMarkdownToken, next_token)
            if end_token.type_name in self.end_token_handlers:
                end_handler_fn = self.end_token_handlers[end_token.type_name]
                output_html = end_handler_fn(output_html, end_token, transform_state)
            else:
                raise AssertionError(
                    f"Markdown token end type {end_token.type_name} not supported."
                )
        else:
            raise AssertionError(
                f"Markdown token type {type(next_token)} not supported."
            )
        return output_html

    # pylint: enable=too-many-arguments

    @classmethod
    def __apply_trailing_text(
        cls, output_html: str, transform_state: TransformState
    ) -> str:
        """
        Apply any trailing text to the output.
        """
        POGGER.debug("__apply_trailing_text>:$:<", output_html)
        stack_text = transform_state.transform_stack.pop()
        trailing_part = [stack_text]
        for next_token_to_test in TransformToGfm.add_trailing_text_tokens:
            if output_html.startswith(next_token_to_test):
                trailing_part.append(ParserHelper.newline_character)
                break

        POGGER.debug("trailing_part>:$:<", trailing_part)
        if trailing_part[-1].endswith("<li>") and output_html.startswith(
            "<blockquote>"
        ):
            trailing_part.append(ParserHelper.newline_character)
        trailing_part.append(output_html)
        POGGER.debug("trailing_part>:$:<", trailing_part)
        if output_html.endswith("</ul>") or output_html.endswith("</ol>"):
            trailing_part.append(ParserHelper.newline_character)
        assert transform_state.add_trailing_text is not None
        trailing_part.append(transform_state.add_trailing_text)
        combined_text = "".join(trailing_part)
        POGGER.debug("__apply_trailing_text>:$:<", combined_text)
        return combined_text

    @classmethod
    def __apply_leading_text(
        cls, output_html: str, transform_state: TransformState
    ) -> str:
        """
        Apply any leading text to the output.
        """

        output_html = (
            f"{output_html}{ParserHelper.newline_character}{transform_state.add_leading_text}"
            if output_html and output_html[-1] != ParserHelper.newline_character
            else f"{output_html}{transform_state.add_leading_text}"
        )
        transform_state.transform_stack.append(output_html)
        return ""

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
            token_parts.extend(
                [
                    ParserHelper.resolve_all_from_text(text_token.extracted_whitespace),
                    adjusted_text_token,
                ]
            )
        elif transform_state.is_in_html_block:
            token_parts.extend(
                [
                    text_token.extracted_whitespace,
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

    @classmethod
    def __handle_start_paragraph_token(
        cls,
        output_html: str,
        next_token: MarkdownToken,
        transform_state: TransformState,
    ) -> str:
        """
        Handle the start paragraph token.
        """
        _ = next_token
        token_parts = [output_html]
        if output_html and output_html[-1] != ParserHelper.newline_character:
            token_parts.append(ParserHelper.newline_character)
        if transform_state.is_in_loose_list:
            token_parts.append("<p>")
        return "".join(token_parts)

    @classmethod
    def __handle_end_paragraph_token(
        cls,
        output_html: str,
        next_token: MarkdownToken,
        transform_state: TransformState,
    ) -> str:
        """
        Handle the end paragraph token.
        """
        _ = next_token

        return (
            f"{output_html}</p>{ParserHelper.newline_character}"
            if transform_state.is_in_loose_list
            else output_html
        )

    @classmethod
    def __handle_blank_line_token(
        cls,
        output_html: str,
        next_token: MarkdownToken,
        transform_state: TransformState,
    ) -> str:
        """
        Handle the black line token.
        """
        _ = next_token

        if transform_state.is_in_html_block:
            output_html = f"{output_html}{ParserHelper.newline_character}"
        return output_html

    @classmethod
    def __handle_start_block_quote_token(
        cls,
        output_html: str,
        next_token: MarkdownToken,
        transform_state: TransformState,
    ) -> str:
        """
        Handle the start block quote token.
        """
        _ = next_token

        token_parts = [output_html]
        if output_html and output_html[-1] != ParserHelper.newline_character:
            token_parts.append(ParserHelper.newline_character)
        transform_state.is_in_loose_list = True
        token_parts.extend(["<blockquote>", ParserHelper.newline_character])
        return "".join(token_parts)

    @classmethod
    def __handle_end_block_quote_token(
        cls,
        output_html: str,
        next_token: MarkdownToken,
        transform_state: TransformState,
    ) -> str:
        """
        Handle the end block quote token.
        """
        _ = next_token

        token_parts = [output_html]
        if output_html[-1] != ParserHelper.newline_character:
            token_parts.append(ParserHelper.newline_character)
        transform_state.is_in_loose_list = (
            TransformToGfmListLooseness.reset_list_looseness(
                transform_state.actual_tokens,
                transform_state.actual_token_index,
            )
        )
        token_parts.extend(["</blockquote>", ParserHelper.newline_character])
        return "".join(token_parts)

    @classmethod
    def __handle_start_indented_code_block_token(
        cls,
        output_html: str,
        next_token: MarkdownToken,
        transform_state: TransformState,
    ) -> str:
        """
        Handle the start indented code block token.
        """
        _ = next_token

        token_parts = []
        if (
            not output_html
            and transform_state.transform_stack
            and transform_state.transform_stack[-1].endswith("<li>")
        ):
            token_parts.append(ParserHelper.newline_character)
        elif output_html and output_html[-1] != ParserHelper.newline_character:
            token_parts.extend([output_html, ParserHelper.newline_character])
        else:
            token_parts.append(output_html)
        transform_state.is_in_code_block, transform_state.is_in_fenced_code_block = (
            True,
            False,
        )
        token_parts.append("<pre><code>")
        return "".join(token_parts)

    @classmethod
    def __handle_end_indented_code_block_token(
        cls,
        output_html: str,
        next_token: MarkdownToken,
        transform_state: TransformState,
    ) -> str:
        """
        Handle the end indented code block token.
        """
        _ = next_token

        transform_state.is_in_code_block = False
        return "".join(
            [
                output_html,
                ParserHelper.newline_character,
                "</code></pre>",
                ParserHelper.newline_character,
            ]
        )

    @classmethod
    def __handle_start_fenced_code_block_token(
        cls,
        output_html: str,
        next_token: MarkdownToken,
        transform_state: TransformState,
    ) -> str:
        """
        Handle the start fenced code block token.
        """
        start_fence_token = cast(FencedCodeBlockMarkdownToken, next_token)
        token_parts = [output_html]
        if (output_html.endswith("</ol>") or output_html.endswith("</ul>")) or (
            output_html and output_html[-1] != ParserHelper.newline_character
        ):
            token_parts.append(ParserHelper.newline_character)
        transform_state.is_in_code_block, transform_state.is_in_fenced_code_block = (
            True,
            True,
        )
        token_parts.append("<pre><code")
        if start_fence_token.extracted_text:
            token_parts.extend(
                [' class="language-', start_fence_token.extracted_text, '"']
            )
        token_parts.append(">")
        return "".join(token_parts)

    @classmethod
    def __handle_end_fenced_code_block_token(
        cls,
        output_html: str,
        next_token: MarkdownToken,
        transform_state: TransformState,
    ) -> str:
        """
        Handle the end fenced code block token.
        """
        end_token = cast(EndMarkdownToken, next_token)
        fenced_token_index = transform_state.actual_token_index - 1
        while not transform_state.actual_tokens[
            fenced_token_index
        ].is_fenced_code_block:
            fenced_token_index -= 1
        fenced_token = cast(
            FencedCodeBlockMarkdownToken,
            transform_state.actual_tokens[fenced_token_index],
        )

        inner_tag_parts = ["<code"]
        if fenced_token.extracted_text:
            inner_tag_parts.extend(
                [
                    ' class="language-',
                    fenced_token.extracted_text,
                    '"',
                ]
            )
        inner_tag_parts.append(">")
        inner_tag = "".join(inner_tag_parts)

        POGGER.debug(f"inner_tag>>:{inner_tag}:<<")
        POGGER.debug(f"output_html>>:{output_html}:<<")
        POGGER.debug(
            f"last_token>>:{transform_state.actual_tokens[transform_state.actual_token_index - 1]}:<<"
        )

        token_parts = [output_html]
        if (
            not output_html.endswith(inner_tag)
            and output_html[-1] != ParserHelper.newline_character
        ):
            token_parts.append(ParserHelper.newline_character)
            POGGER.debug("#1")
        elif (
            output_html[-1] == ParserHelper.newline_character
            and transform_state.last_token
            and transform_state.last_token.is_text
        ):
            POGGER.debug("#2:$", transform_state.last_token)
            text_token = cast(TextMarkdownToken, transform_state.last_token)
            if not (end_token.was_forced and text_token.token_text.endswith("\n\x03")):
                token_parts.append(ParserHelper.newline_character)
        transform_state.is_in_code_block, transform_state.is_in_fenced_code_block = (
            False,
            False,
        )
        token_parts.extend(["</code></pre>", ParserHelper.newline_character])
        return "".join(token_parts)

    @classmethod
    def __handle_thematic_break_token(
        cls,
        output_html: str,
        next_token: MarkdownToken,
        transform_state: TransformState,
    ) -> str:
        """
        Handle the thematic break token.
        """
        _ = (next_token, transform_state)

        token_parts = [output_html]
        if output_html and output_html[-1] != ParserHelper.newline_character:
            token_parts.append(ParserHelper.newline_character)
        token_parts.extend(["<hr />", ParserHelper.newline_character])
        return "".join(token_parts)

    @classmethod
    def __handle_hard_break_token(
        cls,
        output_html: str,
        next_token: MarkdownToken,
        transform_state: TransformState,
    ) -> str:
        """
        Handle the hard line break token.
        """
        _ = (next_token, transform_state)

        return "".join([output_html, "<br />", ParserHelper.newline_character])

    @classmethod
    def __handle_start_atx_heading_token(
        cls,
        output_html: str,
        next_token: MarkdownToken,
        transform_state: TransformState,
    ) -> str:
        """
        Handle the start atx heading token.
        """

        atx_token = cast(AtxHeadingMarkdownToken, next_token)
        previous_token = transform_state.actual_tokens[
            transform_state.actual_token_index - 1
        ]

        token_parts = [output_html]
        if output_html.endswith("</ol>") or output_html.endswith("</ul>"):
            token_parts.append(ParserHelper.newline_character)
        elif previous_token.is_paragraph_end and not transform_state.is_in_loose_list:
            token_parts.append(ParserHelper.newline_character)
        token_parts.extend(["<h", str(atx_token.hash_count), ">"])
        return "".join(token_parts)

    @classmethod
    def __handle_end_atx_heading_token(
        cls,
        output_html: str,
        next_token: MarkdownToken,
        transform_state: TransformState,
    ) -> str:
        """
        Handle the end atx heading token.
        """
        _ = next_token

        fenced_token_index = transform_state.actual_token_index - 1
        while not transform_state.actual_tokens[fenced_token_index].is_atx_heading:
            fenced_token_index -= 1
        fenced_token = cast(
            SetextHeadingMarkdownToken,
            transform_state.actual_tokens[fenced_token_index],
        )

        return "".join(
            [
                output_html,
                "</h",
                str(fenced_token.hash_count),
                ">",
                ParserHelper.newline_character,
            ]
        )

    @classmethod
    def __handle_start_setext_heading_token(
        cls,
        output_html: str,
        next_token: MarkdownToken,
        transform_state: TransformState,
    ) -> str:
        """
        Handle the start setext heading token.
        """
        _ = transform_state
        setext_token = cast(SetextHeadingMarkdownToken, next_token)

        token_parts = [output_html]
        if output_html.endswith("</ol>") or output_html.endswith("</ul>"):
            token_parts.append(ParserHelper.newline_character)
        token_parts.extend(
            ["<h", "1" if setext_token.heading_character == "=" else "2", ">"]
        )
        transform_state.is_in_setext_block = True
        return "".join(token_parts)

    @classmethod
    def __handle_end_setext_heading_token(
        cls,
        output_html: str,
        next_token: MarkdownToken,
        transform_state: TransformState,
    ) -> str:
        """
        Handle the end setext heading token.
        """
        _ = next_token

        fenced_token_index = transform_state.actual_token_index - 1
        while not transform_state.actual_tokens[fenced_token_index].is_setext_heading:
            fenced_token_index -= 1
        fenced_token = cast(
            SetextHeadingMarkdownToken,
            transform_state.actual_tokens[fenced_token_index],
        )
        token_parts = [
            output_html,
            "</h",
            "1" if fenced_token.heading_character == "=" else "2",
            ">",
            ParserHelper.newline_character,
        ]
        transform_state.is_in_setext_block = False
        return "".join(token_parts)

    @classmethod
    def __handle_new_list_item_token(
        cls,
        output_html: str,
        next_token: MarkdownToken,
        transform_state: TransformState,
    ) -> str:
        """
        Handle the new list item token.
        """
        _ = next_token

        transform_state.add_trailing_text, transform_state.add_leading_text = (
            "</li>",
            "<li>",
        )
        token_parts = [output_html]
        if output_html and output_html[-1] == ">":
            token_parts.append(ParserHelper.newline_character)
        return "".join(token_parts)

    @classmethod
    def __handle_inline_code_span_token(
        cls,
        output_html: str,
        next_token: MarkdownToken,
        transform_state: TransformState,
    ) -> str:
        """
        Handle the code span token.
        """
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
        """
        Handle the raw html token.
        """
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
    def __handle_link_reference_definition_token(
        cls,
        output_html: str,
        next_token: MarkdownToken,
        transform_state: TransformState,
    ) -> str:
        """
        Handle the link reference definition token.
        """
        _ = (transform_state, next_token)

        return output_html

    @classmethod
    def __handle_pragma_token(
        cls,
        output_html: str,
        next_token: MarkdownToken,
        transform_state: TransformState,
    ) -> str:
        """
        Handle the link reference definition token.
        """
        _ = (transform_state, next_token)

        return output_html

    @classmethod
    def __handle_email_autolink_token(
        cls,
        output_html: str,
        next_token: MarkdownToken,
        transform_state: TransformState,
    ) -> str:
        """
        Handle the email autolink token.
        """
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
    def __handle_start_list_token(
        cls,
        output_html: str,
        next_token: MarkdownToken,
        transform_state: TransformState,
    ) -> str:
        """
        Handle the start unordered list token.
        """
        list_token = cast(ListStartMarkdownToken, next_token)
        transform_state.is_in_loose_list = (
            TransformToGfmListLooseness.calculate_list_looseness(
                transform_state.actual_tokens,
                transform_state.actual_token_index,
                list_token,
            )
        )
        if list_token.is_ordered_list_start:
            token_parts = ["<ol"]
            if list_token.list_start_content != "1":
                token_parts.extend(
                    [' start="', str(int(list_token.list_start_content)), '"']
                )
            token_parts.extend([">", ParserHelper.newline_character, "<li>"])
            transform_state.add_leading_text = "".join(token_parts)
        else:
            transform_state.add_leading_text = "".join(
                ["<ul>", ParserHelper.newline_character, "<li>"]
            )
        return output_html

    @classmethod
    def __handle_end_list_token(
        cls,
        output_html: str,
        next_token: MarkdownToken,
        transform_state: TransformState,
    ) -> str:
        """
        Handle the end list token for either an ordered or unordered list.
        """
        transform_state.is_in_loose_list = (
            TransformToGfmListLooseness.reset_list_looseness(
                transform_state.actual_tokens,
                transform_state.actual_token_index,
            )
        )
        transform_state.add_trailing_text = "".join(
            [
                "</li>",
                ParserHelper.newline_character,
                "</ul>" if next_token.is_unordered_list_end else "</ol>",
            ]
        )
        return output_html

    @classmethod
    def __handle_uri_autolink(
        cls,
        output_html: str,
        next_token: MarkdownToken,
        transform_state: TransformState,
    ) -> str:
        """
        Handle the uri autolink token.
        """
        _ = transform_state

        autolink_token = cast(UriAutolinkMarkdownToken, next_token)
        in_tag_pretext = InlineHelper.append_text(
            "",
            autolink_token.autolink_text,
            alternate_escape_map=TransformToGfm.uri_autolink_html_character_escape_map,
            add_text_signature=False,
        )

        tag_text_parts = []
        for next_character in in_tag_pretext:
            if next_character in TransformToGfm.raw_html_percent_escape_ascii_chars:
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
    def __handle_start_html_block_token(
        cls,
        output_html: str,
        next_token: MarkdownToken,
        transform_state: TransformState,
    ) -> str:
        """
        Handle the start html block token.
        """
        _ = next_token

        transform_state.is_in_html_block = True
        token_parts = []
        if (
            not output_html
            and transform_state.transform_stack
            and transform_state.transform_stack[-1].endswith("<li>")
        ):
            token_parts.append(ParserHelper.newline_character)
        else:
            previous_token = transform_state.actual_tokens[
                transform_state.actual_token_index - 1
            ]
            POGGER.debug(">previous_token>$>", previous_token)
            token_parts.append(output_html)
            if (
                not previous_token.is_list_end
                and previous_token.is_paragraph_end
                and not transform_state.is_in_loose_list
                or previous_token.is_list_end
            ):
                token_parts.append(ParserHelper.newline_character)
        return "".join(token_parts)

    @classmethod
    def __handle_end_html_block_token(
        cls,
        output_html: str,
        next_token: MarkdownToken,
        transform_state: TransformState,
    ) -> str:
        """
        Handle the end html block token.
        """
        _ = next_token

        transform_state.is_in_html_block = False
        return output_html

    @classmethod
    def __handle_start_emphasis_token(
        cls,
        output_html: str,
        next_token: MarkdownToken,
        transform_state: TransformState,
    ) -> str:
        """
        Handle the start emphasis token.
        """
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
        """
        Handle the end emphasis token.
        """
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
        """
        Handle the start link token.
        """
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
        """
        Handle the end link token.
        """
        _ = (next_token, transform_state)

        return f"{output_html}</a>"

    @classmethod
    def __handle_image_token(
        cls,
        output_html: str,
        next_token: MarkdownToken,
        transform_state: TransformState,
    ) -> str:
        """
        Handle the image token.
        """
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
