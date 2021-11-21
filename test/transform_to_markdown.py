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

    def transform(self, actual_tokens):  # noqa: C901
        """
        Transform the incoming token stream back into Markdown.
        """
        (
            transformed_data,
            avoid_processing,
            previous_token,
            continue_sequence,
            delayed_continue,
        ) = ("", False, None, "", "")

        print("---\nTransformToMarkdown\n---")

        pragma_token = None

        for token_index, current_token in enumerate(actual_tokens):
            next_token = self.__handle_pre_processing(
                current_token,
                transformed_data,
                actual_tokens,
                token_index,
                continue_sequence,
                delayed_continue,
            )

            (
                new_data,
                continue_sequence,
                delayed_continue,
                skip_merge,
                pragma_token,
            ) = self.__process_next_token(
                current_token,
                previous_token,
                next_token,
                transformed_data,
                actual_tokens,
                token_index,
                continue_sequence,
                delayed_continue,
            )

            print(
                f"post-h>new_data>{ParserHelper.make_value_visible(new_data)}"
                + f"<continue_sequence>{continue_sequence}<delayed_continue>{delayed_continue}<"
            )

            (
                new_data,
                delayed_continue,
                continue_sequence,
                transformed_data,
            ) = self.__handle_post_processing(
                current_token,
                new_data,
                skip_merge,
                delayed_continue,
                continue_sequence,
                next_token,
                previous_token,
                actual_tokens,
                transformed_data,
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
        return transformed_data, avoid_processing

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

    # pylint: disable=too-many-arguments
    def __handle_pre_processing(
        self,
        current_token,
        transformed_data,
        actual_tokens,
        token_index,
        continue_sequence,
        delayed_continue,
    ):
        print(
            f"\n\n>>>>{ParserHelper.make_value_visible(current_token)}"
            + f"-->{ParserHelper.make_value_visible(transformed_data)}<--"
        )
        self.__look_for_last_block_token()

        next_token = (
            actual_tokens[token_index + 1]
            if token_index < len(actual_tokens) - 1
            else None
        )

        print(
            f"pre-h>continue_sequence>{continue_sequence}<delayed_continue>{delayed_continue}<"
        )

        return next_token

    # pylint: enable=too-many-arguments

    # pylint: disable=too-many-arguments
    def __handle_post_processing(
        self,
        current_token,
        new_data,
        skip_merge,
        delayed_continue,
        continue_sequence,
        next_token,
        previous_token,
        actual_tokens,
        transformed_data,
    ):
        self.__look_for_last_block_token()
        (
            new_data,
            delayed_continue,
            continue_sequence,
        ) = self.__perform_container_post_processing(
            current_token,
            new_data,
            skip_merge,
            delayed_continue,
            continue_sequence,
            next_token,
            previous_token,
            actual_tokens,
            transformed_data,
        )
        print(
            f"post-p>new_data>{ParserHelper.make_value_visible(new_data)}"
            + f"<continue_sequence>{continue_sequence}<delayed_continue>{delayed_continue}<"
        )
        print(
            f"post-p>transformed_data>{ParserHelper.make_value_visible(transformed_data)}<"
        )

        transformed_data = f"{transformed_data}{new_data}"

        print("---")
        print(
            f">>>>{ParserHelper.make_value_visible(current_token)}"
            + f"-->{ParserHelper.make_value_visible(transformed_data)}<--"
        )
        print(
            f">>container-stack-->{ParserHelper.make_value_visible(self.container_token_stack)}"
        )
        print(f">>block_stack-->{ParserHelper.make_value_visible(self.block_stack)}")

        self.__look_for_last_block_token()
        return new_data, delayed_continue, continue_sequence, transformed_data

    # pylint: enable=too-many-arguments

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
            transformed_data = transformed_data[0:-1]
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
                        f"{transformed_data[0:nth_index]}{ParserHelper.newline_character}"
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
        continue_sequence,
        delayed_continue,
    ):

        skip_merge = False
        pragma_token = None
        if current_token.token_name in self.start_container_token_handlers:
            start_handler_fn = self.start_container_token_handlers[
                current_token.token_name
            ]
            new_data, continue_sequence = start_handler_fn(
                current_token, previous_token, next_token, transformed_data
            )
            skip_merge = True

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
                new_data, continue_sequence, delayed_continue = end_handler_fn(
                    current_token, actual_tokens, token_index
                )
            else:
                assert False, f"end_current_token>>{current_token.type_name}"
        else:
            assert False, f"current_token>>{current_token}"
        return new_data, continue_sequence, delayed_continue, skip_merge, pragma_token

    # pylint: enable=too-many-arguments

    # pylint: disable=too-many-boolean-expressions
    @classmethod
    def __perform_container_post_processing_lists_look_for_special(
        cls,
        block_should_end_with_newline,
        current_token,
        actual_tokens,
        transformed_data,
    ):
        special_text_in_list_exception = False
        if not block_should_end_with_newline:
            ind = actual_tokens.index(current_token)
            print(
                f">>actual_tokens[{ind}]>>{ParserHelper.make_value_visible(actual_tokens[ind])}"
            )
            while actual_tokens[ind].is_inline:
                print(
                    f">>actual_tokens[{ind}]>>{ParserHelper.make_value_visible(actual_tokens[ind])}"
                )
                ind -= 1
            print(
                f"<<actual_tokens[{ind}]>>{ParserHelper.make_value_visible(actual_tokens[ind])}"
            )
            if (
                actual_tokens[ind].is_paragraph
                and (
                    transformed_data
                    and transformed_data[-1] == ParserHelper.newline_character
                )
                and (
                    current_token.is_text
                    or current_token.is_inline_emphasis
                    or current_token.is_inline_link
                    or current_token.is_inline_image
                    or current_token.is_inline_raw_html
                )
            ):
                special_text_in_list_exception = True
        print(f"?>special_text_in_list_exception>{special_text_in_list_exception}")
        return special_text_in_list_exception

    # pylint: enable=too-many-boolean-expressions

    # pylint: disable=too-many-arguments
    def __perform_container_post_processing_lists_merge(
        self,
        next_token,
        current_token,
        skip_merge,
        continue_sequence,
        new_data,
        delayed_continue,
        block_should_end_with_newline,
        top_of_list_token_stack,
        force_newline_processing,
        special_text_in_list_exception,
        merge_with_block_start,
    ):
        print(
            f"s/c>{ParserHelper.make_value_visible(skip_merge)}>>{ParserHelper.make_value_visible(continue_sequence)}>>"
        )
        print(
            f"__merge_with_container_data>new_data>{ParserHelper.make_value_visible(new_data)}"
        )
        print(f"__merge_with_container_data>skip_merge>{skip_merge}")
        print(f"__merge_with_container_data>continue_sequence>{continue_sequence}<")
        if not skip_merge and continue_sequence:
            print(
                f"__merge_with_container_data>:{ParserHelper.make_value_visible(new_data)}:<"
            )
            print(
                f"merge_with_block_start>:{ParserHelper.make_value_visible(merge_with_block_start)}:<"
            )

            need_to_massage_data = (
                current_token.is_setext_heading_end and next_token.is_list_end
            )
            if need_to_massage_data:
                assert new_data and new_data[-1] == ParserHelper.newline_character
                new_data = new_data[:-1]
            new_data, delayed_continue = self.__merge_with_container_data(
                new_data,
                next_token,
                current_token,
                continue_sequence,
                delayed_continue,
                block_should_end_with_newline,
                top_of_list_token_stack,
                force_newline_processing,
                special_text_in_list_exception,
                merge_with_block_start,
            )
            if need_to_massage_data:
                new_data = f"{new_data}{ParserHelper.newline_character}"

        print(f"new_data>{ParserHelper.make_value_visible(new_data)}<<")
        print(f"delayed_continue>{ParserHelper.make_value_visible(delayed_continue)}<<")
        print(
            f"continue_sequence>{ParserHelper.make_value_visible(continue_sequence)}<<"
        )
        return new_data, delayed_continue

    # pylint: enable=too-many-arguments

    # pylint: disable=too-many-arguments
    @classmethod
    def __perform_container_post_processing_lists_init(
        cls, current_token, next_token, previous_token, skip_merge, delayed_continue
    ):
        block_should_end_with_newline, force_newline_processing = False, False
        if current_token.is_fenced_code_block_end:
            block_should_end_with_newline = True
            if next_token.is_list_end:
                skip_merge = True
        elif current_token.is_setext_heading_end:
            block_should_end_with_newline = True
        elif previous_token and previous_token.is_html_block:
            block_should_end_with_newline = True
            force_newline_processing = True

        if skip_merge:
            delayed_continue = ""

        return (
            block_should_end_with_newline,
            force_newline_processing,
            skip_merge,
            delayed_continue,
        )

    # pylint: enable=too-many-arguments

    # pylint: disable=too-many-arguments
    def __perform_container_post_processing_lists(
        self,
        current_token,
        new_data,
        skip_merge,
        delayed_continue,
        continue_sequence,
        next_token,
        top_of_list_token_stack,
        previous_token,
        actual_tokens,
        transformed_data,
    ):
        print(
            f">>__perform_container_post_processing_lists>>:{ParserHelper.make_value_visible(new_data)}:<<"
        )

        (
            block_should_end_with_newline,
            force_newline_processing,
            skip_merge,
            delayed_continue,
        ) = self.__perform_container_post_processing_lists_init(
            current_token, next_token, previous_token, skip_merge, delayed_continue
        )

        print(f">>previous_token>>{ParserHelper.make_value_visible(previous_token)}")
        print(f">>current_token>>{ParserHelper.make_value_visible(current_token)}")
        print(f">>next_token>>{ParserHelper.make_value_visible(next_token)}")
        print(
            f">>self.container_token_stack>>{ParserHelper.make_value_visible(self.container_token_stack)}"
        )

        merge_with_block_start = bool(
            self.container_token_stack[0].is_block_quote_start
        )

        special_text_in_list_exception = (
            self.__perform_container_post_processing_lists_look_for_special(
                block_should_end_with_newline,
                current_token,
                actual_tokens,
                transformed_data,
            )
        )

        print(
            f"?>{ParserHelper.make_value_visible(delayed_continue)}>>{ParserHelper.make_value_visible(new_data)}>>"
        )
        if (
            delayed_continue
            and new_data
            and not current_token.is_blank_line
            and not merge_with_block_start
        ):
            print(
                f"__merge_with_container_data--nd>:{ParserHelper.make_value_visible(new_data)}:<"
            )
            if not special_text_in_list_exception:
                new_data = f"{delayed_continue}{new_data}"
            delayed_continue = ""
            print(
                f"__merge_with_container_data--nd>:{ParserHelper.make_value_visible(new_data)}:<"
            )

        (
            new_data,
            delayed_continue,
        ) = self.__perform_container_post_processing_lists_merge(
            next_token,
            current_token,
            skip_merge,
            continue_sequence,
            new_data,
            delayed_continue,
            block_should_end_with_newline,
            top_of_list_token_stack,
            force_newline_processing,
            special_text_in_list_exception,
            merge_with_block_start,
        )
        return (
            ParserHelper.resolve_all_from_text(new_data),
            delayed_continue,
            continue_sequence,
        )

    # pylint: enable=too-many-arguments

    # pylint: disable=too-many-arguments
    def __perform_container_post_processing(
        self,
        current_token,
        new_data,
        skip_merge,
        delayed_continue,
        continue_sequence,
        next_token,
        previous_token,
        actual_tokens,
        transformed_data,
    ):
        """
        Perform any post processing required by the containers.  This is intentionally
        kept separate to ensure that the leaf and inline processing is distinct and
        separate.
        """

        top_of_list_token_stack = (
            self.container_token_stack[-1] if self.container_token_stack else None
        )
        if top_of_list_token_stack and top_of_list_token_stack.is_block_quote_start:
            print(
                f"pcpp-leading_text_index>{top_of_list_token_stack.leading_text_index}"
            )

        if not top_of_list_token_stack:
            print("nada")

            data_to_emit = (
                ParserHelper.resolve_noops_from_text(new_data)
                if self.block_stack and self.block_stack[-1].is_code_block
                else new_data
            )
            return (
                data_to_emit,
                delayed_continue,
                continue_sequence,
            )

        if top_of_list_token_stack.is_list_start:
            print("lists")
            return self.__perform_container_post_processing_lists(
                current_token,
                new_data,
                skip_merge,
                delayed_continue,
                continue_sequence,
                next_token,
                top_of_list_token_stack,
                previous_token,
                actual_tokens,
                transformed_data,
            )

        assert top_of_list_token_stack.is_block_quote_start
        print("bq")
        (
            new_data,
            delayed_continue,
            continue_sequence,
        ) = self.__perform_container_post_processing_block_quote(
            current_token,
            new_data,
            skip_merge,
            delayed_continue,
            continue_sequence,
            next_token,
            top_of_list_token_stack,
        )
        if top_of_list_token_stack and top_of_list_token_stack.is_block_quote_start:
            print(
                f"pcpp-leading_text_index<{top_of_list_token_stack.leading_text_index}"
            )
        return (
            new_data,
            delayed_continue,
            continue_sequence,
        )

    # pylint: enable=too-many-arguments

    @classmethod
    def __merge_with_noop_in_data(cls, new_data, continue_sequence):
        """
        Take care of a merge for a new leaf line with a NOOP character in the
        sequence.

        Note that the tricky combination of NOOP logic means that this is not
        a candidate for the recombine_string_with_whitespace function.
        """
        split_new_data = new_data.split(ParserHelper.newline_character)
        split_new_data_length = len(split_new_data)
        use_abbreviated_list = False
        if new_data and new_data[-1] == ParserHelper.newline_character:
            split_new_data_length -= 1
            use_abbreviated_list = True
        line_parts = [split_new_data[0]]
        for split_index in range(1, split_new_data_length):
            if (
                split_new_data[split_index]
                and split_new_data[split_index][0]
                == ParserHelper.replace_noop_character
            ):
                line_parts.extend(
                    [ParserHelper.newline_character, split_new_data[split_index][1:]]
                )
            else:
                line_parts.extend(
                    [
                        ParserHelper.newline_character,
                        continue_sequence,
                        split_new_data[split_index],
                    ]
                )
        print(f">>line_parts>>{line_parts}")
        if use_abbreviated_list:
            line_parts.extend([ParserHelper.newline_character, split_new_data[-1]])

        return "".join(line_parts)

    @classmethod
    def __merge_with_blech_in_data(cls, new_data, continue_sequence):
        """
        Take care of a merge for a new leaf line with a blech character in the
        sequence.

        Note that the tricky combination of Blech logic means that this is not
        a candidate for the recombine_string_with_whitespace function.
        """

        split_new_data = new_data.split(ParserHelper.newline_character)
        line_parts = [split_new_data[0]]
        for next_split_item in range(1, len(split_new_data)):
            next_continue_separator, next_data_item = (
                continue_sequence,
                split_new_data[next_split_item],
            )
            while next_data_item and next_data_item[0] == ParserHelper.blech_character:
                next_continue_separator = next_continue_separator[1:]
                next_data_item = next_data_item[1:]
            line_parts.extend(
                [
                    ParserHelper.newline_character,
                    next_continue_separator,
                    next_data_item,
                ]
            )

        return "".join(line_parts)

    @classmethod
    def __merge_with_leading_spaces_in_data(cls, new_data, top_of_list_token_stack):
        """
        Take care of a merge for a new leaf line with leading spaces in the container
        block's whitespaces.
        """
        (
            new_data,
            top_of_list_token_stack.leading_spaces_index,
        ) = ParserHelper.recombine_string_with_whitespace(
            new_data,
            top_of_list_token_stack.leading_spaces,
            top_of_list_token_stack.leading_spaces_index,
            post_increment_index=True,
        )
        return new_data

    def __merge_xx_with_last_list_block(
        self, last_list_block, top_block_stack_token, next_token
    ):
        additional_whitespace = ""
        block_token_index = self.container_token_stack.index(top_block_stack_token)
        list_token_index = self.container_token_stack.index(last_list_block)
        print(
            f"block_token_index>{block_token_index}, list_token_index={list_token_index}"
        )
        if list_token_index > block_token_index:
            extra_count = last_list_block.indent_level - len(
                last_list_block.extracted_whitespace
            )
            print(f"extra_count>{extra_count}")
            print(f"next_token>{ParserHelper.make_value_visible(next_token)}")
            if (
                not next_token.is_blank_line
                and not next_token.is_new_list_item
                and not next_token.is_list_end
            ):
                additional_whitespace = ParserHelper.repeat_string(
                    ParserHelper.space_character, extra_count
                )
                print(f"additional_whitespace->{additional_whitespace}<")
        return additional_whitespace

    def __merge_xx(self, new_data, top_block_stack_token, last_list_block, next_token):
        """
        Take care of a merge for a new leaf line with leading spaces in the container
        block's whitespaces.

        Note that the tricky combination of leading_text_index logic means that this
        is not a candidate for the recombine_string_with_whitespace function.
        """
        split_new_data, split_leading_spaces = (
            new_data.split(ParserHelper.newline_character),
            top_block_stack_token.leading_spaces.split(ParserHelper.newline_character),
        )
        split_leading_spaces_size, new_data = (
            len(split_leading_spaces),
            split_new_data[0],
        )

        print(f"last_list_block>{ParserHelper.make_value_visible(last_list_block)}")
        additional_whitespace = ""
        if last_list_block:
            additional_whitespace = self.__merge_xx_with_last_list_block(
                last_list_block, top_block_stack_token, next_token
            )

        parts_to_merge = [new_data]
        for i in range(1, len(split_new_data)):
            print(f"::{i}::{split_new_data[i]}::")
            print(
                f"::{top_block_stack_token.leading_text_index}::{split_leading_spaces}::"
            )
            if top_block_stack_token.leading_text_index < split_leading_spaces_size:
                print("a")
                parts_to_merge.extend(
                    [
                        ParserHelper.newline_character,
                        split_leading_spaces[top_block_stack_token.leading_text_index],
                        split_new_data[i],
                        additional_whitespace,
                    ]
                )
            else:
                print("b")
                parts_to_merge.extend(
                    [ParserHelper.newline_character, split_new_data[i]]
                )

            print(f"__merge_xx-post->{top_block_stack_token.leading_text_index}")
            top_block_stack_token.leading_text_index += 1

        print(f"parts_to_merge>>{parts_to_merge}<<")
        return "".join(parts_to_merge)

    # pylint: disable=too-many-arguments
    def __merge_with_container_data_ends_with_newline(
        self,
        continue_sequence,
        new_data,
        next_token,
        top_of_list_token_stack,
        current_token,
    ):
        print("block 1")
        delayed_continue = continue_sequence
        last_block_quote_block = self.__find_last_block_quote_on_stack()
        last_list_block = self.__find_last_list_on_stack()
        if last_block_quote_block:
            print("block 1a")
            new_data = self.__merge_xx(
                new_data, last_block_quote_block, last_list_block, next_token
            )
        elif top_of_list_token_stack and top_of_list_token_stack.leading_spaces:
            print("block 1b?")
            if current_token.is_link_reference_definition:
                print("block 1b")
                did_remove_trailing_newline = (
                    new_data and new_data[-1] == ParserHelper.newline_character
                )
                if did_remove_trailing_newline:
                    new_data = new_data[0:-1]
                new_data = self.__merge_with_leading_spaces_in_data(
                    new_data, top_of_list_token_stack
                )
                if did_remove_trailing_newline:
                    new_data = f"{new_data}{ParserHelper.newline_character}"
        return delayed_continue, new_data

    # pylint: enable=too-many-arguments

    # pylint: disable=too-many-arguments
    def __merge_with_container_data_contains_newline(
        self,
        new_data,
        block_should_end_with_newline,
        next_token,
        force_newline_processing,
        continue_sequence,
        top_of_list_token_stack,
    ):
        print("block 2")
        block_ends_with_newline = (
            block_should_end_with_newline
            and new_data
            and new_data[-1] == ParserHelper.newline_character
        )
        remove_trailing_newline = block_ends_with_newline and (
            next_token.is_blank_line or force_newline_processing
        )
        if remove_trailing_newline:
            new_data = new_data[0:-1]

        last_block_quote_block = self.__find_last_block_quote_on_stack()
        if ParserHelper.blech_character in new_data:
            new_data = self.__merge_with_blech_in_data(new_data, continue_sequence)
        elif top_of_list_token_stack.leading_spaces:
            new_data = self.__merge_with_leading_spaces_in_data(
                new_data, top_of_list_token_stack
            )
        elif last_block_quote_block:
            new_data = self.__merge_xx(
                new_data, last_block_quote_block, None, next_token
            )

        if remove_trailing_newline:
            new_data = f"{new_data}{ParserHelper.newline_character}"
        if block_ends_with_newline and next_token and next_token.is_new_list_item:
            new_data = new_data[0 : -len(continue_sequence)]
        return new_data

    # pylint: enable=too-many-arguments

    # pylint: disable=too-many-arguments
    def __merge_with_container_data(
        self,
        new_data,
        next_token,
        current_token,
        continue_sequence,
        delayed_continue,
        block_should_end_with_newline,
        top_of_list_token_stack,
        force_newline_processing,
        special_text_in_list_exception,
        merge_with_block_start,
    ):
        """
        Merge the leaf data with the container data.
        """

        print(f"mwcd:>>new_data>>{ParserHelper.make_value_visible(new_data)}<<")
        if special_text_in_list_exception:
            new_data = f"{ParserHelper.newline_character}{new_data}"

        if ParserHelper.replace_noop_character in new_data:
            print("noop")
            new_data = self.__merge_with_noop_in_data(new_data, continue_sequence)
        elif (
            not block_should_end_with_newline
            and new_data
            and new_data[-1] == ParserHelper.newline_character
        ):
            (
                delayed_continue,
                new_data,
            ) = self.__merge_with_container_data_ends_with_newline(
                continue_sequence,
                new_data,
                next_token,
                top_of_list_token_stack,
                current_token,
            )
        elif ParserHelper.newline_character in new_data:
            new_data = self.__merge_with_container_data_contains_newline(
                new_data,
                block_should_end_with_newline,
                next_token,
                force_newline_processing,
                continue_sequence,
                top_of_list_token_stack,
            )
        elif merge_with_block_start:
            print("block 3")

        if special_text_in_list_exception:
            assert new_data and new_data[0] == ParserHelper.newline_character
            new_data = new_data[1:]

        print(f"mwcd:>>new_data>>{ParserHelper.make_value_visible(new_data)}<<")
        return new_data, delayed_continue

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
            extracted_whitespace = extracted_whitespace[0:line_end_index]
        extracted_whitespace = ParserHelper.resolve_all_from_text(extracted_whitespace)

        if extracted_whitespace:
            print(
                f">>self.container_token_stack>>{ParserHelper.make_value_visible(self.container_token_stack)}<"
            )
            print(
                f">>extracted_whitespace>>{ParserHelper.make_value_visible(extracted_whitespace)}<"
            )
            found_block_token = None
            was_list_found = False
            for i in range(len(self.container_token_stack) - 1, -1, -1):
                print(
                    f">>self.container_token_stack>>{ParserHelper.make_value_visible(self.container_token_stack[i])}<"
                )
                if self.container_token_stack[i].is_block_quote_start:
                    found_block_token = self.container_token_stack[i]
                    break
                was_list_found = True
            print(
                f">>found_block_token>>{ParserHelper.make_value_visible(found_block_token)}<"
            )
            if found_block_token and was_list_found:
                split_leading_spaces = found_block_token.leading_spaces.split(
                    ParserHelper.newline_character
                )
                print(
                    f">>found_block_token.leading_text_index>>{found_block_token.leading_text_index}<"
                )
                print(f">>xy>>{ParserHelper.make_value_visible(split_leading_spaces)}<")
                specific_start = split_leading_spaces[
                    found_block_token.leading_text_index - 1
                ]
                print(
                    f">>specific_start>>{ParserHelper.make_value_visible(specific_start)}<"
                )
                print(
                    f">>extracted_whitespace>>{ParserHelper.make_value_visible(extracted_whitespace)}<"
                )
                if len(specific_start) <= len(extracted_whitespace):
                    extracted_whitespace = extracted_whitespace[len(specific_start) :]

        return extracted_whitespace

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
        extra_newline_after_text_token = ""
        if (
            self.block_stack
            and self.block_stack[-1].is_fenced_code_block
            and previous_token.is_text
        ):
            extra_newline_after_text_token = ParserHelper.newline_character

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
        start_token = current_token.start_markdown_token
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
                ParserHelper.repeat_string(start_token.fence_character, fence_count),
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

        already_existing_whitespace = None
        if len(self.container_token_stack) > 1 and (
            self.container_token_stack[-2].is_list_start
            and current_token.line_number == self.container_token_stack[-2].line_number
        ):
            already_existing_whitespace = ParserHelper.repeat_string(
                " ", self.container_token_stack[-2].indent_level
            )

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
        return selected_leading_sequence, ""

    # pylint: disable=too-many-arguments
    @classmethod
    def __perform_container_post_processing_block_quote(
        cls,
        current_token,
        new_data,
        skip_merge,
        delayed_continue,
        continue_sequence,
        next_token,
        top_of_list_token_stack,
    ):
        _ = (current_token, skip_merge, next_token)

        if ParserHelper.newline_character in new_data:
            composed_data = []
            print(
                f"1<<composed_data<<{ParserHelper.make_value_visible(composed_data)}"
                + f"<<new<<{ParserHelper.make_value_visible(new_data)}<<"
            )
            while ParserHelper.newline_character in new_data:

                print(">>[{ParserHelper.make_value_visible(new_data)}]<<")
                print(f"bq-post->{top_of_list_token_stack.leading_text_index}")
                next_newline_index = new_data.index(ParserHelper.newline_character)
                composed_data.extend(
                    [new_data[0:next_newline_index], ParserHelper.newline_character]
                )

                split_leading_spaces = top_of_list_token_stack.leading_spaces.split(
                    ParserHelper.newline_character
                )
                split_leading_spaces_size = len(split_leading_spaces)
                if (
                    top_of_list_token_stack.leading_text_index
                    < split_leading_spaces_size
                ):
                    composed_data.append(
                        split_leading_spaces[top_of_list_token_stack.leading_text_index]
                    )
                else:
                    print(
                        "top_of_list_token_stack.leading_text_index="
                        + f"{top_of_list_token_stack.leading_text_index},"
                        + f"split_leading_spaces_size={split_leading_spaces_size}"
                    )
                    assert (
                        top_of_list_token_stack.leading_text_index
                        == split_leading_spaces_size
                    )
                print(
                    f"current_token<<{ParserHelper.make_value_visible(current_token)}<<"
                )
                print(f"next_token<<{ParserHelper.make_value_visible(next_token)}<<")

                # bob = True
                # if (current_token.is_fenced_code_block and next_token.is_fenced_code_block_end) or \
                #     (current_token.is_fenced_code_block_end and current_token.was_forced and False) or \
                #     (current_token.is_paragraph_end and next_token.is_block_quote_end and True):
                #     bob = False

                # if bob:
                print(f"bq-post->{top_of_list_token_stack.leading_text_index}")
                top_of_list_token_stack.leading_text_index += 1
                print(f"bq-post->{top_of_list_token_stack.leading_text_index}")
                new_data = new_data[next_newline_index + 1 :]
            print(
                f"2<<composed_data<<{ParserHelper.make_value_visible(composed_data)}"
                + f"<<new<<{ParserHelper.make_value_visible(new_data)}<<"
            )
            composed_data.append(new_data)
            print(
                f"3<<composed_data<<{ParserHelper.make_value_visible(composed_data)}"
                + f"<<new<<{ParserHelper.make_value_visible(new_data)}<<"
            )
            new_data = "".join(composed_data)

        return (
            ParserHelper.resolve_all_from_text(new_data),
            delayed_continue,
            continue_sequence,
        )

    # pylint: enable=too-many-arguments

    def __rehydrate_list_start(
        self, current_token, previous_token, next_token, transformed_data
    ):
        """
        Rehydrate the unordered list start token.
        """
        self.container_token_stack.append(copy.deepcopy(current_token))

        previous_indent, extracted_whitespace = 0, current_token.extracted_whitespace
        if previous_token:
            if previous_token.is_list_start:
                previous_indent = previous_token.indent_level
                assert len(current_token.extracted_whitespace) == previous_indent
                extracted_whitespace = ""
            elif previous_token.is_block_quote_start:

                extracted_whitespace = ""
                previous_indent = (
                    len(
                        previous_token.calculate_next_leading_space_part(
                            increment_index=False
                        )
                    )
                    if ParserHelper.newline_character in previous_token.leading_spaces
                    else len(previous_token.leading_spaces)
                )

        print(f">>extracted_whitespace>>{extracted_whitespace}<<")
        print(
            f">>transformed_data>>{ParserHelper.make_value_visible(transformed_data)}<<"
        )

        (
            adjustment_since_newline,
            extracted_whitespace,
        ) = self.__adjust_whitespace_for_block_quote(
            transformed_data, extracted_whitespace
        )

        start_sequence = (
            f"{extracted_whitespace}{current_token.list_start_sequence}"
            if current_token.is_unordered_list_start
            else f"{extracted_whitespace}{current_token.list_start_content}{current_token.list_start_sequence}"
        )
        print(f">>start_sequence>>:{start_sequence}:<<")
        if not next_token.is_blank_line:
            start_sequence = start_sequence.ljust(
                current_token.indent_level - previous_indent - adjustment_since_newline,
                " ",
            )
            print(f">>start_sequence>>:{start_sequence}:<<")
        return start_sequence, ParserHelper.repeat_string(
            " ", current_token.indent_level
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
        print(f">>transformed_data_since_newline>>:{transformed_data_since_newline}:<<")
        adjustment_since_newline, transformed_data_since_newline_size = 0, len(
            transformed_data_since_newline
        )
        if (
            extracted_whitespace
            and len(extracted_whitespace) >= transformed_data_since_newline_size
            and ">" in transformed_data_since_newline
        ):
            adjustment_since_newline = transformed_data_since_newline_size
            extracted_whitespace = extracted_whitespace[adjustment_since_newline:]
        return adjustment_since_newline, extracted_whitespace

    def __reset_container_continue_sequence(self):
        return (
            ParserHelper.repeat_string(" ", self.container_token_stack[-1].indent_level)
            if self.container_token_stack
            and self.container_token_stack[-1].is_list_start
            else ""
        )

    def __rehydrate_block_quote_end(self, current_token, actual_tokens, token_index):

        text_to_add, continue_sequence, old_line_number = (
            "",
            "",
            self.container_token_stack[-1].line_number,
        )

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

        stack_copy_of_token = self.container_token_stack[-1]
        del self.container_token_stack[-1]
        if any_non_container_end_tokens:
            continue_sequence = self.__reset_container_continue_sequence()
            if (
                self.container_token_stack
                and self.container_token_stack[-1].is_block_quote_start
                and self.container_token_stack[-1].line_number == old_line_number
            ):
                text_to_add = self.container_token_stack[
                    -1
                ].calculate_next_leading_space_part()

            print(f">>current_token>>{ParserHelper.make_value_visible(current_token)}")
            print(
                ">>current_token.start_markdown_token>>"
                + f"{ParserHelper.make_value_visible(current_token.start_markdown_token)}"
            )
            print(
                ">>extracted_whitespace>>:"
                + f"{ParserHelper.make_value_visible(current_token.start_markdown_token.leading_spaces)}:<<"
            )

            print(
                f">>orig>>:{ParserHelper.make_value_visible(current_token.start_markdown_token)}:<<"
            )
            print(f">>copy>>:{ParserHelper.make_value_visible(stack_copy_of_token)}:<<")
            assert str(current_token.start_markdown_token) == str(stack_copy_of_token)

            leading_text_index, expected_leading_text_index = (
                stack_copy_of_token.leading_text_index,
                ParserHelper.count_newlines_in_text(stack_copy_of_token.leading_spaces)
                + 1,
            )

            assert isinstance(expected_leading_text_index, int)
            assert leading_text_index in [
                expected_leading_text_index,
                expected_leading_text_index + 1,
            ], f"leading_text_index={leading_text_index};expected_leading_text_index={expected_leading_text_index}"

        return text_to_add, continue_sequence, continue_sequence

    def __rehydrate_list_start_end(self, current_token, actual_tokens, token_index):
        """
        Rehydrate the ordered list end token.
        """
        _ = actual_tokens, token_index
        del self.container_token_stack[-1]
        continue_sequence, leading_spaces_index, expected_leading_spaces_index = (
            self.__reset_container_continue_sequence(),
            current_token.start_markdown_token.leading_spaces_index,
            ParserHelper.count_newlines_in_text(
                current_token.start_markdown_token.extracted_whitespace
            ),
        )

        assert leading_spaces_index == expected_leading_spaces_index, (
            f"leading_spaces_index={leading_spaces_index};"
            + f"expected_leading_spaces_index={len(expected_leading_spaces_index)}"
        )
        return "", continue_sequence, continue_sequence

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

        start_sequence = (
            f"{extracted_whitespace}{current_token.list_start_content}"
            + f"{self.container_token_stack[-1].list_start_sequence}"
        )
        if not next_token.is_blank_line:
            start_sequence = start_sequence.ljust(
                self.container_token_stack[-1].indent_level - adjustment_since_newline,
                " ",
            )
        continue_sequence = ParserHelper.repeat_string(
            " ", self.container_token_stack[-1].indent_level
        )

        return start_sequence, continue_sequence

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
        main_text = ParserHelper.remove_all_from_text(current_token.token_text)
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

        raw_text = current_token.raw_tag
        raw_text = ParserHelper.remove_all_from_text(raw_text)

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
                main_text = f"{current_token.end_whitespace[0:-1]}{main_text}"
        return main_text

    def __find_last_block_quote_on_stack(self):
        last_block_quote_block = None
        if self.container_token_stack:
            print(
                f"__find_last_block_quote_on_stack>>{ParserHelper.make_value_visible(self.container_token_stack)}<<"
            )
            search_index = len(self.container_token_stack) - 1
            while search_index >= 0:
                if self.container_token_stack[search_index].is_block_quote_start:
                    last_block_quote_block = self.container_token_stack[search_index]
                    break
                search_index -= 1
            print(
                "__find_last_block_quote_on_stack>>search_index>>"
                + f"{ParserHelper.make_value_visible(last_block_quote_block)}<<"
            )
            if last_block_quote_block:
                print(
                    "__find_last_block_quote_on_stack>>last_block_quote_block.leading_text_index>>"
                    + f"{last_block_quote_block.leading_text_index}<<"
                )
        return last_block_quote_block

    def __find_last_list_on_stack(self):
        last_list_block = None
        if self.container_token_stack:
            print(
                f"__find_last_list_on_stack>>{ParserHelper.make_value_visible(self.container_token_stack)}<<"
            )
            search_index = len(self.container_token_stack) - 1
            while search_index >= 0:
                if self.container_token_stack[search_index].is_list_start:
                    last_list_block = self.container_token_stack[search_index]
                    break
                search_index -= 1
            print(
                f"__find_last_list_on_stack>>last_list_block>>{ParserHelper.make_value_visible(last_list_block)}<<"
            )
        return last_list_block
