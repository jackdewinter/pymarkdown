"""
Module to provide for a transformation from tokens to a markdown document.
"""
import inspect

from pymarkdown.link_helper import LinkHelper
from pymarkdown.markdown_token import (
    AtxHeadingMarkdownToken,
    BlankLineMarkdownToken,
    BlockQuoteMarkdownToken,
    EmailAutolinkMarkdownToken,
    EmphasisMarkdownToken,
    EndMarkdownToken,
    FencedCodeBlockMarkdownToken,
    HardBreakMarkdownToken,
    HtmlBlockMarkdownToken,
    ImageStartMarkdownToken,
    IndentedCodeBlockMarkdownToken,
    InlineCodeSpanMarkdownToken,
    LinkReferenceDefinitionMarkdownToken,
    LinkStartMarkdownToken,
    MarkdownToken,
    MarkdownTokenClass,
    NewListItemMarkdownToken,
    OrderedListStartMarkdownToken,
    ParagraphMarkdownToken,
    RawHtmlMarkdownToken,
    SetextHeadingMarkdownToken,
    TextMarkdownToken,
    ThematicBreakMarkdownToken,
    UnorderedListStartMarkdownToken,
    UriAutolinkMarkdownToken,
)
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
        self.block_stack = []
        self.container_token_stack = []

        self.start_container_token_handlers = {}
        self.end_container_token_handlers = {}

        self.register_container_handlers(
            OrderedListStartMarkdownToken,
            self.__rehydrate_ordered_list_start,
            self.__rehydrate_ordered_list_start_end,
        )
        self.register_container_handlers(
            UnorderedListStartMarkdownToken,
            self.__rehydrate_unordered_list_start,
            self.__rehydrate_unordered_list_start_end,
        )
        self.register_container_handlers(
            NewListItemMarkdownToken, self.__rehydrate_next_list_item
        )
        self.register_container_handlers(
            BlockQuoteMarkdownToken,
            self.__rehydrate_block_quote,
            self.__rehydrate_block_quote_end,
        )

        self.start_token_handlers = {}
        self.end_token_handlers = {}

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

        assert issubclass(type_name, MarkdownToken), (
            "Token class '"
            + str(type_name)
            + "' must be descended from the 'MarkdownToken' class."
        )
        token_init_fn = type_name.__dict__["__init__"]
        init_parameters = {}
        for i in inspect.getfullargspec(token_init_fn)[0]:
            if i == "self":
                continue
            init_parameters[i] = ""
        handler_instance = type_name(**init_parameters)
        return handler_instance

    def register_handlers(self, type_name, start_token_handler, end_token_handler=None):
        """
        Register the handlers necessary to deal with token's start and end.
        """
        handler_instance = self.__create_type_instance(type_name)
        assert (
            handler_instance.token_class == MarkdownTokenClass.LEAF_BLOCK
            or handler_instance.token_class == MarkdownTokenClass.INLINE_BLOCK
        )

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
        assert handler_instance.token_class == MarkdownTokenClass.CONTAINER_BLOCK

        self.start_container_token_handlers[
            handler_instance.token_name
        ] = start_token_handler
        if end_token_handler:
            self.end_container_token_handlers[
                handler_instance.token_name
            ] = end_token_handler

    # pylint: disable=too-many-locals, too-many-branches
    def transform(self, actual_tokens):
        """
        Transform the incoming token stream back into Markdown.
        """
        transformed_data = ""
        avoid_processing = False
        previous_token = None

        print("---\nTransformToMarkdown\n---")

        continue_sequence = ""
        delayed_continue = ""
        for token_index, current_token in enumerate(actual_tokens):
            print(
                "\n\n>>>>"
                + ParserHelper.make_value_visible(current_token)
                + "-->"
                + ParserHelper.make_value_visible(transformed_data)
                + "<--"
            )
            next_token = None
            if token_index < len(actual_tokens) - 1:
                next_token = actual_tokens[token_index + 1]
            new_data = ""
            skip_merge = False

            print(
                "pre-h>continue_sequence>"
                + str(continue_sequence)
                + "<delayed_continue>"
                + str(delayed_continue)
                + "<"
            )

            if current_token.token_name in self.start_container_token_handlers:
                start_handler_fn = self.start_container_token_handlers[
                    current_token.token_name
                ]
                new_data, continue_sequence = start_handler_fn(
                    current_token, previous_token, next_token
                )
                skip_merge = True
            elif current_token.token_name in self.start_token_handlers:
                start_handler_fn = self.start_token_handlers[current_token.token_name]
                new_data = start_handler_fn(current_token, previous_token)

            elif isinstance(current_token, EndMarkdownToken):

                if current_token.type_name in self.end_token_handlers:
                    end_handler_fn = self.end_token_handlers[current_token.type_name]
                    new_data = end_handler_fn(current_token, previous_token, next_token)
                elif current_token.type_name in self.end_container_token_handlers:
                    end_handler_fn = self.end_container_token_handlers[
                        current_token.type_name
                    ]
                    new_data, continue_sequence, delayed_continue = end_handler_fn(
                        current_token
                    )
                else:
                    assert False, "end_current_token>>" + str(current_token.type_name)
            else:
                assert False, "current_token>>" + str(current_token)

            print(
                "post-h>new_data>"
                + ParserHelper.make_value_visible(new_data)
                + "<continue_sequence>"
                + str(continue_sequence)
                + "<delayed_continue>"
                + str(delayed_continue)
                + "<"
            )
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
                "post-p>new_data>"
                + ParserHelper.make_value_visible(new_data)
                + "<continue_sequence>"
                + str(continue_sequence)
                + "<delayed_continue>"
                + str(delayed_continue)
                + "<"
            )

            transformed_data += new_data

            print("---")
            print(
                ">>>>"
                + ParserHelper.make_value_visible(current_token)
                + "-->"
                + ParserHelper.make_value_visible(transformed_data)
                + "<--"
            )
            print(
                ">>container-stack-->"
                + ParserHelper.make_value_visible(self.container_token_stack)
            )
            print(
                ">>block_stack-->" + ParserHelper.make_value_visible(self.block_stack)
            )
            print("---")
            previous_token = current_token

        if transformed_data and transformed_data[-1] == ParserHelper.newline_character:
            transformed_data = transformed_data[0:-1]

        assert not self.block_stack
        assert not self.container_token_stack
        return transformed_data, avoid_processing

    # pylint: enable=too-many-locals, too-many-branches

    # pylint: disable=too-many-arguments
    # pylint: disable=unused-argument
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
        if skip_merge:
            delayed_continue = ""

        # TODO handle this better?
        block_should_end_with_newline = False
        force_newline_processing = False
        if current_token.token_name == "end-fcode-block":
            block_should_end_with_newline = True
        elif current_token.token_name == "end-setext":
            block_should_end_with_newline = True
        elif (
            previous_token
            and previous_token.token_name == MarkdownToken.token_html_block
        ):
            block_should_end_with_newline = True
            force_newline_processing = True

        special_text_in_list_exception = False

        print(">>previous_token>>" + ParserHelper.make_value_visible(previous_token))
        print(">>current_token>>" + ParserHelper.make_value_visible(current_token))
        if not block_should_end_with_newline:
            ind = actual_tokens.index(current_token)
            print(
                ">>actual_tokens["
                + str(ind)
                + "]>>"
                + ParserHelper.make_value_visible(actual_tokens[ind])
            )
            while actual_tokens[ind].token_class == MarkdownTokenClass.INLINE_BLOCK:
                print(
                    ">>actual_tokens["
                    + str(ind)
                    + "]>>"
                    + ParserHelper.make_value_visible(actual_tokens[ind])
                )
                ind -= 1
            print(
                "<<actual_tokens["
                + str(ind)
                + "]>>"
                + ParserHelper.make_value_visible(actual_tokens[ind])
            )
            if actual_tokens[ind].token_name == MarkdownToken.token_paragraph:
                if transformed_data.endswith("\n") and (
                    current_token.token_name == MarkdownToken.token_text
                    or current_token.token_name == MarkdownToken.token_inline_emphasis
                    or current_token.token_name == MarkdownToken.token_inline_link
                    or current_token.token_name == MarkdownToken.token_inline_image
                ):
                    special_text_in_list_exception = True

        print("?>special_text_in_list_exception>" + str(special_text_in_list_exception))
        print(
            "?>"
            + ParserHelper.make_value_visible(delayed_continue)
            + ">>"
            + ParserHelper.make_value_visible(new_data)
            + ">>"
        )
        if (
            delayed_continue
            and new_data
            and current_token.token_name != MarkdownToken.token_blank_line
        ):
            print("nd>")
            if not special_text_in_list_exception:
                new_data = delayed_continue + new_data
            delayed_continue = ""

        print(
            "s/c>"
            + ParserHelper.make_value_visible(skip_merge)
            + ">>"
            + ParserHelper.make_value_visible(continue_sequence)
            + ">>"
        )
        print(
            "__merge_with_container_data>new_data>"
            + ParserHelper.make_value_visible(new_data)
        )
        print("__merge_with_container_data>skip_merge>" + str(skip_merge))
        print(
            "__merge_with_container_data>continue_sequence>"
            + str(continue_sequence)
            + "<"
        )
        if not skip_merge and continue_sequence:
            print("__merge_with_container_data>")
            new_data, delayed_continue = self.__merge_with_container_data(
                new_data,
                next_token,
                continue_sequence,
                delayed_continue,
                block_should_end_with_newline,
                top_of_list_token_stack,
                force_newline_processing,
                special_text_in_list_exception,
            )

        print("??>" + ParserHelper.make_value_visible(new_data) + "<<")
        new_data = ParserHelper.resolve_noops_from_text(new_data)
        print("??>" + ParserHelper.make_value_visible(new_data) + "<<")
        return new_data, delayed_continue, continue_sequence

    # pylint: enable=unused-argument
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

        top_of_list_token_stack = None
        if self.container_token_stack:
            top_of_list_token_stack = self.container_token_stack[-1]

        if not top_of_list_token_stack:
            print("nada")

            if self.block_stack and (
                self.block_stack[-1].token_name == MarkdownToken.token_fenced_code_block
                or self.block_stack[-1].token_name
                == MarkdownToken.token_indented_code_block
            ):
                data_to_emit = ParserHelper.resolve_noops_from_text(new_data)
            else:
                data_to_emit = new_data
            return (
                data_to_emit,
                delayed_continue,
                continue_sequence,
            )

        if (
            top_of_list_token_stack.token_name
            == MarkdownToken.token_unordered_list_start
            or top_of_list_token_stack.token_name
            == MarkdownToken.token_ordered_list_start
        ):
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
        assert top_of_list_token_stack.token_name == MarkdownToken.token_block_quote
        print("bq")
        return self.__perform_container_post_processing_block_quote(
            current_token,
            new_data,
            skip_merge,
            delayed_continue,
            continue_sequence,
            next_token,
            top_of_list_token_stack,
        )

    # pylint: enable=too-many-arguments

    @classmethod
    def __merge_with_noop_in_data(cls, new_data, continue_sequence):
        """
        Take care of a merge for a new leaf line with a NOOP character in the
        sequence.
        """
        split_new_data = new_data.split("\n")
        split_new_data_length = len(split_new_data)
        if new_data.endswith("\n"):
            split_new_data_length -= 1
        for split_index in range(1, split_new_data_length):
            if (
                split_new_data[split_index]
                and split_new_data[split_index][0]
                == ParserHelper.replace_noop_character
            ):
                replacement_data = split_new_data[split_index][1:]
            else:
                replacement_data = continue_sequence + split_new_data[split_index]
            split_new_data[split_index] = replacement_data
        new_data = "\n".join(split_new_data)
        return new_data

    @classmethod
    def __merge_with_blech_in_data(cls, new_data, continue_sequence):
        """
        Take care of a merge for a new leaf line with a blech character in the
        sequence.
        """
        split_new_data = new_data.split("\n")
        for next_split_item in range(1, len(split_new_data)):
            next_continue_separator = continue_sequence
            next_data_item = split_new_data[next_split_item]
            while next_data_item.startswith(ParserHelper.blech_character):
                next_continue_separator = next_continue_separator[1:]
                next_data_item = next_data_item[1:]
            next_continue_separator += next_data_item
            split_new_data[next_split_item] = next_continue_separator
        new_data = "\n".join(split_new_data)
        return new_data

    @classmethod
    def __merge_with_leading_spaces_in_data(cls, new_data, top_of_list_token_stack):
        """
        Take care of a merge for a new leaf line with leading spaces in the container
        block's whitespaces.
        """
        split_new_data = new_data.split("\n")
        print("3b>>" + str(split_new_data) + "<")
        print(
            "top_of_list_token_stack>>"
            + ParserHelper.make_value_visible(top_of_list_token_stack)
            + "<"
        )
        split_leading_spaces = top_of_list_token_stack.leading_spaces.split("\n")
        print(
            "top_of_list_token_stack>>"
            + str(top_of_list_token_stack.leading_spaces_index)
            + "<"
            + ParserHelper.make_value_visible(top_of_list_token_stack.leading_spaces)
            + "<"
        )
        new_data = split_new_data[0]
        for i in range(1, len(split_new_data)):
            print("::" + str(i) + "::" + split_new_data[i] + "::")
            new_data += (
                "\n"
                + split_leading_spaces[top_of_list_token_stack.leading_spaces_index]
                + split_new_data[i]
            )
            top_of_list_token_stack.leading_spaces_index += 1
        return new_data

    # pylint: disable=too-many-arguments
    def __merge_with_container_data(
        self,
        new_data,
        next_token,
        continue_sequence,
        delayed_continue,
        block_should_end_with_newline,
        top_of_list_token_stack,
        force_newline_processing,
        special_text_in_list_exception,
    ):
        """
        Merge the leaf data with the container data.
        """

        # TODO can this be simplified like block quote?

        if special_text_in_list_exception:
            print(
                "special_text_in_list_exception>>"
                + ParserHelper.make_value_visible(new_data)
                + ">>"
            )
            new_data = "\n" + new_data
            print(
                "special_text_in_list_exception<<"
                + ParserHelper.make_value_visible(new_data)
                + "<<"
            )

        if ParserHelper.replace_noop_character in new_data:
            print("1>>")
            new_data = self.__merge_with_noop_in_data(new_data, continue_sequence)
        elif not block_should_end_with_newline and new_data.endswith("\n"):
            print("2>>")
            delayed_continue = continue_sequence
        elif "\n" in new_data:
            print(
                "3>>block_should_end_with_newline>>"
                + str(block_should_end_with_newline)
                + ">>new_data>>"
                + ParserHelper.make_value_visible(new_data)
            )
            block_ends_with_newline = (
                block_should_end_with_newline and new_data.endswith("\n")
            )
            print("3>>block_ends_with_newline>>" + str(block_ends_with_newline))
            remove_trailing_newline = False
            if block_ends_with_newline and (
                next_token.token_name == MarkdownToken.token_blank_line
                or force_newline_processing
            ):
                print("3remove_trailing_newline>>")
                remove_trailing_newline = True
                new_data = new_data[0:-1]

            if ParserHelper.blech_character in new_data:
                print("3a>>")
                new_data = self.__merge_with_blech_in_data(new_data, continue_sequence)
            elif top_of_list_token_stack.leading_spaces:
                print("3b>>")
                new_data = self.__merge_with_leading_spaces_in_data(
                    new_data, top_of_list_token_stack
                )

            if remove_trailing_newline:
                new_data += "\n"
            if (
                block_ends_with_newline
                and next_token
                and next_token.token_name == MarkdownToken.token_new_list_item
            ):
                print("4>>")
                new_data = new_data[0 : -len(continue_sequence)]

        if special_text_in_list_exception:
            print(
                "special_text_in_list_exception>>"
                + ParserHelper.make_value_visible(new_data)
                + ">>"
            )
            assert new_data.startswith("\n")
            new_data = new_data[1:]
            print(
                "special_text_in_list_exception<<"
                + ParserHelper.make_value_visible(new_data)
                + "<<"
            )

        return new_data, delayed_continue

    # pylint: enable=too-many-arguments

    # pylint: disable=unused-argument
    def __rehydrate_paragraph(self, current_token, previous_token):
        """
        Rehydrate the paragraph block from the token.
        """
        self.block_stack.append(current_token)
        current_token.rehydrate_index = 0
        extracted_whitespace = current_token.extracted_whitespace
        if ParserHelper.newline_character in extracted_whitespace:
            line_end_index = extracted_whitespace.index(ParserHelper.newline_character)
            extracted_whitespace = extracted_whitespace[0:line_end_index]
        return ParserHelper.resolve_blechs_from_text(extracted_whitespace)

    # pylint: enable=unused-argument

    # pylint: disable=unused-argument
    def __rehydrate_paragraph_end(self, current_token, previous_token, next_token):
        """
        Rehydrate the end of the paragraph block from the token.
        """
        top_stack_token = self.block_stack[-1]
        del self.block_stack[-1]
        return top_stack_token.final_whitespace + ParserHelper.newline_character

    # pylint: enable=unused-argument

    def __rehydrate_blank_line(self, current_token, previous_token):
        """
        Rehydrate the blank line from the token.
        """
        extra_newline_after_text_token = ""
        if (
            self.block_stack
            and self.block_stack[-1].token_name == MarkdownToken.token_fenced_code_block
        ):
            if previous_token.token_name == MarkdownToken.token_text:
                extra_newline_after_text_token = ParserHelper.newline_character

        return (
            extra_newline_after_text_token
            + current_token.extracted_whitespace
            + ParserHelper.newline_character
        )

    # pylint: disable=unused-argument
    def __rehydrate_indented_code_block(self, current_token, previous_token):
        """
        Rehydrate the indented code block from the token.
        """
        self.block_stack.append(current_token)
        return ""

    # pylint: enable=unused-argument

    # pylint: disable=unused-argument
    def __rehydrate_indented_code_block_end(
        self, current_token, previous_token, next_token
    ):
        """
        Rehydrate the end of the indented code block from the token.
        """
        del self.block_stack[-1]
        return ""

    # pylint: enable=unused-argument

    # pylint: disable=unused-argument
    def __rehydrate_html_block(self, current_token, previous_token):
        """
        Rehydrate the html block from the token.
        """
        self.block_stack.append(current_token)
        return "".ljust(current_token.fill_count, " ")

    # pylint: enable=unused-argument

    # pylint: disable=unused-argument
    def __rehydrate_html_block_end(self, current_token, previous_token, next_token):
        """
        Rehydrate the end of the html block from the token.
        """
        del self.block_stack[-1]
        return ""

    # pylint: enable=unused-argument

    # pylint: disable=unused-argument
    def __rehydrate_fenced_code_block(self, current_token, previous_token):
        """
        Rehydrate the fenced code block from the token.
        """
        self.block_stack.append(current_token)

        info_text = current_token.extracted_whitespace_before_info_string
        if current_token.pre_extracted_text:
            info_text += current_token.pre_extracted_text
        else:
            info_text += current_token.extracted_text
        if current_token.pre_text_after_extracted_text:
            info_text += current_token.pre_text_after_extracted_text
        else:
            info_text += current_token.text_after_extracted_text

        return (
            current_token.extracted_whitespace
            + ParserHelper.repeat_string(
                current_token.fence_character, current_token.fence_count
            )
            + info_text
            + ParserHelper.newline_character
        )

    # pylint: enable=unused-argument

    def __rehydrate_fenced_code_block_end(
        self, current_token, previous_token, next_token
    ):
        """
        Rehydrate the end of the fenced code block from the token.
        """
        start_token = current_token.start_markdown_token

        if not current_token.was_forced:
            split_extra_data = current_token.extra_data.split(":")
            assert len(split_extra_data) >= 2
            fence_count = int(split_extra_data[1])

            prefix_whitespace = ParserHelper.newline_character
            if previous_token.is_blank_line or previous_token.is_fenced_code_block:
                prefix_whitespace = ""
            prefix_whitespace += current_token.extracted_whitespace

            del self.block_stack[-1]
            return (
                prefix_whitespace
                + ParserHelper.repeat_string(start_token.fence_character, fence_count)
                + ParserHelper.newline_character
            )

        code_end_sequence = ""
        if (
            next_token is not None
            and previous_token.token_name != MarkdownToken.token_fenced_code_block
        ):
            code_end_sequence = "\n"
        del self.block_stack[-1]
        return code_end_sequence

    def __rehydrate_ordered_list_start(self, current_token, previous_token, next_token):
        """
        Rehydrate the unordered list start token.
        """
        new_instance = current_token.create_copy()
        self.container_token_stack.append(new_instance)

        previous_indent = 0
        extracted_whitespace = current_token.extracted_whitespace
        if previous_token and (
            previous_token.token_name == MarkdownToken.token_unordered_list_start
            or previous_token.token_name == MarkdownToken.token_ordered_list_start
        ):
            previous_indent = previous_token.indent_level
            assert len(current_token.extracted_whitespace) == previous_indent
            extracted_whitespace = ""

        start_sequence = (
            extracted_whitespace
            + current_token.list_start_content
            + current_token.list_start_sequence
        )
        if next_token.token_name != MarkdownToken.token_blank_line:
            start_sequence = start_sequence.ljust(
                current_token.indent_level - previous_indent, " "
            )
        continue_sequence = ParserHelper.repeat_string(" ", current_token.indent_level)
        return start_sequence, continue_sequence

    # pylint: disable=unused-argument
    def __rehydrate_block_quote(self, current_token, previous_token, next_token):
        new_instance = current_token.create_copy()
        self.container_token_stack.append(new_instance)

        print(">bquote>" + ParserHelper.make_value_visible(new_instance))
        split_leading_spaces = new_instance.leading_spaces.split("\n")
        print(
            ">split_leading_spaces>"
            + ParserHelper.make_value_visible(split_leading_spaces)
        )
        print(">leading_text_index>" + str(new_instance.leading_text_index))
        selected_leading_sequence = split_leading_spaces[
            new_instance.leading_text_index
        ]
        new_instance.leading_text_index += 1
        print(">leading_text_index>" + str(new_instance.leading_text_index))
        return selected_leading_sequence, ""

    # pylint: enable=unused-argument

    # pylint: disable=too-many-arguments
    # pylint: disable=unused-argument
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

        if "\n" in new_data:
            composed_data = ""
            print(
                "<<composed_data<<"
                + ParserHelper.make_value_visible(composed_data)
                + "<<new<<"
                + ParserHelper.make_value_visible(new_data)
                + "<<"
            )
            while "\n" in new_data:
                print(">>[" + ParserHelper.make_value_visible(new_data) + "]<<")
                split_leading_spaces = top_of_list_token_stack.leading_spaces.split(
                    "\n"
                )
                print(
                    ">split_leading_spaces>"
                    + str(len(split_leading_spaces))
                    + ">"
                    + ParserHelper.make_value_visible(split_leading_spaces)
                )
                print(
                    ">leading_text_index>"
                    + str(top_of_list_token_stack.leading_text_index)
                )

                next_newline_index = new_data.index("\n")
                composed_data += new_data[0:next_newline_index] + "\n"
                if top_of_list_token_stack.leading_text_index < len(
                    split_leading_spaces
                ):
                    composed_data += split_leading_spaces[
                        top_of_list_token_stack.leading_text_index
                    ]
                else:
                    assert top_of_list_token_stack.leading_text_index == len(
                        split_leading_spaces
                    )
                top_of_list_token_stack.leading_text_index += 1
                new_data = new_data[next_newline_index + 1 :]
                print(
                    ">>composed_data>>"
                    + ParserHelper.make_value_visible(composed_data)
                    + ">>new>>"
                    + ParserHelper.make_value_visible(new_data)
                    + ">>"
                )
            print(
                "<<composed_data<<"
                + ParserHelper.make_value_visible(composed_data)
                + "<<new<<"
                + ParserHelper.make_value_visible(new_data)
                + "<<"
            )
            composed_data += new_data
            print(
                "<<composed_data<<"
                + ParserHelper.make_value_visible(composed_data)
                + "<<new<<"
                + ParserHelper.make_value_visible(new_data)
                + "<<"
            )
            new_data = composed_data

        new_data = ParserHelper.resolve_noops_from_text(new_data)
        return new_data, delayed_continue, continue_sequence

    # pylint: enable=unused-argument
    # pylint: enable=too-many-arguments

    def __rehydrate_unordered_list_start(
        self, current_token, previous_token, next_token
    ):
        """
        Rehydrate the unordered list start token.
        """
        new_instance = current_token.create_copy()
        self.container_token_stack.append(new_instance)

        previous_indent = 0
        extracted_whitespace = current_token.extracted_whitespace
        if previous_token:
            if (
                previous_token.token_name == MarkdownToken.token_unordered_list_start
                or previous_token.token_name == MarkdownToken.token_ordered_list_start
            ):
                previous_indent = previous_token.indent_level
                assert len(current_token.extracted_whitespace) == previous_indent
                extracted_whitespace = ""
            elif previous_token.token_name == MarkdownToken.token_block_quote:
                assert "\n" not in previous_token.leading_spaces
                previous_indent = len(previous_token.leading_spaces)
                extracted_whitespace = ""

        start_sequence = extracted_whitespace + current_token.list_start_sequence
        if next_token.token_name != MarkdownToken.token_blank_line:
            start_sequence = start_sequence.ljust(
                current_token.indent_level - previous_indent, " "
            )
        continue_sequence = ParserHelper.repeat_string(" ", current_token.indent_level)
        return start_sequence, continue_sequence

    def __reset_container_continue_sequence(self):
        continue_sequence = ""
        if self.container_token_stack:
            # TODO what about bq?
            if (
                self.container_token_stack[-1].token_name
                == MarkdownToken.token_unordered_list_start
                or self.container_token_stack[-1].token_name
                == MarkdownToken.token_ordered_list_start
            ):
                continue_sequence = ParserHelper.repeat_string(
                    " ", self.container_token_stack[-1].indent_level
                )
        return continue_sequence

    # pylint: disable=unused-argument
    def __rehydrate_block_quote_end(self, current_token):
        del self.container_token_stack[-1]
        continue_sequence = self.__reset_container_continue_sequence()
        return "", continue_sequence, continue_sequence

    # pylint: enable=unused-argument

    # pylint: disable=unused-argument
    def __rehydrate_unordered_list_start_end(self, current_token):
        """
        Rehydrate the unordered list end token.
        """
        del self.container_token_stack[-1]
        continue_sequence = self.__reset_container_continue_sequence()
        return "", continue_sequence, continue_sequence

    # pylint: enable=unused-argument

    # pylint: disable=unused-argument
    def __rehydrate_ordered_list_start_end(self, current_token):
        """
        Rehydrate the ordered list end token.
        """
        del self.container_token_stack[-1]
        continue_sequence = self.__reset_container_continue_sequence()
        return "", continue_sequence, continue_sequence

    # pylint: enable=unused-argument

    # pylint: disable=unused-argument
    def __rehydrate_next_list_item(self, current_token, previous_token, next_token):
        """
        Rehydrate the next list item token.
        """
        if (
            self.container_token_stack[-1].token_name
            == MarkdownToken.token_unordered_list_start
            or self.container_token_stack[-1].token_name
            == MarkdownToken.token_ordered_list_start
        ):
            self.container_token_stack[-1].indent_level = current_token.indent_level
            self.container_token_stack[
                -1
            ].extracted_whitespace = current_token.extracted_whitespace
            self.container_token_stack[-1].compose_extra_data_field()

            start_sequence = (
                current_token.extracted_whitespace
                + current_token.list_start_content
                + self.container_token_stack[-1].list_start_sequence
            )
            if next_token.token_name != MarkdownToken.token_blank_line:
                start_sequence = start_sequence.ljust(
                    self.container_token_stack[-1].indent_level, " "
                )
            continue_sequence = ParserHelper.repeat_string(
                " ", self.container_token_stack[-1].indent_level
            )
        else:
            assert False

        return start_sequence, continue_sequence

    # pylint: enable=unused-argument

    def __insert_leading_whitespace_at_newlines(self, text_to_modify):
        """
        Deal with re-inserting any removed whitespace at the starts of lines.
        """
        if ParserHelper.newline_character in text_to_modify:
            owning_paragraph_token = None
            for search_index in range(len(self.block_stack) - 1, -1, -1):
                if (
                    self.block_stack[search_index].token_name
                    == MarkdownToken.token_paragraph
                ):
                    owning_paragraph_token = self.block_stack[search_index]
                    break

            print("text>before>" + ParserHelper.make_value_visible(text_to_modify))
            text_to_modify = ParserHelper.remove_backspaces_from_text(text_to_modify)
            text_to_modify = ParserHelper.resolve_replacement_markers_from_text(
                text_to_modify
            )
            print("text>after>" + ParserHelper.make_value_visible(text_to_modify))

            split_text_to_modify = text_to_modify.split(ParserHelper.newline_character)
            if owning_paragraph_token:
                split_parent_whitespace = owning_paragraph_token.extracted_whitespace.split(
                    ParserHelper.newline_character
                )
                print(
                    "owning_paragraph_token>>>>>>>"
                    + ParserHelper.make_value_visible(owning_paragraph_token)
                )
                print(
                    "opt>>rehydrate_index>"
                    + str(owning_paragraph_token.rehydrate_index)
                )
                print("opt>>ws>" + str(split_parent_whitespace))
            print("opt>>text>" + ParserHelper.make_value_visible(split_text_to_modify))

            for modify_index in range(1, len(split_text_to_modify)):
                print("-->" + str(modify_index))
                paragraph_whitespace = ""
                if owning_paragraph_token:
                    paragraph_whitespace = split_parent_whitespace[
                        modify_index + owning_paragraph_token.rehydrate_index
                    ]
                split_text_to_modify[modify_index] = (
                    paragraph_whitespace + split_text_to_modify[modify_index]
                )

            print("opt>>text>" + ParserHelper.make_value_visible(split_text_to_modify))
            took_lines = len(split_text_to_modify) - 1
            if owning_paragraph_token:
                owning_paragraph_token.rehydrate_index += took_lines
            print("opt>>took>" + str(took_lines))
            text_to_modify = ParserHelper.newline_character.join(split_text_to_modify)
            print("opt>>text>" + ParserHelper.make_value_visible(text_to_modify))
        return text_to_modify

    # pylint: disable=unused-argument
    def __rehydrate_inline_image(self, current_token, previous_token):
        """
        Rehydrate the image text from the token.
        """

        if self.block_stack[-1].token_name == MarkdownToken.token_inline_link:
            return ""
        rehydrated_text = LinkHelper.rehydrate_inline_image_text_from_token(
            current_token
        )
        return self.__insert_leading_whitespace_at_newlines(rehydrated_text)

    # pylint: enable=unused-argument

    # pylint: disable=unused-argument
    def __rehydrate_inline_link(self, current_token, previous_token):
        """
        Rehydrate the start of the link from the token.
        """

        self.block_stack.append(current_token)
        rehydrated_text = LinkHelper.rehydrate_inline_link_text_from_token(
            current_token
        )
        return self.__insert_leading_whitespace_at_newlines(rehydrated_text)

    # pylint: enable=unused-argument

    # pylint: disable=unused-argument
    def __rehydrate_inline_link_end(self, current_token, previous_token, next_token):
        """
        Rehydrate the end of the link from the token.
        """
        del self.block_stack[-1]
        return ""

    # pylint: enable=unused-argument

    # pylint: disable=unused-argument
    @classmethod
    def __rehydrate_link_reference_definition(cls, current_token, previous_token):
        """
        Rehydrate the link reference definition from the token.
        """
        if current_token.link_name_debug:
            link_name = current_token.link_name_debug
        else:
            link_name = current_token.link_name

        if current_token.link_destination_raw:
            link_destination = current_token.link_destination_raw
        else:
            link_destination = current_token.link_destination

        if current_token.link_title_raw:
            link_title = current_token.link_title_raw
        else:
            link_title = current_token.link_title

        return (
            current_token.extracted_whitespace
            + "["
            + link_name
            + "]:"
            + current_token.link_destination_whitespace
            + link_destination
            + current_token.link_title_whitespace
            + link_title
            + current_token.end_whitespace
            + ParserHelper.newline_character
        )

    # pylint: enable=unused-argument

    # pylint: disable=unused-argument
    def __rehydrate_atx_heading(self, current_token, previous_token):
        """
        Rehydrate the atx heading block from the token.
        """
        self.block_stack.append(current_token)
        return current_token.extracted_whitespace + ParserHelper.repeat_string(
            "#", current_token.hash_count
        )

    # pylint: enable=unused-argument

    # pylint: disable=unused-argument
    def __rehydrate_atx_heading_end(self, current_token, previous_token, next_token):
        """
        Rehydrate the end of the atx heading block from the token.
        """
        del self.block_stack[-1]
        trailing_hashes = ""
        if current_token.start_markdown_token.remove_trailing_count:
            trailing_hashes = ParserHelper.repeat_string(
                "#", current_token.start_markdown_token.remove_trailing_count
            )

        return (
            current_token.extra_end_data
            + trailing_hashes
            + current_token.extracted_whitespace
            + ParserHelper.newline_character
        )

    # pylint: enable=unused-argument

    # pylint: disable=unused-argument
    def __rehydrate_setext_heading(self, current_token, previous_token):
        """
        Rehydrate the setext heading from the token.
        """
        self.block_stack.append(current_token)
        return current_token.extracted_whitespace

    # pylint: enable=unused-argument

    # pylint: disable=unused-argument
    def __rehydrate_setext_heading_end(self, current_token, previous_token, next_token):
        """
        Rehydrate the end of the setext heading block from the token.
        """
        heading_character = self.block_stack[-1].heading_character
        heading_character_count = self.block_stack[-1].heading_character_count
        final_whitespace = self.block_stack[-1].final_whitespace
        del self.block_stack[-1]
        return (
            final_whitespace
            + ParserHelper.newline_character
            + current_token.extracted_whitespace
            + ParserHelper.repeat_string(heading_character, heading_character_count)
            + current_token.extra_end_data
            + ParserHelper.newline_character
        )

    # pylint: enable=unused-argument

    # pylint: disable=unused-argument
    def __rehydrate_text(self, current_token, previous_token):
        """
        Rehydrate the text from the token.
        """

        if (
            self.block_stack[-1].token_name == MarkdownToken.token_inline_link
            or self.block_stack[-1].token_name == MarkdownToken.token_inline_image
        ):
            return ""

        prefix_text = ""
        print(
            ">>rehydrate_text>>"
            + ParserHelper.make_value_visible(current_token.token_text)
        )
        main_text = ParserHelper.remove_backspaces_from_text(current_token.token_text)

        print(">>rehydrate_text>>" + ParserHelper.make_value_visible(main_text))
        main_text = ParserHelper.resolve_replacement_markers_from_text(main_text)
        main_text = ParserHelper.remove_escapes_from_text(main_text)
        print("<<rehydrate_text>>" + ParserHelper.make_value_visible(main_text))

        print(
            "<<leading_whitespace>>"
            + ParserHelper.make_value_visible(current_token.extracted_whitespace)
        )
        leading_whitespace = ParserHelper.resolve_replacement_markers_from_text(
            current_token.extracted_whitespace
        )
        leading_whitespace = ParserHelper.remove_escapes_from_text(leading_whitespace)
        print(
            "<<leading_whitespace>>"
            + ParserHelper.make_value_visible(leading_whitespace)
        )
        if self.block_stack:
            if (
                self.block_stack[-1].token_name
                == MarkdownToken.token_indented_code_block
            ):
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
            elif self.block_stack[-1].token_name == MarkdownToken.token_html_block:
                main_text += ParserHelper.newline_character
            elif self.block_stack[-1].token_name == MarkdownToken.token_paragraph:
                main_text = self.__reconstitute_paragraph_text(main_text, current_token)
            elif self.block_stack[-1].token_name == MarkdownToken.token_setext_heading:
                main_text = self.__reconstitute_setext_text(main_text, current_token)

        print(
            "<<prefix_text>>"
            + ParserHelper.make_value_visible(prefix_text)
            + "<<leading_whitespace>>"
            + ParserHelper.make_value_visible(leading_whitespace)
            + "<<main_text>>"
            + ParserHelper.make_value_visible(main_text)
            + "<<"
        )
        return prefix_text + leading_whitespace + main_text

    # pylint: enable=unused-argument

    # pylint: disable=unused-argument
    def __rehydrate_hard_break(self, current_token, previous_token):
        """
        Rehydrate the hard break text from the token.
        """
        if self.block_stack[-1].token_name == MarkdownToken.token_inline_link:
            return ""

        return current_token.line_end

    # pylint: enable=unused-argument

    # pylint: disable=unused-argument
    def __rehydrate_inline_emphaisis(self, current_token, previous_token):
        """
        Rehydrate the emphasis text from the token.
        """
        if self.block_stack[-1].token_name == MarkdownToken.token_inline_link:
            return ""

        return ParserHelper.repeat_string(
            current_token.emphasis_character, current_token.emphasis_length
        )

    # pylint: enable=unused-argument

    # pylint: disable=unused-argument
    def __rehydrate_inline_emphaisis_end(
        self, current_token, previous_token, next_token
    ):
        """
        Rehydrate the emphasis end text from the token.
        """
        if self.block_stack[-1].token_name == MarkdownToken.token_inline_link:
            return ""

        print(".extra_end_data>>" + str(current_token.extra_end_data))
        split_end_data = current_token.extra_end_data.split(":")
        emphasis_length = int(split_end_data[0])
        emphasis_character = split_end_data[1]
        return ParserHelper.repeat_string(emphasis_character, emphasis_length)

    # pylint: enable=unused-argument

    # pylint: disable=unused-argument
    def __rehydrate_inline_uri_autolink(self, current_token, previous_token):
        """
        Rehydrate the uri autolink from the token.
        """
        if self.block_stack[-1].token_name == MarkdownToken.token_inline_link:
            return ""
        return "<" + current_token.autolink_text + ">"

    # pylint: enable=unused-argument

    # pylint: disable=unused-argument
    def __rehydrate_inline_email_autolink(self, current_token, previous_token):
        """
        Rehydrate the email autolink from the token.
        """
        if self.block_stack[-1].token_name == MarkdownToken.token_inline_link:
            return ""
        return "<" + current_token.autolink_text + ">"

    # pylint: enable=unused-argument

    # pylint: disable=unused-argument
    def __rehydrate_inline_raw_html(self, current_token, previous_token):
        """
        Rehydrate the email raw html from the token.
        """
        if self.block_stack[-1].token_name == MarkdownToken.token_inline_link:
            return ""
        return "<" + current_token.raw_tag + ">"

    # pylint: enable=unused-argument

    # pylint: disable=unused-argument
    def __rehydrate_inline_code_span(self, current_token, previous_token):
        """
        Rehydrate the code span data from the token.
        """
        if self.block_stack[-1].token_name == MarkdownToken.token_inline_link:
            return ""

        span_text = ParserHelper.resolve_replacement_markers_from_text(
            current_token.span_text
        )
        span_text = ParserHelper.remove_escapes_from_text(span_text)
        leading_whitespace = ParserHelper.resolve_replacement_markers_from_text(
            current_token.leading_whitespace
        )
        trailing_whitespace = ParserHelper.resolve_replacement_markers_from_text(
            current_token.trailing_whitespace
        )
        return (
            current_token.extracted_start_backticks
            + leading_whitespace
            + span_text
            + trailing_whitespace
            + current_token.extracted_start_backticks
        )

    # pylint: enable=unused-argument

    # pylint: disable=unused-argument
    @classmethod
    def __rehydrate_thematic_break(cls, current_token, previous_token):
        """
        Rehydrate the thematic break text from the token.
        """
        return (
            current_token.extracted_whitespace
            + current_token.rest_of_line
            + ParserHelper.newline_character
        )

    # pylint: enable=unused-argument

    def __reconstitute_paragraph_text(self, main_text, current_token):
        """
        For a paragraph block, figure out the text that got us here.
        """
        if ParserHelper.newline_character in main_text:
            split_token_text = main_text.split(ParserHelper.newline_character)
            split_parent_whitespace_text = self.block_stack[
                -1
            ].extracted_whitespace.split(ParserHelper.newline_character)
            print(
                ">>split_token_text>>"
                + ParserHelper.make_value_visible(split_token_text)
            )
            print(
                ">>split_parent_whitespace_text>>"
                + ParserHelper.make_value_visible(split_parent_whitespace_text)
            )

            parent_rehydrate_index = self.block_stack[-1].rehydrate_index
            rejoined_token_text = []
            for iterator in enumerate(split_token_text, start=0):
                print(">>" + str(iterator))
                if iterator[0] == 0:
                    joined_text = iterator[1]
                else:
                    joined_text = (
                        split_parent_whitespace_text[
                            parent_rehydrate_index + iterator[0]
                        ]
                        + iterator[1]
                    )
                    self.block_stack[-1].rehydrate_index += 1
                rejoined_token_text.append(joined_text)
            split_token_text = rejoined_token_text

            if current_token.end_whitespace:
                split_end_whitespace_text = current_token.end_whitespace.split(
                    ParserHelper.newline_character
                )
                print(
                    ">>split_end_whitespace_text>>"
                    + ParserHelper.make_value_visible(split_end_whitespace_text)
                )
                assert len(split_token_text) == len(split_end_whitespace_text)

                joined_token_text = []
                for iterator in enumerate(split_token_text):
                    print(">>" + str(iterator))
                    joined_text = iterator[1] + split_end_whitespace_text[iterator[0]]
                    joined_token_text.append(joined_text)
                split_token_text = joined_token_text
            main_text = ParserHelper.newline_character.join(split_token_text)
        return main_text

    @classmethod
    def __reconstitute_indented_text(
        cls, main_text, prefix_text, indented_whitespace, leading_whitespace
    ):
        """
        For an indented code block, figure out the text that got us here.
        """
        print(
            "prefix_text>>"
            + str(len(prefix_text))
            + ">>"
            + ParserHelper.make_value_visible(prefix_text)
            + ">>"
        )
        print(
            "leading_whitespace>>"
            + str(len(leading_whitespace))
            + ">>"
            + ParserHelper.make_value_visible(leading_whitespace)
            + ">>"
        )
        split_main_text = main_text.split(ParserHelper.newline_character)
        print(
            "split_main_text>>"
            + ParserHelper.make_value_visible(split_main_text)
            + ">>"
        )
        print(
            "indented_whitespace>>"
            + ParserHelper.make_value_visible(indented_whitespace)
            + ">>"
        )
        split_indented_whitespace = (
            prefix_text + leading_whitespace + indented_whitespace
        ).split(ParserHelper.newline_character)
        print(
            "split_indented_whitespace>>"
            + ParserHelper.make_value_visible(split_indented_whitespace)
            + ">>"
        )
        assert len(split_main_text) == len(split_indented_whitespace)

        recombined_text = ""
        for iterator in enumerate(split_main_text):
            recombined_text += (
                split_indented_whitespace[iterator[0]]
                + iterator[1]
                + ParserHelper.newline_character
            )

        print("<<" + ParserHelper.make_value_visible(recombined_text) + ">>")
        return recombined_text, "", ""

    @classmethod
    def __reconstitute_setext_text(cls, main_text, current_token):
        """
        For a setext heading block, figure out the text that got us here.
        """

        if ParserHelper.newline_character in main_text:
            split_token_text = main_text.split(ParserHelper.newline_character)
            split_parent_whitespace_text = current_token.end_whitespace.split(
                ParserHelper.newline_character
            )
            print(
                ">>split_token_text>>"
                + ParserHelper.make_value_visible(split_token_text)
            )
            print(
                ">>split_parent_whitespace_text>>"
                + ParserHelper.make_value_visible(split_parent_whitespace_text)
            )

            rejoined_token_text = []
            for iterator in enumerate(split_token_text, start=0):
                print(">>iterator=" + str(iterator))
                split_setext_text = []
                ws_prefix_text = ""
                ws_suffix_text = ""
                if split_parent_whitespace_text[iterator[0]]:
                    split_setext_text = split_parent_whitespace_text[iterator[0]].split(
                        ParserHelper.whitespace_split_character
                    )
                    print(">>split_setext_text=" + str(split_setext_text))
                    if len(split_setext_text) == 1:
                        if iterator[0] == 0:
                            ws_suffix_text = split_setext_text[0]
                        else:
                            ws_prefix_text = split_setext_text[0]
                    else:
                        assert len(split_setext_text) == 2
                        ws_prefix_text = split_setext_text[0]
                        ws_suffix_text = split_setext_text[1]

                joined_text = ws_prefix_text + iterator[1] + ws_suffix_text
                rejoined_token_text.append(joined_text)

            print(">>rejoined_token_text=" + str(rejoined_token_text))
            main_text = ParserHelper.newline_character.join(rejoined_token_text)
        return main_text
