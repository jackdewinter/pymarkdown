"""
Module to allow for a critical error within a plugin to be encapsulated
    and reported.
"""

from typing import Optional

from pymarkdown.markdown_token import MarkdownToken
from pymarkdown.parser_helper import ParserHelper


class BadPluginError(Exception):
    """
    Class to allow for a critical error within a plugin to be encapsulated
    and reported.
    """

    # pylint: disable=too-many-arguments
    def __init__(
        self,
        plugin_id: Optional[str] = None,
        plugin_action: Optional[str] = None,
        file_name: Optional[str] = None,
        class_name: Optional[str] = None,
        field_name: Optional[str] = None,
        is_constructor: bool = False,
        is_empty: bool = False,
        formatted_message: Optional[str] = None,
        line_number: int = 0,
        column_number: int = 0,
        actual_line: Optional[str] = None,
        actual_token: Optional[MarkdownToken] = None,
        cause: Optional[Exception] = None,
    ) -> None:

        if not formatted_message:
            if file_name:
                formatted_message = BadPluginError.__create_file_name_message(
                    file_name, class_name, is_constructor
                )
            elif class_name:
                formatted_message = BadPluginError.__create_class_name_message(
                    class_name, field_name, is_empty
                )
            else:
                formatted_message = BadPluginError.__create_exception_message(
                    cause, plugin_id, plugin_action
                )

            formatted_message = BadPluginError.__add_suffix(
                formatted_message, actual_line, actual_token, line_number, column_number
            )
        super().__init__(formatted_message)

    # pylint: enable=too-many-arguments

    @staticmethod
    def __create_file_name_message(
        file_name: Optional[str], class_name: Optional[str], is_constructor: bool
    ) -> str:
        if class_name:
            return (
                f"Plugin file named '{file_name}' threw an exception in the constructor for the class '{class_name}'."
                if is_constructor
                else f"Plugin file named '{file_name}' does not contain a class named '{class_name}'."
            )

        return f"Plugin file named '{file_name}' cannot be loaded."

    @staticmethod
    def __create_class_name_message(
        class_name: Optional[str], field_name: Optional[str], is_empty: bool
    ) -> str:
        if field_name:
            return (
                f"Plugin class '{class_name}' returned an empty value for field name '{field_name}'."
                if is_empty
                else f"Plugin class '{class_name}' returned an improperly typed value for field name '{field_name}'."
            )
        return f"Plugin class '{class_name}' had a critical failure loading the plugin details."

    @staticmethod
    def __create_exception_message(
        cause: Optional[Exception],
        plugin_id: Optional[str],
        plugin_action: Optional[str],
    ) -> str:
        if cause and isinstance(cause, ValueError):
            return str(cause)
        assert plugin_id
        return f"Plugin id '{plugin_id.upper()}' had a critical failure during the '{plugin_action}' action."

    @staticmethod
    def __add_suffix(
        formatted_message: str,
        actual_line: Optional[str],
        actual_token: Optional[MarkdownToken],
        line_number: int,
        column_number: int,
    ) -> str:
        if line_number:
            position_message = (
                f"({line_number},{column_number})"
                if column_number
                else f"(Line {line_number})"
            )
            formatted_message = f"{position_message}: {formatted_message}"
        if actual_line:
            formatted_message = f"{formatted_message}\nActual Line: {actual_line}"
        if actual_token:
            formatted_message = f"{formatted_message}\nActual Token: {ParserHelper.make_value_visible(actual_token)}"
        return formatted_message
