"""
Module to provide for an encapsulation of the setext heading element.
"""

from typing import Optional, cast

from pymarkdown.general.parser_helper import ParserHelper
from pymarkdown.general.position_marker import PositionMarker
from pymarkdown.tokens.leaf_markdown_token import LeafMarkdownToken
from pymarkdown.tokens.markdown_token import EndMarkdownToken, MarkdownToken
from pymarkdown.tokens.paragraph_markdown_token import ParagraphMarkdownToken
from pymarkdown.transform_gfm.transform_state import TransformState
from pymarkdown.transform_markdown.markdown_transform_context import (
    MarkdownTransformContext,
    RegisterHtmlTransformHandlersProtocol,
    RegisterMarkdownTransformHandlersProtocol,
)


class SetextHeadingMarkdownToken(LeafMarkdownToken):
    """
    Class to provide for an encapsulation of the setext heading element.
    """

    # pylint: disable=too-many-arguments
    def __init__(
        self,
        heading_character: str,
        heading_character_count: int,
        extracted_whitespace: str,
        position_marker: PositionMarker,
        para_token: ParagraphMarkdownToken,
    ) -> None:
        (
            self.__heading_character,
            self.__heading_character_count,
            self.__final_whitespace,
            self.__original_line_number,
            self.__original_column_number,
        ) = (
            heading_character,
            heading_character_count,
            "",
            para_token.line_number if para_token else -1,
            para_token.column_number if para_token else -1,
        )

        if self.__heading_character == "=":
            self.__hash_count = 1
        elif self.__heading_character == "-":
            self.__hash_count = 2
        else:
            # TODO better way to do this
            self.__hash_count = -1

        LeafMarkdownToken.__init__(
            self,
            MarkdownToken._token_setext_heading,
            "",
            position_marker=position_marker,
            extracted_whitespace=extracted_whitespace,
            requires_end_token=True,
            can_force_close=False,
        )
        self.__compose_extra_data_field()

    # pylint: enable=too-many-arguments
    # pylint: disable=protected-access
    @staticmethod
    def get_markdown_token_type() -> str:
        """
        Get the type of markdown token for rehydration purposes.
        """
        return MarkdownToken._token_setext_heading

    # pylint: enable=protected-access

    @property
    def final_whitespace(self) -> str:
        """
        Returns any final whitespace at the end of the heading that was removed.
        """
        return self.__final_whitespace

    @property
    def heading_character(self) -> str:
        """
        Returns the character associated with the heading start.
        """
        return self.__heading_character

    @property
    def hash_count(self) -> int:
        """
        Returns the count in equivalence of "Atx Hash" counts.
        """
        return self.__hash_count

    @property
    def heading_character_count(self) -> int:
        """
        Returns the count of characters associated with the heading start.
        """
        return self.__heading_character_count

    @property
    def original_line_number(self) -> int:
        """
        Returns the line number where this element actually started.
        """
        return self.__original_line_number

    @property
    def original_column_number(self) -> int:
        """
        Returns the column number where this element actually started.
        """
        return self.__original_column_number

    def set_final_whitespace(self, whitespace_to_set: str) -> None:
        """
        Set the final whitespace for the paragraph. That is any whitespace at the very
        end of the paragraph, removed to prevent hard lines at the end.
        """

        self.__final_whitespace = whitespace_to_set
        self.__compose_extra_data_field()

    def __compose_extra_data_field(self) -> None:
        """
        Compose the object's self.extra_data field from the local object's variables.
        """

        original_location = (
            f"({self.original_line_number},{self.original_column_number})"
        )
        field_parts = [
            self.__heading_character,
            str(self.__heading_character_count),
            self.extracted_whitespace,
            original_location,
        ]
        if self.final_whitespace:
            field_parts.append(self.final_whitespace)
        self._set_extra_data(MarkdownToken.extra_data_separator.join(field_parts))

    def register_for_markdown_transform(
        self, registration_function: RegisterMarkdownTransformHandlersProtocol
    ) -> None:
        """
        Register any rehydration handlers for leaf markdown tokens.
        """
        registration_function(
            SetextHeadingMarkdownToken,
            SetextHeadingMarkdownToken.__rehydrate_setext_heading,
            SetextHeadingMarkdownToken.__rehydrate_setext_heading_end,
        )

    @staticmethod
    def __rehydrate_setext_heading(
        context: MarkdownTransformContext,
        current_token: MarkdownToken,
        previous_token: Optional[MarkdownToken],
    ) -> str:
        """
        Rehydrate the setext heading from the token.
        """
        _ = previous_token

        context.block_stack.append(current_token)
        current_setext_token = cast(SetextHeadingMarkdownToken, current_token)
        return current_setext_token.extracted_whitespace

    @staticmethod
    def __rehydrate_setext_heading_end(
        context: MarkdownTransformContext,
        current_token: MarkdownToken,
        previous_token: Optional[MarkdownToken],
        next_token: Optional[MarkdownToken],
    ) -> str:
        """
        Rehydrate the end of the setext heading block from the token.
        """
        _ = (previous_token, next_token)

        current_start_token = cast(SetextHeadingMarkdownToken, context.block_stack[-1])
        current_end_token = cast(EndMarkdownToken, current_token)

        heading_character = current_start_token.heading_character
        heading_character_count = current_start_token.heading_character_count
        final_whitespace = current_start_token.final_whitespace
        del context.block_stack[-1]
        assert (
            current_end_token.extra_end_data is not None
        ), "extra_end_data must be defined by now"
        return "".join(
            [
                final_whitespace,
                ParserHelper.newline_character,
                current_end_token.extracted_whitespace,
                ParserHelper.repeat_string(heading_character, heading_character_count),
                current_end_token.extra_end_data,
                ParserHelper.newline_character,
            ]
        )

    @staticmethod
    def register_for_html_transform(
        register_handlers: RegisterHtmlTransformHandlersProtocol,
    ) -> None:
        """
        Register any functions required to generate HTML from the tokens.
        """
        register_handlers(
            SetextHeadingMarkdownToken,
            SetextHeadingMarkdownToken.__handle_start_setext_heading_token,
            SetextHeadingMarkdownToken.__handle_end_setext_heading_token,
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
