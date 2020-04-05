"""
Link helper
"""
import urllib

from pymarkdown.constants import Constants
from pymarkdown.emphasis_helper import EmphasisHelper
from pymarkdown.inline_helper import InlineHelper, InlineRequest
from pymarkdown.markdown_token import (
    EndMarkdownToken,
    ImageStartMarkdownToken,
    LinkStartMarkdownToken,
    MarkdownToken,
    SpecialTextMarkdownToken,
    TextMarkdownToken,
)
from pymarkdown.parser_helper import ParserHelper


class LinkHelper:
    """
    Class to helper with the parsing of links.
    """

    __link_definitions = {}
    __link_safe_characters = "/#:?=()*!$'+,;@"

    __special_link_destination_characters = "%&"

    __non_angle_link_nest = "("
    __non_angle_link_unnest = ")"
    __non_angle_link_breaks = Constants.ascii_control_characters + "()\\"

    link_label_start = "["
    link_label_end = "]"
    __link_label_is_definition_character = ":"
    __link_label_breaks = (
        link_label_start + link_label_end + InlineHelper.backslash_character
    )

    __angle_link_start = "<"
    __angle_link_end = ">"
    __angle_link_destination_breaks = (
        __angle_link_end + InlineHelper.backslash_character
    )

    __link_title_single = "'"
    __link_title_double = '"'
    __link_title_parenthesis_open = "("
    __link_title_parenthesis_close = ")"

    __link_format_inline_start = "("
    __link_format_inline_end = ")"
    __link_format_reference_start = "["
    __link_format_reference_end = "]"

    __link_start_sequence = "["
    image_start_sequence = "!["
    __valid_link_starts = [__link_start_sequence, image_start_sequence]

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
            collect_index += 1
        collected_text = collected_text + suffix_text
        print(">>collect_text_from_blocks>>" + str(collected_text) + "<<")
        return collected_text

    @staticmethod
    def extract_link_label(line_to_parse, new_index, include_reference_colon=True):
        """
        Extract the link reference definition's link label.
        """

        collected_destination = ""
        keep_collecting = True
        while keep_collecting:
            keep_collecting = False
            new_index, ert_new = ParserHelper.collect_until_one_of_characters(
                line_to_parse, new_index, LinkHelper.__link_label_breaks
            )
            collected_destination = collected_destination + ert_new
            if ParserHelper.is_character_at_index(
                line_to_parse, new_index, InlineHelper.backslash_character
            ):
                old_new_index = new_index
                inline_request = InlineRequest(line_to_parse, new_index)
                inline_response = InlineHelper.handle_inline_backslash(inline_request)
                new_index = inline_response.new_index
                collected_destination = (
                    collected_destination + line_to_parse[old_new_index:new_index]
                )
                keep_collecting = True
            elif ParserHelper.is_character_at_index(
                line_to_parse, new_index, LinkHelper.link_label_start
            ):
                print(">> unescaped [, bailing")
                return False, -1, None

        print("look for ]>>" + line_to_parse[new_index:] + "<<")
        if not ParserHelper.is_character_at_index(
            line_to_parse, new_index, LinkHelper.link_label_end
        ):
            print(">> no end ], bailing")
            return False, new_index, None
        new_index += 1

        if include_reference_colon:
            print("look for :>>" + line_to_parse[new_index:] + "<<")
            if not ParserHelper.is_character_at_index(
                line_to_parse,
                new_index,
                LinkHelper.__link_label_is_definition_character,
            ):
                print(">> no :, bailing")
                return False, -1, None
            new_index += 1

        return True, new_index, collected_destination

    @staticmethod
    def __parse_angle_link_destination(source_text, new_index):
        """
        Parse a link destination that is included in angle brackets.
        """

        collected_destination = ""
        new_index += 1
        keep_collecting = True
        while keep_collecting:
            keep_collecting = False
            new_index, ert_new = ParserHelper.collect_until_one_of_characters(
                source_text, new_index, LinkHelper.__angle_link_destination_breaks
            )
            collected_destination = collected_destination + ert_new
            if ParserHelper.is_character_at_index(
                source_text, new_index, InlineHelper.backslash_character
            ):
                old_new_index = new_index
                inline_request = InlineRequest(source_text, new_index)
                inline_response = InlineHelper.handle_inline_backslash(inline_request)
                new_index = inline_response.new_index
                collected_destination = (
                    collected_destination + source_text[old_new_index:new_index]
                )
                keep_collecting = True

        if ParserHelper.is_character_at_index(
            source_text, new_index, LinkHelper.__angle_link_end
        ):
            new_index += 1
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
            if ParserHelper.is_character_at_index(
                source_text, new_index, InlineHelper.backslash_character
            ):
                print("backslash")
                old_new_index = new_index
                inline_request = InlineRequest(source_text, new_index)
                inline_response = InlineHelper.handle_inline_backslash(inline_request)
                new_index = inline_response.new_index
                collected_destination = (
                    collected_destination + source_text[old_new_index:new_index]
                )
                keep_collecting = True
            elif ParserHelper.is_character_at_index(
                source_text, new_index, LinkHelper.__non_angle_link_nest
            ):
                print("+1")
                nesting_level += 1
                collected_destination += LinkHelper.__non_angle_link_nest
                new_index += 1
                keep_collecting = True
            elif ParserHelper.is_character_at_index(
                source_text, new_index, LinkHelper.__non_angle_link_unnest
            ):
                print("-1")
                if nesting_level != 0:
                    collected_destination += LinkHelper.__non_angle_link_unnest
                    new_index += 1
                    nesting_level -= 1
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
        if ParserHelper.is_character_at_index(
            source_text, new_index, LinkHelper.__angle_link_start
        ):
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

        ex_link = LinkHelper.__encode_link_destination(ex_link)
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
        if ParserHelper.is_character_at_index(
            source_text, new_index, LinkHelper.__link_title_single
        ):
            new_index, ex_title = InlineHelper.extract_bounded_string(
                source_text, new_index + 1, LinkHelper.__link_title_single, None
            )
        elif ParserHelper.is_character_at_index(
            source_text, new_index, LinkHelper.__link_title_double
        ):
            new_index, ex_title = InlineHelper.extract_bounded_string(
                source_text, new_index + 1, LinkHelper.__link_title_double, None
            )
        elif ParserHelper.is_character_at_index(
            source_text, new_index, LinkHelper.__link_title_parenthesis_open
        ):
            new_index, ex_title = InlineHelper.extract_bounded_string(
                source_text,
                new_index + 1,
                LinkHelper.__link_title_parenthesis_close,
                LinkHelper.__link_title_parenthesis_open,
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
    def extract_link_title(line_to_parse, new_index, is_blank_line):
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
        if not ParserHelper.is_character_at_index(
            source_text, new_index, LinkHelper.__link_format_inline_end
        ):
            inline_link, new_index = LinkHelper.__parse_link_destination(
                source_text, new_index
            )
            if new_index != -1:
                print("before ws>>" + source_text[new_index:] + ">")
                new_index, _ = ParserHelper.extract_any_whitespace(
                    source_text, new_index
                )
                print("after ws>>" + source_text[new_index:] + ">")
                if ParserHelper.is_character_at_index_not(
                    source_text, new_index, LinkHelper.__link_format_inline_end
                ):
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
            if ParserHelper.is_character_at_index(
                source_text, new_index, LinkHelper.__link_format_inline_end
            ):
                new_index += 1
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
    def normalize_link_label(link_label):
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
    def extract_link_destination(line_to_parse, new_index, is_blank_line):
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
    def __look_up_link(link_to_lookup, new_index, link_type):
        """
        Look up a link to see if it is present.
        """

        inline_link = ""
        inline_title = ""
        link_label = LinkHelper.normalize_link_label(link_to_lookup)
        if not link_label or link_label not in LinkHelper.__link_definitions:
            update_index = -1
        else:
            print(link_type)
            update_index = new_index
            inline_link = LinkHelper.__link_definitions[link_label][0]
            inline_title = LinkHelper.__link_definitions[link_label][1]
        return update_index, inline_link, inline_title

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

        (
            inline_link,
            inline_title,
            update_index,
            tried_full_reference_form,
        ) = LinkHelper.look_for_link_formats(source_text, new_index, text_from_blocks)

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
            if start_text == LinkHelper.__link_start_sequence:
                inline_blocks[ind] = LinkStartMarkdownToken(
                    link_uri=inline_link, link_title=inline_title
                )
                token_to_append = EndMarkdownToken(
                    MarkdownToken.token_inline_link, "", ""
                )
            else:
                assert start_text == LinkHelper.image_start_sequence
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

    # pylint: enable=too-many-arguments

    @staticmethod
    def look_for_link_formats(source_text, new_index, text_from_blocks):
        """
        Look for links in the various formats.
        """
        inline_link = ""
        inline_title = ""
        update_index = -1
        tried_full_reference_form = False
        if ParserHelper.is_character_at_index(
            source_text, new_index, LinkHelper.__link_format_inline_start
        ):
            print("inline reference?")
            (
                inline_link,
                inline_title,
                update_index,
            ) = LinkHelper.__process_inline_link_body(source_text, new_index + 1)
        elif ParserHelper.is_character_at_index(
            source_text, new_index, LinkHelper.__link_format_reference_start
        ):
            print("collapsed reference?")
            after_open_index = new_index + 1
            if ParserHelper.is_character_at_index(
                source_text, after_open_index, LinkHelper.__link_format_reference_end
            ):
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
                ) = LinkHelper.extract_link_label(
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
        return inline_link, inline_title, update_index, tried_full_reference_form

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
                if (
                    inline_blocks[search_index].token_text
                    in LinkHelper.__valid_link_starts
                ):
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
            search_index -= 1

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

            if valid_special_start_text == LinkHelper.__link_start_sequence:
                for deactivate_token in inline_blocks:
                    if isinstance(deactivate_token, SpecialTextMarkdownToken):
                        print("inline_blocks>>>>>>>>>>>>>>>>>>" + str(deactivate_token))
                        if (
                            deactivate_token.token_text
                            == LinkHelper.__link_start_sequence
                        ):
                            deactivate_token.active = False
            return updated_index, True, token_to_append, consume_rest_of_line
        is_active = False
        return new_index, is_active, token_to_append, consume_rest_of_line

    @staticmethod
    def add_link_definition(link_name, link_value):
        """
        Add a link definition to the cache of links.
        """
        print(
            ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"
            + str(LinkHelper.__link_definitions)
        )
        print(
            ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"
            + str(link_name)
            + ":"
            + str(link_value)
        )
        if link_name in LinkHelper.__link_definitions:
            # TODO warning?
            print(">>def already present>>" + str(link_name))
        else:
            LinkHelper.__link_definitions[link_name] = link_value
            print(">>added def>>" + str(link_name) + "-->" + str(link_value))

    @staticmethod
    def __encode_link_destination(link_to_encode):

        encoded_link = ""
        percent_index, before_data = ParserHelper.collect_until_one_of_characters(link_to_encode, 0, LinkHelper.__special_link_destination_characters)
        encoded_link += urllib.parse.quote(before_data, safe=LinkHelper.__link_safe_characters)
        while percent_index < len(link_to_encode):
            special_character = link_to_encode[percent_index]
            percent_index += 1
            if special_character == "%":
                hex_guess_characters = link_to_encode[percent_index:percent_index+2]
                if len(hex_guess_characters) == 2:
                    try:
                        int(hex_guess_characters, 16)
                        encoded_link += "%" + hex_guess_characters
                        percent_index += 2
                    except ValueError:
                        encoded_link += "%25"
                else:
                    encoded_link += "%25"
            else:
                assert special_character == "&"
                encoded_link += "&amp;"

            percent_index, before_data = ParserHelper.collect_until_one_of_characters(link_to_encode, percent_index, LinkHelper.__special_link_destination_characters)
            encoded_link += urllib.parse.quote(before_data, safe=LinkHelper.__link_safe_characters)
        return encoded_link
