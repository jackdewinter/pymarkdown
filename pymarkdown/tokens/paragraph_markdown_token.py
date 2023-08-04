"""
Module to provide for an encapsulation of the paragraph element.
"""

from typing import Optional, cast

from pymarkdown.general.parser_helper import ParserHelper
from pymarkdown.general.position_marker import PositionMarker
from pymarkdown.tokens.leaf_markdown_token import LeafMarkdownToken
from pymarkdown.tokens.markdown_token import EndMarkdownToken, MarkdownToken
from pymarkdown.transform_gfm.transform_state import TransformState
from pymarkdown.transform_markdown.markdown_transform_context import (
    MarkdownTransformContext,
    RegisterHtmlTransformHandlersProtocol,
    RegisterMarkdownTransformHandlersProtocol,
)


class ParagraphMarkdownToken(LeafMarkdownToken):
    """
    Class to provide for an encapsulation of the paragraph element.
    """

    def __init__(
        self, extracted_whitespace: str, position_marker: PositionMarker
    ) -> None:
        self.__extracted_whitespace: str = extracted_whitespace
        self.__final_whitespace, self.rehydrate_index = (
            "",
            0,
        )
        LeafMarkdownToken.__init__(
            self,
            MarkdownToken._token_paragraph,
            "",
            position_marker=position_marker,
            requires_end_token=True,
        )
        self.__compose_extra_data_field()

    # pylint: disable=protected-access
    @staticmethod
    def get_markdown_token_type() -> str:
        """
        Get the type of markdown token for rehydration purposes.
        """
        return MarkdownToken._token_paragraph

    # pylint: enable=protected-access

    @property
    def extracted_whitespace(self) -> str:
        """
        Returns any whitespace that was extracted before the processing of this element occurred.
        """
        return self.__extracted_whitespace

    @property
    def final_whitespace(self) -> str:
        """
        Returns any final whitespace at the end of the paragraph that was removed.
        """
        return self.__final_whitespace

    def __compose_extra_data_field(self) -> None:
        """
        Compose the object's self.extra_data field from the local object's variables.
        """

        self._set_extra_data(
            f"{self.__extracted_whitespace}{MarkdownToken.extra_data_separator}{self.__final_whitespace}"
            if self.final_whitespace
            else self.__extracted_whitespace
        )

    def add_whitespace(self, whitespace_to_add: str) -> None:
        """
        Add extra whitespace to the end of the current paragraph.  Should only be
        used when combining text blocks in a paragraph.
        """

        self.__extracted_whitespace = (
            f"{self.__extracted_whitespace}{whitespace_to_add}"
        )
        self.__compose_extra_data_field()

    def set_final_whitespace(self, whitespace_to_set: str) -> None:
        """
        Set the final whitespace for the paragraph. That is any whitespace at the very
        end of the paragraph, removed to prevent hard lines at the end.
        """

        self.__final_whitespace = whitespace_to_set
        self.__compose_extra_data_field()

    def register_for_markdown_transform(
        self, registration_function: RegisterMarkdownTransformHandlersProtocol
    ) -> None:
        """
        Register any rehydration handlers for leaf markdown tokens.
        """
        registration_function(
            ParagraphMarkdownToken,
            ParagraphMarkdownToken.__rehydrate_paragraph,
            ParagraphMarkdownToken.__rehydrate_paragraph_end,
        )

    @staticmethod
    def __rehydrate_paragraph(
        context: MarkdownTransformContext,
        current_token: MarkdownToken,
        previous_token: Optional[MarkdownToken],
    ) -> str:
        """
        Rehydrate the paragraph block from the token.
        """
        _ = previous_token

        context.block_stack.append(current_token)

        current_paragraph_token = cast(ParagraphMarkdownToken, current_token)
        current_paragraph_token.rehydrate_index = 0
        extracted_whitespace = current_paragraph_token.extracted_whitespace
        if ParserHelper.newline_character in extracted_whitespace:
            line_end_index = extracted_whitespace.index(ParserHelper.newline_character)
            extracted_whitespace = extracted_whitespace[:line_end_index]
        return ParserHelper.resolve_all_from_text(extracted_whitespace)

    @staticmethod
    def __rehydrate_paragraph_end(
        context: MarkdownTransformContext,
        current_token: MarkdownToken,
        previous_token: Optional[MarkdownToken],
        next_token: Optional[MarkdownToken],
    ) -> str:
        """
        Rehydrate the end of the paragraph block from the token.
        """
        _ = (previous_token, next_token)

        top_stack_token = cast(ParagraphMarkdownToken, context.block_stack[-1])
        del context.block_stack[-1]

        current_end_token = cast(EndMarkdownToken, current_token)
        current_start_token = cast(
            ParagraphMarkdownToken, current_end_token.start_markdown_token
        )

        rehydrate_index, expected_rehydrate_index = (
            current_start_token.rehydrate_index,
            ParserHelper.count_newlines_in_text(
                current_start_token.extracted_whitespace
            ),
        )
        assert (
            rehydrate_index == expected_rehydrate_index
        ), f"rehydrate_index={rehydrate_index};expected_rehydrate_index={expected_rehydrate_index}"
        return f"{top_stack_token.final_whitespace}{ParserHelper.newline_character}"

    @staticmethod
    def register_for_html_transform(
        register_handlers: RegisterHtmlTransformHandlersProtocol,
    ) -> None:
        """
        Register any functions required to generate HTML from the tokens.
        """
        register_handlers(
            ParagraphMarkdownToken,
            ParagraphMarkdownToken.__handle_start_paragraph_token,
            ParagraphMarkdownToken.__handle_end_paragraph_token,
        )

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
