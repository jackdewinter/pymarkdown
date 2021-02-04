"""
Module to provide for a simple logger wrapper that provides extra
functionality for logging parsing information.
"""
from logging import DEBUG, INFO

from pymarkdown.parser_helper import ParserHelper


class ParserLogger:
    """
    Class to provide for a simple logger wrapper that provides extra
    functionality for logging parsing information.
    """

    def __init__(self, my_logger):
        self.__my_logger = my_logger

    def info(self, log_format, *args):
        """
        Log information at an "INFO" level to the logger.
        """
        if self.__my_logger.isEnabledFor(INFO):
            msg = self.__munge(False, log_format, args)
            self.__my_logger.info(msg, stacklevel=2)

    def debug(self, log_format, *args):
        """
        Log information at a "DEBUG" level to the logger.
        """
        if self.__my_logger.isEnabledFor(DEBUG):
            msg = self.__munge(False, log_format, args)
            self.__my_logger.debug(msg, stacklevel=2)

    def debug_with_visible_whitespace(self, log_format, *args):
        """
        Log information at a "DEBUG" level to the logger, but replace the
        automatic filtering of any string with make_value_visible to
        using make_whitespace_visible.
        """
        if self.__my_logger.isEnabledFor(DEBUG):
            msg = self.__munge(True, log_format, args)
            self.__my_logger.debug(msg, stacklevel=2)

    def is_enabled_for(self, debug_level):
        """
        Wrapper method for the logger.isEnabledFor method.
        """
        return self.__my_logger.isEnabledFor(debug_level)

    # pylint: disable=consider-using-enumerate
    @classmethod
    def __munge(cls, show_whitespace, log_format, args):
        split_log_format = log_format.split("$")
        split_log_format_length = len(split_log_format)
        args_length = len(args)
        if split_log_format_length != args_length + 1:
            raise Exception(
                "The number of $ substitution characters does not equal the number of arguments in the list."
            )

        recipient_array = [None] * (split_log_format_length + args_length)
        for next_array_index in range(0, len(recipient_array)):
            if next_array_index % 2 == 0:
                recipient_array[next_array_index] = split_log_format[
                    int(next_array_index / 2)
                ]
            else:
                if show_whitespace:
                    recipient_array[
                        next_array_index
                    ] = ParserHelper.make_whitespace_visible(
                        args[int(next_array_index / 2)]
                    )
                else:
                    recipient_array[next_array_index] = ParserHelper.make_value_visible(
                        args[int(next_array_index / 2)]
                    )
        return "".join(recipient_array)

    # pylint: enable=consider-using-enumerate
