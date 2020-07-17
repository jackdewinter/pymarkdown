"""
Module to provide for a transformation from tokens to a markdown document.
"""
import os

from pymarkdown.inline_helper import InlineHelper
from pymarkdown.markdown_token import EndMarkdownToken, MarkdownToken


class TransformToMarkdown:
    """
    Class to provide for a transformation from tokens to a markdown document.
    """

    def __init__(self):
        """
        Initializes a new instance of the TransformToMarkdown class.
        """
        self.block_stack = []

        resource_path = None
        if not resource_path:
            resource_path = os.path.join(
                os.path.split(__file__)[0], "../pymarkdown/resources"
            )
        InlineHelper.initialize(resource_path)

    # pylint: disable=too-many-boolean-expressions
    # pylint: disable=too-many-branches
    def transform(self, actual_tokens):
        """
        Transform the incoming token stream back into Markdown.
        """
        transformed_data = ""
        avoid_processing = False

        for next_token in actual_tokens:
            # pre_transform = transformed_data
            if next_token.token_name == MarkdownToken.token_thematic_break:
                transformed_data += self.rehydrate_thematic_break(next_token)
            elif next_token.token_name == MarkdownToken.token_paragraph:
                transformed_data += self.rehydrate_paragraph(next_token)
            elif next_token.token_name == MarkdownToken.token_indented_code_block:
                transformed_data += self.rehydrate_indented_code_block(next_token)
            elif next_token.token_name == MarkdownToken.token_text:
                transformed_data += self.rehydrate_text(next_token)
            elif next_token.token_name == MarkdownToken.token_blank_line:
                transformed_data += self.rehydrate_blank_line(next_token)
            elif (
                next_token.token_name == MarkdownToken.token_unordered_list_start
                or next_token.token_name == MarkdownToken.token_ordered_list_start
                or next_token.token_name == MarkdownToken.token_block_quote
                or next_token.token_name == MarkdownToken.token_fenced_code_block
                or next_token.token_name == MarkdownToken.token_html_block
                or next_token.token_name == MarkdownToken.token_setext_heading
                or next_token.token_name == MarkdownToken.token_atx_heading
                or next_token.token_name
                == MarkdownToken.token_link_reference_definition
                or next_token.token_name == MarkdownToken.token_inline_code_span
                or next_token.token_name == MarkdownToken.token_inline_uri_autolink
                or next_token.token_name == MarkdownToken.token_inline_email_autolink
                or next_token.token_name == MarkdownToken.token_inline_raw_html
                or next_token.token_name == MarkdownToken.token_inline_link
                or next_token.token_name == MarkdownToken.token_inline_image
                or next_token.token_name == MarkdownToken.token_inline_emphasis
            ):
                avoid_processing = True
                break
            elif next_token.token_name == MarkdownToken.token_inline_hard_break:
                transformed_data += self.rehydrate_hard_break(next_token)
            elif next_token.token_name.startswith(EndMarkdownToken.type_name_prefix):

                adjusted_token_name = next_token.token_name[
                    len(EndMarkdownToken.type_name_prefix) :
                ]
                if adjusted_token_name == MarkdownToken.token_paragraph:
                    transformed_data += self.rehydrate_paragraph_end(next_token)
                elif adjusted_token_name == MarkdownToken.token_indented_code_block:
                    transformed_data += self.rehydrate_indented_code_block_end(
                        next_token
                    )
                else:
                    assert False, "end_next_token>>" + str(adjusted_token_name)
            else:
                assert False, "next_token>>" + str(next_token)

            print(
                ">>>>"
                + str(next_token)
                + "\n---\n"
                + transformed_data.replace("\n", "\\n").replace("\t", "\\t")
                + "\n---"
            )

        if transformed_data and transformed_data[-1] == "\n":
            transformed_data = transformed_data[0:-1]
        return transformed_data, avoid_processing

    # pylint: enable=too-many-boolean-expressions
    # pylint: enable=too-many-branches

    def rehydrate_paragraph(self, next_token):
        """
        Rehydrate the paragraph block from the token.
        """
        self.block_stack.append(next_token)
        next_token.rehydrate_index = 0
        extracted_whitespace = next_token.extracted_whitespace
        if "\n" in extracted_whitespace:
            line_end_index = extracted_whitespace.index("\n")
            extracted_whitespace = extracted_whitespace[0:line_end_index]
        return extracted_whitespace

    def rehydrate_paragraph_end(self, next_token):
        """
        Rehydrate the end of the paragraph block from the token.
        """
        assert next_token
        top_stack_token = self.block_stack[-1]
        del self.block_stack[-1]
        return top_stack_token.final_whitespace + "\n"

    @classmethod
    def rehydrate_blank_line(cls, next_token):
        """
        Rehydrate the blank line from the token.
        """
        return next_token.extracted_whitespace + "\n"

    def rehydrate_indented_code_block(self, next_token):
        """
        Rehydrate the indented code block from the token.
        """
        self.block_stack.append(next_token)
        return ""

    def rehydrate_indented_code_block_end(self, next_token):
        """
        Rehydrate the end of the indented code block from the token.
        """
        assert next_token
        del self.block_stack[-1]
        return ""

    # pylint: disable=consider-using-enumerate
    # pylint: disable=too-many-locals
    def rehydrate_text(self, next_token):
        """
        Rehydrate the text from the token.
        """
        prefix_text = ""
        main_text = next_token.token_text.replace(
            InlineHelper.backspace_character, ""
        ).replace("\x08", "")

        print(
            ">>rehydrate_text>>" + main_text.replace("\a", "\\a").replace("\n", "\\n")
        )
        while "\a" in main_text:
            start_replacement_index = main_text.index("\a")
            print(">>start_replacement_index>>" + str(start_replacement_index))
            middle_replacement_index = main_text.index(
                "\a", start_replacement_index + 1
            )
            print(">>middle_replacement_index>>" + str(middle_replacement_index))
            end_replacement_index = main_text.index("\a", middle_replacement_index + 1)
            print(">>end_replacement_index>>" + str(end_replacement_index))

            replace_text = main_text[
                start_replacement_index + 1 : middle_replacement_index
            ]

            # It is possible to have one level of nesting, so deal with it.
            if middle_replacement_index + 1 == end_replacement_index:
                inner_start_replacement_index = main_text.index(
                    "\a", end_replacement_index + 1
                )
                inner_middle_replacement_index = main_text.index(
                    "\a", inner_start_replacement_index + 1
                )
                inner_end_replacement_index = main_text.index(
                    "\a", inner_middle_replacement_index + 1
                )
                assert inner_middle_replacement_index + 1 == inner_end_replacement_index
                end_replacement_index = inner_end_replacement_index

            if start_replacement_index:
                main_text = (
                    main_text[0:start_replacement_index]
                    + replace_text
                    + main_text[end_replacement_index + 1 :]
                )
            else:
                main_text = replace_text + main_text[end_replacement_index + 1 :]
            print(
                ">>rehydrate_text>>"
                + str(len(main_text))
                + ">>"
                + main_text.replace("\a", "\\a").replace("\n", "\\n")
            )

        print(
            "<<rehydrate_text>>" + main_text.replace("\a", "\\a").replace("\n", "\\n")
        )

        leading_whitespace = next_token.extracted_whitespace
        if self.block_stack:
            if (
                self.block_stack[-1].token_name
                == MarkdownToken.token_indented_code_block
            ):
                main_text = self.reconstitute_indented_text(
                    main_text,
                    self.block_stack[-1].extracted_whitespace,
                    leading_whitespace,
                )
                prefix_text = ""
                leading_whitespace = ""
            elif self.block_stack[-1].token_name == MarkdownToken.token_paragraph:
                if "\n" in main_text:
                    split_token_text = main_text.split("\n")
                    split_parent_whitespace_text = self.block_stack[
                        -1
                    ].extracted_whitespace.split("\n")
                    print(
                        ">>split_token_text>>"
                        + str(split_token_text)
                        .replace("\n", "\\n")
                        .replace("\t", "\\t")
                    )
                    print(
                        ">>split_parent_whitespace_text>>"
                        + str(split_parent_whitespace_text)
                        .replace("\n", "\\n")
                        .replace("\t", "\\t")
                    )
                    # TODO never incrementing?
                    parent_rehydrate_index = self.block_stack[-1].rehydrate_index
                    for i in range(1, len(split_token_text)):
                        print(">>" + str(i))
                        joined_text = (
                            split_parent_whitespace_text[parent_rehydrate_index + i]
                            + split_token_text[i]
                        )
                        split_token_text[i] = joined_text
                    if next_token.end_whitespace:
                        split_end_whitespace_text = next_token.end_whitespace.split(
                            "\n"
                        )
                        print(
                            ">>split_end_whitespace_text>>"
                            + str(split_end_whitespace_text)
                            .replace("\n", "\\n")
                            .replace("\t", "\\t")
                        )
                        assert len(split_token_text) == len(split_end_whitespace_text)
                        for i in range(0, len(split_token_text)):
                            print(">>" + str(i))
                            joined_text = (
                                split_token_text[i] + split_end_whitespace_text[i]
                            )
                            split_token_text[i] = joined_text
                    main_text = "\n".join(split_token_text)
        return prefix_text + leading_whitespace + main_text

    # pylint: enable=consider-using-enumerate
    # pylint: enable=too-many-locals

    @classmethod
    def rehydrate_hard_break(cls, next_token):
        """
        Rehydrate the hard break text from the token.
        """
        return next_token.line_end

    @classmethod
    def rehydrate_thematic_break(cls, next_token):
        """
        Rehydrate the thematic break text from the token.
        """
        return next_token.extracted_whitespace + next_token.rest_of_line + "\n"

    @classmethod
    def reconstitute_indented_text(cls, main_text, prefix_text, leading_whitespace):
        """
        For an indented code block, figure out the text that got us here.
        """
        print(">>" + str(prefix_text) + ">>")
        split_main_text = main_text.split("\n")
        print(">>" + str(split_main_text) + ">>")
        recombined_text = ""
        for next_split in split_main_text:
            if next_split:
                recombined_text += prefix_text + leading_whitespace + next_split + "\n"
                leading_whitespace = ""
            else:
                recombined_text += next_split + "\n"
        print("<<" + recombined_text + ">>")
        return recombined_text
