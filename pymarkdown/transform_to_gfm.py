"""
Module to provide for a transformation from markdown tokens to html for GFM.
"""
import inspect
import logging

from pymarkdown.inline_helper import InlineHelper
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

LOGGER = logging.getLogger(__name__)

# pylint: disable=too-many-lines


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
        self.next_token = None
        self.last_token = None


# pylint: enable=too-many-instance-attributes


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

    # pylint: disable=too-many-branches, too-many-locals, too-many-statements
    def __calculate_list_looseness(self, actual_tokens, actual_token_index, next_token):
        """
        Based on the first token in a list, compute the "looseness" of the list.
        """

        LOGGER.debug("\n\n__calculate_list_looseness>>%s", str(actual_token_index))
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
                LOGGER.debug("cll>>start list>>%s", str(current_token))
                check_me = stack_count == 0
                stack_count += 1
                LOGGER.debug(">>list--new>>%s", str(stack_count))
            elif isinstance(current_token, NewListItemMarkdownToken):
                LOGGER.debug("cll>>new list item>>%s", str(current_token))
                check_me = stack_count == 0
                if not current_token.is_block:
                    LOGGER.debug(">>list--item>>%s", str(stack_count))
            elif current_token.token_name == MarkdownToken.token_block_quote:
                LOGGER.debug("cll>>start block quote>>%s", str(current_token))
                stack_count += 1
                LOGGER.debug(">>block--new>>%s", str(stack_count))
            elif (
                current_token.token_name
                == EndMarkdownToken.type_name_prefix + MarkdownToken.token_block_quote
            ):
                LOGGER.debug("cll>>end block quote>>%s", str(current_token))
                stack_count -= 1
                LOGGER.debug(">>block--end>>%s", str(stack_count))
            elif isinstance(current_token, EndMarkdownToken) and (
                current_token.type_name == MarkdownToken.token_unordered_list_start
                or current_token.type_name == MarkdownToken.token_ordered_list_start
            ):
                LOGGER.debug("cll>>end list>>%s", str(current_token))
                if stack_count == 0:
                    stop_me = True
                else:
                    stack_count -= 1
                    if self.__correct_for_me(actual_tokens, current_token_index):
                        is_loose = True
                        stop_me = True
                        LOGGER.debug("!!!latent-LOOSE!!!")
                LOGGER.debug(">>list--end>>%s", str(stack_count))
            elif actual_tokens[current_token_index - 1].is_blank_line:
                search_back_index = current_token_index - 2
                pre_prev_token = actual_tokens[search_back_index]
                LOGGER.debug(">>pre_prev_token>>%s", str(pre_prev_token))

                while pre_prev_token.is_blank_line:
                    search_back_index -= 1
                    pre_prev_token = actual_tokens[search_back_index]

                if pre_prev_token.token_name.startswith(
                    EndMarkdownToken.type_name_prefix
                ):
                    # assert pre_prev_token.start_markdown_token
                    if pre_prev_token.start_markdown_token:
                        pre_prev_token = pre_prev_token.start_markdown_token
                        LOGGER.debug(">>end_>using_start>>%s", str(pre_prev_token))
                    else:
                        end_token_suffix = pre_prev_token.token_name[
                            len(EndMarkdownToken.type_name_prefix) :
                        ]
                        search_back_index -= 1
                        x_token = actual_tokens[search_back_index]
                        while x_token.token_name != end_token_suffix:
                            search_back_index -= 1
                            x_token = actual_tokens[search_back_index]
                        pre_prev_token = x_token
                        LOGGER.debug(">>end_>calc>>%s", str(pre_prev_token))

                current_check = (
                    current_token.is_block
                    and current_token.token_name
                    != MarkdownToken.token_link_reference_definition
                )
                pre_prev_check = (
                    pre_prev_token.is_block
                    and pre_prev_token.token_name
                    != MarkdownToken.token_link_reference_definition
                )

                LOGGER.debug(">>other--stack_count>>%s", str(stack_count))
                LOGGER.debug(
                    ">>other--current_token>>%s>>%s",
                    str(current_token),
                    str(current_check),
                )
                LOGGER.debug(
                    ">>other--current_token-2>>%s>>%s",
                    str(pre_prev_token),
                    str(pre_prev_check),
                )
                check_me = stack_count == 0 and current_check and pre_prev_check

            LOGGER.debug(
                ">>stack_count>>%s>>#%s:%s>>check=%s",
                str(stack_count),
                str(current_token_index),
                str(actual_tokens[current_token_index]),
                str(check_me),
            )
            if check_me:
                LOGGER.debug("check-->?")
                if self.__is_token_loose(actual_tokens, current_token_index):
                    is_loose = True
                    stop_me = True
                    LOGGER.debug("check-->Loose")
                else:
                    LOGGER.debug("check-->Normal")
            if stop_me:
                break
            current_token_index += 1

        assert current_token_index != len(actual_tokens)
        next_token.is_loose = is_loose
        LOGGER.debug(
            "__calculate_list_looseness<<%s<<%s\n\n",
            str(actual_token_index),
            str(is_loose),
        )
        return is_loose

    # pylint: enable=too-many-branches, too-many-locals, too-many-statements

    def __correct_for_me(self, actual_tokens, current_token_index):
        correct_closure = False
        is_valid = False
        assert current_token_index > 0

        is_valid = True
        LOGGER.debug(">>prev>>%s", str(actual_tokens[current_token_index - 1]))
        if actual_tokens[current_token_index - 1].is_blank_line:
            search_index = current_token_index + 1
            while (
                search_index < len(actual_tokens)
                and isinstance(actual_tokens[search_index], EndMarkdownToken)
                and (
                    actual_tokens[search_index].type_name
                    == MarkdownToken.token_unordered_list_start
                    or actual_tokens[search_index].type_name
                    == MarkdownToken.token_ordered_list_start
                )
            ):
                search_index += 1
            LOGGER.debug(
                ">>ss>>%s>>len>>%s", str(search_index), str(len(actual_tokens))
            )
            is_valid = search_index != len(actual_tokens)
        if is_valid:
            LOGGER.debug(">>current>>%s", str(actual_tokens[current_token_index]))
            LOGGER.debug(">>current-1>>%s", str(actual_tokens[current_token_index - 1]))
            correct_closure = self.__is_token_loose(actual_tokens, current_token_index)
            LOGGER.debug(">>correct_closure>>%s", str(correct_closure))
        return correct_closure

    @classmethod
    def __is_token_loose(cls, actual_tokens, current_token_index):
        """
        Check to see if this token inspires looseness.
        """

        check_index = current_token_index - 1
        token_to_check = actual_tokens[check_index]
        LOGGER.debug("token_to_check-->%s", str(token_to_check))

        while (
            token_to_check.token_name == MarkdownToken.token_link_reference_definition
        ):
            check_index -= 1
            token_to_check = actual_tokens[check_index]

        LOGGER.debug("token_to_check-->%s", str(token_to_check))
        if token_to_check.is_blank_line:
            LOGGER.debug("before_blank-->%s", str(actual_tokens[check_index - 1]))
            if isinstance(
                actual_tokens[check_index - 1],
                (
                    NewListItemMarkdownToken,
                    UnorderedListStartMarkdownToken,
                    OrderedListStartMarkdownToken,
                ),
            ):
                LOGGER.debug("!!!Starting Blank!!!")
            else:
                LOGGER.debug("!!!LOOSE!!!")
                return True
        return False

    @classmethod
    def __find_owning_list_start(cls, actual_tokens, actual_token_index):
        """
        Figure out what the list start for the current token is.
        """

        current_index = actual_token_index
        assert not isinstance(
            actual_tokens[current_index], UnorderedListStartMarkdownToken
        ) and not isinstance(
            actual_tokens[current_index], OrderedListStartMarkdownToken
        )

        current_index -= 1
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
                    stack_count -= 1
            elif isinstance(actual_tokens[current_index], EndMarkdownToken) and (
                actual_tokens[current_index].type_name
                == MarkdownToken.token_unordered_list_start
                or actual_tokens[current_index].type_name
                == MarkdownToken.token_ordered_list_start
            ):
                stack_count += 1
            if keep_going:
                current_index -= 1
        return current_index

    def __reset_list_looseness(self, actual_tokens, actual_token_index):
        """
        Based on where we are within the actual tokens being emitted, figure
        out the correct list looseness to use.
        """

        LOGGER.debug("!!!!!!!!!!!!!!!%s", str(actual_token_index))
        search_index = actual_token_index + 1
        stack_count = 0
        while search_index < len(actual_tokens):
            LOGGER.debug(
                "!!%s::%s::%s",
                str(stack_count),
                str(search_index),
                str(actual_tokens[search_index]),
            )
            if isinstance(
                actual_tokens[search_index],
                (UnorderedListStartMarkdownToken, OrderedListStartMarkdownToken),
            ):
                stack_count += 1
            elif isinstance(actual_tokens[search_index], EndMarkdownToken) and (
                actual_tokens[search_index].type_name
                == MarkdownToken.token_unordered_list_start
                or actual_tokens[search_index].type_name
                == MarkdownToken.token_ordered_list_start
            ):
                if not stack_count:
                    break
                stack_count -= 1
            search_index += 1
        LOGGER.debug(
            "!!!!!!!!!!!!!!!%s-of-%s", str(search_index), str(len(actual_tokens))
        )
        # check to see where we are, then grab the matching start to find
        # the loose
        if search_index == len(actual_tokens):
            is_in_loose_list = True
        else:
            LOGGER.debug(">>reset_list_looseness-token_unordered_list_start>>")
            new_index = self.__find_owning_list_start(actual_tokens, search_index)
            LOGGER.debug(">>reset_list_looseness>>%s", str(new_index))
            is_in_loose_list = actual_tokens[new_index].is_loose
        LOGGER.debug("           is_in_loose_list=%s", str(is_in_loose_list))
        return is_in_loose_list

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
            self.__handle_start_ordered_list_token,
            self.__handle_end_list_token,
        )
        self.register_handlers(
            UnorderedListStartMarkdownToken,
            self.__handle_start_unordered_list_token,
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
        LOGGER.debug("\n\n---\n")
        output_html = ""
        transform_state = TransformState(actual_tokens)
        for next_token in transform_state.actual_tokens:
            transform_state.add_trailing_text = None
            transform_state.add_leading_text = None
            transform_state.next_token = None
            if (transform_state.actual_token_index + 1) < len(actual_tokens):
                transform_state.next_token = actual_tokens[
                    transform_state.actual_token_index + 1
                ]
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

            LOGGER.debug("======")
            LOGGER.debug(
                "add_trailing_text-->%s<--",
                ParserHelper.make_value_visible(transform_state.add_trailing_text),
            )
            LOGGER.debug(
                "add_leading_text -->%s<--",
                ParserHelper.make_value_visible(transform_state.add_leading_text),
            )

            if transform_state.add_trailing_text:
                output_html = self.__apply_trailing_text(output_html, transform_state)

            if transform_state.add_leading_text:
                output_html = self.__apply_leading_text(output_html, transform_state)

            LOGGER.debug("------")
            LOGGER.debug(
                "next_token     -->%s<--", ParserHelper.make_value_visible(next_token)
            )
            LOGGER.debug(
                "output_html    -->%s<--", ParserHelper.make_value_visible(output_html)
            )
            LOGGER.debug(
                "transform_stack-->%s<--",
                ParserHelper.make_value_visible(transform_state.transform_stack),
            )

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
        output_html = stack_text + output_html + transform_state.add_trailing_text
        return output_html

    @classmethod
    def __apply_leading_text(cls, output_html, transform_state):
        """
        Apply any leading text to the output.
        """
        if output_html and output_html[-1] != ParserHelper.newline_character:
            output_html += ParserHelper.newline_character
        output_html += transform_state.add_leading_text
        transform_state.transform_stack.append(output_html)
        output_html = ""
        return output_html

    @classmethod
    def __handle_text_token(cls, output_html, next_token, transform_state):
        """
        Handle the text token.
        """
        adjusted_text_token = ParserHelper.resolve_backspaces_from_text(
            next_token.token_text
        )
        adjusted_text_token = ParserHelper.resolve_references_from_text(
            adjusted_text_token
        )
        adjusted_text_token = ParserHelper.resolve_noops_from_text(adjusted_text_token)
        adjusted_text_token = ParserHelper.resolve_blechs_from_text(adjusted_text_token)
        adjusted_text_token = ParserHelper.resolve_escapes_from_text(
            adjusted_text_token
        )

        if transform_state.is_in_code_block:
            if transform_state.is_in_fenced_code_block:
                if transform_state.last_token.is_blank_line:
                    if transform_state.actual_tokens[
                        transform_state.actual_token_index - 2
                    ].is_blank_line:
                        output_html += "\n"

            extracted_whitespace = ParserHelper.resolve_references_from_text(
                next_token.extracted_whitespace
            )
            extracted_whitespace = ParserHelper.resolve_noops_from_text(
                extracted_whitespace
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
        assert next_token
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
        assert next_token
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
                transform_state.last_token.token_name
                != MarkdownToken.token_fenced_code_block
                or not transform_state.next_token.is_blank_line
            )
            exclusion_condition = (
                transform_state.last_token.token_name
                == MarkdownToken.token_fenced_code_block
                and transform_state.next_token.token_name
                == EndMarkdownToken.type_name_prefix
                + MarkdownToken.token_fenced_code_block
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
        assert next_token
        if output_html and not output_html.endswith(ParserHelper.newline_character):
            output_html += ParserHelper.newline_character
        output_html += "<blockquote>" + ParserHelper.newline_character
        transform_state.is_in_loose_list = True
        return output_html

    def __handle_end_block_quote_token(self, output_html, next_token, transform_state):
        """
        Handle the end block quote token.
        """
        assert next_token
        if output_html[-1] != ParserHelper.newline_character:
            output_html += ParserHelper.newline_character
        output_html += "</blockquote>" + ParserHelper.newline_character
        transform_state.is_in_loose_list = self.__reset_list_looseness(
            transform_state.actual_tokens, transform_state.actual_token_index,
        )
        return output_html

    @classmethod
    def __handle_start_indented_code_block_token(
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
            output_html = ParserHelper.newline_character
        elif output_html and output_html[-1] != ParserHelper.newline_character:
            output_html += ParserHelper.newline_character
        output_html += "<pre><code>"
        transform_state.is_in_code_block = True
        transform_state.is_in_fenced_code_block = False
        return output_html

    @classmethod
    def __handle_end_indented_code_block_token(
        cls, output_html, next_token, transform_state
    ):
        """
        Handle the end indented code block token.
        """
        assert next_token
        transform_state.is_in_code_block = False
        output_html += (
            ParserHelper.newline_character
            + "</code></pre>"
            + ParserHelper.newline_character
        )
        return output_html

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
            output_html += "\n"
        elif output_html and output_html[-1] != ParserHelper.newline_character:
            output_html += ParserHelper.newline_character
        output_html += "<pre><code" + inner_tag + ">"
        transform_state.is_in_code_block = True
        transform_state.is_in_fenced_code_block = True
        return output_html

    @classmethod
    def __handle_end_fenced_code_block_token(
        cls, output_html, next_token, transform_state
    ):
        """
        Handle the end fenced code block token.
        """
        assert next_token
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

        if (
            not output_html.endswith(inner_tag)
            and output_html[-1] != ParserHelper.newline_character
        ):
            output_html += ParserHelper.newline_character
        elif (
            output_html[-1] == ParserHelper.newline_character
            and transform_state.actual_tokens[
                transform_state.actual_token_index - 1
            ].is_text
        ):
            output_html += ParserHelper.newline_character
        elif transform_state.last_token.is_blank_line:
            if not next_token.was_forced:
                output_html += ParserHelper.newline_character
        output_html += "</code></pre>" + ParserHelper.newline_character
        transform_state.is_in_code_block = False
        transform_state.is_in_fenced_code_block = False
        return output_html

    @classmethod
    def __handle_thematic_break_token(cls, output_html, next_token, transform_state):
        """
        Handle the thematic break token.
        """
        assert next_token.token_name == MarkdownToken.token_thematic_break
        assert transform_state

        if output_html and output_html[-1] != ParserHelper.newline_character:
            output_html += ParserHelper.newline_character
        output_html += "<hr />" + ParserHelper.newline_character
        return output_html

    @classmethod
    def __handle_hard_break_token(cls, output_html, next_token, transform_state):
        """
        Handle the hard line break token.
        """
        assert next_token.token_name == MarkdownToken.token_inline_hard_break
        assert transform_state
        output_html += "<br />"
        return output_html

    @classmethod
    def __handle_start_atx_heading_token(cls, output_html, next_token, transform_state):
        """
        Handle the start atx heading token.
        """
        previous_token = transform_state.actual_tokens[
            transform_state.actual_token_index - 1
        ]

        if output_html.endswith("</ol>") or output_html.endswith("</ul>"):
            output_html += "\n"
        elif previous_token.is_paragraph_end:
            if not transform_state.is_in_loose_list:
                output_html += ParserHelper.newline_character

        output_html += "<h" + str(next_token.hash_count) + ">"
        return output_html

    @classmethod
    def __handle_end_atx_heading_token(cls, output_html, next_token, transform_state):
        """
        Handle the end atx heading token.
        """
        assert next_token
        fenced_token = transform_state.actual_token_index - 1
        while not transform_state.actual_tokens[fenced_token].is_atx_heading:
            fenced_token -= 1

        output_html += (
            "</h"
            + str(transform_state.actual_tokens[fenced_token].hash_count)
            + ">"
            + ParserHelper.newline_character
        )
        return output_html

    @classmethod
    def __handle_start_setext_heading_token(
        cls, output_html, next_token, transform_state
    ):
        """
        Handle the start setext heading token.
        """
        assert transform_state
        if next_token.heading_character == "=":
            inner_tag = "1"
        else:
            inner_tag = "2"

        if output_html.endswith("</ol>") or output_html.endswith("</ul>"):
            output_html += "\n"
        output_html += "<h" + inner_tag + ">"
        return output_html

    @classmethod
    def __handle_end_setext_heading_token(
        cls, output_html, next_token, transform_state
    ):
        """
        Handle the end setext heading token.
        """
        assert next_token
        fenced_token = transform_state.actual_token_index - 1
        while not transform_state.actual_tokens[fenced_token].is_setext:
            fenced_token -= 1
        if transform_state.actual_tokens[fenced_token].heading_character == "=":
            inner_tag = "1"
        else:
            inner_tag = "2"

        output_html += "</h" + inner_tag + ">" + ParserHelper.newline_character
        return output_html

    @classmethod
    def __handle_new_list_item_token(cls, output_html, next_token, transform_state):
        """
        Handle the new list item token.
        """
        assert next_token
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
        assert transform_state
        adjusted_text_token = ParserHelper.resolve_references_from_text(
            next_token.span_text
        )
        adjusted_text_token = ParserHelper.resolve_escapes_from_text(
            adjusted_text_token
        )

        output_html += "<code>" + adjusted_text_token + "</code>"
        return output_html

    @classmethod
    def __handle_raw_html_token(cls, output_html, next_token, transform_state):
        """
        Handle the raw html token.
        """
        assert transform_state
        output_html += "<" + next_token.raw_tag + ">"
        return output_html

    @classmethod
    def __handle_link_reference_definition_token(
        cls, output_html, next_token, transform_state
    ):
        """
        Handle the link reference definition token.
        """
        assert next_token
        assert transform_state
        return output_html

    @classmethod
    def __handle_email_autolink_token(cls, output_html, next_token, transform_state):
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

    def __handle_start_ordered_list_token(
        self, output_html, next_token, transform_state,
    ):
        """
        Handle the start ordered list token.
        """
        transform_state.is_in_loose_list = self.__calculate_list_looseness(
            transform_state.actual_tokens,
            transform_state.actual_token_index,
            next_token,
        )
        ostart_attribute = ""
        if next_token.list_start_content != "1":
            list_start = int(next_token.list_start_content)
            ostart_attribute = ' start="' + str(list_start) + '"'
        transform_state.add_leading_text = (
            "<ol" + ostart_attribute + ">" + ParserHelper.newline_character + "<li>"
        )
        return output_html

    def __handle_start_unordered_list_token(
        self, output_html, next_token, transform_state,
    ):
        """
        Handle the start unordered list token.
        """
        transform_state.is_in_loose_list = self.__calculate_list_looseness(
            transform_state.actual_tokens,
            transform_state.actual_token_index,
            next_token,
        )
        transform_state.add_leading_text = (
            "<ul>" + ParserHelper.newline_character + "<li>"
        )
        return output_html

    def __handle_end_list_token(
        self, output_html, next_token, transform_state,
    ):
        """
        Handle the end list token for either an ordered or unordered list.
        """
        transform_state.is_in_loose_list = self.__reset_list_looseness(
            transform_state.actual_tokens, transform_state.actual_token_index,
        )
        if next_token.type_name == MarkdownToken.token_unordered_list_start:
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
        assert transform_state
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

        output_html += '<a href="' + in_tag_text + '">' + in_anchor_text + "</a>"
        return output_html

    @classmethod
    def __handle_start_html_block_token(cls, output_html, next_token, transform_state):
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
            output_html = ParserHelper.newline_character
        else:
            previous_token = transform_state.actual_tokens[
                transform_state.actual_token_index - 1
            ]
            LOGGER.debug(">previous_token>%s>", str(previous_token))
            if isinstance(previous_token, EndMarkdownToken) and (
                previous_token.type_name == MarkdownToken.token_unordered_list_start
                or previous_token.type_name == MarkdownToken.token_ordered_list_start
            ):
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
        assert next_token
        transform_state.is_in_html_block = False
        return output_html

    @classmethod
    def __handle_start_emphasis_token(cls, output_html, next_token, transform_state):
        """
        Handle the start emphasis token.
        """
        assert transform_state
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
        assert transform_state
        split_end_data = next_token.extra_end_data.split(":")
        if split_end_data[0] == "1":
            output_html += "</em>"
        else:
            output_html += "</strong>"
        return output_html

    @classmethod
    def __handle_start_link_token(cls, output_html, next_token, transform_state):
        """
        Handle the start link token.
        """
        assert transform_state
        anchor_tag = '<a href="' + next_token.link_uri
        if next_token.link_title:
            anchor_tag = anchor_tag + '" title="' + next_token.link_title
        anchor_tag += '">'
        output_html += anchor_tag
        return output_html

    @classmethod
    def __handle_end_link_token(cls, output_html, next_token, transform_state):
        """
        Handle the end link token.
        """
        assert next_token
        assert transform_state
        output_html += "</a>"
        return output_html

    @classmethod
    def __handle_image_token(cls, output_html, next_token, transform_state):
        """
        Handle the image token.
        """
        assert transform_state
        output_html += "<img "
        output_html += 'src="' + next_token.image_uri + '" '
        output_html += 'alt="' + next_token.image_alt_text + '" '
        if next_token.image_title:
            output_html += 'title="' + next_token.image_title + '" '
        output_html += "/>"
        return output_html
