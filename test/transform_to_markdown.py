"""
Module to provide for a transformation from tokens to a markdown document.
"""
import collections
import copy
import inspect

from pymarkdown.container_markdown_token import (
    BlockQuoteMarkdownToken,
    NewListItemMarkdownToken,
    OrderedListStartMarkdownToken,
    UnorderedListStartMarkdownToken,
)
from pymarkdown.extensions.front_matter_extension import FrontMatterExtension
from pymarkdown.extensions.front_matter_markdown_token import FrontMatterMarkdownToken
from pymarkdown.inline_markdown_token import (
    EmailAutolinkMarkdownToken,
    EmphasisMarkdownToken,
    HardBreakMarkdownToken,
    ImageStartMarkdownToken,
    InlineCodeSpanMarkdownToken,
    LinkStartMarkdownToken,
    RawHtmlMarkdownToken,
    TextMarkdownToken,
    UriAutolinkMarkdownToken,
)
from pymarkdown.leaf_markdown_token import (
    AtxHeadingMarkdownToken,
    BlankLineMarkdownToken,
    FencedCodeBlockMarkdownToken,
    HtmlBlockMarkdownToken,
    IndentedCodeBlockMarkdownToken,
    LinkReferenceDefinitionMarkdownToken,
    ParagraphMarkdownToken,
    SetextHeadingMarkdownToken,
    ThematicBreakMarkdownToken,
)
from pymarkdown.link_helper import LinkHelper
from pymarkdown.markdown_token import MarkdownToken
from pymarkdown.parser_helper import ParserHelper


