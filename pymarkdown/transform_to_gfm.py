"""
Module to provide for a transformation from markdown tokens to html for GFM.
"""
from pymarkdown.inline_helper import InlineHelper
from pymarkdown.markdown_token import (
    AtxHeaderMarkdownToken,
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
    LinkStartMarkdownToken,
    MarkdownToken,
    NewListItemMarkdownToken,
    OrderedListStartMarkdownToken,
    ParagraphMarkdownToken,
    RawHtmlMarkdownToken,
    SetextHeaderMarkdownToken,
    TextMarkdownToken,
    ThematicBreakMarkdownToken,
    UnorderedListStartMarkdownToken,
    UriAutolinkMarkdownToken,
)


# pylint: disable=too-few-public-methods
# pylint: disable=too-many-instance-attributes
class TransformState:
    """
    Class that contains the state of transformation of TransformToGfm.
    """

    def __init__(self, actual_tokens):
        """
        Initializes a new instance of the TransformState class.
        """
        self.is_in_code_block = False
        self.is_in_fenced_code_block = False
        self.is_in_html_block = False
        self.is_in_loose_list = True
        self.transform_stack = []
        self.add_trailing_text = None
        self.add_leading_text = None
        self.actual_tokens = actual_tokens
        self.actual_token_index = 0


# pylint: enable=too-many-instance-attributes
# pylint: enable=too-few-public-methods

