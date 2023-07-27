"""
Module to provide for a transformation from tokens to a markdown document.
"""
import collections
import copy
import logging
from dataclasses import dataclass
from typing import Callable, Dict, List, Optional, Tuple, Union, cast

from pymarkdown.extensions.front_matter_extension import FrontMatterExtension
from pymarkdown.extensions.front_matter_markdown_token import FrontMatterMarkdownToken
from pymarkdown.extensions.pragma_token import PragmaToken
from pymarkdown.links.link_search_helper import LinkSearchHelper
from pymarkdown.markdown_token import (
    EndMarkdownToken,
    MarkdownToken,
    MarkdownTokenClass,
)
from pymarkdown.parser_helper import ParserHelper
from pymarkdown.parser_logger import ParserLogger
from pymarkdown.tab_helper import TabHelper
from pymarkdown.tokens.container_markdown_token import (
    BlockQuoteMarkdownToken,
    ContainerMarkdownToken,
    ListStartMarkdownToken,
    NewListItemMarkdownToken,
    OrderedListStartMarkdownToken,
    UnorderedListStartMarkdownToken,
)
from pymarkdown.tokens.inline_markdown_token import (
    EmailAutolinkMarkdownToken,
    EmphasisMarkdownToken,
    HardBreakMarkdownToken,
    ImageStartMarkdownToken,
    InlineCodeSpanMarkdownToken,
    InlineMarkdownToken,
    LinkStartMarkdownToken,
    RawHtmlMarkdownToken,
    TextMarkdownToken,
    UriAutolinkMarkdownToken,
)
from pymarkdown.tokens.leaf_markdown_token import (
    AtxHeadingMarkdownToken,
    BlankLineMarkdownToken,
    FencedCodeBlockMarkdownToken,
    HtmlBlockMarkdownToken,
    IndentedCodeBlockMarkdownToken,
    LeafMarkdownToken,
    LinkReferenceDefinitionMarkdownToken,
    ParagraphMarkdownToken,
    SetextHeadingMarkdownToken,
    ThematicBreakMarkdownToken,
)

POGGER = ParserLogger(logging.getLogger(__name__))


@dataclass
class MarkdownChangeRecord:
    """
    Class to keep track of changes.
    """

    item_a: bool
    item_b: int
    item_c: MarkdownToken


