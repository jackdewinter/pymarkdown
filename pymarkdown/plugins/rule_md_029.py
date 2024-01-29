"""
Module to implement a plugin that ensures that Ordered List Items have
consistent numeric prefaces.
"""

from typing import List, Optional, Tuple, cast

from pymarkdown.plugin_manager.plugin_details import PluginDetailsV2
from pymarkdown.plugin_manager.plugin_scan_context import PluginScanContext
from pymarkdown.plugin_manager.rule_plugin import RulePlugin
from pymarkdown.tokens.list_start_markdown_token import ListStartMarkdownToken
from pymarkdown.tokens.markdown_token import MarkdownToken


class RuleMd029(RulePlugin):
    """
    Class to implement a plugin that ensures that Ordered List Items have
    consistent numeric prefaces.
    """

    __one_style = "one"
    __ordered_style = "ordered"
    __zero_style = "zero"
    __one_or_ordered_style = "one_or_ordered"

    __valid_styles = [
        __one_style,
        __ordered_style,
        __zero_style,
        __one_or_ordered_style,
    ]

    def __init__(self) -> None:
        super().__init__()
        self.__style = ""
        self.__list_stack: List[MarkdownToken] = []
        self.__ordered_list_stack: List[Tuple[Optional[str], Optional[int]]] = []

    def get_details(self) -> PluginDetailsV2:
        """
        Get the details for the plugin.
        """
        return PluginDetailsV2(
            plugin_name="ol-prefix",
            plugin_id="MD029",
            plugin_enabled_by_default=True,
            plugin_description="Ordered list item prefix",
            plugin_version="0.5.1",
            plugin_url="https://github.com/jackdewinter/pymarkdown/blob/main/docs/rules/rule_md029.md",
            plugin_configuration="style",
            plugin_supports_fix=True,
        )

    @classmethod
    def __validate_configuration_style(cls, found_value: str) -> None:
        if found_value not in RuleMd029.__valid_styles:
            raise ValueError(f"Allowable values: {RuleMd029.__valid_styles}")

    def initialize_from_config(self) -> None:
        """
        Event to allow the plugin to load configuration information.
        """
        self.__style = self.plugin_configuration.get_string_property(
            "style",
            default_value=RuleMd029.__one_or_ordered_style,
            valid_value_fn=self.__validate_configuration_style,
        )

    def starting_new_file(self) -> None:
        """
        Event that the a new file to be scanned is starting.
        """
        self.__list_stack = []
        self.__ordered_list_stack = []

    def __calculate_match_info(
        self, list_style: str, initial: bool, last_known_number: Optional[int]
    ) -> Tuple[str, int]:
        if list_style == RuleMd029.__ordered_style:
            style = "1/2/3"
            if initial:
                expected_number = 1
            else:
                assert last_known_number is not None
                expected_number = last_known_number + 1
        elif list_style == RuleMd029.__one_style:
            style = "1/1/1"
            expected_number = 1
        else:
            assert list_style == RuleMd029.__zero_style
            style = "0/0/0"
            expected_number = 0
        return style, expected_number

    def __match_first_item(
        self, context: PluginScanContext, token: MarkdownToken
    ) -> Tuple[Optional[str], Optional[int]]:
        list_token = cast(ListStartMarkdownToken, token)
        last_known_number: int = int(list_token.list_start_content)

        list_style: str = self.__style
        if list_style == RuleMd029.__one_or_ordered_style and last_known_number != 1:
            list_style = RuleMd029.__ordered_style

        is_valid = True
        if list_style == RuleMd029.__ordered_style:
            is_valid = last_known_number in {0, 1}
        elif list_style == RuleMd029.__one_style:
            is_valid = last_known_number == 1
        elif list_style == RuleMd029.__zero_style:
            is_valid = last_known_number == 0
        # print(f"list_style={list_style},last_known_number={last_known_number},is_valid={is_valid}")
        if is_valid:
            return list_style, last_known_number

        return self.__report_invalid(
            context, list_token, True, list_style, last_known_number, None
        )

    def __match_non_first_items(
        self,
        context: PluginScanContext,
        token: MarkdownToken,
        list_style: Optional[str],
        last_known_number: Optional[int],
    ) -> Tuple[Optional[str], Optional[int]]:
        if list_style:
            list_token = cast(ListStartMarkdownToken, token)
            new_number: int = int(list_token.list_start_content)

            # print(f"list_style={list_style},last_known_number={last_known_number},new_number={new_number}")
            if list_style == RuleMd029.__one_or_ordered_style:
                list_style = (
                    RuleMd029.__one_style
                    if new_number == 1
                    else RuleMd029.__ordered_style
                )

            is_valid = False
            if list_style == RuleMd029.__one_style:
                is_valid = new_number == 1
            elif list_style == RuleMd029.__zero_style:
                is_valid = new_number == 0
            else:
                assert list_style == RuleMd029.__ordered_style
                assert last_known_number is not None
                is_valid = new_number == last_known_number + 1
            if not is_valid:
                return self.__report_invalid(
                    context,
                    list_token,
                    False,
                    list_style,
                    last_known_number,
                    new_number,
                )
            last_known_number = new_number
        return list_style, last_known_number

    # pylint: disable=too-many-arguments
    def __report_invalid(
        self,
        context: PluginScanContext,
        token: ListStartMarkdownToken,
        initial_match: bool,
        list_style: str,
        last_known_number: Optional[int],
        new_number: Optional[int],
    ) -> Tuple[Optional[str], Optional[int]]:
        style, expected_number = self.__calculate_match_info(
            list_style, initial_match, last_known_number
        )
        actual_number = last_known_number if new_number is None else new_number
        extra_error_information = (
            f"Expected: {expected_number}; Actual: {actual_number}; Style: {style}"
        )
        if context.in_fix_mode:
            self.register_fix_token_request(
                context,
                token,
                "next_token",
                "list_start_content",
                str(expected_number),
            )
            if not initial_match and new_number is not None:
                expected_number_as_string = str(expected_number)
                new_number_as_string = str(new_number)
                if delta := len(expected_number_as_string) - len(new_number_as_string):
                    self.register_fix_token_request(
                        context,
                        token,
                        "next_token",
                        "indent_level",
                        token.indent_level + delta,
                    )
            return list_style, expected_number
        self.report_next_token_error(
            context, token, extra_error_information=extra_error_information
        )
        return (None, None)

    # pylint: enable=too-many-arguments

    def next_token(self, context: PluginScanContext, token: MarkdownToken) -> None:
        """
        Event that a new token is being processed.
        """
        if token.is_list_start:
            self.__list_stack.append(token)
            if token.is_ordered_list_start:
                list_style, last_known_number = self.__match_first_item(context, token)
                self.__ordered_list_stack.append((list_style, last_known_number))
        elif token.is_list_end:
            del self.__list_stack[-1]
            if token.is_ordered_list_end:
                del self.__ordered_list_stack[-1]
        elif token.is_new_list_item and self.__list_stack[-1].is_ordered_list_start:
            list_style, last_known_number = self.__ordered_list_stack[-1]
            list_style, last_known_number = self.__match_non_first_items(
                context, token, list_style, last_known_number
            )
            self.__ordered_list_stack[-1] = (list_style, last_known_number)
