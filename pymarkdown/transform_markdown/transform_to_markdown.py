"""
Module to provide for a transformation from tokens to a markdown document.
"""
import collections
import inspect
import logging
from typing import Dict, List, Optional, Tuple, cast

from pymarkdown.extensions.extension_token_types import ExtensionTokenTypes
from pymarkdown.extensions.pragma_token import PragmaToken
from pymarkdown.general.parser_helper import ParserHelper
from pymarkdown.general.parser_logger import ParserLogger
from pymarkdown.general.tab_helper import TabHelper
from pymarkdown.tokens.block_quote_markdown_token import BlockQuoteMarkdownToken
from pymarkdown.tokens.container_markdown_token import ContainerMarkdownToken
from pymarkdown.tokens.end_of_stream_token import SpecialMarkdownToken
from pymarkdown.tokens.inline_markdown_token import InlineMarkdownToken
from pymarkdown.tokens.leaf_markdown_token import LeafMarkdownToken
from pymarkdown.tokens.list_start_markdown_token import ListStartMarkdownToken
from pymarkdown.tokens.markdown_token import (
    EndMarkdownToken,
    MarkdownToken,
    MarkdownTokenClass,
)
from pymarkdown.tokens.new_list_item_markdown_token import NewListItemMarkdownToken
from pymarkdown.tokens.ordered_list_start_markdown_token import (
    OrderedListStartMarkdownToken,
)
from pymarkdown.tokens.token_types import TokenTypes
from pymarkdown.tokens.unordered_list_start_markdown_token import (
    UnorderedListStartMarkdownToken,
)
from pymarkdown.transform_markdown.markdown_transform_context import (
    EndMarkdownContainerTokenTransformProtocol,
    EndMarkdownTokenTransformProtocol,
    MarkdownTransformContext,
    StartMarkdownContainerTokenTransformProtocol,
    StartMarkdownTokenTransformProtocol,
)
from pymarkdown.transform_markdown.transform_block_quote import TransformBlockQuote
from pymarkdown.transform_markdown.transform_containers import (
    MarkdownChangeRecord,
    TransformContainers,
)
from pymarkdown.transform_markdown.transform_list_block import TransformListBlock
from pymarkdown.transform_markdown.transform_new_list_item import TransformNewListItem

POGGER = ParserLogger(logging.getLogger(__name__))


