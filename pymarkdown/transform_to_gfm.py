"""
Module to provide for a transformation from markdown tokens to html for GFM.
"""
from pymarkdown.markdown_token import (  # EmailAutolinkMarkdownToken,; SetextHeaderEndMarkdownToken,; UriAutolinkMarkdownToken,
    AtxHeaderMarkdownToken,
    BlankLineMarkdownToken,
    BlockQuoteMarkdownToken,
    EndMarkdownToken,
    FencedCodeBlockMarkdownToken,
    HardBreakMarkdownToken,
    HtmlBlockMarkdownToken,
    IndentedCodeBlockMarkdownToken,
    InlineCodeSpanMarkdownToken,
    MarkdownToken,
    NewListItemMarkdownToken,
    OrderedListStartMarkdownToken,
    ParagraphMarkdownToken,
    RawHtmlMarkdownToken,
    SetextHeaderMarkdownToken,
    TextMarkdownToken,
    ThematicBreakMarkdownToken,
    UnorderedListStartMarkdownToken,
)


# pylint: disable=too-few-public-methods
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

    # pylint: disable=too-many-statements
    # pylint: disable=too-many-branches
    # pylint: disable=too-many-locals
    @classmethod  # noqa: C901
    def transform(cls, actual_tokens):  # noqa: C901
        """
        Transform the tokens into html.
        """
        print("\n\n---\n")
        output_html = ""
        transform_stack = []
        actual_token_index = 0
        is_in_code_block = False
        is_in_fenced_code_block = False
        is_in_html_block = False
        is_in_loose_list = True
        print("           is_in_loose_list=" + str(is_in_loose_list))
        for next_token in actual_tokens:
            add_trailing_text = None
            add_leading_text = None
            if isinstance(next_token, TextMarkdownToken):
                if is_in_code_block:
                    output_html = (
                        output_html
                        + next_token.extracted_whitespace
                        + next_token.token_text
                    )
                elif is_in_html_block:
                    output_html = (
                        output_html
                        + next_token.extracted_whitespace
                        + next_token.token_text
                        + "\n"
                    )
                else:
                    output_html = output_html + next_token.token_text
            elif isinstance(next_token, ParagraphMarkdownToken):
                if is_in_loose_list:
                    if output_html and output_html[-1] != "\n":
                        output_html = output_html + "\n"
                    output_html = output_html + "<p>"
            elif isinstance(next_token, BlankLineMarkdownToken):
                if is_in_fenced_code_block:
                    output_html = output_html + next_token.extracted_whitespace + "\n"
                elif is_in_html_block:
                    output_html = output_html + "\n"
            elif isinstance(next_token, BlockQuoteMarkdownToken):
                if output_html and not output_html.endswith("\n"):
                    output_html = output_html + "\n"
                output_html = output_html + "<blockquote>\n"
                is_in_loose_list = True
                print("           is_in_loose_list=" + str(is_in_loose_list))
            elif isinstance(next_token, IndentedCodeBlockMarkdownToken):
                if (
                    not output_html
                    and transform_stack
                    and transform_stack[-1].endswith("<li>")
                ):
                    output_html = "\n"
                elif output_html and output_html[-1] != "\n":
                    output_html = output_html + "\n"
                output_html = output_html + "<pre><code>"
                is_in_code_block = True
                is_in_fenced_code_block = False
            elif isinstance(next_token, FencedCodeBlockMarkdownToken):
                inner_tag = ""
                if next_token.extracted_text:
                    inner_tag = ' class="language-' + next_token.extracted_text + '"'
                output_html = output_html + "<pre><code" + inner_tag + ">"
                is_in_code_block = True
                is_in_fenced_code_block = True
            elif isinstance(next_token, HardBreakMarkdownToken):
                output_html = output_html + "<br />"
            elif isinstance(next_token, ThematicBreakMarkdownToken):
                if output_html and output_html[-1] != "\n":
                    output_html = output_html + "\n"
                output_html = output_html + "<hr />\n"
            elif isinstance(next_token, AtxHeaderMarkdownToken):
                output_html = output_html + "<h" + str(next_token.hash_count) + ">"
            elif isinstance(next_token, SetextHeaderMarkdownToken):
                if next_token.header_character == "=":
                    inner_tag = "1"
                else:
                    inner_tag = "2"
                output_html = output_html + "<h" + inner_tag + ">"
            elif isinstance(next_token, NewListItemMarkdownToken):
                if output_html.endswith(">"):
                    output_html = output_html + "\n"
                add_trailing_text = "</li>"
                add_leading_text = "<li>"
            elif isinstance(next_token, OrderedListStartMarkdownToken):

                print("xyz>>OrderedListStartMarkdownToken")
                is_in_loose_list = cls.calculate_list_looseness(
                    actual_tokens, actual_token_index, next_token
                )
                print(
                    "xyz>>OrderedListStartMarkdownToken>>is_loose>>"
                    + str(is_in_loose_list)
                )
                print("           is_in_loose_list=" + str(is_in_loose_list))

                ostart_attribute = ""
                if next_token.list_start_content != "1":
                    list_start = int(next_token.list_start_content)
                    ostart_attribute = ' start="' + str(list_start) + '"'

                add_leading_text = "<ol" + ostart_attribute + ">\n<li>"
                print(
                    "transform_stack>>"
                    + str(transform_stack)
                    + ">>ibl>>"
                    + str(actual_tokens[actual_token_index - 1].is_blank_line)
                )
            elif isinstance(next_token, UnorderedListStartMarkdownToken):

                print("xyz>>UnorderedListStartMarkdownToken")
                is_in_loose_list = cls.calculate_list_looseness(
                    actual_tokens, actual_token_index, next_token
                )
                print(
                    "xyz>>UnorderedListStartMarkdownToken>>is_loose>>"
                    + str(is_in_loose_list)
                )
                print("           is_in_loose_list=" + str(is_in_loose_list))

                add_leading_text = "<ul>\n<li>"
                print(
                    "x>>"
                    + str(transform_stack)
                    + ">>ibl>>"
                    + str(actual_tokens[-1].is_blank_line)
                    + ">>is_in_loose_list>>"
                    + str(is_in_loose_list)
                )
            elif isinstance(next_token, InlineCodeSpanMarkdownToken):
                output_html = output_html + "<code>" + next_token.span_text + "</code>"
            elif isinstance(next_token, RawHtmlMarkdownToken):
                output_html = output_html + "<" + next_token.raw_tag + ">"
            elif isinstance(next_token, HtmlBlockMarkdownToken):
                is_in_html_block = True
                if (
                    not output_html
                    and transform_stack
                    and transform_stack[-1].endswith("<li>")
                ):
                    output_html = "\n"
                else:
                    previous_token = actual_tokens[actual_token_index - 1]
                    if isinstance(previous_token, EndMarkdownToken) and (
                        previous_token.type_name
                        == MarkdownToken.token_unordered_list_start
                        or previous_token.type_name
                        == MarkdownToken.token_ordered_list_start
                    ):
                        output_html = output_html + "\n"
            elif isinstance(next_token, EndMarkdownToken):
                if next_token.type_name == MarkdownToken.token_paragraph:
                    if is_in_loose_list:
                        output_html = output_html + "</p>\n"
                elif next_token.type_name == MarkdownToken.token_indented_code_block:
                    output_html = output_html + "\n</code></pre>\n"
                    is_in_code_block = False
                elif next_token.type_name == MarkdownToken.token_fenced_code_block:
                    fenced_token = actual_token_index - 1
                    while not actual_tokens[fenced_token].is_fenced_code_block:
                        fenced_token = fenced_token - 1

                    inner_tag = ""
                    if actual_tokens[fenced_token].extracted_text:
                        inner_tag = (
                            ' class="language-'
                            + actual_tokens[fenced_token].extracted_text
                            + '"'
                        )
                    inner_tag = "<code" + inner_tag + ">"

                    if not output_html.endswith(inner_tag) and output_html[-1] != "\n":
                        output_html = output_html + "\n"
                    elif (
                        output_html[-1] == "\n"
                        and actual_tokens[actual_token_index - 1].is_text
                    ):
                        output_html = output_html + "\n"
                    output_html = output_html + "</code></pre>\n"
                    is_in_code_block = False
                    is_in_fenced_code_block = False
                elif (
                    next_token.type_name == MarkdownToken.token_unordered_list_start
                    or next_token.type_name == MarkdownToken.token_ordered_list_start
                ):

                    is_in_loose_list = cls.reset_list_looseness(
                        actual_tokens, actual_token_index
                    )
                    if next_token.type_name == MarkdownToken.token_unordered_list_start:
                        add_trailing_text = "</li>\n</ul>"
                    else:
                        add_trailing_text = "</li>\n</ol>"
                elif next_token.type_name == MarkdownToken.token_block_quote:
                    if output_html[-1] != "\n":
                        output_html = output_html + "\n"
                    output_html = output_html + "</blockquote>\n"
                    is_in_loose_list = cls.reset_list_looseness(
                        actual_tokens, actual_token_index
                    )
                elif next_token.type_name == MarkdownToken.token_setext_header:

                    fenced_token = actual_token_index - 1
                    while not actual_tokens[fenced_token].is_setext:
                        fenced_token = fenced_token - 1
                    if actual_tokens[fenced_token].header_character == "=":
                        inner_tag = "1"
                    else:
                        inner_tag = "2"

                    output_html = output_html + "</h" + inner_tag + ">\n"
                elif next_token.type_name == MarkdownToken.token_atx_header:
                    fenced_token = actual_token_index - 1
                    while not actual_tokens[fenced_token].is_atx_header:
                        fenced_token = fenced_token - 1

                    output_html = (
                        output_html
                        + "</h"
                        + str(actual_tokens[fenced_token].hash_count)
                        + ">\n"
                    )
                elif next_token.type_name == MarkdownToken.token_html_block:
                    is_in_html_block = False
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
                + str(add_trailing_text).replace("\n", "\\n")
                + "<--"
            )
            print(
                "add_leading_text -->"
                + str(add_leading_text).replace("\n", "\\n")
                + "<--"
            )

            if add_trailing_text:
                stack_text = transform_stack.pop()

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
                for next_token_to_test in add_trailing_text_tokens:
                    if output_html.startswith(next_token_to_test):
                        output_html = "\n" + output_html
                        break

                if output_html.endswith("</ul>") or output_html.endswith("</ol>"):
                    output_html = output_html + "\n"
                output_html = stack_text + output_html + add_trailing_text

            if add_leading_text:
                if output_html and output_html[-1] != "\n":
                    output_html = output_html + "\n"
                output_html = output_html + add_leading_text
                transform_stack.append(output_html)
                output_html = ""
            print("------")
            print("next_token     -->" + str(next_token).replace("\n", "\\n") + "<--")
            print("output_html    -->" + str(output_html).replace("\n", "\\n") + "<--")
            print(
                "transform_stack-->" + str(transform_stack).replace("\n", "\\n") + "<--"
            )

            actual_token_index = actual_token_index + 1
        if output_html.endswith("\n"):
            output_html = output_html[:-1]
        return output_html

    # pylint: enable=too-many-statements
    # pylint: enable=too-many-branches
    # pylint: enable=too-many-locals


# pylint: enable=too-few-public-methods
