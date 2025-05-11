"""
Module to provide for an encapsulation of the inline code span element.
"""

from typing import Optional, Union, cast

from typing_extensions import override

from pymarkdown.general.parser_helper import ParserHelper
from pymarkdown.tokens.inline_markdown_token import InlineMarkdownToken
from pymarkdown.tokens.markdown_token import MarkdownToken
from pymarkdown.tokens.paragraph_markdown_token import ParagraphMarkdownToken
from pymarkdown.transform_gfm.transform_state import TransformState
from pymarkdown.transform_markdown.markdown_transform_context import (
    MarkdownTransformContext,
    RegisterHtmlTransformHandlersProtocol,
    RegisterMarkdownTransformHandlersProtocol,
)


class InlineCodeSpanMarkdownToken(InlineMarkdownToken):
    """
    Class to provide for an encapsulation of the inline code span element.
    """

    # pylint: disable=too-many-arguments
    def __init__(
        self,
        span_text: str,
        extracted_start_backticks: str,
        leading_whitespace: str,
        trailing_whitespace: str,
        is_in_table: bool,
        line_number: int,
        column_number: int,
    ) -> None:
        (
            self.__span_text,
            self.__extracted_start_backticks,
            self.__leading_whitespace,
            self.__trailing_whitespace,
            self.is_in_table,
        ) = (
            span_text,
            extracted_start_backticks,
            leading_whitespace,
            trailing_whitespace,
            is_in_table,
        )
        InlineMarkdownToken.__init__(
            self,
            MarkdownToken._token_inline_code_span,
            self.__compose_extra_data_field(),
            line_number=line_number,
            column_number=column_number,
        )

    def __compose_extra_data_field(self) -> str:
        """
        Compose the object's self.extra_data field from the local object's variables.
        """
        return MarkdownToken.extra_data_separator.join(
            [
                self.__span_text,
                self.__extracted_start_backticks,
                self.__leading_whitespace,
                self.__trailing_whitespace,
            ]
        )

    @override
    def _modify_token(self, field_name: str, field_value: Union[str, int]) -> bool:
        if field_name == "span_text" and isinstance(field_value, str):
            self.__span_text = field_value
            self._set_extra_data(self.__compose_extra_data_field())
            return True
        return False

    # pylint: disable=protected-access
    @staticmethod
    def get_markdown_token_type() -> str:
        """
        Get the type of markdown token for rehydration purposes.
        """
        return MarkdownToken._token_inline_code_span

    # pylint: enable=protected-access

    # pylint: enable=too-many-arguments
    @property
    def span_text(self) -> str:
        """
        Returns the text that is within the span.
        """
        return self.__span_text

    @property
    def extracted_start_backticks(self) -> str:
        """
        Returns the backticks that started the code span.
        """
        return self.__extracted_start_backticks

    @property
    def leading_whitespace(self) -> str:
        """
        Returns the whitespace at the start of the code span.
        """
        return self.__leading_whitespace

    @property
    def trailing_whitespace(self) -> str:
        """
        Returns the whitespace at the end of the code span.
        """
        return self.__trailing_whitespace

    def register_for_markdown_transform(
        self, registration_function: RegisterMarkdownTransformHandlersProtocol
    ) -> None:
        """
        Register any rehydration handlers for leaf markdown tokens.
        """
        registration_function(
            InlineCodeSpanMarkdownToken,
            InlineCodeSpanMarkdownToken.__rehydrate_inline_code_span,
            None,
        )

    @staticmethod
    def __rehydrate_inline_code_span(
        context: MarkdownTransformContext,
        current_token: MarkdownToken,
        previous_token: Optional[MarkdownToken],
    ) -> str:
        """
        Rehydrate the code span data from the token.
        """
        _ = previous_token

        if context.block_stack[-1].is_inline_link:
            return ""

        current_inline_token = cast(InlineCodeSpanMarkdownToken, current_token)
        span_text = ParserHelper.remove_all_from_text(
            current_inline_token.span_text, include_noops=True
        )
        leading_whitespace = ParserHelper.remove_all_from_text(
            current_inline_token.leading_whitespace
        )
        trailing_whitespace = ParserHelper.remove_all_from_text(
            current_inline_token.trailing_whitespace
        )

        if context.block_stack[-1].is_paragraph:
            block_paragraph_token = cast(
                ParagraphMarkdownToken, context.block_stack[-1]
            )
            (
                leading_whitespace,
                block_paragraph_token.rehydrate_index,
            ) = ParserHelper.recombine_string_with_whitespace(
                leading_whitespace,
                block_paragraph_token.extracted_whitespace,
                block_paragraph_token.rehydrate_index,
            )
            (
                span_text,
                block_paragraph_token.rehydrate_index,
            ) = ParserHelper.recombine_string_with_whitespace(
                span_text,
                block_paragraph_token.extracted_whitespace,
                block_paragraph_token.rehydrate_index,
            )
            (
                trailing_whitespace,
                block_paragraph_token.rehydrate_index,
            ) = ParserHelper.recombine_string_with_whitespace(
                trailing_whitespace,
                block_paragraph_token.extracted_whitespace,
                block_paragraph_token.rehydrate_index,
            )

        return "".join(
            [
                current_inline_token.extracted_start_backticks,
                leading_whitespace,
                span_text,
                trailing_whitespace,
                current_inline_token.extracted_start_backticks,
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
            InlineCodeSpanMarkdownToken,
            InlineCodeSpanMarkdownToken.__handle_inline_code_span_token,
            None,
        )

    @staticmethod
    def __handle_inline_code_span_token(
        output_html: str,
        next_token: MarkdownToken,
        transform_state: TransformState,
    ) -> str:
        _ = transform_state

        code_span_token = cast(InlineCodeSpanMarkdownToken, next_token)
        span_text = code_span_token.span_text
        if code_span_token.is_in_table and "\\" in span_text and "|" in span_text:
            new_span_text = ""
            span_index = 0
            while span_index < len(span_text):
                next_bar_index, before_bar_text = ParserHelper.collect_until_character(
                    span_text, span_index, "|"
                )
                assert next_bar_index is not None
                assert before_bar_text is not None
                if next_bar_index < len(span_text):
                    assert (
                        before_bar_text and before_bar_text[-1] == "\\"
                    )  # for it to be in a code span within a table, it has to be escaped
                    before_bar_text = before_bar_text[:-1]
                    new_span_text = f"{new_span_text}{before_bar_text}|"
                else:
                    new_span_text = f"{new_span_text}{before_bar_text}"
                span_index = next_bar_index + 1
            span_text = new_span_text

        return "".join(
            [
                output_html,
                "<code>",
                ParserHelper.resolve_all_from_text(span_text),
                "</code>",
            ]
        )
