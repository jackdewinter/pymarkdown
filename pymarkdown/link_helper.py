# pylint: disable=too-many-lines
"""
Link helper
"""
import urllib

from pymarkdown.constants import Constants
from pymarkdown.emphasis_helper import EmphasisHelper
from pymarkdown.inline_helper import InlineHelper
from pymarkdown.markdown_token import (
    EndMarkdownToken,
    ImageStartMarkdownToken,
    LinkStartMarkdownToken,
    MarkdownToken,
    SpecialTextMarkdownToken,
    TextMarkdownToken,
)
from pymarkdown.parser_helper import ParserHelper
from pymarkdown.stack_token import LinkDefinitionStackToken


class LinkHelper:
    """
    Class to helper with the parsing of links.
    """

    __link_definitions = {}

    __non_angle_link_breaks = Constants.ascii_control_characters + "()\\"

    @staticmethod
    def initialize():
        """
        Initialize the inline subsystem.
        """
        LinkHelper.__link_definitions = {}

    @staticmethod
    def __consume_text_for_image_alt_text(inline_blocks, ind, remaining_line):
        """
        Consume text from the inline blocks to use as part of the image's alt text.
        """

        image_alt_text = ""
        print(">>" + str(inline_blocks[ind + 1 :]) + "<<")
        while len(inline_blocks) > (ind + 1):
            if isinstance(inline_blocks[ind + 1], SpecialTextMarkdownToken):
                pass
            elif isinstance(inline_blocks[ind + 1], TextMarkdownToken):
                image_alt_text = image_alt_text + inline_blocks[ind + 1].token_text
            elif isinstance(inline_blocks[ind + 1], ImageStartMarkdownToken):
                image_alt_text = image_alt_text + inline_blocks[ind + 1].image_alt_text
            del inline_blocks[ind + 1]
        image_alt_text = image_alt_text + remaining_line
        return image_alt_text

    @staticmethod
    def __collect_text_from_blocks(inline_blocks, ind, suffix_text):
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

    @staticmethod
    def __extract_link_label(line_to_parse, new_index, include_reference_colon=True):
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
                _, new_index, _ = InlineHelper.handle_inline_backslash(
                    line_to_parse, new_index
                )
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

    @staticmethod
    def __parse_angle_link_destination(source_text, new_index):
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
                _, new_index, _ = InlineHelper.handle_inline_backslash(
                    source_text, new_index
                )
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

    @staticmethod
    def __parse_non_angle_link_destination(source_text, new_index):
        """
        Parse a link destination that is not included in angle brackets.
        """

        collected_destination = ""
        nesting_level = 0
        keep_collecting = True
        while keep_collecting:
            print(
                "collected_destination>>"
                + str(collected_destination)
                + "<<source_text<<"
                + source_text[new_index:]
                + ">>nesting_level>>"
                + str(nesting_level)
                + ">>"
            )
            keep_collecting = False
            new_index, before_part = ParserHelper.collect_until_one_of_characters(
                source_text, new_index, LinkHelper.__non_angle_link_breaks
            )
            collected_destination = collected_destination + before_part
            print(">>>>>>" + source_text[new_index:] + "<<<<<")
            if ParserHelper.is_character_at_index(source_text, new_index, "\\"):
                print("backslash")
                old_new_index = new_index
                _, new_index, _ = InlineHelper.handle_inline_backslash(
                    source_text, new_index
                )
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

    @staticmethod
    def __parse_link_destination(source_text, new_index):
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
            new_index, ex_link = LinkHelper.__parse_angle_link_destination(
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
            new_index, ex_link = LinkHelper.__parse_non_angle_link_destination(
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
            ex_link = InlineHelper.handle_backslashes(ex_link)
        print("urllib.parse.quote>>ex_link>>" + str(ex_link) + ">>")

        ex_link = urllib.parse.quote(ex_link, safe="/#:?=()%*")
        print(
            "parse_link_destination>>new_index>>"
            + str(new_index)
            + ">>ex_link>>"
            + str(ex_link)
            + ">>"
        )
        return ex_link, new_index

    @staticmethod
    def __parse_link_title(source_text, new_index):
        """
        Parse an inline link's link title.
        """

        print("parse_link_title>>new_index>>" + source_text[new_index:] + ">>")
        ex_title = ""
        if ParserHelper.is_character_at_index(source_text, new_index, "'"):
            new_index, ex_title = InlineHelper.extract_bounded_string(
                source_text, new_index + 1, "'", None
            )
        elif ParserHelper.is_character_at_index(source_text, new_index, '"'):
            new_index, ex_title = InlineHelper.extract_bounded_string(
                source_text, new_index + 1, '"', None
            )
        elif ParserHelper.is_character_at_index(source_text, new_index, "("):
            new_index, ex_title = InlineHelper.extract_bounded_string(
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
            ex_title = InlineHelper.append_text(
                "", InlineHelper.handle_backslashes(ex_title)
            )
        print("parse_link_title>>after>>" + str(ex_title) + ">>")

        return ex_title, new_index

    @staticmethod
    def __extract_link_title(line_to_parse, new_index, is_blank_line):
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
            inline_title, new_index = LinkHelper.__parse_link_title(
                line_to_parse, new_index
            )
            if new_index == -1:
                return False, -1, None
            if inline_title is None:
                return False, new_index, None
        return True, new_index, inline_title

    @staticmethod
    def __process_inline_link_body(source_text, new_index):
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
            inline_link, new_index = LinkHelper.__parse_link_destination(
                source_text, new_index
            )
            if new_index != -1:
                print("before ws>>" + source_text[new_index:] + ">")
                new_index, _ = ParserHelper.extract_any_whitespace(
                    source_text, new_index
                )
                print("after ws>>" + source_text[new_index:] + ">")
                if ParserHelper.is_character_at_index_not(source_text, new_index, ")"):
                    inline_title, new_index = LinkHelper.__parse_link_title(
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

    @staticmethod
    def __normalize_link_label(link_label):
        """
        Translate a link label into a normalized form to use for comparisons.
        """

        # Fold all whitespace characters (except for space) into a space character
        link_label = ParserHelper.replace_any_of(
            link_label, Constants.non_space_whitespace, " "
        )

        # Fold multiple spaces into a single space character.
        link_label = " ".join(link_label.split())

        # Fold the case of any characters to their lower equivalent.
        link_label = link_label.casefold().strip()
        return link_label

    @staticmethod
    def __extract_link_destination(line_to_parse, new_index, is_blank_line):
        """
        Extract the link reference definition's link destination.
        """
        new_index, _ = ParserHelper.collect_while_one_of_characters(
            line_to_parse, new_index, Constants.whitespace
        )
        if new_index == len(line_to_parse) and not is_blank_line:
            return False, new_index, None

        print("LD>>" + line_to_parse[new_index:] + "<<")
        inline_link, new_index = LinkHelper.__parse_link_destination(
            line_to_parse, new_index
        )
        if new_index == -1:
            return False, -1, None
        return True, new_index, inline_link

    @staticmethod
    def __verify_link_definition_end(line_to_parse, new_index):
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

    @staticmethod
    def __is_link_reference_definition(
        token_stack, line_to_parse, start_index, extracted_whitespace
    ):
        """
        Determine whether or not we have the start of a link reference definition.
        """

        if token_stack[-1].is_paragraph:
            return False

        if (
            ParserHelper.is_length_less_than_or_equal_to(extracted_whitespace, 3)
        ) and ParserHelper.is_character_at_index_one_of(
            line_to_parse, start_index, "["
        ):
            return True
        return False

    @staticmethod
    def __parse_link_reference_definition(
        token_stack, line_to_parse, start_index, extracted_whitespace, is_blank_line,
    ):
        """
        Handle the parsing of what appears to be a link reference definition.
        """
        did_start = LinkHelper.__is_link_reference_definition(
            token_stack, line_to_parse, start_index, extracted_whitespace
        )
        if not did_start:
            return False, -1, None

        print("\nparse_link_reference_definition")
        inline_title = ""
        keep_going, new_index, collected_destination = LinkHelper.__extract_link_label(
            line_to_parse, start_index + 1
        )
        if keep_going:
            keep_going, new_index, inline_link = LinkHelper.__extract_link_destination(
                line_to_parse, new_index, is_blank_line
            )
        if keep_going:
            keep_going, new_index, inline_title = LinkHelper.__extract_link_title(
                line_to_parse, new_index, is_blank_line
            )
        if keep_going:
            keep_going, new_index = LinkHelper.__verify_link_definition_end(
                line_to_parse, new_index
            )
        if keep_going:
            collected_destination = LinkHelper.__normalize_link_label(
                collected_destination
            )
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

    @staticmethod
    def __look_up_link(link_to_lookup, new_index, link_type):
        """
        Look up a link to see if it is present.
        """

        inline_link = ""
        inline_title = ""
        link_label = LinkHelper.__normalize_link_label(link_to_lookup)
        if not link_label or link_label not in LinkHelper.__link_definitions:
            update_index = -1
        else:
            print(link_type)
            update_index = new_index
            inline_link = LinkHelper.__link_definitions[link_label][0]
            inline_title = LinkHelper.__link_definitions[link_label][1]
        return update_index, inline_link, inline_title

    # pylint: disable=too-many-locals
    # pylint: disable=too-many-arguments
    @staticmethod
    def __handle_link_types(
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
        text_from_blocks = LinkHelper.__collect_text_from_blocks(
            inline_blocks, ind, current_string_unresolved + remaining_line
        )
        print("handle_link_types>>text_from_blocks>>" + text_from_blocks + "<<")

        consume_rest_of_line = False
        update_index = -1
        inline_link = None
        inline_title = None
        tried_full_reference_form = False
        if ParserHelper.is_character_at_index(source_text, new_index, "("):
            print("inline reference?")
            (
                inline_link,
                inline_title,
                update_index,
            ) = LinkHelper.__process_inline_link_body(source_text, new_index + 1)
        elif ParserHelper.is_character_at_index(source_text, new_index, "["):
            print("collapsed reference?")
            after_open_index = new_index + 1
            if ParserHelper.is_character_at_index(source_text, after_open_index, "]"):
                print("collapsed reference")
                print(">>" + text_from_blocks + ">>")
                update_index, inline_link, inline_title = LinkHelper.__look_up_link(
                    text_from_blocks, after_open_index + 1, "collapsed reference"
                )
                tried_full_reference_form = True
            else:
                print("full reference?")
                print(">>did_extract>>" + source_text[after_open_index:] + ">")
                (
                    did_extract,
                    after_label_index,
                    ex_label,
                ) = LinkHelper.__extract_link_label(
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
                    update_index, inline_link, inline_title = LinkHelper.__look_up_link(
                        ex_label, after_label_index, "full reference"
                    )

        if update_index == -1 and not tried_full_reference_form:
            print("shortcut?")
            print(">>" + str(inline_blocks) + "<<")
            print(">>" + str(text_from_blocks) + "<<")
            update_index, inline_link, inline_title = LinkHelper.__look_up_link(
                text_from_blocks, new_index, "shortcut"
            )

        token_to_append = None
        if update_index != -1:
            print("<<<<<<<start_text<<<<<<<" + str(start_text) + "<<")
            if start_text == "[":
                inline_blocks[ind] = LinkStartMarkdownToken(
                    link_uri=inline_link, link_title=inline_title
                )
                token_to_append = EndMarkdownToken(
                    MarkdownToken.token_inline_link, "", ""
                )
            else:

                consume_rest_of_line = True
                image_alt_text = LinkHelper.__consume_text_for_image_alt_text(
                    inline_blocks, ind, remaining_line
                )

                inline_blocks[ind] = ImageStartMarkdownToken(
                    image_uri=inline_link,
                    image_title=inline_title,
                    image_alt_text=image_alt_text,
                )
                print("\n>>Image>>" + str(inline_blocks))
                print(">>start_text>>" + str(start_text) + "<<")
                print(">>remaining_line>>" + str(remaining_line) + "<<")
                print(
                    ">>current_string_unresolved>>"
                    + str(current_string_unresolved)
                    + "<<"
                )
                # assert False

        print(
            "handle_link_types<update_index<"
            + str(update_index)
            + "<<"
            + str(token_to_append)
            + "<<"
        )
        return update_index, token_to_append, consume_rest_of_line

    # pylint: enable=too-many-locals
    # pylint: enable=too-many-arguments

    @staticmethod
    def look_for_link_or_image(
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
        consume_rest_of_line = False
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
                        (
                            updated_index,
                            token_to_append,
                            consume_rest_of_line,
                        ) = LinkHelper.__handle_link_types(
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
            + str(consume_rest_of_line)
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

            print("\nresolve_inline_emphasis>>" + str(inline_blocks))
            EmphasisHelper.resolve_inline_emphasis(
                inline_blocks, inline_blocks[search_index]
            )
            print("resolve_inline_emphasis>>" + str(inline_blocks) + "\n")

            if valid_special_start_text == "[":
                for deactivate_token in inline_blocks:
                    if isinstance(deactivate_token, SpecialTextMarkdownToken):
                        print("inline_blocks>>>>>>>>>>>>>>>>>>" + str(deactivate_token))
                        if deactivate_token.token_text == "[":
                            deactivate_token.active = False
            return updated_index, True, token_to_append, consume_rest_of_line
        is_active = False
        return new_index, is_active, token_to_append, consume_rest_of_line

    @staticmethod
    def __add_line_for_lrd_continuation(
        token_stack, was_started, original_line_to_parse
    ):
        """
        As part of processing a link reference definition, add a line to the continuation.
        """

        if was_started:
            print(">>parse_link_reference_definition>>start already marked")
        else:
            print(">>parse_link_reference_definition>>marking start")
            token_stack.append(LinkDefinitionStackToken())
        token_stack[-1].add_continuation_line(original_line_to_parse)

    # pylint: disable=too-many-arguments
    @staticmethod
    def __stop_lrd_continuation(
        token_stack,
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
        del token_stack[-1]
        if did_complete_lrd:
            assert parsed_lrd_tuple
            print(
                ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"
                + str(LinkHelper.__link_definitions)
            )
            print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>" + str(parsed_lrd_tuple))
            if parsed_lrd_tuple[0] in LinkHelper.__link_definitions:
                # TODO warning?
                print(">>def already present>>" + str(parsed_lrd_tuple[0]))
            else:
                LinkHelper.__link_definitions[parsed_lrd_tuple[0]] = parsed_lrd_tuple[1]
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

    @staticmethod
    def __process_lrd_hard_failure(
        token_stack, original_line_to_parse, lines_to_requeue
    ):
        """
        In cases of a hard failure, we have had continuations to the original line
        that make it a bit more difficult to figure out if we have an actual good
        LRD in the mix somehow.  So take lines off the end while we have lines.
        """

        do_again = True
        token_stack[-1].add_continuation_line(original_line_to_parse)
        while do_again and token_stack[-1].continuation_lines:
            print(
                "continuation_lines>>" + str(token_stack[-1].continuation_lines) + "<<"
            )

            lines_to_requeue.append(token_stack[-1].continuation_lines[-1])
            print(">>continuation_line>>" + str(token_stack[-1].continuation_lines[-1]))
            del token_stack[-1].continuation_lines[-1]
            print(
                ">>lines_to_requeue>>"
                + str(lines_to_requeue)
                + ">>"
                + str(len(lines_to_requeue))
            )
            print(
                ">>continuation_lines>>"
                + str(token_stack[-1].continuation_lines)
                + "<<"
            )
            is_blank_line = True
            line_to_parse = token_stack[-1].get_joined_lines("")
            line_to_parse = line_to_parse[0:-1]
            start_index, extracted_whitespace = ParserHelper.extract_whitespace(
                line_to_parse, 0
            )
            print(">>line_to_parse>>" + line_to_parse.replace("\n", "\\n") + "<<")
            (
                did_complete_lrd,
                end_lrd_index,
                parsed_lrd_tuple,
            ) = LinkHelper.__parse_link_reference_definition(
                token_stack,
                line_to_parse,
                start_index,
                extracted_whitespace,
                is_blank_line,
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

    @staticmethod
    def process_link_reference_definition(
        token_stack,
        line_to_parse,
        start_index,
        original_line_to_parse,
        extracted_whitespace,
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
        if token_stack[-1].was_link_definition_started:
            was_started = True
            print(
                ">>continuation_lines>>"
                + str(token_stack[-1].continuation_lines)
                + "<<"
            )
            line_to_parse = token_stack[-1].get_joined_lines(line_to_parse)
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
            ) = LinkHelper.__parse_link_reference_definition(
                token_stack,
                line_to_parse,
                start_index,
                extracted_whitespace,
                is_blank_line,
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
                ) = LinkHelper.__process_lrd_hard_failure(
                    token_stack, original_line_to_parse, lines_to_requeue
                )
        else:
            (
                did_complete_lrd,
                end_lrd_index,
                parsed_lrd_tuple,
            ) = LinkHelper.__parse_link_reference_definition(
                token_stack,
                line_to_parse,
                start_index,
                extracted_whitespace,
                is_blank_line,
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
            LinkHelper.__add_line_for_lrd_continuation(
                token_stack, was_started, original_line_to_parse
            )
            did_pause_lrd = True
        elif was_started:
            force_ignore_first_as_lrd = LinkHelper.__stop_lrd_continuation(
                token_stack,
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
