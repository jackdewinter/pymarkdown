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
    TextMarkdownToken,
)
from pymarkdown.parser_helper import ParserHelper

LOGGER = logging.getLogger(__name__)


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
            ex_ws.replace("\n", "\\n"),
        )
        start_index = new_index
        if new_index == len(line_to_parse) and not is_blank_line:
            return False, new_index, None, None, None, None
        if ex_ws and new_index < len(line_to_parse):
            inline_title, pre_inline_title, new_index = LinkHelper.__parse_link_title(
                line_to_parse, new_index
            )
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
    ):
        """
        Given that a link close character has been found, process it to see if
        there is actually enough other text to properly construct the link.
        """

        LOGGER.debug(">>look_for_link_or_image>>%s<<", str(inline_blocks))
        is_valid = False
        consume_rest_of_line = False
        new_index = next_index + 1
        updated_index = -1
        token_to_append = None

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
                        )
                        if updated_index != -1:
                            is_valid = True
                        else:
                            inline_blocks[search_index].active = False
                        break
                    LOGGER.debug("  not active")
                else:
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
            return updated_index, True, token_to_append, consume_rest_of_line
        is_active = False
        return new_index, is_active, token_to_append, consume_rest_of_line

    # pylint: enable=too-many-arguments

    @staticmethod
    def __consume_text_for_image_alt_text(inline_blocks, ind, remaining_line):
        """
        Consume text from the inline blocks to use as part of the image's alt text.
        """

        image_alt_text = ""
        LOGGER.debug(">>%s<<", str(inline_blocks[ind + 1 :]))
        while len(inline_blocks) > (ind + 1):
            if isinstance(inline_blocks[ind + 1], SpecialTextMarkdownToken):
                pass
            elif isinstance(inline_blocks[ind + 1], TextMarkdownToken):
                image_alt_text = image_alt_text + inline_blocks[ind + 1].token_text
            elif isinstance(inline_blocks[ind + 1], ImageStartMarkdownToken):
                image_alt_text = image_alt_text + inline_blocks[ind + 1].image_alt_text

            LOGGER.debug(">>add>>%s<<%s", str(inline_blocks[ind + 1]), image_alt_text)

            del inline_blocks[ind + 1]

        LOGGER.debug(">>before>>%s>>", image_alt_text)
        image_alt_text = image_alt_text + remaining_line
        LOGGER.debug(">>after>>%s>>", image_alt_text)
        return image_alt_text

    @staticmethod
    def __collect_text_from_blocks(inline_blocks, ind, suffix_text):
        """
        Aggregate the text component of text blocks.
        """

        LOGGER.debug(">>collect_text_from_blocks>>%s", str(inline_blocks))
        LOGGER.debug(">>collect_text_from_blocks>>suffix_text>>%s", str(suffix_text))
        collected_text = ""
        collect_index = ind + 1

        inline_link_end_name = (
            EndMarkdownToken.type_name_prefix + MarkdownToken.token_inline_link
        )

        while collect_index < len(inline_blocks):

            if (
                inline_blocks[collect_index].token_name
                == MarkdownToken.token_inline_link
                or inline_blocks[collect_index].token_name == inline_link_end_name
            ):
                pass
            elif (
                inline_blocks[collect_index].token_name
                == MarkdownToken.token_inline_image
            ):
                collected_text = (
                    collected_text + inline_blocks[collect_index].image_alt_text
                )
            elif (
                inline_blocks[collect_index].token_name
                == MarkdownToken.token_inline_code_span
            ):
                collected_text = collected_text + inline_blocks[collect_index].span_text
            else:
                collected_text = (
                    collected_text + inline_blocks[collect_index].token_text
                )
            LOGGER.debug(
                ">>collect_text>>%s<<%s<<%s<<",
                collected_text,
                str(inline_blocks[collect_index]),
                inline_blocks[collect_index].token_text,
            )
            collect_index += 1
        collected_text = collected_text + suffix_text
        LOGGER.debug(">>collect_text_from_blocks>>%s<<", collected_text)
        return collected_text

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
        if ParserHelper.is_character_at_index(
            source_text, new_index, LinkHelper.__angle_link_start
        ):
            LOGGER.debug(
                ">parse_angle_link_destination>new_index>%s>%s",
                str(new_index),
                str(source_text[new_index:]),
            )
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
                return None, None, -1, None

        if new_index != -1 and "\n" in ex_link:
            return None, None, -1, None
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
            str(ex_link).replace(InlineHelper.backspace_character, "\\b"),
        )

        ex_link = LinkHelper.__encode_link_destination(ex_link)
        LOGGER.debug(
            "parse_link_destination>>new_index>>%s>>ex_link>>%s>>",
            str(new_index),
            str(ex_link),
        )
        return ex_link, pre_handle_link, new_index, source_text[start_index:new_index]

    @staticmethod
    def __parse_link_title(source_text, new_index):
        """
        Parse an inline link's link title.
        """

        LOGGER.debug("parse_link_title>>new_index>>%s>>", source_text[new_index:])
        ex_title = ""
        pre_ex_title = ""
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

        return ex_title, pre_ex_title, new_index

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
        new_index, _ = ParserHelper.extract_any_whitespace(source_text, new_index)
        LOGGER.debug(
            "new_index>>%s>>source_text[]>>%s>", str(new_index), source_text[new_index:]
        )
        if not ParserHelper.is_character_at_index(
            source_text, new_index, LinkHelper.__link_format_inline_end
        ):
            (
                inline_link,
                pre_inline_link,
                new_index,
                _,
            ) = LinkHelper.__parse_link_destination(source_text, new_index)
            if new_index != -1:
                LOGGER.debug("before ws>>%s<", source_text[new_index:])
                new_index, _ = ParserHelper.extract_any_whitespace(
                    source_text, new_index
                )
                LOGGER.debug("after ws>>%s>", source_text[new_index:])
                if ParserHelper.is_character_at_index_not(
                    source_text, new_index, LinkHelper.__link_format_inline_end
                ):
                    (
                        inline_title,
                        pre_inline_title,
                        new_index,
                    ) = LinkHelper.__parse_link_title(source_text, new_index)
                if new_index != -1:
                    new_index, _ = ParserHelper.extract_any_whitespace(
                        source_text, new_index
                    )
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
        return inline_link, pre_inline_link, inline_title, pre_inline_title, new_index

    @staticmethod
    def resolve_backspaces_from_text(token_text):
        """
        Deal with any backslash encoding in text with backspaces.
        """
        adjusted_text_token = token_text
        while InlineHelper.backspace_character in adjusted_text_token:
            next_backspace_index = adjusted_text_token.index(
                InlineHelper.backspace_character
            )
            adjusted_text_token = (
                adjusted_text_token[0 : next_backspace_index - 1]
                + adjusted_text_token[next_backspace_index + 1 :]
            )
        return adjusted_text_token

    @staticmethod
    def __look_up_link(link_to_lookup, new_index, link_type):
        """
        Look up a link to see if it is present.
        """

        inline_link = ""
        inline_title = ""

        link_to_lookup = LinkHelper.resolve_backspaces_from_text(link_to_lookup)

        link_label = LinkHelper.normalize_link_label(link_to_lookup)
        if not link_label or link_label not in LinkHelper.__link_definitions:
            update_index = -1
        else:
            LOGGER.debug(link_type)
            update_index = new_index
            inline_link = LinkHelper.__link_definitions[link_label][0]
            inline_title = LinkHelper.__link_definitions[link_label][1]
        return update_index, inline_link, inline_title

    # pylint: disable=too-many-arguments
    # pylint: disable=too-many-locals
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

        LOGGER.debug(
            "handle_link_types>>%s<<%s<<%s",
            str(inline_blocks),
            str(ind),
            str(len(inline_blocks)),
        )
        LOGGER.debug("handle_link_types>>%s<<", source_text[new_index:])
        LOGGER.debug(
            "handle_link_types>>current_string_unresolved>>%s<<remaining_line<<%s>>",
            str(current_string_unresolved),
            str(remaining_line),
        )
        text_from_blocks = LinkHelper.__collect_text_from_blocks(
            inline_blocks, ind, current_string_unresolved + remaining_line
        )
        LOGGER.debug("handle_link_types>>text_from_blocks>>%s<<", text_from_blocks)

        consume_rest_of_line = False

        (
            inline_link,
            pre_inline_link,
            inline_title,
            pre_inline_title,
            update_index,
            tried_full_reference_form,
            ex_label,
            label_type,
        ) = LinkHelper.__look_for_link_formats(source_text, new_index, text_from_blocks)

        if update_index == -1 and not tried_full_reference_form:
            ex_label = ""
            LOGGER.debug("shortcut?")
            LOGGER.debug(
                ">>%s<<",
                str(inline_blocks).replace(InlineHelper.backspace_character, "\\b"),
            )
            LOGGER.debug(
                ">>%s<<",
                str(text_from_blocks).replace(InlineHelper.backspace_character, "\\b"),
            )

            update_index, inline_link, inline_title = LinkHelper.__look_up_link(
                text_from_blocks, new_index, "shortcut"
            )
            label_type = "shortcut"
            pre_inline_link = ""

        token_to_append = None
        if update_index != -1:
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
            if start_text == LinkHelper.__link_start_sequence:
                inline_blocks[ind] = LinkStartMarkdownToken(
                    inline_link,
                    pre_inline_link,
                    inline_title,
                    pre_inline_title,
                    ex_label,
                    label_type,
                    text_from_blocks,
                )
                token_to_append = EndMarkdownToken(
                    MarkdownToken.token_inline_link, "", "", None
                )
            else:
                assert start_text == LinkHelper.image_start_sequence
                consume_rest_of_line = True
                image_alt_text = LinkHelper.__consume_text_for_image_alt_text(
                    inline_blocks, ind, remaining_line
                )

                inline_blocks[ind] = ImageStartMarkdownToken(
                    inline_link,
                    pre_inline_link,
                    inline_title,
                    pre_inline_title,
                    image_alt_text,
                    ex_label,
                    label_type,
                    text_from_blocks,
                )
                LOGGER.debug("\n>>Image>>%s", str(inline_blocks))
                LOGGER.debug(">>start_text>>%s<<", str(start_text))
                LOGGER.debug(">>remaining_line>>%s<<", str(remaining_line))
                LOGGER.debug(
                    ">>current_string_unresolved>>%s<<", str(current_string_unresolved)
                )
                # assert False

        LOGGER.debug(
            "handle_link_types<update_index<%s<<%s<<",
            str(update_index),
            str(token_to_append),
        )
        return update_index, token_to_append, consume_rest_of_line

    # pylint: enable=too-many-arguments
    # pylint: enable=too-many-locals

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
        tried_full_reference_form = False
        if ParserHelper.is_character_at_index(
            source_text, new_index, LinkHelper.__link_format_inline_start
        ):
            LOGGER.debug("inline reference?")
            (
                inline_link,
                pre_inline_link,
                inline_title,
                pre_inline_title,
                update_index,
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
                LOGGER.debug(">>%s>>", text_from_blocks)
                update_index, inline_link, inline_title = LinkHelper.__look_up_link(
                    text_from_blocks, after_open_index + 1, "collapsed reference",
                )
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
        )

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