# pylint: disable=too-many-lines
class TransformToMarkdown:
    """
    Class to provide for a transformation from tokens to a markdown document.
    """

    def __init__(self) -> None:
        """
        Initializes a new instance of the TransformToMarkdown class.
        """
        self.block_stack: List[MarkdownToken] = []
        self.container_token_stack: List[MarkdownToken] = []
        self.start_container_token_handlers: Dict[
            str,
            Callable[
                [MarkdownToken, Optional[MarkdownToken], Optional[MarkdownToken], str],
                str,
            ],
        ] = {}
        self.end_container_token_handlers: Dict[
            str, Callable[[MarkdownToken, List[MarkdownToken], int], str]
        ] = {}
        self.start_token_handlers: Dict[
            str, Callable[[MarkdownToken, Optional[MarkdownToken]], str]
        ] = {}
        self.end_token_handlers: Dict[
            str,
            Callable[
                [MarkdownToken, Optional[MarkdownToken], Optional[MarkdownToken]], str
            ],
        ] = {}

        self.register_container_handlers(
            OrderedListStartMarkdownToken,
            self.__rehydrate_list_start,
            self.__rehydrate_list_start_end,
        )
        self.register_container_handlers(
            UnorderedListStartMarkdownToken,
            self.__rehydrate_list_start,
            self.__rehydrate_list_start_end,
        )
        self.register_container_handlers(
            NewListItemMarkdownToken, self.__rehydrate_next_list_item
        )
        self.register_container_handlers(
            BlockQuoteMarkdownToken,
            self.__rehydrate_block_quote,
            self.__rehydrate_block_quote_end,
        )

        self.register_handlers(
            ThematicBreakMarkdownToken, self.__rehydrate_thematic_break
        )
        self.register_handlers(
            ParagraphMarkdownToken,
            self.__rehydrate_paragraph,
            self.__rehydrate_paragraph_end,
        )
        self.register_handlers(
            IndentedCodeBlockMarkdownToken,
            self.__rehydrate_indented_code_block,
            self.__rehydrate_indented_code_block_end,
        )
        self.register_handlers(
            HtmlBlockMarkdownToken,
            self.__rehydrate_html_block,
            self.__rehydrate_html_block_end,
        )
        self.register_handlers(
            FencedCodeBlockMarkdownToken,
            self.__rehydrate_fenced_code_block,
            self.__rehydrate_fenced_code_block_end,
        )
        self.register_handlers(
            AtxHeadingMarkdownToken,
            self.__rehydrate_atx_heading,
            self.__rehydrate_atx_heading_end,
        )
        self.register_handlers(
            SetextHeadingMarkdownToken,
            self.__rehydrate_setext_heading,
            self.__rehydrate_setext_heading_end,
        )

        self.register_handlers(
            FrontMatterMarkdownToken, FrontMatterExtension.rehydrate_front_matter
        )

        self.register_handlers(BlankLineMarkdownToken, self.__rehydrate_blank_line)
        self.register_handlers(TextMarkdownToken, self.__rehydrate_text)
        self.register_handlers(
            LinkReferenceDefinitionMarkdownToken,
            self.__rehydrate_link_reference_definition,
        )
        self.register_handlers(
            InlineCodeSpanMarkdownToken, self.__rehydrate_inline_code_span
        )
        self.register_handlers(HardBreakMarkdownToken, self.__rehydrate_hard_break)
        self.register_handlers(
            UriAutolinkMarkdownToken, self.__rehydrate_inline_uri_autolink
        )
        self.register_handlers(
            LinkStartMarkdownToken,
            self.__rehydrate_inline_link,
            self.__rehydrate_inline_link_end,
        )
        self.register_handlers(ImageStartMarkdownToken, self.__rehydrate_inline_image)
        self.register_handlers(
            EmailAutolinkMarkdownToken, self.__rehydrate_inline_email_autolink
        )
        self.register_handlers(RawHtmlMarkdownToken, self.__rehydrate_inline_raw_html)
        self.register_handlers(
            EmphasisMarkdownToken,
            self.__rehydrate_inline_emphaisis,
            self.__rehydrate_inline_emphaisis_end,
        )

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
        ]:
            new_xx = current_token_type.__bases__
            assert len(new_xx) == 1
            current_token_type = new_xx[0]
        if current_token_type == ContainerMarkdownToken:
            token_class = MarkdownTokenClass.CONTAINER_BLOCK
        elif current_token_type == LeafMarkdownToken:
            token_class = MarkdownTokenClass.LEAF_BLOCK
        else:
            assert current_token_type == InlineMarkdownToken
            token_class = MarkdownTokenClass.INLINE_BLOCK

        # if not token_name:
        #     token_init_fn = token_type.__dict__["__init__"]
        #     init_parameters = {
        #         i: "" for i in inspect.getfullargspec(token_init_fn)[0] if i != "self"
        #     }
        #     handler_instance = token_type(**init_parameters)
        #     token_name = handler_instance.token_name
        #     if handler_instance.is_container:
        #         token_class = MarkdownTokenClass.CONTAINER_BLOCK
        #     elif handler_instance.is_leaf:
        #         token_class = MarkdownTokenClass.LEAF_BLOCK
        #         assert False, "-->" + str(token_type)
        #     else:
        #         assert handler_instance.is_inline
        #         token_class = MarkdownTokenClass.INLINE_BLOCK
        assert token_name is not None
        assert token_class is not None
        return token_name, token_class

    def register_handlers(
        self,
        token_type: type,
        start_token_handler: Callable[[MarkdownToken, Optional[MarkdownToken]], str],
        end_token_handler: Optional[
            Callable[
                [MarkdownToken, Optional[MarkdownToken], Optional[MarkdownToken]], str
            ]
        ] = None,
    ) -> None:
        """
        Register the handlers necessary to deal with token's start and end.
        """
        type_name, type_class = self.__get_token_type_info(token_type)

        assert type_class in [
            MarkdownTokenClass.LEAF_BLOCK,
            MarkdownTokenClass.INLINE_BLOCK,
        ]

        self.start_token_handlers[type_name] = start_token_handler
        if end_token_handler:
            self.end_token_handlers[type_name] = end_token_handler

    def register_container_handlers(
        self,
        token_type: type,
        start_token_handler: Callable[
            [MarkdownToken, Optional[MarkdownToken], Optional[MarkdownToken], str], str
        ],
        end_token_handler: Optional[
            Callable[[MarkdownToken, List[MarkdownToken], int], str]
        ] = None,
    ) -> None:
        """
        Register the handlers necessary to deal with token's start and end.
        """
        type_name, type_class = self.__get_token_type_info(token_type)
        assert type_class in [MarkdownTokenClass.CONTAINER_BLOCK]

        self.start_container_token_handlers[type_name] = start_token_handler
        if end_token_handler:
            self.end_container_token_handlers[type_name] = end_token_handler

    @classmethod
    def __transform_container_start(
        cls,
        container_stack: List[MarkdownToken],
        container_records: List[MarkdownChangeRecord],
        transformed_data_length_before_add: int,
        current_token: MarkdownToken,
    ) -> None:
        if not container_stack:
            container_records.clear()
        container_stack.append(current_token)
        record_item = MarkdownChangeRecord(
            True, transformed_data_length_before_add, current_token
        )
        container_records.append(record_item)
        # POGGER.debug("START:" + ParserHelper.make_value_visible(current_token))
        # POGGER.debug(">>" + ParserHelper.make_value_visible(container_stack))
        # POGGER.debug(">>" + ParserHelper.make_value_visible(container_records))

    # pylint: disable=too-many-arguments
    def __transform_container_end(
        self,
        container_stack: List[MarkdownToken],
        container_records: List[MarkdownChangeRecord],
        current_token: MarkdownToken,
        transformed_data: str,
        actual_tokens: List[MarkdownToken],
    ) -> str:
        current_end_token = cast(EndMarkdownToken, current_token)
        # POGGER.debug("END:" + ParserHelper.make_value_visible(current_token.start_markdown_token))
        while container_stack[-1].is_new_list_item:
            del container_stack[-1]
        assert str(container_stack[-1]) == str(
            current_end_token.start_markdown_token
        ), (
            ParserHelper.make_value_visible(container_stack[-1])
            + "=="
            + ParserHelper.make_value_visible(current_end_token.start_markdown_token)
        )
        del container_stack[-1]
        record_item = MarkdownChangeRecord(
            False,
            len(transformed_data),
            current_end_token.start_markdown_token,
        )
        container_records.append(record_item)
        # POGGER.debug(">>" + ParserHelper.make_value_visible(container_stack))
        # POGGER.debug(">>" + ParserHelper.make_value_visible(container_records))

        if not container_stack:
            record_item = container_records[0]
            assert record_item.item_a
            pre_container_text = transformed_data[: record_item.item_b]
            container_text = transformed_data[record_item.item_b :]
            adjusted_text = self.__apply_container_transformation(
                container_text, container_records, actual_tokens
            )
            POGGER.debug(f"pre>:{pre_container_text}:<")
            POGGER.debug(f"adj>:{adjusted_text}:<")
            transformed_data = pre_container_text + adjusted_text
            POGGER.debug(f"trn>:{transformed_data}:<")
        return transformed_data

    # pylint: enable=too-many-arguments

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

            if (
                current_token.is_block_quote_start
                or current_token.is_list_start
                or current_token.is_new_list_item
            ):
                self.__transform_container_start(
                    container_stack,
                    container_records,
                    transformed_data_length_before_add,
                    current_token,
                )
            elif current_token.is_block_quote_end or current_token.is_list_end:
                transformed_data = self.__transform_container_end(
                    container_stack,
                    container_records,
                    current_token,
                    transformed_data,
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

        assert not self.block_stack
        assert not self.container_token_stack
        return transformed_data

    # pylint: disable=too-many-arguments
    @classmethod
    def __manage_records(
        cls,
        container_records: List[MarkdownChangeRecord],
        old_record_index: int,
        token_stack: List[MarkdownToken],
        container_token_indices: List[int],
        removed_tokens: List[MarkdownToken],
    ) -> Tuple[int, bool, MarkdownChangeRecord]:
        did_move_ahead, current_changed_record = (
            True,
            container_records[old_record_index + 1],
        )
        POGGER.debug(
            "   current_changed_record("
            + str(old_record_index + 1)
            + ")-->"
            + ParserHelper.make_value_visible(current_changed_record)
        )
        if current_changed_record.item_a:
            token_stack.append(current_changed_record.item_c)
            container_token_indices.append(0)
        else:
            POGGER.debug(f"   -->{ParserHelper.make_value_visible(token_stack)}")
            POGGER.debug(
                f"   -->{ParserHelper.make_value_visible(container_token_indices)}"
            )

            if token_stack[-1].is_new_list_item:
                removed_tokens.append(token_stack[-1])
                del token_stack[-1]
                del container_token_indices[-1]

            assert str(current_changed_record.item_c) == str(token_stack[-1]), (
                "end:"
                + ParserHelper.make_value_visible(current_changed_record.item_c)
                + "!="
                + ParserHelper.make_value_visible(token_stack[-1])
            )
            removed_tokens.append(token_stack[-1])
            del token_stack[-1]
            del container_token_indices[-1]

        POGGER.debug(
            "   -->current_changed_recordx>"
            + ParserHelper.make_value_visible(current_changed_record)
        )
        POGGER.debug(f"   -->{ParserHelper.make_value_visible(token_stack)}")
        POGGER.debug(
            f"   -->{ParserHelper.make_value_visible(container_token_indices)}"
        )
        old_record_index += 1
        return old_record_index, did_move_ahead, current_changed_record

    # pylint: enable=too-many-arguments

    # pylint: disable=too-many-arguments
    @classmethod
    def __move_to_current_record(
        cls,
        old_record_index: int,
        container_records: List[MarkdownChangeRecord],
        container_text_index: int,
        token_stack: List[MarkdownToken],
        container_token_indices: List[int],
        container_line_length: int,
    ) -> Tuple[int, bool, Optional[MarkdownChangeRecord], List[MarkdownToken]]:
        record_index, current_changed_record, did_move_ahead = (
            old_record_index,
            None,
            False,
        )

        POGGER.debug(f"({container_text_index})")
        POGGER.debug(
            "("
            + str(record_index + 1)
            + "):"
            + ParserHelper.make_value_visible(container_records[1])
        )
        while record_index + 1 < len(container_records) and container_records[
            record_index + 1
        ].item_b <= (container_text_index + container_line_length):
            record_index += 1
        POGGER.debug(
            "("
            + str(record_index + 1)
            + "):"
            + ParserHelper.make_value_visible(container_records[1])
        )
        removed_tokens: List[MarkdownToken] = []
        while old_record_index != record_index:
            (
                old_record_index,
                did_move_ahead,
                current_changed_record,
            ) = cls.__manage_records(
                container_records,
                old_record_index,
                token_stack,
                container_token_indices,
                removed_tokens,
            )

        POGGER.debug(
            f"   removed_tokens={ParserHelper.make_value_visible(removed_tokens)}"
        )
        return record_index, did_move_ahead, current_changed_record, removed_tokens

    # pylint: enable=too-many-arguments

    # pylint: disable=too-many-arguments
    @classmethod
    def __adjust_state_for_element(
        cls,
        token_stack: List[MarkdownToken],
        container_token_indices: List[int],
        did_move_ahead: bool,
        current_changed_record: Optional[MarkdownChangeRecord],
        last_container_token_index: int,
    ) -> None:
        POGGER.debug(f" -->{ParserHelper.make_value_visible(token_stack)}")
        POGGER.debug(f" -->{ParserHelper.make_value_visible(container_token_indices)}")
        did_change_to_list_token = (
            did_move_ahead
            and (current_changed_record is not None and current_changed_record.item_a)
            and (token_stack[-1].is_list_start or token_stack[-1].is_new_list_item)
        )

        # May need earlier if both new item and start of new list on same line
        if not did_change_to_list_token:
            container_token_indices[-1] = last_container_token_index + 1
        elif token_stack[-1].is_new_list_item:
            del token_stack[-1]
            del container_token_indices[-1]
        POGGER.debug(f" -->{ParserHelper.make_value_visible(token_stack)}")
        POGGER.debug(f" -->{ParserHelper.make_value_visible(container_token_indices)}")

    # pylint: enable=too-many-arguments

    @classmethod
    def __apply_primary_transformation_start(
        cls,
        current_changed_record: Optional[MarkdownChangeRecord],
        actual_tokens: List[MarkdownToken],
    ) -> bool:
        is_list_start_after_two_block_starts = False
        if current_changed_record and current_changed_record.item_c.is_list_start:
            list_start_token = current_changed_record.item_c
            list_start_token_index = actual_tokens.index(list_start_token)
            POGGER.debug(
                f" -->list_start_token_index>{ParserHelper.make_value_visible(list_start_token_index)}"
            )

            # pylint: disable=too-many-boolean-expressions
            if (
                list_start_token_index >= 2
                and actual_tokens[list_start_token_index - 1].is_block_quote_start
                and actual_tokens[list_start_token_index - 2].is_block_quote_start
                and actual_tokens[list_start_token_index - 1].line_number
                == list_start_token.line_number
                and actual_tokens[list_start_token_index - 2].line_number
                == list_start_token.line_number
                and actual_tokens[list_start_token_index + 1].is_list_end
                and actual_tokens[list_start_token_index + 2].is_blank_line
            ):
                is_list_start_after_two_block_starts = True
                # pylint: enable=too-many-boolean-expressions
        return is_list_start_after_two_block_starts

    # pylint: disable=too-many-arguments
    @classmethod
    def __apply_primary_transformation(
        cls,
        did_move_ahead: bool,
        token_stack: List[MarkdownToken],
        container_token_indices: List[int],
        current_changed_record: Optional[MarkdownChangeRecord],
        container_line: str,
        actual_tokens: List[MarkdownToken],
    ) -> Tuple[int, bool, str]:
        POGGER.debug(
            f" -->did_move_ahead>{ParserHelper.make_value_visible(did_move_ahead)}"
        )
        POGGER.debug(f" -->{ParserHelper.make_value_visible(token_stack)}")
        POGGER.debug(f" -->{ParserHelper.make_value_visible(container_token_indices)}")
        POGGER.debug(
            f" -->current_changed_record>{ParserHelper.make_value_visible(current_changed_record)}"
        )

        is_list_start_after_two_block_starts = cls.__apply_primary_transformation_start(
            current_changed_record, actual_tokens
        )

        applied_leading_spaces_to_start_of_container_line = (
            not did_move_ahead
            or current_changed_record is None
            or not current_changed_record.item_a
        ) and not is_list_start_after_two_block_starts

        last_container_token_index = container_token_indices[-1]
        if applied_leading_spaces_to_start_of_container_line:
            container_line = cls.__apply_primary_transformation_adjust_container_line(
                token_stack, last_container_token_index, container_line
            )
        return (
            last_container_token_index,
            applied_leading_spaces_to_start_of_container_line,
            container_line,
        )

    # pylint: enable=too-many-arguments

    @classmethod
    def __apply_primary_transformation_adjust_container_line(
        cls,
        token_stack: List[MarkdownToken],
        last_container_token_index: int,
        container_line: str,
    ) -> str:
        POGGER.debug(f" container->{ParserHelper.make_value_visible(token_stack[-1])}")
        if token_stack[-1].is_block_quote_start:
            prev_block_token = cast(BlockQuoteMarkdownToken, token_stack[-1])
            assert prev_block_token.bleading_spaces is not None
            split_leading_spaces = prev_block_token.bleading_spaces.split(
                ParserHelper.newline_character
            )
        else:
            prev_list_token = cast(ListStartMarkdownToken, token_stack[-1])
            assert prev_list_token.leading_spaces is not None
            split_leading_spaces = prev_list_token.leading_spaces.split(
                ParserHelper.newline_character
            )
        if last_container_token_index < len(split_leading_spaces):
            POGGER.debug(f" -->{ParserHelper.make_value_visible(split_leading_spaces)}")
            POGGER.debug(
                " primary-->container_line>:"
                + ParserHelper.make_value_visible(container_line)
                + ":<"
            )
            container_line = (
                split_leading_spaces[last_container_token_index] + container_line
            )
            POGGER.debug(
                " -->container_line>:"
                + ParserHelper.make_value_visible(container_line)
                + ":<"
            )
        return container_line

    @classmethod
    def __find_last_block_quote_on_stack(cls, token_stack: List[MarkdownToken]) -> int:
        POGGER.debug(" looking for nested block start")
        stack_index = len(token_stack) - 2
        nested_block_start_index = -1
        while stack_index >= 0:
            if token_stack[stack_index].is_block_quote_start:
                nested_block_start_index = stack_index
                break
            stack_index -= 1
        return nested_block_start_index

    @classmethod
    def __adjust_for_list_check(
        cls,
        token_stack: List[MarkdownToken],
        removed_tokens: List[MarkdownToken],
        applied_leading_spaces_to_start_of_container_line: bool,
        previous_token: MarkdownToken,
    ) -> bool:
        if not token_stack[-1].is_new_list_item:
            return (
                applied_leading_spaces_to_start_of_container_line
                or token_stack[-1].line_number != previous_token.line_number
            )
        new_list_item_adjust = True
        if len(removed_tokens) == 1 and removed_tokens[-1].is_block_quote_start:
            removed_block_token = cast(BlockQuoteMarkdownToken, removed_tokens[-1])
            assert removed_block_token.bleading_spaces is not None
            leading_spaces_newline_count = removed_block_token.bleading_spaces.count(
                "\n"
            )
            block_quote_end_line = (
                leading_spaces_newline_count + removed_block_token.line_number
            )
            POGGER.debug(
                f"block_quote_end_line={block_quote_end_line} = "
                + f"fg={leading_spaces_newline_count} + "
                + f"line={removed_block_token.line_number}"
            )
            new_list_item_adjust = leading_spaces_newline_count > 1
            POGGER.debug(f"new_list_item_adjust:{new_list_item_adjust}")

        return (
            token_stack[-1].line_number != previous_token.line_number
            and new_list_item_adjust
        )

    # pylint: disable=too-many-arguments
    @classmethod
    def __adjust_for_list_end(
        cls,
        container_line: str,
        token_stack: List[MarkdownToken],
        removed_tokens: List[MarkdownToken],
        applied_leading_spaces_to_start_of_container_line: bool,
        previous_token: MarkdownToken,
        container_token_indices: List[int],
        inner_token_index: int,
        nested_block_start_index: int,
    ) -> str:
        if cls.__adjust_for_list_check(
            token_stack,
            removed_tokens,
            applied_leading_spaces_to_start_of_container_line,
            previous_token,
        ):
            previous_block_token = cast(BlockQuoteMarkdownToken, previous_token)
            assert previous_block_token.bleading_spaces is not None
            split_leading_spaces = previous_block_token.bleading_spaces.split(
                ParserHelper.newline_character
            )
            POGGER.debug(
                f"inner_token_index={inner_token_index} < len(split)={len(split_leading_spaces)}"
            )
            if inner_token_index < len(split_leading_spaces):
                POGGER.debug(
                    " adj-->container_line>:"
                    + ParserHelper.make_value_visible(container_line)
                    + ":<"
                )
                container_line = (
                    split_leading_spaces[inner_token_index] + container_line
                )
                POGGER.debug(
                    " adj-->container_line>:"
                    + ParserHelper.make_value_visible(container_line)
                    + ":<"
                )
        container_token_indices[nested_block_start_index] = inner_token_index + 1
        return container_line

    # pylint: enable=too-many-arguments

    # pylint: disable=too-many-arguments
    @classmethod
    def __adjust_for_list(
        cls,
        token_stack: List[MarkdownToken],
        applied_leading_spaces_to_start_of_container_line: bool,
        container_token_indices: List[int],
        container_line: str,
        removed_tokens: List[MarkdownToken],
    ) -> str:
        if (
            len(token_stack) > 1
            and token_stack[-1].is_list_start
            or token_stack[-1].is_new_list_item
        ):
            nested_block_start_index = (
                TransformToMarkdown.__find_last_block_quote_on_stack(token_stack)
            )
            if nested_block_start_index != -1:
                POGGER.debug(f"nested_block_start_index>{nested_block_start_index}")
                previous_token = token_stack[nested_block_start_index]
                POGGER.debug(
                    f"previous={ParserHelper.make_value_visible(previous_token)}"
                )
                POGGER.debug(
                    " applied_leading_spaces_to_start_of_container_line->"
                    + str(applied_leading_spaces_to_start_of_container_line)
                )
                inner_token_index = container_token_indices[nested_block_start_index]
                POGGER.debug(
                    f"applied:{applied_leading_spaces_to_start_of_container_line} or "
                    + f"end.line:{token_stack[-1].line_number} != prev.line:{previous_token.line_number}"
                )

                container_line = cls.__adjust_for_list_end(
                    container_line,
                    token_stack,
                    removed_tokens,
                    applied_leading_spaces_to_start_of_container_line,
                    previous_token,
                    container_token_indices,
                    inner_token_index,
                    nested_block_start_index,
                )
        return container_line

    # pylint: enable=too-many-arguments

    @classmethod
    def __get_last_list_index(cls, token_stack: List[MarkdownToken]) -> int:
        stack_index = len(token_stack) - 2
        nested_list_start_index = -1
        while stack_index >= 0:
            if (
                token_stack[stack_index].is_list_start
                or token_stack[stack_index].is_new_list_item
            ):
                nested_list_start_index = stack_index
                break
            stack_index -= 1
        return nested_list_start_index

    @classmethod
    def __adjust_for_block_quote_same_line(
        cls,
        container_line: str,
        nested_list_start_index: int,
        token_stack: List[MarkdownToken],
        container_token_indices: List[int],
    ) -> str:
        adj_line = ""
        POGGER.debug(f"adj_line->:{adj_line}:")
        adj_line = cls.__adjust(
            nested_list_start_index - 1,
            token_stack,
            container_token_indices,
            adj_line,
            True,
        )
        POGGER.debug(f"adj_line->:{adj_line}:")
        adj_line = cls.__adjust(
            nested_list_start_index,
            token_stack,
            container_token_indices,
            adj_line,
            True,
        )
        POGGER.debug(f"adj_line->:{adj_line}:")
        return adj_line + container_line

    # pylint: disable=too-many-arguments
    @classmethod
    def __adjust_for_block_quote_previous_line(
        cls,
        container_line: str,
        nested_list_start_index: int,
        token_stack: List[MarkdownToken],
        container_token_indices: List[int],
        line_number: int,
    ) -> str:
        previous_token = token_stack[nested_list_start_index]
        # POGGER.debug(f"nested_list_start_index->{nested_list_start_index}")
        # POGGER.debug(f" yes->{ParserHelper.make_value_visible(previous_token)}")

        # POGGER.debug(f"token_stack[-1].line_number->{token_stack[-1].line_number}")
        # POGGER.debug(f"previous_token.line_number->{previous_token.line_number}")
        # POGGER.debug(f"line_number->{line_number}")
        if (
            token_stack[-1].line_number != previous_token.line_number
            or line_number != previous_token.line_number
        ):
            POGGER.debug("different line as list start")
            container_line = cls.__adjust(
                nested_list_start_index,
                token_stack,
                container_token_indices,
                container_line,
                False,
            )
        else:
            POGGER.debug("same line as list start")
            if nested_list_start_index > 0:
                next_level_index = nested_list_start_index - 1
                pre_previous_token = token_stack[next_level_index]
                # POGGER.debug(
                #     f" pre_previous_token->{ParserHelper.make_value_visible(pre_previous_token)}"
                # )
                if pre_previous_token.is_block_quote_start:
                    # sourcery skip: move-assign
                    different_line_prefix = cls.__adjust(
                        next_level_index,
                        token_stack,
                        container_token_indices,
                        "",
                        False,
                    )
                    # POGGER.debug(f"different_line_prefix>:{different_line_prefix}:<")
                    if pre_previous_token.line_number != previous_token.line_number:
                        container_line = different_line_prefix + container_line
        return container_line

    # pylint: enable=too-many-arguments

    @classmethod
    def __adjust_for_block_quote(
        cls,
        token_stack: List[MarkdownToken],
        container_line: str,
        container_token_indices: List[int],
        line_number: int,
    ) -> str:
        if not (len(token_stack) > 1 and token_stack[-1].is_block_quote_start):
            return container_line

        POGGER.debug(" looking for nested list start")
        nested_list_start_index = TransformToMarkdown.__get_last_list_index(token_stack)
        POGGER.debug(f" afbq={len(token_stack) - 1}")
        POGGER.debug(f" nested_list_start_index={nested_list_start_index}")
        if nested_list_start_index == -1:
            POGGER.debug(" nope")
        elif (
            nested_list_start_index == len(token_stack) - 2
            and nested_list_start_index > 0
            and token_stack[-1].line_number == line_number
            and token_stack[nested_list_start_index - 1].is_block_quote_start
            and token_stack[-1].line_number != token_stack[-2].line_number
        ):
            container_line = cls.__adjust_for_block_quote_same_line(
                container_line,
                nested_list_start_index,
                token_stack,
                container_token_indices,
            )
        else:
            container_line = cls.__adjust_for_block_quote_previous_line(
                container_line,
                nested_list_start_index,
                token_stack,
                container_token_indices,
                line_number,
            )
        return container_line

    # pylint: disable=too-many-arguments
    @classmethod
    def __adjust(
        cls,
        nested_list_start_index: int,
        token_stack: List[MarkdownToken],
        container_token_indices: List[int],
        container_line: str,
        apply_list_fix: bool,
    ) -> str:
        previous_token = token_stack[nested_list_start_index]
        if apply_list_fix and previous_token.is_list_start:
            previous_list_token = cast(ListStartMarkdownToken, previous_token)
            delta = previous_list_token.indent_level - len(container_line)
            POGGER.debug(f"delta->{delta}")
            container_line += ParserHelper.repeat_string(" ", delta)
        if previous_token.is_block_quote_start:
            previous_block_token = cast(BlockQuoteMarkdownToken, previous_token)
            leading_spaces = (
                ""
                if previous_block_token.bleading_spaces is None
                else previous_block_token.bleading_spaces
            )
        else:
            previous_list_token = cast(ListStartMarkdownToken, previous_token)
            leading_spaces = (
                ""
                if previous_list_token.leading_spaces is None
                else previous_list_token.leading_spaces
            )
        split_leading_spaces = leading_spaces.split(ParserHelper.newline_character)
        inner_token_index = container_token_indices[nested_list_start_index]
        assert inner_token_index < len(split_leading_spaces)
        POGGER.debug(
            f"inner_index->{str(container_token_indices[nested_list_start_index])}"
        )
        container_line = split_leading_spaces[inner_token_index] + container_line
        container_token_indices[nested_list_start_index] = inner_token_index + 1
        POGGER.debug(
            f"inner_index->{str(container_token_indices[nested_list_start_index])}"
        )
        return container_line

    # pylint: enable=too-many-arguments

    # pylint: disable=too-many-locals
    def __apply_container_transformation(
        self,
        container_text: str,
        container_records: List[MarkdownChangeRecord],
        actual_tokens: List[MarkdownToken],
    ) -> str:
        POGGER.debug(
            f">>incoming>>:{ParserHelper.make_value_visible(container_text)}:<<"
        )

        POGGER.debug(
            f">>container_records>>{ParserHelper.make_value_visible(container_records)}"
        )

        token_stack: List[MarkdownToken] = []
        container_token_indices: List[int] = []
        (
            base_line_number,
            delta_line,
            split_container_text,
            transformed_parts,
            record_index,
            container_text_index,
            current_changed_record,
        ) = (
            container_records[0].item_c.line_number,
            0,
            container_text.split(ParserHelper.newline_character),
            [],
            -1,
            container_records[0].item_b,
            None,
        )
        POGGER.debug(
            ">>split_container_text>>"
            + ParserHelper.make_value_visible(split_container_text)
        )

        for container_line in split_container_text:  # pragma: no cover
            container_line_length = len(container_line)
            # POGGER.debug(
            #     ParserHelper.newline_character
            #     + str(delta_line)
            #     + "("
            #     + str(base_line_number + delta_line)
            #     + ")>>container_line>>"
            #     + str(container_text_index)
            #     + "-"
            #     + str(container_text_index + container_line_length)
            #     + ":>:"
            #     + ParserHelper.make_value_visible(container_line)
            #     + ":<"
            # )

            old_record_index = record_index
            (
                record_index,
                did_move_ahead,
                current_changed_record,
                removed_tokens,
            ) = self.__move_to_current_record(
                old_record_index,
                container_records,
                container_text_index,
                token_stack,
                container_token_indices,
                container_line_length,
            )

            if not container_token_indices:
                transformed_parts.append(container_line)
                break

            (
                last_container_token_index,
                applied_leading_spaces_to_start_of_container_line,
                container_line,
            ) = self.__apply_primary_transformation(
                did_move_ahead,
                token_stack,
                container_token_indices,
                current_changed_record,
                container_line,
                actual_tokens,
            )

            container_line = self.__adjust_for_list(
                token_stack,
                applied_leading_spaces_to_start_of_container_line,
                container_token_indices,
                container_line,
                removed_tokens,
            )
            container_line = self.__adjust_for_block_quote(
                token_stack,
                container_line,
                container_token_indices,
                base_line_number + delta_line,
            )

            self.__adjust_state_for_element(
                token_stack,
                container_token_indices,
                did_move_ahead,
                current_changed_record,
                last_container_token_index,
            )

            transformed_parts.append(container_line)
            container_text_index += container_line_length + 1
            delta_line += 1

        POGGER.debug(
            "\n<<transformed<<" + ParserHelper.make_value_visible(transformed_parts)
        )
        return ParserHelper.newline_character.join(transformed_parts)

    # pylint: enable=too-many-locals

    def __look_for_last_block_token(self) -> Optional[BlockQuoteMarkdownToken]:
        found_block_token: Optional[BlockQuoteMarkdownToken] = None
        found_token = next(
            (
                self.container_token_stack[i]
                for i in range(len(self.container_token_stack) - 1, -1, -1)
                if self.container_token_stack[i].is_block_quote_start
            ),
            None,
        )
        POGGER.debug(
            f">>found_block_token>>{ParserHelper.make_value_visible(found_token)}<"
        )
        if found_token:
            found_block_token = cast(BlockQuoteMarkdownToken, found_token)
            POGGER.debug(
                f">>found_block_token-->index>>{found_block_token.leading_text_index}<"
            )
        return found_block_token

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
                current_token, previous_token, next_token, transformed_data
            )

        elif current_token.token_name in self.start_token_handlers:
            start_handler_fn = self.start_token_handlers[current_token.token_name]
            new_data = start_handler_fn(current_token, previous_token)

        elif current_token.is_pragma:
            new_data = ""
            pragma_token = cast(PragmaToken, current_token)
        elif current_token.is_end_token:
            current_end_token = cast(EndMarkdownToken, current_token)
            if current_end_token.type_name in self.end_token_handlers:
                end_handler_fn: Callable[
                    [MarkdownToken, Optional[MarkdownToken], Optional[MarkdownToken]],
                    str,
                ] = self.end_token_handlers[current_end_token.type_name]
                new_data = end_handler_fn(current_end_token, previous_token, next_token)
            elif current_end_token.type_name in self.end_container_token_handlers:
                end_container_handler_fn: Callable[
                    [MarkdownToken, List[MarkdownToken], int], str
                ] = self.end_container_token_handlers[current_end_token.type_name]
                new_data = end_container_handler_fn(
                    current_end_token, actual_tokens, token_index
                )
            else:
                raise AssertionError(
                    f"end_current_token>>{current_end_token.type_name}"
                )
        else:
            raise AssertionError(f"current_token>>{current_token}")
        return new_data, pragma_token

    # pylint: enable=too-many-arguments

    def __rehydrate_paragraph(
        self, current_token: MarkdownToken, previous_token: Optional[MarkdownToken]
    ) -> str:
        """
        Rehydrate the paragraph block from the token.
        """
        _ = previous_token

        self.block_stack.append(current_token)

        current_paragraph_token = cast(ParagraphMarkdownToken, current_token)
        current_paragraph_token.rehydrate_index = 0
        extracted_whitespace = current_paragraph_token.extracted_whitespace
        if ParserHelper.newline_character in extracted_whitespace:
            line_end_index = extracted_whitespace.index(ParserHelper.newline_character)
            extracted_whitespace = extracted_whitespace[:line_end_index]
        return ParserHelper.resolve_all_from_text(extracted_whitespace)

    def __rehydrate_paragraph_end(
        self,
        current_token: MarkdownToken,
        previous_token: Optional[MarkdownToken],
        next_token: Optional[MarkdownToken],
    ) -> str:
        """
        Rehydrate the end of the paragraph block from the token.
        """
        _ = (previous_token, next_token)

        top_stack_token = cast(ParagraphMarkdownToken, self.block_stack[-1])
        del self.block_stack[-1]

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

    def __rehydrate_blank_line(
        self, current_token: MarkdownToken, previous_token: Optional[MarkdownToken]
    ) -> str:
        """
        Rehydrate the blank line from the token.
        """
        # if (
        #     self.block_stack
        #     and self.block_stack[-1].is_fenced_code_block
        #     and (previous_token and previous_token.is_text)
        # ):
        #     extra_newline_after_text_token = ParserHelper.newline_character
        # else:
        _ = previous_token
        extra_newline_after_text_token = ""

        current_blank_token = cast(BlankLineMarkdownToken, current_token)
        return f"{extra_newline_after_text_token}{current_blank_token.extracted_whitespace}{ParserHelper.newline_character}"

    def __rehydrate_indented_code_block(
        self, current_token: MarkdownToken, previous_token: Optional[MarkdownToken]
    ) -> str:
        """
        Rehydrate the indented code block from the token.
        """
        _ = previous_token

        self.block_stack.append(current_token)
        return ""

    def __rehydrate_indented_code_block_end(
        self,
        current_token: MarkdownToken,
        previous_token: Optional[MarkdownToken],
        next_token: Optional[MarkdownToken],
    ) -> str:
        """
        Rehydrate the end of the indented code block from the token.
        """
        _ = (current_token, previous_token, next_token)

        del self.block_stack[-1]
        return ""

    def __rehydrate_html_block(
        self, current_token: MarkdownToken, previous_token: Optional[MarkdownToken]
    ) -> str:
        """
        Rehydrate the html block from the token.
        """
        _ = (current_token, previous_token)

        self.block_stack.append(current_token)
        return ""

    def __rehydrate_html_block_end(
        self,
        current_token: MarkdownToken,
        previous_token: Optional[MarkdownToken],
        next_token: Optional[MarkdownToken],
    ) -> str:
        """
        Rehydrate the end of the html block from the token.
        """
        return self.__rehydrate_indented_code_block_end(
            current_token, previous_token, next_token
        )

    def __rehydrate_fenced_code_block(
        self, current_token: MarkdownToken, previous_token: Optional[MarkdownToken]
    ) -> str:
        """
        Rehydrate the fenced code block from the token.
        """
        _ = previous_token

        self.block_stack.append(current_token)
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

    def __rehydrate_fenced_code_block_end(
        self,
        current_token: MarkdownToken,
        previous_token: Optional[MarkdownToken],
        next_token: Optional[MarkdownToken],
    ) -> str:  # sourcery skip: extract-method
        """
        Rehydrate the end of the fenced code block from the token.
        """
        del self.block_stack[-1]

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

    def __search_backward_for_block_quote_start(self) -> int:
        token_stack_index = len(self.container_token_stack) - 2
        while (
            token_stack_index >= 0
            and self.container_token_stack[token_stack_index].is_block_quote_start
        ):
            token_stack_index -= 1
        POGGER.debug(f">token_stack_index>{token_stack_index}")
        POGGER.debug(
            f">token_stack_token-->{ParserHelper.make_value_visible(self.container_token_stack[token_stack_index])}"
        )
        return token_stack_index

    def __rehydrate_block_quote_start(
        self, current_token: BlockQuoteMarkdownToken
    ) -> Tuple[int, bool, BlockQuoteMarkdownToken]:
        POGGER.debug(
            f">bquote>tabbed_bleading_spaces>{ParserHelper.make_value_visible(current_token.tabbed_bleading_spaces)}"
        )
        new_instance = copy.deepcopy(current_token)
        POGGER.debug(
            f">bquote>tabbed_bleading_spaces>{ParserHelper.make_value_visible(new_instance.tabbed_bleading_spaces)}"
        )
        new_instance.leading_text_index = 0
        self.container_token_stack.append(new_instance)
        POGGER.debug(f">bquote>{ParserHelper.make_value_visible(new_instance)}")
        POGGER.debug(
            f">self.container_token_stack>{ParserHelper.make_value_visible(self.container_token_stack)}"
        )
        token_stack_index = self.__search_backward_for_block_quote_start()
        are_tokens_viable = (
            len(self.container_token_stack) > 1 and token_stack_index >= 0
        )
        POGGER.debug(f">are_tokens_viable>{are_tokens_viable}")
        return token_stack_index, are_tokens_viable, new_instance

    def __rehydrate_block_quote(
        self,
        current_token: MarkdownToken,
        previous_token: Optional[MarkdownToken],
        next_token: Optional[MarkdownToken],
        transformed_data: str,
    ) -> str:
        _ = (previous_token, transformed_data)

        current_block_token = cast(BlockQuoteMarkdownToken, current_token)
        (
            token_stack_index,
            are_tokens_viable,
            new_instance,
        ) = self.__rehydrate_block_quote_start(current_block_token)

        if are_tokens_viable:
            container_list_token = cast(
                ListStartMarkdownToken, self.container_token_stack[token_stack_index]
            )
            matching_list_token = (
                container_list_token.last_new_list_token or container_list_token
            )
            POGGER.debug(
                f">matching_list_token>{ParserHelper.make_value_visible(matching_list_token)}"
            )

            POGGER.debug(f">current_token.line_number>{current_token.line_number}")
            POGGER.debug(
                ">container_token_stack[token_stack_index].line_number>"
                + f"{container_list_token.line_number}"
            )

        if (
            are_tokens_viable
            and current_token.line_number == matching_list_token.line_number
        ):
            container_list_token = cast(
                ListStartMarkdownToken, self.container_token_stack[token_stack_index]
            )
            already_existing_whitespace = ParserHelper.repeat_string(
                " ", container_list_token.indent_level
            )
        else:
            already_existing_whitespace = None

        POGGER.debug(
            f">bquote>current_token>{ParserHelper.make_value_visible(current_token)}"
        )
        POGGER.debug(
            f">bquote>next_token>{ParserHelper.make_value_visible(next_token)}"
        )

        if (
            next_token
            and next_token.is_block_quote_start
            and current_token.line_number == next_token.line_number
        ):
            POGGER.debug(">bquote> will be done by following bquote>")
            selected_leading_sequence = ""
        else:
            POGGER.debug(f">bquote>bleading_spaces>{new_instance.bleading_spaces}<")
            POGGER.debug(
                f">bquote>tabbed_bleading_spaces>{ParserHelper.make_value_visible(new_instance.tabbed_bleading_spaces)}"
            )
            selected_leading_sequence = (
                new_instance.calculate_next_bleading_space_part()
            )
            POGGER.debug(
                f">bquote>selected_leading_sequence>{selected_leading_sequence}<"
            )

        POGGER.debug(
            f">bquote>already_existing_whitespace>:{already_existing_whitespace}:<"
        )
        POGGER.debug(
            f">bquote>selected_leading_sequence>:{selected_leading_sequence}:<"
        )
        if already_existing_whitespace and selected_leading_sequence.startswith(
            already_existing_whitespace
        ):
            selected_leading_sequence = selected_leading_sequence[
                len(already_existing_whitespace) :
            ]
            POGGER.debug(
                f">bquote>new selected_leading_sequence>{selected_leading_sequence}<"
            )
        return selected_leading_sequence

    def __look_backward_for_list_or_block_quote_start(self) -> int:
        token_stack_index = len(self.container_token_stack) - 1
        POGGER.debug(f"rls>>token_stack_index>>{token_stack_index}<<")
        if token_stack_index >= 0:
            assert (
                self.container_token_stack[token_stack_index].is_list_start
                or self.container_token_stack[token_stack_index].is_block_quote_start
            )
        # while (
        #     token_stack_index >= 0
        #     and not self.container_token_stack[token_stack_index].is_list_start
        #     and not self.container_token_stack[token_stack_index].is_block_quote_start
        # ):
        #     token_stack_index -= 1
        return token_stack_index

    def __rehydrate_list_start_previous_token_start(
        self,
        current_token: Union[ListStartMarkdownToken, NewListItemMarkdownToken],
        previous_token: MarkdownToken,
        extracted_whitespace: str,
    ) -> Tuple[
        int,
        Optional[str],
        bool,
        Optional[BlockQuoteMarkdownToken],
        Optional[ListStartMarkdownToken],
        Optional[BlockQuoteMarkdownToken],
    ]:
        previous_indent, was_within_block_token = 0, False
        post_adjust_whitespace: Optional[str] = None
        POGGER.debug(
            f"rlspt>>current_token>>{ParserHelper.make_value_visible(current_token)}<<"
        )
        POGGER.debug(
            f"rlspt>>previous_token>>{ParserHelper.make_value_visible(previous_token)}<<"
        )
        POGGER.debug(
            f"rlspt>>extracted_whitespace>>{ParserHelper.make_value_visible(extracted_whitespace)}<<"
        )
        POGGER.debug(
            f"rls>>self.container_token_stack>>{ParserHelper.make_value_visible(self.container_token_stack)}<<"
        )
        containing_block_quote_token = self.__look_for_last_block_token()
        POGGER.debug(
            f"rls>>containing_block_quote_token>>{ParserHelper.make_value_visible(containing_block_quote_token)}<<"
        )
        if containing_block_quote_token:
            POGGER.debug(
                f"rls>>containing_block_quote_token>>{ParserHelper.make_value_visible(containing_block_quote_token.leading_text_index)}<<"
            )

        token_stack_index = self.__look_backward_for_list_or_block_quote_start()
        POGGER.debug(f"rls>>token_stack_index2>>{token_stack_index}<<")

        containing_list_token, deeper_containing_block_quote_token = None, None
        if (
            token_stack_index >= 0
            and containing_block_quote_token
            != self.container_token_stack[token_stack_index]
        ):
            containing_list_token = cast(
                ListStartMarkdownToken, self.container_token_stack[token_stack_index]
            )
            deeper_containing_block_quote_token = containing_block_quote_token
            containing_block_quote_token = None

        return (
            previous_indent,
            post_adjust_whitespace,
            was_within_block_token,
            containing_block_quote_token,
            containing_list_token,
            deeper_containing_block_quote_token,
        )

    def __rehydrate_list_start_previous_token(
        self,
        current_token: Union[ListStartMarkdownToken, NewListItemMarkdownToken],
        previous_token: MarkdownToken,
        next_token: MarkdownToken,
        extracted_whitespace: str,
    ) -> Tuple[int, str, bool, Optional[str], bool, bool]:
        (
            previous_indent,
            post_adjust_whitespace,
            was_within_block_token,
            containing_block_quote_token,
            containing_list_token,
            deeper_containing_block_quote_token,
        ) = self.__rehydrate_list_start_previous_token_start(
            current_token, previous_token, extracted_whitespace
        )

        had_weird_block_quote_in_list = False
        did_container_start_midline = False
        if previous_token.is_list_start:
            POGGER.debug("rlspt>>is_list_start")
            previous_list_token = cast(ListStartMarkdownToken, previous_token)
            (
                previous_indent,
                extracted_whitespace,
            ) = self.__rehydrate_list_start_prev_list(
                current_token, previous_list_token
            )
        elif previous_token.is_block_quote_start:
            POGGER.debug("rlspt>>is_block_quote_start")
            assert containing_block_quote_token is not None
            (
                previous_indent,
                post_adjust_whitespace,
                extracted_whitespace,
            ) = self.__rehydrate_list_start_prev_block_quote(
                current_token,
                previous_token,
                containing_block_quote_token,
            )
        elif containing_block_quote_token:
            POGGER.debug("rlspt>>containing_block_quote_token")
            (
                was_within_block_token,
                previous_indent,
            ) = self.__rehydrate_list_start_contained_in_block_quote(
                current_token, containing_block_quote_token
            )
        elif containing_list_token:
            POGGER.debug("rlspt>>containing_list_token")
            (
                previous_indent,
                extracted_whitespace,
                post_adjust_whitespace,
                did_container_start_midline,
                had_weird_block_quote_in_list,
            ) = self.__rehydrate_list_start_contained_in_list(
                current_token,
                containing_list_token,
                deeper_containing_block_quote_token,
                extracted_whitespace,
                previous_token,
                next_token,
            )

        POGGER.debug(f"xx>>previous_indent:{previous_indent}:")
        POGGER.debug(f"xx>>extracted_whitespace:{extracted_whitespace}:")
        POGGER.debug(f"xx>>was_within_block_token:{was_within_block_token}:")
        POGGER.debug(f"xx>>post_adjust_whitespace:{post_adjust_whitespace}:")
        POGGER.debug(f"xx>>did_container_start_midline:{did_container_start_midline}:")
        return (
            previous_indent,
            extracted_whitespace,
            was_within_block_token,
            post_adjust_whitespace,
            did_container_start_midline,
            had_weird_block_quote_in_list,
        )

    @classmethod
    def __rehydrate_list_start_prev_list(
        cls,
        current_token: Union[ListStartMarkdownToken, NewListItemMarkdownToken],
        previous_token: ListStartMarkdownToken,
    ) -> Tuple[int, str]:
        _ = current_token
        return previous_token.indent_level, ""

    @classmethod
    def __rehydrate_list_start_prev_block_quote(
        cls,
        current_token: Union[ListStartMarkdownToken, NewListItemMarkdownToken],
        previous_token: MarkdownToken,
        containing_block_quote_token: BlockQuoteMarkdownToken,
    ) -> Tuple[int, str, str]:
        previous_block_token = cast(BlockQuoteMarkdownToken, previous_token)
        assert previous_block_token.bleading_spaces is not None
        previous_indent = (
            len(
                previous_block_token.calculate_next_bleading_space_part(
                    increment_index=False
                )
            )
            if ParserHelper.newline_character in previous_block_token.bleading_spaces
            else len(previous_block_token.bleading_spaces)
        )
        POGGER.debug(
            f"adj->current_token>>:{ParserHelper.make_value_visible(current_token)}:<<"
        )
        POGGER.debug(
            f"adj->containing_block_quote_token>>:{ParserHelper.make_value_visible(containing_block_quote_token)}:<<"
        )
        assert current_token.line_number == containing_block_quote_token.line_number
        assert containing_block_quote_token.bleading_spaces is not None
        split_leading_spaces = containing_block_quote_token.bleading_spaces.split(
            ParserHelper.newline_character
        )
        block_quote_leading_space = split_leading_spaces[0]
        block_quote_leading_space_length = len(block_quote_leading_space)

        POGGER.debug(
            f"bq->len>>:{block_quote_leading_space}: {block_quote_leading_space_length}"
        )

        post_adjust_whitespace = "".ljust(
            current_token.column_number - block_quote_leading_space_length - 1, " "
        )
        extracted_whitespace = ""
        POGGER.debug(
            f"post_adjust_whitespace:{post_adjust_whitespace}: extracted_whitespace:{extracted_whitespace}:"
        )
        return previous_indent, post_adjust_whitespace, extracted_whitespace

    @classmethod
    def __rehydrate_list_start_contained_in_block_quote(
        cls,
        current_token: Union[ListStartMarkdownToken, NewListItemMarkdownToken],
        containing_block_quote_token: BlockQuoteMarkdownToken,
    ) -> Tuple[bool, int]:
        block_quote_leading_space = (
            containing_block_quote_token.calculate_next_bleading_space_part(
                increment_index=False, delta=-1
            )
        )
        previous_indent = len(block_quote_leading_space)
        POGGER.debug(f"adj->rls>>previous_indent>>:{previous_indent}:<<")
        POGGER.debug(
            f"adj->rls>>current_token.indent_level>>:{current_token.indent_level}:<<"
        )

        return True, previous_indent

    @classmethod
    def __rehydrate_list_start_contained_in_list_spacingx(
        cls,
        containing_list_token: ListStartMarkdownToken,
        current_token: Union[NewListItemMarkdownToken, ListStartMarkdownToken],
        block_quote_leading_space_length: int,
    ) -> Tuple[int, str]:
        previous_indent = containing_list_token.indent_level
        white_space_length = (
            len(current_token.extracted_whitespace) + block_quote_leading_space_length
        )
        POGGER.debug(f"adj->len(ws)>>:{white_space_length}:<<")
        extracted_whitespace = (
            "".ljust(white_space_length - previous_indent, " ")
            if white_space_length > previous_indent
            else ""
        )
        POGGER.debug(f"adj->previous_indent>>:{previous_indent}:<<")
        POGGER.debug(
            f"adj->extracted_whitespace>>:{ParserHelper.make_value_visible(extracted_whitespace)}:<<"
        )
        return previous_indent, extracted_whitespace

    @classmethod
    def __rehydrate_list_start_contained_in_list_deeper_block_quote(
        cls,
        previous_token: MarkdownToken,
        deeper_containing_block_quote_token: BlockQuoteMarkdownToken,
        current_token: Union[ListStartMarkdownToken, NewListItemMarkdownToken],
    ) -> Tuple[bool, str, bool, int, bool]:
        assert previous_token is not None
        POGGER.debug(
            f"previous_token:{ParserHelper.make_value_visible(previous_token)}:"
        )
        # if previous_token.is_end_token:
        #     POGGER.debug(
        #         f"previous_token.start_markdown_token:{previous_token.start_markdown_token}:"
        #     )
        POGGER.debug(
            f"deeper_containing_block_quote_token:{ParserHelper.make_value_visible(deeper_containing_block_quote_token)}:"
        )
        had_weird_block_quote_in_list = False
        do_perform_block_quote_ending = False
        if previous_token and previous_token.is_end_token:
            previous_end_token = cast(EndMarkdownToken, previous_token)
            if previous_end_token.start_markdown_token.is_block_quote_start:
                had_weird_block_quote_in_list = True
                POGGER.debug(f"previous_token:{previous_token}:")
                POGGER.debug(
                    f"previous_token.start_markdown_token:{previous_end_token.start_markdown_token}:"
                )
                block_quote_token = cast(
                    BlockQuoteMarkdownToken, previous_end_token.start_markdown_token
                )
                POGGER.debug(
                    f"previous_token.start_markdown_token.leading_spaces:{block_quote_token.bleading_spaces}:"
                )
                assert block_quote_token.bleading_spaces is not None
                newline_count = ParserHelper.count_characters_in_text(
                    block_quote_token.bleading_spaces, "\n"
                )
                previous_start_line = block_quote_token.line_number
                POGGER.debug(f"newline_count:{newline_count}:")
                POGGER.debug(f"previous_start_line:{previous_start_line}:")
                projected_start_line = previous_start_line + (newline_count + 1)
                POGGER.debug(f"projected_start_line:{projected_start_line}:")
                do_perform_block_quote_ending = (
                    projected_start_line != current_token.line_number
                )
        (
            block_quote_leading_space,
            starting_whitespace,
            did_container_start_midline,
            check_list_for_indent,
        ) = cls.__rehydrate_list_start_deep(
            do_perform_block_quote_ending,
            previous_token,
            current_token,
            deeper_containing_block_quote_token,
            had_weird_block_quote_in_list,
        )
        POGGER.debug(
            f"block_quote_leading_space:{ParserHelper.make_value_visible(block_quote_leading_space)}:"
        )

        POGGER.debug(f"starting_whitespace:{starting_whitespace}:")
        return (
            check_list_for_indent,
            starting_whitespace,
            did_container_start_midline,
            len(block_quote_leading_space),
            had_weird_block_quote_in_list,
        )

    # pylint: disable=too-many-arguments
    @classmethod
    def __rehydrate_list_start_deep(
        cls,
        do_perform_block_quote_ending: bool,
        previous_token: MarkdownToken,
        current_token: MarkdownToken,
        deeper_containing_block_quote_token: Optional[BlockQuoteMarkdownToken],
        had_weird_block_quote_in_list: bool,
    ) -> Tuple[str, str, bool, bool]:
        starting_whitespace = ""
        did_container_start_midline = False
        check_list_for_indent = True
        if do_perform_block_quote_ending:
            assert isinstance(previous_token, EndMarkdownToken)
            previous_block_quote_token = cast(
                BlockQuoteMarkdownToken, previous_token.start_markdown_token
            )
            assert previous_block_quote_token.bleading_spaces is not None
            split_leading_spaces = previous_block_quote_token.bleading_spaces.split(
                ParserHelper.newline_character
            )
            POGGER.debug(f"split_leading_spaces>>{split_leading_spaces}")
            POGGER.debug(
                f"current_token>>{ParserHelper.make_value_visible(current_token)}"
            )
            # if (
            #     current_token.is_new_list_item
            #     and len(split_leading_spaces) <= 2
            #     and False
            # ):
            #     block_quote_leading_space = ""
            #     starting_whitespace = ""
            # else:
            POGGER.debug(
                f">>{ParserHelper.make_value_visible(previous_token.start_markdown_token)}"
            )

            block_quote_leading_space = split_leading_spaces[-1]
            starting_whitespace = block_quote_leading_space
            did_container_start_midline = True
            # up to here?
            check_list_for_indent = False
        else:
            assert deeper_containing_block_quote_token is not None
            POGGER.debug(
                f"adj->deeper_containing_block_quote_token.line_number>>:{deeper_containing_block_quote_token.line_number}:<<"
            )

            POGGER.debug(
                f"adj->current_token.line_number>>:{current_token.line_number}:<<"
            )
            line_number_delta = (
                current_token.line_number
                - deeper_containing_block_quote_token.line_number
            )
            POGGER.debug(f"index:{line_number_delta}")
            assert deeper_containing_block_quote_token.bleading_spaces is not None
            split_leading_spaces = (
                deeper_containing_block_quote_token.bleading_spaces.split(
                    ParserHelper.newline_character
                )
            )
            POGGER.debug(
                f"split_leading_spaces:{ParserHelper.make_value_visible(split_leading_spaces)}"
            )

            block_quote_leading_space = split_leading_spaces[line_number_delta]
            if had_weird_block_quote_in_list:
                starting_whitespace = block_quote_leading_space
        return (
            block_quote_leading_space,
            starting_whitespace,
            did_container_start_midline,
            check_list_for_indent,
        )

    # pylint: enable=too-many-arguments

    # pylint: disable=too-many-arguments
    @classmethod
    def __calculate_post_adjust_whitespace(
        cls,
        starting_whitespace: str,
        containing_list_token: ListStartMarkdownToken,
        block_quote_leading_space_length: int,
        list_leading_space_length: int,
        list_start_content_length: int,
        add_extracted_whitespace_at_end: bool,
        current_token: Union[ListStartMarkdownToken, NewListItemMarkdownToken],
    ) -> str:
        POGGER.debug(f"adj->starting_whitespace>>:{starting_whitespace}:<<")
        POGGER.debug(
            f"adj->containing_list_token.indent_level>>:{containing_list_token.indent_level}:<<"
        )
        POGGER.debug(
            f"adj->block_quote_leading_space_length>>:{block_quote_leading_space_length}:<<"
        )
        POGGER.debug(f"adj->list_leading_space_length>>:{list_leading_space_length}:<<")
        POGGER.debug(f"list_start_content_length:{list_start_content_length}:<<")

        pad_to_length = (
            containing_list_token.indent_level
            - block_quote_leading_space_length
            - list_leading_space_length
            - list_start_content_length
        )
        POGGER.debug(f"pad_to_length:{pad_to_length}:<<")
        POGGER.debug(f"adj->starting_whitespace>>:{starting_whitespace}:<<")
        post_adjust_whitespace = starting_whitespace.ljust(pad_to_length, " ")
        POGGER.debug(f"adj->post_adjust_whitespace>>:{post_adjust_whitespace}:<<")
        if add_extracted_whitespace_at_end:
            post_adjust_whitespace += current_token.extracted_whitespace
        POGGER.debug(f"adj->post_adjust_whitespace>>:{post_adjust_whitespace}:<<")
        return post_adjust_whitespace

    # pylint: enable=too-many-arguments

    @classmethod
    def __rehydrate_list_start_contained_in_list_start(
        cls,
        previous_token: MarkdownToken,
        current_token: Union[ListStartMarkdownToken, NewListItemMarkdownToken],
        deeper_containing_block_quote_token: Optional[BlockQuoteMarkdownToken],
    ) -> Tuple[str, bool, int, bool, int]:
        starting_whitespace = ""
        check_list_for_indent = True
        did_container_start_midline = False
        block_quote_leading_space_length = 0
        had_weird_block_quote_in_list = False
        list_leading_space_length = 0

        if deeper_containing_block_quote_token:
            (
                check_list_for_indent,
                starting_whitespace,
                did_container_start_midline,
                block_quote_leading_space_length,
                had_weird_block_quote_in_list,
            ) = cls.__rehydrate_list_start_contained_in_list_deeper_block_quote(
                previous_token, deeper_containing_block_quote_token, current_token
            )

        if (
            check_list_for_indent
            and previous_token
            and previous_token.line_number == current_token.line_number
            and previous_token.is_new_list_item
        ):
            previous_new_list_token = cast(NewListItemMarkdownToken, previous_token)
            list_leading_space_length = previous_new_list_token.indent_level

        return (
            starting_whitespace,
            did_container_start_midline,
            block_quote_leading_space_length,
            had_weird_block_quote_in_list,
            list_leading_space_length,
        )

    # pylint: disable=too-many-arguments, too-many-locals
    @classmethod
    def __rehydrate_list_start_contained_in_list(
        cls,
        current_token: Union[ListStartMarkdownToken, NewListItemMarkdownToken],
        containing_list_token: ListStartMarkdownToken,
        deeper_containing_block_quote_token: Optional[BlockQuoteMarkdownToken],
        extracted_whitespace: str,
        previous_token: MarkdownToken,
        next_token: MarkdownToken,
    ) -> Tuple[int, str, str, bool, bool]:
        # POGGER.debug(
        #     f"adj->containing_list_token>>:{ParserHelper.make_value_visible(containing_list_token)}:<<"
        # )
        # POGGER.debug(
        #     f"adj->deeper_containing_block_quote_token>>:{ParserHelper.make_value_visible(deeper_containing_block_quote_token)}:<<"
        # )

        # POGGER.debug(
        #     f"adj->extracted_whitespace>>:{ParserHelper.make_value_visible(extracted_whitespace)}:<<"
        # )
        (
            starting_whitespace,
            did_container_start_midline,
            block_quote_leading_space_length,
            had_weird_block_quote_in_list,
            list_leading_space_length,
        ) = cls.__rehydrate_list_start_contained_in_list_start(
            previous_token, current_token, deeper_containing_block_quote_token
        )

        list_start_content_length = 0
        add_extracted_whitespace_at_end = False
        # POGGER.debug(
        #     f"previous_token-->{ParserHelper.make_value_visible(previous_token)}"
        # )
        # POGGER.debug(
        #     f"current_token-->{ParserHelper.make_value_visible(current_token)}"
        # )
        # POGGER.debug(f"next_token-->{ParserHelper.make_value_visible(next_token)}")
        if current_token.is_new_list_item and previous_token.is_end_token:
            previous_end_token = cast(EndMarkdownToken, previous_token)
            # POGGER.debug(
            #     f"previous_token.start_markdown_token-->{ParserHelper.make_value_visible(previous_end_token.start_markdown_token)}"
            # )
            if previous_end_token.start_markdown_token.is_block_quote_start:
                new_list_token = cast(NewListItemMarkdownToken, containing_list_token)
                list_start_content_length = (
                    len(new_list_token.list_start_content)
                    if new_list_token.is_ordered_list_start
                    else 0
                )
                add_extracted_whitespace_at_end = not next_token.is_block_quote_start

        post_adjust_whitespace = cls.__calculate_post_adjust_whitespace(
            starting_whitespace,
            containing_list_token,
            block_quote_leading_space_length,
            list_leading_space_length,
            list_start_content_length,
            add_extracted_whitespace_at_end,
            current_token,
        )

        (
            previous_indent,
            extracted_whitespace,
        ) = cls.__rehydrate_list_start_contained_in_list_spacingx(
            containing_list_token, current_token, block_quote_leading_space_length
        )
        # POGGER.debug(f"adj->post_adjust_whitespace>>:{post_adjust_whitespace}:<<")
        return (
            previous_indent,
            extracted_whitespace,
            post_adjust_whitespace,
            did_container_start_midline,
            had_weird_block_quote_in_list,
        )

    # pylint: enable=too-many-arguments, too-many-locals

    # pylint: disable=too-many-arguments
    @classmethod
    def __rehydrate_list_start_calculate_start(
        cls,
        current_token: ListStartMarkdownToken,
        next_token: MarkdownToken,
        extracted_whitespace: str,
        previous_indent: int,
        adjustment_since_newline: int,
        post_adjust_whitespace: Optional[str],
    ) -> str:
        start_sequence = (
            f"{extracted_whitespace}{current_token.list_start_sequence}"
            if current_token.is_unordered_list_start
            else f"{extracted_whitespace}{current_token.list_start_content}{current_token.list_start_sequence}"
        )
        POGGER.debug(f">>start_sequence>>:{start_sequence}:<<")
        old_start_sequence = start_sequence
        if next_token.is_blank_line:
            POGGER.debug("blank-line")
            POGGER.debug(f">>next_token.column_number>>:{next_token.column_number}:<<")
            POGGER.debug(
                f">>current_token.column_number>>:{current_token.column_number}:<<"
            )
            list_content_length = 1
            if not current_token.is_unordered_list_start:
                list_content_length += len(current_token.list_start_content)
            new_column_number = (
                next_token.column_number
                - current_token.column_number
                - list_content_length
            )
            start_sequence += ParserHelper.repeat_string(" ", new_column_number)
        elif next_token.is_list_end:
            POGGER.debug("list-end")
        else:
            POGGER.debug("not list-end and not blank-line")
            # POGGER.debug(
            #     f">>current_token>>:{ParserHelper.make_value_visible(current_token)}:<<"
            # )
            # POGGER.debug(
            #     f">>current_token.indent_level>>:{current_token.indent_level}:<<"
            # )
            POGGER.debug(f">>previous_indent>>:{previous_indent}:<<")
            POGGER.debug(f">>adjustment_since_newline>>:{adjustment_since_newline}:<<")
            requested_indent = (
                current_token.indent_level
                + len(extracted_whitespace)
                - (current_token.column_number - 1)
            )
            POGGER.debug(f">>requested_indent>>:{requested_indent}:<<")
            start_sequence = start_sequence.ljust(requested_indent, " ")
        POGGER.debug(
            f">>current_token>>:{ParserHelper.make_value_visible(current_token)}:<<"
        )
        POGGER.debug(f">>next_token>>:{ParserHelper.make_value_visible(next_token)}:<<")

        start_sequence = cls.__rehydrate_list_start_calculate_start_calc(
            current_token, start_sequence, old_start_sequence, post_adjust_whitespace
        )
        return start_sequence

    # pylint: enable=too-many-arguments

    @classmethod
    def __rehydrate_list_start_calculate_start_calc(
        cls,
        current_token: ListStartMarkdownToken,
        start_sequence: str,
        old_start_sequence: str,
        post_adjust_whitespace: Optional[str],
    ) -> str:
        POGGER.debug(f">>tabbed_adjust>>:{str(current_token.tabbed_adjust)}:<<")
        if current_token.tabbed_adjust >= 0:
            POGGER.debug(f">>start_sequence>>:{start_sequence}:<<")
            POGGER.debug(f">>old_start_sequence>>:{old_start_sequence}:<<")
            spaces_to_consume = current_token.tabbed_adjust + 1
            POGGER.debug(f">>spaces_to_consume>>:{str(spaces_to_consume)}:<<")
            start_sequence = (
                start_sequence[: len(old_start_sequence)]
                + "\t"
                + start_sequence[len(old_start_sequence) + spaces_to_consume :]
            )
            POGGER.debug(
                f">>start_sequence>>:{ParserHelper.make_value_visible(start_sequence)}:<<"
            )

        POGGER.debug(f"<<start_sequence<<:{start_sequence}:<<")
        if post_adjust_whitespace:
            POGGER.debug(
                f"<<post_adjust_whitespace<<(post):{post_adjust_whitespace}:<<"
            )
            start_sequence = post_adjust_whitespace + start_sequence
            POGGER.debug(f"<<start_sequence<<(post):{start_sequence}:<<")

        if current_token.tabbed_extracted_whitespace is not None:
            start_sequence = (
                current_token.tabbed_extracted_whitespace
                + start_sequence[len(current_token.extracted_whitespace) :]
            )
        return start_sequence

    def __rehydrate_list_start(
        self,
        current_token: MarkdownToken,
        previous_token: Optional[MarkdownToken],
        next_token: Optional[MarkdownToken],
        transformed_data: str,
    ) -> str:
        """
        Rehydrate the unordered list start token.
        """

        assert next_token is not None
        POGGER.debug(
            f">>current_token>>{ParserHelper.make_value_visible(current_token)}<<"
        )
        current_list_token = cast(ListStartMarkdownToken, current_token)

        extracted_whitespace = current_list_token.extracted_whitespace
        POGGER.debug(f">>extracted_whitespace>>{extracted_whitespace}<<")
        had_weird_block_quote_in_list = False
        if previous_token:
            (
                previous_indent,
                extracted_whitespace,
                was_within_block_token,
                post_adjust_whitespace,
                _,
                had_weird_block_quote_in_list,
            ) = self.__rehydrate_list_start_previous_token(
                current_list_token, previous_token, next_token, extracted_whitespace
            )
            POGGER.debug(f">>extracted_whitespace>>{extracted_whitespace}<<")
            POGGER.debug(f">>post_adjust_whitespace>>{post_adjust_whitespace}<<")
        else:
            previous_indent, post_adjust_whitespace, was_within_block_token = (
                0,
                None,
                False,
            )

        POGGER.debug(
            f">>had_weird_block_quote_in_list>>{had_weird_block_quote_in_list}<<"
        )
        self.container_token_stack.append(copy.deepcopy(current_list_token))

        POGGER.debug(f">>extracted_whitespace>>{extracted_whitespace}<<")
        POGGER.debug(
            f">>transformed_data>>{ParserHelper.make_value_visible(transformed_data)}<<"
        )

        if was_within_block_token:
            adjustment_since_newline = 0
        else:
            (
                adjustment_since_newline,
                extracted_whitespace,
            ) = self.__adjust_whitespace_for_block_quote(
                transformed_data, extracted_whitespace
            )
        POGGER.debug(f">>adjustment_since_newline>>{adjustment_since_newline}<<")
        POGGER.debug(f">>extracted_whitespace>>{extracted_whitespace}<<")

        return self.__rehydrate_list_start_calculate_start(
            current_list_token,
            next_token,
            extracted_whitespace,
            previous_indent,
            adjustment_since_newline,
            post_adjust_whitespace,
        )

    @classmethod
    def __adjust_whitespace_for_block_quote(
        cls, transformed_data: str, extracted_whitespace: str
    ) -> Tuple[int, str]:
        transformed_data_since_newline = transformed_data
        if ParserHelper.newline_character in transformed_data_since_newline:
            last_newline_index = transformed_data_since_newline.rindex(
                ParserHelper.newline_character
            )
            transformed_data_since_newline = transformed_data_since_newline[
                last_newline_index + 1 :
            ]
        adjustment_since_newline = 0
        # transformed_data_since_newline_size = len(
        #     transformed_data_since_newline
        # )
        POGGER.debug(
            f">>transformed_data_since_newline>>:{transformed_data_since_newline}:<<"
        )
        # POGGER.debug(f">>adjustment_since_newline>>:{adjustment_since_newline}:<<")
        # POGGER.debug(
        #     f">>transformed_data_since_newline_size>>:{transformed_data_since_newline_size}:<<"
        # )
        # POGGER.debug(f">>extracted_whitespace>>:{extracted_whitespace}:<<")
        # if (
        #     extracted_whitespace
        #     and len(extracted_whitespace) >= transformed_data_since_newline_size
        #     and ">" in transformed_data_since_newline
        # ):
        #     adjustment_since_newline = transformed_data_since_newline_size
        #     extracted_whitespace = extracted_whitespace[adjustment_since_newline:]
        POGGER.debug(f">>adjustment_since_newline>>:{adjustment_since_newline}:<<")
        POGGER.debug(f">>extracted_whitespace>>:{extracted_whitespace}:<<")
        return adjustment_since_newline, extracted_whitespace

    def __rehydrate_block_quote_end(
        self,
        current_token: MarkdownToken,
        actual_tokens: List[MarkdownToken],
        token_index: int,
    ) -> str:
        POGGER.debug(">>__rehydrate_block_quote_end")
        _ = current_token

        current_end_token = cast(EndMarkdownToken, current_token)
        current_start_token = cast(
            BlockQuoteMarkdownToken, current_end_token.start_markdown_token
        )

        POGGER.debug(
            f"current_start_block_token>:{ParserHelper.make_value_visible(current_start_token)}:<"
        )
        current_end_token_extra = current_end_token.extra_end_data
        POGGER.debug(
            f"current_end_token_extra>:{ParserHelper.make_value_visible(current_end_token_extra)}:<"
        )
        start_leading_index = current_start_token.leading_text_index
        assert current_start_token.bleading_spaces is not None
        split_start_leading = current_start_token.bleading_spaces.split(
            ParserHelper.newline_character
        )
        POGGER.debug(
            f"start_leading_index>>:{ParserHelper.make_value_visible(start_leading_index)}:<"
        )
        POGGER.debug(
            f"split_start_leading>>:{ParserHelper.make_value_visible(split_start_leading)}:<"
        )
        adjusted_end_string = (
            current_end_token_extra
            if start_leading_index + 1 < len(split_start_leading)
            and current_end_token_extra is not None
            else ""
        )
        POGGER.debug(
            f">>{ParserHelper.make_value_visible(actual_tokens[token_index:])}"
        )
        search_index = token_index + 1
        while (
            search_index < len(actual_tokens)
            and actual_tokens[search_index].is_container_end_token
        ):
            search_index += 1
        POGGER.debug(f">>{search_index}")
        any_non_container_end_tokens = search_index < len(actual_tokens)
        POGGER.debug(f">>{any_non_container_end_tokens}")

        del self.container_token_stack[-1]

        return adjusted_end_string

    def __rehydrate_list_start_end(
        self,
        current_token: MarkdownToken,
        actual_tokens: List[MarkdownToken],
        token_index: int,
    ) -> str:
        """
        Rehydrate the ordered list end token.
        """
        _ = actual_tokens, token_index
        del self.container_token_stack[-1]

        current_end_token = cast(EndMarkdownToken, current_token)
        current_start_token = cast(
            ListStartMarkdownToken, current_end_token.start_markdown_token
        )

        leading_spaces_index, expected_leading_spaces_index = (
            current_start_token.leading_spaces_index,
            ParserHelper.count_newlines_in_text(
                current_start_token.extracted_whitespace
            ),
        )

        assert leading_spaces_index == expected_leading_spaces_index, (
            f"leading_spaces_index={leading_spaces_index};"
            + f"expected_leading_spaces_index={expected_leading_spaces_index}"
        )
        return ""

    def __recalc_adjustment_since_newline(self, adjustment_since_newline: int) -> int:
        assert not adjustment_since_newline
        POGGER.debug(
            f"rnli->container_token_stack>:{ParserHelper.make_value_visible(self.container_token_stack)}:"
        )
        stack_index = len(self.container_token_stack) - 1
        found_block_quote_token: Optional[BlockQuoteMarkdownToken] = None
        while stack_index >= 0:
            if self.container_token_stack[stack_index].is_block_quote_start:
                found_block_quote_token = cast(
                    BlockQuoteMarkdownToken, self.container_token_stack[stack_index]
                )
                break
            stack_index -= 1
        POGGER.debug(
            f"rnli->found_block_quote_token>:{ParserHelper.make_value_visible(found_block_quote_token)}:"
        )
        if found_block_quote_token:
            leading_space = found_block_quote_token.calculate_next_bleading_space_part(
                increment_index=False, delta=-1
            )
            POGGER.debug(f"rnli->leading_space>:{leading_space}:")
            adjustment_since_newline = len(leading_space)
        return adjustment_since_newline

    @classmethod
    def __rehydrate_next_list_item_blank_line(
        cls,
        start_sequence: str,
        current_token: NewListItemMarkdownToken,
        next_token: MarkdownToken,
    ) -> str:
        POGGER.debug(f">>next_token.column_number>>:{next_token.column_number}:<<")
        POGGER.debug(
            f">>current_token.column_number>>:{current_token.column_number}:<<"
        )
        start_content_length = 1
        if current_token.list_start_content:
            start_content_length += len(current_token.list_start_content)
        new_column_number = (
            next_token.column_number
            - current_token.column_number
            - start_content_length
        )
        start_sequence += ParserHelper.repeat_string(" ", new_column_number)
        return start_sequence

    # pylint: disable=too-many-arguments
    def __rehydrate_next_list_item_not_blank_line(
        self,
        start_sequence: str,
        did_container_start_midline: bool,
        adjustment_since_newline: int,
        had_weird_block_quote_in_list: bool,
        next_token: MarkdownToken,
    ) -> str:
        POGGER.debug("__rehydrate_next_list_item_not_blank_line")
        # POGGER.debug(f"start_sequence={start_sequence}=")
        # POGGER.debug(f"did_container_start_midline={did_container_start_midline}=")
        # POGGER.debug(f"adjustment_since_newline={adjustment_since_newline}=")

        assert self.container_token_stack[-1].is_list_start
        assert isinstance(self.container_token_stack[-1], ListStartMarkdownToken)

        if did_container_start_midline:
            POGGER.debug("did start midline")
            # POGGER.debug(f"next_token:{ParserHelper.make_value_visible(next_token)}")
            project_indent_level = self.container_token_stack[-1].indent_level
            if next_token and next_token.is_block_quote_start:
                next_block_token = cast(BlockQuoteMarkdownToken, next_token)
                next_block_quote_leading_space = (
                    next_block_token.calculate_next_bleading_space_part(
                        increment_index=False
                    )
                )
                # POGGER.debug(
                #     f"did start midline:next_block_quote_leading_space:{next_block_quote_leading_space}:"
                # )
                ex_whitespace, _ = ParserHelper.extract_spaces(
                    next_block_quote_leading_space, 0
                )
                assert ex_whitespace is not None
                # POGGER.debug(f"did start midline:ab:{ex_whitespace}:")
                project_indent_level -= ex_whitespace
            start_sequence = start_sequence.ljust(project_indent_level, " ")
        else:
            POGGER.debug("did not start midline")
            calculated_indent = (
                self.container_token_stack[-1].indent_level - adjustment_since_newline
            )
            POGGER.debug(
                f"calculated_indent:{calculated_indent} = indent_level:{self.container_token_stack[-1].indent_level} - adjustment_since_newline:{adjustment_since_newline}"
            )
            POGGER.debug(
                f"had_weird_block_quote_in_list:{had_weird_block_quote_in_list}"
            )
            if had_weird_block_quote_in_list:
                POGGER.debug(f"calculated_indent:{calculated_indent}")
                calculated_indent += 2
                POGGER.debug(f"calculated_indent:{calculated_indent}")
            POGGER.debug(
                f"rnli->calculated_indent={calculated_indent} = "
                + f"indent_level={self.container_token_stack[-1].indent_level} - "
                + f"adjustment_since_newline={adjustment_since_newline}"
            )
            POGGER.debug(f"start_sequence:{start_sequence}")
            start_sequence = start_sequence.ljust(calculated_indent, " ")

            # TODO This is a kludge.  The calc_indent is not properly computed.
            if not start_sequence.endswith(" "):
                start_sequence = f"{start_sequence} "
            POGGER.debug(f"start_sequence:{start_sequence}")
        return start_sequence

    # pylint: enable=too-many-arguments

    def __rehydrate_next_list_item(
        self,
        current_token: MarkdownToken,
        previous_token: Optional[MarkdownToken],
        next_token: Optional[MarkdownToken],
        transformed_data: str,
    ) -> str:
        """
        Rehydrate the next list item token.
        """
        _ = previous_token
        assert next_token is not None

        assert self.container_token_stack[-1].is_list_start
        assert isinstance(self.container_token_stack[-1], ListStartMarkdownToken)

        current_list_token = cast(NewListItemMarkdownToken, current_token)

        POGGER.debug("__rehydrate_next_list_item")
        self.container_token_stack[-1].adjust_for_new_list_item(current_list_token)

        (
            adjustment_since_newline,
            extracted_whitespace,
        ) = self.__adjust_whitespace_for_block_quote(
            transformed_data, current_list_token.extracted_whitespace
        )
        POGGER.debug(f"rnli->adjustment_since_newline>:{adjustment_since_newline}:")
        POGGER.debug(f"rnli->extracted_whitespace>:{extracted_whitespace}:")

        did_container_start_midline = False
        had_weird_block_quote_in_list = False
        assert previous_token
        (
            previous_indent,
            extracted_whitespace2,
            _,
            post_adjust_whitespace,
            did_container_start_midline,
            had_weird_block_quote_in_list,
        ) = self.__rehydrate_list_start_previous_token(
            current_list_token, previous_token, next_token, extracted_whitespace
        )
        # else:
        #     previous_indent, post_adjust_whitespace = (0, None)
        POGGER.debug(f">>previous_indent>>{previous_indent}<<")
        POGGER.debug(f">>extracted_whitespace2>>{extracted_whitespace2}<<")
        POGGER.debug(f">>post_adjust_whitespace>>{post_adjust_whitespace}<<")
        POGGER.debug(
            f">>had_weird_block_quote_in_list>>{had_weird_block_quote_in_list}<<"
        )

        adjustment_since_newline = self.__recalc_adjustment_since_newline(
            adjustment_since_newline
        )
        # assert len(post_adjust_whitespace) == adjustment_since_newline

        whitespace_to_use = (
            post_adjust_whitespace
            if did_container_start_midline or had_weird_block_quote_in_list
            else extracted_whitespace
        )

        POGGER.debug(f"rnli->whitespace_to_use>:{whitespace_to_use}:")
        POGGER.debug(f"rnli->adjustment_since_newline>:{adjustment_since_newline}:")
        POGGER.debug(f"rnli->extracted_whitespace>:{extracted_whitespace}:")
        start_sequence = (
            f"{whitespace_to_use}{current_list_token.list_start_content}"
            + f"{self.container_token_stack[-1].list_start_sequence}"
        )

        POGGER.debug(f"rnli->start_sequence>:{start_sequence}:")
        if next_token.is_blank_line:
            start_sequence = self.__rehydrate_next_list_item_blank_line(
                start_sequence, current_list_token, next_token
            )
        else:
            start_sequence = self.__rehydrate_next_list_item_not_blank_line(
                start_sequence,
                did_container_start_midline,
                adjustment_since_newline,
                had_weird_block_quote_in_list,
                next_token,
            )
        POGGER.debug(f"rnli->start_sequence>:{start_sequence}:")

        return start_sequence

    def __insert_leading_whitespace_at_newlines(self, text_to_modify: str) -> str:
        """
        Deal with re-inserting any removed whitespace at the starts of lines.
        """
        if ParserHelper.newline_character in text_to_modify:
            owning_paragraph_token = next(
                (
                    self.block_stack[search_index]
                    for search_index in range(len(self.block_stack) - 1, -1, -1)
                    if self.block_stack[search_index].is_paragraph
                ),
                None,
            )

            POGGER.debug(
                f"text>before>{ParserHelper.make_value_visible(text_to_modify)}"
            )
            text_to_modify = ParserHelper.remove_all_from_text(text_to_modify)
            POGGER.debug(
                f"text>after>{ParserHelper.make_value_visible(text_to_modify)}"
            )

            if owning_paragraph_token:
                paragraph_token = cast(ParagraphMarkdownToken, owning_paragraph_token)
                (
                    text_to_modify,
                    paragraph_token.rehydrate_index,
                ) = ParserHelper.recombine_string_with_whitespace(
                    text_to_modify,
                    paragraph_token.extracted_whitespace,
                    paragraph_token.rehydrate_index,
                    post_increment_index=False,
                )
        return text_to_modify

    def __rehydrate_inline_image(
        self, current_token: MarkdownToken, previous_token: Optional[MarkdownToken]
    ) -> str:
        """
        Rehydrate the image text from the token.
        """
        _ = previous_token

        if self.block_stack[-1].is_inline_link:
            return ""
        inline_current_token = cast(ImageStartMarkdownToken, current_token)
        POGGER.debug(
            f">>>>>>>>:{ParserHelper.make_value_visible(inline_current_token)}:<<<<<"
        )
        rehydrated_text = LinkSearchHelper.rehydrate_inline_image_text_from_token(
            inline_current_token
        )
        POGGER.debug(
            f">>>>>>>>:{ParserHelper.make_value_visible(rehydrated_text)}:<<<<<"
        )
        return self.__insert_leading_whitespace_at_newlines(rehydrated_text)

    def __rehydrate_inline_link(
        self, current_token: MarkdownToken, previous_token: Optional[MarkdownToken]
    ) -> str:
        """
        Rehydrate the start of the link from the token.
        """
        _ = previous_token

        inline_current_token = cast(LinkStartMarkdownToken, current_token)
        self.block_stack.append(current_token)
        rehydrated_text = LinkSearchHelper.rehydrate_inline_link_text_from_token(
            inline_current_token
        )
        return self.__insert_leading_whitespace_at_newlines(rehydrated_text)

    def __rehydrate_inline_link_end(
        self,
        current_token: MarkdownToken,
        previous_token: Optional[MarkdownToken],
        next_token: Optional[MarkdownToken],
    ) -> str:
        """
        Rehydrate the end of the link from the token.
        """
        return self.__rehydrate_indented_code_block_end(
            current_token, previous_token, next_token
        )

    @classmethod
    def __rehydrate_link_reference_definition(
        cls, current_token: MarkdownToken, previous_token: Optional[MarkdownToken]
    ) -> str:
        """
        Rehydrate the link reference definition from the token.
        """
        _ = previous_token

        current_lrd_token = cast(LinkReferenceDefinitionMarkdownToken, current_token)
        link_title_text = (
            current_lrd_token.link_title_raw or current_lrd_token.link_title
        )
        link_destination_text = (
            current_lrd_token.link_destination_raw or current_lrd_token.link_destination
        )
        assert current_lrd_token.link_destination_whitespace is not None
        assert link_destination_text is not None
        assert current_lrd_token.link_title_whitespace is not None
        assert link_title_text is not None
        assert current_lrd_token.end_whitespace is not None
        link_def_parts: List[str] = [
            current_lrd_token.extracted_whitespace,
            "[",
            current_lrd_token.link_name_debug or current_lrd_token.link_name,
            "]:",
            current_lrd_token.link_destination_whitespace,
            link_destination_text,
            current_lrd_token.link_title_whitespace,
            link_title_text,
            current_lrd_token.end_whitespace,
            ParserHelper.newline_character,
        ]

        return "".join(link_def_parts)

    def __rehydrate_atx_heading(
        self, current_token: MarkdownToken, previous_token: Optional[MarkdownToken]
    ) -> str:
        """
        Rehydrate the atx heading block from the token.
        """
        _ = previous_token

        self.block_stack.append(current_token)
        current_start_token = cast(AtxHeadingMarkdownToken, current_token)
        return f'{current_start_token.extracted_whitespace}{ParserHelper.repeat_string("#", current_start_token.hash_count)}'

    def __rehydrate_atx_heading_end(
        self,
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

        del self.block_stack[-1]
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

    def __rehydrate_setext_heading(
        self, current_token: MarkdownToken, previous_token: Optional[MarkdownToken]
    ) -> str:
        """
        Rehydrate the setext heading from the token.
        """
        _ = previous_token

        self.block_stack.append(current_token)
        current_setext_token = cast(SetextHeadingMarkdownToken, current_token)
        return current_setext_token.extracted_whitespace

    def __rehydrate_setext_heading_end(
        self,
        current_token: MarkdownToken,
        previous_token: Optional[MarkdownToken],
        next_token: Optional[MarkdownToken],
    ) -> str:
        """
        Rehydrate the end of the setext heading block from the token.
        """
        _ = (previous_token, next_token)

        current_start_token = cast(SetextHeadingMarkdownToken, self.block_stack[-1])
        current_end_token = cast(EndMarkdownToken, current_token)

        heading_character = current_start_token.heading_character
        heading_character_count = current_start_token.heading_character_count
        final_whitespace = current_start_token.final_whitespace
        del self.block_stack[-1]
        assert current_end_token.extra_end_data is not None
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

    def __rehydrate_text(
        self, current_token: MarkdownToken, previous_token: Optional[MarkdownToken]
    ) -> str:
        """
        Rehydrate the text from the token.
        """
        _ = previous_token

        if self.block_stack[-1].is_inline_link or self.block_stack[-1].is_inline_image:
            return ""

        prefix_text = ""
        current_text_token = cast(TextMarkdownToken, current_token)
        POGGER.debug(
            f">>rehydrate_text>>:{ParserHelper.make_value_visible(current_text_token.token_text)}:<<"
        )
        # main_text = ParserHelper.resolve_noops_from_text(current_text_token.token_text)
        main_text = ParserHelper.remove_all_from_text(
            current_text_token.token_text, include_noops=True
        )

        POGGER.debug(f"<<rehydrate_text>>{ParserHelper.make_value_visible(main_text)}")

        POGGER.debug(
            f">>leading_whitespace>>:{ParserHelper.make_value_visible(current_text_token.extracted_whitespace)}:<<"
        )
        leading_whitespace = ParserHelper.remove_all_from_text(
            current_text_token.extracted_whitespace
        )
        POGGER.debug(
            f"<<leading_whitespace>>:{ParserHelper.make_value_visible(leading_whitespace)}:<<"
        )

        extra_line = ""
        assert self.block_stack
        if self.block_stack[-1].is_indented_code_block:
            code_block_token = cast(
                IndentedCodeBlockMarkdownToken, self.block_stack[-1]
            )
            (
                main_text,
                prefix_text,
                leading_whitespace,
            ) = self.__reconstitute_indented_text(
                main_text,
                code_block_token.extracted_whitespace,
                code_block_token.indented_whitespace,
                leading_whitespace,
            )
        elif self.block_stack[-1].is_html_block:
            extra_line = ParserHelper.newline_character
        elif self.block_stack[-1].is_paragraph:
            main_text = self.__reconstitute_paragraph_text(
                main_text, current_text_token
            )
        elif self.block_stack[-1].is_setext_heading:
            main_text = self.__reconstitute_setext_text(main_text, current_text_token)

        POGGER.debug(
            f"<<prefix_text>>{ParserHelper.make_value_visible(prefix_text)}"
            + f"<<leading_whitespace>>{ParserHelper.make_value_visible(leading_whitespace)}"
            + f"<<main_text>>{ParserHelper.make_value_visible(main_text)}<<"
        )
        return "".join([prefix_text, leading_whitespace, main_text, extra_line])

    def __rehydrate_hard_break(
        self, current_token: MarkdownToken, previous_token: Optional[MarkdownToken]
    ) -> str:
        """
        Rehydrate the hard break text from the token.
        """
        _ = previous_token

        current_hard_break_token = cast(HardBreakMarkdownToken, current_token)
        leading_whitespace = (
            f"{current_hard_break_token.line_end}{ParserHelper.newline_character}"
        )
        if self.block_stack[-1].is_paragraph:
            block_paragraph_token = cast(ParagraphMarkdownToken, self.block_stack[-1])
            (
                leading_whitespace,
                block_paragraph_token.rehydrate_index,
            ) = ParserHelper.recombine_string_with_whitespace(
                leading_whitespace,
                block_paragraph_token.extracted_whitespace,
                block_paragraph_token.rehydrate_index,
            )

        return "" if self.block_stack[-1].is_inline_link else leading_whitespace

    def __rehydrate_inline_emphaisis(
        self, current_token: MarkdownToken, previous_token: Optional[MarkdownToken]
    ) -> str:
        """
        Rehydrate the emphasis text from the token.
        """
        _ = previous_token

        emphasis_token = cast(EmphasisMarkdownToken, current_token)
        return (
            ""
            if self.block_stack[-1].is_inline_link
            else ParserHelper.repeat_string(
                emphasis_token.emphasis_character, emphasis_token.emphasis_length
            )
        )

    def __rehydrate_inline_emphaisis_end(
        self,
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
            if self.block_stack[-1].is_inline_link
            else ParserHelper.repeat_string(
                emphasis_token.emphasis_character,
                emphasis_token.emphasis_length,
            )
        )

    def __rehydrate_inline_uri_autolink(
        self, current_token: MarkdownToken, previous_token: Optional[MarkdownToken]
    ) -> str:
        """
        Rehydrate the uri autolink from the token.
        """
        _ = previous_token

        current_uri_token = cast(UriAutolinkMarkdownToken, current_token)
        return (
            ""
            if self.block_stack[-1].is_inline_link
            else f"<{current_uri_token.autolink_text}>"
        )

    def __rehydrate_inline_email_autolink(
        self, current_token: MarkdownToken, previous_token: Optional[MarkdownToken]
    ) -> str:
        """
        Rehydrate the email autolink from the token.
        """
        _ = previous_token

        current_email_token = cast(EmailAutolinkMarkdownToken, current_token)
        return (
            ""
            if self.block_stack[-1].is_inline_link
            else f"<{current_email_token.autolink_text}>"
        )

    def __rehydrate_inline_raw_html(
        self, current_token: MarkdownToken, previous_token: Optional[MarkdownToken]
    ) -> str:
        """
        Rehydrate the email raw html from the token.
        """
        _ = previous_token

        if self.block_stack[-1].is_inline_link:
            return ""

        current_raw_token = cast(RawHtmlMarkdownToken, current_token)
        raw_text = ParserHelper.remove_all_from_text(current_raw_token.raw_tag)

        if self.block_stack[-1].is_paragraph:
            block_paragraph_token = cast(ParagraphMarkdownToken, self.block_stack[-1])
            POGGER.debug(
                f"raw_html>>before>>{ParserHelper.make_value_visible(raw_text)}"
            )
            block_paragraph_token.rehydrate_index += (
                ParserHelper.count_newlines_in_text(raw_text)
            )
            POGGER.debug(
                f"raw_html>>after>>{ParserHelper.make_value_visible(raw_text)}"
            )
        return f"<{raw_text}>"

    def __rehydrate_inline_code_span(
        self, current_token: MarkdownToken, previous_token: Optional[MarkdownToken]
    ) -> str:
        """
        Rehydrate the code span data from the token.
        """
        _ = previous_token

        if self.block_stack[-1].is_inline_link:
            return ""

        current_inline_token = cast(InlineCodeSpanMarkdownToken, current_token)
        span_text = ParserHelper.remove_all_from_text(current_inline_token.span_text)
        leading_whitespace = ParserHelper.remove_all_from_text(
            current_inline_token.leading_whitespace
        )
        trailing_whitespace = ParserHelper.remove_all_from_text(
            current_inline_token.trailing_whitespace
        )

        if self.block_stack[-1].is_paragraph:
            block_paragraph_token = cast(ParagraphMarkdownToken, self.block_stack[-1])
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

    @classmethod
    def __rehydrate_thematic_break(
        cls, current_token: MarkdownToken, previous_token: Optional[MarkdownToken]
    ) -> str:
        """
        Rehydrate the thematic break text from the token.
        """
        _ = previous_token

        current_thematic_token = cast(ThematicBreakMarkdownToken, current_token)
        return "".join(
            [
                current_thematic_token.extracted_whitespace,
                current_thematic_token.rest_of_line,
                ParserHelper.newline_character,
            ]
        )

    def __reconstitute_paragraph_text(
        self, main_text: str, current_token: TextMarkdownToken
    ) -> str:
        """
        For a paragraph block, figure out the text that got us here.
        """
        if ParserHelper.newline_character in main_text:
            owner_paragraph_token = cast(ParagraphMarkdownToken, self.block_stack[-1])
            (
                main_text,
                owner_paragraph_token.rehydrate_index,
            ) = ParserHelper.recombine_string_with_whitespace(
                main_text,
                owner_paragraph_token.extracted_whitespace,
                owner_paragraph_token.rehydrate_index,
            )
            assert current_token.end_whitespace
            main_text, _ = ParserHelper.recombine_string_with_whitespace(
                main_text,
                current_token.end_whitespace,
                start_text_index=0,
                post_increment_index=True,
                add_whitespace_after=True,
            )
        return main_text

    @classmethod
    def __reconstitute_indented_text(
        cls,
        main_text: str,
        prefix_text: str,
        indented_whitespace: str,
        leading_whitespace: str,
    ) -> Tuple[str, str, str]:
        """
        For an indented code block, figure out the text that got us here.
        """
        recombined_text, _ = ParserHelper.recombine_string_with_whitespace(
            main_text,
            f"{prefix_text}{leading_whitespace}{indented_whitespace}",
            start_text_index=0,
            post_increment_index=True,
        )
        return f"{recombined_text}{ParserHelper.newline_character}", "", ""

    @classmethod
    def __reconstitute_setext_text_item(
        cls,
        text_part_index: int,
        text_part_value: str,
        rejoined_token_text: List[str],
        split_parent_whitespace_text: List[str],
    ) -> None:
        ws_prefix_text = ""
        ws_suffix_text = ""
        if split_parent_whitespace_text[text_part_index]:
            split_setext_text = split_parent_whitespace_text[text_part_index].split(
                ParserHelper.whitespace_split_character
            )
            split_setext_text_size = len(split_setext_text)
            if split_setext_text_size == 1:
                assert text_part_index == 0
                ws_suffix_text = split_setext_text[0]
                # if text_part_index == 0:
                #     ws_suffix_text = split_setext_text[0]
                # else:
                #     ws_prefix_text = split_setext_text[0]
            else:
                assert split_setext_text_size == 2
                ws_prefix_text = split_setext_text[0]
                ws_suffix_text = split_setext_text[1]

        rejoined_token_text.append(
            "".join([ws_prefix_text, text_part_value, ws_suffix_text])
        )

    @classmethod
    def __reconstitute_setext_text(
        cls, main_text: str, current_token: TextMarkdownToken
    ) -> str:
        """
        For a setext heading block, figure out the text that got us here.

        Because of the unique formatting of the setext data, the recombine_string_with_whitespace
        function cannot be used for this.
        """

        if ParserHelper.newline_character in main_text:
            split_token_text = main_text.split(ParserHelper.newline_character)
            assert current_token.end_whitespace is not None
            split_parent_whitespace_text = current_token.end_whitespace.split(
                ParserHelper.newline_character
            )

            rejoined_token_text: List[str] = []
            for text_part_index, text_part_value in enumerate(split_token_text):
                cls.__reconstitute_setext_text_item(
                    text_part_index,
                    text_part_value,
                    rejoined_token_text,
                    split_parent_whitespace_text,
                )

            main_text = ParserHelper.newline_character.join(rejoined_token_text)
        else:
            POGGER.debug(f"main_text>>{ParserHelper.make_value_visible(main_text)}")
            POGGER.debug(
                f"current_token>>{ParserHelper.make_value_visible(current_token)}"
            )
            if current_token.end_whitespace and current_token.end_whitespace.endswith(
                ParserHelper.whitespace_split_character
            ):
                main_text = f"{current_token.end_whitespace[:-1]}{main_text}"
        return main_text
