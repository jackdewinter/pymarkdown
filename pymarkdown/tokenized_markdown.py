# pylint: disable=too-many-lines
"""
Module to provide a tokenization of a markdown-encoded string.
"""
import json
import os
import re
import string
import sys
import urllib

from pymarkdown.html_helper import HtmlHelper
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
    SetextHeaderEndMarkdownToken,
    SetextHeaderMarkdownToken,
    SpecialTextMarkdownToken,
    TextMarkdownToken,
    ThematicBreakMarkdownToken,
    UnorderedListStartMarkdownToken,
    UriAutolinkMarkdownToken,
)
from pymarkdown.parser_helper import ParserHelper
from pymarkdown.stack_token import (
    BlockQuoteStackToken,
    DocumentStackToken,
    FencedCodeBlockStackToken,
    HtmlBlockStackToken,
    IndentedCodeBlockStackToken,
    LinkDefinitionStackToken,
    OrderedListStackToken,
    ParagraphStackToken,
    UnorderedListStackToken,
)


# pylint: disable=too-many-public-methods
# pylint: disable=too-many-instance-attributes
class TokenizedMarkdown:
    """
    Class to provide a tokenization of a markdown-encoded string.
    """

    # pylint: disable=too-many-statements
    def __init__(self):
        """
        Initializes a new instance of the TokenizedMarkdown class.
        """
        self.tokenized_document = None
        self.stack = []
        self.stack.append(DocumentStackToken())
        self.link_definitions = {}

        self.ulist_start_characters = "-+*"
        self.olist_start_characters = ".)"
        self.block_quote_character = ">"

        self.atx_character = "#"
        self.html_block_start_character = "<"
        self.fenced_code_block_start_characters = "~`"
        self.thematic_break_characters = "*_-"
        self.setext_characters = "-="
        self.html_tag_start = "/"
        self.html_tag_end = ">"

        self.html_block_1 = "1"
        self.html_block_2 = "2"
        self.html_block_3 = "3"
        self.html_block_4 = "4"
        self.html_block_5 = "5"
        self.html_block_6 = "6"
        self.html_block_7 = "7"
        self.html_block_2_to_5_start = "!"
        self.html_block_2_continued_start = "--"
        self.html_block_3_continued_start = "?"
        self.html_block_4_continued_start = string.ascii_uppercase
        self.html_block_5_continued_start = "[CDATA["
        self.html_block_1_end_tags = ["</script>", "</pre>", "</style>"]
        self.html_block_2_end = "-->"
        self.html_block_3_end = "?>"
        self.html_block_4_end = self.html_tag_end
        self.html_block_5_end = "]]>"
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
        self.valid_inline_text_block_sequence_starts = "`\\&\n<*_[!]"
        self.valid_tag_name_start = string.ascii_letters
        self.valid_tag_name_characters = string.ascii_letters + string.digits + "-"
        self.tag_attribute_name_start = string.ascii_letters + "_:"
        self.tag_attribute_name_characters = (
            string.ascii_letters + string.digits + "_.:-"
        )
        self.unquoted_attribute_value_stop = "\"'=<>`" + " \x09\x0a\x0b\x0c\x0d"

        self.whitespace = "\x20\x09\x0a\x0b\x0c\x0d"
        self.non_space_whitespace = self.whitespace[1:]
        self.unicode_whitespace = "\x20\x09\x0a\x0c\x0d\u00a0\u1680\u2000\u2001\u2002\u2003\u2004\u2005\u2006\u2007\u2008\u2009\u200A\u202F\u205F\u3000"
        self.punctuation_characters = (
            "\u0020\u0021\u0022\u0023\u0024\u0025\u0026\u0027\u0028\u0029\u002a\u002b\u002c\u002d\u002e\u002f"
            + "\u003a\u003b\u003c\u003d\u003e\u003f\u0040"
            + "\u005b\u005c\u005d\u005e\u005f\u0060"
            + "\u007b\u007c\u007d\u007e"
        )
        self.ascii_control_characters = (
            "\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f"
            + "\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f"
            + "\x20\x7f"
        )

        self.inline_emphasis = "*_"
        self.inline_processing_needed = self.inline_emphasis + "[]"

        self.backslash_punctuation = "!\"#$%&'()*+,-./:;<=>?@[]^_`{|}~\\"
        self.resource_path = os.path.join(os.path.split(__file__)[0], "resources")
        self.entity_map = None
        self.valid_scheme_characters = string.ascii_letters + string.digits + ".-+"
        self.valid_email_regex = "^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$"
        self.html_character_escape_map = {
            "<": "&lt;",
            ">": "&gt;",
            "&": "&amp;",
            '"': "&quot;",
        }

    # pylint: enable=too-many-statements

    def load_entity_map(self):
        """
        Load the entity map, refreshed from https://html.spec.whatwg.org/entities.json
        into a dict that was can use.
        """

        master_entities_file = os.path.join(self.resource_path, "entities.json")
        try:
            with open(os.path.abspath(master_entities_file), "r") as infile:
                results_dictionary = json.load(infile)
        except json.decoder.JSONDecodeError as ex:
            print(
                "Named character entity map file '"
                + master_entities_file
                + "' is not a valid JSON file ("
                + str(ex)
                + ")."
            )
            sys.exit(1)
        except IOError as ex:
            print(
                "Named character entity map file '"
                + master_entities_file
                + "' was not loaded ("
                + str(ex)
                + ")."
            )
            sys.exit(1)

        approved_entity_map = {}
        for next_name in results_dictionary:

            # Downloaded file is for HTML5, which includes some names that do
            # not end with ";".  These are excluded.
            if not next_name.endswith(";"):
                continue

            char_entity = results_dictionary[next_name]
            entity_characters = char_entity["characters"]
            entity_codepoints = char_entity["codepoints"]

            # The only entities we should encounter either have a length of 1 or 2
            if len(entity_characters) == 1:
                assert len(entity_codepoints) == 1
                assert ord(entity_characters[0]) == entity_codepoints[0]
            else:
                assert len(entity_codepoints) == 2
                assert ord(entity_characters[0]) == entity_codepoints[0]
                assert ord(entity_characters[1]) == entity_codepoints[1]
            approved_entity_map[next_name] = entity_characters
        return approved_entity_map

    def transform(self, your_text_string):
        """
        Transform a markdown-encoded string into an array of tokens.
        """
        self.entity_map = self.load_entity_map()

        print("\n\n>>>>>>>parse_blocks_pass>>>>>>")
        first_pass_results = self.parse_blocks_pass(your_text_string)

        print("\n\n>>>>>>>coalesce_text_blocks>>>>>>")
        coalesced_results = self.coalesce_text_blocks(first_pass_results)

        print("\n\n>>>>>>>parse_inline>>>>>>")
        final_pass_results = self.parse_inline(coalesced_results)

        print("\n\n>>>>>>>final_pass_results>>>>>>")
        return final_pass_results

    def parse_blocks_pass(self, your_text_string):
        """
        The first pass at the tokens is to deal with blocks.
        """

        self.tokenized_document = []
        next_token = your_text_string.split("\n", 1)
        token_to_use = next_token
        did_start_close = False
        did_started_close = False
        requeue = []
        ignore_link_definition_start = False
        print("---")
        print("---" + str(token_to_use) + "---")
        print("---")
        while True:
            print("next-line>>" + str(token_to_use))
            print("stack>>" + str(self.stack))
            print("current_block>>" + str(self.stack[-1]))
            print("---")

            lines_to_requeue = []
            if did_start_close:
                print("\n\ncleanup")
                did_started_close = True
                _, lines_to_requeue, force_ignore_first_as_lrd = self.close_open_blocks(
                    self.tokenized_document,
                    include_block_quotes=True,
                    include_lists=True,
                    caller_can_handle_requeue=True,
                )
                if not lines_to_requeue:
                    break

                did_start_close = False
                token_to_use = None
                print(
                    "\n\n\n\n\n\n\n\n\n\n>>lines_to_requeue>>" + str(lines_to_requeue)
                )
            else:
                next_line = token_to_use[0]
                tokens_from_line = []
                if not next_line or not next_line.strip():
                    print("\n\nblank line")
                    (
                        tokens_from_line,
                        lines_to_requeue,
                        force_ignore_first_as_lrd,
                    ) = self.handle_blank_line(next_line, from_main_transform=True)
                else:
                    print("\n\nnormal lines")
                    (
                        tokens_from_line,
                        _,
                        lines_to_requeue,
                        force_ignore_first_as_lrd,
                    ) = self.parse_line_for_container_blocks(
                        next_line, ignore_link_definition_start
                    )

            if lines_to_requeue:
                print("requeuing lines: " + str(lines_to_requeue))
                for i in lines_to_requeue:
                    requeue.insert(0, i)
                ignore_link_definition_start = force_ignore_first_as_lrd
            else:
                ignore_link_definition_start = False

            print("---")
            print("before>>" + str(self.tokenized_document))
            print("before>>" + str(tokens_from_line))
            self.tokenized_document.extend(tokens_from_line)
            print("after>>" + str(self.tokenized_document))
            if requeue:
                print("requeue>>" + str(requeue))
            print("---")

            (
                token_to_use,
                next_token,
                did_start_close,
                did_started_close,
            ) = self.determine_next_token_process(
                requeue, next_token, did_start_close, did_started_close
            )

        return self.tokenized_document

    @classmethod
    def determine_next_token_process(
        cls, requeue, next_token, did_start_close, did_started_close
    ):
        """
        For the parse_blocks_pass function, determine the next token to parse.
        """

        token_to_use = None
        if requeue:
            print(">>Requeues present")
            token_to_use = requeue[0]
            del requeue[0]
            token_to_use = (token_to_use, None)
            print(">>Requeue>>" + str(token_to_use))
            print(">>Requeues left>>" + str(requeue))
        elif did_started_close:
            did_start_close = True
        else:
            if len(next_token) == 2:
                next_token = next_token[1].split("\n", 1)
                token_to_use = next_token
            else:
                next_token = None
                token_to_use = None
                did_start_close = True

        return token_to_use, next_token, did_start_close, did_started_close

    @classmethod
    def coalesce_text_blocks(cls, first_pass_results):
        """
        Take a pass and combine any two adjacent text blocks into one.
        """

        coalesced_list = []
        coalesced_list.extend(first_pass_results[0:1])
        for coalesce_index in range(1, len(first_pass_results)):
            did_process = False
            print(
                "coalesce_text_blocks>>>>"
                + str(first_pass_results[coalesce_index])
                + "<<"
            )
            if coalesced_list[-1].is_text:
                print(">>coalesce_text_blocks>>>>" + str(coalesced_list[-1]) + "<<")
                if first_pass_results[coalesce_index].is_text or (
                    first_pass_results[coalesce_index].is_blank_line
                    and coalesced_list[-2].is_code_block
                ):

                    print("text-text>>" + str(coalesced_list[-2]) + "<<")
                    remove_leading_spaces = 0
                    if coalesced_list[-2].is_indented_code_block:
                        remove_leading_spaces = len(coalesced_list[-2].extra_data)
                        if remove_leading_spaces > 4:
                            remove_leading_spaces = 4
                    elif coalesced_list[-2].is_fenced_code_block:
                        remove_leading_spaces = len(
                            coalesced_list[-2].extracted_whitespace
                        )
                    elif coalesced_list[-2].is_paragraph:
                        remove_leading_spaces = -1

                    print("remove_leading_spaces>>" + str(remove_leading_spaces))
                    print("combine1>>" + str(coalesced_list[-1]))
                    print("combine2>>" + str(first_pass_results[coalesce_index]))
                    coalesced_list[-1].combine(
                        first_pass_results[coalesce_index], remove_leading_spaces
                    )
                    print("combined>>" + str(coalesced_list[-1]))
                    did_process = True
            if not did_process:
                coalesced_list.append(first_pass_results[coalesce_index])

        for coalesce_index in range(1, len(coalesced_list)):
            if (
                coalesced_list[coalesce_index].is_text
                and coalesced_list[coalesce_index - 1].is_paragraph
            ):
                print(
                    "full_paragraph_text>" + str(coalesced_list[coalesce_index]) + "<"
                )
                print(
                    "full_paragraph_text>"
                    + str(len(coalesced_list[coalesce_index].token_text))
                    + ">"
                    + coalesced_list[coalesce_index].token_text
                    + "<"
                )
                removed_ws = coalesced_list[coalesce_index].remove_final_whitespace()
                print(
                    "full_paragraph_text>"
                    + str(len(coalesced_list[coalesce_index].token_text))
                    + ">"
                    + coalesced_list[coalesce_index].token_text
                    + "<"
                )
                print(
                    "full_paragraph_text>"
                    + str(coalesced_list[coalesce_index - 1])
                    + ">"
                )
                coalesced_list[coalesce_index - 1].set_final_whitespace(removed_ws)
                print(
                    "full_paragraph_text>"
                    + str(coalesced_list[coalesce_index - 1])
                    + ">"
                )

        return coalesced_list

    def parse_inline(self, coalesced_results):
        """
        Parse and resolve any inline elements.
        """

        for next_token in coalesced_results:
            print(">>" + str(next_token) + "<<")
        print("")

        coalesced_list = []
        coalesced_list.extend(coalesced_results[0:1])
        for coalesce_index in range(1, len(coalesced_results)):
            if coalesced_results[coalesce_index].is_text and (
                coalesced_list[-1].is_paragraph
                or coalesced_list[-1].is_setext
                or coalesced_list[-1].is_atx_header
                or coalesced_list[-1].is_code_block
            ):
                if coalesced_list[-1].is_code_block:
                    encoded_text = self.append_text(
                        "", coalesced_results[coalesce_index].token_text
                    )
                    processed_tokens = [
                        TextMarkdownToken(
                            encoded_text,
                            coalesced_results[coalesce_index].extracted_whitespace,
                        )
                    ]
                elif coalesced_list[-1].is_setext:
                    combined_test = (
                        coalesced_results[coalesce_index].extracted_whitespace
                        + coalesced_results[coalesce_index].token_text
                    )
                    processed_tokens = self.process_inline_text_block(
                        combined_test.replace("\t", "    ")
                    )
                elif coalesced_list[-1].is_atx_header:
                    processed_tokens = self.process_inline_text_block(
                        coalesced_results[coalesce_index].token_text.replace(
                            "\t", "    "
                        ),
                        coalesced_results[coalesce_index].extracted_whitespace.replace(
                            "\t", "    "
                        ),
                    )
                else:
                    print(
                        ">>before_add_ws>>"
                        + str(coalesced_list[-1])
                        + ">>add>>"
                        + str(coalesced_results[coalesce_index].extracted_whitespace)
                        + ">>"
                    )
                    coalesced_list[-1].add_whitespace(
                        coalesced_results[coalesce_index].extracted_whitespace.replace(
                            "\t", "    "
                        )
                    )
                    print(">>after_add_ws>>" + str(coalesced_list[-1]))
                    processed_tokens = self.process_inline_text_block(
                        coalesced_results[coalesce_index].token_text.replace(
                            "\t", "    "
                        )
                    )
                coalesced_list.extend(processed_tokens)
            else:
                coalesced_list.append(coalesced_results[coalesce_index])
        return coalesced_list

    @classmethod
    def index_any_of(cls, source_text, find_any, start_index=0):
        """
        Determine if any of the specified characters are in the source string.
        """

        while start_index < len(source_text):
            if source_text[start_index] in find_any:
                return start_index
            start_index = start_index + 1
        return -1

    def handle_backslashes(self, source_text):
        """
        Handle the processing of backslashes for anything other than the text
        blocks, which have additional needs for parsing.
        """

        valid_sequence_starts = "\\&"
        start_index = 0
        current_string = ""
        next_index = self.index_any_of(source_text, valid_sequence_starts, start_index)
        while next_index != -1:
            current_string = current_string + source_text[start_index:next_index]
            current_char = source_text[next_index]
            if current_char == "\\":
                new_string, new_index, _ = self.handle_inline_backslash(
                    source_text, next_index
                )
            else:  # if source_text[next_index] == "&":
                new_string, new_index = self.handle_character_reference(
                    source_text, next_index
                )
            current_string = current_string + new_string
            start_index = new_index
            next_index = self.index_any_of(
                source_text, valid_sequence_starts, start_index
            )

        if start_index < len(source_text):
            current_string = current_string + source_text[start_index:]
        return current_string

    def append_text(
        self, string_to_append_to, text_to_append, alternate_escape_map=None
    ):
        """
        Append the text to the given string, doing any needed encoding as we go.
        """

        if not alternate_escape_map:
            alternate_escape_map = self.html_character_escape_map

        start_index = 0
        next_index = self.index_any_of(
            text_to_append, alternate_escape_map.keys(), start_index
        )
        while next_index != -1:
            string_to_append_to = (
                string_to_append_to
                + text_to_append[start_index:next_index]
                + alternate_escape_map[text_to_append[next_index]]
            )

            start_index = next_index + 1
            next_index = self.index_any_of(
                text_to_append, alternate_escape_map.keys(), start_index
            )

        if start_index < len(text_to_append):
            string_to_append_to = string_to_append_to + text_to_append[start_index:]

        return string_to_append_to

    # pylint: disable=too-many-branches
    # pylint: disable=too-many-statements
    # pylint: disable=too-many-locals
    def process_inline_text_block(self, source_text, starting_whitespace=""):
        """
        Process a text block for any inline items.
        """

        print("process_inline_text_block<<" + str(source_text) + ">>")
        inline_blocks = []
        start_index = 0
        current_string = ""
        current_string_unresolved = ""
        end_string = None

        next_index = self.index_any_of(
            source_text, self.valid_inline_text_block_sequence_starts, start_index
        )
        print("next_index>>" + str(next_index))
        have_processed_once = False
        while next_index != -1:

            new_tokens = None
            new_string = None
            new_string_unresolved = None
            new_index = None
            have_processed_once = True
            whitespace_to_add = None

            remaining_line = source_text[start_index:next_index]

            if source_text[next_index] == "`":
                new_string, new_index, new_tokens = self.handle_inline_backtick(
                    source_text, next_index
                )
            elif source_text[next_index] == "\\":
                (
                    new_string,
                    new_index,
                    new_string_unresolved,
                ) = self.handle_inline_backslash(source_text, next_index)
            elif source_text[next_index] == "&":
                new_string, new_index = self.handle_character_reference(
                    source_text, next_index
                )
            elif source_text[next_index] == "<":
                new_string, new_index, new_tokens = self.handle_angle_brackets(
                    source_text, next_index
                )
            elif source_text[next_index] in self.inline_processing_needed:
                print(
                    "\nBEFORE:handle_inline_special>"
                    + str(current_string)
                    + "<"
                    + str(remaining_line)
                    + "<"
                )
                new_string, new_index, new_tokens = self.handle_inline_special(
                    inline_blocks,
                    source_text,
                    next_index,
                    1,
                    remaining_line,
                    current_string_unresolved,
                )
            elif source_text[next_index] == "!":
                if ParserHelper.are_characters_at_index(source_text, next_index, "!["):
                    new_string, new_index, new_tokens = self.handle_inline_special(
                        inline_blocks, source_text, next_index, 2, remaining_line, "",
                    )
                else:
                    new_string = "!"
                    new_index = next_index + 1
            else:  # if source_text[next_index] == "\n":
                (
                    new_string,
                    whitespace_to_add,
                    new_index,
                    new_tokens,
                    remaining_line,
                    end_string,
                    current_string,
                ) = self.handle_line_end(
                    next_index, remaining_line, end_string, current_string
                )

            current_string = self.append_text(current_string, remaining_line)
            current_string_unresolved = self.append_text(
                current_string_unresolved, remaining_line
            )

            print(
                "\nreplace>"
                + current_string
                + "<"
                + new_string
                + "<"
                + str(new_index)
                + "<"
            )
            if new_tokens:
                if current_string:
                    # assert end_string is None
                    inline_blocks.append(
                        TextMarkdownToken(
                            current_string,
                            starting_whitespace,
                            end_whitespace=end_string,
                        )
                    )
                    current_string = ""
                    current_string_unresolved = ""
                    starting_whitespace = ""
                    end_string = None

                inline_blocks.extend(new_tokens)

            if whitespace_to_add:
                end_string = self.modify_end_string(end_string, whitespace_to_add)

            current_string = self.append_text(current_string, new_string)

            if new_string_unresolved:
                current_string_unresolved = self.append_text(
                    current_string_unresolved, new_string_unresolved
                )
            else:
                current_string_unresolved = self.append_text(
                    current_string_unresolved, new_string
                )

            start_index = new_index
            next_index = self.index_any_of(
                source_text, self.valid_inline_text_block_sequence_starts, start_index
            )

        if start_index < len(source_text):
            current_string = self.append_text(current_string, source_text[start_index:])
            current_string_unresolved = self.append_text(
                current_string_unresolved, source_text[start_index:]
            )

        if end_string is not None:
            print("xx-end-lf>" + end_string.replace("\n", "\\n") + "<")
        if current_string or not have_processed_once:
            inline_blocks.append(
                TextMarkdownToken(
                    current_string, starting_whitespace, end_whitespace=end_string
                )
            )
        print(">>" + str(inline_blocks) + "<<")

        return self.resolve_inline_emphasis(inline_blocks, None)

    # pylint: enable=too-many-branches
    # pylint: enable=too-many-statements
    # pylint: enable=too-many-locals

    def is_open_close_emphasis_valid(self, open_token, close_token):
        """
        Determine if these two tokens together make a valid open/close emphasis pair.
        """

        matching_delimiter = close_token.token_text[0]
        is_valid_opener = False

        if not (
            open_token.token_text and open_token.token_text[0] == matching_delimiter
        ):
            print("  delimiter mismatch")
        elif not open_token.active:
            print("  not active")
        elif open_token.active and self.is_potential_opener(open_token):
            is_valid_opener = True
            is_closer_both = self.is_potential_closer(
                close_token
            ) and self.is_potential_opener(close_token)
            print("is_closer_both>>" + str(is_closer_both))
            is_opener_both = self.is_potential_closer(
                open_token
            ) and self.is_potential_opener(open_token)
            print("is_opener_both>>" + str(is_opener_both))
            if is_closer_both or is_opener_both:
                sum_repeat_count = close_token.repeat_count + open_token.repeat_count
                print("sum_delims>>" + str(sum_repeat_count))
                print("closer_delims>>" + str(close_token.repeat_count))
                print("opener_delims>>" + str(open_token.repeat_count))

                if sum_repeat_count % 3 == 0:
                    is_valid_opener = (
                        close_token.repeat_count % 3 == 0
                        and open_token.repeat_count % 3 == 0
                    )

        return is_valid_opener

    @classmethod
    def process_emphasis_pair(
        cls, inline_blocks, open_token, close_token, current_position
    ):
        """
        Given that we have found a valid open and close block, process them.
        """

        # Figure out whether we have emphasis or strong emphasis
        emphasis_length = 1
        if close_token.repeat_count >= 2 and open_token.repeat_count >= 2:
            emphasis_length = 2

        # add emph node in main stream
        start_index_in_blocks = inline_blocks.index(open_token)
        inline_blocks.insert(
            start_index_in_blocks + 1, EmphasisMarkdownToken(emphasis_length),
        )
        end_index_in_blocks = inline_blocks.index(close_token)
        inline_blocks.insert(
            end_index_in_blocks,
            EndMarkdownToken(
                MarkdownToken.token_inline_emphasis, "", str(emphasis_length),
            ),
        )
        end_index_in_blocks = end_index_in_blocks + 1

        # remove emphasis_length from open and close nodes
        print(
            str(end_index_in_blocks)
            + ">>close_token>>"
            + close_token.show_process_emphasis()
            + "<<"
        )
        close_token.reduce_repeat_count(emphasis_length)
        if not close_token.repeat_count:
            inline_blocks.remove(close_token)
            print("close_token>>removed")
            end_index_in_blocks = end_index_in_blocks - 1
            close_token.active = False
        else:
            current_position = current_position - 1
        print("close_token>>" + close_token.show_process_emphasis() + "<<")

        print(
            str(start_index_in_blocks)
            + ">>open_token>>"
            + open_token.show_process_emphasis()
            + "<<"
        )
        open_token.reduce_repeat_count(emphasis_length)
        if not open_token.repeat_count:
            inline_blocks.remove(open_token)
            print("open_token>>removed")
            end_index_in_blocks = end_index_in_blocks - 1
            open_token.active = False
        print("open_token>>" + open_token.show_process_emphasis() + "<<")

        # "remove" between start and end from delimiter_stack
        inline_index = start_index_in_blocks + 1
        while inline_index < end_index_in_blocks:
            print(
                "inline_index>>"
                + str(inline_index)
                + ">>end>>"
                + str(end_index_in_blocks)
                + ">>"
                + str(len(inline_blocks))
            )
            if isinstance(inline_blocks[inline_index], SpecialTextMarkdownToken):
                inline_blocks[inline_index].active = False
            inline_index = inline_index + 1

        return current_position

    @classmethod
    def find_token_in_delimiter_stack(cls, inline_blocks, delimiter_stack, wall_token):
        """
        Find the specified token in the delimiter stack, based solely on
        position in the inline_blocks.
        """

        if wall_token:
            wall_index_in_inlines = inline_blocks.index(wall_token)
            print(">>wall_index_in_inlines>>" + str(wall_index_in_inlines))
            while wall_index_in_inlines >= 0:
                if isinstance(
                    inline_blocks[wall_index_in_inlines], SpecialTextMarkdownToken
                ):
                    wall_index_in_inlines = delimiter_stack.index(
                        inline_blocks[wall_index_in_inlines]
                    )
                    break
                wall_index_in_inlines = wall_index_in_inlines - 1
            print(">>wall_index_in_inlines(mod)>>" + str(wall_index_in_inlines))
            stack_bottom = wall_index_in_inlines
        else:
            stack_bottom = -1
        return stack_bottom

    def resolve_inline_emphasis(self, inline_blocks, wall_token):
        """
        Resolve the inline emphasis by interpreting the special text tokens.
        """

        delimiter_stack = []
        special_count = 0
        for next_block in inline_blocks:
            print("special_count>>" + str(special_count) + ">>" + str(next_block))
            special_count = special_count + 1
            if not isinstance(next_block, SpecialTextMarkdownToken):
                continue
            print(
                "i>>"
                + str(len(delimiter_stack))
                + ">>"
                + next_block.show_process_emphasis()
            )
            delimiter_stack.append(next_block)

        stack_bottom = self.find_token_in_delimiter_stack(
            inline_blocks, delimiter_stack, wall_token
        )
        current_position = stack_bottom + 1
        openers_bottom = stack_bottom
        if current_position < len(delimiter_stack):
            print(
                "BLOCK("
                + str(current_position)
                + ") of ("
                + str(len(delimiter_stack))
                + ")"
            )
            print(
                "BLOCK("
                + str(current_position)
                + ")-->"
                + delimiter_stack[current_position].show_process_emphasis()
            )

            while current_position < (len(delimiter_stack) - 1):
                current_position = current_position + 1
                print(
                    "Block("
                    + str(current_position)
                    + ")-->"
                    + delimiter_stack[current_position].show_process_emphasis()
                )
                if not delimiter_stack[current_position].active:
                    print("not active")
                    continue
                if (
                    delimiter_stack[current_position].token_text[0]
                    not in self.inline_emphasis
                ):
                    print("not emphasis")
                    continue
                if not self.is_potential_closer(delimiter_stack[current_position]):
                    print("not closer")
                    continue

                close_token = delimiter_stack[current_position]
                print("potential closer-->" + str(current_position))
                scan_index = current_position - 1
                is_valid_opener = False
                while (
                    scan_index >= 0
                    and scan_index > stack_bottom
                    and scan_index > openers_bottom
                ):
                    print("potential opener:" + str(scan_index))
                    open_token = delimiter_stack[scan_index]
                    is_valid_opener = self.is_open_close_emphasis_valid(
                        open_token, close_token
                    )
                    if is_valid_opener:
                        break
                    scan_index = scan_index - 1
                    print(
                        "scan_index-->"
                        + str(scan_index)
                        + ">stack_bottom>"
                        + str(stack_bottom)
                        + ">openers_bottom>"
                        + str(openers_bottom)
                        + ">"
                    )

                if is_valid_opener:
                    print("FOUND OPEN")
                    current_position = self.process_emphasis_pair(
                        inline_blocks, open_token, close_token, current_position
                    )
                else:
                    # openers_bottom = current_position - 1
                    print("NOT FOUND OPEN, openers_bottom=" + str(openers_bottom))

                print("next->" + str(current_position))

        self.reset_token_text(inline_blocks)
        self.clear_remaining_emphasis(delimiter_stack, stack_bottom)
        return inline_blocks

    @classmethod
    def reset_token_text(cls, inline_blocks):
        """
        Once we are completed with any emphasis processing, ensure that any
        special emphasis tokens are limited to the specified lengths.
        """

        # TODO roll this in to reduce_repeat_count
        for next_block in inline_blocks:
            if isinstance(next_block, SpecialTextMarkdownToken):
                next_block.token_text = next_block.token_text[
                    0 : next_block.repeat_count
                ]
                next_block.compose_extra_data_field()

    @classmethod
    def clear_remaining_emphasis(cls, delimiter_stack, stack_bottom):
        """
        After processing is finished, clear any active states to ensure we don't
        process them in the future.
        """

        clear_index = stack_bottom + 1
        while clear_index < len(delimiter_stack):
            delimiter_stack[clear_index].active = False
            clear_index = clear_index + 1

    def is_right_flanking_delimiter_run(self, current_token):
        """
        Is the current token a right flanking delimiter run?
        """

        preceding_two = current_token.preceding_two.rjust(2, " ")
        following_two = current_token.following_two.ljust(2, " ")

        return preceding_two[-1] not in self.unicode_whitespace and (
            not preceding_two[-1] in self.punctuation_characters
            or (
                preceding_two[-1] in self.punctuation_characters
                and (
                    following_two[0] in self.unicode_whitespace
                    or following_two[0] in self.punctuation_characters
                )
            )
        )

    def is_left_flanking_delimiter_run(self, current_token):
        """
        Is the current token a left flanking delimiter run?
        """

        preceding_two = current_token.preceding_two.rjust(2, " ")
        following_two = current_token.following_two.ljust(2, " ")

        return following_two[0] not in self.unicode_whitespace and (
            not following_two[0] in self.punctuation_characters
            or (
                following_two[0] in self.punctuation_characters
                and (
                    preceding_two[-1] in self.unicode_whitespace
                    or preceding_two[-1] in self.punctuation_characters
                )
            )
        )

    def is_potential_closer(self, current_token):
        """
        Determine if the current token is a potential closer.
        """

        assert current_token.token_text[0] in self.inline_emphasis

        # Rule 3 and 7
        is_closer = False
        if current_token.token_text[0] == "*":
            is_closer = self.is_right_flanking_delimiter_run(current_token)
        # Rule 4 and 8
        else:  # elif current_token.token_text[0] == "_":
            is_closer = self.is_right_flanking_delimiter_run(current_token)
            if is_closer:
                is_left_flanking = self.is_left_flanking_delimiter_run(current_token)

                following_two = current_token.following_two.ljust(2, " ")
                is_closer = not is_left_flanking or (
                    is_left_flanking and following_two[0] in self.punctuation_characters
                )
        return is_closer

    def is_potential_opener(self, current_token):
        """
        Determine if the current token is a potential opener.
        """

        assert current_token.token_text[0] in self.inline_emphasis

        # Rule 1
        is_opener = False
        if current_token.token_text[0] == "*":
            is_opener = self.is_left_flanking_delimiter_run(current_token)
        else:  # elif current_token.token_text[0] == "_":
            is_opener = self.is_left_flanking_delimiter_run(current_token)
            if is_opener:
                is_right_flanking = self.is_right_flanking_delimiter_run(current_token)
                preceding_two = current_token.preceding_two.ljust(2, " ")
                is_opener = not is_right_flanking or (
                    is_right_flanking
                    and preceding_two[-1] in self.punctuation_characters
                )
        return is_opener

    @classmethod
    def modify_end_string(cls, end_string, removed_end_whitespace):
        """
        Modify the string at the end of the paragraph.
        """
        print(
            ">>removed_end_whitespace>>"
            + str(type(removed_end_whitespace))
            + ">>"
            + removed_end_whitespace
            + ">>"
        )
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>NewLine")
        if end_string:
            print(">>end_string>>" + end_string.replace("\n", "\\n") + ">>")
        print(
            ">>removed_end_whitespace>>"
            + removed_end_whitespace.replace("\n", "\\n")
            + ">>"
        )
        if end_string is None:
            end_string = removed_end_whitespace + "\n"
        else:
            end_string = end_string + removed_end_whitespace + "\n"
        print(">>end_string>>" + end_string.replace("\n", "\\n") + ">>")
        return end_string

    def handle_line_end(self, next_index, remaining_line, end_string, current_string):
        """
        Handle the inline case of having the end of line character encountered.
        """

        new_tokens = []

        _, last_non_whitespace_index = ParserHelper.collect_backwards_while_character(
            remaining_line, -1, " "
        )
        print(">>last_non_whitespace_index>>" + str(last_non_whitespace_index))
        print(">>current_string>>" + current_string + ">>")
        removed_end_whitespace = remaining_line[last_non_whitespace_index:]
        remaining_line = remaining_line[0:last_non_whitespace_index]

        append_to_current_string = "\n"
        whitespace_to_add = None
        print(
            ">>len(r_e_w)>>"
            + str(len(removed_end_whitespace))
            + ">>rem>>"
            + remaining_line
            + ">>"
        )
        if (
            len(removed_end_whitespace) == 0
            and len(current_string) >= 1
            and current_string[len(current_string) - 1] == "\\"
        ):
            new_tokens.append(HardBreakMarkdownToken())
            current_string = current_string[0:-1]
        elif len(removed_end_whitespace) >= 2:
            new_tokens.append(HardBreakMarkdownToken())
            whitespace_to_add = removed_end_whitespace
        else:
            end_string = self.modify_end_string(end_string, removed_end_whitespace)

        return (
            append_to_current_string,
            whitespace_to_add,
            next_index + 1,
            new_tokens,
            remaining_line,
            end_string,
            current_string,
        )

    def handle_inline_backslash(self, source_text, next_index):
        """
        Handle the inline case of having a backslash.
        """

        new_index = next_index + 1
        new_string = ""
        new_string_unresolved = ""
        if new_index >= len(source_text) or (
            new_index < len(source_text) and source_text[new_index] == "\n"
        ):
            new_string = "\\"
            new_string_unresolved = new_string
        else:
            if source_text[new_index] in self.backslash_punctuation:
                new_string = source_text[new_index]
                new_string_unresolved = "\\" + new_string
            else:
                new_string = "\\" + source_text[new_index]
                new_string_unresolved = new_string
            new_index = new_index + 1
        return new_string, new_index, new_string_unresolved

    def handle_inline_backtick(self, source_text, next_index):
        """
        Handle the inline case of backticks for code spans.
        """

        print("before_collect>" + str(next_index))
        (
            new_index,
            extracted_start_backticks,
        ) = ParserHelper.collect_while_one_of_characters(source_text, next_index, "`")
        print("after_collect>" + str(new_index) + ">" + extracted_start_backticks)

        end_backtick_start_index = source_text.find(
            extracted_start_backticks, new_index
        )
        while end_backtick_start_index != -1:
            (
                end_backticks_index,
                end_backticks_attempt,
            ) = ParserHelper.collect_while_one_of_characters(
                source_text, end_backtick_start_index, "`"
            )
            if len(end_backticks_attempt) == len(extracted_start_backticks):
                break
            end_backtick_start_index = source_text.find(
                extracted_start_backticks, end_backticks_index
            )
        if end_backtick_start_index == -1:
            return extracted_start_backticks, new_index, None

        between_text = source_text[new_index:end_backtick_start_index]
        between_text = (
            between_text.replace("\r\n", " ").replace("\r", " ").replace("\n", " ")
        )

        print(
            "after_collect>"
            + between_text
            + ">>"
            + str(end_backtick_start_index)
            + ">>"
            + source_text[end_backtick_start_index:]
            + "<<"
        )
        if len(between_text) > 2 and between_text[0] == " " and between_text[-1] == " ":
            stripped_between_attempt = between_text[1:-1]
            if len(stripped_between_attempt.strip()) != 0:
                between_text = stripped_between_attempt

        between_text = self.append_text("", between_text)
        print("between_text>>" + between_text + "<<")
        end_backtick_start_index = end_backtick_start_index + len(
            extracted_start_backticks
        )
        return "", end_backtick_start_index, [InlineCodeSpanMarkdownToken(between_text)]

    @classmethod
    def handle_numeric_character_reference(cls, source_text, new_index):
        """
        Handle a character reference that is numeric in nature.
        """

        new_index = new_index + 1
        translated_reference = -1
        if new_index < len(source_text) and (
            source_text[new_index] == "x" or source_text[new_index] == "X"
        ):
            hex_char = source_text[new_index]
            new_index = new_index + 1
            end_index, collected_string = ParserHelper.collect_while_one_of_characters(
                source_text, new_index, string.hexdigits
            )
            print(
                "&#x>>a>>"
                + str(end_index)
                + ">>b>>"
                + str(collected_string)
                + ">>"
                + str(len(source_text))
            )
            delta = end_index - new_index
            print("delta>>" + str(delta) + ">>")
            if 1 <= delta <= 6:
                translated_reference = int(collected_string, 16)
            new_string = "&#" + hex_char + collected_string
            new_index = end_index
        else:
            end_index, collected_string = ParserHelper.collect_while_one_of_characters(
                source_text, new_index, string.digits
            )
            print(
                "&#>>a>>"
                + str(end_index)
                + ">>b>>"
                + str(collected_string)
                + ">>"
                + str(len(source_text))
            )
            delta = end_index - new_index
            print("delta>>" + str(delta) + ">>")
            if 1 <= delta <= 7:
                translated_reference = int(collected_string)
            new_string = "&#" + collected_string
            new_index = end_index

        if (
            translated_reference >= 0
            and new_index < len(source_text)
            and source_text[new_index] == ";"
        ):
            new_index = new_index + 1
            if translated_reference == 0:
                new_string = "\ufffd"
            else:
                new_string = chr(translated_reference)
        return new_string, new_index

    def handle_character_reference(self, source_text, next_index):
        """
        Handle a generic character reference.
        """

        new_index = next_index + 1
        new_string = ""
        if new_index < len(source_text) and source_text[new_index] == "#":
            new_string, new_index = self.handle_numeric_character_reference(
                source_text, new_index
            )
        else:
            end_index, collected_string = ParserHelper.collect_while_one_of_characters(
                source_text, new_index, string.ascii_letters + string.digits
            )
            if collected_string:
                collected_string = "&" + collected_string
                if end_index < len(source_text) and source_text[end_index] == ";":
                    end_index = end_index + 1
                    collected_string = collected_string + ";"
                    if collected_string in self.entity_map:
                        collected_string = self.entity_map[collected_string]
                new_string = collected_string
                new_index = end_index
            else:
                new_string = "&"
        return new_string, new_index

    def parse_valid_uri_autolink(self, text_to_parse):
        """
        Parse a possible uri autolink and determine if it is valid.
        """

        uri_scheme = ""
        if "<" not in text_to_parse and text_to_parse[0] in string.ascii_letters:
            path_index, uri_scheme = ParserHelper.collect_while_one_of_characters(
                text_to_parse, 1, self.valid_scheme_characters
            )
            uri_scheme = text_to_parse[0] + uri_scheme
        if (
            len(uri_scheme) >= 2
            and len(uri_scheme) <= 32
            and path_index < len(text_to_parse)
            and text_to_parse[path_index] == ":"
        ):
            path_index = path_index + 1
            while path_index < len(text_to_parse):
                if ord(text_to_parse[path_index]) <= 32:
                    break
                path_index = path_index + 1
            if path_index == len(text_to_parse):
                return UriAutolinkMarkdownToken(text_to_parse)
        return None

    def parse_valid_email_autolink(self, text_to_parse):
        """
        Parse a possible email autolink and determine if it is valid.
        """
        if re.match(self.valid_email_regex, text_to_parse):
            return EmailAutolinkMarkdownToken(text_to_parse)
        return None

    @classmethod
    def process_raw_special(
        cls, remaining_line, special_start, special_end, do_extra_check=False,
    ):
        """
        Parse a possible raw html special sequence, and return if it is valid.
        """
        valid_raw_html = None
        parse_index = -1

        if remaining_line.startswith(special_start):
            remaining_line = remaining_line[len(special_start) :]
            parse_index = remaining_line.find(special_end)
        if parse_index != -1:
            remaining_line = remaining_line[0:parse_index]
            parse_index = parse_index + len(special_start) + len(special_end)
            if (not do_extra_check) or (
                not (
                    remaining_line.startswith(">")
                    or remaining_line.startswith("->")
                    or remaining_line.endswith("-")
                    or "--" in remaining_line
                )
            ):
                valid_raw_html = special_start + remaining_line + special_end[0:-1]
        return valid_raw_html, parse_index

    def parse_raw_declaration(self, text_to_parse):
        """
        Parse a possible raw html declaration sequence, and return if it is valid.
        """

        valid_raw_html = None
        if ParserHelper.is_character_at_index_one_of(text_to_parse, 0, "!"):
            (
                parse_index,
                declaration_name,
            ) = ParserHelper.collect_while_one_of_characters(
                text_to_parse, 1, self.html_block_4_continued_start
            )
            if declaration_name:
                whitespace_count, _ = ParserHelper.collect_while_character(
                    text_to_parse, parse_index, " "
                )
                if whitespace_count:
                    valid_raw_html = text_to_parse
        return valid_raw_html

    def parse_raw_tag_name(self, text_to_parse, start_index):
        """
        Parse a HTML tag name from the string.
        """
        tag_name = ""
        if ParserHelper.is_character_at_index_one_of(
            text_to_parse, start_index, self.valid_tag_name_start
        ):
            index = start_index + 1
            while ParserHelper.is_character_at_index_one_of(
                text_to_parse, index, self.valid_tag_name_characters
            ):
                index = index + 1
            tag_name = text_to_parse[0:index]
        return tag_name

    def parse_tag_attributes(self, text_to_parse, start_index):
        """
        Handle the parsing of the attributes for an open tag.
        """
        parse_index, _ = ParserHelper.collect_while_one_of_characters(
            text_to_parse, start_index, self.tag_attribute_name_characters
        )
        end_name_index, extracted_whitespace = ParserHelper.extract_any_whitespace(
            text_to_parse, parse_index
        )
        if ParserHelper.is_character_at_index(text_to_parse, end_name_index, "="):
            (
                value_start_index,
                extracted_whitespace,
            ) = ParserHelper.extract_any_whitespace(text_to_parse, end_name_index + 1)
            if ParserHelper.is_character_at_index_one_of(
                text_to_parse, value_start_index, "'"
            ):
                value_end_index, _ = ParserHelper.collect_until_character(
                    text_to_parse, value_start_index + 1, "'"
                )
                if not ParserHelper.is_character_at_index(
                    text_to_parse, value_end_index, "'"
                ):
                    return None, -1
                value_end_index = value_end_index + 1
            elif ParserHelper.is_character_at_index_one_of(
                text_to_parse, value_start_index, '"'
            ):
                value_end_index, _ = ParserHelper.collect_until_character(
                    text_to_parse, value_start_index + 1, '"'
                )
                if not ParserHelper.is_character_at_index(
                    text_to_parse, value_end_index, '"'
                ):
                    return None, -1
                value_end_index = value_end_index + 1
            else:
                value_end_index, _ = ParserHelper.collect_until_one_of_characters(
                    text_to_parse, value_start_index, self.unquoted_attribute_value_stop
                )
            end_name_index, extracted_whitespace = ParserHelper.extract_any_whitespace(
                text_to_parse, value_end_index
            )

        return end_name_index, extracted_whitespace

    def parse_raw_open_tag(self, text_to_parse):
        """
        Parse the current line as if it is an open tag, and determine if it is valid.
        """

        end_parse_index = -1
        valid_raw_html = None
        tag_name = self.parse_raw_tag_name(text_to_parse, 0)
        if tag_name:
            parse_index, extracted_whitespace = ParserHelper.extract_any_whitespace(
                text_to_parse, len(tag_name)
            )
            if extracted_whitespace:
                while (
                    extracted_whitespace
                    and ParserHelper.is_character_at_index_one_of(
                        text_to_parse, parse_index, self.tag_attribute_name_start
                    )
                ):
                    parse_index, extracted_whitespace = self.parse_tag_attributes(
                        text_to_parse, parse_index
                    )
                    if parse_index is None:
                        return parse_index, extracted_whitespace

            if ParserHelper.is_character_at_index(text_to_parse, parse_index, "/"):
                parse_index = parse_index + 1

            if ParserHelper.is_character_at_index(text_to_parse, parse_index, ">"):
                valid_raw_html = text_to_parse[0:parse_index]
                end_parse_index = parse_index + 1

        return valid_raw_html, end_parse_index

    def parse_raw_close_tag(self, text_to_parse):
        """
        Parse the current line as if it is a close tag, and determine if it is valid.
        """
        valid_raw_html = None
        if ParserHelper.is_character_at_index(text_to_parse, 0, "/"):
            tag_name = self.parse_raw_tag_name(text_to_parse, 1)
            if tag_name:
                parse_index = len(tag_name)
                if parse_index != len(text_to_parse):
                    parse_index, _ = ParserHelper.extract_whitespace(
                        text_to_parse, parse_index
                    )
                if parse_index == len(text_to_parse):
                    valid_raw_html = text_to_parse
        return valid_raw_html

    def parse_raw_html(self, only_between_angles, remaining_line):
        """
        Given an open HTML tag character (<), try the various possibilities for
        types of tag, and determine if any of them parse validly.
        """

        valid_raw_html = None
        remaining_line_parse_index = -1

        valid_raw_html, remaining_line_parse_index = self.parse_raw_open_tag(
            remaining_line
        )
        if not valid_raw_html:
            valid_raw_html = self.parse_raw_close_tag(only_between_angles)
        if not valid_raw_html:
            valid_raw_html, remaining_line_parse_index = self.process_raw_special(
                remaining_line,
                self.html_block_2_to_5_start + self.html_block_2_continued_start,
                self.html_block_2_end,
                True,
            )
        if not valid_raw_html:
            valid_raw_html, remaining_line_parse_index = self.process_raw_special(
                remaining_line,
                self.html_block_3_continued_start,
                self.html_block_3_end,
            )
        if not valid_raw_html:
            valid_raw_html, remaining_line_parse_index = self.process_raw_special(
                remaining_line,
                self.html_block_2_to_5_start + self.html_block_5_continued_start,
                self.html_block_5_end,
            )
        if not valid_raw_html:
            valid_raw_html = self.parse_raw_declaration(only_between_angles)

        if valid_raw_html:
            return RawHtmlMarkdownToken(valid_raw_html), remaining_line_parse_index
        return None, -1

    def handle_angle_brackets(self, source_text, next_index):
        """
        Given an open angle bracket, determine which of the three possibilities it is.
        """
        closing_angle_index = source_text.find(">", next_index)
        new_token = None
        if closing_angle_index not in (-1, next_index + 1):

            between_brackets = source_text[next_index + 1 : closing_angle_index]
            remaining_line = source_text[next_index + 1 :]
            closing_angle_index = closing_angle_index + 1
            new_token = self.parse_valid_uri_autolink(between_brackets)
            if not new_token:
                new_token = self.parse_valid_email_autolink(between_brackets)
            if not new_token:
                new_token, after_index = self.parse_raw_html(
                    between_brackets, remaining_line
                )
                if after_index != -1:
                    closing_angle_index = after_index + next_index + 1

        if new_token:
            return "", closing_angle_index, [new_token]
        return "<", next_index + 1, None

    # pylint: disable=too-many-arguments
    def handle_inline_special(
        self,
        inline_blocks,
        source_text,
        next_index,
        special_length,
        remaining_line,
        current_string_unresolved,
    ):
        """
        Handle the collection of special inline characters for later processing.
        """

        inline_emphasis = ["*", "_"]
        preceeding_two = None
        following_two = None
        new_token = None
        repeat_count = 1
        is_active = True
        special_sequence = source_text[next_index : next_index + special_length]
        if special_length == 1 and special_sequence in inline_emphasis:
            repeat_count, new_index = ParserHelper.collect_while_character(
                source_text, next_index, special_sequence
            )
            special_sequence = source_text[next_index:new_index]

            preceeding_two = source_text[max(0, next_index - 2) : next_index]
            following_two = source_text[
                new_index : min(len(source_text), new_index + 2)
            ]
        else:
            if special_length == 1 and special_sequence[0] == "]":
                print(
                    "\nPOSSIBLE LINK CLOSE_FOUND>>"
                    + str(special_length)
                    + ">>"
                    + special_sequence
                    + ">>"
                )
                print(">>inline_blocks>>" + str(inline_blocks) + "<<")
                print(">>remaining_line>>" + str(remaining_line) + "<<")
                print(
                    ">>current_string_unresolved>>"
                    + str(current_string_unresolved)
                    + "<<"
                )
                print(">>source_text>>" + source_text[next_index:] + "<<")
                print("")
                new_index, is_active, new_token = self.look_for_link_or_image(
                    inline_blocks,
                    source_text,
                    next_index,
                    remaining_line,
                    current_string_unresolved,
                )
                print(">>inline_blocks>>" + str(inline_blocks) + "<<")
                print(">>new_token>>" + str(new_token) + "<<")
                print(">>source_text>>" + source_text[new_index:] + "<<")
            else:
                repeat_count = special_length
                new_index = next_index + special_length

        if not new_token:
            new_token = SpecialTextMarkdownToken(
                special_sequence, repeat_count, preceeding_two, following_two, is_active
            )
        return "", new_index, [new_token]

    # pylint: enable=too-many-arguments

    # pylint: disable=too-many-arguments
    def look_for_link_or_image(
        self,
        inline_blocks,
        source_text,
        next_index,
        remaining_line,
        current_string_unresolved,
    ):
        """
        Given that a link close character has been found, process it to see if
        there is actually enough other text to properly construct the link.
        """

        print(">>look_for_link_or_image>>" + str(inline_blocks) + "<<")
        is_valid = False
        new_index = next_index + 1
        updated_index = -1
        token_to_append = None

        valid_special_start_text = None
        search_index = len(inline_blocks) - 1
        while search_index >= 0:
            if isinstance(inline_blocks[search_index], SpecialTextMarkdownToken):
                print(
                    "search_index>>"
                    + str(search_index)
                    + ">>"
                    + inline_blocks[search_index].show_process_emphasis()
                )
                if inline_blocks[search_index].token_text in ["[", "!["]:
                    valid_special_start_text = inline_blocks[search_index].token_text
                    if inline_blocks[search_index].active:
                        print(">>>>>>" + str(inline_blocks))
                        updated_index, token_to_append = self.handle_link_types(
                            inline_blocks,
                            search_index,
                            source_text,
                            new_index,
                            valid_special_start_text,
                            remaining_line,
                            current_string_unresolved,
                        )
                        if updated_index != -1:
                            is_valid = True
                        else:
                            inline_blocks[search_index].active = False
                        break
                    print("  not active")
                else:
                    print("  not link")
            search_index = search_index - 1

        print(
            ">>look_for_link_or_image>>"
            + str(inline_blocks)
            + "<<is_valid<<"
            + str(is_valid)
            + "<<"
        )
        if is_valid:
            # if link set all [ before to inactive
            print("")
            print("SET TO INACTIVE-->" + str(valid_special_start_text))
            print("ind-->" + str(search_index))

            assert isinstance(
                inline_blocks[search_index],
                (LinkStartMarkdownToken, ImageStartMarkdownToken),
            )

            print("\bresolve_inline_emphasis>>" + str(inline_blocks))
            self.resolve_inline_emphasis(inline_blocks, inline_blocks[search_index])

            if valid_special_start_text == "[":
                for deactivate_token in inline_blocks:
                    if isinstance(deactivate_token, SpecialTextMarkdownToken):
                        print("inline_blocks>>>>>>>>>>>>>>>>>>" + str(deactivate_token))
                        if deactivate_token.token_text == "[":
                            deactivate_token.active = False
            return updated_index, True, token_to_append
        is_active = False
        return new_index, is_active, token_to_append

    # pylint: enable=too-many-arguments
    @classmethod
    def collect_text_from_blocks(cls, inline_blocks, ind, suffix_text):
        """
        Aggregate the text component of text blocks.
        """

        print(">>collect_text_from_blocks>>" + str(inline_blocks))
        print(">>collect_text_from_blocks>>suffix_text>>" + str(suffix_text))
        collected_text = ""
        collect_index = ind + 1
        while collect_index < len(inline_blocks):
            collected_text = collected_text + inline_blocks[collect_index].token_text
            collect_index = collect_index + 1
        collected_text = collected_text + suffix_text
        print(">>collect_text_from_blocks>>" + str(collected_text) + "<<")
        return collected_text

    # pylint: disable=too-many-locals
    # pylint: disable=too-many-arguments
    def handle_link_types(
        self,
        inline_blocks,
        ind,
        source_text,
        new_index,
        start_text,
        remaining_line,
        current_string_unresolved,
    ):
        """
        After finding a link specifier, figure out what type of link it is.
        """

        print(
            "handle_link_types>>"
            + str(inline_blocks)
            + "<<"
            + str(ind)
            + "<<"
            + str(len(inline_blocks))
        )
        print("handle_link_types>>" + source_text[new_index:] + "<<")
        print(
            "handle_link_types>>current_string_unresolved>>"
            + str(current_string_unresolved)
            + "<<remaining_line<<"
            + str(remaining_line)
            + ">>"
        )
        text_from_blocks = self.collect_text_from_blocks(
            inline_blocks, ind, current_string_unresolved + remaining_line
        )
        print("handle_link_types>>text_from_blocks>>" + text_from_blocks + "<<")

        update_index = -1
        inline_link = None
        inline_title = None
        tried_full_reference_form = False
        if ParserHelper.is_character_at_index(source_text, new_index, "("):
            print("inline reference?")
            inline_link, inline_title, update_index = self.process_inline_link_body(
                source_text, new_index + 1
            )
        elif ParserHelper.is_character_at_index(source_text, new_index, "["):
            print("collapsed reference?")
            after_open_index = new_index + 1
            if ParserHelper.is_character_at_index(source_text, after_open_index, "]"):
                print("collapsed reference")
                print(">>" + text_from_blocks + ">>")
                update_index, inline_link, inline_title = self.look_up_link(
                    text_from_blocks, after_open_index + 1, "collapsed reference"
                )
                tried_full_reference_form = True
            else:
                print("full reference?")
                print(">>did_extract>>" + source_text[after_open_index:] + ">")
                did_extract, after_label_index, ex_label = self.extract_link_label(
                    source_text, after_open_index, include_reference_colon=False
                )
                print(
                    ">>did_extract>>"
                    + str(did_extract)
                    + ">after_label_index>"
                    + str(after_label_index)
                    + ">ex_label>"
                    + str(ex_label)
                    + ">"
                )
                if did_extract:
                    tried_full_reference_form = True
                    update_index, inline_link, inline_title = self.look_up_link(
                        ex_label, after_label_index, "full reference"
                    )

        if update_index == -1 and not tried_full_reference_form:
            print("shortcut?")
            print("link_definitions>>" + str(self.link_definitions) + "<<")
            print(">>" + str(inline_blocks) + "<<")
            print(">>" + str(text_from_blocks) + "<<")
            update_index, inline_link, inline_title = self.look_up_link(
                text_from_blocks, new_index, "shortcut"
            )

        token_to_append = None
        if update_index != -1:
            if start_text == "[":
                inline_blocks[ind] = LinkStartMarkdownToken(
                    link_uri=inline_link, link_title=inline_title
                )
                token_to_append = EndMarkdownToken(
                    MarkdownToken.token_inline_link, "", ""
                )
            else:
                inline_blocks[ind] = ImageStartMarkdownToken(
                    link_uri=inline_link, link_title=inline_title
                )
                token_to_append = EndMarkdownToken(
                    MarkdownToken.token_inline_image, "", ""
                )

        print(
            "handle_link_types<update_index<"
            + str(update_index)
            + "<<"
            + str(token_to_append)
            + "<<"
        )
        return update_index, token_to_append

    # pylint: enable=too-many-locals
    # pylint: enable=too-many-arguments

    def look_up_link(self, link_to_lookup, new_index, link_type):
        """
        Look up a link to see if it is present.
        """

        inline_link = ""
        inline_title = ""
        link_label = self.normalize_link_label(link_to_lookup)
        if not link_label or link_label not in self.link_definitions:
            update_index = -1
        else:
            print(link_type)
            update_index = new_index
            inline_link = self.link_definitions[link_label][0]
            inline_title = self.link_definitions[link_label][1]
        return update_index, inline_link, inline_title

    def process_inline_link_body(self, source_text, new_index):
        """
        Given that an inline link has been identified, process it's body.
        """

        print("process_inline_link_body>>" + source_text[new_index:] + "<<")
        inline_link = ""
        inline_title = ""
        new_index, _ = ParserHelper.extract_any_whitespace(source_text, new_index)
        print(
            "new_index>>"
            + str(new_index)
            + ">>source_text[]>>"
            + source_text[new_index:]
            + ">"
        )
        if not ParserHelper.is_character_at_index(source_text, new_index, ")"):
            inline_link, new_index = self.parse_link_destination(source_text, new_index)
            if new_index != -1:
                print("before ws>>" + source_text[new_index:] + ">")
                new_index, _ = ParserHelper.extract_any_whitespace(
                    source_text, new_index
                )
                print("after ws>>" + source_text[new_index:] + ">")
                if ParserHelper.is_character_at_index_not(source_text, new_index, ")"):
                    inline_title, new_index = self.parse_link_title(
                        source_text, new_index
                    )
                if new_index != -1:
                    new_index, _ = ParserHelper.extract_any_whitespace(
                        source_text, new_index
                    )
        print(
            "inline_link>>"
            + str(inline_link)
            + ">>inline_title>>"
            + str(inline_title)
            + ">new_index>"
            + str(new_index)
            + ">"
        )
        if new_index != -1:
            if ParserHelper.is_character_at_index(source_text, new_index, ")"):
                new_index = new_index + 1
            else:
                new_index = -1
        print(
            "process_inline_link_body>>inline_link>>"
            + str(inline_link)
            + ">>inline_title>>"
            + str(inline_title)
            + ">new_index>"
            + str(new_index)
            + ">"
        )
        return inline_link, inline_title, new_index

    def parse_angle_link_destination(self, source_text, new_index):
        """
        Parse a link destination that is included in angle brackets.
        """

        collected_destination = ""
        new_index = new_index + 1
        angle_link_breaks = ">\\"
        keep_collecting = True
        while keep_collecting:
            keep_collecting = False
            new_index, ert_new = ParserHelper.collect_until_one_of_characters(
                source_text, new_index, angle_link_breaks
            )
            collected_destination = collected_destination + ert_new
            if ParserHelper.is_character_at_index(source_text, new_index, "\\"):
                old_new_index = new_index
                _, new_index, _ = self.handle_inline_backslash(source_text, new_index)
                collected_destination = (
                    collected_destination + source_text[old_new_index:new_index]
                )
                keep_collecting = True

        if ParserHelper.is_character_at_index(source_text, new_index, ">"):
            new_index = new_index + 1
        else:
            new_index = -1
            collected_destination = ""
        return new_index, collected_destination

    def parse_non_angle_link_destination(self, source_text, new_index):
        """
        Parse a link destination that is not included in angle brackets.
        """

        link_breaks = self.ascii_control_characters + "()\\"
        collected_destination = ""
        nesting_level = 0
        keep_collecting = True
        while keep_collecting:
            print(
                "collected_destination>>"
                + str(collected_destination)
                + "<<"
                + source_text[new_index:]
                + ">>nesting_level>>"
                + str(nesting_level)
                + ">>"
            )
            keep_collecting = False
            new_index, before_part = ParserHelper.collect_until_one_of_characters(
                source_text, new_index, link_breaks
            )
            collected_destination = collected_destination + before_part
            print(">>>>>>" + source_text[new_index:] + "<<<<<")
            if ParserHelper.is_character_at_index(source_text, new_index, "\\"):
                print("backslash")
                old_new_index = new_index
                _, new_index, _ = self.handle_inline_backslash(source_text, new_index)
                collected_destination = (
                    collected_destination + source_text[old_new_index:new_index]
                )
                keep_collecting = True
            elif ParserHelper.is_character_at_index(source_text, new_index, "("):
                print("+1")
                nesting_level = nesting_level + 1
                collected_destination = collected_destination + "("
                new_index = new_index + 1
                keep_collecting = True
            elif ParserHelper.is_character_at_index(source_text, new_index, ")"):
                print("-1")
                if nesting_level != 0:
                    collected_destination = collected_destination + ")"
                    new_index = new_index + 1
                    nesting_level = nesting_level - 1
                    keep_collecting = True
        ex_link = collected_destination
        print("collected_destination>>" + str(collected_destination))
        if nesting_level != 0:
            return -1, None
        return new_index, ex_link

    def parse_link_destination(self, source_text, new_index):
        """
        Parse an inline link's link destination.
        """

        print("parse_link_destination>>new_index>>" + source_text[new_index:] + ">>")
        ex_link = ""
        if ParserHelper.is_character_at_index(source_text, new_index, "<"):
            print(
                ">parse_angle_link_destination>new_index>"
                + str(new_index)
                + ">"
                + str(source_text[new_index:])
            )
            new_index, ex_link = self.parse_angle_link_destination(
                source_text, new_index
            )
            print(
                ">parse_angle_link_destination>new_index>"
                + str(new_index)
                + ">ex_link>"
                + ex_link
                + ">"
            )
        else:
            print(
                ">parse_non_angle_link_destination>new_index>"
                + str(new_index)
                + ">"
                + str(source_text[new_index:])
            )
            new_index, ex_link = self.parse_non_angle_link_destination(
                source_text, new_index
            )
            print(
                ">parse_non_angle_link_destination>new_index>"
                + str(new_index)
                + ">ex_link>"
                + str(ex_link)
                + ">"
            )
            if not ex_link:
                return None, -1

        if new_index != -1 and "\n" in ex_link:
            return None, -1
        print(
            "handle_backslashes>>new_index>>"
            + str(new_index)
            + ">>ex_link>>"
            + str(ex_link)
            + ">>"
        )
        if new_index != -1 and ex_link:
            ex_link = self.handle_backslashes(ex_link)
        print("urllib.parse.quote>>ex_link>>" + str(ex_link) + ">>")

        # TODO Check with checkmark.js as to how they encode and emulate instead of using python library
        ex_link = urllib.parse.quote(ex_link, safe="/#:?=()%*")
        print(
            "parse_link_destination>>new_index>>"
            + str(new_index)
            + ">>ex_link>>"
            + str(ex_link)
            + ">>"
        )
        return ex_link, new_index

    def parse_link_title(self, source_text, new_index):
        """
        Parse an inline link's link title.
        """

        print("parse_link_title>>new_index>>" + source_text[new_index:] + ">>")
        ex_title = ""
        if ParserHelper.is_character_at_index(source_text, new_index, "'"):
            new_index, ex_title = self.extract_bounded_string(
                source_text, new_index + 1, "'", None
            )
        elif ParserHelper.is_character_at_index(source_text, new_index, '"'):
            new_index, ex_title = self.extract_bounded_string(
                source_text, new_index + 1, '"', None
            )
        elif ParserHelper.is_character_at_index(source_text, new_index, "("):
            new_index, ex_title = self.extract_bounded_string(
                source_text, new_index + 1, ")", "("
            )
        else:
            new_index = -1
        print(
            "parse_link_title>>new_index>>"
            + str(new_index)
            + ">>ex_link>>"
            + str(ex_title)
            + ">>"
        )
        if ex_title is not None:
            ex_title = self.append_text("", self.handle_backslashes(ex_title))
        print("parse_link_title>>after>>" + str(ex_title) + ">>")

        return ex_title, new_index

    def extract_bounded_string(
        self, source_text, new_index, close_character, start_character
    ):
        """
        Extract a string that is bounded by some manner of characters.
        """

        break_characters = "\\" + close_character
        if start_character:
            break_characters = break_characters + start_character
        nesting_level = 0
        print(
            "extract_bounded_string>>new_index>>"
            + str(new_index)
            + ">>data>>"
            + source_text[new_index:]
            + ">>"
        )
        next_index, data = ParserHelper.collect_until_one_of_characters(
            source_text, new_index, break_characters
        )
        print(">>next_index1>>" + str(next_index) + ">>data>>" + data + ">>")
        while next_index < len(source_text) and not (
            source_text[next_index] == close_character and nesting_level == 0
        ):
            if ParserHelper.is_character_at_index(source_text, next_index, "\\"):
                print("pre-back>>next_index>>" + str(next_index) + ">>")
                old_index = next_index
                _, next_index, _ = self.handle_inline_backslash(source_text, next_index)
                data = data + source_text[old_index:next_index]
            elif start_character is not None and ParserHelper.is_character_at_index(
                source_text, next_index, start_character
            ):
                print("pre-start>>next_index>>" + str(next_index) + ">>")
                data = data + start_character
                next_index = next_index + 1
                nesting_level = nesting_level + 1
            else:  # elif ParserHelper.is_character_at_index(
                # source_text, next_index, close_character
                # ):
                print("pre-close>>next_index>>" + str(next_index) + ">>")
                data = data + close_character
                next_index = next_index + 1
                nesting_level = nesting_level - 1
            next_index, new_data = ParserHelper.collect_until_one_of_characters(
                source_text, next_index, break_characters
            )
            print("back>>next_index>>" + str(next_index) + ">>data>>" + data + ">>")
            data = data + new_data
        print(">>next_index2>>" + str(next_index) + ">>data>>" + data + ">>")
        if (
            ParserHelper.is_character_at_index(source_text, next_index, close_character)
            and nesting_level == 0
        ):
            print("extract_bounded_string>>found-close")
            return next_index + 1, data
        # if next_index == len(source_text):
        print(
            "extract_bounded_string>>ran out of string>>next_index>>" + str(next_index)
        )
        return next_index, None

    # pylint: disable=too-many-arguments
    def close_open_blocks(
        self,
        destination_array=None,
        only_these_blocks=None,
        include_block_quotes=False,
        include_lists=False,
        until_this_index=-1,
        caller_can_handle_requeue=False,
    ):
        """
        Close any open blocks that are currently on the stack.
        """

        new_tokens = []
        lines_to_requeue = []
        force_ignore_first_as_lrd = False
        if destination_array:
            new_tokens = destination_array

        while not self.stack[-1].is_document:
            print("cob>>" + str(self.stack))
            if only_these_blocks:
                print("cob-only-type>>" + str(only_these_blocks))
                print("cob-only-type>>" + str(type(self.stack[-1])))
                # pylint: disable=unidiomatic-typecheck
                if type(self.stack[-1]) not in only_these_blocks:
                    print("cob>>not in only")
                    break
                # pylint: enable=unidiomatic-typecheck
            if not include_block_quotes and self.stack[-1].is_block_quote:
                print("cob>>not block quotes")
                break
            if not include_lists and self.stack[-1].is_list:
                print("cob>>not lists")
                break
            if until_this_index != -1:
                print(
                    "NOT ME!!!!"
                    + str(until_this_index)
                    + "<<"
                    + str(len(self.stack))
                    + "<<"
                )
                if until_this_index >= len(self.stack):
                    break

            if self.stack[-1].was_link_definition_started:
                print(
                    "cob->process_link_reference_definition>>stopping link definition"
                )
                (
                    outer_processed,
                    did_complete_lrd,
                    did_pause_lrd,
                    lines_to_requeue,
                    force_ignore_first_as_lrd,
                ) = self.process_link_reference_definition("", 0, "", "")
                if caller_can_handle_requeue and lines_to_requeue:
                    break
                assert not lines_to_requeue
                print(
                    "cob->process_link_reference_definition>>outer_processed>>"
                    + str(outer_processed)
                    + ">did_complete_lrd>"
                    + str(did_complete_lrd)
                    + "<"
                )
                assert not did_pause_lrd
            else:
                adjusted_tokens = self.remove_top_element_from_stack()
                new_tokens.extend(adjusted_tokens)
        return new_tokens, lines_to_requeue, force_ignore_first_as_lrd
        # pylint: enable=too-many-arguments

    def remove_top_element_from_stack(self):
        """
        Once it is decided that we need to remove the top element from the stack,
        make sure to do it uniformly.
        """

        new_tokens = []
        print("cob->te->" + str(self.stack[-1]))
        extra_elements = []
        if self.stack[-1].is_indented_code_block:
            extra_elements.extend(self.extract_markdown_tokens_back_to_blank_line())

        new_tokens.append(self.stack[-1].generate_close_token())
        new_tokens.extend(extra_elements)
        del self.stack[-1]
        return new_tokens

    def handle_blank_line(self, input_line, from_main_transform):
        """
        Handle the processing of a blank line.
        """

        if (
            self.stack[-1].is_paragraph
            and len(self.stack) >= 2
            and self.stack[-2].is_list
        ):
            from_main_transform = False
        elif self.stack[-1].is_list:
            from_main_transform = False

        close_only_these_blocks = None
        do_include_block_quotes = True
        if not from_main_transform:
            close_only_these_blocks = [ParagraphStackToken]
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
            + ">>last_stack>>"
            + str(self.stack[-1])
        )

        lines_to_requeue = []
        force_ignore_first_as_lrd = None
        new_tokens = None
        if self.stack[-1].was_link_definition_started:
            print("process_link_reference_definition>>stopping link definition")
            (
                _,
                _,
                did_pause_lrd,
                lines_to_requeue,
                force_ignore_first_as_lrd,
            ) = self.process_link_reference_definition("", 0, "", "")
            assert not did_pause_lrd
        elif self.stack[-1].is_code_block:
            stack_bq_count = self.__count_of_block_quotes_on_stack()
            if stack_bq_count:
                print("hbl>>code block within block quote")
            else:
                print("hbl>>code block")
                new_tokens = []
        elif self.stack[-1].is_html_block:
            new_tokens = self.check_blank_html_block_end()
        elif (
            is_processing_list
            and self.tokenized_document[-1].is_blank_line
            and self.tokenized_document[-2].is_list_start
        ):
            print("double blank in list")
            new_tokens, _, _ = self.close_open_blocks(
                until_this_index=in_index, include_lists=True
            )

        if new_tokens is None:
            new_tokens, _, _ = self.close_open_blocks(
                only_these_blocks=close_only_these_blocks,
                include_block_quotes=do_include_block_quotes,
            )

        print("new_tokens>>" + str(new_tokens))
        assert non_whitespace_index == len(input_line)
        new_tokens.append(BlankLineMarkdownToken(extracted_whitespace))
        return new_tokens, lines_to_requeue, force_ignore_first_as_lrd

    def parse_indented_code_block(
        self, line_to_parse, start_index, extracted_whitespace
    ):
        """
        Handle the parsing of an indented code block
        """

        new_tokens = []

        if (
            ParserHelper.is_length_greater_than_or_equal_to(extracted_whitespace, 4)
            and not self.stack[-1].is_paragraph
        ):
            if not self.stack[-1].is_indented_code_block:
                self.stack.append(IndentedCodeBlockStackToken())
                new_tokens.append(IndentedCodeBlockMarkdownToken(extracted_whitespace))
                extracted_whitespace = "".rjust(
                    ParserHelper.calculate_length(extracted_whitespace) - 4
                )
            new_tokens.append(
                TextMarkdownToken(line_to_parse[start_index:], extracted_whitespace)
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
            ParserHelper.is_length_less_than_or_equal_to(extracted_whitespace, 3)
            or skip_whitespace_check
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

            if collected_count >= 3:
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
        if is_fence_start and not self.stack[-1].is_html_block:
            if self.stack[-1].is_fenced_code_block:
                print("pfcb->end")

                if (
                    self.stack[-1].code_fence_character == line_to_parse[start_index]
                    and collected_count >= self.stack[-1].fence_character_count
                    and non_whitespace_index >= len(line_to_parse)
                ):
                    new_tokens.append(
                        self.stack[-1].generate_close_token(extracted_whitespace)
                    )
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

                    new_tokens, _, _ = self.close_open_blocks(
                        only_these_blocks=[ParagraphStackToken],
                    )

                    self.stack.append(
                        FencedCodeBlockStackToken(
                            code_fence_character=line_to_parse[start_index],
                            fence_character_count=collected_count,
                        )
                    )
                    extracted_text = self.handle_backslashes(extracted_text)
                    text_after_extracted_text = self.handle_backslashes(
                        text_after_extracted_text
                    )
                    new_tokens.append(
                        FencedCodeBlockMarkdownToken(
                            line_to_parse[start_index],
                            collected_count,
                            extracted_text,
                            text_after_extracted_text,
                            extracted_whitespace,
                            extracted_whitespace_before_info_string,
                        )
                    )
        return new_tokens

    def is_link_reference_definition(
        self, line_to_parse, start_index, extracted_whitespace
    ):
        """
        Determine whether or not we have the start of a link reference definition.
        """

        if self.stack[-1].is_paragraph:
            return False

        if (
            ParserHelper.is_length_less_than_or_equal_to(extracted_whitespace, 3)
        ) and ParserHelper.is_character_at_index_one_of(
            line_to_parse, start_index, "["
        ):
            return True
        return False

    def extract_link_label(
        self, line_to_parse, new_index, include_reference_colon=True
    ):
        """
        Extract the link reference definition's link label.
        """

        angle_link_breaks = "[]]\\"

        collected_destination = ""
        keep_collecting = True
        while keep_collecting:
            keep_collecting = False
            new_index, ert_new = ParserHelper.collect_until_one_of_characters(
                line_to_parse, new_index, angle_link_breaks
            )
            collected_destination = collected_destination + ert_new
            if ParserHelper.is_character_at_index(line_to_parse, new_index, "\\"):
                old_new_index = new_index
                _, new_index, _ = self.handle_inline_backslash(line_to_parse, new_index)
                collected_destination = (
                    collected_destination + line_to_parse[old_new_index:new_index]
                )
                keep_collecting = True
            elif ParserHelper.is_character_at_index(line_to_parse, new_index, "["):
                print(">> unescaped [, bailing")
                return False, -1, None

        print("look for ]>>" + line_to_parse[new_index:] + "<<")
        if not ParserHelper.is_character_at_index(line_to_parse, new_index, "]"):
            print(">> no end ], bailing")
            return False, new_index, None
        new_index = new_index + 1

        if include_reference_colon:
            print("look for :>>" + line_to_parse[new_index:] + "<<")
            if not ParserHelper.is_character_at_index(line_to_parse, new_index, ":"):
                print(">> no :, bailing")
                return False, -1, None
            new_index = new_index + 1

        return True, new_index, collected_destination

    def extract_link_destination(self, line_to_parse, new_index, is_blank_line):
        """
        Extract the link reference definition's link destination.
        """
        new_index, _ = ParserHelper.collect_while_one_of_characters(
            line_to_parse, new_index, self.whitespace
        )
        if new_index == len(line_to_parse) and not is_blank_line:
            return False, new_index, None

        print("LD>>" + line_to_parse[new_index:] + "<<")
        inline_link, new_index = self.parse_link_destination(line_to_parse, new_index)
        if new_index == -1:
            return False, -1, None
        return True, new_index, inline_link

    def extract_link_title(self, line_to_parse, new_index, is_blank_line):
        """
        Extract the link reference definition's optional link title.
        """

        inline_title = ""
        print("before ws>>" + line_to_parse[new_index:] + ">")
        new_index, ex_ws = ParserHelper.extract_any_whitespace(line_to_parse, new_index)
        print(
            "after ws>>"
            + line_to_parse[new_index:]
            + ">ex_ws>"
            + ex_ws.replace("\n", "\\n")
        )
        if new_index == len(line_to_parse) and not is_blank_line:
            return False, new_index, None
        if ex_ws and new_index < len(line_to_parse):
            inline_title, new_index = self.parse_link_title(line_to_parse, new_index)
            if new_index == -1:
                return False, -1, None
            if inline_title is None:
                return False, new_index, None
        return True, new_index, inline_title

    @classmethod
    def verify_link_definition_end(cls, line_to_parse, new_index):
        """
        Verify that the link reference definition's ends properly.
        """

        print("look for EOL-ws>>" + line_to_parse[new_index:] + "<<")
        new_index, _ = ParserHelper.extract_any_whitespace(line_to_parse, new_index)
        print("look for EOL>>" + line_to_parse[new_index:] + "<<")
        if new_index < len(line_to_parse):
            print(">> characters left at EOL, bailing")
            return False, -1
        return True, new_index

    def parse_link_reference_definition(
        self, line_to_parse, start_index, extracted_whitespace, is_blank_line
    ):
        """
        Handle the parsing of what appears to be a link reference definition.
        """
        did_start = self.is_link_reference_definition(
            line_to_parse, start_index, extracted_whitespace
        )
        if not did_start:
            return False, -1, None

        print("\nparse_link_reference_definition")
        inline_title = ""
        keep_going, new_index, collected_destination = self.extract_link_label(
            line_to_parse, start_index + 1
        )
        if keep_going:
            keep_going, new_index, inline_link = self.extract_link_destination(
                line_to_parse, new_index, is_blank_line
            )
        if keep_going:
            keep_going, new_index, inline_title = self.extract_link_title(
                line_to_parse, new_index, is_blank_line
            )
        if keep_going:
            keep_going, new_index = self.verify_link_definition_end(
                line_to_parse, new_index
            )
        if keep_going:
            collected_destination = self.normalize_link_label(collected_destination)
            if not collected_destination:
                new_index = -1
                keep_going = False
        if not keep_going:
            return False, new_index, None

        assert new_index != -1

        print(">>collected_destination(norml)>>" + str(collected_destination))
        print(">>inline_link>>" + str(inline_link) + "<<")
        print(">>inline_title>>" + str(inline_title) + "<<")
        parsed_lrd_tuple = (collected_destination, (inline_link, inline_title))
        return True, new_index, parsed_lrd_tuple

    @classmethod
    def replace_any_of(
        cls, string_to_search_in, characters_to_search_for, replace_with
    ):
        """
        Replace any of a given set of characters with a given sequence.
        """

        rebuilt_string = ""
        start_index = 0
        index, ex_str = ParserHelper.collect_until_one_of_characters(
            string_to_search_in, start_index, characters_to_search_for
        )
        while index < len(string_to_search_in):
            rebuilt_string = rebuilt_string + ex_str + replace_with
            start_index = index + 1
            index, ex_str = ParserHelper.collect_until_one_of_characters(
                string_to_search_in, start_index, characters_to_search_for
            )
        rebuilt_string = rebuilt_string + ex_str
        return rebuilt_string

    def normalize_link_label(self, link_label):
        """
        Translate a link label into a normalized form to use for comparisons.
        """

        # Fold all whitespace characters (except for space) into a space character
        link_label = self.replace_any_of(link_label, self.non_space_whitespace, " ")

        # Fold multiple spaces into a single space character.
        link_label = " ".join(link_label.split())

        # Fold the case of any characters to their lower equivalent.
        link_label = link_label.casefold().strip()
        return link_label

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
            ParserHelper.is_length_less_than_or_equal_to(extracted_whitespace, 3)
            or skip_whitespace_check
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
            if self.stack[-1].is_paragraph:
                new_tokens.append(self.stack[-1].generate_close_token())
                del self.stack[-1]
            if this_bq_count == 0 and stack_bq_count > 0:
                new_tokens, _, _ = self.close_open_blocks(
                    destination_array=new_tokens,
                    only_these_blocks=[BlockQuoteStackToken],
                    include_block_quotes=True,
                )
            new_tokens.append(
                ThematicBreakMarkdownToken(
                    start_char,
                    extracted_whitespace.replace("\t", "    "),
                    line_to_parse[start_index:index].replace("\t", "    "),
                )
            )
        return new_tokens

    def parse_atx_headings(self, line_to_parse, start_index, extracted_whitespace):
        """
        Handle the parsing of an atx heading.
        """

        new_tokens = []
        if ParserHelper.is_length_less_than_or_equal_to(
            extracted_whitespace, 3
        ) and ParserHelper.is_character_at_index(
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

                new_tokens, _, _ = self.close_open_blocks(new_tokens)
                remaining_line = line_to_parse[non_whitespace_index:]
                (
                    end_index,
                    extracted_whitespace_at_end,
                ) = ParserHelper.extract_whitespace_from_end(remaining_line)
                remove_trailing_count = 0
                while (
                    end_index > 0
                    and remaining_line[end_index - 1] == self.atx_character
                ):
                    end_index = end_index - 1
                    remove_trailing_count = remove_trailing_count + 1
                extracted_whitespace_before_end = ""
                if remove_trailing_count:
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
                            remove_trailing_count = 0
                    else:
                        remaining_line = ""
                else:
                    extracted_whitespace_at_end = remaining_line[end_index:]
                    remaining_line = remaining_line[0:end_index]
                new_tokens.append(
                    AtxHeaderMarkdownToken(
                        hash_count, remove_trailing_count, extracted_whitespace,
                    )
                )
                new_tokens.append(
                    TextMarkdownToken(remaining_line, extracted_whitespace_at_start)
                )
                new_tokens.append(
                    EndMarkdownToken(
                        "atx",
                        extracted_whitespace_at_end,
                        extracted_whitespace_before_end,
                    )
                )
        return new_tokens

    def parse_setext_headings(
        self, line_to_parse, start_index, extracted_whitespace, this_bq_count
    ):
        """
        Handle the parsing of an setext heading.
        """

        new_tokens = []
        if (
            ParserHelper.is_length_less_than_or_equal_to(extracted_whitespace, 3)
            and ParserHelper.is_character_at_index_one_of(
                line_to_parse, start_index, self.setext_characters
            )
            and (self.stack[-1].is_paragraph)
            and (this_bq_count == self.__count_of_block_quotes_on_stack())
        ):
            _, collected_to_index = ParserHelper.collect_while_character(
                line_to_parse, start_index, line_to_parse[start_index]
            )
            (
                after_whitespace_index,
                extra_whitespace_after_setext,
            ) = ParserHelper.extract_whitespace(line_to_parse, collected_to_index)
            if after_whitespace_index == len(line_to_parse):

                # This is unusual.  Normally, close_open_blocks is used to close off
                # blocks based on the stack token.  However, since the setext takes
                # the last paragraph of text (see case 61) and translates it
                # into a header, this has to be done separately, as there is no
                # stack token to close.
                new_tokens.append(
                    SetextHeaderEndMarkdownToken(
                        extracted_whitespace, extra_whitespace_after_setext
                    )
                )
                token_index = len(self.tokenized_document) - 1
                while not self.tokenized_document[token_index].is_paragraph:
                    token_index = token_index - 1

                replacement_token = SetextHeaderMarkdownToken(
                    line_to_parse[start_index],
                    self.tokenized_document[token_index].extra_data,
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
            return [BlankLineMarkdownToken("")]

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
            and self.tokenized_document[-1].is_blank_line
            and self.tokenized_document[-2].is_any_list_token
        ):

            did_find, last_list_index = self.check_for_list_in_process()
            assert did_find
            new_tokens, _, _ = self.close_open_blocks(until_this_index=last_list_index)
        if stack_bq_count != 0 and this_bq_count == 0:
            new_tokens, _, _ = self.close_open_blocks(
                only_these_blocks=[BlockQuoteStackToken], include_block_quotes=True,
            )

        if not self.stack[-1].is_paragraph:
            self.stack.append(ParagraphStackToken())
            new_tokens.append(ParagraphMarkdownToken(extracted_whitespace))
            extracted_whitespace = ""

        new_tokens.append(
            TextMarkdownToken(line_to_parse[start_index:], extracted_whitespace)
        )
        return new_tokens
        # pylint: enable=too-many-arguments

    def __count_of_block_quotes_on_stack(self):
        """
        Helper method to count the number of block quotes currently on the stack.
        """

        stack_bq_count = 0
        for next_item_on_stack in self.stack:
            if next_item_on_stack.is_block_quote:
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
        self, this_bq_count, stack_bq_count, line_to_parse, extracted_whitespace,
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

            if self.stack[-1].is_code_block or is_fenced_start:
                print("__check_for_lazy_handling>>code block")
                assert not container_level_tokens
                container_level_tokens, _, _ = self.close_open_blocks(
                    only_these_blocks=[BlockQuoteStackToken, type(self.stack[-1])],
                    include_block_quotes=True,
                )
            else:
                print("__check_for_lazy_handling>>not code block")
                print("__check_for_lazy_handling>>" + str(self.stack))

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
            container_level_tokens, _, _ = self.close_open_blocks(
                only_these_blocks=[ParagraphStackToken, IndentedCodeBlockStackToken],
            )
            while this_bq_count > stack_bq_count:
                self.stack.append(BlockQuoteStackToken())
                stack_bq_count = stack_bq_count + 1
                container_level_tokens.append(
                    BlockQuoteMarkdownToken(extracted_whitespace)
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

        if not self.stack[-1].is_fenced_code_block:
            print("handle_block_quote_section>>not fenced")
            container_level_tokens, stack_bq_count = self.__ensure_stack_at_level(
                this_bq_count, stack_bq_count, extracted_whitespace
            )

            line_to_parse = line_to_parse[start_index:]

            if not line_to_parse.strip():
                (leaf_tokens, lines_to_requeue, _,) = self.handle_blank_line(
                    line_to_parse, from_main_transform=False
                )
                # TODO will need to deal with force_ignore_first_as_lrd
                assert not lines_to_requeue
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
            (
                ParserHelper.is_length_less_than_or_equal_to(adj_ws, 3)
                or skip_whitespace_check
            )
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
                self.stack[-1].is_paragraph
                and not (self.stack[-2].is_list)
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
            ParserHelper.is_length_less_than_or_equal_to(adj_ws, 3)
            or skip_whitespace_check
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
                    self.stack[-1].is_paragraph
                    and not (self.stack[-2].is_list)
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
            + str(new_stack)
        )
        if self.stack[last_list_index] == new_stack:
            balancing_tokens, _, _ = self.close_open_blocks(
                until_this_index=last_list_index, include_block_quotes=True
            )
            return True, True, balancing_tokens

        document_token_index = len(self.tokenized_document) - 1
        while document_token_index >= 0 and not (
            self.tokenized_document[document_token_index].is_any_list_token
        ):
            document_token_index = document_token_index - 1
        assert document_token_index >= 0

        print(
            "ARE-EQUAL>>Last_List_token="
            + str(self.tokenized_document[document_token_index])
        )
        old_start_index = self.tokenized_document[document_token_index].indent_level

        old_last_marker_character = self.stack[last_list_index].list_character[-1]
        new_last_marker_character = new_stack.list_character[-1]
        current_start_index = new_stack.ws_before_marker
        print(
            "old>>"
            + str(self.stack[last_list_index].extra_data)
            + ">>"
            + old_last_marker_character
        )
        print("new>>" + str(new_stack.extra_data) + ">>" + new_last_marker_character)
        if (
            self.stack[last_list_index].type_name == new_stack.type_name
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
                    last_stack_depth = self.stack[-1].ws_before_marker
                    while current_start_index < last_stack_depth:
                        last_stack_index = self.stack.index(self.stack[-1])
                        close_tokens, _, _ = self.close_open_blocks(
                            until_this_index=last_stack_index, include_lists=True
                        )
                        assert close_tokens
                        balancing_tokens.extend(close_tokens)
                        print("close_tokens>>" + str(close_tokens))
                        last_stack_depth = self.stack[-1].ws_before_marker

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
    # pylint: disable=too-many-locals
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
        ws_after_marker = ParserHelper.calculate_length(after_marker_whitespace)
        ws_before_marker = ParserHelper.calculate_length(extracted_whitespace)

        print(
            ">>stack_bq_count>>"
            + str(stack_bq_count)
            + ">>this_bq_count>>"
            + str(this_bq_count)
        )
        while this_bq_count < stack_bq_count:

            inf = len(self.stack) - 1
            while not self.stack[inf].is_block_quote:
                inf = inf - 1

            container_level_tokens, _, _ = self.close_open_blocks(
                until_this_index=inf, include_block_quotes=True, include_lists=True
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
        # pylint: enable=too-many-locals

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

        print("new_stack>>" + str(new_stack))
        no_para_start_if_empty = True
        container_level_tokens = []

        emit_item = True
        emit_li = True
        did_find, last_list_index = self.check_for_list_in_process()
        if did_find:
            print("list-in-process>>" + str(self.stack[last_list_index]))
            container_level_tokens, _, _ = self.close_open_blocks(
                until_this_index=last_list_index + 1
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
                close_tokens, _, _ = self.close_open_blocks(
                    until_this_index=last_list_index, include_lists=True
                )
                assert close_tokens
                container_level_tokens.extend(close_tokens)
        else:
            print("NOT list-in-process>>" + str(self.stack[last_list_index]))
            container_level_tokens, _, _ = self.close_open_blocks()
        print("container_level_tokens>>" + str(container_level_tokens))

        if emit_item or not emit_li:
            self.stack.append(new_stack)
            container_level_tokens.append(new_token)
        else:
            assert emit_li
            container_level_tokens.append(NewListItemMarkdownToken(indent_level))
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
        while stack_index >= 0 and not self.stack[stack_index].is_list:
            stack_index = stack_index - 1
        return stack_index >= 0, stack_index

    # pylint: disable=too-many-locals
    def list_in_process(self, line_to_parse, start_index, extracted_whitespace, ind):
        """
        Handle the processing of a line where there is a list in process.
        """

        container_level_tokens = []

        print("!!!!!FOUND>>" + str(self.stack[ind]))
        print("!!!!!FOUND>>" + str(self.stack[ind].extra_data))
        requested_list_indent = self.stack[ind].indent_level
        before_ws_length = self.stack[ind].ws_before_marker
        after_ws_length = self.stack[ind].ws_after_marker
        print(
            "!!!!!requested_list_indent>>"
            + str(requested_list_indent)
            + ",before_ws="
            + str(before_ws_length)
            + ",after_ws="
            + str(after_ws_length)
        )

        leading_space_length = ParserHelper.calculate_length(extracted_whitespace)
        is_in_paragraph = self.stack[-1].is_paragraph

        started_ulist, _ = self.is_ulist_start(
            line_to_parse, start_index, extracted_whitespace, skip_whitespace_check=True
        )
        started_olist, _, _, _ = self.is_olist_start(
            line_to_parse, start_index, extracted_whitespace, skip_whitespace_check=True
        )

        allow_list_continue = True
        if leading_space_length >= 4 and (started_ulist or started_olist):
            allow_list_continue = not self.tokenized_document[-1].is_blank_line

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
            is_in_paragraph = self.stack[-1].is_paragraph
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

                    container_level_tokens, _, _ = self.close_open_blocks(
                        until_this_index=ind, include_lists=True
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
        while stack_index >= 0 and not self.stack[stack_index].is_list:
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
                self.tokenized_document[token_index].is_any_list_token
            ):
                token_index = token_index - 1
            print(
                "PLFCB>>Started list-last token>>"
                + str(self.tokenized_document[token_index])
            )
            assert token_index >= 0

            old_start_index = self.tokenized_document[token_index].indent_level

            ws_len = ParserHelper.calculate_length(extracted_whitespace)
            print(
                "old_start_index>>" + str(old_start_index) + ">>ws_len>>" + str(ws_len)
            )
            if ws_len >= old_start_index:
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

        if ParserHelper.is_length_less_than_or_equal_to(
            adj_ws, 3
        ) and ParserHelper.is_character_at_index(
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
            (
                _,
                line_to_parse,
                lines_to_requeue,
                _,
            ) = self.parse_line_for_container_blocks(
                adj_line_to_parse,
                False,
                container_depth=container_depth + 1,
                foobar=adj_block,
                init_bq=this_bq_count,
            )
            assert not lines_to_requeue
            # TODO will need to deal with force_ignore_first_as_lrd

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
                new_stack = UnorderedListStackToken(
                    indent_level,
                    line_to_parse[start_index],
                    ws_before_marker,
                    ws_after_marker,
                )
                new_token = UnorderedListStartMarkdownToken(
                    line_to_parse[start_index], indent_level, extracted_whitespace
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

                new_stack = OrderedListStackToken(
                    indent_level,
                    line_to_parse[start_index : index + 1],
                    ws_before_marker,
                    ws_after_marker,
                )
                new_token = OrderedListStartMarkdownToken(
                    line_to_parse[index],
                    line_to_parse[start_index:index],
                    indent_level,
                    extracted_whitespace,
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
            if ind.is_list:
                current_container_blocks.append(ind)

        adj_ws = self.calculate_adjusted_whitespace(
            current_container_blocks, line_to_parse, extracted_whitespace, foobar=foobar
        )

        stack_bq_count = self.__count_of_block_quotes_on_stack()

        return current_container_blocks, adj_ws, stack_bq_count, this_bq_count

    # pylint: disable=too-many-locals
    # pylint: disable=too-many-arguments
    # pylint: disable=too-many-statements
    def parse_line_for_container_blocks(
        self,
        line_to_parse,
        ignore_link_definition_start,
        container_depth=0,
        foobar=None,
        init_bq=None,
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
            return container_level_tokens, line_to_parse, None, None

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
                this_bq_count, stack_bq_count, line_to_parse, extracted_whitespace,
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

        lines_to_requeue = []
        force_ignore_first_as_lrd = None
        if not leaf_tokens:
            print("parsing leaf>>")
            (
                leaf_tokens,
                lines_to_requeue,
                force_ignore_first_as_lrd,
            ) = self.parse_line_for_leaf_blocks(
                line_to_parse,
                0,
                this_bq_count,
                no_para_start_if_empty,
                ignore_link_definition_start,
            )
            print("parsed leaf>>" + str(leaf_tokens))
            print("parsed leaf>>" + str(len(leaf_tokens)))
            print(
                "parsed leaf>>lines_to_requeue>>"
                + str(lines_to_requeue)
                + ">"
                + str(len(lines_to_requeue))
            )
            print(
                "parsed leaf>>force_ignore_first_as_lrd>>"
                + str(force_ignore_first_as_lrd)
                + ">"
            )

        container_level_tokens.extend(leaf_tokens)
        print(
            "clt-end>>"
            + str(len(container_level_tokens))
            + ">>"
            + str(container_level_tokens)
            + "<<"
        )
        return (
            container_level_tokens,
            line_to_parse,
            lines_to_requeue,
            force_ignore_first_as_lrd,
        )
        # pylint: enable=too-many-locals
        # pylint: enable=too-many-arguments
        # pylint: enable=too-many-statements

    def check_for_special_html_blocks(self, line_to_parse, character_index):
        """
        Check for the easy to spot special blocks: 2-5.
        """

        html_block_type = None
        if character_index < len(line_to_parse):
            if ParserHelper.is_character_at_index(
                line_to_parse, character_index, self.html_block_2_to_5_start
            ):
                if ParserHelper.are_characters_at_index(
                    line_to_parse,
                    character_index + 1,
                    self.html_block_2_continued_start,
                ):
                    html_block_type = self.html_block_2
                elif ParserHelper.is_character_at_index_one_of(
                    line_to_parse,
                    character_index + 1,
                    self.html_block_4_continued_start,
                ):
                    html_block_type = self.html_block_4
                elif ParserHelper.are_characters_at_index(
                    line_to_parse,
                    character_index + 1,
                    self.html_block_5_continued_start,
                ):
                    html_block_type = self.html_block_5
            elif ParserHelper.is_character_at_index(
                line_to_parse, character_index, self.html_block_3_continued_start
            ):
                html_block_type = self.html_block_3

        return html_block_type

    def check_for_normal_html_blocks(
        self, remaining_html_tag, line_to_parse, character_index
    ):
        """
        Check for the the html blocks that are harder to identify: 1, 6-7.
        """

        html_block_type = None

        if HtmlHelper.is_valid_block_1_tag_name(remaining_html_tag):
            html_block_type = self.html_block_1
        else:
            adjusted_remaining_html_tag = remaining_html_tag
            is_end_tag = False
            print("6/7?")
            if adjusted_remaining_html_tag.startswith(self.html_tag_start):
                adjusted_remaining_html_tag = adjusted_remaining_html_tag[1:]
                is_end_tag = True
                print("end")
            print(">>" + str(character_index) + ">>" + str(len(line_to_parse)))
            print(">>" + line_to_parse[character_index:] + "<<")
            if (
                character_index < len(line_to_parse)
                and line_to_parse[character_index] == self.html_tag_end
                and adjusted_remaining_html_tag.endswith(self.html_tag_start)
            ):
                adjusted_remaining_html_tag = adjusted_remaining_html_tag[0:-1]
                print("-otherend")
            print(
                "adjusted_remaining_html_tag-->" + adjusted_remaining_html_tag + "<--"
            )
            if adjusted_remaining_html_tag in self.html_block_6_start:
                html_block_type = self.html_block_6
            elif is_end_tag:
                print("end?")
                is_complete, complete_parse_index = HtmlHelper.is_complete_html_end_tag(
                    adjusted_remaining_html_tag, line_to_parse, character_index
                )
                if is_complete:
                    html_block_type = self.html_block_7
                    character_index = complete_parse_index
                    print("7-end")
            else:
                print("7-start?")
                (
                    is_complete,
                    complete_parse_index,
                ) = HtmlHelper.is_complete_html_start_tag(
                    adjusted_remaining_html_tag, line_to_parse, character_index
                )
                if is_complete:
                    html_block_type = self.html_block_7
                    character_index = complete_parse_index
                    print("7-start")
            if html_block_type == self.html_block_7:
                print("7>>EOL check")
                new_index, _ = ParserHelper.extract_whitespace(
                    line_to_parse, character_index
                )
                print(">>" + line_to_parse[character_index:] + "<<")
                if new_index != len(line_to_parse):
                    html_block_type = None
                    print("7>>not EOL, reset")
                else:
                    print("7>>EOL-->" + html_block_type)
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
            print("html_block_type>>" + str(html_block_type))
        if not html_block_type:
            return None, None
        if html_block_type == self.html_block_7:
            print("7>>>" + str(self.stack))
            print("7>>>" + str(self.tokenized_document))
            if self.stack[-1].is_paragraph:
                return None, None
        return html_block_type, remaining_html_tag

    def parse_html_block(self, line_to_parse, start_index, extracted_whitespace):
        """
        Determine if we have the criteria that we need to start an HTML block.
        """

        new_tokens = []
        if (
            ParserHelper.is_length_less_than_or_equal_to(extracted_whitespace, 3)
        ) and ParserHelper.is_character_at_index(
            line_to_parse, start_index, self.html_block_start_character
        ):
            print("HTML-START?")
            html_block_type, remaining_html_tag = self.determine_html_block_type(
                line_to_parse, start_index
            )
            if html_block_type:
                print("HTML-STARTED::" + html_block_type + ":" + remaining_html_tag)
                new_tokens, _, _ = self.close_open_blocks(
                    only_these_blocks=[ParagraphStackToken],
                )
                self.stack.append(
                    HtmlBlockStackToken(html_block_type, remaining_html_tag)
                )
                new_tokens.append(HtmlBlockMarkdownToken())
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

        print("HTML-LINE")
        new_tokens = []
        new_tokens.append(
            TextMarkdownToken(line_to_parse[start_index:], extracted_whitespace)
        )

        is_block_terminated = False
        adj_line = line_to_parse[start_index:]
        if self.stack[-1].html_block_type == self.html_block_1:
            for next_end_tag in self.html_block_1_end_tags:
                if next_end_tag in adj_line:
                    is_block_terminated = True
        elif self.stack[-1].html_block_type == self.html_block_2:
            is_block_terminated = self.html_block_2_end in adj_line
        elif self.stack[-1].html_block_type == self.html_block_3:
            is_block_terminated = self.html_block_3_end in adj_line
        elif self.stack[-1].html_block_type == self.html_block_4:
            is_block_terminated = self.html_block_4_end in adj_line
        elif self.stack[-1].html_block_type == self.html_block_5:
            is_block_terminated = self.html_block_5_end in adj_line

        if is_block_terminated:
            terminated_block_tokens, _, _ = self.close_open_blocks(
                only_these_blocks=[type(self.stack[-1])],
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

        new_tokens = []
        if (
            self.stack[-1].html_block_type == self.html_block_6
            or self.stack[-1].html_block_type == self.html_block_7
        ):
            new_tokens, _, _ = self.close_open_blocks(
                only_these_blocks=[type(self.stack[-1])],
            )

        return new_tokens

    def extract_markdown_tokens_back_to_blank_line(self):
        """
        Extract tokens going back to the last blank line token.
        """

        pre_tokens = []
        while self.tokenized_document[-1].is_blank_line:
            last_element = self.tokenized_document[-1]
            pre_tokens.append(last_element)
            del self.tokenized_document[-1]
        return pre_tokens

    def process_link_reference_definition(
        self, line_to_parse, start_index, original_line_to_parse, extracted_whitespace
    ):
        """
        Process a link deference definition.  Note, this requires a lot of work to
        handle properly because of partial definitions across lines.
        """
        did_complete_lrd = False
        did_pause_lrd = False
        lines_to_requeue = []
        force_ignore_first_as_lrd = False

        was_started = False
        is_blank_line = not line_to_parse and not start_index
        if self.stack[-1].was_link_definition_started:
            was_started = True
            print(
                ">>continuation_lines>>" + str(self.stack[-1].continuation_lines) + "<<"
            )
            line_to_parse = self.stack[-1].get_joined_lines(line_to_parse)
            start_index, extracted_whitespace = ParserHelper.extract_whitespace(
                line_to_parse, 0
            )
            print(">>line_to_parse>>" + line_to_parse.replace("\n", "\\n") + "<<")

        if was_started:
            print(">>parse_link_reference_definition>>was_started")
            (
                did_complete_lrd,
                end_lrd_index,
                parsed_lrd_tuple,
            ) = self.parse_link_reference_definition(
                line_to_parse, start_index, extracted_whitespace, is_blank_line
            )
            print(
                ">>parse_link_reference_definition>>was_started>>did_complete_lrd>>"
                + str(did_complete_lrd)
                + ">>end_lrd_index>>"
                + str(end_lrd_index)
                + ">>len(line_to_parse)>>"
                + str(len(line_to_parse))
            )

            if not (
                did_complete_lrd
                or (
                    not is_blank_line
                    and not did_complete_lrd
                    and (end_lrd_index == len(line_to_parse))
                )
            ):
                print(
                    ">>parse_link_reference_definition>>was_started>>GOT HARD FAILURE"
                )
                (
                    is_blank_line,
                    line_to_parse,
                    did_complete_lrd,
                    end_lrd_index,
                    parsed_lrd_tuple,
                ) = self.process_lrd_hard_failure(
                    original_line_to_parse, lines_to_requeue
                )
        else:
            (
                did_complete_lrd,
                end_lrd_index,
                parsed_lrd_tuple,
            ) = self.parse_link_reference_definition(
                line_to_parse, start_index, extracted_whitespace, is_blank_line
            )
            print(
                ">>parse_link_reference_definition>>did_complete_lrd>>"
                + str(did_complete_lrd)
                + ">>end_lrd_index>>"
                + str(end_lrd_index)
                + ">>len(line_to_parse)>>"
                + str(len(line_to_parse))
            )
        if (
            end_lrd_index >= 0
            and end_lrd_index == len(line_to_parse)
            and not is_blank_line
        ):
            self.add_line_for_lrd_continuation(was_started, original_line_to_parse)
            did_pause_lrd = True
        elif was_started:
            force_ignore_first_as_lrd = self.stop_lrd_continuation(
                did_complete_lrd,
                parsed_lrd_tuple,
                end_lrd_index,
                original_line_to_parse,
                is_blank_line,
            )
        else:
            print(">>parse_link_reference_definition>>other")

        return (
            did_complete_lrd or end_lrd_index != -1,
            did_complete_lrd,
            did_pause_lrd,
            lines_to_requeue,
            force_ignore_first_as_lrd,
        )

    def process_lrd_hard_failure(self, original_line_to_parse, lines_to_requeue):
        """
        In cases of a hard failure, we have had continuations to the original line
        that make it a bit more difficult to figure out if we have an actual good
        LRD in the mix somehow.  So take lines off the end while we have lines.
        """

        do_again = True
        self.stack[-1].add_continuation_line(original_line_to_parse)
        while do_again and self.stack[-1].continuation_lines:
            print(
                "continuation_lines>>" + str(self.stack[-1].continuation_lines) + "<<"
            )

            lines_to_requeue.append(self.stack[-1].continuation_lines[-1])
            print(">>continuation_line>>" + str(self.stack[-1].continuation_lines[-1]))
            del self.stack[-1].continuation_lines[-1]
            print(
                ">>lines_to_requeue>>"
                + str(lines_to_requeue)
                + ">>"
                + str(len(lines_to_requeue))
            )
            print(
                ">>continuation_lines>>" + str(self.stack[-1].continuation_lines) + "<<"
            )
            is_blank_line = True
            line_to_parse = self.stack[-1].get_joined_lines("")
            line_to_parse = line_to_parse[0:-1]
            start_index, extracted_whitespace = ParserHelper.extract_whitespace(
                line_to_parse, 0
            )
            print(">>line_to_parse>>" + line_to_parse.replace("\n", "\\n") + "<<")
            (
                did_complete_lrd,
                end_lrd_index,
                parsed_lrd_tuple,
            ) = self.parse_link_reference_definition(
                line_to_parse, start_index, extracted_whitespace, is_blank_line
            )
            print(
                ">>parse_link_reference_definition>>was_started>>did_complete_lrd>>"
                + str(did_complete_lrd)
                + ">>end_lrd_index>>"
                + str(end_lrd_index)
                + ">>len(line_to_parse)>>"
                + str(len(line_to_parse))
            )
            do_again = not did_complete_lrd
        return (
            is_blank_line,
            line_to_parse,
            did_complete_lrd,
            end_lrd_index,
            parsed_lrd_tuple,
        )

    def add_line_for_lrd_continuation(self, was_started, original_line_to_parse):
        """
        As part of processing a link reference definition, add a line to the continuation.
        """

        if was_started:
            print(">>parse_link_reference_definition>>start already marked")
        else:
            print(">>parse_link_reference_definition>>marking start")
            self.stack.append(LinkDefinitionStackToken())
        self.stack[-1].add_continuation_line(original_line_to_parse)

    # pylint: disable=too-many-arguments
    def stop_lrd_continuation(
        self,
        did_complete_lrd,
        parsed_lrd_tuple,
        end_lrd_index,
        original_line_to_parse,
        is_blank_line,
    ):
        """
        As part of processing a link reference definition, stop a continuation.
        """

        force_ignore_first_as_lrd = False
        print(">>parse_link_reference_definition>>no longer need start")
        del self.stack[-1]
        if did_complete_lrd:
            assert parsed_lrd_tuple
            print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>" + str(self.link_definitions))
            print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>" + str(parsed_lrd_tuple))
            if parsed_lrd_tuple[0] in self.link_definitions:
                # TODO warning?
                print(">>def already present>>" + str(parsed_lrd_tuple[0]))
            else:
                self.link_definitions[parsed_lrd_tuple[0]] = parsed_lrd_tuple[1]
                print(
                    ">>added def>>"
                    + str(parsed_lrd_tuple[0])
                    + "-->"
                    + str(parsed_lrd_tuple[1])
                )

            assert not (end_lrd_index < -1 and original_line_to_parse)
        else:
            assert is_blank_line
            force_ignore_first_as_lrd = True
        return force_ignore_first_as_lrd

    # pylint: enable=too-many-arguments

    # pylint: disable=too-many-arguments
    # pylint: disable=too-many-locals
    # pylint: disable=too-many-branches
    # pylint: disable=too-many-statements
    def parse_line_for_leaf_blocks(
        self,
        line_to_parse,
        start_index,
        this_bq_count,
        no_para_start_if_empty,
        ignore_link_definition_start,
    ):
        """
        Parse the contents of a line for a leaf block.
        """

        print("Leaf Line:" + line_to_parse + ":")
        new_tokens = []
        pre_tokens = []
        lines_to_requeue = []
        force_ignore_first_as_lrd = None
        original_line_to_parse = line_to_parse[start_index:]
        start_index, extracted_whitespace = ParserHelper.extract_whitespace(
            line_to_parse, start_index
        )

        if self.stack[
            -1
        ].is_indented_code_block and ParserHelper.is_length_less_than_or_equal_to(
            extracted_whitespace, 3
        ):
            pre_tokens.append(self.stack[-1].generate_close_token())
            del self.stack[-1]
            pre_tokens.extend(self.extract_markdown_tokens_back_to_blank_line())

        outer_processed = False
        fenced_tokens = None

        if not self.stack[-1].was_link_definition_started:
            fenced_tokens = self.parse_fenced_code_block(
                line_to_parse, start_index, extracted_whitespace
            )
            if fenced_tokens:
                new_tokens.extend(fenced_tokens)
                outer_processed = True
            elif self.stack[-1].is_fenced_code_block:
                new_tokens.append(
                    TextMarkdownToken(line_to_parse[start_index:], extracted_whitespace)
                )
                outer_processed = True

        did_complete_lrd = False
        did_pause_lrd = False
        if not outer_processed and not ignore_link_definition_start:
            print(
                "plflb-process_link_reference_definition>>outer_processed>>"
                + line_to_parse[start_index:]
            )
            (
                outer_processed,
                did_complete_lrd,
                did_pause_lrd,
                lines_to_requeue,
                force_ignore_first_as_lrd,
            ) = self.process_link_reference_definition(
                line_to_parse, start_index, original_line_to_parse, extracted_whitespace
            )
            if lines_to_requeue:
                outer_processed = True
            print(
                "plflb-process_link_reference_definition>>outer_processed>>"
                + str(outer_processed)
                + ">did_complete_lrd>"
                + str(did_complete_lrd)
                + "<did_pause_lrd<"
                + str(did_pause_lrd)
                + "<lines_to_requeue<"
                + str(lines_to_requeue)
                + "<"
                + str(len(lines_to_requeue))
            )

        if not outer_processed and not self.stack[-1].is_html_block:
            html_tokens = self.parse_html_block(
                line_to_parse, start_index, extracted_whitespace
            )
            new_tokens.extend(html_tokens)
        if self.stack[-1].is_html_block:
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
                    line_to_parse, start_index, extracted_whitespace, this_bq_count,
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

        assert new_tokens or did_complete_lrd or did_pause_lrd or lines_to_requeue
        print(">>leaf--adding>>" + str(new_tokens))
        pre_tokens.extend(new_tokens)
        return pre_tokens, lines_to_requeue, force_ignore_first_as_lrd

    # pylint: enable=too-many-locals
    # pylint: enable=too-many-arguments
    # pylint: enable=too-many-branches
    # pylint: enable=too-many-statements
