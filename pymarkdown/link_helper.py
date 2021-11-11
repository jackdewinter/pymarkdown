"""
Link helper
"""
import logging
import urllib
import urllib.parse

from pymarkdown.constants import Constants
from pymarkdown.emphasis_helper import EmphasisHelper
from pymarkdown.inline_helper import InlineHelper, InlineRequest
from pymarkdown.inline_markdown_token import (
    ImageStartMarkdownToken,
    LinkStartMarkdownToken,
)
from pymarkdown.parser_helper import ParserHelper
from pymarkdown.parser_logger import ParserLogger

POGGER = ParserLogger(logging.getLogger(__name__))


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
    __non_angle_link_breaks = f"{Constants.ascii_control_characters}()\\"

    link_label_start = "["
    link_label_end = "]"
    __link_label_is_definition_character = ":"
    __link_label_breaks = (
        f"{link_label_start}{link_label_end}{InlineHelper.backslash_character}"
    )

    __angle_link_start = "<"
    __angle_link_end = ">"
    __angle_link_destination_breaks = (
        f"{__angle_link_end}{InlineHelper.backslash_character}"
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
        POGGER.debug(
            ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>$",
            LinkHelper.__link_definitions,
        )
        POGGER.debug(
            ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>$:$",
            link_name,
            link_value,
        )
        did_add_definition = link_name not in LinkHelper.__link_definitions
        if did_add_definition:
            LinkHelper.__link_definitions[link_name] = link_value
            POGGER.debug(">>added def>>$-->$", link_name, link_value)
        return did_add_definition

    @staticmethod
    def extract_link_label(line_to_parse, new_index, include_reference_colon=True):
        """
        Extract the link reference definition's link label.
        """
        label_parts, keep_collecting = [], True

        while keep_collecting:
            keep_collecting = False
            new_index, ert_new = ParserHelper.collect_until_one_of_characters(
                line_to_parse, new_index, LinkHelper.__link_label_breaks
            )
            label_parts.append(ert_new)
            if ParserHelper.is_character_at_index(
                line_to_parse, new_index, InlineHelper.backslash_character
            ):
                old_new_index = new_index
                inline_request = InlineRequest(line_to_parse, new_index)
                inline_response = InlineHelper.handle_inline_backslash(inline_request)
                new_index = inline_response.new_index
                label_parts.append(line_to_parse[old_new_index:new_index])
                keep_collecting = True
            elif ParserHelper.is_character_at_index(
                line_to_parse, new_index, LinkHelper.link_label_start
            ):
                POGGER.debug(">> unescaped [, bailing")
                return False, -1, None

        POGGER.debug("look for ]>>$<<", line_to_parse[new_index:])
        if not ParserHelper.is_character_at_index(
            line_to_parse, new_index, LinkHelper.link_label_end
        ):
            POGGER.debug(">> no end ], bailing")
            return False, new_index, None
        new_index += 1

        if include_reference_colon:
            POGGER.debug(
                "look for :>>$<<",
                line_to_parse[new_index:],
            )
            if not ParserHelper.is_character_at_index(
                line_to_parse,
                new_index,
                LinkHelper.__link_label_is_definition_character,
            ):
                POGGER.debug(">> no :, bailing")
                return False, -1, None
            new_index += 1

        return True, new_index, "".join(label_parts)

    @staticmethod
    def extract_link_title(line_to_parse, new_index, is_blank_line):
        """
        Extract the link reference definition's optional link title.
        """
        inline_title, pre_inline_title = "", ""
        POGGER.debug("before ws>>$>", line_to_parse[new_index:])
        new_index, ex_ws = ParserHelper.extract_any_whitespace(line_to_parse, new_index)
        POGGER.debug(
            "after ws>>$>ex_ws>$",
            line_to_parse[new_index:],
            ex_ws,
        )
        start_index, line_to_parse_size = new_index, len(line_to_parse)
        if new_index == line_to_parse_size and not is_blank_line:
            return False, new_index, None, None, None, None
        if ex_ws and new_index < line_to_parse_size:
            (
                inline_title,
                pre_inline_title,
                new_index,
                _,
            ) = LinkHelper.__parse_link_title(line_to_parse, new_index)
            if new_index == -1 or inline_title is None:
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

        POGGER.debug("LD>>$<<", line_to_parse[new_index:])
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
            link_label, Constants.non_space_whitespace, ParserHelper.space_character
        )

        # Fold multiple spaces into a single space character.
        link_label = ParserHelper.space_character.join(link_label.split())

        # Fold the case of any characters to their lower equivalent.
        return link_label.casefold().strip()

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

        POGGER.debug(
            ">>look_for_link_or_image>>$<<",
            inline_blocks,
        )
        POGGER.debug(">>source_text>>$<<", source_text)
        POGGER.debug(">>next_index>>$<<", next_index)
        POGGER.debug(">>remaining_line>>$<<", remaining_line)
        POGGER.debug(
            ">>current_string_unresolved>>$<<",
            current_string_unresolved,
        )
        is_valid, consume_rest_of_line, new_index, updated_index, token_to_append = (
            False,
            False,
            next_index + 1,
            -1,
            None,
        )

        POGGER.debug("LOOKING FOR START")
        LinkHelper.__display_specials_in_tokens(inline_blocks)

        valid_special_start_text, search_index = None, len(inline_blocks) - 1
        while search_index >= 0:
            if inline_blocks[search_index].is_special_text:
                if POGGER.is_debug_enabled:
                    POGGER.debug(
                        "search_index>>$>>$",
                        search_index,
                        inline_blocks[search_index].show_process_emphasis(),
                    )
                if (
                    inline_blocks[search_index].token_text
                    in LinkHelper.__valid_link_starts
                ):
                    valid_special_start_text = inline_blocks[search_index].token_text
                    if inline_blocks[search_index].is_active:
                        POGGER.debug(">>>>>>$", inline_blocks)
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

                    POGGER.debug("  not active:$", search_index)
                    LinkHelper.__revert_token_to_normal_text_token(
                        inline_blocks, search_index
                    )
                    break
                POGGER.debug("  not link")
            search_index -= 1

        POGGER.debug(
            ">>look_for_link_or_image>>$<<is_valid<<$<<$<<",
            inline_blocks,
            is_valid,
            consume_rest_of_line,
        )
        if is_valid:
            # if link set all [ before to inactive
            POGGER.debug("")
            POGGER.debug("SET TO INACTIVE-->$", valid_special_start_text)
            POGGER.debug("ind-->$", search_index)

            assert (
                inline_blocks[search_index].is_inline_link
                or inline_blocks[search_index].is_inline_image
            )

            POGGER.debug(
                "\nresolve_inline_emphasis>>$",
                inline_blocks,
            )
            EmphasisHelper.resolve_inline_emphasis(
                inline_blocks, inline_blocks[search_index]
            )
            POGGER.debug(
                "resolve_inline_emphasis>>$\n",
                inline_blocks,
            )

            if valid_special_start_text == LinkHelper.__link_start_sequence:
                POGGER.debug("DEACTIVATING")
                LinkHelper.__display_specials_in_tokens(inline_blocks)
                for deactivate_token in inline_blocks:
                    if deactivate_token.is_special_text:
                        POGGER.debug(
                            "inline_blocks>>>>>>>>>>>>>>>>>>$", deactivate_token
                        )
                        if (
                            deactivate_token.token_text
                            == LinkHelper.__link_start_sequence
                        ):
                            deactivate_token.deactivate()
                POGGER.debug("DEACTIVATED")
                LinkHelper.__display_specials_in_tokens(inline_blocks)
            return updated_index, True, token_to_append, consume_rest_of_line
        return new_index, False, token_to_append, consume_rest_of_line

    # pylint: enable=too-many-arguments

    @staticmethod
    def __revert_token_to_normal_text_token(inline_blocks, search_index):
        """
        Revert this token from a special text token back to a normal text token.
        """

        POGGER.debug("REVERTING")
        LinkHelper.__display_specials_in_tokens(inline_blocks)

        text_token_to_replace = inline_blocks[search_index]
        inline_blocks.insert(search_index, text_token_to_replace.create_copy())
        del inline_blocks[search_index + 1]

        POGGER.debug("REVERTED")
        LinkHelper.__display_specials_in_tokens(inline_blocks)

    @staticmethod
    def __display_specials_in_tokens(inline_blocks):
        display_parts = []
        for deactivate_token in inline_blocks:
            if deactivate_token.is_special_text:
                display_parts.extend(
                    [
                        f",>>Spec:{deactivate_token.is_active}:{deactivate_token}<<",
                    ]
                )
            else:
                display_parts.extend([",", str(deactivate_token)])

        POGGER.debug("$", "".join(display_parts)[1:])

    @staticmethod
    def __consume_text_for_image_alt_text(
        inline_blocks, ind, remaining_line, text_from_blocks_raw, xx_fn
    ):
        """
        Consume text from the inline blocks to use as part of the image's alt text.
        """

        inline_blocks_size, ind_plus_one = len(inline_blocks), ind + 1

        POGGER.debug("inline_blocks_size>>$<<", inline_blocks_size)
        POGGER.debug("ind>>$<<", ind)
        POGGER.debug(">>$<<", inline_blocks[ind_plus_one:])
        if inline_blocks_size > (ind_plus_one):

            alt_text_parts = []

            while inline_blocks_size > (ind_plus_one):
                if inline_blocks[ind_plus_one].is_special_text:
                    if inline_blocks[ind_plus_one].token_text == "]":
                        alt_text_parts.append(inline_blocks[ind_plus_one].token_text)
                elif inline_blocks[ind_plus_one].is_text:
                    alt_text_parts.append(
                        ParserHelper.resolve_all_from_text(
                            inline_blocks[ind_plus_one].token_text
                        )
                    )
                elif inline_blocks[ind_plus_one].is_inline_raw_html:
                    alt_text_parts.extend(
                        ["<", inline_blocks[ind_plus_one].raw_tag, ">"]
                    )
                elif inline_blocks[ind_plus_one].is_inline_code_span:
                    alt_text_parts.append(
                        ParserHelper.resolve_all_from_text(
                            inline_blocks[ind_plus_one].span_text
                        )
                    )
                elif inline_blocks[ind_plus_one].is_inline_autolink:
                    alt_text_parts.append(
                        ParserHelper.resolve_all_from_text(
                            inline_blocks[ind_plus_one].autolink_text
                        )
                    )
                elif (
                    inline_blocks[ind_plus_one].is_inline_link
                    or inline_blocks[ind_plus_one].is_inline_link_end
                    or inline_blocks[ind_plus_one].is_inline_emphasis
                    or inline_blocks[ind_plus_one].is_inline_emphasis_end
                ):
                    pass
                elif inline_blocks[ind_plus_one].is_inline_hard_break:
                    alt_text_parts.append(ParserHelper.newline_character)
                else:
                    assert inline_blocks[
                        ind_plus_one
                    ].is_inline_image, f"Not handled: {ParserHelper.make_value_visible(inline_blocks[ind_plus_one])}"
                    alt_text_parts.append(inline_blocks[ind_plus_one].image_alt_text)

                del inline_blocks[ind_plus_one]
                inline_blocks_size -= 1

            alt_text_parts.append(remaining_line)
            image_alt_text = "".join(alt_text_parts)
            POGGER.debug(">>after>>$>>", image_alt_text)
        else:
            POGGER.debug(">>composing>>$>>", text_from_blocks_raw)
            image_alt_text = xx_fn(text_from_blocks_raw)
            image_alt_text = ParserHelper.resolve_all_from_text(image_alt_text)
            image_alt_text = InlineHelper.append_text(
                "", image_alt_text, add_text_signature=False
            )
            POGGER.debug(">>composed>>$>>", image_alt_text)

        POGGER.debug(">>image_alt_text>>$>>", image_alt_text)
        POGGER.debug(">>text_from_blocks_raw>>$>>", text_from_blocks_raw)
        return image_alt_text, text_from_blocks_raw

    # pylint: disable=too-many-branches
    @staticmethod
    def __collect_text_from_blocks(inline_blocks, ind, suffix_text):
        """
        Aggregate the text component of text blocks.
        """

        POGGER.debug(
            ">>collect_text_from_blocks>>$",
            inline_blocks,
        )
        POGGER.debug(
            ">>collect_text_from_blocks>>suffix_text>>$",
            suffix_text,
        )

        (
            text_parts,
            text_raw_parts,
            collect_index,
            is_inside_of_link,
            inline_blocks_size,
        ) = ([], [], ind + 1, False, len(inline_blocks))
        while collect_index < inline_blocks_size:

            POGGER.debug(">>collect_text>>$<<", inline_blocks[collect_index])

            if inline_blocks[collect_index].is_inline_link_end:
                is_inside_of_link = False
            elif inline_blocks[collect_index].is_inline_link:
                (
                    is_inside_of_link,
                    raw_text,
                ) = True, LinkHelper.rehydrate_inline_link_text_from_token(
                    inline_blocks[collect_index]
                )
                text_raw_parts.append(raw_text)
            elif inline_blocks[collect_index].is_inline_image:
                text_raw_parts.append(
                    LinkHelper.rehydrate_inline_image_text_from_token(
                        inline_blocks[collect_index]
                    )
                )
                text_parts.append(inline_blocks[collect_index].image_alt_text)
            elif inline_blocks[collect_index].is_inline_code_span:
                if not is_inside_of_link:
                    POGGER.debug("CODESPAN>>$<<", inline_blocks[collect_index])
                    sub_parts = [
                        inline_blocks[collect_index].extracted_start_backticks,
                        ParserHelper.remove_all_from_text(
                            inline_blocks[collect_index].leading_whitespace
                        ),
                        ParserHelper.remove_all_from_text(
                            inline_blocks[collect_index].span_text
                        ),
                        ParserHelper.remove_all_from_text(
                            inline_blocks[collect_index].trailing_whitespace
                        ),
                        inline_blocks[collect_index].extracted_start_backticks,
                    ]
                    text_parts.extend(sub_parts)
                    text_raw_parts.extend(sub_parts)
            elif inline_blocks[collect_index].is_inline_raw_html:
                if not is_inside_of_link:
                    sub_parts = ["<", inline_blocks[collect_index].raw_tag, ">"]
                    text_parts.extend(sub_parts)
                    text_raw_parts.extend(sub_parts)
            elif inline_blocks[collect_index].is_inline_autolink:
                if not is_inside_of_link:
                    sub_parts = ["<", inline_blocks[collect_index].autolink_text, ">"]
                    text_parts.extend(sub_parts)
                    text_raw_parts.extend(sub_parts)
            elif inline_blocks[collect_index].is_inline_hard_break:
                POGGER.debug(
                    "is_inline_hard_break>>collected_text_raw>>$<<", text_raw_parts
                )
                converted_text = inline_blocks[collect_index].line_end
                text_parts.append(converted_text)
                if converted_text == "\\":
                    text_parts.append(converted_text)
                text_parts.append(ParserHelper.newline_character)
                text_raw_parts.append(converted_text)
                text_raw_parts.append(ParserHelper.newline_character)
                POGGER.debug(
                    "is_inline_hard_break>>collected_text_raw>>$<<", text_raw_parts
                )
            elif not is_inside_of_link:
                text_parts.append(inline_blocks[collect_index].token_text)
                text_raw_parts.append(inline_blocks[collect_index].token_text)
            POGGER.debug(
                ">>collect_text>>$<<$<<", text_parts, inline_blocks[collect_index]
            )
            POGGER.debug(">>collected_text_raw>>$<<", text_raw_parts)
            collect_index += 1

        POGGER.debug(">>collect_text_from_blocks>>$<<$<<", text_parts, suffix_text)
        POGGER.debug(">>collected_text_raw>>$<<$<<", text_raw_parts, suffix_text)
        text_parts.append(suffix_text)
        text_raw_parts.append(suffix_text)

        return "".join(text_parts), "".join(text_raw_parts)

    # pylint: enable=too-many-branches

    @staticmethod
    def __parse_angle_link_destination(source_text, new_index):
        """
        Parse a link destination that is included in angle brackets.
        """

        destination_parts, keep_collecting, new_index = [], True, new_index + 1
        while keep_collecting:
            keep_collecting = False
            new_index, ert_new = ParserHelper.collect_until_one_of_characters(
                source_text, new_index, LinkHelper.__angle_link_destination_breaks
            )
            destination_parts.append(ert_new)
            if ParserHelper.is_character_at_index(
                source_text, new_index, InlineHelper.backslash_character
            ):
                old_new_index = new_index
                inline_request = InlineRequest(source_text, new_index)
                inline_response = InlineHelper.handle_inline_backslash(inline_request)
                keep_collecting, new_index = True, inline_response.new_index
                destination_parts.append(source_text[old_new_index:new_index])

        if ParserHelper.is_character_at_index(
            source_text, new_index, LinkHelper.__angle_link_end
        ):
            new_index += 1
        else:
            new_index = -1
            destination_parts.clear()
        return new_index, "".join(destination_parts)

    @staticmethod
    def __parse_non_angle_link_destination(source_text, new_index):
        """
        Parse a link destination that is not included in angle brackets.
        """

        destination_parts, keep_collecting, nesting_level = [], True, 0
        while keep_collecting:
            POGGER.debug(
                "collected_destination>>$<<source_text<<$>>nesting_level>>$>>",
                destination_parts,
                source_text[new_index:],
                nesting_level,
            )
            keep_collecting = False
            new_index, before_part = ParserHelper.collect_until_one_of_characters(
                source_text, new_index, LinkHelper.__non_angle_link_breaks
            )
            destination_parts.append(before_part)
            POGGER.debug(">>>>>>$<<<<<", source_text[new_index:])
            if ParserHelper.is_character_at_index(
                source_text, new_index, InlineHelper.backslash_character
            ):
                POGGER.debug("backslash")
                keep_collecting, old_new_index = True, new_index
                inline_request = InlineRequest(source_text, new_index)
                inline_response = InlineHelper.handle_inline_backslash(inline_request)
                new_index = inline_response.new_index
                destination_parts.append(source_text[old_new_index:new_index])
            elif ParserHelper.is_character_at_index(
                source_text, new_index, LinkHelper.__non_angle_link_nest
            ):
                POGGER.debug("+1")
                nesting_level += 1
                destination_parts.append(LinkHelper.__non_angle_link_nest)
                new_index += 1
                keep_collecting = True
            elif ParserHelper.is_character_at_index(
                source_text, new_index, LinkHelper.__non_angle_link_unnest
            ):
                POGGER.debug("-1")
                if nesting_level:
                    destination_parts.append(LinkHelper.__non_angle_link_unnest)
                    new_index += 1
                    nesting_level -= 1
                    keep_collecting = True

        if nesting_level:
            return -1, None
        return new_index, "".join(destination_parts)

    @staticmethod
    def __parse_link_destination(source_text, new_index):
        """
        Parse an inline link's link destination.
        """

        POGGER.debug("parse_link_destination>>new_index>>$>>", source_text[new_index:])
        start_index, did_use_angle_start = new_index, False
        if ParserHelper.is_character_at_index(
            source_text, new_index, LinkHelper.__angle_link_start
        ):
            POGGER.debug(
                ">parse_angle_link_destination>new_index>$>$",
                new_index,
                source_text[new_index:],
            )
            did_use_angle_start = True
            new_index, ex_link = LinkHelper.__parse_angle_link_destination(
                source_text, new_index
            )
            POGGER.debug(
                ">parse_angle_link_destination>new_index>$>ex_link>$>",
                new_index,
                ex_link,
            )
        else:
            POGGER.debug(
                ">parse_non_angle_link_destination>new_index>$>$",
                new_index,
                source_text[new_index:],
            )
            new_index, ex_link = LinkHelper.__parse_non_angle_link_destination(
                source_text, new_index
            )
            POGGER.debug(
                ">parse_non_angle_link_destination>new_index>$>ex_link>$>",
                new_index,
                ex_link,
            )
            if not ex_link:
                return None, None, -1, None, None

        if new_index != -1 and ParserHelper.newline_character in ex_link:
            return None, None, -1, None, None
        POGGER.debug(
            "handle_backslashes>>new_index>>$>>ex_link>>$>>",
            new_index,
            ex_link,
        )

        pre_handle_link = ex_link
        if new_index != -1 and ex_link:
            ex_link = InlineHelper.handle_backslashes(ex_link, add_text_signature=False)
        POGGER.debug(
            "urllib.parse.quote>>ex_link>>$>>",
            ex_link,
        )

        ex_link = LinkHelper.__encode_link_destination(ex_link)
        POGGER.debug(
            "parse_link_destination>>new_index>>$>>ex_link>>$>>",
            new_index,
            ex_link,
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

        POGGER.debug("parse_link_title>>new_index>>$>>", source_text[new_index:])
        ex_title, bounding_character = "", ""
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
        POGGER.debug(
            "parse_link_title>>new_index>>$>>ex_link>>$>>",
            new_index,
            ex_title,
        )
        pre_ex_title = ex_title
        if ex_title is not None:
            ex_title = InlineHelper.append_text(
                "",
                InlineHelper.handle_backslashes(ex_title, add_text_signature=False),
                add_text_signature=False,
            )
        POGGER.debug("parse_link_title>>pre>>$>>", pre_ex_title)
        POGGER.debug("parse_link_title>>after>>$>>", ex_title)

        return ex_title, pre_ex_title, new_index, bounding_character

    @staticmethod
    def __process_inline_link_body(source_text, new_index):
        """
        Given that an inline link has been identified, process it's body.
        """

        POGGER.debug("process_inline_link_body>>$<<", source_text[new_index:])
        (
            inline_link,
            pre_inline_link,
            inline_title,
            pre_inline_title,
            did_use_angle_start,
            bounding_character,
            before_title_whitespace,
            after_title_whitespace,
        ) = ("", "", "", "", "", "", "", "")

        new_index, before_link_whitespace = ParserHelper.extract_any_whitespace(
            source_text, new_index
        )

        POGGER.debug(
            "new_index>>$>>source_text[]>>$>", new_index, source_text[new_index:]
        )
        if not ParserHelper.is_character_at_index(
            source_text, new_index, LinkHelper.__link_format_inline_end
        ):
            POGGER.debug(">>search for link destination")
            (
                inline_link,
                pre_inline_link,
                new_index,
                _,
                did_use_angle_start,
            ) = LinkHelper.__parse_link_destination(source_text, new_index)
            POGGER.debug(
                ">>link destination>>$>>$>>",
                source_text,
                new_index,
            )
            if new_index != -1:
                POGGER.debug(
                    "before ws>>$<",
                    source_text[new_index:],
                )
                (
                    new_index,
                    before_title_whitespace,
                ) = ParserHelper.extract_any_whitespace(source_text, new_index)
                POGGER.debug(
                    "after ws>>$>",
                    source_text[new_index:],
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
        POGGER.debug(
            "inline_link>>$>>inline_title>>$>new_index>$>",
            inline_link,
            inline_title,
            new_index,
        )
        if new_index != -1:
            if ParserHelper.is_character_at_index(
                source_text, new_index, LinkHelper.__link_format_inline_end
            ):
                new_index += 1
            else:
                new_index = -1
        POGGER.debug(
            "process_inline_link_body>>inline_link>>$>>inline_title>>$>new_index>$>",
            inline_link,
            inline_title,
            new_index,
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

        POGGER.debug("pre>>$<<", link_to_lookup)
        inline_link, inline_title, link_to_lookup = (
            "",
            "",
            ParserHelper.remove_all_from_text(link_to_lookup),
        )
        POGGER.debug("mid(pre-norm)>>$<<", link_to_lookup)

        link_label = LinkHelper.normalize_link_label(link_to_lookup)
        POGGER.debug("post>>$<<", link_label)

        POGGER.debug("defs>>$<<", LinkHelper.__link_definitions)
        if not link_label or link_label not in LinkHelper.__link_definitions:
            update_index = -1
        else:
            POGGER.debug(link_type)
            update_index, inline_link, inline_title = (
                new_index,
                LinkHelper.__link_definitions[link_label][0],
                LinkHelper.__link_definitions[link_label][1],
            )
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

        POGGER.debug(
            "handle_link_types>>$<<$<<",
            inline_blocks,
            ind,
        )
        POGGER.debug(
            "handle_link_types>source_text>>$<<",
            source_text,
        )
        POGGER.debug("handle_link_types>>$<<", source_text[new_index:])
        POGGER.debug(
            "handle_link_types>>current_string_unresolved>>$<<remaining_line<<$>>",
            current_string_unresolved,
            remaining_line,
        )
        text_from_blocks, text_from_blocks_raw = LinkHelper.__collect_text_from_blocks(
            inline_blocks, ind, f"{current_string_unresolved}{remaining_line}"
        )
        POGGER.debug(
            "handle_link_types>>text_from_blocks>>$<<",
            text_from_blocks,
        )
        POGGER.debug(
            "handle_link_types>>text_from_blocks_raw>>$<<",
            text_from_blocks_raw,
        )
        POGGER.debug(
            "handle_link_types>>text_from_blocks>>$<<",
            text_from_blocks,
        )
        text_from_blocks = ParserHelper.resolve_backspaces_from_text(text_from_blocks)
        POGGER.debug(
            "handle_link_types>>text_from_blocks>>$<<",
            text_from_blocks,
        )

        consume_rest_of_line = False

        POGGER.debug("__look_for_link_formats>>$>>", new_index)
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
        POGGER.debug("__look_for_link_formats>>update_index>>$>>", update_index)

        # u != -1 - inline valid
        # tried_full_reference_form - collapsed or full valid
        if update_index == -1 and not tried_full_reference_form:
            ex_label = ""
            POGGER.debug("shortcut?")
            POGGER.debug(
                ">>$<<",
                inline_blocks,
            )
            POGGER.debug(
                ">>$<<",
                text_from_blocks,
            )

            update_index, inline_link, inline_title = LinkHelper.__look_up_link(
                text_from_blocks, new_index, "shortcut"
            )
            label_type, pre_inline_link = "shortcut", ""

        token_to_append = None
        POGGER.debug("<<<<<<<new_index<<<<<<<$<<", new_index)
        POGGER.debug("<<<<<<<update_index<<<<<<<$<<", update_index)
        POGGER.debug("<<<<<<<text_from_blocks_raw<<<<<<<$<<", text_from_blocks_raw)
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

        POGGER.debug(
            "handle_link_types<update_index<$<<$<<",
            update_index,
            token_to_append,
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
        consume_rest_of_line, token_to_append = False, None

        POGGER.debug("<<<<<<<start_text<<<<<<<$<<", start_text)
        POGGER.debug(">>inline_link>>$>>", inline_link)
        POGGER.debug(">>pre_inline_link>>$>>", pre_inline_link)
        POGGER.debug(">>inline_title>>$>>", inline_title)
        POGGER.debug(">>pre_inline_title>>$>>", pre_inline_title)
        POGGER.debug(
            ">>text_from_blocks>>$>>",
            text_from_blocks,
        )
        if pre_inline_link == inline_link:
            pre_inline_link = ""
        if pre_inline_title == inline_title:
            pre_inline_title = ""
        POGGER.debug(">>pre_inline_link>>$>>", pre_inline_link)

        text_from_blocks_raw = ParserHelper.resolve_backspaces_from_text(
            text_from_blocks_raw
        )
        POGGER.debug(">>text_from_blocks_raw>>$>>", text_from_blocks_raw)
        POGGER.debug(">>inline_blocks[ind]>>$>>", inline_blocks[ind])

        line_number, column_number = (
            inline_blocks[ind].line_number,
            inline_blocks[ind].column_number,
        )
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
            token_to_append = inline_blocks[
                ind
            ].generate_close_markdown_token_from_markdown_token("", "", False)
        else:
            assert start_text == LinkHelper.image_start_sequence
            consume_rest_of_line = True
            POGGER.debug("\n>>__consume_text_for_image_alt_text>>$>>", inline_blocks)
            POGGER.debug("\n>>__consume_text_for_image_alt_text>>$>>", ind)
            POGGER.debug("\n>>__consume_text_for_image_alt_text>>$>>", remaining_line)
            (
                image_alt_text,
                text_from_blocks_raw,
            ) = LinkHelper.__consume_text_for_image_alt_text(
                inline_blocks, ind, remaining_line, text_from_blocks_raw, xx_fn
            )
            POGGER.debug("\n>>__consume_text_for_image_alt_text>>$>>", image_alt_text)

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
            POGGER.debug("\n>>Image>>$", inline_blocks)
            POGGER.debug(">>start_text>>$<<", start_text)
            POGGER.debug(">>remaining_line>>$<<", remaining_line)
            POGGER.debug(">>current_string_unresolved>>$<<", current_string_unresolved)
        return consume_rest_of_line, token_to_append

    # pylint: enable=too-many-arguments, too-many-locals

    # pylint: disable=too-many-locals
    @staticmethod
    def __look_for_link_formats(source_text, new_index, text_from_blocks):
        """
        Look for links in the various formats.
        """
        (
            inline_link,
            pre_inline_link,
            inline_title,
            pre_inline_title,
            update_index,
            ex_label,
            label_type,
            did_use_angle_start,
            bounding_character,
            before_link_whitespace,
            before_title_whitespace,
            after_title_whitespace,
            tried_full_reference_form,
        ) = ("", "", "", "", -1, "", "", "", "", "", "", "", False)
        if ParserHelper.is_character_at_index(
            source_text, new_index, LinkHelper.__link_format_inline_start
        ):
            POGGER.debug("inline reference? >>$>>", new_index)
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
            POGGER.debug("collapsed reference?")
            after_open_index = new_index + 1
            if ParserHelper.is_character_at_index(
                source_text, after_open_index, LinkHelper.__link_format_reference_end
            ):
                POGGER.debug("collapsed reference")
                POGGER.debug(">>$>>", text_from_blocks)
                update_index, inline_link, inline_title = LinkHelper.__look_up_link(
                    text_from_blocks,
                    after_open_index + 1,
                    "collapsed reference",
                )
                POGGER.debug("collapsed reference>update_index>$", update_index)
                label_type, tried_full_reference_form = "collapsed", True
            else:
                POGGER.debug("full reference?")
                POGGER.debug(">>did_extract>>$>", source_text[after_open_index:])
                (
                    did_extract,
                    after_label_index,
                    ex_label,
                ) = LinkHelper.extract_link_label(
                    source_text, after_open_index, include_reference_colon=False
                )
                POGGER.debug(
                    ">>did_extract>>$>after_label_index>$>ex_label>$>",
                    did_extract,
                    after_label_index,
                    ex_label,
                )
                if did_extract:
                    label_type, tried_full_reference_form = "full", True
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

        el_parts = []
        percent_index, before_data = ParserHelper.collect_until_one_of_characters(
            link_to_encode, 0, LinkHelper.__special_link_destination_characters
        )
        el_parts.append(
            urllib.parse.quote(before_data, safe=LinkHelper.__link_safe_characters)
        )
        link_to_encode_size = len(link_to_encode)
        while percent_index < link_to_encode_size:
            special_character = link_to_encode[percent_index]
            percent_index += 1
            if special_character == "%":
                hex_guess_characters = link_to_encode[percent_index : percent_index + 2]
                if len(hex_guess_characters) == 2:
                    try:
                        int(hex_guess_characters, 16)
                        el_parts.extend(["%", hex_guess_characters])
                        percent_index += 2
                    except ValueError:
                        el_parts.append("%25")
                else:
                    el_parts.append("%25")
            else:
                assert special_character == "&"
                el_parts.append("&amp;")

            percent_index, before_data = ParserHelper.collect_until_one_of_characters(
                link_to_encode,
                percent_index,
                LinkHelper.__special_link_destination_characters,
            )
            el_parts.append(
                urllib.parse.quote(before_data, safe=LinkHelper.__link_safe_characters)
            )

        return "".join(el_parts)

    @staticmethod
    def rehydrate_inline_image_text_from_token(image_token):
        """
        Given an image token, rehydrate it's original text from the token.
        """
        return f"!{LinkHelper.rehydrate_inline_link_text_from_token(image_token)}"

    @staticmethod
    def rehydrate_inline_link_text_from_token(link_token):
        """
        Given a link token, rehydrate it's original text from the token.
        """

        link_parts = []
        if link_token.label_type == "shortcut":
            link_parts.extend(
                [
                    "[",
                    ParserHelper.remove_all_from_text(link_token.text_from_blocks),
                    "]",
                ]
            )
        elif link_token.label_type == "full":
            link_parts.extend(
                ["[", link_token.text_from_blocks, "][", link_token.ex_label, "]"]
            )
        elif link_token.label_type == "collapsed":
            link_parts.extend(["[", link_token.text_from_blocks, "][]"])
        else:
            assert link_token.label_type == "inline"

            link_parts.extend(
                [
                    "[",
                    ParserHelper.remove_all_from_text(link_token.text_from_blocks),
                    "](",
                    link_token.before_link_whitespace,
                    f"<{link_token.active_link_uri}>"
                    if link_token.did_use_angle_start
                    else link_token.active_link_uri,
                    link_token.before_title_whitespace,
                ]
            )
            if link_token.active_link_title:
                if link_token.inline_title_bounding_character == "'":
                    title_prefix = "'"
                    title_suffix = "'"
                elif link_token.inline_title_bounding_character == "(":
                    title_prefix = "("
                    title_suffix = ")"
                else:
                    title_prefix = '"'
                    title_suffix = '"'

                link_parts.extend(
                    [
                        title_prefix,
                        link_token.active_link_title,
                        title_suffix,
                        link_token.after_title_whitespace,
                    ]
                )
            link_parts.append(")")
        return "".join(link_parts)
