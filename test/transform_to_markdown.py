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
from pymarkdown.extensions.front_matter_markdown_token import (
    FrontMatterExtension,
    FrontMatterMarkdownToken,
)
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

    def __transform_container_end(
        self, container_stack, container_records, current_token, transformed_data
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
                container_text, container_records
            )
            print("pre>:" + str(pre_container_text) + ":<")
            print("adj>:" + str(adjusted_text) + ":<")
            transformed_data = pre_container_text + adjusted_text
            print("trn>:" + str(transformed_data) + ":<")
        return transformed_data

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

            (new_data, pragma_token,) = self.__process_next_token(
                current_token,
                previous_token,
                next_token,
                transformed_data,
                actual_tokens,
                token_index,
            )

            print(f"post-h>new_data>{ParserHelper.make_value_visible(new_data)}")
            transformed_data_length_before_add = len(transformed_data)
            transformed_data += new_data

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
                    container_stack, container_records, current_token, transformed_data
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

        print("(" + str(container_text_index) + ")")
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
        while old_record_index != record_index:
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
                print("   -->" + ParserHelper.make_value_visible(token_stack))
                print(
                    "   -->" + ParserHelper.make_value_visible(container_token_indices)
                )
                assert str(current_changed_record[2]) == str(token_stack[-1]), (
                    "end:"
                    + ParserHelper.make_value_visible(current_changed_record[2])
                    + "!="
                    + ParserHelper.make_value_visible(token_stack[-1])
                )
                del token_stack[-1]
                del container_token_indices[-1]

            print(
                "   -->current_changed_record>"
                + ParserHelper.make_value_visible(current_changed_record)
            )
            print("   -->" + ParserHelper.make_value_visible(token_stack))
            print("   -->" + ParserHelper.make_value_visible(container_token_indices))
            old_record_index += 1
        return record_index, did_move_ahead, current_changed_record

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
        print(" -->" + ParserHelper.make_value_visible(token_stack))
        print(" -->" + ParserHelper.make_value_visible(container_token_indices))
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
        print(" -->" + ParserHelper.make_value_visible(token_stack))
        print(" -->" + ParserHelper.make_value_visible(container_token_indices))

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
    ):
        print(" -->did_move_ahead>" + ParserHelper.make_value_visible(did_move_ahead))
        print(" -->" + ParserHelper.make_value_visible(token_stack))
        print(" -->" + ParserHelper.make_value_visible(container_token_indices))
        print(" -->did_move_ahead>" + ParserHelper.make_value_visible(did_move_ahead))
        print(
            " -->current_changed_record>"
            + ParserHelper.make_value_visible(current_changed_record)
        )
        last_container_token_index = container_token_indices[-1]

        applied_leading_spaces_to_start_of_container_line = not (
            did_move_ahead and current_changed_record[0]
        )
        if applied_leading_spaces_to_start_of_container_line:
            print(" container->" + ParserHelper.make_value_visible(token_stack[-1]))
            split_leading_spaces = token_stack[-1].leading_spaces.split(
                ParserHelper.newline_character
            )
            if last_container_token_index < len(split_leading_spaces):
                print(" -->" + ParserHelper.make_value_visible(split_leading_spaces))
                print(
                    " -->container_line>"
                    + ParserHelper.make_value_visible(container_line)
                )
                container_line = (
                    split_leading_spaces[last_container_token_index] + container_line
                )
                print(
                    " -->container_line>"
                    + ParserHelper.make_value_visible(container_line)
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
    def __adjust_for_list(
        cls,
        token_stack,
        applied_leading_spaces_to_start_of_container_line,
        container_token_indices,
        container_line,
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
                previous_token = token_stack[nested_block_start_index]
                print(
                    " nested_block_start_index->"
                    + str(nested_block_start_index)
                    + ":previous_token="
                    + ParserHelper.make_value_visible(previous_token)
                )
                print(
                    " token_stack[-1]="
                    + ParserHelper.make_value_visible(token_stack[-1])
                )
                print(
                    " applied_leading_spaces_to_start_of_container_line->"
                    + str(applied_leading_spaces_to_start_of_container_line)
                )
                inner_token_index = container_token_indices[nested_block_start_index]
                if (
                    applied_leading_spaces_to_start_of_container_line
                    or token_stack[-1].line_number != previous_token.line_number
                ):
                    split_leading_spaces = previous_token.leading_spaces.split(
                        ParserHelper.newline_character
                    )
                    if inner_token_index < len(split_leading_spaces):
                        print(
                            " -->container_line>"
                            + ParserHelper.make_value_visible(container_line)
                        )
                        container_line = (
                            split_leading_spaces[inner_token_index] + container_line
                        )
                        print(
                            " -->container_line>"
                            + ParserHelper.make_value_visible(container_line)
                        )
                container_token_indices[nested_block_start_index] = (
                    inner_token_index + 1
                )
        return container_line

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
    def __adjust_for_block_quote(
        cls, token_stack, container_line, container_token_indices, line_number
    ):

        if not (len(token_stack) > 1 and token_stack[-1].is_block_quote_start):
            return container_line

        print(" looking for nested list start")
        nested_list_start_index = TransformToMarkdown.__get_last_list_index(token_stack)
        print(" afbq=" + str(len(token_stack) - 1))
        print(" nested_list_start_index=" + str(nested_list_start_index))
        if nested_list_start_index == -1:
            print(" nope")
        elif (
            nested_list_start_index == len(token_stack) - 2
            and nested_list_start_index > 0
            and token_stack[-1].line_number == line_number
            and token_stack[nested_list_start_index - 1].is_block_quote_start
            and token_stack[-1].line_number != token_stack[-2].line_number
        ):

            adj_line = ""
            print("adj_line->:" + adj_line + ":")
            adj_line = cls.__adjust(
                nested_list_start_index - 1,
                token_stack,
                container_token_indices,
                adj_line,
                True,
            )
            print("adj_line->:" + adj_line + ":")
            adj_line = cls.__adjust(
                nested_list_start_index,
                token_stack,
                container_token_indices,
                adj_line,
                True,
            )
            print("adj_line->:" + adj_line + ":")
            container_line = adj_line + container_line
        else:
            previous_token = token_stack[nested_list_start_index]
            print(" yes->" + ParserHelper.make_value_visible(previous_token))
            print("token_stack[-1].line_number->" + str(token_stack[-1].line_number))
            print("previous_token.line_number->" + str(previous_token.line_number))
            print("line_number->" + str(line_number))
            if (
                token_stack[-1].line_number != previous_token.line_number
                or line_number != previous_token.line_number
            ):
                container_line = cls.__adjust(
                    nested_list_start_index,
                    token_stack,
                    container_token_indices,
                    container_line,
                    False,
                )
        return container_line

    # pylint: disable=too-many-arguments, unused-private-member
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
            print("delta->" + str(delta))
            container_line += ParserHelper.repeat_string(" ", delta)
        split_leading_spaces = previous_token.leading_spaces.split(
            ParserHelper.newline_character
        )
        inner_token_index = container_token_indices[nested_list_start_index]
        if inner_token_index < len(split_leading_spaces):
            print(
                "inner_index->" + str(container_token_indices[nested_list_start_index])
            )
            container_line = split_leading_spaces[inner_token_index] + container_line
            container_token_indices[nested_list_start_index] = inner_token_index + 1
            print(
                "inner_index->" + str(container_token_indices[nested_list_start_index])
            )
        return container_line

    # pylint: enable=too-many-arguments, unused-private-member

    # pylint: disable=too-many-locals
    def __apply_container_transformation(self, container_text, container_records):
        print(">>incoming>>:" + ParserHelper.make_value_visible(container_text) + ":<<")
        print(
            ">>container_records>>" + ParserHelper.make_value_visible(container_records)
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
            )

            container_line = self.__adjust_for_list(
                token_stack,
                applied_leading_spaces_to_start_of_container_line,
                container_token_indices,
                container_line,
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
        found_block_token = None
        for i in range(len(self.container_token_stack) - 1, -1, -1):
            if self.container_token_stack[i].is_block_quote_start:
                found_block_token = self.container_token_stack[i]
                break
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
        if len(self.container_token_stack) > 1 and (
            token_stack_index >= 0
            and current_token.line_number
            == self.container_token_stack[token_stack_index].line_number
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

        if already_existing_whitespace and selected_leading_sequence.startswith(
            already_existing_whitespace
        ):
            selected_leading_sequence = selected_leading_sequence[
                len(already_existing_whitespace) :
            ]
        return selected_leading_sequence

    def __rehydrate_list_start_previous_token(
        self, current_token, previous_token, extracted_whitespace
    ):
        previous_indent, post_adjust_whitespace, was_within_block_token = 0, None, False

        print(
            f"rls>>previous_token>>{ParserHelper.make_value_visible(previous_token)}<<"
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

        token_stack_index = len(self.container_token_stack) - 1
        print(f"rls>>token_stack_index>>{token_stack_index}<<")
        while token_stack_index >= 0:
            if (
                self.container_token_stack[token_stack_index].is_list_start
                or self.container_token_stack[token_stack_index].is_block_quote_start
            ):
                break
            token_stack_index -= 1

        containing_list_token, deeper_containing_block_quote_token = None, None
        if (
            token_stack_index >= 0
            and containing_block_quote_token
            != self.container_token_stack[token_stack_index]
        ):
            containing_list_token = self.container_token_stack[token_stack_index]
            deeper_containing_block_quote_token = containing_block_quote_token
            containing_block_quote_token = None

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
            ) = self.__rehydrate_list_start_contained_in_list(
                current_token,
                containing_list_token,
                deeper_containing_block_quote_token,
                extracted_whitespace,
            )
        return (
            previous_indent,
            extracted_whitespace,
            was_within_block_token,
            post_adjust_whitespace,
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
    def __rehydrate_list_start_contained_in_list(
        cls,
        current_token,
        containing_list_token,
        deeper_containing_block_quote_token,
        extracted_whitespace,
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
        if deeper_containing_block_quote_token:
            print(
                "adj->deeper_containing_block_quote_token.line_number>>:"
                + f"{deeper_containing_block_quote_token.line_number}:<<"
            )
            print(
                "adj->current_token.line_number>>:" + f"{current_token.line_number}:<<"
            )
            line_number_delta = (
                current_token.line_number
                - deeper_containing_block_quote_token.line_number
            )
            print("index:" + str(line_number_delta))
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
            print(
                "block_quote_leading_space:"
                + ParserHelper.make_value_visible(block_quote_leading_space)
            )

            block_quote_leading_space_length = len(block_quote_leading_space)
        print(
            f"adj->block_quote_leading_space_length>>:{block_quote_leading_space_length}:<<"
        )
        post_adjust_whitespace = "".ljust(
            containing_list_token.indent_level - block_quote_leading_space_length, " "
        )

        previous_indent = containing_list_token.indent_level
        white_space_length = (
            len(current_token.extracted_whitespace) + block_quote_leading_space_length
        )
        print(f"adj->len(ws)>>:{white_space_length}:<<")
        # assert len(current_token.extracted_whitespace) == previous_indent
        extracted_whitespace = (
            "".ljust(white_space_length - previous_indent, " ")
            if white_space_length > previous_indent
            else ""
        )
        print(f"adj->previous_indent>>:{previous_indent}:<<")
        print(
            f"adj->extracted_whitespace>>:{ParserHelper.make_value_visible(extracted_whitespace)}:<<"
        )
        print(f"adj->post_adjust_whitespace>>:{post_adjust_whitespace}:<<")
        return previous_indent, extracted_whitespace, post_adjust_whitespace

    def __rehydrate_list_start(
        self, current_token, previous_token, next_token, transformed_data
    ):
        """
        Rehydrate the unordered list start token.
        """
        print(f">>current_token>>{ParserHelper.make_value_visible(current_token)}<<")
        extracted_whitespace = current_token.extracted_whitespace
        print(f">>extracted_whitespace>>{extracted_whitespace}<<")
        if previous_token:
            (
                previous_indent,
                extracted_whitespace,
                was_within_block_token,
                post_adjust_whitespace,
            ) = self.__rehydrate_list_start_previous_token(
                current_token, previous_token, extracted_whitespace
            )
            print(f">>extracted_whitespace>>{extracted_whitespace}<<")
        else:
            previous_indent, post_adjust_whitespace, was_within_block_token = (
                0,
                None,
                False,
            )

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

        start_sequence = (
            f"{extracted_whitespace}{current_token.list_start_sequence}"
            if current_token.is_unordered_list_start
            else f"{extracted_whitespace}{current_token.list_start_content}{current_token.list_start_sequence}"
        )
        print(f">>start_sequence>>:{start_sequence}:<<")
        if not next_token.is_blank_line:
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

        if previous_token:
            (
                previous_indent,
                extracted_whitespace2,
                _,
                post_adjust_whitespace,
            ) = self.__rehydrate_list_start_previous_token(
                current_token, previous_token, extracted_whitespace
            )
        else:
            previous_indent, post_adjust_whitespace = (0, None)
        print(f">>previous_indent>>{previous_indent}<<")
        print(f">>extracted_whitespace2>>{extracted_whitespace2}<<")
        print(f">>post_adjust_whitespace>>{post_adjust_whitespace}<<")

        adjustment_since_newline = self.__recalc_adjustment_since_newline(
            adjustment_since_newline
        )

        print(f"rnli->adjustment_since_newline>:{adjustment_since_newline}:")
        print(f"rnli->extracted_whitespace>:{extracted_whitespace}:")
        start_sequence = (
            f"{extracted_whitespace}{current_token.list_start_content}"
            + f"{self.container_token_stack[-1].list_start_sequence}"
        )
        # start_sequence = (
        #     f"{extracted_whitespace2}{self.container_token_stack[-1].list_start_sequence}"
        #     if current_token.is_unordered_list_start
        #     else f"{extracted_whitespace2}{current_token.list_start_content}" + \
        #           f"{self.container_token_stack[-1].list_start_sequence}"
        # )

        print(f"rnli->start_sequence>:{start_sequence}:")
        if not next_token.is_blank_line:
            start_sequence = start_sequence.ljust(
                self.container_token_stack[-1].indent_level - adjustment_since_newline,
                " ",
            )
            # start_sequence = start_sequence.ljust(
            #     current_token.indent_level - previous_indent - adjustment_since_newline,
            #     " ",
            # )
        else:
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
        print(f"rnli->start_sequence>:{start_sequence}:")

        return start_sequence

    def __insert_leading_whitespace_at_newlines(self, text_to_modify):
        """
        Deal with re-inserting any removed whitespace at the starts of lines.
        """
        if ParserHelper.newline_character in text_to_modify:
            owning_paragraph_token = None
            for search_index in range(len(self.block_stack) - 1, -1, -1):
                if self.block_stack[search_index].is_paragraph:
                    owning_paragraph_token = self.block_stack[search_index]
                    break

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
            f">>rehydrate_text>>{ParserHelper.make_value_visible(current_token.token_text)}"
        )
        # main_text = ParserHelper.resolve_noops_from_text(current_token.token_text)
        main_text = ParserHelper.remove_all_from_text(
            current_token.token_text, include_noops=True
        )

        print(f"<<rehydrate_text>>{ParserHelper.make_value_visible(main_text)}")

        print(
            f">>leading_whitespace>>{ParserHelper.make_value_visible(current_token.extracted_whitespace)}"
        )
        leading_whitespace = ParserHelper.remove_all_from_text(
            current_token.extracted_whitespace
        )
        print(
            f"<<leading_whitespace>>{ParserHelper.make_value_visible(leading_whitespace)}"
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

    # pylint: disable=unused-private-member
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

    # pylint: enable=unused-private-member

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
