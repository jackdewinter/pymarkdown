"""
Link helper
"""
import logging
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
)
from pymarkdown.parser_helper import ParserHelper

LOGGER = logging.getLogger(__name__)


# pylint: disable=too-many-lines
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
    def add_link_definition(link_name, link_value):
        """
        Add a link definition to the cache of links.
        """
        LOGGER.debug(
            ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>%s",
            str(LinkHelper.__link_definitions),
        )
        LOGGER.debug(
            ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>%s:%s",
            str(link_name),
            str(link_value),
        )
        did_add_definition = False
        if link_name in LinkHelper.__link_definitions:
            LOGGER.debug(">>def already present>>%s", str(link_name))
        else:
            LinkHelper.__link_definitions[link_name] = link_value
            did_add_definition = True
            LOGGER.debug(">>added def>>%s-->%s", str(link_name), str(link_value))
        return did_add_definition

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
                LOGGER.debug(">> unescaped [, bailing")
                return False, -1, None

        LOGGER.debug("look for ]>>%s<<", line_to_parse[new_index:])
        if not ParserHelper.is_character_at_index(
            line_to_parse, new_index, LinkHelper.link_label_end
        ):
            LOGGER.debug(">> no end ], bailing")
            return False, new_index, None
        new_index += 1

        if include_reference_colon:
            LOGGER.debug("look for :>>%s<<", line_to_parse[new_index:])
            if not ParserHelper.is_character_at_index(
                line_to_parse,
                new_index,
                LinkHelper.__link_label_is_definition_character,
            ):
                LOGGER.debug(">> no :, bailing")
                return False, -1, None
            new_index += 1

        return True, new_index, collected_destination

    @staticmethod
    def extract_link_title(line_to_parse, new_index, is_blank_line):
        """
        Extract the link reference definition's optional link title.
        """
        inline_title = ""
        pre_inline_title = ""
        LOGGER.debug("before ws>>%s>", line_to_parse[new_index:])
        new_index, ex_ws = ParserHelper.extract_any_whitespace(line_to_parse, new_index)
        LOGGER.debug(
            "after ws>>%s>ex_ws>%s",
            line_to_parse[new_index:],
            ParserHelper.make_value_visible(ex_ws),
        )
        start_index = new_index
        if new_index == len(line_to_parse) and not is_blank_line:
            return False, new_index, None, None, None, None
        if ex_ws and new_index < len(line_to_parse):
            (
                inline_title,
                pre_inline_title,
                new_index,
                _,
            ) = LinkHelper.__parse_link_title(line_to_parse, new_index)
            if new_index == -1:
                return False, -1, None, None, None, None
            if inline_title is None:
                return False, new_index, None, None, None, None
        return (
            True,
            new_index,
            inline_title,
            pre_inline_title,
            ex_ws,
            line_to_parse[start_index:new_index],
        )

    @staticmethod
    def extract_link_destination(line_to_parse, new_index, is_blank_line):
        """
        Extract the link reference definition's link destination.
        """
        new_index, prefix_whitespace = ParserHelper.collect_while_one_of_characters(
            line_to_parse, new_index, Constants.whitespace
        )
        if new_index == len(line_to_parse) and not is_blank_line:
            return False, new_index, None, None, None, None

        LOGGER.debug("LD>>%s<<", line_to_parse[new_index:])
        (
            inline_link,
            pre_inline_link,
            new_index,
            inline_raw_link,
            _,
        ) = LinkHelper.__parse_link_destination(line_to_parse, new_index)
        if new_index == -1:
            return False, -1, None, None, None, None
        return (
            True,
            new_index,
            inline_link,
            pre_inline_link,
            prefix_whitespace,
            inline_raw_link,
        )

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

    # pylint: disable=too-many-arguments
    @staticmethod
    def look_for_link_or_image(
        inline_blocks,
        source_text,
        next_index,
        remaining_line,
        current_string_unresolved,
        xx_fn,
    ):
        """
        Given that a link close character has been found, process it to see if
        there is actually enough other text to properly construct the link.
        """

        LOGGER.debug(">>look_for_link_or_image>>%s<<", str(inline_blocks))
        LOGGER.debug(">>source_text>>%s<<", str(source_text))
        LOGGER.debug(">>next_index>>%s<<", str(next_index))
        LOGGER.debug(">>remaining_line>>%s<<", str(remaining_line))
        LOGGER.debug(
            ">>current_string_unresolved>>%s<<", str(current_string_unresolved)
        )
        is_valid = False
        consume_rest_of_line = False
        new_index = next_index + 1
        updated_index = -1
        token_to_append = None

        LOGGER.debug("LOOKING FOR START")
        LinkHelper.__display_specials_in_tokens(inline_blocks)

        valid_special_start_text = None
        search_index = len(inline_blocks) - 1
        while search_index >= 0:
            if isinstance(inline_blocks[search_index], SpecialTextMarkdownToken):
                LOGGER.debug(
                    "search_index>>%s>>%s",
                    str(search_index),
                    inline_blocks[search_index].show_process_emphasis(),
                )
                if (
                    inline_blocks[search_index].token_text
                    in LinkHelper.__valid_link_starts
                ):
                    valid_special_start_text = inline_blocks[search_index].token_text
                    if inline_blocks[search_index].active:
                        LOGGER.debug(">>>>>>%s", str(inline_blocks))
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
                            xx_fn,
                        )
                        if updated_index != -1:
                            is_valid = True
                            break

                    LOGGER.debug("  not active:%s", str(search_index))
                    LinkHelper.__revert_token_to_normal_text_token(
                        inline_blocks, search_index
                    )
                    break
                LOGGER.debug("  not link")
            search_index -= 1

        LOGGER.debug(
            ">>look_for_link_or_image>>%s<<is_valid<<%s<<%s<<",
            str(inline_blocks),
            str(is_valid),
            str(consume_rest_of_line),
        )
        if is_valid:
            # if link set all [ before to inactive
            LOGGER.debug("")
            LOGGER.debug("SET TO INACTIVE-->%s", str(valid_special_start_text))
            LOGGER.debug("ind-->%s", str(search_index))

            assert isinstance(
                inline_blocks[search_index],
                (LinkStartMarkdownToken, ImageStartMarkdownToken),
            )

            LOGGER.debug("\nresolve_inline_emphasis>>%s", str(inline_blocks))
            EmphasisHelper.resolve_inline_emphasis(
                inline_blocks, inline_blocks[search_index]
            )
            LOGGER.debug("resolve_inline_emphasis>>%s\n", str(inline_blocks))

            if valid_special_start_text == LinkHelper.__link_start_sequence:
                LOGGER.debug("DEACTIVATING")
                LinkHelper.__display_specials_in_tokens(inline_blocks)
                for deactivate_token in inline_blocks:
                    if isinstance(deactivate_token, SpecialTextMarkdownToken):
                        LOGGER.debug(
                            "inline_blocks>>>>>>>>>>>>>>>>>>%s", str(deactivate_token)
                        )
                        if (
                            deactivate_token.token_text
                            == LinkHelper.__link_start_sequence
                        ):
                            deactivate_token.active = False
                LOGGER.debug("DEACTIVATED")
                LinkHelper.__display_specials_in_tokens(inline_blocks)
            return updated_index, True, token_to_append, consume_rest_of_line
        is_active = False
        return new_index, is_active, token_to_append, consume_rest_of_line

    # pylint: enable=too-many-arguments

    @staticmethod
    def __revert_token_to_normal_text_token(inline_blocks, search_index):
        """
        Revert this token from a special text token back to a normal text token.
        """

        LOGGER.debug("REVERTING")
        LinkHelper.__display_specials_in_tokens(inline_blocks)

        text_token_to_replace = inline_blocks[search_index]
        replacement_token = text_token_to_replace.create_copy()
        inline_blocks.insert(search_index, replacement_token)
        del inline_blocks[search_index + 1]

        LOGGER.debug("REVERTED")
        LinkHelper.__display_specials_in_tokens(inline_blocks)

    @staticmethod
    def __display_specials_in_tokens(inline_blocks):
        display_string = ""
        for deactivate_token in inline_blocks:
            if isinstance(deactivate_token, SpecialTextMarkdownToken):
                display_string += (
                    ",>>Spec:"
                    + str(deactivate_token.active)
                    + ":"
                    + str(deactivate_token)
                    + "<<"
                )
            else:
                display_string += "," + str(deactivate_token)
        LOGGER.debug(display_string[1:])

    @staticmethod
    def __consume_text_for_image_alt_text(
        inline_blocks, ind, remaining_line, text_from_blocks_raw, xx_fn
    ):
        """
        Consume text from the inline blocks to use as part of the image's alt text.
        """

        image_alt_text = ""
        LOGGER.debug("len(inline_blocks)>>%s<<", str(len(inline_blocks)))
        LOGGER.debug("ind>>%s<<", str(ind))
        LOGGER.debug(">>%s<<", str(inline_blocks[ind + 1 :]))
        if len(inline_blocks) > (ind + 1):
            while len(inline_blocks) > (ind + 1):
                if isinstance(inline_blocks[ind + 1], SpecialTextMarkdownToken):
                    if inline_blocks[ind + 1].token_text == "]":
                        image_alt_text += inline_blocks[ind + 1].token_text
                elif inline_blocks[ind + 1].token_name == MarkdownToken.token_text:
                    image_alt_text += inline_blocks[ind + 1].token_text
                elif (
                    inline_blocks[ind + 1].token_name
                    == MarkdownToken.token_inline_raw_html
                ):
                    image_alt_text += "<" + inline_blocks[ind + 1].raw_tag + ">"
                elif (
                    inline_blocks[ind + 1].token_name
                    == MarkdownToken.token_inline_code_span
                ):
                    image_alt_text += ParserHelper.resolve_references_from_text(
                        inline_blocks[ind + 1].span_text
                    )
                elif (
                    inline_blocks[ind + 1].token_name == MarkdownToken.token_inline_link
                ):
                    pass
                elif (
                    inline_blocks[ind + 1].token_name
                    == EndMarkdownToken.type_name_prefix
                    + MarkdownToken.token_inline_link
                ):
                    pass
                else:
                    assert (
                        inline_blocks[ind + 1].token_name
                        == MarkdownToken.token_inline_image
                    ), (
                        "Not handled: "
                        + ParserHelper.make_value_visible(inline_blocks[ind + 1])
                    )
                    image_alt_text += inline_blocks[ind + 1].image_alt_text

                LOGGER.debug(
                    ">>add>>%s<<%s", str(inline_blocks[ind + 1]), image_alt_text
                )

                del inline_blocks[ind + 1]
            LOGGER.debug(">>before>>%s>>", image_alt_text)
            image_alt_text = image_alt_text + remaining_line
            LOGGER.debug(">>after>>%s>>", image_alt_text)
        else:
            image_alt_text = xx_fn(text_from_blocks_raw)
            image_alt_text = ParserHelper.resolve_backspaces_from_text(image_alt_text)
        return image_alt_text, text_from_blocks_raw

    @staticmethod
    def __collect_text_from_blocks(inline_blocks, ind, suffix_text):
        """
        Aggregate the text component of text blocks.
        """

        LOGGER.debug(">>collect_text_from_blocks>>%s", str(inline_blocks))
        LOGGER.debug(">>collect_text_from_blocks>>suffix_text>>%s", str(suffix_text))
        collected_text = ""
        collected_text_raw = ""
        collect_index = ind + 1

        inline_link_end_name = (
            EndMarkdownToken.type_name_prefix + MarkdownToken.token_inline_link
        )

        is_inside_of_link = False
        while collect_index < len(inline_blocks):

            LOGGER.debug(
                ">>collect_text>>%s<<%s<<",
                inline_blocks[collect_index].token_name,
                str(inline_blocks[collect_index]),
            )

            if inline_blocks[collect_index].token_name == inline_link_end_name:
                is_inside_of_link = False
            elif (
                inline_blocks[collect_index].token_name
                == MarkdownToken.token_inline_link
            ):
                is_inside_of_link = True
                raw_text = LinkHelper.rehydrate_inline_link_text_from_token(
                    inline_blocks[collect_index]
                )
                collected_text_raw += raw_text
            elif (
                inline_blocks[collect_index].token_name
                == MarkdownToken.token_inline_image
            ):
                raw_text = LinkHelper.rehydrate_inline_image_text_from_token(
                    inline_blocks[collect_index]
                )
                collected_text_raw += raw_text
                collected_text += inline_blocks[collect_index].image_alt_text
            elif (
                inline_blocks[collect_index].token_name
                == MarkdownToken.token_inline_code_span
            ):
                converted_text = "`" + inline_blocks[collect_index].span_text + "`"
                collected_text += converted_text
                collected_text_raw += converted_text
            elif (
                inline_blocks[collect_index].token_name
                == MarkdownToken.token_inline_raw_html
            ):
                converted_text = "<" + inline_blocks[collect_index].raw_tag + ">"
                collected_text += converted_text
                collected_text_raw += converted_text
            elif not is_inside_of_link:
                collected_text += inline_blocks[collect_index].token_text
                collected_text_raw += inline_blocks[collect_index].token_text
            LOGGER.debug(
                ">>collect_text>>%s<<%s<<%s<<",
                collected_text,
                str(inline_blocks[collect_index]),
                inline_blocks[collect_index].token_text,
            )
            LOGGER.debug(
                ">>collected_text_raw>>%s<<", collected_text_raw,
            )
            collect_index += 1

        LOGGER.debug(
            ">>collect_text_from_blocks>>%s<<%s<<", collected_text, suffix_text
        )
        LOGGER.debug(">>collected_text_raw>>%s<<%s<<", collected_text_raw, suffix_text)
        collected_text += suffix_text
        collected_text_raw += suffix_text
        LOGGER.debug(">>collect_text_from_blocks>>%s<<", collected_text)
        LOGGER.debug(">>collected_text_raw>>%s<<", collected_text_raw)
        return collected_text, collected_text_raw

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
            LOGGER.debug(
                "collected_destination>>%s<<source_text<<%s>>nesting_level>>%s>>",
                str(collected_destination),
                source_text[new_index:],
                str(nesting_level),
            )
            keep_collecting = False
            new_index, before_part = ParserHelper.collect_until_one_of_characters(
                source_text, new_index, LinkHelper.__non_angle_link_breaks
            )
            collected_destination = collected_destination + before_part
            LOGGER.debug(">>>>>>%s<<<<<", source_text[new_index:])
            if ParserHelper.is_character_at_index(
                source_text, new_index, InlineHelper.backslash_character
            ):
                LOGGER.debug("backslash")
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
                LOGGER.debug("+1")
                nesting_level += 1
                collected_destination += LinkHelper.__non_angle_link_nest
                new_index += 1
                keep_collecting = True
            elif ParserHelper.is_character_at_index(
                source_text, new_index, LinkHelper.__non_angle_link_unnest
            ):
                LOGGER.debug("-1")
                if nesting_level != 0:
                    collected_destination += LinkHelper.__non_angle_link_unnest
                    new_index += 1
                    nesting_level -= 1
                    keep_collecting = True
        ex_link = collected_destination
        LOGGER.debug("collected_destination>>%s", str(collected_destination))
        if nesting_level != 0:
            return -1, None
        return new_index, ex_link

    @staticmethod
    def __parse_link_destination(source_text, new_index):
        """
        Parse an inline link's link destination.
        """

        LOGGER.debug("parse_link_destination>>new_index>>%s>>", source_text[new_index:])
        start_index = new_index
        did_use_angle_start = False
        if ParserHelper.is_character_at_index(
            source_text, new_index, LinkHelper.__angle_link_start
        ):
            LOGGER.debug(
                ">parse_angle_link_destination>new_index>%s>%s",
                str(new_index),
                str(source_text[new_index:]),
            )
            did_use_angle_start = True
            new_index, ex_link = LinkHelper.__parse_angle_link_destination(
                source_text, new_index
            )
            LOGGER.debug(
                ">parse_angle_link_destination>new_index>%s>ex_link>%s>",
                str(new_index),
                ex_link,
            )
        else:
            LOGGER.debug(
                ">parse_non_angle_link_destination>new_index>%s>%s",
                str(new_index),
                str(source_text[new_index:]),
            )
            new_index, ex_link = LinkHelper.__parse_non_angle_link_destination(
                source_text, new_index
            )
            LOGGER.debug(
                ">parse_non_angle_link_destination>new_index>%s>ex_link>%s>",
                str(new_index),
                str(ex_link),
            )
            if not ex_link:
                return None, None, -1, None, None

        if new_index != -1 and ParserHelper.newline_character in ex_link:
            return None, None, -1, None, None
        LOGGER.debug(
            "handle_backslashes>>new_index>>%s>>ex_link>>%s>>",
            str(new_index),
            str(ex_link),
        )

        pre_handle_link = ex_link
        if new_index != -1 and ex_link:
            ex_link = InlineHelper.handle_backslashes(ex_link, add_text_signature=False)
        LOGGER.debug(
            "urllib.parse.quote>>ex_link>>%s>>",
            ParserHelper.make_value_visible(ex_link),
        )

        ex_link = LinkHelper.__encode_link_destination(ex_link)
        LOGGER.debug(
            "parse_link_destination>>new_index>>%s>>ex_link>>%s>>",
            str(new_index),
            str(ex_link),
        )
        return (
            ex_link,
            pre_handle_link,
            new_index,
            source_text[start_index:new_index],
            did_use_angle_start,
        )

    @staticmethod
    def __parse_link_title(source_text, new_index):
        """
        Parse an inline link's link title.
        """

        LOGGER.debug("parse_link_title>>new_index>>%s>>", source_text[new_index:])
        ex_title = ""
        pre_ex_title = ""
        bounding_character = ""
        if ParserHelper.is_character_at_index(
            source_text, new_index, LinkHelper.__link_title_single
        ):
            bounding_character = LinkHelper.__link_title_single
            new_index, ex_title = InlineHelper.extract_bounded_string(
                source_text, new_index + 1, LinkHelper.__link_title_single, None
            )
        elif ParserHelper.is_character_at_index(
            source_text, new_index, LinkHelper.__link_title_double
        ):
            bounding_character = LinkHelper.__link_title_double
            new_index, ex_title = InlineHelper.extract_bounded_string(
                source_text, new_index + 1, LinkHelper.__link_title_double, None
            )
        elif ParserHelper.is_character_at_index(
            source_text, new_index, LinkHelper.__link_title_parenthesis_open
        ):
            bounding_character = LinkHelper.__link_title_parenthesis_open
            new_index, ex_title = InlineHelper.extract_bounded_string(
                source_text,
                new_index + 1,
                LinkHelper.__link_title_parenthesis_close,
                LinkHelper.__link_title_parenthesis_open,
            )
        else:
            new_index = -1
        LOGGER.debug(
            "parse_link_title>>new_index>>%s>>ex_link>>%s>>",
            str(new_index),
            str(ex_title),
        )
        pre_ex_title = ex_title
        if ex_title is not None:
            ex_title = InlineHelper.append_text(
                "",
                InlineHelper.handle_backslashes(ex_title, add_text_signature=False),
                add_text_signature=False,
            )
        LOGGER.debug("parse_link_title>>pre>>%s>>", str(pre_ex_title))
        LOGGER.debug("parse_link_title>>after>>%s>>", str(ex_title))

        return ex_title, pre_ex_title, new_index, bounding_character

    @staticmethod
    def __process_inline_link_body(source_text, new_index):
        """
        Given that an inline link has been identified, process it's body.
        """

        LOGGER.debug("process_inline_link_body>>%s<<", source_text[new_index:])
        inline_link = ""
        pre_inline_link = ""
        inline_title = ""
        pre_inline_title = ""
        did_use_angle_start = ""
        bounding_character = ""
        before_title_whitespace = ""
        after_title_whitespace = ""

        new_index, before_link_whitespace = ParserHelper.extract_any_whitespace(
            source_text, new_index
        )

        LOGGER.debug(
            "new_index>>%s>>source_text[]>>%s>", str(new_index), source_text[new_index:]
        )
        if not ParserHelper.is_character_at_index(
            source_text, new_index, LinkHelper.__link_format_inline_end
        ):
            LOGGER.debug(">>search for link destination")
            (
                inline_link,
                pre_inline_link,
                new_index,
                _,
                did_use_angle_start,
            ) = LinkHelper.__parse_link_destination(source_text, new_index)
            LOGGER.debug(
                ">>link destination>>%s>>%s>>",
                ParserHelper.make_value_visible(source_text),
                str(new_index),
            )
            if new_index != -1:
                LOGGER.debug(
                    "before ws>>%s<",
                    ParserHelper.make_value_visible(source_text[new_index:]),
                )
                (
                    new_index,
                    before_title_whitespace,
                ) = ParserHelper.extract_any_whitespace(source_text, new_index)
                LOGGER.debug(
                    "after ws>>%s>",
                    ParserHelper.make_value_visible(source_text[new_index:]),
                )
                if ParserHelper.is_character_at_index_not(
                    source_text, new_index, LinkHelper.__link_format_inline_end
                ):
                    (
                        inline_title,
                        pre_inline_title,
                        new_index,
                        bounding_character,
                    ) = LinkHelper.__parse_link_title(source_text, new_index)
                if new_index != -1:
                    (
                        new_index,
                        after_title_whitespace,
                    ) = ParserHelper.extract_any_whitespace(source_text, new_index)
        LOGGER.debug(
            "inline_link>>%s>>inline_title>>%s>new_index>%s>",
            str(inline_link),
            str(inline_title),
            str(new_index),
        )
        if new_index != -1:
            if ParserHelper.is_character_at_index(
                source_text, new_index, LinkHelper.__link_format_inline_end
            ):
                new_index += 1
            else:
                new_index = -1
        LOGGER.debug(
            "process_inline_link_body>>inline_link>>%s>>inline_title>>%s>new_index>%s>",
            str(inline_link),
            str(inline_title),
            str(new_index),
        )
        return (
            inline_link,
            pre_inline_link,
            inline_title,
            pre_inline_title,
            new_index,
            did_use_angle_start,
            bounding_character,
            before_link_whitespace,
            before_title_whitespace,
            after_title_whitespace,
        )

    @staticmethod
    def __look_up_link(link_to_lookup, new_index, link_type):
        """
        Look up a link to see if it is present.
        """

        inline_link = ""
        inline_title = ""

        link_to_lookup = ParserHelper.resolve_backspaces_from_text(link_to_lookup)
        link_to_lookup = ParserHelper.resolve_replacement_markers_from_text(
            link_to_lookup
        )
        link_to_lookup = ParserHelper.remove_escapes_from_text(link_to_lookup)

        link_label = LinkHelper.normalize_link_label(link_to_lookup)
        if not link_label or link_label not in LinkHelper.__link_definitions:
            update_index = -1
        else:
            LOGGER.debug(link_type)
            update_index = new_index
            inline_link = LinkHelper.__link_definitions[link_label][0]
            inline_title = LinkHelper.__link_definitions[link_label][1]
        return update_index, inline_link, inline_title

    # pylint: disable=too-many-arguments, too-many-locals
    @staticmethod
    def __handle_link_types(
        inline_blocks,
        ind,
        source_text,
        new_index,
        start_text,
        remaining_line,
        current_string_unresolved,
        xx_fn,
    ):
        """
        After finding a link specifier, figure out what type of link it is.
        """

        LOGGER.debug(
            "handle_link_types>>%s<<%s<<%s",
            str(inline_blocks),
            str(ind),
            str(len(inline_blocks)),
        )
        LOGGER.debug(
            "handle_link_types>source_text>>%s<<",
            ParserHelper.make_value_visible(source_text),
        )
        LOGGER.debug("handle_link_types>>%s<<", source_text[new_index:])
        LOGGER.debug(
            "handle_link_types>>current_string_unresolved>>%s<<remaining_line<<%s>>",
            ParserHelper.make_value_visible(current_string_unresolved),
            ParserHelper.make_value_visible(remaining_line),
        )
        text_from_blocks, text_from_blocks_raw = LinkHelper.__collect_text_from_blocks(
            inline_blocks, ind, current_string_unresolved + remaining_line
        )
        LOGGER.debug(
            "handle_link_types>>text_from_blocks>>%s<<%s<<",
            str(len(text_from_blocks)),
            ParserHelper.make_value_visible(text_from_blocks),
        )
        LOGGER.debug(
            "handle_link_types>>text_from_blocks_raw>>%s<<%s<<",
            str(len(text_from_blocks_raw)),
            ParserHelper.make_value_visible(text_from_blocks_raw),
        )
        LOGGER.debug(
            "handle_link_types>>text_from_blocks>>%s<<",
            ParserHelper.make_value_visible(text_from_blocks),
        )
        text_from_blocks = ParserHelper.resolve_backspaces_from_text(text_from_blocks)
        LOGGER.debug(
            "handle_link_types>>text_from_blocks>>%s<<",
            ParserHelper.make_value_visible(text_from_blocks),
        )

        consume_rest_of_line = False

        LOGGER.debug("__look_for_link_formats>>%s>>", str(new_index))
        (
            inline_link,
            pre_inline_link,
            inline_title,
            pre_inline_title,
            update_index,
            tried_full_reference_form,
            ex_label,
            label_type,
            did_use_angle_start,
            inline_title_bounding_character,
            before_link_whitespace,
            before_title_whitespace,
            after_title_whitespace,
        ) = LinkHelper.__look_for_link_formats(source_text, new_index, text_from_blocks)
        LOGGER.debug("__look_for_link_formats>>update_index>>%s>>", str(update_index))

        # u != -1 - inline valid
        # tried_full_reference_form - collapsed or full valid
        if update_index == -1 and not tried_full_reference_form:
            ex_label = ""
            LOGGER.debug("shortcut?")
            LOGGER.debug(
                ">>%s<<", ParserHelper.make_value_visible(inline_blocks),
            )
            LOGGER.debug(
                ">>%s<<", ParserHelper.make_value_visible(text_from_blocks),
            )

            update_index, inline_link, inline_title = LinkHelper.__look_up_link(
                text_from_blocks, new_index, "shortcut"
            )
            label_type = "shortcut"
            pre_inline_link = ""

        token_to_append = None
        LOGGER.debug("<<<<<<<new_index<<<<<<<%s<<", str(new_index))
        LOGGER.debug("<<<<<<<update_index<<<<<<<%s<<", str(update_index))
        if update_index != -1:
            consume_rest_of_line, token_to_append = LinkHelper.__create_link_token(
                start_text,
                inline_link,
                pre_inline_link,
                inline_title,
                pre_inline_title,
                text_from_blocks,
                text_from_blocks_raw,
                inline_blocks,
                ind,
                did_use_angle_start,
                inline_title_bounding_character,
                before_link_whitespace,
                before_title_whitespace,
                after_title_whitespace,
                ex_label,
                label_type,
                remaining_line,
                current_string_unresolved,
                xx_fn,
            )

        LOGGER.debug(
            "handle_link_types<update_index<%s<<%s<<",
            str(update_index),
            str(token_to_append),
        )
        return update_index, token_to_append, consume_rest_of_line

    # pylint: enable=too-many-arguments, too-many-locals

    # pylint: disable=too-many-arguments, too-many-locals
    @staticmethod
    def __create_link_token(
        start_text,
        inline_link,
        pre_inline_link,
        inline_title,
        pre_inline_title,
        text_from_blocks,
        text_from_blocks_raw,
        inline_blocks,
        ind,
        did_use_angle_start,
        inline_title_bounding_character,
        before_link_whitespace,
        before_title_whitespace,
        after_title_whitespace,
        ex_label,
        label_type,
        remaining_line,
        current_string_unresolved,
        xx_fn,
    ):
        """
        Create the right type of link token.
        """
        consume_rest_of_line = False
        token_to_append = None

        LOGGER.debug("<<<<<<<start_text<<<<<<<%s<<", str(start_text))
        LOGGER.debug(">>inline_link>>%s>>", inline_link)
        LOGGER.debug(">>pre_inline_link>>%s>>", pre_inline_link)
        LOGGER.debug(">>inline_title>>%s>>", inline_title)
        LOGGER.debug(">>pre_inline_title>>%s>>", pre_inline_title)
        LOGGER.debug(">>text_from_blocks>>%s>>", text_from_blocks)
        if pre_inline_link == inline_link:
            pre_inline_link = ""
        if pre_inline_title == inline_title:
            pre_inline_title = ""
        LOGGER.debug(">>pre_inline_link>>%s>>", pre_inline_link)

        text_from_blocks_raw = ParserHelper.resolve_backspaces_from_text(
            text_from_blocks_raw
        )
        LOGGER.debug(">>text_from_blocks_raw>>%s>>", text_from_blocks_raw)
        LOGGER.debug(">>inline_blocks[ind]>>%s>>", inline_blocks[ind])

        line_number = inline_blocks[ind].line_number
        column_number = inline_blocks[ind].column_number
        if start_text == LinkHelper.__link_start_sequence:
            inline_blocks[ind] = LinkStartMarkdownToken(
                inline_link,
                pre_inline_link,
                inline_title,
                pre_inline_title,
                ex_label,
                label_type,
                text_from_blocks_raw,
                did_use_angle_start,
                inline_title_bounding_character,
                before_link_whitespace,
                before_title_whitespace,
                after_title_whitespace,
                line_number,
                column_number,
            )
            token_to_append = EndMarkdownToken(
                MarkdownToken.token_inline_link, "", "", inline_blocks[ind], False
            )
        else:
            assert start_text == LinkHelper.image_start_sequence
            consume_rest_of_line = True
            LOGGER.debug(
                "\n>>__consume_text_for_image_alt_text>>%s>>", str(inline_blocks)
            )
            LOGGER.debug("\n>>__consume_text_for_image_alt_text>>%s>>", str(ind))
            LOGGER.debug(
                "\n>>__consume_text_for_image_alt_text>>%s>>", str(remaining_line)
            )
            (
                image_alt_text,
                text_from_blocks_raw,
            ) = LinkHelper.__consume_text_for_image_alt_text(
                inline_blocks, ind, remaining_line, text_from_blocks_raw, xx_fn
            )
            LOGGER.debug(
                "\n>>__consume_text_for_image_alt_text>>%s>>", str(image_alt_text)
            )

            inline_blocks[ind] = ImageStartMarkdownToken(
                inline_link,
                pre_inline_link,
                inline_title,
                pre_inline_title,
                image_alt_text,
                ex_label,
                label_type,
                text_from_blocks_raw,
                did_use_angle_start,
                inline_title_bounding_character,
                before_link_whitespace,
                before_title_whitespace,
                after_title_whitespace,
                line_number,
                column_number,
            )
            LOGGER.debug("\n>>Image>>%s", str(inline_blocks))
            LOGGER.debug(">>start_text>>%s<<", str(start_text))
            LOGGER.debug(">>remaining_line>>%s<<", str(remaining_line))
            LOGGER.debug(
                ">>current_string_unresolved>>%s<<", str(current_string_unresolved)
            )
        return consume_rest_of_line, token_to_append

    # pylint: enable=too-many-arguments, too-many-locals

    # pylint: disable=too-many-locals
    @staticmethod
    def __look_for_link_formats(source_text, new_index, text_from_blocks):
        """
        Look for links in the various formats.
        """
        inline_link = ""
        pre_inline_link = ""
        inline_title = ""
        pre_inline_title = ""
        update_index = -1
        ex_label = ""
        label_type = ""
        did_use_angle_start = ""
        bounding_character = ""
        before_link_whitespace = ""
        before_title_whitespace = ""
        after_title_whitespace = ""
        tried_full_reference_form = False
        if ParserHelper.is_character_at_index(
            source_text, new_index, LinkHelper.__link_format_inline_start
        ):
            LOGGER.debug("inline reference? >>%s>>", str(new_index))
            (
                inline_link,
                pre_inline_link,
                inline_title,
                pre_inline_title,
                update_index,
                did_use_angle_start,
                bounding_character,
                before_link_whitespace,
                before_title_whitespace,
                after_title_whitespace,
            ) = LinkHelper.__process_inline_link_body(source_text, new_index + 1)
            label_type = "inline"
        elif ParserHelper.is_character_at_index(
            source_text, new_index, LinkHelper.__link_format_reference_start
        ):
            LOGGER.debug("collapsed reference?")
            after_open_index = new_index + 1
            if ParserHelper.is_character_at_index(
                source_text, after_open_index, LinkHelper.__link_format_reference_end
            ):
                LOGGER.debug("collapsed reference")
                LOGGER.debug(
                    ">>%s>>", ParserHelper.make_value_visible(text_from_blocks)
                )
                update_index, inline_link, inline_title = LinkHelper.__look_up_link(
                    text_from_blocks, after_open_index + 1, "collapsed reference",
                )
                LOGGER.debug("collapsed reference>update_index>%s", str(update_index))
                tried_full_reference_form = True
                label_type = "collapsed"
            else:
                LOGGER.debug("full reference?")
                LOGGER.debug(">>did_extract>>%s>", source_text[after_open_index:])
                (
                    did_extract,
                    after_label_index,
                    ex_label,
                ) = LinkHelper.extract_link_label(
                    source_text, after_open_index, include_reference_colon=False
                )
                LOGGER.debug(
                    ">>did_extract>>%s>after_label_index>%s>ex_label>%s>",
                    str(did_extract),
                    str(after_label_index),
                    str(ex_label),
                )
                if did_extract:
                    tried_full_reference_form = True
                    label_type = "full"
                    update_index, inline_link, inline_title = LinkHelper.__look_up_link(
                        ex_label, after_label_index, "full reference"
                    )
        return (
            inline_link,
            pre_inline_link,
            inline_title,
            pre_inline_title,
            update_index,
            tried_full_reference_form,
            ex_label,
            label_type,
            did_use_angle_start,
            bounding_character,
            before_link_whitespace,
            before_title_whitespace,
            after_title_whitespace,
        )

    # pylint: enable=too-many-locals

    @staticmethod
    def __encode_link_destination(link_to_encode):

        encoded_link = ""
        percent_index, before_data = ParserHelper.collect_until_one_of_characters(
            link_to_encode, 0, LinkHelper.__special_link_destination_characters
        )
        encoded_link += urllib.parse.quote(
            before_data, safe=LinkHelper.__link_safe_characters
        )
        while percent_index < len(link_to_encode):
            special_character = link_to_encode[percent_index]
            percent_index += 1
            if special_character == "%":
                hex_guess_characters = link_to_encode[percent_index : percent_index + 2]
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

            percent_index, before_data = ParserHelper.collect_until_one_of_characters(
                link_to_encode,
                percent_index,
                LinkHelper.__special_link_destination_characters,
            )
            encoded_link += urllib.parse.quote(
                before_data, safe=LinkHelper.__link_safe_characters
            )
        return encoded_link

    @staticmethod
    def rehydrate_inline_image_text_from_token(image_token):
        """
        Given an image token, rehydrate it's original text from the token.
        """

        if image_token.pre_image_uri:
            image_uri = image_token.pre_image_uri
        else:
            image_uri = image_token.image_uri

        if image_token.pre_image_title:
            image_title = image_token.pre_image_title
        else:
            image_title = image_token.image_title

        image_text = ""
        if image_token.label_type == "inline":
            if image_token.did_use_angle_start:
                image_uri = "<" + image_uri + ">"

            link_text = ParserHelper.remove_backspaces_from_text(
                image_token.text_from_blocks
            )
            image_text = (
                "!["
                + link_text
                + "]("
                + image_token.before_link_whitespace
                + image_uri
                + image_token.before_title_whitespace
            )
            if image_title:
                title_prefix = '"'
                title_suffix = '"'
                if image_token.inline_title_bounding_character == "'":
                    title_prefix = "'"
                    title_suffix = "'"
                elif image_token.inline_title_bounding_character == "(":
                    title_prefix = "("
                    title_suffix = ")"

                image_text += (
                    title_prefix
                    + image_title
                    + title_suffix
                    + image_token.after_title_whitespace
                )
            image_text += ")"
        elif image_token.label_type == "shortcut":
            link_text = ParserHelper.remove_backspaces_from_text(
                image_token.text_from_blocks
            )
            image_text = "![" + link_text + "]"
        elif image_token.label_type == "full":
            image_text = (
                "![" + image_token.text_from_blocks + "][" + image_token.ex_label + "]"
            )
        else:
            assert image_token.label_type == "collapsed"
            image_text = "![" + image_token.text_from_blocks + "][]"

        return image_text

    # pylint: disable=too-many-branches
    @staticmethod
    def rehydrate_inline_link_text_from_token(link_token):
        """
        Given a link token, rehydrate it's original text from the token.
        """

        link_text = ""
        if link_token.label_type == "shortcut":
            link_label = ParserHelper.remove_backspaces_from_text(
                link_token.text_from_blocks
            )
            link_label = ParserHelper.remove_escapes_from_text(link_label)
            link_text = "[" + link_label + "]"
        elif link_token.label_type == "full":

            link_text = (
                "[" + link_token.text_from_blocks + "][" + link_token.ex_label + "]"
            )

        elif link_token.label_type == "collapsed":

            link_text = "[" + link_token.text_from_blocks + "][]"
        else:
            assert link_token.label_type == "inline"

            if link_token.pre_link_uri:
                link_uri = link_token.pre_link_uri
            else:
                link_uri = link_token.link_uri
            if link_token.did_use_angle_start:
                link_uri = "<" + link_uri + ">"

            link_label = ParserHelper.remove_backspaces_from_text(
                link_token.text_from_blocks
            )
            link_label = ParserHelper.remove_escapes_from_text(link_label)
            link_text = (
                "[" + link_label + "](" + link_token.before_link_whitespace + link_uri
            )
            if link_token.link_title:
                title_prefix = '"'
                title_suffix = '"'
                if link_token.inline_title_bounding_character == "'":
                    title_prefix = "'"
                    title_suffix = "'"
                elif link_token.inline_title_bounding_character == "(":
                    title_prefix = "("
                    title_suffix = ")"

                if link_token.pre_link_title:
                    link_title = link_token.pre_link_title
                else:
                    link_title = link_token.link_title

                link_text += (
                    link_token.before_title_whitespace
                    + title_prefix
                    + link_title
                    + title_suffix
                    + link_token.after_title_whitespace
                )
            else:
                link_text += link_token.before_title_whitespace
            link_text += ")"
        return link_text

    # pylint: enable=too-many-branches