# pylint: disable=too-many-public-methods
class TransformToGfm:
    """
    Class to provide for a transformation from markdown tokens to html for GFM.
    """

    add_trailing_text_tokens = [
        "<hr />",
        "<p>",
        "<h1>",
        "<h2>",
        "<h3>",
        "<h4>",
        "<h5>",
        "<h6>",
        "<pre>",
        "<ul>",
        "<ol>",
        '<ol start="',
    ]
    uri_autolink_html_character_escape_map = {
        "<": "&lt;",
        ">": "&gt;",
        "&": "&amp;",
    }
    raw_html_percent_escape_ascii_chars = '"%[\\]^`{}|'

    @classmethod
    def calculate_list_looseness(cls, actual_tokens, actual_token_index, next_token):
        """
        Based on the first token in a list, compute the "looseness" of the list.
        """

        is_loose = False
        current_token_index = actual_token_index + 1
        stack_count = 0
        while True:

            current_token = actual_tokens[current_token_index]
            check_me = False
            stop_me = False
            if isinstance(
                current_token,
                (UnorderedListStartMarkdownToken, OrderedListStartMarkdownToken),
            ):
                check_me = stack_count == 0
                stack_count = stack_count + 1
            elif (
                isinstance(current_token, NewListItemMarkdownToken)
                or current_token.is_block
            ):
                check_me = stack_count == 0
            elif isinstance(current_token, EndMarkdownToken) and (
                current_token.type_name == MarkdownToken.token_unordered_list_start
                or current_token.type_name == MarkdownToken.token_ordered_list_start
            ):
                if stack_count == 0:
                    stop_me = True
                else:
                    stack_count = stack_count - 1

            print(
                ">>stack_count>>"
                + str(stack_count)
                + ">>#"
                + str(current_token_index)
                + ":"
                + str(actual_tokens[current_token_index])
            )
            if check_me:
                print("check")
                if cls.is_token_loose(actual_tokens, current_token_index):
                    is_loose = True
                    stop_me = True
                    print("!!!LOOSE!!!")
            if stop_me:
                break
            current_token_index = current_token_index + 1

        assert current_token_index != len(actual_tokens)
        next_token.is_loose = is_loose
        return is_loose

    @classmethod
    def is_token_loose(cls, actual_tokens, current_token_index):
        """
        Check to see if this token inspires looseness.
        """

        token_to_check = actual_tokens[current_token_index - 1]
        print("token_to_check-->" + str(token_to_check))
        if isinstance(token_to_check, EndMarkdownToken) and (
            token_to_check.type_name == MarkdownToken.token_unordered_list_start
            or token_to_check.type_name == MarkdownToken.token_ordered_list_start
        ):
            if actual_tokens[current_token_index - 2].is_blank_line:
                token_to_check = actual_tokens[current_token_index - 2]
        print("token_to_check-->" + str(token_to_check))
        if token_to_check.is_blank_line:
            if isinstance(
                actual_tokens[current_token_index - 2],
                (
                    NewListItemMarkdownToken,
                    UnorderedListStartMarkdownToken,
                    OrderedListStartMarkdownToken,
                ),
            ):
                print("!!!Starting Blank!!!")
            else:
                print("!!!LOOSE!!!")
                return True
        return False

    @classmethod
    def find_owning_list_start(cls, actual_tokens, actual_token_index):
        """
        Figure out what the list start for the current token is.
        """

        current_index = actual_token_index
        assert not isinstance(
            actual_tokens[current_index], UnorderedListStartMarkdownToken
        ) and not isinstance(
            actual_tokens[current_index], OrderedListStartMarkdownToken
        )

        current_index = current_index - 1
        keep_going = True
        stack_count = 0
        while keep_going and current_index >= 0:
            if isinstance(
                actual_tokens[current_index],
                (UnorderedListStartMarkdownToken, OrderedListStartMarkdownToken),
            ):
                if stack_count == 0:
                    keep_going = False
                else:
                    stack_count = stack_count - 1
            elif isinstance(actual_tokens[current_index], EndMarkdownToken) and (
                actual_tokens[current_index].type_name
                == MarkdownToken.token_unordered_list_start
                or actual_tokens[current_index].type_name
                == MarkdownToken.token_ordered_list_start
            ):
                stack_count = stack_count + 1
            if keep_going:
                current_index = current_index - 1
        return current_index

    @classmethod
    def reset_list_looseness(cls, actual_tokens, actual_token_index):
        """
        Based on where we are within the actual tokens being emitted, figure
        out the correct list looseness to use.
        """

        print("!!!!!!!!!!!!!!!" + str(actual_token_index))
        search_index = actual_token_index + 1
        while search_index < len(actual_tokens):
            print("!!" + str(search_index) + "::" + str(actual_tokens[search_index]))
            if isinstance(actual_tokens[search_index], EndMarkdownToken) and (
                actual_tokens[search_index].type_name
                == MarkdownToken.token_unordered_list_start
                or actual_tokens[search_index].type_name
                == MarkdownToken.token_ordered_list_start
            ):
                break
            search_index = search_index + 1
        print("!!!!!!!!!!!!!!!" + str(search_index) + "-of-" + str(len(actual_tokens)))
        # check to see where we are, then grab the matching start to find
        # the loose
        if search_index == len(actual_tokens):
            is_in_loose_list = True
        else:
            print(">>reset_list_looseness-token_unordered_list_start>>")
            new_index = cls.find_owning_list_start(actual_tokens, search_index)
            print(">>reset_list_looseness>>" + str(new_index))
            is_in_loose_list = actual_tokens[new_index].is_loose
        print("           is_in_loose_list=" + str(is_in_loose_list))
        return is_in_loose_list

    def __init__(self):
        self.start_token_handlers = {}
        self.end_token_handlers = {}

        sample_token = ThematicBreakMarkdownToken("", "", "")
        self.register_handlers(
            sample_token.token_name, self.handle_thematic_break_token
        )
        sample_token = HardBreakMarkdownToken()
        self.register_handlers(sample_token.token_name, self.handle_hard_break_token)

        sample_token = AtxHeaderMarkdownToken("", "", "")
        self.register_handlers(
            sample_token.token_name,
            self.handle_start_atx_header_token,
            self.handle_end_atx_header_token,
        )

        sample_token = LinkStartMarkdownToken("", "")
        self.register_handlers(
            sample_token.token_name,
            self.handle_start_link_token,
            self.handle_end_link_token,
        )

        sample_token = ImageStartMarkdownToken("", "", "")
        self.register_handlers(sample_token.token_name, self.handle_image_token)

        sample_token = InlineCodeSpanMarkdownToken("")
        self.register_handlers(
            sample_token.token_name, self.handle_inline_code_span_token
        )

        sample_token = RawHtmlMarkdownToken("")
        self.register_handlers(sample_token.token_name, self.handle_raw_html_token)

        sample_token = EmailAutolinkMarkdownToken("")
        self.register_handlers(
            sample_token.token_name, self.handle_email_autolink_token
        )

        sample_token = UriAutolinkMarkdownToken("")
        self.register_handlers(sample_token.token_name, self.handle_uri_autolink)

        sample_token = SetextHeaderMarkdownToken("", "")
        self.register_handlers(
            sample_token.token_name,
            self.handle_start_setext_header_token,
            self.handle_end_setext_header_token,
        )

        sample_token = EmphasisMarkdownToken("")
        self.register_handlers(
            sample_token.token_name,
            self.handle_start_emphasis_token,
            self.handle_end_emphasis_token,
        )

        sample_token = TextMarkdownToken("", "")
        self.register_handlers(sample_token.token_name, self.handle_text_token)

        sample_token = ParagraphMarkdownToken("")
        self.register_handlers(
            sample_token.token_name,
            self.handle_start_paragraph_token,
            self.handle_end_paragraph_token,
        )

        sample_token = BlankLineMarkdownToken("")
        self.register_handlers(sample_token.token_name, self.handle_blank_line_token)

        sample_token = BlockQuoteMarkdownToken("")
        self.register_handlers(
            sample_token.token_name,
            self.handle_start_block_quote_token,
            self.handle_end_block_quote_token,
        )

        sample_token = IndentedCodeBlockMarkdownToken("")
        self.register_handlers(
            sample_token.token_name,
            self.handle_start_indented_code_block_token,
            self.handle_end_indented_code_block_token,
        )

        sample_token = FencedCodeBlockMarkdownToken("", "", "", "", "", "")
        self.register_handlers(
            sample_token.token_name,
            self.handle_start_fenced_code_block_token,
            self.handle_end_fenced_code_block_token,
        )

        sample_token = NewListItemMarkdownToken("")
        self.register_handlers(sample_token.token_name, self.handle_new_list_item_token)

        sample_token = OrderedListStartMarkdownToken("", "", "", "")
        self.register_handlers(
            sample_token.token_name,
            self.handle_start_ordered_list_token,
            self.handle_end_list_token,
        )

        sample_token = UnorderedListStartMarkdownToken("", "", "")
        self.register_handlers(
            sample_token.token_name,
            self.handle_start_unordered_list_token,
            self.handle_end_list_token,
        )
        sample_token = HtmlBlockMarkdownToken()
        self.register_handlers(
            sample_token.token_name,
            self.handle_start_html_block_token,
            self.handle_end_html_block_token,
        )

    def register_handlers(
        self, token_name, start_token_handler, end_token_handler=None
    ):
        """
        Register the handlers necessary to deal with token's start and end.
        """
        self.start_token_handlers[token_name] = start_token_handler
        if end_token_handler:
            self.end_token_handlers[token_name] = end_token_handler

    def transform(self, actual_tokens):
        """
        Transform the tokens into html.
        """
        print("\n\n---\n")
        output_html = ""
        transform_state = TransformState(actual_tokens)
        for next_token in transform_state.actual_tokens:
            transform_state.add_trailing_text = None
            transform_state.add_leading_text = None
            if next_token.token_name in self.start_token_handlers:
                start_handler_fn = self.start_token_handlers[next_token.token_name]
                output_html = start_handler_fn(output_html, next_token, transform_state)

            elif isinstance(next_token, EndMarkdownToken):
                if next_token.type_name in self.end_token_handlers:
                    end_handler_fn = self.end_token_handlers[next_token.type_name]
                    output_html = end_handler_fn(
                        output_html, next_token, transform_state
                    )
                else:
                    assert False, (
                        "Markdown token end type "
                        + next_token.type_name
                        + " not supported."
                    )
            else:
                assert False, (
                    "Markdown token type " + str(type(next_token)) + " not supported."
                )

            print("======")
            print(
                "add_trailing_text-->"
                + str(transform_state.add_trailing_text).replace("\n", "\\n")
                + "<--"
            )
            print(
                "add_leading_text -->"
                + str(transform_state.add_leading_text).replace("\n", "\\n")
                + "<--"
            )

            if transform_state.add_trailing_text:
                output_html = self.apply_trailing_text(output_html, transform_state)

            if transform_state.add_leading_text:
                output_html = self.apply_leading_text(output_html, transform_state)

            print("------")
            print("next_token     -->" + str(next_token).replace("\n", "\\n") + "<--")
            print("output_html    -->" + str(output_html).replace("\n", "\\n") + "<--")
            print(
                "transform_stack-->"
                + str(transform_state.transform_stack).replace("\n", "\\n")
                + "<--"
            )

            transform_state.actual_token_index = transform_state.actual_token_index + 1
        if output_html.endswith("\n"):
            output_html = output_html[:-1]
        return output_html

    @classmethod
    def apply_trailing_text(cls, output_html, transform_state):
        """
        Apply any trailing text to the output.
        """
        stack_text = transform_state.transform_stack.pop()

        for next_token_to_test in TransformToGfm.add_trailing_text_tokens:
            if output_html.startswith(next_token_to_test):
                output_html = "\n" + output_html
                break

        if output_html.endswith("</ul>") or output_html.endswith("</ol>"):
            output_html = output_html + "\n"
        output_html = stack_text + output_html + transform_state.add_trailing_text
        return output_html

    @classmethod
    def apply_leading_text(cls, output_html, transform_state):
        """
        Apply any leading text to the output.
        """
        if output_html and output_html[-1] != "\n":
            output_html = output_html + "\n"
        output_html = output_html + transform_state.add_leading_text
        transform_state.transform_stack.append(output_html)
        output_html = ""
        return output_html

    @classmethod
    def handle_text_token(cls, output_html, next_token, transform_state):
        """
        Handle the text token.
        """
        if transform_state.is_in_code_block:
            output_html = (
                output_html + next_token.extracted_whitespace + next_token.token_text
            )
        elif transform_state.is_in_html_block:
            output_html = (
                output_html
                + next_token.extracted_whitespace
                + next_token.token_text
                + "\n"
            )
        else:
            output_html = output_html + next_token.token_text

        return output_html

    @classmethod
    def handle_start_paragraph_token(cls, output_html, next_token, transform_state):
        """
        Handle the start paragraph token.
        """
        assert next_token
        if transform_state.is_in_loose_list:
            if output_html and output_html[-1] != "\n":
                output_html = output_html + "\n"
            output_html = output_html + "<p>"
        return output_html

    @classmethod
    def handle_end_paragraph_token(cls, output_html, next_token, transform_state):
        """
        Handle the end paragraph token.
        """
        assert next_token
        if transform_state.is_in_loose_list:
            output_html = output_html + "</p>\n"
        return output_html

    @classmethod
    def handle_blank_line_token(cls, output_html, next_token, transform_state):
        """
        Handle the black line token.
        """
        if transform_state.is_in_fenced_code_block:
            output_html = output_html + next_token.extracted_whitespace + "\n"
        elif transform_state.is_in_html_block:
            output_html = output_html + "\n"
        return output_html

    @classmethod
    def handle_start_block_quote_token(cls, output_html, next_token, transform_state):
        """
        Handle the start block quote token.
        """
        assert next_token
        if output_html and not output_html.endswith("\n"):
            output_html = output_html + "\n"
        output_html = output_html + "<blockquote>\n"
        transform_state.is_in_loose_list = True
        return output_html

    def handle_end_block_quote_token(self, output_html, next_token, transform_state):
        """
        Handle the end block quote token.
        """
        assert next_token
        if output_html[-1] != "\n":
            output_html = output_html + "\n"
        output_html = output_html + "</blockquote>\n"
        transform_state.is_in_loose_list = self.reset_list_looseness(
            transform_state.actual_tokens, transform_state.actual_token_index,
        )
        return output_html

    @classmethod
    def handle_start_indented_code_block_token(
        cls, output_html, next_token, transform_state
    ):
        """
        Handle the start indented code block token.
        """
        assert next_token
        if (
            not output_html
            and transform_state.transform_stack
            and transform_state.transform_stack[-1].endswith("<li>")
        ):
            output_html = "\n"
        elif output_html and output_html[-1] != "\n":
            output_html = output_html + "\n"
        output_html = output_html + "<pre><code>"
        transform_state.is_in_code_block = True
        transform_state.is_in_fenced_code_block = False
        return output_html

    @classmethod
    def handle_end_indented_code_block_token(
        cls, output_html, next_token, transform_state
    ):
        """
        Handle the end indented code block token.
        """
        assert next_token
        transform_state.is_in_code_block = False
        output_html = output_html + "\n</code></pre>\n"
        return output_html

    @classmethod
    def handle_start_fenced_code_block_token(
        cls, output_html, next_token, transform_state
    ):
        """
        Handle the start fenced code block token.
        """
        inner_tag = ""
        if next_token.extracted_text:
            inner_tag = ' class="language-' + next_token.extracted_text + '"'
        output_html = output_html + "<pre><code" + inner_tag + ">"
        transform_state.is_in_code_block = True
        transform_state.is_in_fenced_code_block = True
        return output_html

    @classmethod
    def handle_end_fenced_code_block_token(
        cls, output_html, next_token, transform_state
    ):
        """
        Handle the end fenced code block token.
        """
        assert next_token
        fenced_token = transform_state.actual_token_index - 1
        while not transform_state.actual_tokens[fenced_token].is_fenced_code_block:
            fenced_token = fenced_token - 1

        inner_tag = ""
        if transform_state.actual_tokens[fenced_token].extracted_text:
            inner_tag = (
                ' class="language-'
                + transform_state.actual_tokens[fenced_token].extracted_text
                + '"'
            )
        inner_tag = "<code" + inner_tag + ">"

        if not output_html.endswith(inner_tag) and output_html[-1] != "\n":
            output_html = output_html + "\n"
        elif (
            output_html[-1] == "\n"
            and transform_state.actual_tokens[
                transform_state.actual_token_index - 1
            ].is_text
        ):
            output_html = output_html + "\n"
        output_html = output_html + "</code></pre>\n"
        transform_state.is_in_code_block = False
        transform_state.is_in_fenced_code_block = False
        return output_html

    @classmethod
    def handle_thematic_break_token(cls, output_html, next_token, transform_state):
        """
        Handle the thematic break token.
        """
        assert next_token.token_name == MarkdownToken.token_thematic_break
        assert transform_state

        if output_html and output_html[-1] != "\n":
            output_html = output_html + "\n"
        output_html = output_html + "<hr />\n"
        return output_html

    @classmethod
    def handle_hard_break_token(cls, output_html, next_token, transform_state):
        """
        Handle the hard line break token.
        """
        assert next_token.token_name == MarkdownToken.token_inline_hard_break
        assert transform_state
        output_html = output_html + "<br />"
        return output_html

    @classmethod
    def handle_start_atx_header_token(cls, output_html, next_token, transform_state):
        """
        Handle the start atx header token.
        """
        assert transform_state
        output_html = output_html + "<h" + str(next_token.hash_count) + ">"
        return output_html

    @classmethod
    def handle_end_atx_header_token(cls, output_html, next_token, transform_state):
        """
        Handle the end atx header token.
        """
        assert next_token
        fenced_token = transform_state.actual_token_index - 1
        while not transform_state.actual_tokens[fenced_token].is_atx_header:
            fenced_token = fenced_token - 1

        output_html = (
            output_html
            + "</h"
            + str(transform_state.actual_tokens[fenced_token].hash_count)
            + ">\n"
        )
        return output_html

    @classmethod
    def handle_start_setext_header_token(cls, output_html, next_token, transform_state):
        """
        Handle the start setext header token.
        """
        assert transform_state
        if next_token.header_character == "=":
            inner_tag = "1"
        else:
            inner_tag = "2"
        output_html = output_html + "<h" + inner_tag + ">"
        return output_html

    @classmethod
    def handle_end_setext_header_token(cls, output_html, next_token, transform_state):
        """
        Handle the end setext header token.
        """
        assert next_token
        fenced_token = transform_state.actual_token_index - 1
        while not transform_state.actual_tokens[fenced_token].is_setext:
            fenced_token = fenced_token - 1
        if transform_state.actual_tokens[fenced_token].header_character == "=":
            inner_tag = "1"
        else:
            inner_tag = "2"

        output_html = output_html + "</h" + inner_tag + ">\n"
        return output_html

    @classmethod
    def handle_new_list_item_token(cls, output_html, next_token, transform_state):
        """
        Handle the new list item token.
        """
        assert next_token
        if output_html.endswith(">"):
            output_html = output_html + "\n"
        transform_state.add_trailing_text = "</li>"
        transform_state.add_leading_text = "<li>"
        return output_html

    @classmethod
    def handle_inline_code_span_token(cls, output_html, next_token, transform_state):
        """
        Handle the code span token.
        """
        assert transform_state
        output_html = output_html + "<code>" + next_token.span_text + "</code>"
        return output_html

    @classmethod
    def handle_raw_html_token(cls, output_html, next_token, transform_state):
        """
        Handle the raw html token.
        """
        assert transform_state
        output_html = output_html + "<" + next_token.raw_tag + ">"
        return output_html

    @classmethod
    def handle_email_autolink_token(cls, output_html, next_token, transform_state):
        """
        Handle the email autolink token.
        """
        assert transform_state
        output_html = (
            output_html
            + '<a href="mailto:'
            + next_token.autolink_text
            + '">'
            + next_token.autolink_text
            + "</a>"
        )
        return output_html

    def handle_start_ordered_list_token(
        self, output_html, next_token, transform_state,
    ):
        """
        Handle the start ordered list token.
        """
        transform_state.is_in_loose_list = self.calculate_list_looseness(
            transform_state.actual_tokens,
            transform_state.actual_token_index,
            next_token,
        )
        ostart_attribute = ""
        if next_token.list_start_content != "1":
            list_start = int(next_token.list_start_content)
            ostart_attribute = ' start="' + str(list_start) + '"'
        transform_state.add_leading_text = "<ol" + ostart_attribute + ">\n<li>"
        return output_html

    def handle_start_unordered_list_token(
        self, output_html, next_token, transform_state,
    ):
        """
        Handle the start unordered list token.
        """
        transform_state.is_in_loose_list = self.calculate_list_looseness(
            transform_state.actual_tokens,
            transform_state.actual_token_index,
            next_token,
        )
        transform_state.add_leading_text = "<ul>\n<li>"
        return output_html

    def handle_end_list_token(
        self, output_html, next_token, transform_state,
    ):
        """
        Handle the end list token for either an ordered or unordered list.
        """
        transform_state.is_in_loose_list = self.reset_list_looseness(
            transform_state.actual_tokens, transform_state.actual_token_index,
        )
        if next_token.type_name == MarkdownToken.token_unordered_list_start:
            transform_state.add_trailing_text = "</li>\n</ul>"
        else:
            transform_state.add_trailing_text = "</li>\n</ol>"
        return output_html

    @classmethod
    def handle_uri_autolink(cls, output_html, next_token, transform_state):
        """
        Handle the uri autolink token.
        """
        assert transform_state
        in_tag_pretext = InlineHelper.append_text(
            "",
            next_token.autolink_text,
            alternate_escape_map=TransformToGfm.uri_autolink_html_character_escape_map,
        )
        in_tag_text = ""
        for next_character in in_tag_pretext:
            if next_character in TransformToGfm.raw_html_percent_escape_ascii_chars:
                in_tag_text = in_tag_text + "%" + (hex(ord(next_character))[2:]).upper()
            elif ord(next_character) >= 128:
                encoded_data = next_character.encode("utf8")
                for encoded_byte in encoded_data:
                    in_tag_text = in_tag_text + "%" + (hex(encoded_byte)[2:]).upper()
            else:
                in_tag_text = in_tag_text + next_character

        in_anchor_text = InlineHelper.append_text("", next_token.autolink_text)

        output_html = (
            output_html + '<a href="' + in_tag_text + '">' + in_anchor_text + "</a>"
        )
        return output_html

    @classmethod
    def handle_start_html_block_token(cls, output_html, next_token, transform_state):
        """
        Handle the start html block token.
        """
        assert next_token
        transform_state.is_in_html_block = True
        if (
            not output_html
            and transform_state.transform_stack
            and transform_state.transform_stack[-1].endswith("<li>")
        ):
            output_html = "\n"
        else:
            previous_token = transform_state.actual_tokens[
                transform_state.actual_token_index - 1
            ]
            if isinstance(previous_token, EndMarkdownToken) and (
                previous_token.type_name == MarkdownToken.token_unordered_list_start
                or previous_token.type_name == MarkdownToken.token_ordered_list_start
            ):
                output_html = output_html + "\n"
        return output_html

    @classmethod
    def handle_end_html_block_token(cls, output_html, next_token, transform_state):
        """
        Handle the end html block token.
        """
        assert next_token
        transform_state.is_in_html_block = False
        return output_html

    @classmethod
    def handle_start_emphasis_token(cls, output_html, next_token, transform_state):
        """
        Handle the start emphasis token.
        """
        assert transform_state
        if next_token.emphasis_length == 1:
            output_html = output_html + "<em>"
        else:
            output_html = output_html + "<strong>"
        return output_html

    @classmethod
    def handle_end_emphasis_token(cls, output_html, next_token, transform_state):
        """
        Handle the end emphasis token.
        """
        assert transform_state
        if next_token.extra_end_data == "1":
            output_html = output_html + "</em>"
        else:
            output_html = output_html + "</strong>"
        return output_html

    @classmethod
    def handle_start_link_token(cls, output_html, next_token, transform_state):
        """
        Handle the start link token.
        """
        assert transform_state
        anchor_tag = '<a href="' + next_token.link_uri
        if next_token.link_title:
            anchor_tag = anchor_tag + '" title="' + next_token.link_title
        anchor_tag = anchor_tag + '">'
        output_html = output_html + anchor_tag
        return output_html

    @classmethod
    def handle_end_link_token(cls, output_html, next_token, transform_state):
        """
        Handle the end link token.
        """
        assert next_token
        assert transform_state
        output_html = output_html + "</a>"
        return output_html

    @classmethod
    def handle_image_token(cls, output_html, next_token, transform_state):
        """
        Handle the image token.
        """
        assert transform_state
        output_html = output_html + "<img "
        output_html = output_html + 'src="' + next_token.image_uri + '" '
        output_html = output_html + 'alt="' + next_token.image_alt_text + '" '
        if next_token.image_title:
            output_html = output_html + 'title="' + next_token.image_title + '" '
        output_html = output_html + "/>"
        return output_html


# pylint: enable=too-few-public-methods
