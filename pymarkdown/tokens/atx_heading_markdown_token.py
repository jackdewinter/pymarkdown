"""
Module to provide for an encapsulation of the atx heading element.
"""

from typing import Optional, Union, cast

from typing_extensions import override

from pymarkdown.general.parser_helper import ParserHelper
from pymarkdown.general.position_marker import PositionMarker
from pymarkdown.tokens.leaf_markdown_token import LeafMarkdownToken
from pymarkdown.tokens.markdown_token import EndMarkdownToken, MarkdownToken
from pymarkdown.tokens.setext_heading_markdown_token import SetextHeadingMarkdownToken
from pymarkdown.transform_gfm.transform_state import TransformState
from pymarkdown.transform_markdown.markdown_transform_context import (
    MarkdownTransformContext,
    RegisterHtmlTransformHandlersProtocol,
    RegisterMarkdownTransformHandlersProtocol,
)


class AtxHeadingMarkdownToken(LeafMarkdownToken):
    """
    Class to provide for an encapsulation of the atx heading element.
    """

    def __init__(
        self,
        hash_count: int,
        remove_trailing_count: int,
        extracted_whitespace: str,
        position_marker: PositionMarker,
    ) -> None:
        self.__hash_count, self.__remove_trailing_count = (
            hash_count,
            remove_trailing_count,
        )

        LeafMarkdownToken.__init__(
            self,
            MarkdownToken._token_atx_heading,
            "",
            position_marker=position_marker,
            extracted_whitespace=extracted_whitespace,
            requires_end_token=True,
            can_force_close=False,
        )
        self.__compose_extra_data_field()

    # pylint: disable=protected-access
    @staticmethod
    def get_markdown_token_type() -> str:
        """
        Get the type of markdown token for rehydration purposes.
        """
        return MarkdownToken._token_atx_heading

    # pylint: enable=protected-access

    @override
    def _modify_token(self, field_name: str, field_value: Union[str, int]) -> bool:
        if (
            field_name == "hash_count"
            and isinstance(field_value, int)
            and 1 <= field_value <= 6
        ):
            self.__hash_count = field_value
            self.__compose_extra_data_field()
            return True
        return False

    @property
    def hash_count(self) -> int:
        """
        Returns the number of hash marks specified at the start of the line.
        """
        return self.__hash_count

    @property
    def remove_trailing_count(self) -> int:
        """
        Returns the number of hash marks specified at the end of the line.
        """
        return self.__remove_trailing_count

    def __compose_extra_data_field(self) -> None:
        """
        Compose the object's self.extra_data field from the local object's variables.
        """
        self._set_extra_data(
            MarkdownToken.extra_data_separator.join(
                [
                    str(self.__hash_count),
                    str(self.__remove_trailing_count),
                    self.extracted_whitespace,
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
            AtxHeadingMarkdownToken,
            AtxHeadingMarkdownToken.__rehydrate_atx_heading,
            AtxHeadingMarkdownToken.__rehydrate_atx_heading_end,
        )

    @staticmethod
    def __rehydrate_atx_heading(
        context: MarkdownTransformContext,
        current_token: MarkdownToken,
        previous_token: Optional[MarkdownToken],
    ) -> str:
        """
        Rehydrate the atx heading block from the token.
        """
        _ = previous_token

        context.block_stack.append(current_token)
        current_start_token = cast(AtxHeadingMarkdownToken, current_token)
        return f'{current_start_token.extracted_whitespace}{ParserHelper.repeat_string("#", current_start_token.hash_count)}'

    @staticmethod
    def __rehydrate_atx_heading_end(
        context: MarkdownTransformContext,
        current_token: MarkdownToken,
        previous_token: Optional[MarkdownToken],
        next_token: Optional[MarkdownToken],
    ) -> str:
        """
        Rehydrate the end of the atx heading block from the token.
        """
        _ = (previous_token, next_token)

        current_end_token = cast(EndMarkdownToken, current_token)
        current_start_token = cast(
            AtxHeadingMarkdownToken, current_end_token.start_markdown_token
        )

        del context.block_stack[-1]
        assert current_end_token.extra_end_data is not None
        return "".join(
            [
                current_end_token.extra_end_data,
                ParserHelper.repeat_string(
                    "#", current_start_token.remove_trailing_count
                )
                if current_start_token.remove_trailing_count
                else "",
                current_end_token.extracted_whitespace,
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
            AtxHeadingMarkdownToken,
            AtxHeadingMarkdownToken.__handle_start_atx_heading_token,
            AtxHeadingMarkdownToken.__handle_end_atx_heading_token,
        )

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
