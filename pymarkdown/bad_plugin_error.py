"""
Module to allow for a critical error within a plugin to be encapsulated
    and reported.
"""

from pymarkdown.parser_helper import ParserHelper


class BadPluginError(Exception):
    """
    Class to allow for a critical error within a plugin to be encapsulated
    and reported.
    """

    # pylint: disable=too-many-arguments
    def __init__(
        self,
        plugin_id=None,
        plugin_action=None,
        file_name=None,
        class_name=None,
        field_name=None,
        is_constructor=False,
        is_empty=False,
        formatted_message=None,
        line_number=0,
        column_number=0,
        actual_line=None,
        actual_token=None,
        cause=None,
    ):

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
    def __create_file_name_message(file_name, class_name, is_constructor):
        if class_name:
            return (
                f"Plugin file named '{file_name}' threw an exception in the constructor for the class '{class_name}'."
                if is_constructor
                else f"Plugin file named '{file_name}' does not contain a class named '{class_name}'."
            )

        return f"Plugin file named '{file_name}' cannot be loaded."

    @staticmethod
    def __create_class_name_message(class_name, field_name, is_empty):
        if field_name:
            return (
                f"Plugin class '{class_name}' returned an empty value for field name '{field_name}'."
                if is_empty
                else f"Plugin class '{class_name}' returned an improperly typed value for field name '{field_name}'."
            )
        return f"Plugin class '{class_name}' had a critical failure loading the plugin details."

    @staticmethod
    def __create_exception_message(cause, plugin_id, plugin_action):
        if cause and isinstance(cause, ValueError):
            return str(cause)
        return f"Plugin id '{plugin_id.upper()}' had a critical failure during the '{plugin_action}' action."

    @staticmethod
    def __add_suffix(
        formatted_message, actual_line, actual_token, line_number, column_number
    ):
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
