"""
Module to provide a tokenization of a markdown-encoded string.
"""


class TokenizedMarkdown:
    """
    Class to provide a tokenization of a markdown-encoded string.
    """

    def __init__(self):
        """
        Initializes a new instance of the TokenizedMarkdown class.
        """
        self.ws_char = " \t"
        self.tokenized_document = None
        self.stack = ["document"]

    def transform(self, your_text_string):
        """
        Transform a markdown-encoded string into an array of tokens.
        """

        self.tokenized_document = []
        next_token = your_text_string.split("\n", 1)
        while next_token:
            print("\nnext-line>>" + str(next_token))
            print("stack>>" + str(self.stack))
            print("current_block>>" + self.stack[-1])

            next_line = next_token[0]
            new_tokens = []
            if not next_line or not next_line.strip():
                new_tokens = self.handle_blank_line(next_line)
            else:
                new_tokens = self.parse_line(next_line)

            self.tokenized_document.extend(new_tokens)
            if len(next_token) == 2:
                next_token = next_token[1].split("\n", 1)
            elif len(next_token) == 1:
                break

        print("cleanup")
        return self.close_open_blocks(self.tokenized_document)

    def close_open_blocks(self, destination_array=None, only_these_blocks=None):
        """
        Close any open blocks that are currently on the stack.
        """

        new_tokens = []
        if destination_array:
            new_tokens = destination_array

        while self.stack[-1] != "document":
            print("close_open_blocks>>>>>>>>" + self.stack[-1])
            if only_these_blocks and self.stack[-1] not in only_these_blocks:
                break

            top_element = self.stack[-1]
            print("cob>>>" + str(self.tokenized_document))

            extra_elements = []
            if top_element == "icode-block":
                while self.tokenized_document[-1].startswith("[BLANK"):
                    last_element = self.tokenized_document[-1]
                    extra_elements.append(last_element)
                    del self.tokenized_document[-1]

            new_tokens.append("[end-" + top_element + "]")
            new_tokens.extend(extra_elements)
            del self.stack[-1]
        return new_tokens

    def handle_blank_line(self, input_line):
        """
        Handle the processing of a blank line.
        """

        new_tokens = self.close_open_blocks(only_these_blocks=["para"])

        non_whitespace_index, extracted_whitespace = self.extract_whitespace(
            input_line, 0
        )
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

        if (
            self.determine_whitespace_length(extracted_whitespace) >= 4
            and self.stack[-1] != "para"
        ):
            if self.stack[-1] != "icode-block":
                self.stack.append("icode-block")
                new_tokens.append("[icode-block:" + extracted_whitespace + "]")
                extracted_whitespace = ""
            new_tokens.append(
                "[text:"
                + line_to_parse[start_index:]
                + ":"
                + extracted_whitespace
                + "]"
            )
        return new_tokens

    def parse_thematic_break(self, line_to_parse, start_index, extracted_whitespace):
        """
        Handle the parsing of a thematic break.
        """

        new_tokens = []

        if self.determine_whitespace_length(extracted_whitespace) <= 3 and (
            line_to_parse[start_index] == "*"
            or line_to_parse[start_index] == "-"
            or line_to_parse[start_index] == "_"
        ):
            start_char = line_to_parse[start_index]
            index = start_index

            char_count = 0
            while index < len(line_to_parse):
                if line_to_parse[index] in self.ws_char:
                    index = index + 1
                elif line_to_parse[index] == start_char:
                    index = index + 1
                    char_count = char_count + 1
                else:
                    break

            if char_count >= 3 and index == len(line_to_parse):
                if self.stack[-1] == "para":
                    new_tokens.append("[end-" + self.stack[-1] + "]")
                    del self.stack[-1]
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
        if self.determine_whitespace_length(extracted_whitespace) <= 3 and (
            line_to_parse[start_index] == "#"
        ):
            hash_count, new_index = self.collect_while_character(
                line_to_parse, start_index, "#"
            )
            (
                non_whitespace_index,
                extracted_whitespace_at_start,
            ) = self.extract_whitespace(line_to_parse, new_index)

            if hash_count <= 6 and (
                extracted_whitespace_at_start
                or non_whitespace_index == len(line_to_parse)
            ):

                new_tokens = self.close_open_blocks(new_tokens)
                remaining_line = line_to_parse[non_whitespace_index:]
                (
                    end_index,
                    extracted_whitespace_at_end,
                ) = self.extract_whitespace_from_end(remaining_line)
                while end_index > 0 and remaining_line[end_index - 1] == "#":
                    end_index = end_index - 1
                extracted_whitespace_before_end = ""
                if end_index > 0:
                    if remaining_line[end_index - 1] in self.ws_char:
                        remaining_line = remaining_line[:end_index]
                        (
                            end_index,
                            extracted_whitespace_before_end,
                        ) = self.extract_whitespace_from_end(remaining_line)
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
            self.determine_whitespace_length(extracted_whitespace) <= 3
            and (line_to_parse[start_index] == "=" or line_to_parse[start_index] == "-")
            and self.stack[-1] == "para"
        ):

            _, collected_to_index = self.collect_while_character(
                line_to_parse, start_index, line_to_parse[start_index]
            )
            (
                after_whitespace_index,
                extra_whitespace_after_setext,
            ) = self.extract_whitespace(line_to_parse, collected_to_index)
            if after_whitespace_index == len(line_to_parse):
                new_tokens.append(
                    "[end-setext:"
                    + extracted_whitespace
                    + ":"
                    + extra_whitespace_after_setext
                    + "]"
                )
                for token_index in range(len(self.tokenized_document) - 1, -1, -1):
                    if self.tokenized_document[token_index].startswith("[para:"):
                        print("boing")
                        replacement_token = (
                            "[setext:"
                            + line_to_parse[start_index]
                            + ":"
                            + self.tokenized_document[token_index][len("[para:") :]
                        )
                        self.tokenized_document[token_index] = replacement_token
                        break
                del self.stack[-1]
        return new_tokens

    def parse_paragraph(self, line_to_parse, start_index, extracted_whitespace):
        """
        Handle the parsing of a paragraph.
        """

        new_tokens = []

        if self.stack[-1] != "para":
            self.stack.append("para")
            new_tokens.append("[para:" + extracted_whitespace + "]")
            extracted_whitespace = ""
        new_tokens.append(
            "[text:" + line_to_parse[start_index:] + ":" + extracted_whitespace + "]"
        )
        return new_tokens

    def parse_line(self, line_to_parse):
        """
        Parse the contents of a line.
        """

        print("Line:" + line_to_parse + ":")
        new_tokens = []
        pre_tokens = []
        start_index, extracted_whitespace = self.extract_whitespace(line_to_parse, 0)

        if (
            self.stack[-1] == "icode-block"
            and self.determine_whitespace_length(extracted_whitespace) <= 3
        ):
            pre_tokens.append("[end-" + self.stack[-1] + "]")
            del self.stack[-1]
            print("icode>>" + self.tokenized_document[-1])
            while self.tokenized_document[-1].startswith("[BLANK"):
                last_element = self.tokenized_document[-1]
                pre_tokens.append(last_element)
                del self.tokenized_document[-1]

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
                line_to_parse, start_index, extracted_whitespace
            )
        if not new_tokens:
            new_tokens = self.parse_paragraph(
                line_to_parse, start_index, extracted_whitespace
            )

        pre_tokens.extend(new_tokens)
        return pre_tokens

    @classmethod
    def collect_while_character(cls, line_to_parse, start_index, match_character):
        """
        Collect a sequence of the same character from a given starting point in a string.
        """

        index = start_index
        while index < len(line_to_parse) and line_to_parse[index] == match_character:
            index = index + 1
        return index - start_index, index

    def extract_whitespace(self, source_string, start_index):
        """
        From the start_index, continue extracting whitespace while we have it.
        """

        index = start_index
        while index < len(source_string) and source_string[index] in self.ws_char:
            index = index + 1

        return index, source_string[start_index:index]

    def extract_whitespace_from_end(self, source_string):
        """
        From the start_index, continue extracting whitespace while we have it.
        """
        if not source_string:
            return 0, ""

        index = len(source_string) - 1
        while index >= 0 and source_string[index] in self.ws_char:
            index = index - 1

        return index + 1, source_string[index + 1 :]

    @classmethod
    def determine_whitespace_length(cls, extracted_whitespace):
        """
        Given a string of whitespace characters, determine the length.
        """

        whitespace_length = 0
        for next_character in extracted_whitespace:
            if next_character == " ":
                whitespace_length = whitespace_length + 1
            elif next_character == "\t":
                whitespace_length = whitespace_length + 4
            else:
                raise ValueError()
        return whitespace_length
