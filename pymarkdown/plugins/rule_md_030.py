"""
Module to implement a plugin that ensures consistent spacing after the list markers.
"""
from pymarkdown.plugin_manager import Plugin, PluginDetails


# pylint: disable=too-many-instance-attributes
class RuleMd030(Plugin):
    """
    Class to implement a plugin that ensures consistent spacing after the list markers.
    """

    def __init__(self):
        super().__init__()
        self.__debug = False
        self.__ul_single = None
        self.__ul_multi = None
        self.__ol_single = None
        self.__ol_multi = None
        self.__list_stack = None
        self.__last_non_end_token = None
        self.__list_tokens = None

    def get_details(self):
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
    def __validate_minimum(cls, found_value):
        if found_value < 1:
            raise ValueError("Allowable values are any integer greater than 0.")

    def initialize_from_config(self):
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

    def starting_new_file(self):
        """
        Event that the a new file to be scanned is starting.
        """
        self.__list_stack = []
        self.__list_tokens = []
        self.__last_non_end_token = None

    def __is_current_list_multiline(self):
        is_multiline = False
        for token_index, list_token in enumerate(self.__list_tokens[-1]):
            if token_index:
                delta = (
                    list_token.line_number
                    - self.__list_tokens[-1][token_index - 1].line_number
                )
                # if self.__debug:
                #     print(
                #         "delta="
                #         + str(delta)
                #         + ", n->"
                #         + str(list_token.line_number)
                #         + ", n-1->"
                #         + str(self.__list_tokens[-1][token_index - 1].line_number)
                #     )
                if delta > 1:
                    is_multiline = True
                    break
        if not is_multiline:
            delta = (
                self.__last_non_end_token.line_number
                - self.__list_tokens[-1][-1].line_number
            )
            # if self.__debug:
            #     print(
            #         "delta="
            #         + str(delta)
            #         + ", n->"
            #         + str(self.__last_non_end_token.line_number)
            #         + ", n-1->"
            #         + str(self.__list_tokens[-1][-1].line_number)
            #     )
            is_multiline = delta > 1
        return is_multiline

    def __handle_list_end(self, context):
        is_multiline = self.__is_current_list_multiline()
        # if self.__debug:
        #     print("is_multiline=" + str(is_multiline))
        if self.__list_tokens[-1][0].is_ordered_list_start:
            required_spaces = self.__ol_multi if is_multiline else self.__ol_single
        else:
            required_spaces = self.__ul_multi if is_multiline else self.__ul_single
        for _, list_token in enumerate(self.__list_tokens[-1]):
            delta = list_token.indent_level - list_token.column_number
            if self.__list_stack[-1].is_ordered_list_start:
                delta -= len(list_token.list_start_content)
            # if self.__debug:
            #     print("y=" + str(list_token).replace("\n", "\\n"))
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

    def next_token(self, context, token):
        """
        Event that a new token is being processed.
        """
        if token.is_list_start:
            self.__list_stack.append(token)
            self.__list_tokens.append([])
            self.__list_tokens[-1].append(token)
            self.__last_non_end_token = None
        elif token.is_list_end:
            self.__handle_list_end(context)
            del self.__list_stack[-1]
            del self.__list_tokens[-1]
        elif token.is_new_list_item:
            self.__list_tokens[-1].append(token)
            self.__last_non_end_token = None
        elif not token.is_end_token:
            self.__last_non_end_token = token


# pylint: enable=too-many-instance-attributes
