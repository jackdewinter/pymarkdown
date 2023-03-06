"""
Module to provide for the ability to parse the text for a link.
"""
import logging
import urllib
import urllib.parse
from typing import Dict, List, Optional, Tuple

from pymarkdown.constants import Constants
from pymarkdown.inline.inline_backslash_helper import InlineBackslashHelper
from pymarkdown.inline.inline_helper import InlineHelper
from pymarkdown.inline.inline_request import InlineRequest
from pymarkdown.links.link_helper_properties import LinkHelperProperties
from pymarkdown.links.link_reference_titles import LinkReferenceTitles
from pymarkdown.parser_helper import ParserHelper
from pymarkdown.parser_logger import ParserLogger

POGGER = ParserLogger(logging.getLogger(__name__))


class LinkParseHelper:
    """
    Class to provide for the ability to parse the text for a link.
    """

    __link_definitions: Dict[str, LinkReferenceTitles] = {}

    __link_safe_characters = "/#:?=()*!$'+,;@"
    __special_link_destination_characters = "%&"

    __link_format_inline_start = "("
    __link_format_inline_end = ")"

    __link_title_single = "'"
    __link_title_double = '"'
    __link_title_parenthesis_open = "("
    __link_title_parenthesis_close = ")"

    __link_format_inline_end = ")"
    __link_format_reference_start = "["
    __link_format_reference_end = "]"

    link_label_start = "["
    link_label_end = "]"
    __link_label_is_definition_character = ":"
    __link_label_breaks = (
        f"{link_label_start}{link_label_end}{InlineBackslashHelper.backslash_character}"
    )

    __angle_link_start = "<"
    __angle_link_end = ">"
    __angle_link_destination_breaks = (
        f"{__angle_link_end}{InlineBackslashHelper.backslash_character}"
    )

    __non_angle_link_nest = "("
    __non_angle_link_unnest = ")"
    __non_angle_link_breaks = f"{Constants.ascii_control_characters}()\\"

    @staticmethod
    def initialize() -> None:
        """
        Initialize the inline subsystem.
        """
        LinkParseHelper.__link_definitions = {}

    @staticmethod
    def add_link_definition(link_name: str, link_value: LinkReferenceTitles) -> bool:
        """
        Add a link definition to the cache of links.
        """
        POGGER.debug(
            ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>$",
            LinkParseHelper.__link_definitions,
        )
        POGGER.debug(
            ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>$:$",
            link_name,
            link_value,
        )
        did_add_definition = link_name not in LinkParseHelper.__link_definitions
        if did_add_definition:
            LinkParseHelper.__link_definitions[link_name] = link_value
            POGGER.debug(">>added def>>$-->$", link_name, link_value)
        return did_add_definition

    @staticmethod
    def normalize_link_label(link_label: str) -> str:
        """
        Translate a link label into a normalized form to use for comparisons.
        """

        # Fold all whitespace characters (except for space) into a space character
        link_label = ParserHelper.replace_any_of(
            link_label,
            Constants.non_space_ascii_whitespace,
            ParserHelper.space_character,
        )

        # Fold multiple spaces into a single space character.
        link_label = ParserHelper.space_character.join(link_label.split())

        # Fold the case of any characters to their lower equivalent.
        return link_label.casefold().strip()

    @staticmethod
    def look_up_link(
        link_to_lookup: str, new_index: int, link_type: str
    ) -> Tuple[int, str, str]:
        """
        Look up a link to see if it is present.
        """

        POGGER.debug("pre>>$<<", link_to_lookup)
        link_to_lookup = ParserHelper.remove_all_from_text(link_to_lookup)
        POGGER.debug("mid(pre-norm)>>$<<", link_to_lookup)

        link_label = LinkParseHelper.normalize_link_label(link_to_lookup)
        POGGER.debug("post>>$<<", link_label)

        POGGER.debug("defs>>$<<", LinkParseHelper.__link_definitions)
        if not link_label or link_label not in LinkParseHelper.__link_definitions:
            update_index: int = -1
            inline_link: str = ""
            inline_title: str = ""
        else:
            POGGER.debug(link_type)
            link_titles = LinkParseHelper.__link_definitions[link_label]
            assert link_titles.inline_link is not None
            assert link_titles.inline_title is not None
            update_index, inline_link, inline_title = (
                new_index,
                link_titles.inline_link,
                link_titles.inline_title,
            )
        return update_index, inline_link, inline_title

    @staticmethod
    def __try_to_find_link_match(
        new_index: int,
        source_text: str,
        text_from_blocks: str,
        tabified_text: Optional[str],
    ) -> Tuple[str, bool, int, str, str, Optional[str]]:
        POGGER.debug("collapsed reference?")

        # TODO label type as Enum?

        text_to_scan = source_text
        if tabified_text:
            assert tabified_text is not None
            text_to_scan = tabified_text
            tabified_new_index = LinkParseHelper.__translate_between_strings(
                source_text, tabified_text, new_index
            )
            POGGER.debug("tabified_new_index>:$:<", tabified_new_index)
            new_index = tabified_new_index

        after_open_index = new_index + 1
        tried_full_reference_form = ParserHelper.is_character_at_index(
            text_to_scan, after_open_index, LinkParseHelper.__link_format_reference_end
        )
        if tried_full_reference_form:
            ex_label: Optional[str] = ""

            POGGER.debug("collapsed reference")
            POGGER.debug(">>$>>", text_from_blocks)
            update_index, inline_link, inline_title = LinkParseHelper.look_up_link(
                text_from_blocks,
                after_open_index + 1,
                "collapsed reference",
            )
            POGGER.debug("collapsed reference>update_index>$", update_index)
            label_type = Constants.link_type__collapsed
        else:
            (
                ex_label,
                label_type,
                inline_link,
                inline_title,
                update_index,
                tried_full_reference_form,
            ) = LinkParseHelper.__try_to_find_link_match_try_full(
                text_to_scan, after_open_index
            )

        if tabified_text and update_index != -1:
            assert tabified_text is not None

            # Both of the above functions consume the last character of the link.
            # Instead of guessing, we "rewind" the index by one character so that
            # we can have something to sync on that is not an end of line or whitespace.
            assert (
                tabified_text[update_index - 1]
                == LinkParseHelper.__link_format_reference_end
            )
            untabified_update_index = LinkParseHelper.__translate_between_strings(
                tabified_text, source_text, update_index - 1
            )
            POGGER.debug("untabified_update_index>:$:<", untabified_update_index)
            update_index = untabified_update_index + 1

        return (
            label_type,
            tried_full_reference_form,
            update_index,
            inline_link,
            inline_title,
            ex_label,
        )

    @staticmethod
    def __try_to_find_link_match_try_full(
        text_to_scan: str, after_open_index: int
    ) -> Tuple[Optional[str], str, str, str, int, bool]:
        POGGER.debug("full reference?")
        POGGER.debug(">>did_extract>>$>", text_to_scan[after_open_index:])
        (
            did_extract,
            after_label_index,
            ex_label,
        ) = LinkParseHelper.extract_link_label(
            text_to_scan, after_open_index, include_reference_colon=False
        )
        POGGER.debug(
            ">>did_extract>>$>after_label_index>$>ex_label>$>",
            did_extract,
            after_label_index,
            ex_label,
        )
        tried_full_reference_form = did_extract
        if tried_full_reference_form:
            assert ex_label is not None
            label_type = Constants.link_type__full
            update_index, inline_link, inline_title = LinkParseHelper.look_up_link(
                ex_label, after_label_index, "full reference"
            )
        else:
            label_type, inline_link, inline_title, update_index = "", "", "", -1
        return (
            ex_label,
            label_type,
            inline_link,
            inline_title,
            update_index,
            tried_full_reference_form,
        )

    @staticmethod
    def __translate_between_strings(
        source_text: str, destination_text: str, next_index: int
    ) -> int:
        stop_character = source_text[next_index]

        POGGER.debug("source_text>:$:<", source_text)
        POGGER.debug("index>:$:< == >:$:<", next_index, stop_character)
        POGGER.debug("destination_text>:$:<", destination_text)

        found_in_source_text_count = 0
        found_in_source_text_index = source_text.find(stop_character)
        POGGER.debug(
            "source_text[$]>:$:<",
            found_in_source_text_index,
            source_text[found_in_source_text_index:],
        )
        while found_in_source_text_index != next_index:
            found_in_source_text_count += 1
            found_in_source_text_index = source_text.find(
                stop_character, found_in_source_text_index + 1
            )
            POGGER.debug(
                "source_text[$]>:$:<",
                found_in_source_text_index,
                source_text[found_in_source_text_index:],
            )
        POGGER.debug("found_in_source_text_count>:$:<", found_in_source_text_count)
        POGGER.debug(
            "source_text[$]>:$:<",
            found_in_source_text_index,
            source_text[found_in_source_text_index:],
        )

        found_in_destination_text_count = 0
        stop_character_in_destination_index = destination_text.find(stop_character)
        POGGER.debug(
            "stop_character_in_destination_index[$]>:$:<",
            stop_character_in_destination_index,
            destination_text[stop_character_in_destination_index:],
        )
        while found_in_destination_text_count != found_in_source_text_count:
            found_in_destination_text_count += 1
            stop_character_in_destination_index = destination_text.find(
                stop_character, stop_character_in_destination_index + 1
            )
            POGGER.debug(
                "adj_tabified_text[$]>:$:<",
                stop_character_in_destination_index,
                destination_text[stop_character_in_destination_index:],
            )
            assert stop_character_in_destination_index != -1
        POGGER.debug(
            "found_in_destination_text_count>:$:<", found_in_destination_text_count
        )
        POGGER.debug(
            "adj_tabified_text[$]>:$:<",
            stop_character_in_destination_index,
            destination_text[stop_character_in_destination_index:],
        )
        assert destination_text[stop_character_in_destination_index] == stop_character
        return stop_character_in_destination_index

    @staticmethod
    def __parse_link_title(
        source_text: str, new_index: int
    ) -> Tuple[Optional[str], Optional[str], int, str]:
        """
        Parse an inline link's link title.
        """

        POGGER.debug("parse_link_title>>new_index>>$>>", source_text[new_index:])
        ex_title: Optional[str] = ""
        bounding_character = ""
        newer_index: Optional[int] = new_index
        assert newer_index is not None
        if ParserHelper.is_character_at_index(
            source_text, newer_index, LinkParseHelper.__link_title_single
        ):
            bounding_character = LinkParseHelper.__link_title_single
            newer_index, ex_title = InlineHelper.extract_bounded_string(
                source_text, newer_index + 1, LinkParseHelper.__link_title_single, None
            )
        elif ParserHelper.is_character_at_index(
            source_text, newer_index, LinkParseHelper.__link_title_double
        ):
            bounding_character = LinkParseHelper.__link_title_double
            newer_index, ex_title = InlineHelper.extract_bounded_string(
                source_text, newer_index + 1, LinkParseHelper.__link_title_double, None
            )
        elif ParserHelper.is_character_at_index(
            source_text, newer_index, LinkParseHelper.__link_title_parenthesis_open
        ):
            bounding_character = LinkParseHelper.__link_title_parenthesis_open
            newer_index, ex_title = InlineHelper.extract_bounded_string(
                source_text,
                newer_index + 1,
                LinkParseHelper.__link_title_parenthesis_close,
                LinkParseHelper.__link_title_parenthesis_open,
            )
        else:
            newer_index = -1
        POGGER.debug(
            "parse_link_title>>new_index>>$>>ex_link>>$>>",
            newer_index,
            ex_title,
        )
        pre_ex_title = ex_title
        if ex_title is not None:
            ex_title = InlineHelper.append_text(
                "",
                InlineBackslashHelper.handle_backslashes(ex_title),
                add_text_signature=False,
            )
        POGGER.debug("parse_link_title>>pre>>$>>", pre_ex_title)
        POGGER.debug("parse_link_title>>after>>$>>", ex_title)

        assert newer_index is not None
        return ex_title, pre_ex_title, newer_index, bounding_character

    @staticmethod
    def extract_link_title(
        line_to_parse: str, new_index: Optional[int], is_blank_line: bool
    ) -> Tuple[
        bool, Optional[int], Optional[str], Optional[str], Optional[str], Optional[str]
    ]:
        """
        Extract the link reference definition's optional link title.
        """
        POGGER.debug("before ws>>$>", line_to_parse[new_index:])
        assert new_index is not None
        new_index, ex_ws = ParserHelper.extract_ascii_whitespace(
            line_to_parse, new_index
        )
        assert new_index is not None
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
            ) = LinkParseHelper.__parse_link_title(line_to_parse, new_index)
            if new_index == -1 or inline_title is None:
                return False, new_index, None, None, None, None
        else:
            inline_title, pre_inline_title = "", ""
        return (
            True,
            new_index,
            inline_title,
            pre_inline_title,
            ex_ws,
            line_to_parse[start_index:new_index],
        )

    @staticmethod
    def __encode_link_destination(link_to_encode: str) -> str:
        percent_index, before_data = ParserHelper.collect_until_one_of_characters(
            link_to_encode, 0, LinkParseHelper.__special_link_destination_characters
        )
        assert percent_index is not None
        assert before_data is not None
        el_parts, link_to_encode_size = [
            urllib.parse.quote(before_data, safe=LinkParseHelper.__link_safe_characters)
        ], len(link_to_encode)
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
                LinkParseHelper.__special_link_destination_characters,
            )
            assert percent_index is not None
            assert before_data is not None
            el_parts.append(
                urllib.parse.quote(
                    before_data, safe=LinkParseHelper.__link_safe_characters
                )
            )

        return "".join(el_parts)

    @staticmethod
    def __parse_link_destination(
        source_text: str, new_index: int
    ) -> Tuple[Optional[str], Optional[str], int, Optional[str], Optional[bool]]:
        """
        Parse an inline link's link destination.
        """

        POGGER.debug("parse_link_destination>>new_index>>$>>", source_text[new_index:])
        start_index = new_index
        did_use_angle_start = ParserHelper.is_character_at_index(
            source_text, new_index, LinkParseHelper.__angle_link_start
        )
        ex_link: Optional[str] = ""
        if did_use_angle_start:
            POGGER.debug(
                ">parse_angle_link_destination>new_index>$>$",
                new_index,
                source_text[new_index:],
            )
            new_index, ex_link = LinkParseHelper.__parse_angle_link_destination(
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
            newer_index, ex_link = LinkParseHelper.__parse_non_angle_link_destination(
                source_text, new_index
            )
            assert newer_index is not None
            new_index = newer_index
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
            ex_link = InlineBackslashHelper.handle_backslashes(ex_link)
        POGGER.debug(
            "urllib.parse.quote>>ex_link>>$>>",
            ex_link,
        )

        ex_link = LinkParseHelper.__encode_link_destination(ex_link)
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
    def __parse_non_angle_link_destination(
        source_text: str, new_index: int
    ) -> Tuple[Optional[int], Optional[str]]:
        """
        Parse a link destination that is not included in angle brackets.
        """

        destination_parts: List[str] = []
        keep_collecting, nesting_level = True, 0
        newer_index: Optional[int] = new_index
        while keep_collecting:
            assert newer_index is not None
            POGGER.debug(
                "collected_destination>>$<<source_text<<$>>nesting_level>>$>>",
                destination_parts,
                source_text[newer_index:],
                nesting_level,
            )
            newer_index, before_part = ParserHelper.collect_until_one_of_characters(
                source_text, newer_index, LinkParseHelper.__non_angle_link_breaks
            )
            assert newer_index is not None
            assert before_part is not None
            destination_parts.append(before_part)
            POGGER.debug(">>>>>>$<<<<<", source_text[newer_index:])
            if ParserHelper.is_character_at_index(
                source_text, newer_index, InlineBackslashHelper.backslash_character
            ):
                POGGER.debug("backslash")
                old_new_index = newer_index
                inline_request = InlineRequest(source_text, newer_index)
                inline_response = InlineBackslashHelper.handle_inline_backslash(
                    inline_request
                )
                newer_index = inline_response.new_index
                destination_parts.append(source_text[old_new_index:newer_index])
            elif ParserHelper.is_character_at_index(
                source_text, newer_index, LinkParseHelper.__non_angle_link_nest
            ):
                POGGER.debug("+1")
                nesting_level += 1
                destination_parts.append(LinkParseHelper.__non_angle_link_nest)
                newer_index += 1
            elif ParserHelper.is_character_at_index(
                source_text, newer_index, LinkParseHelper.__non_angle_link_unnest
            ):
                POGGER.debug("-1")
                keep_collecting = bool(nesting_level)
                if keep_collecting:
                    destination_parts.append(LinkParseHelper.__non_angle_link_unnest)
                    newer_index += 1
                    nesting_level -= 1
            else:
                keep_collecting = False

        if nesting_level:
            return -1, None
        return newer_index, "".join(destination_parts)

    @staticmethod
    def __parse_angle_link_destination(
        source_text: str, new_index: int
    ) -> Tuple[int, str]:
        """
        Parse a link destination that is included in angle brackets.
        """

        destination_parts: List[str] = []
        newer_index: Optional[int] = new_index + 1
        while True:
            assert newer_index is not None
            newer_index, ert_new = ParserHelper.collect_until_one_of_characters(
                source_text,
                newer_index,
                LinkParseHelper.__angle_link_destination_breaks,
            )
            assert newer_index is not None
            assert ert_new is not None
            destination_parts.append(ert_new)

            if not ParserHelper.is_character_at_index(
                source_text, newer_index, InlineBackslashHelper.backslash_character
            ):
                break

            old_new_index = newer_index
            inline_request = InlineRequest(source_text, newer_index)
            inline_response = InlineBackslashHelper.handle_inline_backslash(
                inline_request
            )
            newer_index = inline_response.new_index
            destination_parts.append(source_text[old_new_index:newer_index])
        if ParserHelper.is_character_at_index(
            source_text, newer_index, LinkParseHelper.__angle_link_end
        ):
            newer_index += 1
        else:
            newer_index = -1
            destination_parts.clear()
        return newer_index, "".join(destination_parts)

    @staticmethod
    def __parse_inline_link_properties(
        source_text: str, new_index: int, lhp: LinkHelperProperties
    ) -> int:
        lhp.inline_title = ""
        lhp.pre_inline_title = ""
        lhp.bounding_character = ""
        lhp.before_title_whitespace = ""
        lhp.after_title_whitespace = ""
        newer_index: Optional[int] = None
        temp_bool = None
        POGGER.debug(">>search for link destination")
        (
            lhp.inline_link,
            lhp.pre_inline_link,
            newer_index,
            _,
            temp_bool,
        ) = LinkParseHelper.__parse_link_destination(source_text, new_index)
        lhp.did_use_angle_start = temp_bool
        POGGER.debug(
            ">>link destination>>$>>$>>",
            source_text,
            newer_index,
        )
        if newer_index != -1:
            POGGER.debug(
                "before ws>>$<",
                source_text[newer_index:],
            )
            (
                newer_index,
                lhp.before_title_whitespace,
            ) = ParserHelper.extract_ascii_whitespace(source_text, newer_index)
            POGGER.debug(
                "after ws>>$>",
                source_text[newer_index:],
            )
            assert newer_index is not None
            if ParserHelper.is_character_at_index_not(
                source_text, newer_index, LinkParseHelper.__link_format_inline_end
            ):
                (
                    lhp.inline_title,
                    lhp.pre_inline_title,
                    newer_index,
                    lhp.bounding_character,
                ) = LinkParseHelper.__parse_link_title(source_text, newer_index)
        if newer_index != -1:
            (
                newer_index,
                lhp.after_title_whitespace,
            ) = ParserHelper.extract_ascii_whitespace(source_text, newer_index)
        assert newer_index is not None
        return newer_index

    @staticmethod
    def extract_link_label(
        line_to_parse: str, new_index: int, include_reference_colon: bool = True
    ) -> Tuple[bool, int, Optional[str]]:
        """
        Extract the link reference definition's link label.
        """
        label_parts: List[str] = []

        while True:
            newer_index, ert_new = ParserHelper.collect_until_one_of_characters(
                line_to_parse, new_index, LinkParseHelper.__link_label_breaks
            )
            assert newer_index is not None
            assert ert_new is not None
            new_index = newer_index
            label_parts.append(ert_new)
            if ParserHelper.is_character_at_index(
                line_to_parse, new_index, InlineBackslashHelper.backslash_character
            ):
                old_new_index = new_index
                inline_response = InlineBackslashHelper.handle_inline_backslash(
                    InlineRequest(line_to_parse, new_index)
                )
                assert inline_response.new_index is not None
                new_index = inline_response.new_index
                label_parts.append(line_to_parse[old_new_index:new_index])
            elif ParserHelper.is_character_at_index(
                line_to_parse, new_index, LinkParseHelper.link_label_start
            ):
                POGGER.debug(">> unescaped [, bailing")
                return False, -1, None
            else:
                break  # pragma: no cover

        POGGER.debug("look for ]>>$<<", line_to_parse[new_index:])
        if not ParserHelper.is_character_at_index(
            line_to_parse, new_index, LinkParseHelper.link_label_end
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
                LinkParseHelper.__link_label_is_definition_character,
            ):
                POGGER.debug(">> no :, bailing")
                return False, -1, None
            new_index += 1

        return True, new_index, "".join(label_parts)

    @staticmethod
    def extract_link_destination(
        line_to_parse: str, start_index: int, is_blank_line: bool
    ) -> Tuple[
        bool, Optional[int], Optional[str], Optional[str], Optional[str], Optional[str]
    ]:
        """
        Extract the link reference definition's link destination.
        """
        after_whitespace_index: Optional[int] = None
        (
            after_whitespace_index,
            prefix_whitespace,
        ) = ParserHelper.collect_while_one_of_characters(
            line_to_parse, start_index, Constants.ascii_whitespace
        )
        assert after_whitespace_index is not None
        if after_whitespace_index == len(line_to_parse) and not is_blank_line:
            return False, after_whitespace_index, None, None, None, None

        assert prefix_whitespace is not None
        POGGER.debug(
            "Pre-LD>>$<<", ParserHelper.make_whitespace_visible(prefix_whitespace)
        )
        POGGER.debug("LD>>$<<", line_to_parse[after_whitespace_index:])
        (
            inline_link,
            pre_inline_link,
            after_whitespace_index,
            inline_raw_link,
            _,
        ) = LinkParseHelper.__parse_link_destination(
            line_to_parse, after_whitespace_index
        )
        if after_whitespace_index == -1:
            return False, -1, None, None, None, None
        return (
            True,
            after_whitespace_index,
            inline_link,
            pre_inline_link,
            prefix_whitespace,
            inline_raw_link,
        )

    @staticmethod
    def __process_inline_link_body(
        source_text: str,
        new_index: int,
        tabified_text: Optional[str],
        lhp: LinkHelperProperties,
    ) -> int:
        """
        Given that an inline link has been identified, process it's body.
        """

        POGGER.debug("process_inline_link_body>:$:<", source_text[new_index:])
        POGGER.debug("source_text>:$:<", source_text)
        POGGER.debug("tabified_text>:$:<", tabified_text)

        text_to_scan = source_text
        if tabified_text:
            text_to_scan = tabified_text
            tabified_new_index = LinkParseHelper.__translate_between_strings(
                source_text, tabified_text, new_index
            )
            POGGER.debug("tabified_new_index>:$:<", tabified_new_index)
            new_index = tabified_new_index

        new_index += 1

        newer_index, lhp.before_link_whitespace = ParserHelper.extract_ascii_whitespace(
            text_to_scan, new_index
        )

        POGGER.debug(
            "newer_index>>$>>text_to_scan[]>>$>",
            newer_index,
            text_to_scan[newer_index:],
        )
        assert newer_index is not None
        if not ParserHelper.is_character_at_index(
            text_to_scan, newer_index, LinkParseHelper.__link_format_inline_end
        ):
            newer_index = LinkParseHelper.__parse_inline_link_properties(
                text_to_scan, newer_index, lhp
            )
        else:
            (
                lhp.inline_link,
                lhp.pre_inline_link,
                lhp.inline_title,
                lhp.pre_inline_title,
                lhp.did_use_angle_start,
                lhp.bounding_character,
                lhp.before_title_whitespace,
                lhp.after_title_whitespace,
            ) = ("", "", "", "", False, "", "", "")
        POGGER.debug(
            "inline_link>>$>>inline_title>>$>newer_index>$>",
            lhp.inline_link,
            lhp.inline_title,
            newer_index,
        )
        assert newer_index is not None
        (
            newer_index,
            lhp.did_use_angle_start,
        ) = LinkParseHelper.__process_inline_link_body_final(
            newer_index, source_text, tabified_text, lhp.did_use_angle_start
        )
        POGGER.debug(
            "process_inline_link_body>>inline_link>>$>>inline_title>>$>new_index>$>",
            lhp.inline_link,
            lhp.inline_title,
            newer_index,
        )
        return newer_index

    @staticmethod
    def __process_inline_link_body_final(
        newer_index: int,
        source_text: str,
        tabified_text: Optional[str],
        did_use_angle_start: Optional[bool],
    ) -> Tuple[int, bool]:
        if newer_index != -1:
            if tabified_text:
                untabified_newer_index = LinkParseHelper.__translate_between_strings(
                    tabified_text, source_text, newer_index
                )
                POGGER.debug("untabified_newer_index>:$:<", untabified_newer_index)
                newer_index = untabified_newer_index

            assert did_use_angle_start is not None
            if ParserHelper.is_character_at_index(
                source_text, newer_index, LinkParseHelper.__link_format_inline_end
            ):
                newer_index += 1
            else:
                newer_index = -1
        else:
            did_use_angle_start = False
        return newer_index, did_use_angle_start

    @staticmethod
    def look_for_link_formats(
        source_text: str,
        new_index: int,
        text_from_blocks: str,
        tabified_text: Optional[str],
    ) -> Tuple[int, bool, LinkHelperProperties,]:
        """
        Look for links in the various formats.
        """
        (
            update_index,
            tried_full_reference_form,
        ) = (-1, False)
        lhp: LinkHelperProperties = LinkHelperProperties()
        lhp.did_use_angle_start = False
        lhp.bounding_character = ""
        lhp.label_type = ""
        lhp.inline_link = ""
        lhp.pre_inline_link = ""
        lhp.inline_title = ""
        lhp.pre_inline_title = ""
        lhp.ex_label = ""
        lhp.before_link_whitespace = ""
        lhp.before_title_whitespace = ""
        lhp.after_title_whitespace = ""
        if ParserHelper.is_character_at_index(
            source_text, new_index, LinkParseHelper.__link_format_inline_start
        ):
            POGGER.debug("inline reference? >>$>>", new_index)
            update_index = LinkParseHelper.__process_inline_link_body(
                source_text, new_index, tabified_text, lhp
            )
            lhp.label_type = Constants.link_type__inline
        elif ParserHelper.is_character_at_index(
            source_text, new_index, LinkParseHelper.__link_format_reference_start
        ):
            (
                lhp.label_type,
                tried_full_reference_form,
                update_index,
                lhp.inline_link,
                lhp.inline_title,
                lhp.ex_label,
            ) = LinkParseHelper.__try_to_find_link_match(
                new_index, source_text, text_from_blocks, tabified_text
            )
        POGGER.debug("__look_for_link_formats>>update_index>>$>>", update_index)
        return (
            update_index,
            tried_full_reference_form,
            lhp,
        )
