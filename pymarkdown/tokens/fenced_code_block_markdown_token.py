"""
Module to provide for an encapsulation of the fenced code block element.
"""

from typing import Callable, Optional, cast

from pymarkdown.parser_helper import ParserHelper
from pymarkdown.position_marker import PositionMarker
from pymarkdown.tokens.leaf_markdown_token import LeafMarkdownToken
from pymarkdown.tokens.markdown_token import EndMarkdownToken, MarkdownToken
from pymarkdown.transform_markdown.markdown_transform_context import (
    MarkdownTransformContext,
)


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
        self,
        registration_function: Callable[
            [
                type,
                Callable[
                    [MarkdownTransformContext, MarkdownToken, Optional[MarkdownToken]],
                    str,
                ],
                Optional[
                    Callable[
                        [
                            MarkdownTransformContext,
                            MarkdownToken,
                            Optional[MarkdownToken],
                            Optional[MarkdownToken],
                        ],
                        str,
                    ]
                ],
            ],
            None,
        ],
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
