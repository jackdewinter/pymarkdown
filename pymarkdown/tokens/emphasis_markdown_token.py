"""
Module to provide for an encapsulation of the inline emphasis element.
"""

from typing import List, Optional, Union, cast

from pymarkdown.general.parser_helper import ParserHelper
from pymarkdown.tokens.html_items import HtmlCloseTagItem, HtmlItems, HtmlOpenTagItem
from pymarkdown.tokens.inline_markdown_token import InlineMarkdownToken
from pymarkdown.tokens.markdown_token import EndMarkdownToken, MarkdownToken
from pymarkdown.transform_gfm.transform_state import TransformState
from pymarkdown.transform_markdown.markdown_transform_context import (
    MarkdownTransformContext,
    RegisterHtmlTransformHandlersProtocol,
    RegisterMarkdownTransformHandlersProtocol,
)


class EmphasisMarkdownToken(InlineMarkdownToken):
    """
    Class to provide for an encapsulation of the inline emphasis element.
    """

    def __init__(
        self,
        emphasis_length: int,
        emphasis_character: str,
        line_number: int = 0,
        column_number: int = 0,
    ) -> None:
        """
        Initialize an instance of the EmphasisMarkdownToken class.
        """
        self.__emphasis_length, self.__emphasis_character = (
            emphasis_length,
            emphasis_character,
        )
        InlineMarkdownToken.__init__(
            self,
            MarkdownToken._token_inline_emphasis,
            None,
            line_number=line_number,
            column_number=column_number,
            requires_end_token=True,
            can_force_close=False,
        )
        self.__compose_extra_data_field()

    def __compose_extra_data_field(self) -> None:
        """
        Compose the object's self.extra_data field from the local object's variables.
        """
        self._set_extra_data(
            MarkdownToken.extra_data_separator.join(
                [str(self.__emphasis_length), self.__emphasis_character]
            )
        )

    # pylint: disable=protected-access
    @staticmethod
    def get_markdown_token_type() -> str:
        """
        Get the type of markdown token for rehydration purposes.
        """
        return MarkdownToken._token_inline_emphasis

    # pylint: enable=protected-access

    @property
    def emphasis_length(self) -> int:
        """
        Returns the length of the current emphasis text.
        """
        return self.__emphasis_length

    @property
    def emphasis_character(self) -> str:
        """
        Returns the character used for the current emphasis text.
        """
        return self.__emphasis_character

    def _modify_token(self, field_name: str, field_value: Union[str, int]) -> bool:
        if (
            field_name == "emphasis_character"
            and isinstance(field_value, str)
            and field_value in ["*", "_"]
        ):
            self.__emphasis_character = field_value
            self.__compose_extra_data_field()
            return True
        return super()._modify_token(field_name, field_value)

    def register_for_markdown_transform(
        self, registration_function: RegisterMarkdownTransformHandlersProtocol
    ) -> None:
        """
        Register any rehydration handlers for leaf markdown tokens.
        """
        registration_function(
            EmphasisMarkdownToken,
            EmphasisMarkdownToken.__rehydrate_inline_emphaisis,
            EmphasisMarkdownToken.__rehydrate_inline_emphaisis_end,
        )

    @staticmethod
    def __rehydrate_inline_emphaisis(
        context: MarkdownTransformContext,
        current_token: MarkdownToken,
        previous_token: Optional[MarkdownToken],
    ) -> str:
        """
        Rehydrate the emphasis text from the token.
        """
        _ = previous_token

        emphasis_token = cast(EmphasisMarkdownToken, current_token)
        return (
            ""
            if context.block_stack[-1].is_inline_link
            else ParserHelper.repeat_string(
                emphasis_token.emphasis_character, emphasis_token.emphasis_length
            )
        )

    @staticmethod
    def __rehydrate_inline_emphaisis_end(
        context: MarkdownTransformContext,
        current_token: MarkdownToken,
        previous_token: Optional[MarkdownToken],
        next_token: Optional[MarkdownToken],
    ) -> str:
        """
        Rehydrate the emphasis end text from the token.
        """
        _ = (previous_token, next_token)

        emphasis_end_token = cast(EndMarkdownToken, current_token)
        emphasis_token = cast(
            EmphasisMarkdownToken, emphasis_end_token.start_markdown_token
        )

        return (
            ""
            if context.block_stack[-1].is_inline_link
            else ParserHelper.repeat_string(
                emphasis_token.emphasis_character,
                emphasis_token.emphasis_length,
            )
        )

    @staticmethod
    def register_for_html_transform(
        register_handlers: RegisterHtmlTransformHandlersProtocol,
    ) -> None:
        """
        Register any functions required to generate HTML from the tokens.
        """
        register_handlers(
            EmphasisMarkdownToken,
            EmphasisMarkdownToken.__handle_start_emphasis_token,
            EmphasisMarkdownToken.__handle_end_emphasis_token,
        )

    @staticmethod
    def __handle_start_emphasis_token(
        output_html: str,
        output_parts: List[HtmlItems],
        next_token: MarkdownToken,
        transform_state: TransformState,
    ) -> str:
        _ = transform_state

        emphasis_token = cast(EmphasisMarkdownToken, next_token)

        if emphasis_token.emphasis_character == "~":
            output_parts.append(HtmlOpenTagItem("del"))
        else:
            output_parts.append(
                HtmlOpenTagItem(
                    "em" if emphasis_token.emphasis_length == 1 else "strong"
                )
            )

        return EmphasisMarkdownToken.__handle_start_emphasis_token_old(
            output_html, emphasis_token
        )

    @staticmethod
    def __handle_end_emphasis_token(
        output_html: str,
        output_parts: List[HtmlItems],
        next_token: MarkdownToken,
        transform_state: TransformState,
    ) -> str:
        _ = transform_state

        end_token = cast(EndMarkdownToken, next_token)
        emphasis_token = cast(EmphasisMarkdownToken, end_token.start_markdown_token)

        if emphasis_token.emphasis_character == "~":
            output_parts.append(HtmlCloseTagItem("del"))
        else:
            output_parts.append(
                HtmlCloseTagItem(
                    "em" if emphasis_token.emphasis_length == 1 else "strong"
                )
            )

        return EmphasisMarkdownToken.__handle_end_emphasis_token_old(
            output_html, emphasis_token
        )

    @staticmethod
    def __handle_start_emphasis_token_old(
        output_html: str, emphasis_token: "EmphasisMarkdownToken"
    ) -> str:
        if emphasis_token.emphasis_character == "~":
            return f"{output_html}<del>"

        return "".join(
            [
                output_html,
                "<em>" if emphasis_token.emphasis_length == 1 else "<strong>",
            ]
        )

    @staticmethod
    def __handle_end_emphasis_token_old(
        output_html: str, emphasis_token: "EmphasisMarkdownToken"
    ) -> str:
        if emphasis_token.emphasis_character == "~":
            return f"{output_html}</del>"
        return "".join(
            [
                output_html,
                "</em>" if emphasis_token.emphasis_length == 1 else "</strong>",
            ]
        )
