"""
Module to provide for a transformation from markdown tokens to html for GFM.
"""
import inspect
import logging

from pymarkdown.container_markdown_token import (
    BlockQuoteMarkdownToken,
    NewListItemMarkdownToken,
    OrderedListStartMarkdownToken,
    UnorderedListStartMarkdownToken,
)
from pymarkdown.inline_helper import InlineHelper
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
from pymarkdown.markdown_token import MarkdownToken
from pymarkdown.parser_helper import ParserHelper
from pymarkdown.parser_logger import ParserLogger
from pymarkdown.transform_to_gfm_list_looseness import TransformToGfmListLooseness

POGGER = ParserLogger(logging.getLogger(__name__))


# pylint: disable=too-many-instance-attributes, too-few-public-methods
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
        self.next_token = None
        self.last_token = None


# pylint: enable=too-many-instance-attributes, too-few-public-methods


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

    def __init__(self):
        self.start_token_handlers = {}
        self.end_token_handlers = {}

        self.register_handlers(
            ThematicBreakMarkdownToken, self.__handle_thematic_break_token
        )
        self.register_handlers(HardBreakMarkdownToken, self.__handle_hard_break_token)
        self.register_handlers(
            AtxHeadingMarkdownToken,
            self.__handle_start_atx_heading_token,
            self.__handle_end_atx_heading_token,
        )
        self.register_handlers(
            LinkStartMarkdownToken,
            self.__handle_start_link_token,
            self.__handle_end_link_token,
        )
        self.register_handlers(ImageStartMarkdownToken, self.__handle_image_token)
        self.register_handlers(
            InlineCodeSpanMarkdownToken, self.__handle_inline_code_span_token
        )
        self.register_handlers(RawHtmlMarkdownToken, self.__handle_raw_html_token)
        self.register_handlers(
            EmailAutolinkMarkdownToken, self.__handle_email_autolink_token
        )
        self.register_handlers(UriAutolinkMarkdownToken, self.__handle_uri_autolink)
        self.register_handlers(
            SetextHeadingMarkdownToken,
            self.__handle_start_setext_heading_token,
            self.__handle_end_setext_heading_token,
        )
        self.register_handlers(
            EmphasisMarkdownToken,
            self.__handle_start_emphasis_token,
            self.__handle_end_emphasis_token,
        )
        self.register_handlers(TextMarkdownToken, self.__handle_text_token)
        self.register_handlers(
            ParagraphMarkdownToken,
            self.__handle_start_paragraph_token,
            self.__handle_end_paragraph_token,
        )
        self.register_handlers(BlankLineMarkdownToken, self.__handle_blank_line_token)
        self.register_handlers(
            BlockQuoteMarkdownToken,
            self.__handle_start_block_quote_token,
            self.__handle_end_block_quote_token,
        )
        self.register_handlers(
            IndentedCodeBlockMarkdownToken,
            self.__handle_start_indented_code_block_token,
            self.__handle_end_indented_code_block_token,
        )
        self.register_handlers(
            FencedCodeBlockMarkdownToken,
            self.__handle_start_fenced_code_block_token,
            self.__handle_end_fenced_code_block_token,
        )
        self.register_handlers(
            NewListItemMarkdownToken, self.__handle_new_list_item_token
        )
        self.register_handlers(
            OrderedListStartMarkdownToken,
            self.__handle_start_list_token,
            self.__handle_end_list_token,
        )
        self.register_handlers(
            UnorderedListStartMarkdownToken,
            self.__handle_start_list_token,
            self.__handle_end_list_token,
        )
        self.register_handlers(
            HtmlBlockMarkdownToken,
            self.__handle_start_html_block_token,
            self.__handle_end_html_block_token,
        )
        self.register_handlers(
            LinkReferenceDefinitionMarkdownToken,
            self.__handle_link_reference_definition_token,
        )

    def register_handlers(self, type_name, start_token_handler, end_token_handler=None):
        """
        Register the handlers necessary to deal with token's start and end.
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

        self.start_token_handlers[handler_instance.token_name] = start_token_handler
        if end_token_handler:
            self.end_token_handlers[handler_instance.token_name] = end_token_handler

    def transform(self, actual_tokens):
        """
        Transform the tokens into html.
        """
        POGGER.debug("\n\n---\n")
        output_html = ""
        transform_state = TransformState(actual_tokens)
        actual_tokens_size = len(actual_tokens)
        for next_token in transform_state.actual_tokens:
            transform_state.add_trailing_text = None
            transform_state.add_leading_text = None
            transform_state.next_token = None
            if (transform_state.actual_token_index + 1) < actual_tokens_size:
                transform_state.next_token = actual_tokens[
                    transform_state.actual_token_index + 1
                ]
            if next_token.token_name in self.start_token_handlers:
                start_handler_fn = self.start_token_handlers[next_token.token_name]
                output_html = start_handler_fn(output_html, next_token, transform_state)

            elif next_token.is_end_token:
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

            POGGER.debug("======")
            POGGER.debug(
                "add_trailing_text-->$<--",
                transform_state.add_trailing_text,
            )
            POGGER.debug("add_leading_text -->$<--", transform_state.add_leading_text)

            if transform_state.add_trailing_text:
                output_html = self.__apply_trailing_text(output_html, transform_state)

            if transform_state.add_leading_text:
                output_html = self.__apply_leading_text(output_html, transform_state)

            POGGER.debug("------")
            POGGER.debug("next_token     -->$<--", next_token)
            POGGER.debug("output_html    -->$<--", output_html)
            POGGER.debug("transform_stack-->$<--", transform_state.transform_stack)

            transform_state.last_token = next_token
            transform_state.actual_token_index += 1
        if output_html.endswith(ParserHelper.newline_character):
            output_html = output_html[:-1]
        return output_html

    @classmethod
    def __apply_trailing_text(cls, output_html, transform_state):
        """
        Apply any trailing text to the output.
        """
        stack_text = transform_state.transform_stack.pop()

        for next_token_to_test in TransformToGfm.add_trailing_text_tokens:
            if output_html.startswith(next_token_to_test):
                output_html = ParserHelper.newline_character + output_html
                break

        if output_html.endswith("</ul>") or output_html.endswith("</ol>"):
            output_html += ParserHelper.newline_character
        return stack_text + output_html + transform_state.add_trailing_text

    @classmethod
    def __apply_leading_text(cls, output_html, transform_state):
        """
        Apply any leading text to the output.
        """
        if output_html and output_html[-1] != ParserHelper.newline_character:
            output_html += ParserHelper.newline_character
        output_html += transform_state.add_leading_text
        transform_state.transform_stack.append(output_html)
        return ""

    @classmethod
    def __handle_text_token(cls, output_html, next_token, transform_state):
        """
        Handle the text token.
        """
        adjusted_text_token = ParserHelper.resolve_all_from_text(next_token.token_text)

        if transform_state.is_in_code_block:
            if transform_state.is_in_fenced_code_block:
                if transform_state.last_token.is_blank_line:
                    if transform_state.actual_tokens[
                        transform_state.actual_token_index - 2
                    ].is_blank_line:
                        output_html += ParserHelper.newline_character

            extracted_whitespace = ParserHelper.resolve_all_from_text(
                next_token.extracted_whitespace
            )
            output_html += extracted_whitespace + adjusted_text_token
        elif transform_state.is_in_html_block:
            output_html += (
                next_token.extracted_whitespace
                + adjusted_text_token
                + ParserHelper.newline_character
            )
        else:
            output_html += adjusted_text_token

        return output_html

    @classmethod
    def __handle_start_paragraph_token(cls, output_html, next_token, transform_state):
        """
        Handle the start paragraph token.
        """
        _ = next_token

        if output_html and output_html[-1] != ParserHelper.newline_character:
            output_html += ParserHelper.newline_character
        if transform_state.is_in_loose_list:
            output_html += "<p>"
        return output_html

    @classmethod
    def __handle_end_paragraph_token(cls, output_html, next_token, transform_state):
        """
        Handle the end paragraph token.
        """
        _ = next_token

        if transform_state.is_in_loose_list:
            output_html += "</p>" + ParserHelper.newline_character
        return output_html

    @classmethod
    def __handle_blank_line_token(cls, output_html, next_token, transform_state):
        """
        Handle the black line token.
        """
        if transform_state.is_in_fenced_code_block:
            primary_condition = (
                not transform_state.last_token.is_fenced_code_block
                or not transform_state.next_token.is_blank_line
            )
            exclusion_condition = (
                transform_state.last_token.is_fenced_code_block
                and transform_state.next_token.is_fenced_code_block_end
            )
            if primary_condition and not exclusion_condition:
                output_html += (
                    ParserHelper.newline_character + next_token.extracted_whitespace
                )
            else:
                output_html += next_token.extracted_whitespace
        elif transform_state.is_in_html_block:
            output_html += ParserHelper.newline_character
        return output_html

    @classmethod
    def __handle_start_block_quote_token(cls, output_html, next_token, transform_state):
        """
        Handle the start block quote token.
        """
        _ = next_token

        if output_html and not output_html.endswith(ParserHelper.newline_character):
            output_html += ParserHelper.newline_character
        transform_state.is_in_loose_list = True
        return output_html + "<blockquote>" + ParserHelper.newline_character

    @classmethod
    def __handle_end_block_quote_token(cls, output_html, next_token, transform_state):
        """
        Handle the end block quote token.
        """
        _ = next_token

        if output_html[-1] != ParserHelper.newline_character:
            output_html += ParserHelper.newline_character
        transform_state.is_in_loose_list = (
            TransformToGfmListLooseness.reset_list_looseness(
                transform_state.actual_tokens,
                transform_state.actual_token_index,
            )
        )
        return output_html + "</blockquote>" + ParserHelper.newline_character

    @classmethod
    def __handle_start_indented_code_block_token(
        cls, output_html, next_token, transform_state
    ):
        """
        Handle the start indented code block token.
        """
        _ = next_token

        if (
            not output_html
            and transform_state.transform_stack
            and transform_state.transform_stack[-1].endswith("<li>")
        ):
            output_html = ParserHelper.newline_character
        elif output_html and output_html[-1] != ParserHelper.newline_character:
            output_html += ParserHelper.newline_character
        transform_state.is_in_code_block = True
        transform_state.is_in_fenced_code_block = False
        return output_html + "<pre><code>"

    @classmethod
    def __handle_end_indented_code_block_token(
        cls, output_html, next_token, transform_state
    ):
        """
        Handle the end indented code block token.
        """
        _ = next_token

        transform_state.is_in_code_block = False
        return output_html + (
            ParserHelper.newline_character
            + "</code></pre>"
            + ParserHelper.newline_character
        )

    @classmethod
    def __handle_start_fenced_code_block_token(
        cls, output_html, next_token, transform_state
    ):
        """
        Handle the start fenced code block token.
        """
        inner_tag = ""
        if next_token.extracted_text:
            inner_tag = ' class="language-' + next_token.extracted_text + '"'

        if output_html.endswith("</ol>") or output_html.endswith("</ul>"):
            output_html += ParserHelper.newline_character
        elif output_html and output_html[-1] != ParserHelper.newline_character:
            output_html += ParserHelper.newline_character
        transform_state.is_in_code_block = True
        transform_state.is_in_fenced_code_block = True
        return output_html + "<pre><code" + inner_tag + ">"

    @classmethod
    def __handle_end_fenced_code_block_token(
        cls, output_html, next_token, transform_state
    ):
        """
        Handle the end fenced code block token.
        """
        fenced_token = transform_state.actual_token_index - 1
        while not transform_state.actual_tokens[fenced_token].is_fenced_code_block:
            fenced_token -= 1

        inner_tag = ""
        if transform_state.actual_tokens[fenced_token].extracted_text:
            inner_tag = (
                ' class="language-'
                + transform_state.actual_tokens[fenced_token].extracted_text
                + '"'
            )
        inner_tag = "<code" + inner_tag + ">"

        POGGER.debug("inner_tag>>:" + inner_tag + ":<<")
        POGGER.debug("output_html>>:" + output_html + ":<<")
        POGGER.debug(
            "last_token>>:"
            + str(transform_state.actual_tokens[transform_state.actual_token_index - 1])
            + ":<<"
        )
        if (
            not output_html.endswith(inner_tag)
            and output_html[-1] != ParserHelper.newline_character
        ):
            output_html += ParserHelper.newline_character
            POGGER.debug("#1")
        elif (
            output_html[-1] == ParserHelper.newline_character
            and transform_state.last_token.is_text
        ):
            POGGER.debug("#2")
            output_html += ParserHelper.newline_character
        elif transform_state.last_token.is_blank_line:
            POGGER.debug("#3?")
            if not next_token.was_forced:
                POGGER.debug("#3")
                output_html += ParserHelper.newline_character
        transform_state.is_in_code_block = False
        transform_state.is_in_fenced_code_block = False
        return output_html + "</code></pre>" + ParserHelper.newline_character

    @classmethod
    def __handle_thematic_break_token(cls, output_html, next_token, transform_state):
        """
        Handle the thematic break token.
        """
        _ = (next_token, transform_state)

        if output_html and output_html[-1] != ParserHelper.newline_character:
            output_html += ParserHelper.newline_character
        return output_html + "<hr />" + ParserHelper.newline_character

    @classmethod
    def __handle_hard_break_token(cls, output_html, next_token, transform_state):
        """
        Handle the hard line break token.
        """
        _ = (next_token, transform_state)

        return output_html + "<br />"

    @classmethod
    def __handle_start_atx_heading_token(cls, output_html, next_token, transform_state):
        """
        Handle the start atx heading token.
        """
        previous_token = transform_state.actual_tokens[
            transform_state.actual_token_index - 1
        ]

        if output_html.endswith("</ol>") or output_html.endswith("</ul>"):
            output_html += ParserHelper.newline_character
        elif previous_token.is_paragraph_end:
            if not transform_state.is_in_loose_list:
                output_html += ParserHelper.newline_character
        return output_html + "<h" + str(next_token.hash_count) + ">"

    @classmethod
    def __handle_end_atx_heading_token(cls, output_html, next_token, transform_state):
        """
        Handle the end atx heading token.
        """
        _ = next_token

        fenced_token = transform_state.actual_token_index - 1
        while not transform_state.actual_tokens[fenced_token].is_atx_heading:
            fenced_token -= 1

        return output_html + (
            "</h"
            + str(transform_state.actual_tokens[fenced_token].hash_count)
            + ">"
            + ParserHelper.newline_character
        )

    @classmethod
    def __handle_start_setext_heading_token(
        cls, output_html, next_token, transform_state
    ):
        """
        Handle the start setext heading token.
        """
        _ = transform_state

        if next_token.heading_character == "=":
            inner_tag = "1"
        else:
            inner_tag = "2"

        if output_html.endswith("</ol>") or output_html.endswith("</ul>"):
            output_html += ParserHelper.newline_character
        return output_html + "<h" + inner_tag + ">"

    @classmethod
    def __handle_end_setext_heading_token(
        cls, output_html, next_token, transform_state
    ):
        """
        Handle the end setext heading token.
        """
        _ = next_token

        fenced_token = transform_state.actual_token_index - 1
        while not transform_state.actual_tokens[fenced_token].is_setext_heading:
            fenced_token -= 1
        if transform_state.actual_tokens[fenced_token].heading_character == "=":
            inner_tag = "1"
        else:
            inner_tag = "2"

        return output_html + "</h" + inner_tag + ">" + ParserHelper.newline_character

    @classmethod
    def __handle_new_list_item_token(cls, output_html, next_token, transform_state):
        """
        Handle the new list item token.
        """
        _ = next_token

        if output_html.endswith(">"):
            output_html += ParserHelper.newline_character
        transform_state.add_trailing_text = "</li>"
        transform_state.add_leading_text = "<li>"
        return output_html

    @classmethod
    def __handle_inline_code_span_token(cls, output_html, next_token, transform_state):
        """
        Handle the code span token.
        """
        _ = transform_state

        adjusted_text = ParserHelper.resolve_all_from_text(next_token.span_text)

        return output_html + "<code>" + adjusted_text + "</code>"

    @classmethod
    def __handle_raw_html_token(cls, output_html, next_token, transform_state):
        """
        Handle the raw html token.
        """
        _ = transform_state

        adjusted_text = ParserHelper.resolve_all_from_text(next_token.raw_tag)

        return output_html + "<" + adjusted_text + ">"

    @classmethod
    def __handle_link_reference_definition_token(
        cls, output_html, next_token, transform_state
    ):
        """
        Handle the link reference definition token.
        """
        _ = (transform_state, next_token)

        return output_html

    @classmethod
    def __handle_email_autolink_token(cls, output_html, next_token, transform_state):
        """
        Handle the email autolink token.
        """
        _ = transform_state

        return (
            output_html
            + '<a href="mailto:'
            + next_token.autolink_text
            + '">'
            + next_token.autolink_text
            + "</a>"
        )

    @classmethod
    def __handle_start_list_token(
        cls,
        output_html,
        next_token,
        transform_state,
    ):
        """
        Handle the start unordered list token.
        """
        transform_state.is_in_loose_list = (
            TransformToGfmListLooseness.calculate_list_looseness(
                transform_state.actual_tokens,
                transform_state.actual_token_index,
                next_token,
            )
        )
        if next_token.is_ordered_list_start:
            ostart_attribute = ""
            if next_token.list_start_content != "1":
                list_start = int(next_token.list_start_content)
                ostart_attribute = ' start="' + str(list_start) + '"'
            transform_state.add_leading_text = (
                "<ol" + ostart_attribute + ">" + ParserHelper.newline_character + "<li>"
            )
        else:
            transform_state.add_leading_text = (
                "<ul>" + ParserHelper.newline_character + "<li>"
            )
        return output_html

    @classmethod
    def __handle_end_list_token(
        cls,
        output_html,
        next_token,
        transform_state,
    ):
        """
        Handle the end list token for either an ordered or unordered list.
        """
        transform_state.is_in_loose_list = (
            TransformToGfmListLooseness.reset_list_looseness(
                transform_state.actual_tokens,
                transform_state.actual_token_index,
            )
        )
        if next_token.is_unordered_list_end:
            transform_state.add_trailing_text = (
                "</li>" + ParserHelper.newline_character + "</ul>"
            )
        else:
            transform_state.add_trailing_text = (
                "</li>" + ParserHelper.newline_character + "</ol>"
            )
        return output_html

    @classmethod
    def __handle_uri_autolink(cls, output_html, next_token, transform_state):
        """
        Handle the uri autolink token.
        """
        _ = transform_state

        in_tag_pretext = InlineHelper.append_text(
            "",
            next_token.autolink_text,
            alternate_escape_map=TransformToGfm.uri_autolink_html_character_escape_map,
            add_text_signature=False,
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

        in_anchor_text = InlineHelper.append_text(
            "", next_token.autolink_text, add_text_signature=False
        )

        return output_html + '<a href="' + in_tag_text + '">' + in_anchor_text + "</a>"

    @classmethod
    def __handle_start_html_block_token(cls, output_html, next_token, transform_state):
        """
        Handle the start html block token.
        """
        _ = next_token

        transform_state.is_in_html_block = True
        if (
            not output_html
            and transform_state.transform_stack
            and transform_state.transform_stack[-1].endswith("<li>")
        ):
            output_html = ParserHelper.newline_character
        else:
            previous_token = transform_state.actual_tokens[
                transform_state.actual_token_index - 1
            ]
            POGGER.debug(">previous_token>$>", previous_token)
            if previous_token.is_list_end:
                output_html += ParserHelper.newline_character
            elif previous_token.is_paragraph_end:
                if not transform_state.is_in_loose_list:
                    output_html += ParserHelper.newline_character
        return output_html

    @classmethod
    def __handle_end_html_block_token(cls, output_html, next_token, transform_state):
        """
        Handle the end html block token.
        """
        _ = next_token

        transform_state.is_in_html_block = False
        return output_html

    @classmethod
    def __handle_start_emphasis_token(cls, output_html, next_token, transform_state):
        """
        Handle the start emphasis token.
        """
        _ = transform_state

        if next_token.emphasis_length == 1:
            output_html += "<em>"
        else:
            output_html += "<strong>"
        return output_html

    @classmethod
    def __handle_end_emphasis_token(cls, output_html, next_token, transform_state):
        """
        Handle the end emphasis token.
        """
        _ = transform_state

        if next_token.start_markdown_token.emphasis_length == 1:
            output_html += "</em>"
        else:
            output_html += "</strong>"
        return output_html

    @classmethod
    def __handle_start_link_token(cls, output_html, next_token, transform_state):
        """
        Handle the start link token.
        """
        _ = transform_state

        anchor_tag = '<a href="' + next_token.link_uri
        if next_token.link_title:
            anchor_tag += '" title="' + next_token.link_title
        anchor_tag += '">'
        return output_html + anchor_tag

    @classmethod
    def __handle_end_link_token(cls, output_html, next_token, transform_state):
        """
        Handle the end link token.
        """
        _ = (next_token, transform_state)

        return output_html + "</a>"

    @classmethod
    def __handle_image_token(cls, output_html, next_token, transform_state):
        """
        Handle the image token.
        """
        _ = transform_state

        output_html += (
            '<img src="'
            + next_token.link_uri
            + '" alt="'
            + next_token.image_alt_text
            + '" '
        )
        if next_token.link_title:
            output_html += 'title="' + next_token.link_title + '" '
        return output_html + "/>"
