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

        self.stack = ["document"]

    def transform(self, your_text_string):
        """
        Transform a markdown-encoded string into an array of tokens.
        """

        tokenized_document = []
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

            for token_to_copy in new_tokens:
                tokenized_document.append(token_to_copy)
            if len(next_token) == 2:
                next_token = next_token[1].split("\n", 1)
            elif len(next_token) == 1:
                break

        print("cleanup")
        while self.stack[len(self.stack) - 1] != "document":
            stack_topper = self.stack[-1]
            tokenized_document.append("[end-" + stack_topper + "]")
            del self.stack[-1]
        return tokenized_document

    def handle_blank_line(self, input_line):
        """
        Handle the processing of a blank line.
        """

        new_tokens = []
        if self.stack[-1] != "document":
            new_tokens.append("[end-" + self.stack[-1] + "]")
            del self.stack[-1]

        non_whitespace_index, extracted_whitespace = self.extract_whitespace(
            input_line, 0
        )
        assert non_whitespace_index == len(input_line)
        new_tokens.append("[BLANK:" + extracted_whitespace + "]")
        return new_tokens

    def extract_whitespace(self, source_string, start_index):
        """
        From the start_index, continue extracting whitespace while we have it.
        """

        index = start_index
        while index < len(source_string) and source_string[index] in self.ws_char:
            index = index + 1

        return index, source_string[start_index:index]

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

    def handle_paragraph(self, line_to_parse, start_index, extracted_whitespace):
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
        start_index, extracted_whitespace = self.extract_whitespace(line_to_parse, 0)

        new_tokens = self.parse_thematic_break(
            line_to_parse, start_index, extracted_whitespace
        )

        # para
        if not new_tokens:
            new_tokens = self.handle_paragraph(
                line_to_parse, start_index, extracted_whitespace
            )

        return new_tokens
