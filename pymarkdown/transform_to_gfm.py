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

    # pylint: disable=too-many-statements
    # pylint: disable=too-many-branches
    @classmethod  # noqa: C901
    def transform(cls, actual_tokens):  # noqa: C901
        """
        Transform the tokens into html.
        """
        output_html = ""
        transform_stack = []
        actual_token_index = 0
        is_in_code_block = False
        is_in_fenced_code_block = False
        is_in_html_block = False
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
                if output_html and output_html[-1] != "\n":
                    output_html = output_html + "\n"
                output_html = output_html + "<p>"
            elif isinstance(next_token, BlankLineMarkdownToken):
                if is_in_fenced_code_block:
                    output_html = output_html + next_token.extracted_whitespace + "\n"
                elif is_in_html_block:
                    output_html = output_html + "\n"
            elif isinstance(next_token, BlockQuoteMarkdownToken):
                output_html = output_html + "<blockquote>\n"
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
                if output_html and output_html[-1] != "\n":
                    output_html = output_html + "\n"
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
                add_leading_text = "<ol>\n<li>"
                print(
                    "transform_stack>>"
                    + str(transform_stack)
                    + ">>ibl>>"
                    + str(actual_tokens[-1].is_blank_line)
                )
                if (
                    transform_stack
                    and not actual_tokens[actual_token_index - 1].is_blank_line
                ):
                    if output_html.startswith("<p>") and output_html.endswith("</p>\n"):
                        reduced_paragraph = output_html[len("<p>") : -len("</p>\n")]
                        if "<" not in reduced_paragraph:
                            output_html = reduced_paragraph
            elif isinstance(next_token, UnorderedListStartMarkdownToken):
                add_leading_text = "<ul>\n<li>"
                print(
                    "x>>"
                    + str(transform_stack)
                    + ">>ibl>>"
                    + str(actual_tokens[-1].is_blank_line)
                )
                if (
                    transform_stack
                    and not actual_tokens[actual_token_index - 1].is_blank_line
                ):
                    if output_html.startswith("<p>") and output_html.endswith("</p>\n"):
                        reduced_paragraph = output_html[len("<p>") : -len("</p>\n")]
                        if "<" not in reduced_paragraph:
                            output_html = reduced_paragraph
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
            elif isinstance(next_token, EndMarkdownToken):
                if next_token.type_name == MarkdownToken.token_paragraph:
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
                    output_html = output_html + "</code></pre>\n"
                    is_in_code_block = False
                    is_in_fenced_code_block = False
                elif next_token.type_name == MarkdownToken.token_unordered_list_start:
                    add_trailing_text = "</li>\n</ul>"
                elif next_token.type_name == MarkdownToken.token_ordered_list_start:
                    add_trailing_text = "</li>\n</ol>"
                elif next_token.type_name == MarkdownToken.token_block_quote:
                    if output_html[-1] != "\n":
                        output_html = output_html + "\n"
                    output_html = output_html + "</blockquote>\n"
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
                    print(
                        "Markdown token end type "
                        + next_token.type_name
                        + " not supported."
                    )
            else:
                print(
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
                if output_html.startswith("<p>") and output_html.endswith("</p>\n"):
                    reduced_paragraph = output_html[len("<p>") : -len("</p>\n")]
                    if "<" not in reduced_paragraph:
                        output_html = reduced_paragraph
                if output_html.startswith("<hr />") or output_html.startswith("<p>"):
                    output_html = "\n" + output_html
                if output_html.endswith("</ul>"):
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


# pylint: enable=too-few-public-methods
