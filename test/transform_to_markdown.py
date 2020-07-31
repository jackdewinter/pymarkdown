"""
Module to provide for a transformation from tokens to a markdown document.
"""
import os

from pymarkdown.inline_helper import InlineHelper
from pymarkdown.link_helper import LinkHelper
from pymarkdown.markdown_token import EndMarkdownToken, MarkdownToken


# pylint: disable=too-many-public-methods
class TransformToMarkdown:
    """
    Class to provide for a transformation from tokens to a markdown document.
    """

    def __init__(self):
        """
        Initializes a new instance of the TransformToMarkdown class.
        """
        self.block_stack = []

        # TODO do I still need this?
        resource_path = None
        if not resource_path:
            resource_path = os.path.join(
                os.path.split(__file__)[0], "../pymarkdown/resources"
            )
        InlineHelper.initialize(resource_path)

    # pylint: disable=too-many-boolean-expressions
    # pylint: disable=too-many-branches
    # pylint: disable=too-many-statements
    def transform(self, actual_tokens):  # noqa: C901
        """
        Transform the incoming token stream back into Markdown.
        """
        transformed_data = ""
        avoid_processing = False
        previous_token = None

        for next_token in actual_tokens:
            # pre_transform = transformed_data
            if next_token.token_name == MarkdownToken.token_thematic_break:
                transformed_data += self.rehydrate_thematic_break(next_token)
            elif next_token.token_name == MarkdownToken.token_paragraph:
                transformed_data += self.rehydrate_paragraph(next_token)
            elif next_token.token_name == MarkdownToken.token_indented_code_block:
                transformed_data += self.rehydrate_indented_code_block(next_token)
            elif next_token.token_name == MarkdownToken.token_html_block:
                transformed_data += self.rehydrate_html_block(next_token)
            elif next_token.token_name == MarkdownToken.token_fenced_code_block:
                transformed_data += self.rehydrate_fenced_code_block(next_token)
            elif next_token.token_name == MarkdownToken.token_text:
                transformed_data += self.rehydrate_text(next_token)
            elif next_token.token_name == MarkdownToken.token_setext_heading:
                transformed_data += self.rehydrate_setext_heading(next_token)
            elif next_token.token_name == MarkdownToken.token_atx_heading:
                transformed_data += self.rehydrate_atx_heading(next_token)
            elif next_token.token_name == MarkdownToken.token_blank_line:
                transformed_data += self.rehydrate_blank_line(next_token)
            elif next_token.token_name == MarkdownToken.token_link_reference_definition:
                transformed_data += self.rehydrate_link_reference_definition(next_token)
            elif next_token.token_name == MarkdownToken.token_inline_link:
                transformed_data += self.rehydrate_inline_link(next_token)
            elif next_token.token_name == MarkdownToken.token_inline_image:
                transformed_data += self.rehydrate_inline_image(next_token)

            elif (
                next_token.token_name == MarkdownToken.token_unordered_list_start
                or next_token.token_name == MarkdownToken.token_ordered_list_start
                or next_token.token_name == MarkdownToken.token_block_quote
            ):
                avoid_processing = True
                break
            elif next_token.token_name == MarkdownToken.token_inline_hard_break:
                transformed_data += self.rehydrate_hard_break(next_token)
            elif next_token.token_name == MarkdownToken.token_inline_emphasis:
                transformed_data += self.rehydrate_inline_emphaisis(next_token)
            elif next_token.token_name == MarkdownToken.token_inline_uri_autolink:
                transformed_data += self.rehydrate_inline_uri_autolink(next_token)
            elif next_token.token_name == MarkdownToken.token_inline_email_autolink:
                transformed_data += self.rehydrate_inline_email_autolink(next_token)
            elif next_token.token_name == MarkdownToken.token_inline_raw_html:
                transformed_data += self.rehydrate_inline_raw_html(next_token)
            elif next_token.token_name == MarkdownToken.token_inline_code_span:
                transformed_data += self.rehydrate_inline_code_span(next_token)
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
                elif adjusted_token_name == MarkdownToken.token_fenced_code_block:
                    transformed_data += self.rehydrate_fenced_code_block_end(
                        next_token, previous_token
                    )
                elif adjusted_token_name == MarkdownToken.token_html_block:
                    transformed_data += self.rehydrate_html_block_end(next_token)
                elif adjusted_token_name == MarkdownToken.token_setext_heading:
                    transformed_data += self.rehydrate_setext_heading_end(next_token)
                elif adjusted_token_name == MarkdownToken.token_atx_heading:
                    transformed_data += self.rehydrate_atx_heading_end(next_token)
                elif adjusted_token_name == MarkdownToken.token_inline_emphasis:
                    transformed_data += self.rehydrate_inline_emphaisis_end(next_token)
                elif adjusted_token_name == MarkdownToken.token_inline_link:
                    transformed_data += self.rehydrate_inline_link_end(next_token)
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
            previous_token = next_token

        if transformed_data and transformed_data[-1] == "\n":
            transformed_data = transformed_data[0:-1]
        return transformed_data, avoid_processing

    # pylint: enable=too-many-boolean-expressions
    # pylint: enable=too-many-branches
    # pylint: enable=too-many-statements

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

    def rehydrate_html_block(self, next_token):
        """
        Rehydrate the html block from the token.
        """
        self.block_stack.append(next_token)
        return ""

    def rehydrate_html_block_end(self, next_token):
        """
        Rehydrate the end of the html block from the token.
        """
        assert next_token
        del self.block_stack[-1]
        return ""

    def rehydrate_fenced_code_block(self, next_token):
        """
        Rehydrate the fenced code block from the token.
        """
        self.block_stack.append(next_token)

        info_text = next_token.extracted_whitespace_before_info_string
        if next_token.pre_extracted_text:
            info_text += next_token.pre_extracted_text
        else:
            info_text += next_token.extracted_text
        if next_token.pre_text_after_extracted_text:
            info_text += next_token.pre_text_after_extracted_text
        else:
            info_text += next_token.text_after_extracted_text

        return (
            next_token.extracted_whitespace
            + "".rjust(next_token.fence_count, next_token.fence_character)
            + info_text
            + "\n"
        )

    def rehydrate_fenced_code_block_end(self, next_token, previous_token):
        """
        Rehydrate the end of the fenced code block from the token.
        """
        start_token = next_token.start_markdown_token

        if next_token.extra_data:
            split_extra_data = next_token.extra_data.split(":")
            assert len(split_extra_data) == 2
            fence_count = int(split_extra_data[1])

            prefix_whitespace = "\n"
            if previous_token.is_blank_line or previous_token.is_fenced_code_block:
                prefix_whitespace = ""
            prefix_whitespace += next_token.extracted_whitespace

            del self.block_stack[-1]
            return (
                prefix_whitespace
                + "".rjust(fence_count, start_token.fence_character)
                + "\n"
            )
        return ""

    def __insert_leading_whitespace_at_newlines(self, text_to_modify):
        """
        Deal with re-inserting any removed whitespace at the starts of lines.
        """
        if "\n" in text_to_modify:
            owning_paragraph_token = None
            for search_index in range(len(self.block_stack) - 1, -1, -1):
                if (
                    self.block_stack[search_index].token_name
                    == MarkdownToken.token_paragraph
                ):
                    owning_paragraph_token = self.block_stack[search_index]
                    break

            split_text_to_modify = text_to_modify.split("\n")
            split_parent_whitespace = owning_paragraph_token.extracted_whitespace.split(
                "\n"
            )
            print(
                "owning_paragraph_token>>>>>>>"
                + str(owning_paragraph_token).replace("\n", "\\n")
            )
            print("opt>>text>" + str(split_text_to_modify).replace("\n", "\\n"))
            print("opt>>ws>" + str(split_parent_whitespace))
            print("opt>>rehydrate_index>" + str(owning_paragraph_token.rehydrate_index))

            for modify_index in range(1, len(split_text_to_modify)):
                print("-->" + str(modify_index))
                split_text_to_modify[modify_index] = (
                    split_parent_whitespace[
                        modify_index + owning_paragraph_token.rehydrate_index
                    ]
                    + split_text_to_modify[modify_index]
                )

            print("opt>>text>" + str(split_text_to_modify).replace("\n", "\\n"))
            took_lines = len(split_text_to_modify) - 1
            owning_paragraph_token.rehydrate_index += took_lines
            print("opt>>took>" + str(took_lines))
            text_to_modify = "\n".join(split_text_to_modify)
            print("opt>>text>" + str(text_to_modify).replace("\n", "\\n"))
        return text_to_modify

    def rehydrate_inline_image(self, next_token):
        """
        Rehydrate the image text from the token.
        """

        if self.block_stack[-1].token_name == MarkdownToken.token_inline_link:
            return ""
        rehydrated_text = LinkHelper.rehydrate_inline_image_text_from_token(next_token)
        return self.__insert_leading_whitespace_at_newlines(rehydrated_text)

    def rehydrate_inline_link(self, next_token):
        """
        Rehydrate the start of the link from the token.
        """

        self.block_stack.append(next_token)
        rehydrated_text = LinkHelper.rehydrate_inline_link_text_from_token(next_token)
        return self.__insert_leading_whitespace_at_newlines(rehydrated_text)

    def rehydrate_inline_link_end(self, next_token):
        """
        Rehydrate the end of the link from the token.
        """

        assert next_token
        del self.block_stack[-1]
        return ""

    @classmethod
    def rehydrate_link_reference_definition(cls, next_token):
        """
        Rehydrate the link reference definition from the token.
        """

        if next_token.link_name_debug:
            link_name = next_token.link_name_debug
        else:
            link_name = next_token.link_name

        if next_token.link_destination_raw:
            link_destination = next_token.link_destination_raw
        else:
            link_destination = next_token.link_destination

        if next_token.link_title_raw:
            link_title = next_token.link_title_raw
        else:
            link_title = next_token.link_title

        return (
            next_token.extracted_whitespace
            + "["
            + link_name
            + "]:"
            + next_token.link_destination_whitespace
            + link_destination
            + next_token.link_title_whitespace
            + link_title
            + next_token.end_whitespace
            + "\n"
        )

    def rehydrate_atx_heading(self, next_token):
        """
        Rehydrate the atx heading block from the token.
        """

        self.block_stack.append(next_token)
        return next_token.extracted_whitespace + "".rjust(next_token.hash_count, "#")

    def rehydrate_atx_heading_end(self, next_token):
        """
        Rehydrate the end of the atx heading block from the token.
        """

        del self.block_stack[-1]
        trailing_hashes = ""
        if next_token.start_markdown_token.remove_trailing_count:
            trailing_hashes = "".rjust(
                next_token.start_markdown_token.remove_trailing_count, "#"
            )

        return (
            next_token.extra_end_data
            + trailing_hashes
            + next_token.extracted_whitespace
            + "\n"
        )

    def rehydrate_setext_heading(self, next_token):
        """
        Rehydrate the setext heading from the token.
        """
        self.block_stack.append(next_token)
        return next_token.extracted_whitespace

    def rehydrate_setext_heading_end(self, next_token):
        """
        Rehydrate the end of the setext heading block from the token.
        """
        heading_character = self.block_stack[-1].heading_character
        heading_character_count = self.block_stack[-1].heading_character_count
        final_whitespace = self.block_stack[-1].final_whitespace
        del self.block_stack[-1]
        return (
            final_whitespace
            + "\n"
            + next_token.extracted_whitespace
            + "".rjust(heading_character_count, heading_character)
            + next_token.extra_end_data
            + "\n"
        )

    # pylint: disable=too-many-locals
    # pylint: disable=too-many-statements
    # pylint: disable=too-many-branches
    # pylint: disable=too-many-nested-blocks
    def rehydrate_text(self, next_token):
        """
        Rehydrate the text from the token.
        """

        if (
            self.block_stack[-1].token_name == MarkdownToken.token_inline_link
            or self.block_stack[-1].token_name == MarkdownToken.token_inline_image
        ):
            return ""

        prefix_text = ""
        main_text = next_token.token_text.replace(
            InlineHelper.backspace_character, ""
        ).replace("\x08", "")

        print(
            ">>rehydrate_text>>" + main_text.replace("\a", "\\a").replace("\n", "\\n")
        )
        main_text = self.resolve_replacement_markers(main_text)
        print(
            "<<rehydrate_text>>" + main_text.replace("\a", "\\a").replace("\n", "\\n")
        )

        print(
            "<<leading_whitespace>>"
            + next_token.extracted_whitespace.replace("\a", "\\a")
            .replace("\n", "\\n")
            .replace("\x03", "\\x03")
        )
        leading_whitespace = self.resolve_replacement_markers(
            next_token.extracted_whitespace
        )
        print(
            "<<leading_whitespace>>"
            + leading_whitespace.replace("\a", "\\a")
            .replace("\n", "\\n")
            .replace("\x03", "\\x03")
        )
        if self.block_stack:
            if (
                self.block_stack[-1].token_name
                == MarkdownToken.token_indented_code_block
            ):
                main_text = self.reconstitute_indented_text(
                    main_text,
                    self.block_stack[-1].extracted_whitespace,
                    self.block_stack[-1].indented_whitespace,
                    leading_whitespace,
                )
                prefix_text = ""
                leading_whitespace = ""
            elif self.block_stack[-1].token_name == MarkdownToken.token_html_block:
                main_text += "\n"
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

                        joined_token_text = []
                        for iterator in enumerate(split_token_text):
                            print(">>" + str(iterator))
                            joined_text = (
                                iterator[1] + split_end_whitespace_text[iterator[0]]
                            )
                            joined_token_text.append(joined_text)
                        split_token_text = joined_token_text
                    main_text = "\n".join(split_token_text)
            elif self.block_stack[-1].token_name == MarkdownToken.token_setext_heading:
                if "\n" in main_text:
                    split_token_text = main_text.split("\n")
                    split_parent_whitespace_text = next_token.end_whitespace.split("\n")
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
                    parent_rehydrate_index = 0  # self.block_stack[-1].rehydrate_index

                    rejoined_token_text = []
                    for iterator in enumerate(split_token_text, start=0):
                        print(">>iterator=" + str(iterator))
                        split_setext_text = []
                        ws_prefix_text = ""
                        ws_suffix_text = ""
                        if split_parent_whitespace_text[iterator[0]]:
                            split_setext_text = split_parent_whitespace_text[
                                iterator[0]
                            ].split("\x02")
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
                    main_text = "\n".join(rejoined_token_text)
        return prefix_text + leading_whitespace + main_text

    # pylint: enable=too-many-statements
    # pylint: enable=too-many-branches
    # pylint: enable=too-many-locals
    # pylint: enable=too-many-nested-blocks

    def rehydrate_hard_break(self, next_token):
        """
        Rehydrate the hard break text from the token.
        """
        if self.block_stack[-1].token_name == MarkdownToken.token_inline_link:
            return ""

        return next_token.line_end

    def rehydrate_inline_emphaisis(self, next_token):
        """
        Rehydrate the emphasis text from the token.
        """
        if self.block_stack[-1].token_name == MarkdownToken.token_inline_link:
            return ""

        return "".rjust(next_token.emphasis_length, next_token.emphasis_character)

    def rehydrate_inline_emphaisis_end(self, next_token):
        """
        Rehydrate the emphasis end text from the token.
        """
        if self.block_stack[-1].token_name == MarkdownToken.token_inline_link:
            return ""

        print(".extra_end_data>>" + str(next_token.extra_end_data))
        split_end_data = next_token.extra_end_data.split(":")
        emphasis_length = int(split_end_data[0])
        emphasis_character = split_end_data[1]
        return "".rjust(emphasis_length, emphasis_character)

    def rehydrate_inline_uri_autolink(self, next_token):
        """
        Rehydrate the uri autolink from the token.
        """
        if self.block_stack[-1].token_name == MarkdownToken.token_inline_link:
            return ""
        return "<" + next_token.autolink_text + ">"

    def rehydrate_inline_email_autolink(self, next_token):
        """
        Rehydrate the email autolink from the token.
        """
        if self.block_stack[-1].token_name == MarkdownToken.token_inline_link:
            return ""
        return "<" + next_token.autolink_text + ">"

    def rehydrate_inline_raw_html(self, next_token):
        """
        Rehydrate the email raw html from the token.
        """
        if self.block_stack[-1].token_name == MarkdownToken.token_inline_link:
            return ""
        return "<" + next_token.raw_tag + ">"

    def rehydrate_inline_code_span(self, next_token):
        """
        Rehydrate the code span data from the token.
        """
        if self.block_stack[-1].token_name == MarkdownToken.token_inline_link:
            return ""

        span_text = self.resolve_replacement_markers(next_token.span_text)
        leading_whitespace = self.resolve_replacement_markers(
            next_token.leading_whitespace
        )
        trailing_whitespace = self.resolve_replacement_markers(
            next_token.trailing_whitespace
        )
        return (
            next_token.extracted_start_backticks
            + leading_whitespace
            + span_text
            + trailing_whitespace
            + next_token.extracted_start_backticks
        )

    @classmethod
    def rehydrate_thematic_break(cls, next_token):
        """
        Rehydrate the thematic break text from the token.
        """
        return next_token.extracted_whitespace + next_token.rest_of_line + "\n"

    @classmethod
    def reconstitute_indented_text(
        cls, main_text, prefix_text, indented_whitespace, leading_whitespace
    ):
        """
        For an indented code block, figure out the text that got us here.
        """
        print(
            "\n\nprefix_text>>"
            + str(len(prefix_text))
            + ">>"
            + str(prefix_text).replace("\n", "\\n")
            + ">>"
        )
        print(
            "leading_whitespace>>"
            + str(len(leading_whitespace))
            + ">>"
            + str(leading_whitespace).replace("\n", "\\n")
            + ">>"
        )
        split_main_text = main_text.split("\n")
        print("split_main_text>>" + str(split_main_text).replace("\n", "\\n") + ">>")
        print(
            "indented_whitespace>>"
            + str(indented_whitespace).replace("\n", "\\n")
            + ">>"
        )
        split_indented_whitespace = (
            prefix_text + leading_whitespace + indented_whitespace
        ).split("\n")
        print(
            "split_indented_whitespace>>"
            + str(split_indented_whitespace).replace("\n", "\\n")
            + ">>"
        )
        assert len(split_main_text) == len(split_indented_whitespace)

        recombined_text = ""
        for iterator in enumerate(split_main_text):
            recombined_text += (
                split_indented_whitespace[iterator[0]] + iterator[1] + "\n"
            )

        print("<<" + recombined_text.replace("\n", "\\n") + ">>")
        return recombined_text

    @classmethod
    def resolve_replacement_markers(cls, main_text):
        """
        Resolve the alert characters (i.e. replacement markers) out of the text string.
        """

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
        return main_text


# pylint: enable=too-many-public-methods
