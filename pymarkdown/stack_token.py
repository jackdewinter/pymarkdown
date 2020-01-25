"""
Module to provide for an element that can be added to the stack.
"""


class StackToken:
    """
    Class to provide for an element to place on the stack.
    """

    stack_base_document = "document"
    stack_unordered_list = "ulist"
    stack_ordered_list = "olist"
    stack_html_block = "html-block"
    stack_block_quote = "block-quote"
    stack_fenced_code = "fcode-block"
    stack_indented_code = "icode-block"
    stack_paragraph = "para"

    def __init__(self, type_name, extra_data=None):
        self.type_name = type_name
        self.extra_data = extra_data

    def __str__(self):
        add_extra = ""
        if self.extra_data:
            add_extra = ":" + self.extra_data
        return "StackToken(" + self.type_name + add_extra + ")"

    def __repr__(self):
        return self.__str__()

    def generate_close_token(self, extracted_whitespace=None):
        """
        Generate the token emitted to close off the current stack token
        """

        close_token = "[end-" + self.type_name
        if extracted_whitespace:
            if not close_token.endswith(":"):
                close_token = close_token + ":"
            close_token = close_token + extracted_whitespace
        return close_token + "]"

    @property
    def is_document(self):
        """
        Is this stack token a document token?
        """
        return self.type_name == self.stack_base_document

    @property
    def is_list(self):
        """
        Is this stack token one of the list tokens?
        """
        return (
            self.type_name == self.stack_ordered_list
            or self.type_name == self.stack_unordered_list
        )

    @property
    def is_html_block(self):
        """
        Is this stack token a html block token?
        """
        return self.type_name == self.stack_html_block

    @property
    def is_fenced_code_block(self):
        """
        Is this stack token a fenced code block token?
        """
        return self.type_name == self.stack_fenced_code

    @property
    def is_indented_code_block(self):
        """
        Is this stack token an indented code block token?
        """
        return self.type_name == self.stack_indented_code

    @property
    def is_block_quote(self):
        """
        Is this stack token a block quote token?
        """
        return self.type_name == self.stack_block_quote

    @property
    def is_paragraph(self):
        """
        Is this stack token a paragraph token?
        """
        return self.type_name == self.stack_paragraph


# pylint: disable=too-few-public-methods
class DocumentStackToken(StackToken):
    """
    Class to provide for a stack token at the root.
    """

    def __init__(self):
        StackToken.__init__(self, StackToken.stack_base_document)


class ParagraphStackToken(StackToken):
    """
    Class to provide for a stack token for a paragraph.
    """

    def __init__(self):
        StackToken.__init__(self, StackToken.stack_paragraph)


class OrderedListStackToken(StackToken):
    """
    Class to provide for a stack token for an ordered list.
    """

    def __init__(self, extra_data):
        StackToken.__init__(self, StackToken.stack_ordered_list, extra_data)


class UnorderedListStackToken(StackToken):
    """
    Class to provide for a stack token for an unordered list.
    """

    def __init__(self, extra_data):
        StackToken.__init__(self, StackToken.stack_unordered_list, extra_data)


class HtmlBlockStackToken(StackToken):
    """
    Class to provide for a stack token for a html block.
    """

    def __init__(self, extra_data):
        StackToken.__init__(self, StackToken.stack_html_block, extra_data)


class BlockQuoteStackToken(StackToken):
    """
    Class to provide for a stack token for a block quote.
    """

    def __init__(self):
        StackToken.__init__(self, StackToken.stack_block_quote)


class FencedCodeBlockStackToken(StackToken):
    """
    Class to provide for a stack token for a fenced code block.
    """

    def __init__(self, extra_data):
        StackToken.__init__(self, StackToken.stack_fenced_code, extra_data)


class IndentedCodeBlockStackToken(StackToken):
    """
    Class to provide for a stack token for an indented code block.
    """

    def __init__(self):
        StackToken.__init__(self, StackToken.stack_indented_code)
