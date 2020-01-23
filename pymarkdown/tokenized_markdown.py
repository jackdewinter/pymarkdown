# pylint: disable=too-many-lines
"""
Module to provide a tokenization of a markdown-encoded string.
"""
import string

from pymarkdown.html_helper import HtmlHelper
from pymarkdown.parser_helper import ParserHelper


# pylint: disable=too-many-public-methods
# pylint: disable=too-many-instance-attributes
class TokenizedMarkdown:
    """
    Class to provide a tokenization of a markdown-encoded string.
    """

    def __init__(self):
        """
        Initializes a new instance of the TokenizedMarkdown class.
        """
        self.tokenized_document = None
        self.stack = ["document"]

        self.ulist_start_characters = "-+*"
        self.olist_start_characters = ".)"
        self.block_quote_character = ">"

        self.atx_character = "#"
        self.html_block_start_character = "<"
        self.fenced_code_block_start_characters = "~`"
        self.thematic_break_characters = "*_-"
        self.setext_characters = "-="
        self.html_block_1_end_tags = ["</script>", "</pre>", "</style>"]
        self.html_block_6_start = [
            "address",
            "article",
            "aside",
            "base",
            "basefont",
            "blockquote",
            "body",
            "caption",
            "center",
            "col",
            "colgroup",
            "dd",
            "details",
            "dialog",
            "dir",
            "div",
            "dl",
            "dt",
            "fieldset",
            "figcaption",
            "figure",
            "footer",
            "form",
            "frame",
            "frameset",
            "h1",
            "h2",
            "h3",
            "h4",
            "h5",
            "h6",
            "head",
            "header",
            "hr",
            "html",
            "iframe",
            "legend",
            "li",
            "link",
            "main",
            "menu",
            "menuitem",
            "nav",
            "noframes",
            "ol",
            "optgroup",
            "option",
            "p",
            "param",
            "section",
            "source",
            "summary",
            "table",
            "tbody",
            "td",
            "tfoot",
            "th",
            "thead",
            "title",
            "tr",
            "track",
            "ul",
        ]

    def transform(self, your_text_string):
        """
        Transform a markdown-encoded string into an array of tokens.
        """

        self.tokenized_document = []
        next_token = your_text_string.split("\n", 1)
        print("---")
        while next_token:
            print("next-line>>" + str(next_token))
            print("stack>>" + str(self.stack))
            print("current_block>>" + self.stack[-1])
            print("---")

            next_line = next_token[0].replace("\t", "    ")
            tokens_from_line = []
            if not next_line or not next_line.strip():
                tokens_from_line = self.handle_blank_line(
                    next_line, from_main_transform=True
                )
            else:
                tokens_from_line, _ = self.parse_line_for_container_blocks(next_line)

            print("---")
            print("before>>" + str(self.tokenized_document))

            assert tokens_from_line
            self.tokenized_document.extend(tokens_from_line)
            print("after>>" + str(self.tokenized_document))
            print("---")

            if len(next_token) == 2:
                next_token = next_token[1].split("\n", 1)
            else:
                next_token = None

        print("cleanup")
        return self.close_open_blocks(
            self.tokenized_document, include_block_quotes=True, include_lists=True
        )

    # pylint: disable=too-many-arguments
    def close_open_blocks(
        self,
        destination_array=None,
        only_these_blocks=None,
        include_block_quotes=False,
        include_lists=False,
        until_me=-1,
    ):
        """
        Close any open blocks that are currently on the stack.
        """

        new_tokens = []
        if destination_array:
            new_tokens = destination_array

        while self.stack[-1] != "document":
            print("cob>>" + str(self.stack))
            if only_these_blocks and self.stack[-1] not in only_these_blocks:
                do_break = True
                print("cob>>not in only")
                if self.stack[-1].startswith("block-quote:"):
                    print("cob>>not in only - checking presence of BQ")
                    do_break = False
                    for next_block in only_these_blocks:
                        if next_block == "block-quote:":
                            do_break = True
                if do_break:
                    break
            if not include_block_quotes and (self.stack[-1].startswith("block-quote:")):
                print("cob>>not block quotes")
                break
            if not include_lists and (
                self.stack[-1].startswith("ulist") or self.stack[-1].startswith("olist")
            ):
                print("cob>>not lists")
                break
            if until_me != -1:
                print("NOT ME!!!!" + str(until_me) + "<<" + str(len(self.stack)) + "<<")
                if until_me >= len(self.stack):
                    break

            adjusted_tokens = self.remove_top_element_from_stack()
            new_tokens.extend(adjusted_tokens)
        return new_tokens
        # pylint: enable=too-many-arguments

    def remove_top_element_from_stack(self):
        """
        Once it is decided that we need to remove the top element from the stack,
        make sure to do it uniformly.
        """

        new_tokens = []
        print("cob->te->" + str(self.stack[-1]))
        extra_elements = []
        if self.stack[-1] == "icode-block":
            while self.tokenized_document[-1].startswith("[BLANK"):
                last_element = self.tokenized_document[-1]
                extra_elements.append(last_element)
                del self.tokenized_document[-1]

        if self.stack[-1].startswith("fcode-block"):
            new_tokens.append("[end-fcode-block:]")
        elif self.stack[-1].startswith("html-block"):
            new_tokens.append("[end-html-block]")
        elif self.stack[-1].startswith("ulist"):
            new_tokens.append("[end-ulist]")
        elif self.stack[-1].startswith("olist"):
            new_tokens.append("[end-olist]")
        elif self.stack[-1].startswith("block-quote"):
            new_tokens.append("[end-block-quote]")
        else:
            new_tokens.append("[end-" + self.stack[-1] + "]")
        new_tokens.extend(extra_elements)
        del self.stack[-1]
        return new_tokens

    def handle_blank_line(self, input_line, from_main_transform):
        """
        Handle the processing of a blank line.
        """

        if (
            self.stack[-1] == "para"
            and len(self.stack) >= 2
            and (
                self.stack[-2].startswith("ulist") or self.stack[-2].startswith("olist")
            )
        ):
            from_main_transform = False
        elif self.stack[-1].startswith("ulist") or self.stack[-1].startswith("olist"):
            from_main_transform = False

        close_only_these_blocks = None
        do_include_block_quotes = True
        if not from_main_transform:
            close_only_these_blocks = ["para"]
            do_include_block_quotes = False
        print("from_main_transform>>" + str(from_main_transform))
        print("close_only_these_blocks>>" + str(close_only_these_blocks))
        print("do_include_block_quotes>>" + str(do_include_block_quotes))

        non_whitespace_index, extracted_whitespace = ParserHelper.extract_whitespace(
            input_line, 0
        )

        is_processing_list, in_index = self.check_for_list_in_process()
        print(
            "is_processing_list>>"
            + str(is_processing_list)
            + ">>in_index>>"
            + str(in_index)
        )

        new_tokens = None
        if self.stack[-1] == "icode-block" or self.stack[-1].startswith("fcode-block:"):
            stack_bq_count = self.__count_of_block_quotes_on_stack()
            if stack_bq_count:
                print("hbl>>code block within block quote")
            else:
                print("hbl>>code block")
                new_tokens = []
        elif self.stack[-1].startswith("html-block:"):
            new_tokens = self.check_blank_html_block_end()
        elif is_processing_list:
            print("tokenized_document-1>>" + self.tokenized_document[-1])
            print("tokenized_document-2>>" + self.tokenized_document[-2])
            if self.tokenized_document[-1].startswith("[BLANK:") and (
                self.tokenized_document[-2].startswith("[ulist:")
                or self.tokenized_document[-2].startswith("[olist:")
            ):
                print("double blank in list")
                new_tokens = self.close_open_blocks(
                    until_me=in_index, include_lists=True
                )

        if new_tokens is None:
            new_tokens = self.close_open_blocks(
                only_these_blocks=close_only_these_blocks,
                include_block_quotes=do_include_block_quotes,
            )

        print("new_tokens>>" + str(new_tokens))
        assert non_whitespace_index == len(input_line)
        new_tokens.append("[BLANK:" + extracted_whitespace + "]")
        return new_tokens

    def parse_indented_code_block(
        self, line_to_parse, start_index, extracted_whitespace
    ):
        """
        Handle the parsing of an indented code block
        """

        new_tokens = []

        if len(extracted_whitespace) >= 4 and self.stack[-1] != "para":
            if self.stack[-1] != "icode-block":
                self.stack.append("icode-block")
                new_tokens.append("[icode-block:    ]")
                extracted_whitespace = "".rjust(len(extracted_whitespace) - 4)
            new_tokens.append(
                "[text:"
                + line_to_parse[start_index:]
                + ":"
                + extracted_whitespace
                + "]"
            )
        return new_tokens

    def is_fenced_code_block(
        self,
        line_to_parse,
        start_index,
        extracted_whitespace,
        skip_whitespace_check=False,
    ):
        """
        Determine if we have the start of a fenced code block.
        """

        if (
            len(extracted_whitespace) <= 3 or skip_whitespace_check
        ) and ParserHelper.is_character_at_index_one_of(
            line_to_parse, start_index, self.fenced_code_block_start_characters
        ):
            print(
                "ifcb:collected_count>>"
                + line_to_parse
                + "<<"
                + str(start_index)
                + "<<"
            )
            collected_count, new_index = ParserHelper.collect_while_character(
                line_to_parse, start_index, line_to_parse[start_index]
            )
            print("ifcb:collected_count:" + str(collected_count))
            (
                non_whitespace_index,
                extracted_whitespace_before_info_string,
            ) = ParserHelper.extract_whitespace(line_to_parse, new_index)

            non_whitespace_index_character = None
            if non_whitespace_index < len(line_to_parse):
                non_whitespace_index_character = line_to_parse[non_whitespace_index]

            if collected_count >= 3 and non_whitespace_index_character != "`":
                print("ifcb:True")
                return (
                    True,
                    non_whitespace_index,
                    extracted_whitespace_before_info_string,
                    collected_count,
                )
        return False, None, None, None

    def parse_fenced_code_block(self, line_to_parse, start_index, extracted_whitespace):
        """
        Handle the parsing of a fenced code block
        """

        new_tokens = []
        (
            is_fence_start,
            non_whitespace_index,
            extracted_whitespace_before_info_string,
            collected_count,
        ) = self.is_fenced_code_block(line_to_parse, start_index, extracted_whitespace)
        if is_fence_start and not self.stack[-1].startswith("html-block:"):
            preface = "fcode-block:"
            if self.stack[-1].startswith(preface):
                print("pfcb->end")
                if (
                    self.stack[-1][len(preface)] == line_to_parse[start_index]
                    and collected_count >= int(self.stack[-1][len(preface) + 2 :])
                    and non_whitespace_index >= len(line_to_parse)
                ):
                    new_tokens.append("[end-fcode-block:" + extracted_whitespace + "]")
                    del self.stack[-1]
            else:
                print("pfcb->check")
                if (
                    line_to_parse[start_index] == "~"
                    or "`" not in line_to_parse[non_whitespace_index:]
                ):
                    print("pfcb->start")
                    (
                        after_extracted_text_index,
                        extracted_text,
                    ) = ParserHelper.extract_until_whitespace(
                        line_to_parse, non_whitespace_index
                    )
                    text_after_extracted_text = line_to_parse[
                        after_extracted_text_index:
                    ]

                    new_tokens = self.close_open_blocks(only_these_blocks=["para"])

                    self.stack.append(
                        "fcode-block:"
                        + line_to_parse[start_index]
                        + ":"
                        + str(collected_count)
                    )
                    new_tokens.append(
                        "[fcode-block:"
                        + line_to_parse[start_index]
                        + ":"
                        + str(collected_count)
                        + ":"
                        + extracted_text
                        + ":"
                        + text_after_extracted_text
                        + ":"
                        + extracted_whitespace
                        + ":"
                        + extracted_whitespace_before_info_string
                        + "]"
                    )
        return new_tokens

    def is_thematic_break(
        self,
        line_to_parse,
        start_index,
        extracted_whitespace,
        skip_whitespace_check=False,
    ):
        """
        Determine whether or not we have a thematic break.
        """

        thematic_break_character = None
        end_of_break_index = None
        if (
            len(extracted_whitespace) <= 3 or skip_whitespace_check
        ) and ParserHelper.is_character_at_index_one_of(
            line_to_parse, start_index, self.thematic_break_characters
        ):
            start_char = line_to_parse[start_index]
            index = start_index

            char_count = 0
            while index < len(line_to_parse):
                if ParserHelper.is_character_at_index_whitespace(line_to_parse, index):
                    index = index + 1
                elif line_to_parse[index] == start_char:
                    index = index + 1
                    char_count = char_count + 1
                else:
                    break

            if char_count >= 3 and index == len(line_to_parse):
                thematic_break_character = start_char
                end_of_break_index = index

        return thematic_break_character, end_of_break_index

    def parse_thematic_break(
        self, line_to_parse, start_index, extracted_whitespace, this_bq_count,
    ):
        """
        Handle the parsing of a thematic break.
        """

        new_tokens = []
        stack_bq_count = self.__count_of_block_quotes_on_stack()

        start_char, index = self.is_thematic_break(
            line_to_parse, start_index, extracted_whitespace
        )
        if start_char:
            if self.stack[-1] == "para":
                new_tokens.append("[end-" + self.stack[-1] + "]")
                del self.stack[-1]
            if this_bq_count == 0 and stack_bq_count > 0:
                new_tokens = self.close_open_blocks(
                    destination_array=new_tokens,
                    only_these_blocks="block-quote:",
                    include_block_quotes=True,
                )
            new_tokens.append(
                "[tbreak:"
                + start_char
                + ":"
                + extracted_whitespace
                + ":"
                + line_to_parse[start_index:index]
                + "]"
            )
        return new_tokens

    def parse_atx_headings(self, line_to_parse, start_index, extracted_whitespace):
        """
        Handle the parsing of an atx heading.
        """

        new_tokens = []
        if len(extracted_whitespace) <= 3 and ParserHelper.is_character_at_index(
            line_to_parse, start_index, self.atx_character
        ):
            hash_count, new_index = ParserHelper.collect_while_character(
                line_to_parse, start_index, self.atx_character
            )
            (
                non_whitespace_index,
                extracted_whitespace_at_start,
            ) = ParserHelper.extract_whitespace(line_to_parse, new_index)

            if hash_count <= 6 and (
                extracted_whitespace_at_start
                or non_whitespace_index == len(line_to_parse)
            ):

                new_tokens = self.close_open_blocks(new_tokens)
                remaining_line = line_to_parse[non_whitespace_index:]
                (
                    end_index,
                    extracted_whitespace_at_end,
                ) = ParserHelper.extract_whitespace_from_end(remaining_line)
                while end_index > 0 and remaining_line[end_index - 1] == "#":
                    end_index = end_index - 1
                extracted_whitespace_before_end = ""
                if end_index > 0:
                    if ParserHelper.is_character_at_index_whitespace(
                        remaining_line, end_index - 1
                    ):
                        remaining_line = remaining_line[:end_index]
                        (
                            end_index,
                            extracted_whitespace_before_end,
                        ) = ParserHelper.extract_whitespace_from_end(remaining_line)
                        remaining_line = remaining_line[:end_index]
                    else:
                        extracted_whitespace_at_end = ""
                else:
                    remaining_line = ""

                new_tokens.append(
                    "[atx:"
                    + str(hash_count)
                    + ":"
                    + remaining_line
                    + ":"
                    + extracted_whitespace
                    + ":"
                    + extracted_whitespace_at_start
                    + ":"
                    + extracted_whitespace_at_end
                    + ":"
                    + extracted_whitespace_before_end
                    + "]"
                )
        return new_tokens

    def parse_setext_headings(self, line_to_parse, start_index, extracted_whitespace):
        """
        Handle the parsing of an setext heading.
        """

        new_tokens = []
        if (
            len(extracted_whitespace) <= 3
            and ParserHelper.is_character_at_index_one_of(
                line_to_parse, start_index, self.setext_characters
            )
            and (self.stack[-1] == "para")
        ):
            _, collected_to_index = ParserHelper.collect_while_character(
                line_to_parse, start_index, line_to_parse[start_index]
            )
            (
                after_whitespace_index,
                extra_whitespace_after_setext,
            ) = ParserHelper.extract_whitespace(line_to_parse, collected_to_index)
            if after_whitespace_index == len(line_to_parse):
                new_tokens.append(
                    "[end-setext:"
                    + extracted_whitespace
                    + ":"
                    + extra_whitespace_after_setext
                    + "]"
                )
                token_index = len(self.tokenized_document) - 1
                while not (
                    self.tokenized_document[token_index].startswith("[para:")
                    or self.tokenized_document[token_index] == "[html-block]"
                ):
                    token_index = token_index - 1
                replacement_token = (
                    "[setext:"
                    + line_to_parse[start_index]
                    + ":"
                    + self.tokenized_document[token_index][len("[para:") :]
                )
                self.tokenized_document[token_index] = replacement_token
                del self.stack[-1]
        return new_tokens

    # pylint: disable=too-many-arguments
    def parse_paragraph(
        self,
        line_to_parse,
        start_index,
        extracted_whitespace,
        this_bq_count,
        no_para_start_if_empty,
    ):
        """
        Handle the parsing of a paragraph.
        """

        new_tokens = []

        if no_para_start_if_empty and start_index >= len(line_to_parse):
            print("Escaping paragraph due to empty w/ blank")
            return ["[BLANK:]"]

        stack_bq_count = self.__count_of_block_quotes_on_stack()
        print(
            "parse_paragraph>stack_bq_count>"
            + str(stack_bq_count)
            + ">this_bq_count>"
            + str(this_bq_count)
            + "<"
        )

        if (
            len(self.tokenized_document) >= 2
            and self.tokenized_document[-1].startswith("[BLANK:")
            and (
                self.tokenized_document[-2].startswith("[ulist:")
                or self.tokenized_document[-2].startswith("[olist:")
                or self.tokenized_document[-2].startswith("[li")
            )
        ):

            did_find, last_list_index = self.check_for_list_in_process()
            assert did_find
            new_tokens = self.close_open_blocks(until_me=last_list_index)
        if stack_bq_count != 0 and this_bq_count == 0:
            new_tokens = self.close_open_blocks(
                only_these_blocks="block-quote:", include_block_quotes=True
            )

        if self.stack[-1] != "para":
            self.stack.append("para")
            new_tokens.append("[para:" + extracted_whitespace + "]")
            extracted_whitespace = ""
        new_tokens.append(
            "[text:" + line_to_parse[start_index:] + ":" + extracted_whitespace + "]"
        )
        return new_tokens
        # pylint: enable=too-many-arguments

    def __count_of_block_quotes_on_stack(self):
        """
        Helper method to count the number of block quotes currently on the stack.
        """

        stack_bq_count = 0
        for next_item_on_stack in self.stack:
            if next_item_on_stack.startswith("block-quote:"):
                stack_bq_count = stack_bq_count + 1

        return stack_bq_count

    def __count_block_quote_starts(self, line_to_parse, start_index):
        """
        Having detected a block quote character (">") on a line, continue to consume
        and count while the block quote pattern is there.
        """

        this_bq_count = 1
        start_index = start_index + 1

        while True:
            if ParserHelper.is_character_at_index_whitespace(
                line_to_parse, start_index
            ):
                start_index = start_index + 1
            if start_index == len(
                line_to_parse
            ) or ParserHelper.is_character_at_index_not(
                line_to_parse, start_index, self.block_quote_character
            ):
                break
            this_bq_count = this_bq_count + 1
            start_index = start_index + 1
        return this_bq_count, start_index

    # pylint: disable=too-many-arguments
    def __check_for_lazy_handling(
        self,
        this_bq_count,
        stack_bq_count,
        line_to_parse,
        start_index,
        extracted_whitespace,
    ):
        """
        Check if there is any processing to be handled during the handling of
        lazy continuation lines in block quotes.
        """

        print("__check_for_lazy_handling")
        container_level_tokens = []
        if this_bq_count == 0 and stack_bq_count > 0:
            print("haven't processed")
            print(
                "this_bq_count>"
                + str(this_bq_count)
                + ">>stack_bq_count>>"
                + str(stack_bq_count)
                + "<<"
            )

            is_fenced_start, _, _, _ = self.is_fenced_code_block(
                line_to_parse, 0, extracted_whitespace, skip_whitespace_check=True
            )
            print("fenced_start?" + str(is_fenced_start))

            if (
                self.stack[-1].startswith("fcode-block:")
                or self.stack[-1] == "icode-block"
                or is_fenced_start
            ):
                print("__check_for_lazy_handling>>code block")
                assert not container_level_tokens
                container_level_tokens = self.close_open_blocks(
                    only_these_blocks=["block-quote:", self.stack[-1]],
                    include_block_quotes=True,
                )
            else:
                print("__check_for_lazy_handling>>not code block")
                print("__check_for_lazy_handling>>" + str(self.stack))

        if stack_bq_count > 0:
            print("is_set_atx???")
            # TODO replace?
            if (
                len(extracted_whitespace) <= 3
                and ParserHelper.is_character_at_index_one_of(
                    line_to_parse, start_index, self.setext_characters
                )
                and self.stack[-1] == "para"
            ):
                print("set_atx")
                assert not container_level_tokens
                container_level_tokens = self.close_open_blocks(
                    only_these_blocks=["para", "block-quote:"],
                    include_block_quotes=True,
                )
            else:
                print("no set atx!!!!!!!!!!!!")

        return container_level_tokens
        # pylint: enable=too-many-arguments

    def __ensure_stack_at_level(
        self, this_bq_count, stack_bq_count, extracted_whitespace
    ):
        """
        Ensure that the block quote stack is at the proper level on the stack.
        """

        container_level_tokens = []
        if this_bq_count > stack_bq_count:
            container_level_tokens = self.close_open_blocks(
                only_these_blocks=["para", "icode-block"]
            )
            while this_bq_count > stack_bq_count:
                self.stack.append("block-quote:")
                stack_bq_count = stack_bq_count + 1
                container_level_tokens.append(
                    "[block-quote:" + extracted_whitespace + "]"
                )
        return container_level_tokens, stack_bq_count

    # pylint: disable=too-many-arguments
    def handle_block_quote_section(
        self,
        line_to_parse,
        start_index,
        this_bq_count,
        stack_bq_count,
        extracted_whitespace,
    ):
        """
        Handle the processing of a section clearly identified as having block quotes.
        """

        leaf_tokens = []
        container_level_tokens = []

        this_bq_count, start_index = self.__count_block_quote_starts(
            line_to_parse, start_index
        )

        if not self.stack[-1].startswith("fcode-block:"):
            print("handle_block_quote_section>>not fenced")
            container_level_tokens, stack_bq_count = self.__ensure_stack_at_level(
                this_bq_count, stack_bq_count, extracted_whitespace
            )

            line_to_parse = line_to_parse[start_index:]

            if not line_to_parse.strip():
                leaf_tokens = self.handle_blank_line(
                    line_to_parse, from_main_transform=False
                )
        else:
            print("handle_block_quote_section>>fenced")
        return (
            line_to_parse,
            start_index,
            leaf_tokens,
            container_level_tokens,
            stack_bq_count,
            this_bq_count,
        )
        # pylint: enable=too-many-arguments

    # pylint: disable=too-many-arguments
    def is_ulist_start(
        self,
        line_to_parse,
        start_index,
        extracted_whitespace,
        skip_whitespace_check=False,
        adj_ws=None,
    ):
        """
        Determine if we have the start of an un-numbered list.
        """

        print("is_ulist_start>>pre>>")
        is_start = False
        after_all_whitespace_index = -1
        if adj_ws is None:
            adj_ws = extracted_whitespace

        if (
            (len(adj_ws) <= 3 or skip_whitespace_check)
            and ParserHelper.is_character_at_index_one_of(
                line_to_parse, start_index, self.ulist_start_characters
            )
            and (
                ParserHelper.is_character_at_index_whitespace(
                    line_to_parse, start_index + 1
                )
                or ((start_index + 1) == len(line_to_parse))
            )
        ):

            print("is_ulist_start>>mid>>")
            after_all_whitespace_index, _ = ParserHelper.extract_whitespace(
                line_to_parse, start_index + 1
            )
            print(
                "after_all_whitespace_index>>"
                + str(after_all_whitespace_index)
                + ">>len>>"
                + str(len(line_to_parse))
            )

            is_break, _ = self.is_thematic_break(
                line_to_parse, start_index, extracted_whitespace
            )
            if not is_break and not (
                self.stack[-1] == "para"
                and not (
                    self.stack[-2].startswith("ulist")
                    or self.stack[-2].startswith("olist")
                )
                and (after_all_whitespace_index == len(line_to_parse))
            ):
                is_start = True

        print("is_ulist_start>>result>>" + str(is_start))
        return is_start, after_all_whitespace_index
        # pylint: enable=too-many-arguments

    # pylint: disable=too-many-arguments
    def is_olist_start(
        self,
        line_to_parse,
        start_index,
        extracted_whitespace,
        skip_whitespace_check=False,
        adj_ws=None,
    ):
        """
        Determine if we have the start of an numbered or ordered list.
        """

        is_start = False
        end_whitespace_index = -1
        index = None
        my_count = None
        if adj_ws is None:
            adj_ws = extracted_whitespace
        if (
            len(adj_ws) <= 3 or skip_whitespace_check
        ) and ParserHelper.is_character_at_index_one_of(
            line_to_parse, start_index, string.digits
        ):
            index = start_index
            while ParserHelper.is_character_at_index_one_of(
                line_to_parse, index, string.digits
            ):
                index = index + 1
            my_count = index - start_index
            olist_index_number = line_to_parse[start_index:index]
            print("olist?" + olist_index_number + "<<count>>" + str(my_count) + "<<")
            print("olist>>" + str(line_to_parse[index]))
            print("index+1>>" + str(index + 1) + ">>len>>" + str(len(line_to_parse)))

            end_whitespace_index, _ = ParserHelper.extract_whitespace(
                line_to_parse, index + 1
            )
            print(
                "end_whitespace_index>>"
                + str(end_whitespace_index)
                + ">>len>>"
                + str(len(line_to_parse))
                + ">>"
                + olist_index_number
            )

            if (
                my_count <= 9
                and ParserHelper.is_character_at_index_one_of(
                    line_to_parse, index, self.olist_start_characters
                )
                and not (
                    self.stack[-1] == "para"
                    and not (
                        self.stack[-2].startswith("ulist")
                        or self.stack[-2].startswith("olist")
                    )
                    and (
                        (end_whitespace_index == len(line_to_parse))
                        or olist_index_number != "1"
                    )
                )
                and (
                    ParserHelper.is_character_at_index_whitespace(
                        line_to_parse, index + 1
                    )
                    or ((index + 1) == len(line_to_parse))
                )
            ):
                is_start = True

        print("is_olist_start>>result>>" + str(is_start))
        return is_start, index, my_count, end_whitespace_index
        # pylint: enable=too-many-arguments

    # pylint: disable=too-many-locals
    def are_list_starts_equal(
        self, last_list_index, new_stack, current_container_blocks
    ):
        """
        Check to see if the list starts are equal, and hence a continuation of
        the current list.
        """

        balancing_tokens = []

        print(
            "ARE-EQUAL>>stack>>"
            + str(self.stack[last_list_index])
            + ">>new>>"
            + new_stack
        )
        if self.stack[last_list_index] == new_stack:
            balancing_tokens = self.close_open_blocks(
                until_me=last_list_index, include_block_quotes=True
            )
            return True, True, balancing_tokens

        document_token_index = len(self.tokenized_document) - 1
        last_list_token = ""
        while document_token_index >= 0 and not (
            self.tokenized_document[document_token_index].startswith("[olist:")
            or self.tokenized_document[document_token_index].startswith("[ulist:")
            or self.tokenized_document[document_token_index].startswith("[li:")
        ):
            document_token_index = document_token_index - 1
        assert document_token_index >= 0
        print(
            "ARE-EQUAL>>Last_List_token="
            + self.tokenized_document[document_token_index]
        )
        last_list_token = self.tokenized_document[document_token_index]

        split_list_start_from_stack = self.stack[last_list_index].split(":")
        assert len(split_list_start_from_stack) == 5
        split_list_start_from_new_stack = new_stack.split(":")
        assert len(split_list_start_from_new_stack) == 5
        if last_list_token.startswith("[li:"):
            split_list_start = last_list_token[0:-1].split(":")
            print(
                "last_list_token>>"
                + last_list_token
                + ">>split_list_start>>"
                + str(split_list_start)
                + ">>"
            )
            assert len(split_list_start) == 2
            old_start_index = int(split_list_start[1])
        else:
            split_list_start = last_list_token.split(":")
            print(
                "last_list_token>>"
                + last_list_token
                + ">>split_list_start>>"
                + str(split_list_start)
                + ">>"
            )
            assert len(split_list_start) == 5
            old_start_index = int(split_list_start[3])

        old_last_marker_character = split_list_start_from_stack[2][-1]
        new_last_marker_character = split_list_start_from_new_stack[2][-1]
        current_start_index = int(split_list_start_from_new_stack[3])
        print(
            "old>>"
            + str(split_list_start_from_stack)
            + ">>"
            + old_last_marker_character
        )
        print(
            "new>>"
            + str(split_list_start_from_new_stack)
            + ">>"
            + new_last_marker_character
        )
        if (
            split_list_start_from_stack[0] == split_list_start_from_new_stack[0]
            and old_last_marker_character == new_last_marker_character
        ):
            print("are_list_starts_equal>>ELIGIBLE!!!")
            print(
                "are_list_starts_equal>>current_start_index>>"
                + str(current_start_index)
                + ">>old_start_index>>"
                + str(old_start_index)
            )
            if current_start_index < old_start_index:

                print("current_container_blocks>>" + str(current_container_blocks))
                if len(current_container_blocks) > 1:
                    print("current_container_blocks-->" + str(self.stack))
                    split_last_stack = self.stack[-1].split(":")
                    last_stack_depth = int(split_last_stack[3])
                    while current_start_index < last_stack_depth:
                        last_stack_index = self.stack.index(self.stack[-1])
                        close_tokens = self.close_open_blocks(
                            until_me=last_stack_index, include_lists=True
                        )
                        assert close_tokens
                        balancing_tokens.extend(close_tokens)
                        print("close_tokens>>" + str(close_tokens))
                        split_last_stack = self.stack[-1].split(":")
                        last_stack_depth = int(split_last_stack[3])

                return True, True, balancing_tokens
            return True, False, balancing_tokens
        print("SUBLIST WITH DIFFERENT")
        print("are_list_starts_equal>>ELIGIBLE!!!")
        print(
            "are_list_starts_equal>>current_start_index>>"
            + str(current_start_index)
            + ">>old_start_index>>"
            + str(old_start_index)
        )
        if current_start_index >= old_start_index:
            return True, False, balancing_tokens
        return False, False, balancing_tokens
        # pylint: enable=too-many-locals

    # pylint: disable=too-many-arguments
    def pre_list(
        self,
        line_to_parse,
        start_index,
        extracted_whitespace,
        marker_width,
        stack_bq_count,
        this_bq_count,
    ):
        """
        Handle the processing of the first part of the list.
        """

        container_level_tokens = []

        (
            after_marker_ws_index,
            after_marker_whitespace,
        ) = ParserHelper.extract_whitespace(line_to_parse, start_index + 1)
        ws_after_marker = len(after_marker_whitespace)
        ws_before_marker = len(extracted_whitespace)

        print(
            ">>stack_bq_count>>"
            + str(stack_bq_count)
            + ">>this_bq_count>>"
            + str(this_bq_count)
        )
        while this_bq_count < stack_bq_count:

            inf = len(self.stack) - 1
            while not self.stack[inf].startswith("block-quote:"):
                inf = inf - 1

            container_level_tokens = self.close_open_blocks(
                until_me=inf, include_block_quotes=True, include_lists=True
            )
            print("container_level_tokens>>" + str(container_level_tokens))
            stack_bq_count = stack_bq_count - 1

        print(
            ">>>>>XX>>"
            + str(after_marker_ws_index)
            + ">>"
            + str(len(line_to_parse))
            + "<<"
        )
        if after_marker_ws_index == len(line_to_parse):
            print("BOOOOOOOM")
            indent_level = 2 + marker_width
            remaining_whitespace = 0
            ws_after_marker = 1
        else:
            indent_level = ws_before_marker + 1 + ws_after_marker + marker_width
            remaining_whitespace = 0
            print(
                "ws_after_marker>>"
                + str(ws_after_marker)
                + "<<es<<"
                + str(len(extracted_whitespace))
                + "<<indent_level<<"
                + str(indent_level)
                + "<<rem<<"
                + str(remaining_whitespace)
                + "<<"
            )
            if ws_after_marker > 4:
                indent_level = indent_level - ws_after_marker + 1
                remaining_whitespace = ws_after_marker - 1
                ws_after_marker = 1
        print(
            "ws_after_marker>>"
            + str(ws_after_marker)
            + "<<indent_level<<"
            + str(indent_level)
            + "<<rem<<"
            + str(remaining_whitespace)
            + "<<"
        )
        return (
            indent_level,
            remaining_whitespace,
            ws_after_marker,
            after_marker_ws_index,
            ws_before_marker,
            container_level_tokens,
            stack_bq_count,
        )
        # pylint: enable=too-many-arguments

    # pylint: disable=too-many-locals, too-many-arguments
    def post_list(
        self,
        new_stack,
        new_token,
        line_to_parse,
        remaining_whitespace,
        after_marker_ws_index,
        indent_level,
        current_container_blocks,
    ):
        """
        Handle the processing of the last part of the list.
        """

        print("new_stack>>" + new_stack)
        no_para_start_if_empty = True
        container_level_tokens = []

        emit_item = True
        emit_li = True
        did_find, last_list_index = self.check_for_list_in_process()
        if did_find:
            print("list-in-process>>" + self.stack[last_list_index])
            container_level_tokens = self.close_open_blocks(
                until_me=last_list_index + 1
            )
            print("old-stack>>" + str(container_level_tokens) + "<<")

            do_not_emit, emit_li, extra_tokens = self.are_list_starts_equal(
                last_list_index, new_stack, current_container_blocks
            )
            print("extra_tokens>>" + str(extra_tokens))
            container_level_tokens.extend(extra_tokens)
            if do_not_emit:
                emit_item = False
                print("post_list>>don't emit")
            else:
                print("post_list>>close open blocks and emit")
                close_tokens = self.close_open_blocks(
                    until_me=last_list_index, include_lists=True
                )
                assert close_tokens
                container_level_tokens.extend(close_tokens)
        else:
            print("NOT list-in-process>>" + self.stack[last_list_index])
            container_level_tokens = self.close_open_blocks()
        print("container_level_tokens>>" + str(container_level_tokens))

        if emit_item or not emit_li:
            self.stack.append(new_stack)
            container_level_tokens.append(new_token)
        else:
            assert emit_li
            container_level_tokens.append("[li:" + str(indent_level) + "]")
        stri = ""
        line_to_parse = (
            stri.rjust(remaining_whitespace, " ")
            + line_to_parse[after_marker_ws_index:]
        )

        return no_para_start_if_empty, container_level_tokens, line_to_parse
        # pylint: enable=too-many-locals, too-many-arguments

    def check_for_list_in_process(self):
        """
        From the end of the stack, check to see if there is already a list in progress.
        """

        stack_index = len(self.stack) - 1
        while stack_index >= 0 and not (
            self.stack[stack_index].startswith("ulist")
            or self.stack[stack_index].startswith("olist")
        ):
            stack_index = stack_index - 1
        return stack_index >= 0, stack_index

    # pylint: disable=too-many-locals
    def list_in_process(self, line_to_parse, start_index, extracted_whitespace, ind):
        """
        Handle the processing of a line where there is a list in process.
        """

        container_level_tokens = []

        print("!!!!!FOUND>>" + self.stack[ind])
        split_list_info = self.stack[ind][len("ulist") + 1 :].split(":")
        print("!!!!!FOUND>>" + str(split_list_info))
        assert len(split_list_info) == 4
        requested_list_indent = int(split_list_info[0])
        before_ws_length = int(split_list_info[2])
        after_ws_length = int(split_list_info[3])
        print(
            "!!!!!requested_list_indent>>"
            + str(requested_list_indent)
            + ",before_ws="
            + str(before_ws_length)
            + ",after_ws="
            + str(after_ws_length)
        )

        leading_space_length = len(extracted_whitespace)
        is_in_paragraph = self.stack[-1] == "para"

        started_ulist, _ = self.is_ulist_start(
            line_to_parse, start_index, extracted_whitespace, skip_whitespace_check=True
        )
        started_olist, _, _, _ = self.is_olist_start(
            line_to_parse, start_index, extracted_whitespace, skip_whitespace_check=True
        )

        allow_list_continue = True
        if leading_space_length >= 4 and (started_ulist or started_olist):
            allow_list_continue = not self.tokenized_document[-1].startswith("[BLANK:")

        print(
            "leading_space_length>>"
            + str(leading_space_length)
            + ">>requested_list_indent>>"
            + str(requested_list_indent)
            + ">>is_in_paragraph>>"
            + str(is_in_paragraph)
        )
        if leading_space_length >= requested_list_indent and allow_list_continue:
            print("enough ws to continue")
            remaining_indent = leading_space_length - requested_list_indent
            line_to_parse = (
                "".rjust(remaining_indent, " ") + line_to_parse[start_index:]
            )
        else:
            requested_list_indent = requested_list_indent - before_ws_length
            is_in_paragraph = self.stack[-1] == "para"
            print(
                "leading_space_length>>"
                + str(leading_space_length)
                + ">>adj requested_list_indent>>"
                + str(requested_list_indent)
                + ">>"
                + str(is_in_paragraph)
                + "<<"
            )
            if (
                is_in_paragraph
                and leading_space_length >= requested_list_indent
                and allow_list_continue
            ):
                print("adjusted enough ws to continue")
                remaining_indent = requested_list_indent - requested_list_indent
                line_to_parse = (
                    "".rjust(remaining_indent, " ") + line_to_parse[start_index:]
                )
            else:
                print("ws(naa)>>line_to_parse>>" + line_to_parse + "<<")
                print("ws(naa)>>stack>>" + str(self.stack))
                print("ws(naa)>>tokens>>" + str(self.tokenized_document))

                is_theme_break, _ = self.is_thematic_break(
                    line_to_parse,
                    start_index,
                    extracted_whitespace,
                    skip_whitespace_check=True,
                )
                print("ws(naa)>>is_theme_break>>" + str(is_theme_break))

                if not is_in_paragraph or is_theme_break:
                    print("ws (normal and adjusted) not enough to continue")

                    container_level_tokens = self.close_open_blocks(
                        until_me=ind, include_lists=True
                    )
                else:
                    print("ws (normal and adjusted) continue")

        return container_level_tokens, line_to_parse
        # pylint: enable=too-many-locals

    def calculate_adjusted_whitespace(
        self, current_container_blocks, line_to_parse, extracted_whitespace, foobar=None
    ):
        """
        Based on the last container on the stack, determine what the adjusted whitespace is.
        """

        adj_ws = extracted_whitespace
        stack_index = len(self.stack) - 1
        while stack_index >= 0 and not (
            self.stack[stack_index].startswith("ulist:")
            or self.stack[stack_index].startswith("olist:")
        ):
            stack_index = stack_index - 1
        if stack_index < 0:
            print("PLFCB>>No Started lists")
            assert len(current_container_blocks) == 0
            if foobar is None:
                print("PLFCB>>No Started Block Quote")
            else:
                print("PLFCB>>Started Block Quote")
                adj_ws = extracted_whitespace[foobar:]
        else:
            assert len(current_container_blocks) >= 1
            print("PLFCB>>Started list-last stack>>" + str(self.stack[stack_index]))
            token_index = len(self.tokenized_document) - 1
            while token_index >= 0 and not (
                self.tokenized_document[token_index].startswith("[ulist:")
                or self.tokenized_document[token_index].startswith("[olist:")
                or self.tokenized_document[token_index].startswith("[li:")
            ):
                token_index = token_index - 1
            print(
                "PLFCB>>Started list-last token>>"
                + str(self.tokenized_document[token_index])
            )
            last_list_token = self.tokenized_document[token_index]
            if last_list_token.startswith("[li:"):
                split_list_start = last_list_token[0:-1].split(":")
                assert len(split_list_start) == 2
                old_start_index = int(split_list_start[1])
            else:
                split_list_start = last_list_token.split(":")
                assert len(split_list_start) == 5
                old_start_index = int(split_list_start[3])

            ws_len = len(extracted_whitespace)
            print(
                "old_start_index>>" + str(old_start_index) + ">>ws_len>>" + str(ws_len)
            )
            if ws_len >= old_start_index:
                # line_to_parse = line_to_parse[old_start_index:]
                # start_index, extracted_whitespace = self.extract_whitespace(line_to_parse, xxxxx)
                print("RELINE:" + line_to_parse + ":")
                adj_ws = extracted_whitespace[old_start_index:]
            else:
                print("DOWNGRADE")
        return adj_ws

    def is_block_quote_start(
        self, line_to_parse, start_index, extracted_whitespace, adj_ws=None
    ):
        """
        Determine if we have the start of a block quote section.
        """

        if adj_ws is None:
            adj_ws = extracted_whitespace

        if len(adj_ws) <= 3 and ParserHelper.is_character_at_index(
            line_to_parse, start_index, self.block_quote_character
        ):
            return True
        return False

    # pylint: disable=too-many-locals, too-many-arguments
    def handle_nested_container_blocks(
        self,
        container_depth,
        this_bq_count,
        stack_bq_count,
        line_to_parse,
        end_of_ulist_start_index,
        end_of_olist_start_index,
        end_of_bquote_start_index,
        leaf_tokens,
        container_level_tokens,
    ):
        """
        Handle the processing of nested container blocks, as they can contain
        themselves and get somewhat messy.
        """

        assert container_depth < 10
        print("check next container_start>")
        nested_ulist_start, _ = self.is_ulist_start(line_to_parse, 0, "")
        nested_olist_start, _, _, _ = self.is_olist_start(line_to_parse, 0, "")
        nested_block_start = self.is_block_quote_start(line_to_parse, 0, "")
        print(
            "check next container_start>ulist>"
            + str(nested_ulist_start)
            + ">index>"
            + str(end_of_ulist_start_index)
        )
        print(
            "check next container_start>olist>"
            + str(nested_olist_start)
            + ">index>"
            + str(end_of_olist_start_index)
        )
        print(
            "check next container_start>bquote>"
            + str(nested_block_start)
            + ">index>"
            + str(end_of_bquote_start_index)
        )
        print("check next container_start>stack>>" + str(self.stack))
        print("check next container_start>leaf_tokens>>" + str(leaf_tokens))
        print(
            "check next container_start>container_level_tokens>>"
            + str(container_level_tokens)
        )

        adj_line_to_parse = line_to_parse

        print("check next container_start>pre>>" + str(adj_line_to_parse) + "<<")
        active_container_index = max(
            end_of_ulist_start_index,
            end_of_olist_start_index,
            end_of_bquote_start_index,
        )
        print(
            "check next container_start>max>>"
            + str(active_container_index)
            + ">>bq>>"
            + str(end_of_bquote_start_index)
        )
        print(
            "^^"
            + adj_line_to_parse[0:end_of_bquote_start_index]
            + "^^"
            + adj_line_to_parse[end_of_bquote_start_index:]
            + "^^"
        )
        if (
            end_of_bquote_start_index != -1
            and not nested_ulist_start
            and not nested_olist_start
        ):  # and active_container_index == end_of_bquote_start_index:
            adj_line_to_parse = adj_line_to_parse[end_of_bquote_start_index:]

        print(
            "check next container_start>mid>>stack_bq_count>>"
            + str(stack_bq_count)
            + "<<this_bq_count<<"
            + str(this_bq_count)
        )
        adj_line_to_parse = "".rjust(active_container_index) + adj_line_to_parse
        print("check next container_start>post<<" + str(adj_line_to_parse) + "<<")

        print("leaf_tokens>>" + str(leaf_tokens))
        if leaf_tokens:
            self.tokenized_document.extend(leaf_tokens)
            leaf_tokens = []
        if container_level_tokens:
            self.tokenized_document.extend(container_level_tokens)
            container_level_tokens = []

        print("check next container_start>stack>>" + str(self.stack))
        print(
            "check next container_start>tokenized_document>>"
            + str(self.tokenized_document)
        )

        if nested_ulist_start or nested_olist_start or nested_block_start:
            print("check next container_start>recursing")
            print("check next container_start>>" + adj_line_to_parse + "\n")

            adj_block = None
            if end_of_bquote_start_index != -1:
                adj_block = end_of_bquote_start_index

            print("adj_line_to_parse>>>" + str(adj_line_to_parse) + "<<<")
            _, line_to_parse = self.parse_line_for_container_blocks(
                adj_line_to_parse,
                container_depth=container_depth + 1,
                foobar=adj_block,
                init_bq=this_bq_count,
            )
            print("\ncheck next container_start>recursed")
            print("check next container_start>stack>>" + str(self.stack))
            print(
                "check next container_start>tokenized_document>>"
                + str(self.tokenized_document)
            )
            print("check next container_start>line_parse>>" + str(line_to_parse))
        return line_to_parse, leaf_tokens, container_level_tokens
        # pylint: enable=too-many-locals, too-many-arguments

    # pylint: disable=too-many-locals, too-many-arguments
    def handle_ulist_block(
        self,
        did_process,
        was_container_start,
        no_para_start_if_empty,
        line_to_parse,
        start_index,
        extracted_whitespace,
        adj_ws,
        stack_bq_count,
        this_bq_count,
        current_container_blocks,
    ):
        """
        Handle the processing of a ulist block.
        """

        end_of_ulist_start_index = -1
        container_level_tokens = []
        if not did_process:
            started_ulist, end_of_ulist_start_index = self.is_ulist_start(
                line_to_parse, start_index, extracted_whitespace, adj_ws=adj_ws
            )
            if started_ulist:
                print("clt>>ulist-start")

                (
                    indent_level,
                    remaining_whitespace,
                    ws_after_marker,
                    after_marker_ws_index,
                    ws_before_marker,
                    container_level_tokens,
                    stack_bq_count,
                ) = self.pre_list(
                    line_to_parse,
                    start_index,
                    extracted_whitespace,
                    0,
                    stack_bq_count,
                    this_bq_count,
                )

                print(
                    "total="
                    + str(indent_level)
                    + ";ws-before="
                    + str(ws_before_marker)
                    + ";ws_after="
                    + str(ws_after_marker)
                )
                new_stack = (
                    "ulist:"
                    + str(indent_level)
                    + ":"
                    + line_to_parse[start_index]
                    + ":"
                    + str(ws_before_marker)
                    + ":"
                    + str(ws_after_marker)
                )
                new_token = (
                    "[ulist:"
                    + line_to_parse[start_index]
                    + "::"
                    + str(indent_level)
                    + ":"
                    + extracted_whitespace
                    + "]"
                )

                (
                    no_para_start_if_empty,
                    new_container_level_tokens,
                    line_to_parse,
                ) = self.post_list(
                    new_stack,
                    new_token,
                    line_to_parse,
                    remaining_whitespace,
                    after_marker_ws_index,
                    indent_level,
                    current_container_blocks,
                )
                assert new_container_level_tokens
                container_level_tokens.extend(new_container_level_tokens)
                did_process = True
                was_container_start = True

        return (
            did_process,
            was_container_start,
            end_of_ulist_start_index,
            no_para_start_if_empty,
            line_to_parse,
            container_level_tokens,
        )
        # pylint: enable=too-many-locals, too-many-arguments

    # pylint: disable=too-many-locals, too-many-arguments
    def handle_olist_block(
        self,
        did_process,
        was_container_start,
        no_para_start_if_empty,
        line_to_parse,
        start_index,
        extracted_whitespace,
        adj_ws,
        stack_bq_count,
        this_bq_count,
        current_container_blocks,
    ):
        """
        Handle the processing of a olist block.
        """

        end_of_olist_start_index = -1
        container_level_tokens = []
        if not did_process:
            (
                started_olist,
                index,
                my_count,
                end_of_olist_start_index,
            ) = self.is_olist_start(
                line_to_parse, start_index, extracted_whitespace, adj_ws=adj_ws
            )
            if started_olist:
                assert not container_level_tokens
                print("clt>>olist-start")

                (
                    indent_level,
                    remaining_whitespace,
                    ws_after_marker,
                    after_marker_ws_index,
                    ws_before_marker,
                    container_level_tokens,
                    stack_bq_count,
                ) = self.pre_list(
                    line_to_parse,
                    index,
                    extracted_whitespace,
                    my_count,
                    stack_bq_count,
                    this_bq_count,
                )

                print(
                    "total="
                    + str(indent_level)
                    + ";ws-before="
                    + str(ws_before_marker)
                    + ";ws_after="
                    + str(ws_after_marker)
                )

                new_stack = (
                    "olist:"
                    + str(indent_level)
                    + ":"
                    + line_to_parse[start_index : index + 1]
                    + ":"
                    + str(ws_before_marker)
                    + ":"
                    + str(ws_after_marker)
                )
                new_token = (
                    "[olist:"
                    + line_to_parse[index]
                    + ":"
                    + line_to_parse[start_index:index]
                    + ":"
                    + str(indent_level)
                    + ":"
                    + extracted_whitespace
                    + "]"
                )

                (
                    no_para_start_if_empty,
                    new_container_level_tokens,
                    line_to_parse,
                ) = self.post_list(
                    new_stack,
                    new_token,
                    line_to_parse,
                    remaining_whitespace,
                    after_marker_ws_index,
                    indent_level,
                    current_container_blocks,
                )
                assert new_container_level_tokens
                container_level_tokens.extend(new_container_level_tokens)
                did_process = True
                was_container_start = True
        return (
            did_process,
            was_container_start,
            end_of_olist_start_index,
            no_para_start_if_empty,
            line_to_parse,
            container_level_tokens,
        )
        # pylint: enable=too-many-locals, too-many-arguments

    # pylint: disable=too-many-arguments
    def handle_block_quote_block(
        self,
        line_to_parse,
        start_index,
        extracted_whitespace,
        adj_ws,
        this_bq_count,
        stack_bq_count,
    ):
        """
        Handle the processing of a blockquote block.
        """

        did_process = False
        was_container_start = False
        end_of_bquote_start_index = -1
        leaf_tokens = []
        container_level_tokens = []

        if self.is_block_quote_start(
            line_to_parse, start_index, extracted_whitespace, adj_ws=adj_ws
        ):
            print("clt>>block-start")
            (
                line_to_parse,
                start_index,
                leaf_tokens,
                container_level_tokens,
                stack_bq_count,
                alt_this_bq_count,
            ) = self.handle_block_quote_section(
                line_to_parse,
                start_index,
                this_bq_count,
                stack_bq_count,
                extracted_whitespace,
            )

            # TODO for nesting, may need to augment with this_bq_count already set.
            if this_bq_count == 0:
                this_bq_count = alt_this_bq_count
            else:
                print(
                    ">>>>>>>>>>>>>>>"
                    + str(this_bq_count)
                    + ">>>"
                    + str(alt_this_bq_count)
                )
                this_bq_count = alt_this_bq_count

            did_process = True
            was_container_start = True
            end_of_bquote_start_index = start_index

        return (
            did_process,
            was_container_start,
            end_of_bquote_start_index,
            this_bq_count,
            stack_bq_count,
            line_to_parse,
            start_index,
            leaf_tokens,
            container_level_tokens,
        )
        # pylint: enable=too-many-arguments

    def calculate_for_container_blocks(
        self, line_to_parse, extracted_whitespace, foobar, init_bq
    ):
        """
        Perform some calculations that will be needed for parsing the container blocks.
        """

        this_bq_count = 0
        if init_bq is not None:
            this_bq_count = init_bq

        current_container_blocks = []
        for ind in self.stack:
            if ind.startswith("olist:") or ind.startswith("ulist:"):
                current_container_blocks.append(ind)

        adj_ws = self.calculate_adjusted_whitespace(
            current_container_blocks, line_to_parse, extracted_whitespace, foobar=foobar
        )

        stack_bq_count = self.__count_of_block_quotes_on_stack()

        return current_container_blocks, adj_ws, stack_bq_count, this_bq_count

    # pylint: disable=too-many-locals
    def parse_line_for_container_blocks(
        self, line_to_parse, container_depth=0, foobar=None, init_bq=None
    ):
        """
        Parse the line, taking care to handle any container blocks before deciding
        whether or not to pass the (remaining parts of the) line to the leaf block
        processor.
        """

        print("Line:" + line_to_parse + ":")
        no_para_start_if_empty = False

        start_index, extracted_whitespace = ParserHelper.extract_whitespace(
            line_to_parse, 0
        )

        (
            current_container_blocks,
            adj_ws,
            stack_bq_count,
            this_bq_count,
        ) = self.calculate_for_container_blocks(
            line_to_parse, extracted_whitespace, foobar, init_bq
        )

        end_of_olist_start_index = -1
        end_of_ulist_start_index = -1

        print("LINE-pre-block-start>" + line_to_parse)
        (
            did_process,
            was_container_start,
            end_of_bquote_start_index,
            this_bq_count,
            stack_bq_count,
            line_to_parse,
            start_index,
            leaf_tokens,
            container_level_tokens,
        ) = self.handle_block_quote_block(
            line_to_parse,
            start_index,
            extracted_whitespace,
            adj_ws,
            this_bq_count,
            stack_bq_count,
        )

        print("LINE-pre-ulist>" + line_to_parse)
        (
            did_process,
            was_container_start,
            end_of_ulist_start_index,
            no_para_start_if_empty,
            line_to_parse,
            resultant_tokens,
        ) = self.handle_ulist_block(
            did_process,
            was_container_start,
            no_para_start_if_empty,
            line_to_parse,
            start_index,
            extracted_whitespace,
            adj_ws,
            stack_bq_count,
            this_bq_count,
            current_container_blocks,
        )
        container_level_tokens.extend(resultant_tokens)

        print("LINE-pre-olist>" + line_to_parse)
        (
            did_process,
            was_container_start,
            end_of_olist_start_index,
            no_para_start_if_empty,
            line_to_parse,
            resultant_tokens,
        ) = self.handle_olist_block(
            did_process,
            was_container_start,
            no_para_start_if_empty,
            line_to_parse,
            start_index,
            extracted_whitespace,
            adj_ws,
            stack_bq_count,
            this_bq_count,
            current_container_blocks,
        )
        container_level_tokens.extend(resultant_tokens)

        print(
            "LINE-another_container_start>did_start>>"
            + str(was_container_start)
            + ">>"
            + line_to_parse
        )
        if was_container_start and line_to_parse:
            (
                line_to_parse,
                leaf_tokens,
                container_level_tokens,
            ) = self.handle_nested_container_blocks(
                container_depth,
                this_bq_count,
                stack_bq_count,
                line_to_parse,
                end_of_ulist_start_index,
                end_of_olist_start_index,
                end_of_bquote_start_index,
                leaf_tokens,
                container_level_tokens,
            )
            no_para_start_if_empty = True

        if container_depth:
            assert not leaf_tokens
            print(">>>>>>>>" + line_to_parse + "<<<<<<<<<<")
            return container_level_tokens, line_to_parse

        print("LINE-list-in-progress>" + line_to_parse)

        if not did_process:
            is_list_in_process, ind = self.check_for_list_in_process()
            if is_list_in_process:
                assert not container_level_tokens
                print("clt>>list-in-progress")
                container_level_tokens, line_to_parse = self.list_in_process(
                    line_to_parse, start_index, extracted_whitespace, ind
                )
                did_process = True

        if did_process:
            print(
                "clt-before-lead>>"
                + str(len(container_level_tokens))
                + ">>"
                + str(container_level_tokens)
            )

        print("LINE-lazy>" + line_to_parse)
        if not leaf_tokens:
            print("clt>>lazy-check")
            lazy_tokens = self.__check_for_lazy_handling(
                this_bq_count,
                stack_bq_count,
                line_to_parse,
                start_index,
                extracted_whitespace,
            )
            if lazy_tokens:
                print("clt>>lazy-found")
                container_level_tokens.extend(lazy_tokens)
                did_process = True

        if did_process:
            print(
                "clt-after-leaf>>"
                + str(len(container_level_tokens))
                + ">>"
                + str(container_level_tokens)
            )

        if not leaf_tokens:
            print("parsing leaf>>")
            leaf_tokens = self.parse_line_for_leaf_blocks(
                line_to_parse, 0, this_bq_count, no_para_start_if_empty
            )
            print("parsed leaf>>" + str(leaf_tokens))
            print("parsed leaf>>" + str(len(leaf_tokens)))

        assert leaf_tokens
        container_level_tokens.extend(leaf_tokens)
        print(
            "clt-end>>"
            + str(len(container_level_tokens))
            + ">>"
            + str(container_level_tokens)
            + "<<"
        )
        return container_level_tokens, line_to_parse
        # pylint: enable=too-many-locals

    @classmethod
    def check_for_special_html_blocks(cls, line_to_parse, character_index):
        """
        Check for the easy to spot special blocks: 2-5.
        """

        html_block_type = None
        if character_index < len(line_to_parse):
            if ParserHelper.is_character_at_index(line_to_parse, character_index, "!"):
                if ParserHelper.are_characters_at_index(
                    line_to_parse, character_index + 1, "--"
                ):
                    html_block_type = "2"
                elif ParserHelper.is_character_at_index_one_of(
                    line_to_parse, character_index + 1, string.ascii_uppercase
                ):
                    html_block_type = "4"
                elif ParserHelper.are_characters_at_index(
                    line_to_parse, character_index + 1, "[CDATA["
                ):
                    html_block_type = "5"
            elif ParserHelper.is_character_at_index(
                line_to_parse, character_index, "?"
            ):
                html_block_type = "3"

        return html_block_type

    def check_for_normal_html_blocks(
        self, remaining_html_tag, line_to_parse, character_index
    ):
        """
        Check for the the html blocks that are harder to identify: 1, 6-7.
        """

        html_block_type = None

        if HtmlHelper.is_valid_block_1_tag_name(remaining_html_tag):
            html_block_type = "1"
        else:
            adjusted_remaining_html_tag = remaining_html_tag
            is_end_tag = False
            print("6/7?")
            if adjusted_remaining_html_tag.startswith("/"):
                adjusted_remaining_html_tag = adjusted_remaining_html_tag[1:]
                is_end_tag = True
                print("end")
            print(">>" + str(character_index) + ">>" + str(len(line_to_parse)))
            if (
                character_index < len(line_to_parse)
                and line_to_parse[character_index] == ">"
                and adjusted_remaining_html_tag.endswith("/")
            ):
                adjusted_remaining_html_tag = adjusted_remaining_html_tag[0:-1]
                print("-otherend")
            print(
                "adjusted_remaining_html_tag-->" + adjusted_remaining_html_tag + "<--"
            )
            if adjusted_remaining_html_tag in self.html_block_6_start:
                print("6")
                html_block_type = "6"
            elif is_end_tag:
                print("end?")
                if HtmlHelper.is_complete_html_end_tag(
                    adjusted_remaining_html_tag, line_to_parse, character_index,
                ):
                    html_block_type = "7"
                    print("7-end")
            else:
                if HtmlHelper.is_complete_html_start_tag(
                    adjusted_remaining_html_tag, line_to_parse, character_index,
                ):
                    html_block_type = "7"
                    print("7-start")
        return html_block_type

    def determine_html_block_type(self, line_to_parse, start_index):
        """
        Determine the type of the html block that we are starting.
        """

        print(">>" + str(start_index) + ">>" + line_to_parse + "<<")
        character_index = start_index + 1
        remaining_html_tag = ""

        html_block_type = self.check_for_special_html_blocks(
            line_to_parse, character_index
        )
        if not html_block_type:
            (
                character_index,
                remaining_html_tag,
            ) = ParserHelper.collect_until_one_of_characters(
                line_to_parse, character_index, " >"
            )
            remaining_html_tag = remaining_html_tag.lower()

            print("remaining_html_tag>>" + remaining_html_tag)
            html_block_type = self.check_for_normal_html_blocks(
                remaining_html_tag, line_to_parse, character_index
            )
        if not html_block_type:
            return None
        if html_block_type == "7":
            print("7>>>" + str(self.stack))
            print("7>>>" + str(self.tokenized_document))
            if self.stack[-1] == "para":
                return None
        return html_block_type + ":" + remaining_html_tag

    def parse_html_block(self, line_to_parse, start_index, extracted_whitespace):
        """
        Determine if we have the criteria that we need to start an HTML block.
        """

        new_tokens = []
        if (len(extracted_whitespace) <= 3) and ParserHelper.is_character_at_index(
            line_to_parse, start_index, self.html_block_start_character
        ):
            print("HTML-START?")
            block_start_info = self.determine_html_block_type(
                line_to_parse, start_index
            )
            if block_start_info:
                print("HTML-STARTED::" + block_start_info)
                new_tokens = self.close_open_blocks(only_these_blocks=["para"])
                self.stack.append("html-block:" + block_start_info)
                new_tokens.append("[html-block]")
            else:
                print("HTML-NOT-STARTED")
        return new_tokens

    def check_normal_html_block_end(
        self, line_to_parse, start_index, extracted_whitespace
    ):
        """
        Check to see if we have encountered the end of the current HTML block
        via text on a normal line.
        """

        # xx = self.parse_setext_headings(line_to_parse, start_index, extracted_whitespace)
        # if xx:
        #    print("HTML-LINE:" + str(xx))
        #    return xx
        print("HTML-LINE")
        new_tokens = []
        new_tokens.append(
            "[text:" + line_to_parse[start_index:] + ":" + extracted_whitespace + "]"
        )

        split_stack_value = self.stack[-1].split(":")
        print(">>" + str(split_stack_value) + "<<")
        assert len(split_stack_value) >= 3

        is_block_terminated = False
        adj_line = line_to_parse[start_index:]
        if split_stack_value[1] == "1":
            for next_end_tag in self.html_block_1_end_tags:
                if next_end_tag in adj_line:
                    is_block_terminated = True
        elif split_stack_value[1] == "2":
            is_block_terminated = "-->" in adj_line
        elif split_stack_value[1] == "3":
            is_block_terminated = "?>" in adj_line
        elif split_stack_value[1] == "4":
            is_block_terminated = ">" in adj_line
        elif split_stack_value[1] == "5":
            is_block_terminated = "]]>" in adj_line

        if is_block_terminated:
            terminated_block_tokens = self.close_open_blocks(
                only_these_blocks=self.stack[-1]
            )
            assert terminated_block_tokens
            new_tokens.extend(terminated_block_tokens)
        return new_tokens

    def check_blank_html_block_end(self):
        """
        Check to see if we have encountered the end of the current HTML block
        via an empty line or BLANK.
        """

        print("HTML-BLANK")

        split_stack_value = self.stack[-1].split(":")
        print(">>" + str(split_stack_value) + "<<")
        assert len(split_stack_value) >= 3

        new_tokens = []
        if split_stack_value[1] == "6" or split_stack_value[1] == "7":
            new_tokens = self.close_open_blocks(only_these_blocks=self.stack[-1])

        return new_tokens

    def parse_line_for_leaf_blocks(
        self, line_to_parse, start_index, this_bq_count, no_para_start_if_empty
    ):
        """
        Parse the contents of a line for a leaf block.
        """

        print("Leaf Line:" + line_to_parse + ":")
        new_tokens = []
        pre_tokens = []
        start_index, extracted_whitespace = ParserHelper.extract_whitespace(
            line_to_parse, start_index
        )

        if self.stack[-1] == "icode-block" and len(extracted_whitespace) <= 3:
            pre_tokens.append("[end-" + self.stack[-1] + "]")
            del self.stack[-1]
            while self.tokenized_document[-1].startswith("[BLANK"):
                last_element = self.tokenized_document[-1]
                pre_tokens.append(last_element)
                del self.tokenized_document[-1]

        outer_processed = False

        fenced_tokens = self.parse_fenced_code_block(
            line_to_parse, start_index, extracted_whitespace
        )
        if fenced_tokens:
            new_tokens.extend(fenced_tokens)
            outer_processed = True
        elif self.stack[-1].startswith("fcode-block:"):
            new_tokens.append(
                "[text:"
                + line_to_parse[start_index:]
                + ":"
                + extracted_whitespace
                + "]"
            )
            outer_processed = True

        if not outer_processed and not self.stack[-1].startswith("html-block:"):
            html_tokens = self.parse_html_block(
                line_to_parse, start_index, extracted_whitespace
            )
            new_tokens.extend(html_tokens)
        if self.stack[-1].startswith("html-block:"):
            html_tokens = self.check_normal_html_block_end(
                line_to_parse, start_index, extracted_whitespace
            )
            assert html_tokens
            new_tokens.extend(html_tokens)
            outer_processed = True

        if not outer_processed:
            assert not new_tokens
            new_tokens = self.parse_atx_headings(
                line_to_parse, start_index, extracted_whitespace
            )
            if not new_tokens:
                new_tokens = self.parse_indented_code_block(
                    line_to_parse, start_index, extracted_whitespace
                )
            if not new_tokens:
                new_tokens = self.parse_setext_headings(
                    line_to_parse, start_index, extracted_whitespace
                )
            if not new_tokens:
                new_tokens = self.parse_thematic_break(
                    line_to_parse, start_index, extracted_whitespace, this_bq_count,
                )
            if not new_tokens:
                new_tokens = self.parse_paragraph(
                    line_to_parse,
                    start_index,
                    extracted_whitespace,
                    this_bq_count,
                    no_para_start_if_empty,
                )

        assert new_tokens
        pre_tokens.extend(new_tokens)
        return pre_tokens
