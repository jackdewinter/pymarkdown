"""
Module to implement a plugin that ensures that a mandates set of headers are present.
"""

from typing import List, Optional, Tuple, Union, cast

from pymarkdown.general.parser_helper import ParserHelper
from pymarkdown.plugin_manager.plugin_details import PluginDetails
from pymarkdown.plugin_manager.plugin_scan_context import PluginScanContext
from pymarkdown.plugin_manager.rule_plugin import RulePlugin
from pymarkdown.tokens.atx_heading_markdown_token import AtxHeadingMarkdownToken
from pymarkdown.tokens.markdown_token import MarkdownToken
from pymarkdown.tokens.text_markdown_token import TextMarkdownToken


class RuleMd043(RulePlugin):
    """
    Class to implement a plugin that ensures that a mandates set of headers are present.
    """

    def __init__(self) -> None:
        super().__init__()
        # self.__show_debug = False
        self.__collected_tokens: List[MarkdownToken] = []
        self.__all_tokens: List[List[MarkdownToken]] = []
        self.__headings_have_wildcards: bool = False
        self.__compiled_headings: List[Union[str, Tuple[int, str]]] = []
        self.__prefix_index: int = -1
        self.__suffix_index: int = -1

    def get_details(self) -> PluginDetails:
        """
        Get the details for the plugin.
        """
        return PluginDetails(
            plugin_name="required-headings,required-headers",
            plugin_id="MD043",
            plugin_enabled_by_default=True,
            plugin_description="Required heading structure",
            plugin_version="0.5.0",
            plugin_interface_version=1,
            plugin_url="https://github.com/jackdewinter/pymarkdown/blob/main/docs/rules/rule_md043.md",
            plugin_configuration="headings",
        )

    @classmethod
    def __validate_heading_pattern(cls, found_value: str) -> None:
        if found_value.strip(" "):
            _, _, compile_error = cls.__compile(found_value)
            if compile_error:
                raise ValueError(f"Heading format not valid: {compile_error}")

    @classmethod
    def __compile(
        cls, found_value: str
    ) -> Tuple[List[Union[str, Tuple[int, str]]], bool, Optional[str]]:
        found_parts = found_value.split(",")
        compiled_lines: List[Union[str, Tuple[int, str]]] = []
        are_any_wildcards = False
        for next_part in found_parts:
            next_part = next_part.strip(" ")
            if next_part == "*":
                if compiled_lines and compiled_lines[-1] == "*":
                    return (
                        [],
                        False,
                        "Two wildcard elements cannot be next to each other.",
                    )
                compiled_lines.append(next_part)
                are_any_wildcards = True
            else:
                count, new_index = ParserHelper.collect_while_character(
                    next_part, 0, "#"
                )
                if not count:
                    return [], False, "Element must start with hash characters (#)."
                if count > 6:
                    return (
                        [],
                        False,
                        "Element must start with between 1 and 6 hash characters (#).",
                    )
                assert next_part is not None
                assert new_index is not None
                new_index, extracted_whitespace = ParserHelper.extract_ascii_whitespace(
                    next_part, new_index
                )
                if not extracted_whitespace or len(extracted_whitespace) != 1:
                    return (
                        [],
                        False,
                        "Element must have exactly one space character and one non-space character after any hash characters (#).",
                    )
                compiled_lines.append((count, next_part[new_index:]))
        return compiled_lines, are_any_wildcards, None

    def initialize_from_config(self) -> None:
        """
        Event to allow the plugin to load configuration information.
        """
        raw_headings = self.plugin_configuration.get_string_property(
            "headings",
            default_value="",
            valid_value_fn=self.__validate_heading_pattern,
        )
        self.__compiled_headings = []
        self.__headings_have_wildcards = False
        if raw_headings:
            (
                self.__compiled_headings,
                self.__headings_have_wildcards,
                _,
            ) = self.__compile(raw_headings)
        if self.__headings_have_wildcards:
            self.__prefix_index = -1
            heading_index = 0
            while (
                heading_index < len(self.__compiled_headings)
                and self.__prefix_index == -1
            ):
                heading_contents = self.__compiled_headings[heading_index]
                if heading_contents == "*":
                    self.__prefix_index = heading_index
                else:
                    heading_index += 1

            self.__suffix_index = -1
            heading_index = len(self.__compiled_headings) - 1
            while heading_index >= 0 and self.__suffix_index == -1:
                heading_contents = self.__compiled_headings[heading_index]
                if heading_contents == "*":
                    self.__suffix_index = heading_index + 1
                else:
                    heading_index -= 1

    def __verify_single_heading_match_atx(
        self, matching_all_token_index: int, hash_count: int, expected_text: str
    ) -> Tuple[Optional[MarkdownToken], Optional[str]]:
        failure_token, failure_reason = (None, None)

        these_tokens = self.__all_tokens[matching_all_token_index]
        atx_token = cast(AtxHeadingMarkdownToken, these_tokens[0])
        if atx_token.hash_count != hash_count:
            failure_reason = f"Bad heading level: Expected: {hash_count}, Actual: {atx_token.hash_count}"
        elif len(these_tokens) != 2 or not these_tokens[1].is_text:
            failure_reason = "Bad heading: Required headings must only be normal text."
        else:
            text_token = cast(TextMarkdownToken, these_tokens[1])
            if text_token.token_text != expected_text:
                failure_reason = f"Bad heading text: Expected: {expected_text}, Actual: {text_token.token_text}"
        if failure_reason:
            failure_token = these_tokens[0]
        return failure_token, failure_reason

    def __verify_single_heading_match(
        self,
        this_compiled_heading: Union[str, Tuple[int, str]],
        matching_all_token_index: int,
    ) -> Tuple[Optional[MarkdownToken], Optional[str]]:
        failure_token, failure_reason = (None, None)

        assert len(this_compiled_heading) == 2
        this_heading = cast(Tuple[int, str], this_compiled_heading)
        hash_count: int = this_heading[0]
        expected_text: str = this_heading[1]
        if matching_all_token_index >= len(self.__all_tokens):
            failure_token = self.__all_tokens[-1][0]
            failure_reason = f"Missing heading: {ParserHelper.repeat_string('#', hash_count)} {expected_text}"
        else:
            failure_token, failure_reason = self.__verify_single_heading_match_atx(
                matching_all_token_index, hash_count, expected_text
            )
        return failure_token, failure_reason

    def __verify_group_heading_match(
        self, heading_index: int, all_token_index: int, scan_limit: int = -1
    ) -> Tuple[int, int, Optional[MarkdownToken], Optional[str]]:
        if scan_limit < 0:
            scan_limit = len(self.__compiled_headings)

        failure_token, failure_reason = (None, None)
        # if self.__show_debug:
        #     print(
        #         "vghm:heading_index="
        #         + str(heading_index)
        #         + ",len="
        #         + str(len(self.__compiled_headings))
        #         + ",scan_limit="
        #         + str(scan_limit)
        #     )
        while (
            not failure_token
            and heading_index < len(self.__compiled_headings)
            and heading_index < scan_limit
        ):
            this_compiled_heading: Union[str, Tuple[int, str]] = (
                self.__compiled_headings[heading_index]
            )
            # if self.__show_debug:
            #     print(
            #         "vghm:this_compiled_heading="
            #         + str(this_compiled_heading)
            #         + ",all_token_index="
            #         + str(all_token_index)
            #     )
            failure_token, failure_reason = self.__verify_single_heading_match(
                this_compiled_heading, all_token_index
            )
            # if self.__show_debug:
            #     print(
            #         "vghm:failure_token="
            #         + str(failure_token)
            #         + ",failure_reason="
            #         + str(failure_reason)
            #     )
            if not failure_token:
                heading_index += 1
                all_token_index += 1
        return heading_index, all_token_index, failure_token, failure_reason

    def __handle_no_wildcards_match(self, context: PluginScanContext) -> None:
        end_index, _, failure_token, failure_reason = self.__verify_group_heading_match(
            0, 0
        )
        if failure_token:
            self.report_next_token_error(
                context, failure_token, extra_error_information=failure_reason
            )
        elif end_index < len(self.__all_tokens):
            anchor_token = self.__all_tokens[end_index][0]
            self.report_next_token_error(
                context, anchor_token, extra_error_information="Extra heading"
            )

    def __handle_wildcard_prefix(
        self,
    ) -> Tuple[int, int, Optional[MarkdownToken], Optional[str]]:
        (
            top_heading_index,
            top_token_index,
            failure_token,
            failure_reason,
        ) = self.__verify_group_heading_match(0, 0, scan_limit=self.__prefix_index)
        # if self.__show_debug:
        #     print(
        #         "top_heading_index="
        #         + str(top_heading_index)
        #         + ",top_token_index="
        #         + str(top_token_index)
        #         + ",failed_xx="
        #         + str(failure_reason)
        #     )
        return top_heading_index, top_token_index, failure_token, failure_reason

    def __handle_wildcard_suffix(
        self, top_token_index: int
    ) -> Tuple[int, int, Optional[MarkdownToken], Optional[str]]:
        bottom_heading_index = len(self.__compiled_headings)
        bottom_token_index = len(self.__all_tokens)

        start_all_token_index = len(self.__all_tokens) - (
            len(self.__compiled_headings) - self.__suffix_index
        )
        # if self.__show_debug:
        #     print(
        #         "start_all_token_index="
        #         + str(start_all_token_index)
        #         + ",top_token_index="
        #         + str(top_token_index)
        #     )
        if start_all_token_index < top_token_index:
            failure_token: Optional[MarkdownToken] = self.__all_tokens[-1][0]
            failure_reason: Optional[str] = "Overlapped."
        else:
            (
                _,
                _,
                failure_token,
                failure_reason,
            ) = self.__verify_group_heading_match(
                self.__suffix_index, start_all_token_index
            )
            # if self.__show_debug:
            #     print(
            #         "bottom_suffix_index="
            #         + str(bottom_suffix_index)
            #         + ",bottom_all_token_index="
            #         + str(bottom_all_token_index)
            #         + ",failure_reason="
            #         + str(failure_reason)
            #     )
            bottom_heading_index = self.__suffix_index
            bottom_token_index = start_all_token_index
        return bottom_heading_index, bottom_token_index, failure_token, failure_reason

    def starting_new_file(self) -> None:
        """
        Event that the a new file to be scanned is starting.
        """
        self.__collected_tokens = []
        self.__all_tokens = []

    def __do_recursive(
        self,
        remaining_headings: List[Union[str, Tuple[int, str]]],
        top_heading_index: int,
        remaining_tokens: List[List[MarkdownToken]],
        top_token_index: int,
    ) -> bool:
        bottom_heading_index = top_heading_index + len(remaining_headings)

        # if self.__show_debug:
        #     print(
        #         "remaining_headings:"
        #         + str(remaining_headings)
        #         + ",top="
        #         + str(top_heading_index)
        #         + ",bottom="
        #         + str(bottom_heading_index)
        #     )
        #     print(
        #         "remaining_tokens:"
        #         + str(remaining_tokens)
        #         + ",index="
        #         + str(top_token_index)
        #     )
        assert remaining_headings[0] == "*" and remaining_headings[-1] == "*"
        start_index = 1
        end_index = 2
        while remaining_headings[end_index] != "*":
            end_index += 1
        delta = end_index - start_index
        # if self.__show_debug:
        #     print(
        #         "start_index="
        #         + str(start_index)
        #         + ",end_index="
        #         + str(end_index)
        #         + ",delta="
        #         + str(delta)
        #     )
        #     print("headings:" + str(remaining_headings[start_index:end_index]))
        search_index = 0
        heading_index = top_heading_index + 1
        scan_limit = top_heading_index + 1 + delta
        found_match = False
        while search_index < len(remaining_headings) and search_index < len(
            remaining_tokens
        ):
            found_match, search_index = self.__do_recursive_loop(
                heading_index,
                top_token_index,
                search_index,
                scan_limit,
                bottom_heading_index,
                top_heading_index,
                remaining_tokens,
                remaining_headings,
            )
            if found_match:
                break
        return found_match

    # pylint: disable=too-many-arguments
    def __do_recursive_loop(
        self,
        heading_index: int,
        top_token_index: int,
        search_index: int,
        scan_limit: int,
        bottom_heading_index: int,
        top_heading_index: int,
        remaining_tokens: List[List[MarkdownToken]],
        remaining_headings: List[Union[str, Tuple[int, str]]],
    ) -> Tuple[bool, int]:
        (
            end_heading_index,
            end_token_index,
            failure_token,
            _,
        ) = self.__verify_group_heading_match(
            heading_index, top_token_index + search_index, scan_limit=scan_limit
        )
        # if self.__show_debug:
        #     print(str((end_heading_index, end_token_index, failure_token)))
        found_match = False
        if not failure_token and end_heading_index < len(self.__compiled_headings):
            # if self.__show_debug:
            #     print(
            #         "FOUND:"
            #         + str((end_heading_index, end_token_index, failure_token))
            #     )
            if end_heading_index == bottom_heading_index - 1:
                # if self.__show_debug:
                #     print("done")
                found_match = True
            else:
                found_match = self.__prepare_and_do_recurse(
                    end_heading_index,
                    top_heading_index,
                    end_token_index,
                    top_token_index,
                    remaining_headings,
                    remaining_tokens,
                )
                # if self.__show_debug:
                #     print("found_match=" + str(found_match))
        if not found_match:
            search_index += 1
        return found_match, search_index

    # pylint: enable=too-many-arguments

    # pylint: disable=too-many-arguments
    def __prepare_and_do_recurse(
        self,
        end_heading_index: int,
        top_heading_index: int,
        end_token_index: int,
        top_token_index: int,
        remaining_headings: List[Union[str, Tuple[int, str]]],
        remaining_tokens: List[List[MarkdownToken]],
    ) -> bool:
        new_top_heading_index = end_heading_index
        new_remaining_headings = remaining_headings[
            (end_heading_index - top_heading_index) :
        ]

        new_remaining_tokens = remaining_tokens[(end_token_index - top_token_index) :]
        new_top_token_index = end_token_index

        return self.__do_recursive(
            new_remaining_headings,
            new_top_heading_index,
            new_remaining_tokens,
            new_top_token_index,
        )

    # pylint: enable=too-many-arguments

    def completed_file(self, context: PluginScanContext) -> None:
        """
        Event that the file being currently scanned is now completed.
        """
        if not self.__compiled_headings:
            return

        # if self.__show_debug:
        #     print("self.__compiled_headings>" + str(self.__compiled_headings))
        #     print("self.__all_tokens>" + str(self.__all_tokens))
        failure_token = None

        if not self.__headings_have_wildcards:
            self.__handle_no_wildcards_match(context)
            return

        # if self.__show_debug:
        #     print(
        #         "__prefix_index="
        #         + str(self.__prefix_index)
        #         + ",__suffix_index="
        #         + str(self.__suffix_index)
        #         + ",len="
        #         + str(len(self.__compiled_headings))
        #     )
        top_heading_index = 0
        top_token_index = 0
        bottom_heading_index = len(self.__compiled_headings)
        bottom_token_index = len(self.__all_tokens)
        if self.__prefix_index != 0:
            (
                top_heading_index,
                top_token_index,
                failure_token,
                _,
            ) = self.__handle_wildcard_prefix()
        if not failure_token and self.__suffix_index != len(self.__compiled_headings):
            (
                bottom_heading_index,
                bottom_token_index,
                failure_token,
                _,
            ) = self.__handle_wildcard_suffix(top_token_index)
        if not failure_token:
            remaining_headings = self.__compiled_headings[
                top_heading_index:bottom_heading_index
            ]
            remaining_tokens = self.__all_tokens[top_token_index:bottom_token_index]
            # if self.__show_debug:
            #     print(
            #         "top_index="
            #         + str(top_heading_index)
            #         + ",bottom_index="
            #         + str(bottom_heading_index)
            #         + ",remaining_headings="
            #         + str(remaining_headings)
            #     )
            #     print(
            #         "top_token_index="
            #         + str(top_token_index)
            #         + ",bottom_token_index="
            #         + str(bottom_token_index)
            #         + ",remaining_tokens="
            #         + str(remaining_tokens)
            #     )
            if len(remaining_headings) != 1:
                recurse_result = self.__do_recursive(
                    remaining_headings,
                    top_heading_index,
                    remaining_tokens,
                    top_token_index,
                )
                if not recurse_result:
                    self.report_next_token_error(
                        context,
                        remaining_tokens[0][0],
                        extra_error_information="Multiple wildcard matching failed.",
                    )
        if failure_token:
            self.report_next_token_error(
                context,
                failure_token,
                extra_error_information="Wildcard heading match failed.",
            )

    def next_token(self, context: PluginScanContext, token: MarkdownToken) -> None:
        """
        Event that a new token is being processed.
        """
        _ = context

        if self.__collected_tokens:
            if token.is_atx_heading_end or token.is_setext_heading_end:
                self.__all_tokens.append(self.__collected_tokens)
                self.__collected_tokens = []
            else:
                self.__collected_tokens.append(token)
        elif self.__compiled_headings:
            if token.is_atx_heading or token.is_setext_heading:
                self.__collected_tokens = [token]
