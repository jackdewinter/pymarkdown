"""
Module to provide for a simplified way to setup logging.
"""

import argparse
import logging
import sys
from typing import Optional

from application_properties import ApplicationProperties

LOGGER = logging.getLogger(__name__)


class ApplicationLogging:
    """
    Class to provide for a simplified way to setup logging.
    """

    __log_level_critical = "CRITICAL"
    __log_level_error = "ERROR"
    __log_level_warning = "WARNING"
    __log_level_info = "INFO"
    __log_level_debug = "DEBUG"
    __available_log_maps = {
        __log_level_critical: logging.CRITICAL,
        __log_level_error: logging.ERROR,
        __log_level_warning: logging.WARNING,
        __log_level_info: logging.INFO,
        __log_level_debug: logging.DEBUG,
    }

    def __init__(
        self,
        application_properties: Optional[ApplicationProperties] = None,
        show_stack_trace: bool = False,
        default_log_level: str = __log_level_warning,
    ):
        self.__show_stack_trace = show_stack_trace
        self.__default_log_level = default_log_level
        self.__properties = application_properties
        self.__new_handler: Optional[logging.FileHandler] = None

    @property
    def show_stack_trace(self) -> bool:
        """
        Gets a value indicating whether or not stack tracing was enabled.
        """
        return self.__show_stack_trace

    def pre_initialize_with_args(self, args: argparse.Namespace) -> None:
        """
        Pre-Initialize the logging for the application.  This is done to provide
        logging before any configuration has been initialized and sets logging
        to default values.
        """
        self.pre_initialize(args.show_stack_trace)

    def pre_initialize(self, show_stack_trace: bool = False) -> None:
        """
        Pre-Initialize the logging for the application.  This is done to provide
        logging before any configuration has been initialized and sets logging
        to default values.
        """
        base_logger = logging.getLogger()
        base_logger.setLevel(logging.DEBUG if show_stack_trace else logging.WARNING)

    def initialize(self, args: argparse.Namespace) -> None:
        """
        Initialize the logging for the application.
        """

        try:
            self.__show_stack_trace = args.show_stack_trace
            if not self.__show_stack_trace and self.__properties:
                self.__show_stack_trace = self.__properties.get_boolean_property(
                    "log.stack-trace"
                )

            effective_log_file = args.log_file
            if not effective_log_file and self.__properties:
                effective_log_file = self.__properties.get_string_property("log.file")

            effective_log_level = args.log_level
            if not effective_log_level and self.__properties:
                effective_log_level = self.__properties.get_string_property(
                    "log.level", valid_value_fn=ApplicationLogging.__log_level_type
                )
            if effective_log_level is None:
                effective_log_level = self.__default_log_level

            if effective_log_file:
                self.__new_handler = logging.FileHandler(effective_log_file)
                logging.getLogger().addHandler(self.__new_handler)
            else:
                temp_log_level = (
                    logging.DEBUG if self.__show_stack_trace else logging.CRITICAL
                )
                logging.basicConfig(stream=sys.stdout, level=temp_log_level)

            log_level_to_enact = ApplicationLogging.__available_log_maps[
                effective_log_level
            ]

            logging.getLogger().setLevel(log_level_to_enact)
        except Exception:
            self.terminate()
            raise

    def terminate(self) -> None:
        """
        Terminate the logging for the application.
        """
        if self.__new_handler:
            self.__new_handler.close()
            self.__new_handler = None

    @staticmethod
    def add_default_command_line_arguments(
        parser_to_add_to: argparse.ArgumentParser,
    ) -> None:
        """
        Add a set of default command line arguments to an argparse styled command line.
        """
        parser_to_add_to.add_argument(
            "--stack-trace",
            dest="show_stack_trace",
            action="store_true",
            default=False,
            help="if an error occurs, print out the stack trace for debug purposes",
        )
        parser_to_add_to.add_argument(
            "--log-level",
            dest="log_level",
            action="store",
            help="minimum level required to log messages",
            type=ApplicationLogging.__log_level_type,
            choices=list(ApplicationLogging.__available_log_maps.keys()),
        )
        parser_to_add_to.add_argument(
            "--log-file",
            dest="log_file",
            action="store",
            help="destination file for log messages",
        )

    @staticmethod
    def __log_level_type(argument: str) -> str:
        """
        Function to help argparse limit the valid log levels.
        """
        if argument in ApplicationLogging.__available_log_maps:
            return argument
        raise ValueError(f"Value '{argument}' is not a valid log level.")
