"""
Module to provide for an encapsulation of the indented code block element.
"""

from typing import Callable, Optional

from pymarkdown.parser_helper import ParserHelper
from pymarkdown.tokens.leaf_markdown_token import LeafMarkdownToken
from pymarkdown.tokens.markdown_token import MarkdownToken
from pymarkdown.transform_markdown.markdown_transform_context import (
    MarkdownTransformContext,
)
from pymarkdown.transform_state import TransformState


class IndentedCodeBlockMarkdownToken(LeafMarkdownToken):
    """
    Class to provide for an encapsulation of the indented code block element.
    """

    def __init__(
        self, extracted_whitespace: str, line_number: int, column_number: int
    ) -> None:
        self.__indented_whitespace = ""
        LeafMarkdownToken.__init__(
            self,
            MarkdownToken._token_indented_code_block,
            extracted_whitespace,
            line_number=line_number,
            column_number=column_number,
            extracted_whitespace=extracted_whitespace,
            requires_end_token=True,
        )
        self.__compose_extra_data_field()

    # pylint: disable=protected-access
    @staticmethod
    def get_markdown_token_type() -> str:
        """
        Get the type of markdown token for rehydration purposes.
        """
        return MarkdownToken._token_indented_code_block

    # pylint: enable=protected-access

    @property
    def indented_whitespace(self) -> str:
        """
        Returns any indented whitespace that comes before the text.
        """
        return self.__indented_whitespace

    def __compose_extra_data_field(self) -> None:
        """
        Compose the object's self.extra_data field from the local object's variables.
        """
        self._set_extra_data(
            MarkdownToken.extra_data_separator.join(
                [self.extracted_whitespace, self.indented_whitespace]
            )
        )

    def add_indented_whitespace(self, indented_whitespace: str) -> None:
        """
        Add the indented whitespace that comes before the text.
        """
        self.__indented_whitespace = (
            f"{self.__indented_whitespace}{ParserHelper.newline_character}"
            + f"{indented_whitespace}"
        )
        self.__compose_extra_data_field()

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
            IndentedCodeBlockMarkdownToken,
            IndentedCodeBlockMarkdownToken.__rehydrate_indented_code_block,
            IndentedCodeBlockMarkdownToken.__rehydrate_indented_code_block_end,
        )

    @staticmethod
    def __rehydrate_indented_code_block(
        context: MarkdownTransformContext,
        current_token: MarkdownToken,
        previous_token: Optional[MarkdownToken],
    ) -> str:
        """
        Rehydrate the indented code block from the token.
        """
        _ = previous_token

        context.block_stack.append(current_token)
        return ""

    @staticmethod
    def __rehydrate_indented_code_block_end(
        context: MarkdownTransformContext,
        current_token: MarkdownToken,
        previous_token: Optional[MarkdownToken],
        next_token: Optional[MarkdownToken],
    ) -> str:
        """
        Rehydrate the end of the indented code block from the token.
        """
        _ = (current_token, previous_token, next_token)

        del context.block_stack[-1]
        return ""

    @staticmethod
    def register_for_html_transform(
        register_handlers: Callable[
            [
                type,
                Callable[[str, MarkdownToken, TransformState], str],
                Optional[Callable[[str, MarkdownToken, TransformState], str]],
            ],
            None,
        ]
    ) -> None:
        """
        Register any functions required to generate HTML from the tokens.
        """
        register_handlers(
            IndentedCodeBlockMarkdownToken,
            IndentedCodeBlockMarkdownToken.__handle_start_indented_code_block_token,
            IndentedCodeBlockMarkdownToken.__handle_end_indented_code_block_token,
        )

    @staticmethod
    def __handle_start_indented_code_block_token(
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

    @staticmethod
    def __handle_end_indented_code_block_token(
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