# pylint: disable=too-many-lines
class TransformToMarkdown:
    """
    Class to provide for a transformation from tokens to a markdown document.
    """

    def __init__(self):
        """
        Initializes a new instance of the TransformToMarkdown class.
        """
        (
            self.block_stack,
            self.container_token_stack,
            self.start_container_token_handlers,
            self.end_container_token_handlers,
            self.start_token_handlers,
            self.end_token_handlers,
        ) = ([], [], {}, {}, {}, {})

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

    @classmethod
    def __create_type_instance(cls, type_name):
        """
        Create an instance of the specified type.
        """

        assert issubclass(
            type_name, MarkdownToken
        ), f"Token class '{type_name}' must be descended from the 'MarkdownToken' class."
        token_init_fn, init_parameters = type_name.__dict__["__init__"], {}
        for i in inspect.getfullargspec(token_init_fn)[0]:
            if i == "self":
                continue
            init_parameters[i] = ""
        return type_name(**init_parameters)

    def register_handlers(self, type_name, start_token_handler, end_token_handler=None):
        """
        Register the handlers necessary to deal with token's start and end.
        """
        handler_instance = self.__create_type_instance(type_name)
        assert handler_instance.is_leaf or handler_instance.is_inline

        self.start_token_handlers[handler_instance.token_name] = start_token_handler
        if end_token_handler:
            self.end_token_handlers[handler_instance.token_name] = end_token_handler

    def register_container_handlers(
        self, type_name, start_token_handler, end_token_handler=None
    ):
        """
        Register the handlers necessary to deal with token's start and end.
        """
        handler_instance = self.__create_type_instance(type_name)
        assert handler_instance.is_container

        self.start_container_token_handlers[
            handler_instance.token_name
        ] = start_token_handler
        if end_token_handler:
            self.end_container_token_handlers[
                handler_instance.token_name
            ] = end_token_handler

    @classmethod
    def __transform_container_start(
        cls,
        container_stack,
        container_records,
        transformed_data_length_before_add,
        current_token,
    ):
        if not container_stack:
            container_records.clear()
        container_stack.append(current_token)
        record_item = (True, transformed_data_length_before_add, current_token)
        container_records.append(record_item)
        # print("START:" + ParserHelper.make_value_visible(current_token))
        # print(">>" + ParserHelper.make_value_visible(container_stack))
        # print(">>" + ParserHelper.make_value_visible(container_records))

    # pylint: disable=too-many-arguments
    def __transform_container_end(
        self,
        container_stack,
        container_records,
        current_token,
        transformed_data,
        actual_tokens,
    ):
        # print("END:" + ParserHelper.make_value_visible(current_token.start_markdown_token))
        while container_stack[-1].is_new_list_item:
            del container_stack[-1]
        assert str(container_stack[-1]) == str(current_token.start_markdown_token), (
            ParserHelper.make_value_visible(container_stack[-1])
            + "=="
            + ParserHelper.make_value_visible(current_token.start_markdown_token)
        )
        del container_stack[-1]
        record_item = (
            False,
            len(transformed_data),
            current_token.start_markdown_token,
        )
        container_records.append(record_item)
        # print(">>" + ParserHelper.make_value_visible(container_stack))
        # print(">>" + ParserHelper.make_value_visible(container_records))

        if not container_stack:
            record_item = container_records[0]
            assert record_item[0]
            pre_container_text = transformed_data[: record_item[1]]
            container_text = transformed_data[record_item[1] :]
            adjusted_text = self.__apply_container_transformation(
                container_text, container_records, actual_tokens
            )
            print(f"pre>:{pre_container_text}:<")
            print(f"adj>:{adjusted_text}:<")
            transformed_data = pre_container_text + adjusted_text
            print(f"trn>:{transformed_data}:<")
        return transformed_data

    # pylint: enable=too-many-arguments

    def transform(self, actual_tokens):  # noqa: C901
        """
        Transform the incoming token stream back into Markdown.
        """
        (
            transformed_data,
            previous_token,
            container_stack,
            container_records,
            pragma_token,
        ) = ("", None, [], [], None)

        print("---\nTransformToMarkdown\n---")

        for token_index, current_token in enumerate(actual_tokens):

            next_token = (
                actual_tokens[token_index + 1]
                if token_index < len(actual_tokens) - 1
                else None
            )

            print(
                f"pre-h>current_token>:{ParserHelper.make_value_visible(current_token)}:"
            )
            (new_data, pragma_token,) = self.__process_next_token(
                current_token,
                previous_token,
                next_token,
                transformed_data,
                actual_tokens,
                token_index,
            )

            print(f"post-h>new_data>:{ParserHelper.make_value_visible(new_data)}:")
            transformed_data_length_before_add = len(transformed_data)
            print(
                f"post-h>transformed_data>:{ParserHelper.make_value_visible(transformed_data)}:"
            )
            transformed_data += new_data
            print(
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

            print("---")
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
        container_records,
        old_record_index,
        token_stack,
        container_token_indices,
        removed_tokens,
    ):
        did_move_ahead, current_changed_record = (
            True,
            container_records[old_record_index + 1],
        )
        print(
            "   current_changed_record("
            + str(old_record_index + 1)
            + ")-->"
            + ParserHelper.make_value_visible(current_changed_record)
        )
        if current_changed_record[0]:
            token_stack.append(current_changed_record[2])
            container_token_indices.append(0)
        else:
            print(f"   -->{ParserHelper.make_value_visible(token_stack)}")
            print(f"   -->{ParserHelper.make_value_visible(container_token_indices)}")

            if token_stack[-1].is_new_list_item:
                removed_tokens.append(token_stack[-1])
                del token_stack[-1]
                del container_token_indices[-1]

            assert str(current_changed_record[2]) == str(token_stack[-1]), (
                "end:"
                + ParserHelper.make_value_visible(current_changed_record[2])
                + "!="
                + ParserHelper.make_value_visible(token_stack[-1])
            )
            removed_tokens.append(token_stack[-1])
            del token_stack[-1]
            del container_token_indices[-1]

        print(
            "   -->current_changed_recordx>"
            + ParserHelper.make_value_visible(current_changed_record)
        )
        print(f"   -->{ParserHelper.make_value_visible(token_stack)}")
        print(f"   -->{ParserHelper.make_value_visible(container_token_indices)}")
        old_record_index += 1
        return old_record_index, did_move_ahead, current_changed_record

    # pylint: enable=too-many-arguments

    # pylint: disable=too-many-arguments
    @classmethod
    def __move_to_current_record(
        cls,
        old_record_index,
        container_records,
        container_text_index,
        token_stack,
        container_token_indices,
        container_line_length,
    ):
        record_index, current_changed_record, did_move_ahead = (
            old_record_index,
            None,
            False,
        )

        print(f"({container_text_index})")
        print(
            "("
            + str(record_index + 1)
            + "):"
            + ParserHelper.make_value_visible(container_records[1])
        )
        while record_index + 1 < len(container_records) and container_records[
            record_index + 1
        ][1] <= (container_text_index + container_line_length):
            record_index += 1
        print(
            "("
            + str(record_index + 1)
            + "):"
            + ParserHelper.make_value_visible(container_records[1])
        )
        removed_tokens = []
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

        print(f"   removed_tokens={ParserHelper.make_value_visible(removed_tokens)}")
        return record_index, did_move_ahead, current_changed_record, removed_tokens

    # pylint: enable=too-many-arguments

    # pylint: disable=too-many-arguments
    @classmethod
    def __adjust_state_for_element(
        cls,
        token_stack,
        container_token_indices,
        did_move_ahead,
        current_changed_record,
        last_container_token_index,
    ):
        print(f" -->{ParserHelper.make_value_visible(token_stack)}")
        print(f" -->{ParserHelper.make_value_visible(container_token_indices)}")
        did_change_to_list_token = (
            did_move_ahead
            and current_changed_record[0]
            and (token_stack[-1].is_list_start or token_stack[-1].is_new_list_item)
        )

        # May need earlier if both new item and start of new list on same line
        if not did_change_to_list_token:
            container_token_indices[-1] = last_container_token_index + 1
        elif token_stack[-1].is_new_list_item:
            del token_stack[-1]
            del container_token_indices[-1]
        print(f" -->{ParserHelper.make_value_visible(token_stack)}")
        print(f" -->{ParserHelper.make_value_visible(container_token_indices)}")

    # pylint: enable=too-many-arguments

    # pylint: disable=too-many-arguments
    @classmethod
    def __apply_primary_transformation(
        cls,
        did_move_ahead,
        token_stack,
        container_token_indices,
        current_changed_record,
        container_line,
        actual_tokens,
    ):
        print(f" -->did_move_ahead>{ParserHelper.make_value_visible(did_move_ahead)}")
        print(f" -->{ParserHelper.make_value_visible(token_stack)}")
        print(f" -->{ParserHelper.make_value_visible(container_token_indices)}")
        print(
            " -->current_changed_record>"
            + ParserHelper.make_value_visible(current_changed_record)
        )
        is_list_start_after_two_block_starts = False
        if current_changed_record and current_changed_record[2].is_list_start:
            list_start_token = current_changed_record[2]
            list_start_token_index = actual_tokens.index(list_start_token)
            print(
                " -->list_start_token_index>"
                + ParserHelper.make_value_visible(list_start_token_index)
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

        last_container_token_index = container_token_indices[-1]

        applied_leading_spaces_to_start_of_container_line = (
            not (did_move_ahead and current_changed_record[0])
            and not is_list_start_after_two_block_starts
        )
        if applied_leading_spaces_to_start_of_container_line:
            print(f" container->{ParserHelper.make_value_visible(token_stack[-1])}")
            split_leading_spaces = token_stack[-1].leading_spaces.split(
                ParserHelper.newline_character
            )
            if last_container_token_index < len(split_leading_spaces):
                print(f" -->{ParserHelper.make_value_visible(split_leading_spaces)}")
                print(
                    " primary-->container_line>:"
                    + ParserHelper.make_value_visible(container_line)
                    + ":<"
                )
                container_line = (
                    split_leading_spaces[last_container_token_index] + container_line
                )
                print(
                    " -->container_line>:"
                    + ParserHelper.make_value_visible(container_line)
                    + ":<"
                )
        return (
            last_container_token_index,
            applied_leading_spaces_to_start_of_container_line,
            container_line,
        )

    # pylint: enable=too-many-arguments

    @classmethod
    def __find_last_block_quote_on_stack(cls, token_stack):
        print(" looking for nested block start")
        stack_index = len(token_stack) - 2
        nested_block_start_index = -1
        while stack_index >= 0:
            if token_stack[stack_index].is_block_quote_start:
                nested_block_start_index = stack_index
                break
            stack_index -= 1
        return nested_block_start_index

    @classmethod
    def __xx(
        cls,
        token_stack,
        removed_tokens,
        applied_leading_spaces_to_start_of_container_line,
        previous_token,
    ):
        if not token_stack[-1].is_new_list_item:

            return (
                applied_leading_spaces_to_start_of_container_line
                or token_stack[-1].line_number != previous_token.line_number
            )
        new_list_item_adjust = True
        if len(removed_tokens) == 1 and removed_tokens[-1].is_block_quote_start:
            leading_spaces_newline_count = removed_tokens[-1].leading_spaces.count("\n")
            block_quote_end_line = (
                leading_spaces_newline_count + removed_tokens[-1].line_number
            )
            print(
                f"block_quote_end_line={block_quote_end_line} = "
                + f"fg={leading_spaces_newline_count} + "
                + f"line={removed_tokens[-1].line_number}"
            )
            new_list_item_adjust = leading_spaces_newline_count > 1
            print(f"new_list_item_adjust:{new_list_item_adjust}")

        return (
            token_stack[-1].line_number != previous_token.line_number
            and new_list_item_adjust
        )

    # pylint: disable=too-many-arguments
    @classmethod
    def __adjust_for_list(
        cls,
        token_stack,
        applied_leading_spaces_to_start_of_container_line,
        container_token_indices,
        container_line,
        removed_tokens,
    ):

        if (
            len(token_stack) > 1
            and token_stack[-1].is_list_start
            or token_stack[-1].is_new_list_item
        ):
            nested_block_start_index = (
                TransformToMarkdown.__find_last_block_quote_on_stack(token_stack)
            )
            if nested_block_start_index != -1:
                print(f"nested_block_start_index>{nested_block_start_index}")
                previous_token = token_stack[nested_block_start_index]
                print(f"previous={ParserHelper.make_value_visible(previous_token)}")
                print(
                    " applied_leading_spaces_to_start_of_container_line->"
                    + str(applied_leading_spaces_to_start_of_container_line)
                )
                inner_token_index = container_token_indices[nested_block_start_index]
                print(
                    f"applied:{applied_leading_spaces_to_start_of_container_line} or "
                    + f"end.line:{token_stack[-1].line_number} != prev.line:{previous_token.line_number}"
                )

                if cls.__xx(
                    token_stack,
                    removed_tokens,
                    applied_leading_spaces_to_start_of_container_line,
                    previous_token,
                ):
                    split_leading_spaces = previous_token.leading_spaces.split(
                        ParserHelper.newline_character
                    )
                    print(
                        f"inner_token_index={inner_token_index} < len(split)={len(split_leading_spaces)}"
                    )
                    if inner_token_index < len(split_leading_spaces):
                        print(
                            " adj-->container_line>:"
                            + ParserHelper.make_value_visible(container_line)
                            + ":<"
                        )
                        container_line = (
                            split_leading_spaces[inner_token_index] + container_line
                        )
                        print(
                            " adj-->container_line>:"
                            + ParserHelper.make_value_visible(container_line)
                            + ":<"
                        )
                container_token_indices[nested_block_start_index] = (
                    inner_token_index + 1
                )
        return container_line

    # pylint: enable=too-many-arguments

    @classmethod
    def __get_last_list_index(cls, token_stack):
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
        container_line,
        nested_list_start_index,
        token_stack,
        container_token_indices,
    ):
        adj_line = ""
        print(f"adj_line->:{adj_line}:")
        adj_line = cls.__adjust(
            nested_list_start_index - 1,
            token_stack,
            container_token_indices,
            adj_line,
            True,
        )
        print(f"adj_line->:{adj_line}:")
        adj_line = cls.__adjust(
            nested_list_start_index,
            token_stack,
            container_token_indices,
            adj_line,
            True,
        )
        print(f"adj_line->:{adj_line}:")
        container_line = adj_line + container_line
        return container_line

    # pylint: disable=too-many-arguments
    @classmethod
    def __adjust_for_block_quote_previous_line(
        cls,
        container_line,
        nested_list_start_index,
        token_stack,
        container_token_indices,
        line_number,
    ):
        previous_token = token_stack[nested_list_start_index]
        print(f"nested_list_start_index->{nested_list_start_index}")
        print(f" yes->{ParserHelper.make_value_visible(previous_token)}")

        print(f"token_stack[-1].line_number->{token_stack[-1].line_number}")
        print(f"previous_token.line_number->{previous_token.line_number}")
        print(f"line_number->{line_number}")
        if (
            token_stack[-1].line_number != previous_token.line_number
            or line_number != previous_token.line_number
        ):
            print("different line as list start")
            container_line = cls.__adjust(
                nested_list_start_index,
                token_stack,
                container_token_indices,
                container_line,
                False,
            )
        else:
            print("same line as list start")
            if nested_list_start_index > 0:
                next_level_index = nested_list_start_index - 1
                pre_previous_token = token_stack[next_level_index]
                print(
                    f" pre_previous_token->{ParserHelper.make_value_visible(pre_previous_token)}"
                )
                if pre_previous_token.is_block_quote_start:
                    different_line_prefix = cls.__adjust(
                        next_level_index,
                        token_stack,
                        container_token_indices,
                        "",
                        False,
                    )
                    print(f"different_line_prefix>:{different_line_prefix}:<")
                    if pre_previous_token.line_number != previous_token.line_number:
                        container_line = different_line_prefix + container_line
        return container_line

    # pylint: enable=too-many-arguments

    @classmethod
    def __adjust_for_block_quote(
        cls, token_stack, container_line, container_token_indices, line_number
    ):

        if not (len(token_stack) > 1 and token_stack[-1].is_block_quote_start):
            return container_line

        print(" looking for nested list start")
        nested_list_start_index = TransformToMarkdown.__get_last_list_index(token_stack)
        print(f" afbq={len(token_stack) - 1}")
        print(f" nested_list_start_index={nested_list_start_index}")
        if nested_list_start_index == -1:
            print(" nope")
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
        nested_list_start_index,
        token_stack,
        container_token_indices,
        container_line,
        apply_list_fix,
    ):
        previous_token = token_stack[nested_list_start_index]
        if apply_list_fix and previous_token.is_list_start:
            delta = previous_token.indent_level - len(container_line)
            print(f"delta->{delta}")
            container_line += ParserHelper.repeat_string(" ", delta)
        leading_spaces = (
            ""
            if previous_token.leading_spaces is None
            else previous_token.leading_spaces
        )
        split_leading_spaces = leading_spaces.split(ParserHelper.newline_character)
        inner_token_index = container_token_indices[nested_list_start_index]
        if inner_token_index < len(split_leading_spaces):
            print(
                f"inner_index->{str(container_token_indices[nested_list_start_index])}"
            )
            container_line = split_leading_spaces[inner_token_index] + container_line
            container_token_indices[nested_list_start_index] = inner_token_index + 1
            print(
                f"inner_index->{str(container_token_indices[nested_list_start_index])}"
            )
        return container_line

    # pylint: enable=too-many-arguments

    # pylint: disable=too-many-locals
    def __apply_container_transformation(
        self, container_text, container_records, actual_tokens
    ):
        print(f">>incoming>>:{ParserHelper.make_value_visible(container_text)}:<<")

        print(
            f">>container_records>>{ParserHelper.make_value_visible(container_records)}"
        )

        (
            base_line_number,
            delta_line,
            split_container_text,
            transformed_parts,
            token_stack,
            container_token_indices,
            record_index,
            container_text_index,
            current_changed_record,
        ) = (
            container_records[0][2].line_number,
            0,
            container_text.split(ParserHelper.newline_character),
            [],
            [],
            [],
            -1,
            container_records[0][1],
            None,
        )
        print(
            ">>split_container_text>>"
            + ParserHelper.make_value_visible(split_container_text)
        )

        for container_line in split_container_text:
            container_line_length = len(container_line)
            print(
                ParserHelper.newline_character
                + str(delta_line)
                + "("
                + str(base_line_number + delta_line)
                + ")>>container_line>>"
                + str(container_text_index)
                + "-"
                + str(container_text_index + container_line_length)
                + ":>:"
                + ParserHelper.make_value_visible(container_line)
                + ":<"
            )

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

        print("\n<<transformed<<" + ParserHelper.make_value_visible(transformed_parts))
        return ParserHelper.newline_character.join(transformed_parts)

    # pylint: enable=too-many-locals

    def __look_for_last_block_token(self):
        found_block_token = next(
            (
                self.container_token_stack[i]
                for i in range(len(self.container_token_stack) - 1, -1, -1)
                if self.container_token_stack[i].is_block_quote_start
            ),
            None,
        )
        print(
            f">>found_block_token>>{ParserHelper.make_value_visible(found_block_token)}<"
        )
        if found_block_token:
            print(
                f">>found_block_token-->index>>{found_block_token.leading_text_index}<"
            )
        return found_block_token

    @classmethod
    def __correct_for_final_newline(cls, transformed_data, actual_tokens):
        if (
            transformed_data
            and transformed_data[-1] == ParserHelper.newline_character
            and not (
                actual_tokens[-1].is_fenced_code_block_end
                and actual_tokens[-1].was_forced
                and not actual_tokens[-2].is_fenced_code_block
            )
        ):
            transformed_data = transformed_data[:-1]
        return transformed_data

    @classmethod
    def __handle_pragma_processing(cls, pragma_token, transformed_data):
        ordered_lines = collections.OrderedDict(
            sorted(pragma_token.pragma_lines.items())
        )

        for next_line_number in ordered_lines:
            if next_line_number == 1:
                if transformed_data:
                    transformed_data = (
                        f"{ordered_lines[next_line_number]}"
                        + f"{ParserHelper.newline_character}{transformed_data}"
                    )
                else:
                    transformed_data = ordered_lines[next_line_number]
            else:
                nth_index = ParserHelper.find_nth_occurrence(
                    transformed_data,
                    ParserHelper.newline_character,
                    next_line_number - 1,
                )
                if nth_index == -1:
                    transformed_data = (
                        f"{transformed_data}{ParserHelper.newline_character}"
                        + f"{ordered_lines[next_line_number]}"
                    )
                else:
                    transformed_data = (
                        f"{transformed_data[:nth_index]}{ParserHelper.newline_character}"
                        + f"{ordered_lines[next_line_number]}{transformed_data[nth_index:]}"
                    )
        return transformed_data

    # pylint: disable=too-many-arguments
    def __process_next_token(
        self,
        current_token,
        previous_token,
        next_token,
        transformed_data,
        actual_tokens,
        token_index,
    ):

        pragma_token = None
        if current_token.token_name in self.start_container_token_handlers:
            start_handler_fn = self.start_container_token_handlers[
                current_token.token_name
            ]
            new_data = start_handler_fn(
                current_token, previous_token, next_token, transformed_data
            )

        elif current_token.token_name in self.start_token_handlers:
            start_handler_fn = self.start_token_handlers[current_token.token_name]
            new_data = start_handler_fn(current_token, previous_token)

        elif current_token.is_pragma:
            new_data = ""
            pragma_token = current_token
        elif current_token.is_end_token:
            if current_token.type_name in self.end_token_handlers:
                end_handler_fn = self.end_token_handlers[current_token.type_name]
                new_data = end_handler_fn(current_token, previous_token, next_token)
            elif current_token.type_name in self.end_container_token_handlers:
                end_handler_fn = self.end_container_token_handlers[
                    current_token.type_name
                ]
                new_data = end_handler_fn(current_token, actual_tokens, token_index)
            else:
                raise AssertionError(f"end_current_token>>{current_token.type_name}")
        else:
            raise AssertionError(f"current_token>>{current_token}")
        return new_data, pragma_token

    # pylint: enable=too-many-arguments

    def __rehydrate_paragraph(self, current_token, previous_token):
        """
        Rehydrate the paragraph block from the token.
        """
        _ = previous_token

        self.block_stack.append(current_token)
        current_token.rehydrate_index = 0
        extracted_whitespace = current_token.extracted_whitespace
        if ParserHelper.newline_character in extracted_whitespace:
            line_end_index = extracted_whitespace.index(ParserHelper.newline_character)
            extracted_whitespace = extracted_whitespace[:line_end_index]
        return ParserHelper.resolve_all_from_text(extracted_whitespace)

    def __rehydrate_paragraph_end(self, current_token, previous_token, next_token):
        """
        Rehydrate the end of the paragraph block from the token.
        """
        _ = (previous_token, next_token)

        top_stack_token = self.block_stack[-1]
        del self.block_stack[-1]

        rehydrate_index, expected_rehydrate_index = (
            current_token.start_markdown_token.rehydrate_index,
            ParserHelper.count_newlines_in_text(
                current_token.start_markdown_token.extracted_whitespace
            ),
        )
        assert (
            rehydrate_index == expected_rehydrate_index
        ), f"rehydrate_index={rehydrate_index};expected_rehydrate_index={expected_rehydrate_index}"
        return f"{top_stack_token.final_whitespace}{ParserHelper.newline_character}"

    def __rehydrate_blank_line(self, current_token, previous_token):
        """
        Rehydrate the blank line from the token.
        """
        if (
            self.block_stack
            and self.block_stack[-1].is_fenced_code_block
            and previous_token.is_text
        ):
            extra_newline_after_text_token = ParserHelper.newline_character
        else:
            extra_newline_after_text_token = ""

        return f"{extra_newline_after_text_token}{current_token.extracted_whitespace}{ParserHelper.newline_character}"

    def __rehydrate_indented_code_block(self, current_token, previous_token):
        """
        Rehydrate the indented code block from the token.
        """
        _ = previous_token

        self.block_stack.append(current_token)
        return ""

    def __rehydrate_indented_code_block_end(
        self, current_token, previous_token, next_token
    ):
        """
        Rehydrate the end of the indented code block from the token.
        """
        _ = (current_token, previous_token, next_token)

        del self.block_stack[-1]
        return ""

    def __rehydrate_html_block(self, current_token, previous_token):
        """
        Rehydrate the html block from the token.
        """
        _ = (current_token, previous_token)

        self.block_stack.append(current_token)
        return ""

    def __rehydrate_html_block_end(self, current_token, previous_token, next_token):
        """
        Rehydrate the end of the html block from the token.
        """
        return self.__rehydrate_indented_code_block_end(
            current_token, previous_token, next_token
        )

    def __rehydrate_fenced_code_block(self, current_token, previous_token):
        """
        Rehydrate the fenced code block from the token.
        """
        _ = previous_token

        self.block_stack.append(current_token)

        code_block_start_parts = [
            current_token.extracted_whitespace,
            ParserHelper.repeat_string(
                current_token.fence_character, current_token.fence_count
            ),
            current_token.extracted_whitespace_before_info_string,
            current_token.pre_extracted_text or current_token.extracted_text,
            current_token.pre_text_after_extracted_text
            or current_token.text_after_extracted_text,
            ParserHelper.newline_character,
        ]

        return "".join(code_block_start_parts)

    def __rehydrate_fenced_code_block_end(
        self, current_token, previous_token, next_token
    ):
        """
        Rehydrate the end of the fenced code block from the token.
        """
        del self.block_stack[-1]

        if not current_token.was_forced:
            # We need to do this as the ending fence may be longer than the opening fence.
            split_extra_data = current_token.extra_data.split(":")
            assert len(split_extra_data) >= 2
            fence_count = int(split_extra_data[1])

            fence_parts = [
                ""
                if previous_token.is_blank_line or previous_token.is_fenced_code_block
                else ParserHelper.newline_character,
                current_token.extracted_whitespace,
                ParserHelper.repeat_string(
                    current_token.start_markdown_token.fence_character, fence_count
                ),
                ParserHelper.newline_character,
            ]

            return "".join(fence_parts)

        return (
            ParserHelper.newline_character
            if next_token is not None and not previous_token.is_fenced_code_block
            else ""
        )

    def __search_backward_for_block_quote_start(self):
        token_stack_index = len(self.container_token_stack) - 2
        while (
            token_stack_index >= 0
            and self.container_token_stack[token_stack_index].is_block_quote_start
        ):
            token_stack_index -= 1
        print(f">token_stack_index>{token_stack_index}")
        print(
            f">token_stack_token-->{ParserHelper.make_value_visible(self.container_token_stack[token_stack_index])}"
        )
        return token_stack_index

    def __rehydrate_block_quote(
        self, current_token, previous_token, next_token, transformed_data
    ):
        _ = (previous_token, transformed_data)

        new_instance = copy.deepcopy(current_token)
        new_instance.leading_text_index = 0
        self.container_token_stack.append(new_instance)
        print(f">bquote>{ParserHelper.make_value_visible(new_instance)}")
        print(
            f">self.container_token_stack>{ParserHelper.make_value_visible(self.container_token_stack)}"
        )

        token_stack_index = self.__search_backward_for_block_quote_start()
        are_tokens_viable = (
            len(self.container_token_stack) > 1 and token_stack_index >= 0
        )
        print(f">are_tokens_viable>{are_tokens_viable}")
        if are_tokens_viable:
            matching_list_token = (
                self.container_token_stack[token_stack_index].last_new_list_token
                or self.container_token_stack[token_stack_index]
            )
            print(
                f">matching_list_token>{ParserHelper.make_value_visible(matching_list_token)}"
            )

            print(f">current_token.line_number>{current_token.line_number}")
            print(
                ">container_token_stack[token_stack_index].line_number>"
                + f"{self.container_token_stack[token_stack_index].line_number}"
            )

        if (
            are_tokens_viable
            and current_token.line_number == matching_list_token.line_number
        ):
            already_existing_whitespace = ParserHelper.repeat_string(
                " ", self.container_token_stack[token_stack_index].indent_level
            )
        else:
            already_existing_whitespace = None

        print(f">bquote>current_token>{ParserHelper.make_value_visible(current_token)}")
        print(f">bquote>next_token>{ParserHelper.make_value_visible(next_token)}")

        if (
            next_token
            and next_token.is_block_quote_start
            and current_token.line_number == next_token.line_number
        ):
            print(">bquote> will be done by following bquote>")
            selected_leading_sequence = ""
        else:
            selected_leading_sequence = new_instance.calculate_next_leading_space_part()
            print(f">bquote>selected_leading_sequence>{selected_leading_sequence}<")

        print(f">bquote>already_existing_whitespace>:{already_existing_whitespace}:<")
        print(f">bquote>selected_leading_sequence>:{selected_leading_sequence}:<")
        if already_existing_whitespace and selected_leading_sequence.startswith(
            already_existing_whitespace
        ):
            selected_leading_sequence = selected_leading_sequence[
                len(already_existing_whitespace) :
            ]
            print(f">bquote>new selected_leading_sequence>{selected_leading_sequence}<")
        return selected_leading_sequence

    def __look_backward_for_list_or_block_quote_start(self):
        token_stack_index = len(self.container_token_stack) - 1
        print(f"rls>>token_stack_index>>{token_stack_index}<<")
        while (
            token_stack_index >= 0
            and not self.container_token_stack[token_stack_index].is_list_start
            and not self.container_token_stack[token_stack_index].is_block_quote_start
        ):
            token_stack_index -= 1
        return token_stack_index

    def __rehydrate_list_start_previous_token(
        self, current_token, previous_token, next_token, extracted_whitespace
    ):
        previous_indent, post_adjust_whitespace, was_within_block_token = 0, None, False

        print(
            f"rlspt>>current_token>>{ParserHelper.make_value_visible(current_token)}<<"
        )
        print(
            f"rlspt>>previous_token>>{ParserHelper.make_value_visible(previous_token)}<<"
        )
        print(
            f"rlspt>>extracted_whitespace>>{ParserHelper.make_value_visible(extracted_whitespace)}<<"
        )

        print(
            f"rls>>self.container_token_stack>>{ParserHelper.make_value_visible(self.container_token_stack)}<<"
        )
        containing_block_quote_token = self.__look_for_last_block_token()
        print(
            "rls>>containing_block_quote_token>>"
            + f"{ParserHelper.make_value_visible(containing_block_quote_token)}<<"
        )
        if containing_block_quote_token:
            print(
                "rls>>containing_block_quote_token>>"
                + f"{ParserHelper.make_value_visible(containing_block_quote_token.leading_text_index)}<<"
            )

        token_stack_index = self.__look_backward_for_list_or_block_quote_start()
        print(f"rls>>token_stack_index2>>{token_stack_index}<<")

        containing_list_token, deeper_containing_block_quote_token = None, None
        if (
            token_stack_index >= 0
            and containing_block_quote_token
            != self.container_token_stack[token_stack_index]
        ):
            containing_list_token = self.container_token_stack[token_stack_index]
            deeper_containing_block_quote_token = containing_block_quote_token
            containing_block_quote_token = None

        did_container_start_midline = False
        had_weird_block_quote_in_list = False
        if previous_token.is_list_start:
            print("rlspt>>is_list_start")
            (
                previous_indent,
                extracted_whitespace,
            ) = self.__rehydrate_list_start_prev_list(current_token, previous_token)
        elif previous_token.is_block_quote_start:
            print("rlspt>>is_block_quote_start")
            (
                previous_indent,
                post_adjust_whitespace,
                extracted_whitespace,
            ) = self.__rehydrate_list_start_prev_block_quote(
                current_token,
                previous_token,
                containing_block_quote_token,
                extracted_whitespace,
            )
        elif containing_block_quote_token:
            print("rlspt>>containing_block_quote_token")
            (
                was_within_block_token,
                previous_indent,
            ) = self.__rehydrate_list_start_contained_in_block_quote(
                current_token, containing_block_quote_token
            )
        elif containing_list_token:
            print("rlspt>>containing_list_token")
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

        print(f"xx>>previous_indent:{previous_indent}:")
        print(f"xx>>extracted_whitespace:{extracted_whitespace}:")
        print(f"xx>>was_within_block_token:{was_within_block_token}:")
        print(f"xx>>post_adjust_whitespace:{post_adjust_whitespace}:")
        print(f"xx>>did_container_start_midline:{did_container_start_midline}:")
        return (
            previous_indent,
            extracted_whitespace,
            was_within_block_token,
            post_adjust_whitespace,
            did_container_start_midline,
            had_weird_block_quote_in_list,
        )

    @classmethod
    def __rehydrate_list_start_prev_list(cls, current_token, previous_token):
        _ = current_token
        return previous_token.indent_level, ""

    @classmethod
    def __rehydrate_list_start_prev_block_quote(
        cls,
        current_token,
        previous_token,
        containing_block_quote_token,
        extracted_whitespace,
    ):
        previous_indent = (
            len(previous_token.calculate_next_leading_space_part(increment_index=False))
            if ParserHelper.newline_character in previous_token.leading_spaces
            else len(previous_token.leading_spaces)
        )
        print(
            f"adj->current_token>>:{ParserHelper.make_value_visible(current_token)}:<<"
        )
        print(
            f"adj->containing_block_quote_token>>:{ParserHelper.make_value_visible(containing_block_quote_token)}:<<"
        )
        assert current_token.line_number == containing_block_quote_token.line_number
        split_leading_spaces = containing_block_quote_token.leading_spaces.split(
            ParserHelper.newline_character
        )
        block_quote_leading_space = split_leading_spaces[0]
        block_quote_leading_space_length = len(block_quote_leading_space)

        print(
            f"bq->len>>:{block_quote_leading_space}: {block_quote_leading_space_length}"
        )

        post_adjust_whitespace = "".ljust(
            current_token.column_number - block_quote_leading_space_length - 1, " "
        )
        extracted_whitespace = ""
        print(
            f"post_adjust_whitespace:{post_adjust_whitespace}: extracted_whitespace:{extracted_whitespace}:"
        )
        return previous_indent, post_adjust_whitespace, extracted_whitespace

    @classmethod
    def __rehydrate_list_start_contained_in_block_quote(
        cls, current_token, containing_block_quote_token
    ):
        block_quote_leading_space = (
            containing_block_quote_token.calculate_next_leading_space_part(
                increment_index=False, delta=-1
            )
        )
        previous_indent = len(block_quote_leading_space)
        print(f"adj->rls>>previous_indent>>:{previous_indent}:<<")
        print(f"adj->rls>>current_token.indent_level>>:{current_token.indent_level}:<<")

        return True, previous_indent

    @classmethod
    def __rehydrate_list_start_contained_in_list_spacingx(
        cls, containing_list_token, current_token, block_quote_leading_space_length
    ):
        previous_indent = containing_list_token.indent_level
        white_space_length = (
            len(current_token.extracted_whitespace) + block_quote_leading_space_length
        )
        print(f"adj->len(ws)>>:{white_space_length}:<<")
        extracted_whitespace = (
            "".ljust(white_space_length - previous_indent, " ")
            if white_space_length > previous_indent
            else ""
        )
        print(f"adj->previous_indent>>:{previous_indent}:<<")
        print(
            f"adj->extracted_whitespace>>:{ParserHelper.make_value_visible(extracted_whitespace)}:<<"
        )
        return previous_indent, extracted_whitespace

    # pylint: disable=too-many-locals
    @classmethod
    def __rehydrate_list_start_contained_in_list_deeper_block_quote(
        cls, previous_token, deeper_containing_block_quote_token, current_token
    ):
        starting_whitespace = ""
        did_container_start_midline = False
        check_list_for_indent = True
        if previous_token:
            print(f"previous_token:{ParserHelper.make_value_visible(previous_token)}:")
        if previous_token.is_end_token:
            print(
                f"previous_token.start_markdown_token:{previous_token.start_markdown_token}:"
            )
        if deeper_containing_block_quote_token:
            print(
                f"deeper_containing_block_quote_token:{ParserHelper.make_value_visible(deeper_containing_block_quote_token)}:"
            )
        do_perform_block_quote_ending = False
        had_weird_block_quote_in_list = False
        if (
            previous_token
            and previous_token.is_end_token
            and previous_token.start_markdown_token.is_block_quote_start
        ):
            had_weird_block_quote_in_list = True
            print(f"previous_token:{previous_token}:")
            print(
                f"previous_token.start_markdown_token:{previous_token.start_markdown_token}:"
            )
            print(
                f"previous_token.start_markdown_token.leading_spaces:{previous_token.start_markdown_token.leading_spaces}:"
            )
            newline_count = ParserHelper.count_characters_in_text(
                previous_token.start_markdown_token.leading_spaces, "\n"
            )
            previous_start_line = previous_token.start_markdown_token.line_number
            print(f"newline_count:{newline_count}:")
            print(f"previous_start_line:{previous_start_line}:")
            projected_start_line = previous_start_line + (newline_count + 1)
            print(f"projected_start_line:{projected_start_line}:")
            do_perform_block_quote_ending = (
                projected_start_line != current_token.line_number
            )
        if do_perform_block_quote_ending:
            split_leading_spaces = (
                previous_token.start_markdown_token.leading_spaces.split(
                    ParserHelper.newline_character
                )
            )
            print(f"split_leading_spaces>>{split_leading_spaces}")
            print(f"current_token>>{ParserHelper.make_value_visible(current_token)}")
            # if (
            #     current_token.is_new_list_item
            #     and len(split_leading_spaces) <= 2
            #     and False
            # ):
            #     block_quote_leading_space = ""
            #     starting_whitespace = ""
            # else:
            print(
                ">>"
                + ParserHelper.make_value_visible(previous_token.start_markdown_token)
            )
            block_quote_leading_space = split_leading_spaces[-1]
            starting_whitespace = block_quote_leading_space
            did_container_start_midline = True
            # up to here?
            check_list_for_indent = False
        else:
            print(
                "adj->deeper_containing_block_quote_token.line_number>>:"
                + f"{deeper_containing_block_quote_token.line_number}:<<"
            )
            print(f"adj->current_token.line_number>>:{current_token.line_number}:<<")
            line_number_delta = (
                current_token.line_number
                - deeper_containing_block_quote_token.line_number
            )
            print(f"index:{line_number_delta}")
            split_leading_spaces = (
                deeper_containing_block_quote_token.leading_spaces.split(
                    ParserHelper.newline_character
                )
            )
            print(
                "split_leading_spaces:"
                + ParserHelper.make_value_visible(split_leading_spaces)
            )
            block_quote_leading_space = split_leading_spaces[line_number_delta]
            if had_weird_block_quote_in_list:
                starting_whitespace = block_quote_leading_space
        print(
            "block_quote_leading_space:"
            + ParserHelper.make_value_visible(block_quote_leading_space)
            + ":"
        )
        block_quote_leading_space_length = len(block_quote_leading_space)
        print(f"starting_whitespace:{starting_whitespace}:")
        return (
            check_list_for_indent,
            starting_whitespace,
            did_container_start_midline,
            block_quote_leading_space_length,
            had_weird_block_quote_in_list,
        )

    # pylint: enable=too-many-locals

    # pylint: disable=too-many-arguments
    @classmethod
    def __calculate_post_adjust_whitespace(
        cls,
        starting_whitespace,
        containing_list_token,
        block_quote_leading_space_length,
        list_leading_space_length,
        list_start_content_length,
        add_extracted_whitespace_at_end,
        current_token,
    ):
        print(f"adj->starting_whitespace>>:{starting_whitespace}:<<")
        print(
            f"adj->containing_list_token.indent_level>>:{containing_list_token.indent_level}:<<"
        )
        print(
            f"adj->block_quote_leading_space_length>>:{block_quote_leading_space_length}:<<"
        )
        print(f"adj->list_leading_space_length>>:{list_leading_space_length}:<<")
        print(f"list_start_content_length:{list_start_content_length}:<<")

        pad_to_length = (
            containing_list_token.indent_level
            - block_quote_leading_space_length
            - list_leading_space_length
            - list_start_content_length
        )
        print(f"pad_to_length:{pad_to_length}:<<")
        print(f"adj->starting_whitespace>>:{starting_whitespace}:<<")
        post_adjust_whitespace = starting_whitespace.ljust(pad_to_length, " ")
        print(f"adj->post_adjust_whitespace>>:{post_adjust_whitespace}:<<")
        if add_extracted_whitespace_at_end:
            post_adjust_whitespace += current_token.extracted_whitespace
        print(f"adj->post_adjust_whitespace>>:{post_adjust_whitespace}:<<")
        return post_adjust_whitespace

    # pylint: enable=too-many-arguments

    # pylint: disable=too-many-arguments, too-many-locals
    @classmethod
    def __rehydrate_list_start_contained_in_list(
        cls,
        current_token,
        containing_list_token,
        deeper_containing_block_quote_token,
        extracted_whitespace,
        previous_token,
        next_token,
    ):

        print(
            f"adj->containing_list_token>>:{ParserHelper.make_value_visible(containing_list_token)}:<<"
        )
        print(
            "adj->deeper_containing_block_quote_token>>:"
            + f"{ParserHelper.make_value_visible(deeper_containing_block_quote_token)}:<<"
        )
        print(
            f"adj->extracted_whitespace>>:{ParserHelper.make_value_visible(extracted_whitespace)}:<<"
        )
        block_quote_leading_space_length = 0
        list_leading_space_length = 0
        starting_whitespace = ""
        did_container_start_midline = False
        check_list_for_indent = True
        had_weird_block_quote_in_list = False
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
            list_leading_space_length = previous_token.indent_level

        list_start_content_length = 0
        add_extracted_whitespace_at_end = False
        print(f"previous_token-->{ParserHelper.make_value_visible(previous_token)}")
        print(f"current_token-->{ParserHelper.make_value_visible(current_token)}")
        print(f"next_token-->{ParserHelper.make_value_visible(next_token)}")
        if (
            current_token.is_new_list_item
            and previous_token.is_end_token
            and previous_token.start_markdown_token.is_block_quote_start
        ):
            print(
                "previous_token.start_markdown_token-->"
                + f"{ParserHelper.make_value_visible(previous_token.start_markdown_token)}"
            )
            list_start_content_length = (
                len(containing_list_token.list_start_content)
                if containing_list_token.is_ordered_list_start
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
        print(f"adj->post_adjust_whitespace>>:{post_adjust_whitespace}:<<")
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
        current_token,
        next_token,
        extracted_whitespace,
        previous_indent,
        adjustment_since_newline,
        post_adjust_whitespace,
    ):
        start_sequence = (
            f"{extracted_whitespace}{current_token.list_start_sequence}"
            if current_token.is_unordered_list_start
            else f"{extracted_whitespace}{current_token.list_start_content}{current_token.list_start_sequence}"
        )
        print(f">>start_sequence>>:{start_sequence}:<<")
        if not next_token.is_blank_line:
            if next_token.is_list_end:
                print("list-end")
            else:
                print("not list-end and not blank-line")
                print(
                    f">>current_token>>:{ParserHelper.make_value_visible(current_token)}:<<"
                )
                print(f">>current_token.indent_level>>:{current_token.indent_level}:<<")
                print(f">>previous_indent>>:{previous_indent}:<<")
                print(f">>adjustment_since_newline>>:{adjustment_since_newline}:<<")
                requested_indent = (
                    current_token.indent_level
                    + len(extracted_whitespace)
                    - (current_token.column_number - 1)
                )
                print(f">>requested_indent>>:{requested_indent}:<<")
                start_sequence = start_sequence.ljust(requested_indent, " ")
        else:
            print("blank-line")
            print(f">>next_token.column_number>>:{next_token.column_number}:<<")
            print(f">>current_token.column_number>>:{current_token.column_number}:<<")
            list_content_length = 1
            if not current_token.is_unordered_list_start:
                list_content_length += len(current_token.list_start_content)
            new_column_number = (
                next_token.column_number
                - current_token.column_number
                - list_content_length
            )
            start_sequence += ParserHelper.repeat_string(" ", new_column_number)

        print(f"<<start_sequence<<:{start_sequence}:<<")
        if post_adjust_whitespace:
            print(f"<<post_adjust_whitespace<<(post):{post_adjust_whitespace}:<<")
            start_sequence = post_adjust_whitespace + start_sequence
            print(f"<<start_sequence<<(post):{start_sequence}:<<")
        return start_sequence

    # pylint: enable=too-many-arguments

    def __rehydrate_list_start(
        self, current_token, previous_token, next_token, transformed_data
    ):
        """
        Rehydrate the unordered list start token.
        """
        print(f">>current_token>>{ParserHelper.make_value_visible(current_token)}<<")
        extracted_whitespace = current_token.extracted_whitespace
        print(f">>extracted_whitespace>>{extracted_whitespace}<<")
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
                current_token, previous_token, next_token, extracted_whitespace
            )
            print(f">>extracted_whitespace>>{extracted_whitespace}<<")
            print(f">>post_adjust_whitespace>>{post_adjust_whitespace}<<")
        else:
            previous_indent, post_adjust_whitespace, was_within_block_token = (
                0,
                None,
                False,
            )

        print(f">>had_weird_block_quote_in_list>>{had_weird_block_quote_in_list}<<")
        self.container_token_stack.append(copy.deepcopy(current_token))

        print(f">>extracted_whitespace>>{extracted_whitespace}<<")
        print(
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
        print(f">>extracted_whitespace>>{extracted_whitespace}<<")

        return self.__rehydrate_list_start_calculate_start(
            current_token,
            next_token,
            extracted_whitespace,
            previous_indent,
            adjustment_since_newline,
            post_adjust_whitespace,
        )

    @classmethod
    def __adjust_whitespace_for_block_quote(
        cls, transformed_data, extracted_whitespace
    ):
        transformed_data_since_newline = transformed_data
        if ParserHelper.newline_character in transformed_data_since_newline:
            last_newline_index = transformed_data_since_newline.rindex(
                ParserHelper.newline_character
            )
            transformed_data_since_newline = transformed_data_since_newline[
                last_newline_index + 1 :
            ]
        adjustment_since_newline, transformed_data_since_newline_size = 0, len(
            transformed_data_since_newline
        )
        print(f">>transformed_data_since_newline>>:{transformed_data_since_newline}:<<")
        print(f">>adjustment_since_newline>>:{adjustment_since_newline}:<<")
        print(
            f">>transformed_data_since_newline_size>>:{transformed_data_since_newline_size}:<<"
        )
        print(f">>extracted_whitespace>>:{extracted_whitespace}:<<")
        if (
            extracted_whitespace
            and len(extracted_whitespace) >= transformed_data_since_newline_size
            and ">" in transformed_data_since_newline
        ):
            adjustment_since_newline = transformed_data_since_newline_size
            extracted_whitespace = extracted_whitespace[adjustment_since_newline:]
        print(f">>adjustment_since_newline>>:{adjustment_since_newline}:<<")
        print(f">>extracted_whitespace>>:{extracted_whitespace}:<<")
        return adjustment_since_newline, extracted_whitespace

    def __rehydrate_block_quote_end(self, current_token, actual_tokens, token_index):

        _ = current_token
        print(f">>{ParserHelper.make_value_visible(actual_tokens[token_index:])}")
        search_index = token_index + 1
        while (
            search_index < len(actual_tokens)
            and actual_tokens[search_index].is_container_end_token
        ):
            search_index += 1
        print(f">>{search_index}")
        any_non_container_end_tokens = search_index < len(actual_tokens)
        print(f">>{any_non_container_end_tokens}")

        del self.container_token_stack[-1]

        return ""

    def __rehydrate_list_start_end(self, current_token, actual_tokens, token_index):
        """
        Rehydrate the ordered list end token.
        """
        _ = actual_tokens, token_index
        del self.container_token_stack[-1]
        leading_spaces_index, expected_leading_spaces_index = (
            current_token.start_markdown_token.leading_spaces_index,
            ParserHelper.count_newlines_in_text(
                current_token.start_markdown_token.extracted_whitespace
            ),
        )

        assert leading_spaces_index == expected_leading_spaces_index, (
            f"leading_spaces_index={leading_spaces_index};"
            + f"expected_leading_spaces_index={len(expected_leading_spaces_index)}"
        )
        return ""

    def __recalc_adjustment_since_newline(self, adjustment_since_newline):
        if not adjustment_since_newline:
            print(
                f"rnli->container_token_stack>:{ParserHelper.make_value_visible(self.container_token_stack)}:"
            )
            stack_index = len(self.container_token_stack) - 1
            found_block_quote_token = None
            while stack_index >= 0:
                if self.container_token_stack[stack_index].is_block_quote_start:
                    found_block_quote_token = self.container_token_stack[stack_index]
                    break
                stack_index -= 1
            print(
                f"rnli->found_block_quote_token>:{ParserHelper.make_value_visible(found_block_quote_token)}:"
            )
            if found_block_quote_token:
                leading_space = (
                    found_block_quote_token.calculate_next_leading_space_part(
                        increment_index=False, delta=-1
                    )
                )
                print(f"rnli->leading_space>:{leading_space}:")
                adjustment_since_newline = len(leading_space)
        return adjustment_since_newline

    @classmethod
    def __rehydrate_next_list_item_blank_line(
        cls, start_sequence, current_token, next_token
    ):
        print(f">>next_token.column_number>>:{next_token.column_number}:<<")
        print(f">>current_token.column_number>>:{current_token.column_number}:<<")
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
        start_sequence,
        did_container_start_midline,
        adjustment_since_newline,
        had_weird_block_quote_in_list,
        next_token,
    ):
        print("__rehydrate_next_list_item_not_blank_line")
        print(f"start_sequence={start_sequence}=")
        print(f"did_container_start_midline={did_container_start_midline}=")
        print(f"adjustment_since_newline={adjustment_since_newline}=")
        if did_container_start_midline:
            print("did start midline")
            print(f"next_token:{ParserHelper.make_value_visible(next_token)}")
            project_indent_level = self.container_token_stack[-1].indent_level
            if next_token and next_token.is_block_quote_start:
                next_block_quote_leading_space = (
                    next_token.calculate_next_leading_space_part(increment_index=False)
                )
                print(
                    f"did start midline:next_block_quote_leading_space:{next_block_quote_leading_space}:"
                )
                ex_whitespace, _ = ParserHelper.extract_whitespace(
                    next_block_quote_leading_space, 0
                )
                print(f"did start midline:ab:{ex_whitespace}:")
                project_indent_level -= ex_whitespace
            start_sequence = start_sequence.ljust(project_indent_level, " ")
        else:
            print("did not start midline")
            calculated_indent = (
                self.container_token_stack[-1].indent_level - adjustment_since_newline
            )
            print(
                f"calculated_indent:{calculated_indent} = indent_level:{self.container_token_stack[-1].indent_level} - adjustment_since_newline:{adjustment_since_newline}"
            )
            print(f"had_weird_block_quote_in_list:{had_weird_block_quote_in_list}")
            if had_weird_block_quote_in_list:
                print(f"calculated_indent:{calculated_indent}")
                calculated_indent += 2
                print(f"calculated_indent:{calculated_indent}")
            print(
                f"rnli->calculated_indent={calculated_indent} = "
                + f"indent_level={self.container_token_stack[-1].indent_level} - "
                + f"adjustment_since_newline={adjustment_since_newline}"
            )
            print(f"start_sequence:{start_sequence}")
            start_sequence = start_sequence.ljust(calculated_indent, " ")

            # TODO This is a kludge.  The calc_indent is not properly computed.
            if not start_sequence.endswith(" "):
                start_sequence = f"{start_sequence} "
            print(f"start_sequence:{start_sequence}")
        return start_sequence

    # pylint: enable=too-many-arguments

    def __rehydrate_next_list_item(
        self, current_token, previous_token, next_token, transformed_data
    ):
        """
        Rehydrate the next list item token.
        """
        _ = previous_token

        assert self.container_token_stack[-1].is_list_start

        print("__rehydrate_next_list_item")
        self.container_token_stack[-1].adjust_for_new_list_item(current_token)

        (
            adjustment_since_newline,
            extracted_whitespace,
        ) = self.__adjust_whitespace_for_block_quote(
            transformed_data, current_token.extracted_whitespace
        )
        print(f"rnli->adjustment_since_newline>:{adjustment_since_newline}:")
        print(f"rnli->extracted_whitespace>:{extracted_whitespace}:")

        did_container_start_midline = False
        had_weird_block_quote_in_list = False
        if previous_token:
            (
                previous_indent,
                extracted_whitespace2,
                _,
                post_adjust_whitespace,
                did_container_start_midline,
                had_weird_block_quote_in_list,
            ) = self.__rehydrate_list_start_previous_token(
                current_token, previous_token, next_token, extracted_whitespace
            )
        else:
            previous_indent, post_adjust_whitespace = (0, None)
        print(f">>previous_indent>>{previous_indent}<<")
        print(f">>extracted_whitespace2>>{extracted_whitespace2}<<")
        print(f">>post_adjust_whitespace>>{post_adjust_whitespace}<<")
        print(f">>had_weird_block_quote_in_list>>{had_weird_block_quote_in_list}<<")

        adjustment_since_newline = self.__recalc_adjustment_since_newline(
            adjustment_since_newline
        )
        # assert len(post_adjust_whitespace) == adjustment_since_newline

        whitespace_to_use = (
            post_adjust_whitespace
            if did_container_start_midline or had_weird_block_quote_in_list
            else extracted_whitespace
        )

        print(f"rnli->whitespace_to_use>:{whitespace_to_use}:")
        print(f"rnli->adjustment_since_newline>:{adjustment_since_newline}:")
        print(f"rnli->extracted_whitespace>:{extracted_whitespace}:")
        start_sequence = (
            f"{whitespace_to_use}{current_token.list_start_content}"
            + f"{self.container_token_stack[-1].list_start_sequence}"
        )

        print(f"rnli->start_sequence>:{start_sequence}:")
        if next_token.is_blank_line:
            start_sequence = self.__rehydrate_next_list_item_blank_line(
                start_sequence, current_token, next_token
            )
        else:
            start_sequence = self.__rehydrate_next_list_item_not_blank_line(
                start_sequence,
                did_container_start_midline,
                adjustment_since_newline,
                had_weird_block_quote_in_list,
                next_token,
            )
        print(f"rnli->start_sequence>:{start_sequence}:")

        return start_sequence

    def __insert_leading_whitespace_at_newlines(self, text_to_modify):
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

            print(f"text>before>{ParserHelper.make_value_visible(text_to_modify)}")
            text_to_modify = ParserHelper.remove_all_from_text(text_to_modify)
            print(f"text>after>{ParserHelper.make_value_visible(text_to_modify)}")

            if owning_paragraph_token:
                (
                    text_to_modify,
                    owning_paragraph_token.rehydrate_index,
                ) = ParserHelper.recombine_string_with_whitespace(
                    text_to_modify,
                    owning_paragraph_token.extracted_whitespace,
                    owning_paragraph_token.rehydrate_index,
                    post_increment_index=False,
                )
        return text_to_modify

    def __rehydrate_inline_image(self, current_token, previous_token):
        """
        Rehydrate the image text from the token.
        """
        _ = previous_token

        if self.block_stack[-1].is_inline_link:
            return ""
        print(f">>>>>>>>:{ParserHelper.make_value_visible(current_token)}:<<<<<")
        rehydrated_text = LinkHelper.rehydrate_inline_image_text_from_token(
            current_token
        )
        print(f">>>>>>>>:{ParserHelper.make_value_visible(rehydrated_text)}:<<<<<")
        return self.__insert_leading_whitespace_at_newlines(rehydrated_text)

    def __rehydrate_inline_link(self, current_token, previous_token):
        """
        Rehydrate the start of the link from the token.
        """
        _ = previous_token

        self.block_stack.append(current_token)
        rehydrated_text = LinkHelper.rehydrate_inline_link_text_from_token(
            current_token
        )
        return self.__insert_leading_whitespace_at_newlines(rehydrated_text)

    def __rehydrate_inline_link_end(self, current_token, previous_token, next_token):
        """
        Rehydrate the end of the link from the token.
        """
        return self.__rehydrate_indented_code_block_end(
            current_token, previous_token, next_token
        )

    @classmethod
    def __rehydrate_link_reference_definition(cls, current_token, previous_token):
        """
        Rehydrate the link reference definition from the token.
        """
        _ = previous_token

        link_def_parts = [
            current_token.extracted_whitespace,
            "[",
            current_token.link_name_debug or current_token.link_name,
            "]:",
            current_token.link_destination_whitespace,
            current_token.link_destination_raw or current_token.link_destination,
            current_token.link_title_whitespace,
            current_token.link_title_raw or current_token.link_title,
            current_token.end_whitespace,
            ParserHelper.newline_character,
        ]

        return "".join(link_def_parts)

    def __rehydrate_atx_heading(self, current_token, previous_token):
        """
        Rehydrate the atx heading block from the token.
        """
        _ = previous_token

        self.block_stack.append(current_token)
        return f'{current_token.extracted_whitespace}{ParserHelper.repeat_string("#", current_token.hash_count)}'

    def __rehydrate_atx_heading_end(self, current_token, previous_token, next_token):
        """
        Rehydrate the end of the atx heading block from the token.
        """
        _ = (previous_token, next_token)

        del self.block_stack[-1]
        return "".join(
            [
                current_token.extra_end_data,
                ParserHelper.repeat_string(
                    "#", current_token.start_markdown_token.remove_trailing_count
                )
                if current_token.start_markdown_token.remove_trailing_count
                else "",
                current_token.extracted_whitespace,
                ParserHelper.newline_character,
            ]
        )

    def __rehydrate_setext_heading(self, current_token, previous_token):
        """
        Rehydrate the setext heading from the token.
        """
        _ = previous_token

        self.block_stack.append(current_token)
        return current_token.extracted_whitespace

    def __rehydrate_setext_heading_end(self, current_token, previous_token, next_token):
        """
        Rehydrate the end of the setext heading block from the token.
        """
        _ = (previous_token, next_token)

        heading_character = self.block_stack[-1].heading_character
        heading_character_count = self.block_stack[-1].heading_character_count
        final_whitespace = self.block_stack[-1].final_whitespace
        del self.block_stack[-1]
        return "".join(
            [
                final_whitespace,
                ParserHelper.newline_character,
                current_token.extracted_whitespace,
                ParserHelper.repeat_string(heading_character, heading_character_count),
                current_token.extra_end_data,
                ParserHelper.newline_character,
            ]
        )

    def __rehydrate_text(self, current_token, previous_token):
        """
        Rehydrate the text from the token.
        """
        _ = previous_token

        if self.block_stack[-1].is_inline_link or self.block_stack[-1].is_inline_image:
            return ""

        prefix_text = ""
        print(
            f">>rehydrate_text>>:{ParserHelper.make_value_visible(current_token.token_text)}:<<"
        )
        # main_text = ParserHelper.resolve_noops_from_text(current_token.token_text)
        main_text = ParserHelper.remove_all_from_text(
            current_token.token_text, include_noops=True
        )

        print(f"<<rehydrate_text>>{ParserHelper.make_value_visible(main_text)}")

        print(
            f">>leading_whitespace>>:{ParserHelper.make_value_visible(current_token.extracted_whitespace)}:<<"
        )
        leading_whitespace = ParserHelper.remove_all_from_text(
            current_token.extracted_whitespace
        )
        print(
            f"<<leading_whitespace>>:{ParserHelper.make_value_visible(leading_whitespace)}:<<"
        )

        extra_line = ""
        if self.block_stack:
            if self.block_stack[-1].is_indented_code_block:
                (
                    main_text,
                    prefix_text,
                    leading_whitespace,
                ) = self.__reconstitute_indented_text(
                    main_text,
                    self.block_stack[-1].extracted_whitespace,
                    self.block_stack[-1].indented_whitespace,
                    leading_whitespace,
                )
            elif self.block_stack[-1].is_html_block:
                extra_line = ParserHelper.newline_character
            elif self.block_stack[-1].is_paragraph:
                main_text = self.__reconstitute_paragraph_text(main_text, current_token)
            elif self.block_stack[-1].is_setext_heading:
                main_text = self.__reconstitute_setext_text(main_text, current_token)

        print(
            f"<<prefix_text>>{ParserHelper.make_value_visible(prefix_text)}"
            + f"<<leading_whitespace>>{ParserHelper.make_value_visible(leading_whitespace)}"
            + f"<<main_text>>{ParserHelper.make_value_visible(main_text)}<<"
        )
        return "".join([prefix_text, leading_whitespace, main_text, extra_line])

    def __rehydrate_hard_break(self, current_token, previous_token):
        """
        Rehydrate the hard break text from the token.
        """
        _ = previous_token

        leading_whitespace = f"{current_token.line_end}{ParserHelper.newline_character}"
        if self.block_stack[-1].is_paragraph:
            (
                leading_whitespace,
                self.block_stack[-1].rehydrate_index,
            ) = ParserHelper.recombine_string_with_whitespace(
                leading_whitespace,
                self.block_stack[-1].extracted_whitespace,
                self.block_stack[-1].rehydrate_index,
            )

        return "" if self.block_stack[-1].is_inline_link else leading_whitespace

    def __rehydrate_inline_emphaisis(self, current_token, previous_token):
        """
        Rehydrate the emphasis text from the token.
        """
        _ = previous_token

        return (
            ""
            if self.block_stack[-1].is_inline_link
            else ParserHelper.repeat_string(
                current_token.emphasis_character, current_token.emphasis_length
            )
        )

    def __rehydrate_inline_emphaisis_end(
        self, current_token, previous_token, next_token
    ):
        """
        Rehydrate the emphasis end text from the token.
        """
        _ = (previous_token, next_token)

        return (
            ""
            if self.block_stack[-1].is_inline_link
            else ParserHelper.repeat_string(
                current_token.start_markdown_token.emphasis_character,
                current_token.start_markdown_token.emphasis_length,
            )
        )

    def __rehydrate_inline_uri_autolink(self, current_token, previous_token):
        """
        Rehydrate the uri autolink from the token.
        """
        _ = previous_token

        return (
            ""
            if self.block_stack[-1].is_inline_link
            else f"<{current_token.autolink_text}>"
        )

    def __rehydrate_inline_email_autolink(self, current_token, previous_token):
        """
        Rehydrate the email autolink from the token.
        """
        _ = previous_token

        return (
            ""
            if self.block_stack[-1].is_inline_link
            else f"<{current_token.autolink_text}>"
        )

    def __rehydrate_inline_raw_html(self, current_token, previous_token):
        """
        Rehydrate the email raw html from the token.
        """
        _ = previous_token

        if self.block_stack[-1].is_inline_link:
            return ""

        raw_text = ParserHelper.remove_all_from_text(current_token.raw_tag)

        if self.block_stack[-1].is_paragraph:
            print(f"raw_html>>before>>{ParserHelper.make_value_visible(raw_text)}")
            self.block_stack[-1].rehydrate_index += ParserHelper.count_newlines_in_text(
                raw_text
            )
            print(f"raw_html>>after>>{ParserHelper.make_value_visible(raw_text)}")
        return f"<{raw_text}>"

    def __rehydrate_inline_code_span(self, current_token, previous_token):
        """
        Rehydrate the code span data from the token.
        """
        _ = previous_token

        if self.block_stack[-1].is_inline_link:
            return ""

        span_text = ParserHelper.remove_all_from_text(current_token.span_text)
        leading_whitespace = ParserHelper.remove_all_from_text(
            current_token.leading_whitespace
        )
        trailing_whitespace = ParserHelper.remove_all_from_text(
            current_token.trailing_whitespace
        )

        if self.block_stack[-1].is_paragraph:
            (
                leading_whitespace,
                self.block_stack[-1].rehydrate_index,
            ) = ParserHelper.recombine_string_with_whitespace(
                leading_whitespace,
                self.block_stack[-1].extracted_whitespace,
                self.block_stack[-1].rehydrate_index,
            )
            (
                span_text,
                self.block_stack[-1].rehydrate_index,
            ) = ParserHelper.recombine_string_with_whitespace(
                span_text,
                self.block_stack[-1].extracted_whitespace,
                self.block_stack[-1].rehydrate_index,
            )
            (
                trailing_whitespace,
                self.block_stack[-1].rehydrate_index,
            ) = ParserHelper.recombine_string_with_whitespace(
                trailing_whitespace,
                self.block_stack[-1].extracted_whitespace,
                self.block_stack[-1].rehydrate_index,
            )

        return "".join(
            [
                current_token.extracted_start_backticks,
                leading_whitespace,
                span_text,
                trailing_whitespace,
                current_token.extracted_start_backticks,
            ]
        )

    @classmethod
    def __rehydrate_thematic_break(cls, current_token, previous_token):
        """
        Rehydrate the thematic break text from the token.
        """
        _ = previous_token

        return "".join(
            [
                current_token.extracted_whitespace,
                current_token.rest_of_line,
                ParserHelper.newline_character,
            ]
        )

    def __reconstitute_paragraph_text(self, main_text, current_token):
        """
        For a paragraph block, figure out the text that got us here.
        """
        if ParserHelper.newline_character in main_text:
            (
                main_text,
                self.block_stack[-1].rehydrate_index,
            ) = ParserHelper.recombine_string_with_whitespace(
                main_text,
                self.block_stack[-1].extracted_whitespace,
                self.block_stack[-1].rehydrate_index,
            )
            if current_token.end_whitespace:
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
        cls, main_text, prefix_text, indented_whitespace, leading_whitespace
    ):
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
        text_part_index,
        text_part_value,
        rejoined_token_text,
        split_parent_whitespace_text,
    ):
        ws_prefix_text = ""
        ws_suffix_text = ""
        if split_parent_whitespace_text[text_part_index]:
            split_setext_text = split_parent_whitespace_text[text_part_index].split(
                ParserHelper.whitespace_split_character
            )
            split_setext_text_size = len(split_setext_text)
            if split_setext_text_size == 1:
                if text_part_index == 0:
                    ws_suffix_text = split_setext_text[0]
                else:
                    ws_prefix_text = split_setext_text[0]
            else:
                assert split_setext_text_size == 2
                ws_prefix_text = split_setext_text[0]
                ws_suffix_text = split_setext_text[1]

        rejoined_token_text.append(
            "".join([ws_prefix_text, text_part_value, ws_suffix_text])
        )

    @classmethod
    def __reconstitute_setext_text(cls, main_text, current_token):
        """
        For a setext heading block, figure out the text that got us here.

        Because of the unique formatting of the setext data, the recombine_string_with_whitespace
        function cannot be used for this.
        """

        if ParserHelper.newline_character in main_text:
            split_token_text = main_text.split(ParserHelper.newline_character)
            split_parent_whitespace_text = current_token.end_whitespace.split(
                ParserHelper.newline_character
            )

            rejoined_token_text = []
            for text_part_index, text_part_value in enumerate(split_token_text):
                cls.__reconstitute_setext_text_item(
                    text_part_index,
                    text_part_value,
                    rejoined_token_text,
                    split_parent_whitespace_text,
                )

            main_text = ParserHelper.newline_character.join(rejoined_token_text)
        else:
            print(f"main_text>>{ParserHelper.make_value_visible(main_text)}")
            print(f"current_token>>{ParserHelper.make_value_visible(current_token)}")
            if current_token.end_whitespace and current_token.end_whitespace.endswith(
                ParserHelper.whitespace_split_character
            ):
                main_text = f"{current_token.end_whitespace[:-1]}{main_text}"
        return main_text
