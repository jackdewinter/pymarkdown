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
        (
            self.is_in_code_block,
            self.is_in_fenced_code_block,
            self.is_in_html_block,
            self.is_in_loose_list,
            self.transform_stack,
            self.add_trailing_text,
            self.add_leading_text,
            self.actual_tokens,
            self.actual_token_index,
            self.next_token,
            self.last_token,
        ) = (False, False, False, True, [], None, None, actual_tokens, 0, None, None)


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
        self.start_token_handlers, self.end_token_handlers = {}, {}

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
        assert issubclass(
            type_name, MarkdownToken
        ), f"Token class '{str(type_name)}' must be descended from the 'MarkdownToken' class."
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
        transform_state, output_html, actual_tokens_size = (
            TransformState(actual_tokens),
            "",
            len(actual_tokens),
        )
        for next_token in transform_state.actual_tokens:
            (
                transform_state.add_trailing_text,
                transform_state.add_leading_text,
                transform_state.next_token,
            ) = (None, None, None)
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
                    assert (
                        False
                    ), f"Markdown token end type {next_token.type_name} not supported."
            else:
                assert (
                    False
                ), f"Markdown token type {str(type(next_token))} not supported."

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
        if output_html and output_html[-1] == ParserHelper.newline_character:
            output_html = output_html[:-1]
        return output_html

    @classmethod
    def __apply_trailing_text(cls, output_html, transform_state):
        """
        Apply any trailing text to the output.
        """
        stack_text = transform_state.transform_stack.pop()
        trailing_part = [stack_text]
        for next_token_to_test in TransformToGfm.add_trailing_text_tokens:
            if output_html.startswith(next_token_to_test):
                trailing_part.append(ParserHelper.newline_character)
                break

        trailing_part.append(output_html)
        if output_html.endswith("</ul>") or output_html.endswith("</ol>"):
            trailing_part.append(ParserHelper.newline_character)
        trailing_part.append(transform_state.add_trailing_text)
        return "".join(trailing_part)

    @classmethod
    def __apply_leading_text(cls, output_html, transform_state):
        """
        Apply any leading text to the output.
        """

        output_html = (
            f"{output_html}{ParserHelper.newline_character}{transform_state.add_leading_text}"
            if output_html and output_html[-1] != ParserHelper.newline_character
            else f"{output_html}{transform_state.add_leading_text}"
        )
        transform_state.transform_stack.append(output_html)
        return ""

    @classmethod
    def __handle_text_token(cls, output_html, next_token, transform_state):
        """
        Handle the text token.
        """
        adjusted_text_token = ParserHelper.resolve_all_from_text(next_token.token_text)

        token_parts = []
        if transform_state.is_in_code_block:
            if transform_state.is_in_fenced_code_block:
                if transform_state.last_token.is_blank_line:
                    if transform_state.actual_tokens[
                        transform_state.actual_token_index - 2
                    ].is_blank_line:
                        token_parts.append(ParserHelper.newline_character)

            token_parts.extend(
                [
                    ParserHelper.resolve_all_from_text(next_token.extracted_whitespace),
                    adjusted_text_token,
                ]
            )
        elif transform_state.is_in_html_block:
            token_parts.extend(
                [
                    next_token.extracted_whitespace,
                    adjusted_text_token,
                    ParserHelper.newline_character,
                ]
            )
        else:
            token_parts.append(adjusted_text_token)

        token_parts.insert(0, output_html)
        return "".join(token_parts)

    @classmethod
    def __handle_start_paragraph_token(cls, output_html, next_token, transform_state):
        """
        Handle the start paragraph token.
        """
        _ = next_token
        token_parts = [output_html]
        if output_html and output_html[-1] != ParserHelper.newline_character:
            token_parts.append(ParserHelper.newline_character)
        if transform_state.is_in_loose_list:
            token_parts.append("<p>")
        return "".join(token_parts)

    @classmethod
    def __handle_end_paragraph_token(cls, output_html, next_token, transform_state):
        """
        Handle the end paragraph token.
        """
        _ = next_token

        return (
            f"{output_html}</p>{ParserHelper.newline_character}"
            if transform_state.is_in_loose_list
            else output_html
        )

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
            output_html = (
                f"{output_html}{ParserHelper.newline_character}{next_token.extracted_whitespace}"
                if primary_condition and not exclusion_condition
                else f"{output_html}{next_token.extracted_whitespace}"
            )
        elif transform_state.is_in_html_block:
            output_html = f"{output_html}{ParserHelper.newline_character}"
        return output_html

    @classmethod
    def __handle_start_block_quote_token(cls, output_html, next_token, transform_state):
        """
        Handle the start block quote token.
        """
        _ = next_token

        token_parts = [output_html]
        if output_html and not output_html[-1] == ParserHelper.newline_character:
            token_parts.append(ParserHelper.newline_character)
        transform_state.is_in_loose_list = True
        token_parts.extend(["<blockquote>", ParserHelper.newline_character])
        return "".join(token_parts)

    @classmethod
    def __handle_end_block_quote_token(cls, output_html, next_token, transform_state):
        """
        Handle the end block quote token.
        """
        _ = next_token

        token_parts = [output_html]
        if output_html[-1] != ParserHelper.newline_character:
            token_parts.append(ParserHelper.newline_character)
        transform_state.is_in_loose_list = (
            TransformToGfmListLooseness.reset_list_looseness(
                transform_state.actual_tokens,
                transform_state.actual_token_index,
            )
        )
        token_parts.extend(["</blockquote>", ParserHelper.newline_character])
        return "".join(token_parts)

    @classmethod
    def __handle_start_indented_code_block_token(
        cls, output_html, next_token, transform_state
    ):
        """
        Handle the start indented code block token.
        """
        _ = next_token

        token_parts = []
        if (
            not output_html
            and transform_state.transform_stack
            and transform_state.transform_stack[-1].endswith("<li>")
        ):
            token_parts.append(ParserHelper.newline_character)
        elif output_html and output_html[-1] != ParserHelper.newline_character:
            token_parts.extend([output_html, ParserHelper.newline_character])
        else:
            token_parts.append(output_html)
        transform_state.is_in_code_block, transform_state.is_in_fenced_code_block = (
            True,
            False,
        )
        token_parts.append("<pre><code>")
        return "".join(token_parts)

    @classmethod
    def __handle_end_indented_code_block_token(
        cls, output_html, next_token, transform_state
    ):
        """
        Handle the end indented code block token.
        """
        _ = next_token

        transform_state.is_in_code_block = False
        return "".join(
            [
                output_html,
                ParserHelper.newline_character,
                "</code></pre>",
                ParserHelper.newline_character,
            ]
        )

    @classmethod
    def __handle_start_fenced_code_block_token(
        cls, output_html, next_token, transform_state
    ):
        """
        Handle the start fenced code block token.
        """
        token_parts = [output_html]
        if (output_html.endswith("</ol>") or output_html.endswith("</ul>")) or (
            output_html and output_html[-1] != ParserHelper.newline_character
        ):
            token_parts.append(ParserHelper.newline_character)
        transform_state.is_in_code_block, transform_state.is_in_fenced_code_block = (
            True,
            True,
        )
        token_parts.append("<pre><code")
        if next_token.extracted_text:
            token_parts.extend([' class="language-', next_token.extracted_text, '"'])
        token_parts.append(">")
        return "".join(token_parts)

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

        # TODO can we store this in the begin so we don't have to compute it again?
        inner_tag_parts = ["<code"]
        if transform_state.actual_tokens[fenced_token].extracted_text:
            inner_tag_parts.extend(
                [
                    ' class="language-',
                    transform_state.actual_tokens[fenced_token].extracted_text,
                    '"',
                ]
            )
        inner_tag_parts.append(">")
        inner_tag = "".join(inner_tag_parts)

        POGGER.debug(f"inner_tag>>:{inner_tag}:<<")
        POGGER.debug(f"output_html>>:{output_html}:<<")
        POGGER.debug(
            f"last_token>>:{str(transform_state.actual_tokens[transform_state.actual_token_index - 1])}:<<"
        )

        token_parts = [output_html]
        if (
            not output_html.endswith(inner_tag)
            and output_html[-1] != ParserHelper.newline_character
        ):
            token_parts.append(ParserHelper.newline_character)
            POGGER.debug("#1")
        elif (
            output_html[-1] == ParserHelper.newline_character
            and transform_state.last_token.is_text
        ):
            POGGER.debug("#2")
            token_parts.append(ParserHelper.newline_character)
        elif transform_state.last_token.is_blank_line and not next_token.was_forced:
            POGGER.debug("#3")
            token_parts.append(ParserHelper.newline_character)
        transform_state.is_in_code_block, transform_state.is_in_fenced_code_block = (
            False,
            False,
        )
        token_parts.extend(["</code></pre>", ParserHelper.newline_character])
        return "".join(token_parts)

    @classmethod
    def __handle_thematic_break_token(cls, output_html, next_token, transform_state):
        """
        Handle the thematic break token.
        """
        _ = (next_token, transform_state)

        token_parts = [output_html]
        if output_html and output_html[-1] != ParserHelper.newline_character:
            token_parts.append(ParserHelper.newline_character)
        token_parts.extend(["<hr />", ParserHelper.newline_character])
        return "".join(token_parts)

    @classmethod
    def __handle_hard_break_token(cls, output_html, next_token, transform_state):
        """
        Handle the hard line break token.
        """
        _ = (next_token, transform_state)

        return "".join([output_html, "<br />"])

    @classmethod
    def __handle_start_atx_heading_token(cls, output_html, next_token, transform_state):
        """
        Handle the start atx heading token.
        """
        previous_token = transform_state.actual_tokens[
            transform_state.actual_token_index - 1
        ]

        token_parts = [output_html]
        if output_html.endswith("</ol>") or output_html.endswith("</ul>"):
            token_parts.append(ParserHelper.newline_character)
        elif previous_token.is_paragraph_end and not transform_state.is_in_loose_list:
            token_parts.append(ParserHelper.newline_character)
        token_parts.extend(["<h", str(next_token.hash_count), ">"])
        return "".join(token_parts)

    @classmethod
    def __handle_end_atx_heading_token(cls, output_html, next_token, transform_state):
        """
        Handle the end atx heading token.
        """
        _ = next_token

        fenced_token = transform_state.actual_token_index - 1
        while not transform_state.actual_tokens[fenced_token].is_atx_heading:
            fenced_token -= 1

        return "".join(
            [
                output_html,
                "</h",
                str(transform_state.actual_tokens[fenced_token].hash_count),
                ">",
                ParserHelper.newline_character,
            ]
        )

    @classmethod
    def __handle_start_setext_heading_token(
        cls, output_html, next_token, transform_state
    ):
        """
        Handle the start setext heading token.
        """
        _ = transform_state

        token_parts = [output_html]
        if output_html.endswith("</ol>") or output_html.endswith("</ul>"):
            token_parts.append(ParserHelper.newline_character)
        token_parts.extend(
            ["<h", "1" if next_token.heading_character == "=" else "2", ">"]
        )
        return "".join(token_parts)

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
        token_parts = [
            output_html,
            "</h",
            "1"
            if transform_state.actual_tokens[fenced_token].heading_character == "="
            else "2",
            ">",
            ParserHelper.newline_character,
        ]
        return "".join(token_parts)

    @classmethod
    def __handle_new_list_item_token(cls, output_html, next_token, transform_state):
        """
        Handle the new list item token.
        """
        _ = next_token

        transform_state.add_trailing_text, transform_state.add_leading_text = (
            "</li>",
            "<li>",
        )
        token_parts = [output_html]
        if output_html and output_html[-1] == ">":
            token_parts.append(ParserHelper.newline_character)
        return "".join(token_parts)

    @classmethod
    def __handle_inline_code_span_token(cls, output_html, next_token, transform_state):
        """
        Handle the code span token.
        """
        _ = transform_state

        return "".join(
            [
                output_html,
                "<code>",
                ParserHelper.resolve_all_from_text(next_token.span_text),
                "</code>",
            ]
        )

    @classmethod
    def __handle_raw_html_token(cls, output_html, next_token, transform_state):
        """
        Handle the raw html token.
        """
        _ = transform_state

        return "".join(
            [
                output_html,
                "<",
                ParserHelper.resolve_all_from_text(next_token.raw_tag),
                ">",
            ]
        )

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

        return "".join(
            [
                output_html,
                '<a href="mailto:',
                next_token.autolink_text,
                '">',
                next_token.autolink_text,
                "</a>",
            ]
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
            token_parts = ["<ol"]
            if next_token.list_start_content != "1":
                token_parts.extend(
                    [' start="', str(int(next_token.list_start_content)), '"']
                )
            token_parts.extend([">", ParserHelper.newline_character, "<li>"])
            transform_state.add_leading_text = "".join(token_parts)
        else:
            transform_state.add_leading_text = "".join(
                ["<ul>", ParserHelper.newline_character, "<li>"]
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
        transform_state.add_trailing_text = "".join(
            [
                "</li>",
                ParserHelper.newline_character,
                "</ul>" if next_token.is_unordered_list_end else "</ol>",
            ]
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

        tag_text_parts = []
        for next_character in in_tag_pretext:
            if next_character in TransformToGfm.raw_html_percent_escape_ascii_chars:
                tag_text_parts.extend(["%", (hex(ord(next_character))[2:]).upper()])
            elif ord(next_character) >= 128:
                encoded_data = next_character.encode("utf8")
                for encoded_byte in encoded_data:
                    tag_text_parts.extend(["%", (hex(encoded_byte)[2:]).upper()])
            else:
                tag_text_parts.append(next_character)

        return "".join(
            [
                output_html,
                '<a href="',
                "".join(tag_text_parts),
                '">',
                InlineHelper.append_text(
                    "", next_token.autolink_text, add_text_signature=False
                ),
                "</a>",
            ]
        )

    @classmethod
    def __handle_start_html_block_token(cls, output_html, next_token, transform_state):
        """
        Handle the start html block token.
        """
        _ = next_token

        transform_state.is_in_html_block = True
        token_parts = []
        if (
            not output_html
            and transform_state.transform_stack
            and transform_state.transform_stack[-1].endswith("<li>")
        ):
            token_parts.append(ParserHelper.newline_character)
        else:
            previous_token = transform_state.actual_tokens[
                transform_state.actual_token_index - 1
            ]
            POGGER.debug(">previous_token>$>", previous_token)
            token_parts.append(output_html)
            if previous_token.is_list_end:
                token_parts.append(ParserHelper.newline_character)
            elif previous_token.is_paragraph_end:
                if not transform_state.is_in_loose_list:
                    token_parts.append(ParserHelper.newline_character)
        return "".join(token_parts)

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

        return "".join(
            [output_html, "<em>" if next_token.emphasis_length == 1 else "<strong>"]
        )

    @classmethod
    def __handle_end_emphasis_token(cls, output_html, next_token, transform_state):
        """
        Handle the end emphasis token.
        """
        _ = transform_state

        return "".join(
            [
                output_html,
                "</em>"
                if next_token.start_markdown_token.emphasis_length == 1
                else "</strong>",
            ]
        )

    @classmethod
    def __handle_start_link_token(cls, output_html, next_token, transform_state):
        """
        Handle the start link token.
        """
        _ = transform_state
        return "".join(
            [
                output_html,
                '<a href="',
                next_token.link_uri,
                f'" title="{next_token.link_title}' if next_token.link_title else "",
                '">',
            ]
        )

    @classmethod
    def __handle_end_link_token(cls, output_html, next_token, transform_state):
        """
        Handle the end link token.
        """
        _ = (next_token, transform_state)

        return f"{output_html}</a>"

    @classmethod
    def __handle_image_token(cls, output_html, next_token, transform_state):
        """
        Handle the image token.
        """
        _ = transform_state

        return "".join(
            [
                output_html,
                '<img src="',
                next_token.link_uri,
                '" alt="',
                next_token.image_alt_text,
                '" ',
                (f'title="{next_token.link_title}" ' if next_token.link_title else ""),
                "/>",
            ]
        )
