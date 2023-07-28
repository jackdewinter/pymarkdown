"""
Module to provide for the handlers for leaf tokens to allow transformation into HTML.
"""
import logging
from typing import Callable, cast

from pymarkdown.parser_helper import ParserHelper
from pymarkdown.parser_logger import ParserLogger
from pymarkdown.tokens.leaf_markdown_token import (
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
from pymarkdown.tokens.markdown_token import EndMarkdownToken, MarkdownToken
from pymarkdown.tokens.text_markdown_token import TextMarkdownToken
from pymarkdown.transform_state import TransformState

POGGER = ParserLogger(logging.getLogger(__name__))


class TransformToGfmLeafTokenHandlers:
    """
    Class to provide for the handlers for leaf tokens to allow transformation into HTML.
    """

    @staticmethod
    def register_handlers(
        register_fn: Callable[
            [
                type,
                Callable[[str, MarkdownToken, TransformState], str],
                Callable[[str, MarkdownToken, TransformState], str],
            ],
            None,
        ]
    ) -> None:
        """
        Register the handlers for this module.
        """
        register_fn(
            ThematicBreakMarkdownToken,
            TransformToGfmLeafTokenHandlers.__handle_thematic_break_token,
            TransformToGfmLeafTokenHandlers.null,
        )
        register_fn(
            AtxHeadingMarkdownToken,
            TransformToGfmLeafTokenHandlers.__handle_start_atx_heading_token,
            TransformToGfmLeafTokenHandlers.__handle_end_atx_heading_token,
        )
        register_fn(
            SetextHeadingMarkdownToken,
            TransformToGfmLeafTokenHandlers.__handle_start_setext_heading_token,
            TransformToGfmLeafTokenHandlers.__handle_end_setext_heading_token,
        )
        register_fn(
            IndentedCodeBlockMarkdownToken,
            TransformToGfmLeafTokenHandlers.__handle_start_indented_code_block_token,
            TransformToGfmLeafTokenHandlers.__handle_end_indented_code_block_token,
        )
        register_fn(
            FencedCodeBlockMarkdownToken,
            TransformToGfmLeafTokenHandlers.__handle_start_fenced_code_block_token,
            TransformToGfmLeafTokenHandlers.__handle_end_fenced_code_block_token,
        )
        register_fn(
            HtmlBlockMarkdownToken,
            TransformToGfmLeafTokenHandlers.__handle_start_html_block_token,
            TransformToGfmLeafTokenHandlers.__handle_end_html_block_token,
        )
        register_fn(
            LinkReferenceDefinitionMarkdownToken,
            TransformToGfmLeafTokenHandlers.__handle_link_reference_definition_token,
            TransformToGfmLeafTokenHandlers.null,
        )
        register_fn(
            ParagraphMarkdownToken,
            TransformToGfmLeafTokenHandlers.__handle_start_paragraph_token,
            TransformToGfmLeafTokenHandlers.__handle_end_paragraph_token,
        )
        register_fn(
            BlankLineMarkdownToken,
            TransformToGfmLeafTokenHandlers.__handle_blank_line_token,
            TransformToGfmLeafTokenHandlers.null,
        )

    @staticmethod
    def null(
        output_html: str,
        next_token: MarkdownToken,
        transform_state: TransformState,
    ) -> str:
        """
        Do nothing.
        """
        _ = (next_token, transform_state)
        return output_html

    @staticmethod
    def __handle_thematic_break_token(
        output_html: str,
        next_token: MarkdownToken,
        transform_state: TransformState,
    ) -> str:
        _ = (next_token, transform_state)

        token_parts = [output_html]
        if output_html and output_html[-1] != ParserHelper.newline_character:
            token_parts.append(ParserHelper.newline_character)
        token_parts.extend(["<hr />", ParserHelper.newline_character])
        return "".join(token_parts)

    @staticmethod
    def __handle_start_atx_heading_token(
        output_html: str,
        next_token: MarkdownToken,
        transform_state: TransformState,
    ) -> str:
        atx_token = cast(AtxHeadingMarkdownToken, next_token)
        previous_token = transform_state.actual_tokens[
            transform_state.actual_token_index - 1
        ]

        token_parts = [output_html]
        if (output_html.endswith("</ol>") or output_html.endswith("</ul>")) or (
            previous_token.is_paragraph_end and not transform_state.is_in_loose_list
        ):
            token_parts.append(ParserHelper.newline_character)
        token_parts.extend(["<h", str(atx_token.hash_count), ">"])
        return "".join(token_parts)

    @staticmethod
    def __handle_end_atx_heading_token(
        output_html: str,
        next_token: MarkdownToken,
        transform_state: TransformState,
    ) -> str:
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

    @staticmethod
    def __handle_start_setext_heading_token(
        output_html: str,
        next_token: MarkdownToken,
        transform_state: TransformState,
    ) -> str:
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

    @staticmethod
    def __handle_end_setext_heading_token(
        output_html: str,
        next_token: MarkdownToken,
        transform_state: TransformState,
    ) -> str:
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

    @staticmethod
    def __handle_start_paragraph_token(
        output_html: str,
        next_token: MarkdownToken,
        transform_state: TransformState,
    ) -> str:
        _ = next_token
        token_parts = [output_html]
        if output_html and output_html[-1] != ParserHelper.newline_character:
            token_parts.append(ParserHelper.newline_character)
        if transform_state.is_in_loose_list:
            token_parts.append("<p>")
        return "".join(token_parts)

    @staticmethod
    def __handle_end_paragraph_token(
        output_html: str,
        next_token: MarkdownToken,
        transform_state: TransformState,
    ) -> str:
        _ = next_token

        return (
            f"{output_html}</p>{ParserHelper.newline_character}"
            if transform_state.is_in_loose_list
            else output_html
        )

    @classmethod
    def __handle_start_indented_code_block_token(
        cls,
        output_html: str,
        next_token: MarkdownToken,
        transform_state: TransformState,
    ) -> str:
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
    def __handle_start_html_block_token(
        cls,
        output_html: str,
        next_token: MarkdownToken,
        transform_state: TransformState,
    ) -> str:
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
        _ = next_token

        transform_state.is_in_html_block = False
        return output_html

    @classmethod
    def __handle_link_reference_definition_token(
        cls,
        output_html: str,
        next_token: MarkdownToken,
        transform_state: TransformState,
    ) -> str:
        _ = (transform_state, next_token)

        return output_html

    @classmethod
    def __handle_blank_line_token(
        cls,
        output_html: str,
        next_token: MarkdownToken,
        transform_state: TransformState,
    ) -> str:
        _ = next_token

        if transform_state.is_in_html_block:
            output_html = f"{output_html}{ParserHelper.newline_character}"
        return output_html