# pylint: disable=too-many-lines
class TransformToMarkdown:
    """
    Class to provide for a transformation from tokens to a markdown document.
    """

    def __init__(self) -> None:
        """
        Initializes a new instance of the TransformToMarkdown class.
        """

        self.context = MarkdownTransformContext()

        self.start_container_token_handlers: Dict[
            str,
            StartMarkdownContainerTokenTransformProtocol,
        ] = {}
        self.end_container_token_handlers: Dict[
            str,
            EndMarkdownContainerTokenTransformProtocol,
        ] = {}
        self.start_token_handlers: Dict[
            str,
            StartMarkdownTokenTransformProtocol,
        ] = {}
        self.end_token_handlers: Dict[
            str,
            EndMarkdownTokenTransformProtocol,
        ] = {}

        self.register_container_handlers(
            OrderedListStartMarkdownToken,
            TransformListBlock.rehydrate_list_start,
            TransformListBlock.rehydrate_list_start_end,
        )
        self.register_container_handlers(
            UnorderedListStartMarkdownToken,
            TransformListBlock.rehydrate_list_start,
            TransformListBlock.rehydrate_list_start_end,
        )
        self.register_container_handlers(
            NewListItemMarkdownToken, TransformNewListItem.rehydrate_next_list_item
        )
        self.register_container_handlers(
            BlockQuoteMarkdownToken,
            TransformBlockQuote.rehydrate_block_quote,
            TransformBlockQuote.rehydrate_block_quote_end,
        )

        ert = TokenTypes.get_inline_token_types()
        ert.extend(TokenTypes.get_leaf_token_types())
        ert.extend(TokenTypes.get_special_token_types())
        ert.extend(ExtensionTokenTypes.get_token_types())
        for token_type in ert:
            token_init_fn = token_type.__dict__["__init__"]
            init_parameters = {
                i: "" for i in inspect.getfullargspec(token_init_fn)[0] if i != "self"
            }
            handler_instance = token_type(**init_parameters)
            handler_instance.register_for_markdown_transform(self.register_handlers)

    def __get_token_type_info(self, token_type: type) -> Tuple[str, MarkdownTokenClass]:
        current_token_type = token_type
        token_name = None
        token_class = None
        assert "get_markdown_token_type" in token_type.__dict__
        token_name = token_type.__dict__["get_markdown_token_type"].__func__()

        while current_token_type not in [
            ContainerMarkdownToken,
            LeafMarkdownToken,
            InlineMarkdownToken,
            SpecialMarkdownToken,
        ]:
            new_bases = list(current_token_type.__bases__)
            assert len(new_bases) == 1
            current_token_type = new_bases[0]
        if current_token_type == ContainerMarkdownToken:
            token_class = MarkdownTokenClass.CONTAINER_BLOCK
        elif current_token_type == LeafMarkdownToken:
            token_class = MarkdownTokenClass.LEAF_BLOCK
        elif current_token_type == InlineMarkdownToken:
            token_class = MarkdownTokenClass.INLINE_BLOCK
        else:
            assert current_token_type == SpecialMarkdownToken
            token_class = MarkdownTokenClass.SPECIAL

        assert token_name is not None
        assert token_class is not None
        return token_name, token_class

    def register_handlers(
        self,
        token_type: type,
        start_token_handler: StartMarkdownTokenTransformProtocol,
        end_token_handler: Optional[EndMarkdownTokenTransformProtocol] = None,
    ) -> None:
        """
        Register the handlers necessary to deal with token's start and end.
        """
        type_name, type_class = self.__get_token_type_info(token_type)

        assert type_class in [
            MarkdownTokenClass.LEAF_BLOCK,
            MarkdownTokenClass.INLINE_BLOCK,
            MarkdownTokenClass.SPECIAL,
        ]

        self.start_token_handlers[type_name] = start_token_handler
        if end_token_handler:
            self.end_token_handlers[type_name] = end_token_handler

    def register_container_handlers(
        self,
        token_type: type,
        start_token_handler: StartMarkdownContainerTokenTransformProtocol,
        end_token_handler: Optional[EndMarkdownContainerTokenTransformProtocol] = None,
    ) -> None:
        """
        Register the handlers necessary to deal with token's start and end.
        """
        type_name, type_class = self.__get_token_type_info(token_type)
        assert type_class in [MarkdownTokenClass.CONTAINER_BLOCK]

        self.start_container_token_handlers[type_name] = start_token_handler
        if end_token_handler:
            self.end_container_token_handlers[type_name] = end_token_handler

    def transform(self, actual_tokens: List[MarkdownToken]) -> str:  # noqa: C901
        """
        Transform the incoming token stream back into Markdown.
        """
        container_stack: List[MarkdownToken] = []
        container_records: List[MarkdownChangeRecord] = []
        (
            transformed_data,
            previous_token,
            pragma_token,
        ) = ("", None, None)

        POGGER.debug("---\nTransformToMarkdown\n---")

        for token_index, current_token in enumerate(actual_tokens):
            if current_token.is_list_start:
                list_token = cast(ListStartMarkdownToken, current_token)
                list_token.reset_last_list_item()

            next_token = (
                actual_tokens[token_index + 1]
                if token_index < len(actual_tokens) - 1
                else None
            )

            POGGER.debug(
                f"pre-h>current_token>:{ParserHelper.make_value_visible(current_token)}:"
            )
            (
                new_data,
                pragma_token,
            ) = self.__process_next_token(
                current_token,
                previous_token,
                next_token,
                transformed_data,
                actual_tokens,
                token_index,
            )

            POGGER.debug(
                f"post-h>new_data>:{ParserHelper.make_value_visible(new_data)}:"
            )
            transformed_data_length_before_add = len(transformed_data)
            POGGER.debug(
                f"post-h>transformed_data>:{ParserHelper.make_value_visible(transformed_data)}:"
            )
            transformed_data += new_data
            POGGER.debug(
                f"post-h>transformed_data>:{ParserHelper.make_value_visible(transformed_data)}:"
            )

            transformed_data = TransformContainers.handle_current_token(
                current_token,
                transformed_data,
                container_stack,
                container_records,
                transformed_data_length_before_add,
                actual_tokens,
            )

            POGGER.debug("---")
            previous_token = current_token

        transformed_data = self.__correct_for_final_newline(
            transformed_data, actual_tokens
        )
        if pragma_token:
            transformed_data = self.__handle_pragma_processing(
                pragma_token, transformed_data
            )

        assert not self.context.block_stack
        assert not self.context.container_token_stack
        return transformed_data

    @classmethod
    def __correct_for_final_newline(
        cls, transformed_data: str, actual_tokens: List[MarkdownToken]
    ) -> str:
        was_forced_fenced_end = False
        if actual_tokens[-1].is_fenced_code_block_end:
            prev_end_token = cast(EndMarkdownToken, actual_tokens[-1])
            was_forced_fenced_end = prev_end_token.was_forced
        if (
            transformed_data
            and transformed_data[-1] == ParserHelper.newline_character
            and not (
                was_forced_fenced_end and not actual_tokens[-2].is_fenced_code_block
            )
        ):
            transformed_data = transformed_data[:-1]
        return transformed_data

    @classmethod
    def __handle_pragma_processing(
        cls, pragma_token: PragmaToken, transformed_data: str
    ) -> str:
        ordered_lines = collections.OrderedDict(
            sorted(pragma_token.pragma_lines.items())
        )

        for next_line_number in ordered_lines:
            POGGER.debug(
                f"pragma-->{ParserHelper.make_value_visible(ordered_lines[next_line_number])}<--"
            )
            detabified_pragma = TabHelper.detabify_string(
                ordered_lines[next_line_number]
            )
            POGGER.debug(
                f"pragma-->{ParserHelper.make_value_visible(detabified_pragma)}<--"
            )

            if next_line_number == 1:
                if transformed_data:
                    transformed_data = (
                        f"{detabified_pragma}"
                        + f"{ParserHelper.newline_character}{transformed_data}"
                    )
                else:
                    transformed_data = detabified_pragma
            else:
                nth_index = ParserHelper.find_nth_occurrence(
                    transformed_data,
                    ParserHelper.newline_character,
                    next_line_number - 1,
                )
                if nth_index == -1:
                    transformed_data = (
                        f"{transformed_data}{ParserHelper.newline_character}"
                        + f"{detabified_pragma}"
                    )
                else:
                    transformed_data = (
                        f"{transformed_data[:nth_index]}{ParserHelper.newline_character}"
                        + f"{detabified_pragma}{transformed_data[nth_index:]}"
                    )
        return transformed_data

    # pylint: disable=too-many-arguments
    def __process_next_token(
        self,
        current_token: MarkdownToken,
        previous_token: Optional[MarkdownToken],
        next_token: Optional[MarkdownToken],
        transformed_data: str,
        actual_tokens: List[MarkdownToken],
        token_index: int,
    ) -> Tuple[str, Optional[PragmaToken]]:
        pragma_token: Optional[PragmaToken] = None
        if current_token.token_name in self.start_container_token_handlers:
            start_container_handler_fn = self.start_container_token_handlers[
                current_token.token_name
            ]
            new_data = start_container_handler_fn(
                self.context,
                current_token,
                previous_token,
                next_token,
                transformed_data,
            )

        elif current_token.token_name in self.start_token_handlers:
            start_handler_fn = self.start_token_handlers[current_token.token_name]
            new_data = start_handler_fn(self.context, current_token, previous_token)

        elif current_token.is_pragma:
            new_data = ""
            pragma_token = cast(PragmaToken, current_token)
        elif current_token.is_end_token:
            current_end_token = cast(EndMarkdownToken, current_token)
            if current_end_token.type_name in self.end_token_handlers:
                end_handler_fn: EndMarkdownTokenTransformProtocol = (
                    self.end_token_handlers[current_end_token.type_name]
                )
                new_data = end_handler_fn(
                    self.context, current_end_token, previous_token, next_token
                )
            elif current_end_token.type_name in self.end_container_token_handlers:
                end_container_handler_fn: EndMarkdownContainerTokenTransformProtocol = (
                    self.end_container_token_handlers[current_end_token.type_name]
                )
                new_data = end_container_handler_fn(
                    self.context, current_end_token, actual_tokens, token_index
                )
            else:
                raise AssertionError(
                    f"end_current_token>>{current_end_token.type_name}"
                )
        else:
            raise AssertionError(f"current_token>>{current_token}")
        return new_data, pragma_token

    # pylint: enable=too-many-arguments
