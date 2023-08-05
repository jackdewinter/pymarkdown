"""
Module to provide for an encapsulation of the fenced code block element.
"""

import logging
from typing import Optional, cast

from pymarkdown.general.parser_helper import ParserHelper
from pymarkdown.general.parser_logger import ParserLogger
from pymarkdown.general.position_marker import PositionMarker
from pymarkdown.tokens.leaf_markdown_token import LeafMarkdownToken
from pymarkdown.tokens.markdown_token import EndMarkdownToken, MarkdownToken
from pymarkdown.tokens.text_markdown_token import TextMarkdownToken
from pymarkdown.transform_gfm.transform_state import TransformState
from pymarkdown.transform_markdown.markdown_transform_context import (
    MarkdownTransformContext,
    RegisterHtmlTransformHandlersProtocol,
    RegisterMarkdownTransformHandlersProtocol,
)

POGGER = ParserLogger(logging.getLogger(__name__))


class FencedCodeBlockMarkdownToken(LeafMarkdownToken):
    """
    Class to provide for an encapsulation of the fenced code block element.
    """

    # pylint: disable=too-many-arguments
    def __init__(
        self,
        fence_character: str,
        fence_count: int,
        extracted_text: str,
        pre_extracted_text: str,
        text_after_extracted_text: str,
        pre_text_after_extracted_text: str,
        extracted_whitespace: str,
        extracted_whitespace_before_info_string: str,
        position_marker: PositionMarker,
    ) -> None:
        (
            self.__extracted_text,
            self.__pre_extracted_text,
            self.__extracted_whitespace_before_info_string,
            self.__text_after_extracted_text,
            self.__pre_text_after_extracted_text,
            self.__fence_character,
            self.__fence_count,
        ) = (
            extracted_text,
            pre_extracted_text,
            extracted_whitespace_before_info_string,
            text_after_extracted_text,
            pre_text_after_extracted_text,
            fence_character,
            fence_count,
        )
        LeafMarkdownToken.__init__(
            self,
            MarkdownToken._token_fenced_code_block,
            "",
            position_marker=position_marker,
            extracted_whitespace=extracted_whitespace,
            requires_end_token=True,
        )
        self.__compose_extra_data_field()

    # pylint: enable=too-many-arguments
    # pylint: disable=protected-access
    @staticmethod
    def get_markdown_token_type() -> str:
        """
        Get the type of markdown token for rehydration purposes.
        """
        return MarkdownToken._token_fenced_code_block

    # pylint: enable=protected-access

    @property
    def fence_character(self) -> str:
        """
        Returns the character used for the fence.
        """
        return self.__fence_character

    @property
    def fence_count(self) -> int:
        """
        Returns the number of fence characters used for the fence.
        """
        return self.__fence_count

    @property
    def extracted_text(self) -> str:
        """
        Returns the text extracted from the info string.
        """
        return self.__extracted_text

    @property
    def pre_extracted_text(self) -> str:
        """
        Returns the text extracted from the info string.
        """
        return self.__pre_extracted_text

    @property
    def text_after_extracted_text(self) -> str:
        """
        Returns the text extracted after the info string.
        """
        return self.__text_after_extracted_text

    @property
    def pre_text_after_extracted_text(self) -> str:
        """
        Returns the text extracted after after the info string.
        """
        return self.__pre_text_after_extracted_text

    @property
    def extracted_whitespace_before_info_string(self) -> str:
        """
        Returns any whitespace that was extracted before the info string was processed.
        """
        return self.__extracted_whitespace_before_info_string

    def __compose_extra_data_field(self) -> None:
        """
        Compose the object's self.extra_data field from the local object's variables.
        """
        self._set_extra_data(
            MarkdownToken.extra_data_separator.join(
                [
                    self.__fence_character,
                    str(self.__fence_count),
                    self.__extracted_text,
                    self.__pre_extracted_text,
                    self.__text_after_extracted_text,
                    self.__pre_text_after_extracted_text,
                    self.extracted_whitespace,
                    self.__extracted_whitespace_before_info_string,
                ]
            )
        )

    def register_for_markdown_transform(
        self, registration_function: RegisterMarkdownTransformHandlersProtocol
    ) -> None:
        """
        Register any rehydration handlers for leaf markdown tokens.
        """
        registration_function(
            FencedCodeBlockMarkdownToken,
            FencedCodeBlockMarkdownToken.__rehydrate_fenced_code_block,
            FencedCodeBlockMarkdownToken.__rehydrate_fenced_code_block_end,
        )

    @staticmethod
    def __rehydrate_fenced_code_block(
        context: MarkdownTransformContext,
        current_token: MarkdownToken,
        previous_token: Optional[MarkdownToken],
    ) -> str:
        """
        Rehydrate the fenced code block from the token.
        """
        _ = previous_token

        context.block_stack.append(current_token)
        current_fenced_token = cast(FencedCodeBlockMarkdownToken, current_token)

        code_block_start_parts = [
            current_fenced_token.extracted_whitespace,
            ParserHelper.repeat_string(
                current_fenced_token.fence_character, current_fenced_token.fence_count
            ),
            current_fenced_token.extracted_whitespace_before_info_string,
            current_fenced_token.pre_extracted_text
            or current_fenced_token.extracted_text,
            current_fenced_token.pre_text_after_extracted_text
            or current_fenced_token.text_after_extracted_text,
            ParserHelper.newline_character,
        ]

        return "".join(code_block_start_parts)

    @staticmethod
    def __rehydrate_fenced_code_block_end(
        context: MarkdownTransformContext,
        current_token: MarkdownToken,
        previous_token: Optional[MarkdownToken],
        next_token: Optional[MarkdownToken],
    ) -> str:  # sourcery skip: extract-method
        """
        Rehydrate the end of the fenced code block from the token.
        """
        del context.block_stack[-1]

        current_end_token = cast(EndMarkdownToken, current_token)
        if not current_end_token.was_forced:
            # We need to do this as the ending fence may be longer than the opening fence.
            assert current_token.extra_data is not None
            split_extra_data = current_token.extra_data.split(":")
            assert len(split_extra_data) >= 3
            extra_end_space = split_extra_data[1]
            fence_count = int(split_extra_data[2])

            current_start_token = cast(
                FencedCodeBlockMarkdownToken, current_end_token.start_markdown_token
            )

            fence_parts = [
                ""
                if previous_token is not None
                and (
                    previous_token.is_blank_line or previous_token.is_fenced_code_block
                )
                else ParserHelper.newline_character,
                current_end_token.extracted_whitespace,
                ParserHelper.repeat_string(
                    current_start_token.fence_character, fence_count
                ),
                extra_end_space,
                ParserHelper.newline_character,
            ]

            return "".join(fence_parts)

        assert previous_token is not None
        is_previous_code_block = previous_token.is_fenced_code_block
        return (
            ParserHelper.newline_character
            if next_token is not None and not is_previous_code_block
            else ""
        )

    @staticmethod
    def register_for_html_transform(
        register_handlers: RegisterHtmlTransformHandlersProtocol,
    ) -> None:
        """
        Register any functions required to generate HTML from the tokens.
        """
        register_handlers(
            FencedCodeBlockMarkdownToken,
            FencedCodeBlockMarkdownToken.__handle_start_fenced_code_block_token,
            FencedCodeBlockMarkdownToken.__handle_end_fenced_code_block_token,
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
