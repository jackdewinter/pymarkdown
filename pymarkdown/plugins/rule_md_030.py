"""
Module to implement a plugin that ensures consistent spacing after the list markers.
"""
from typing import Dict, List, Optional, cast

from pymarkdown.container_markdown_token import ListStartMarkdownToken
from pymarkdown.markdown_token import MarkdownToken
from pymarkdown.plugin_manager.plugin_details import PluginDetails
from pymarkdown.plugin_manager.plugin_scan_context import PluginScanContext
from pymarkdown.plugin_manager.rule_plugin import RulePlugin


# pylint: disable=too-many-instance-attributes
class RuleMd030(RulePlugin):
    """
    Class to implement a plugin that ensures consistent spacing after the list markers.
    """

    def __init__(self) -> None:
        super().__init__()
        # self.__debug = False
        self.__ul_single = None
        self.__ul_multi = None
        self.__ol_single = None
        self.__ol_multi = None
        self.__list_stack: List[MarkdownToken] = []
        self.__list_tokens: List[List[MarkdownToken]] = []
        self.__current_list_parent: Optional[MarkdownToken] = None
        self.__paragraph_count_map: Dict[str, int] = {}

    def get_details(self) -> PluginDetails:
        """
        Get the details for the plugin.
        """
        return PluginDetails(
            plugin_name="list-marker-space",
            plugin_id="MD030",
            plugin_enabled_by_default=True,
            plugin_description="Spaces after list markers",
            plugin_version="0.5.0",
            plugin_interface_version=1,
            plugin_url="https://github.com/jackdewinter/pymarkdown/blob/main/docs/rules/rule_md030.md",
            plugin_configuration="ul_single,ol_single,ul_multi,ol_multi",
        )

    @classmethod
    def __validate_minimum(cls, found_value: int) -> None:
        if found_value < 1:
            raise ValueError("Allowable values are any integer greater than 0.")

    def initialize_from_config(self) -> None:
        """
        Event to allow the plugin to load configuration information.
        """
        self.__ul_single = self.plugin_configuration.get_integer_property(
            "ul_single",
            default_value=1,
            valid_value_fn=self.__validate_minimum,
        )
        self.__ul_multi = self.plugin_configuration.get_integer_property(
            "ul_multi",
            default_value=1,
            valid_value_fn=self.__validate_minimum,
        )
        self.__ol_single = self.plugin_configuration.get_integer_property(
            "ol_single",
            default_value=1,
            valid_value_fn=self.__validate_minimum,
        )
        self.__ol_multi = self.plugin_configuration.get_integer_property(
            "ol_multi",
            default_value=1,
            valid_value_fn=self.__validate_minimum,
        )

    def starting_new_file(self) -> None:
        """
        Event that the a new file to be scanned is starting.
        """
        self.__list_stack = []
        self.__list_tokens = []
        self.__current_list_parent = None
        self.__paragraph_count_map = {}

    def __handle_list_end(self, context: PluginScanContext) -> None:

        for list_token in self.__list_tokens[-1]:
            this_list_token_paragraph_count = 0
            if str(list_token) in self.__paragraph_count_map:
                this_list_token_paragraph_count = self.__paragraph_count_map[
                    str(list_token)
                ]
            if self.__list_tokens[-1][0].is_ordered_list_start:
                required_spaces = (
                    self.__ol_multi
                    if this_list_token_paragraph_count > 1
                    else self.__ol_single
                )
            else:
                required_spaces = (
                    self.__ul_multi
                    if this_list_token_paragraph_count > 1
                    else self.__ul_single
                )
            # if self.__debug:
            #     print(">>" + str(list_token))
            #     print(
            #         ">>"
            #         + str(this_list_token_paragraph_count)
            #         + "..."
            #         + str(required_spaces)
            #     )
            #     print(">>" + str(self.__paragraph_count_map))
            if str(list_token) in self.__paragraph_count_map:
                del self.__paragraph_count_map[str(list_token)]
            # if self.__debug:
            #     print(">>" + str(self.__paragraph_count_map))

            list_start_token = cast(ListStartMarkdownToken, list_token)
            delta = list_start_token.indent_level - list_token.column_number
            if self.__list_stack[-1].is_ordered_list_start:
                delta -= len(list_start_token.list_start_content)
            # if self.__debug:
            #     print("y=" + str(list_token).replace(ParserHelper.newline_character, "\\n"))
            #     print(
            #         "token_index="
            #         + str(token_index)
            #         + "::"
            #         + str(list_token.indent_level)
            #         + ":"
            #         + str(list_token.column_number)
            #     )
            #     print(
            #         "delta=" + str(delta) + ",required_spaces=" + str(required_spaces)
            #     )
            if delta != required_spaces:
                extra_error_information = (
                    f"Expected: {required_spaces}; Actual: {delta}"
                )
                self.report_next_token_error(
                    context, list_token, extra_error_information=extra_error_information
                )

    def next_token(self, context: PluginScanContext, token: MarkdownToken) -> None:
        """
        Event that a new token is being processed.
        """
        # if self.__debug:
        #     print(">>>>" + str(token))
        #     print("parent-->" + str(self.__current_list_parent))
        #     print("paragraph_count_map-->" + str(self.__paragraph_count_map))
        if token.is_list_start:
            self.__list_stack.append(token)
            self.__list_tokens.append([])
            self.__list_tokens[-1].append(token)
            self.__current_list_parent = token
        elif token.is_list_end:
            self.__handle_list_end(context)
            del self.__list_stack[-1]
            del self.__list_tokens[-1]
            self.__current_list_parent = None
            if self.__list_tokens:
                # if self.__debug:
                #     print("__list_stack-->" + str(self.__list_stack))
                #     print("__list_tokens-->" + str(self.__list_tokens))
                self.__current_list_parent = self.__list_tokens[-1][-1]
        elif token.is_new_list_item:
            self.__list_tokens[-1].append(token)
            self.__current_list_parent = token
        elif token.is_paragraph and self.__current_list_parent:
            new_count = (
                self.__paragraph_count_map[str(self.__current_list_parent)]
                if str(self.__current_list_parent) in self.__paragraph_count_map
                else 0
            )
            self.__paragraph_count_map[str(self.__current_list_parent)] = new_count + 1
        # if self.__debug:
        #     print("parent-->" + str(self.__current_list_parent))


# pylint: enable=too-many-instance-attributes
