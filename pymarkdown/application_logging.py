"""
Module to provide for a simplified way to setup logging.
"""

import argparse
import logging
import sys
from typing import List, Optional, Tuple

from application_properties import ApplicationProperties

LOGGER = logging.getLogger(__name__)


class ApplicationLogging:
    """
    Class to provide for a simplified way to setup logging.
    """

    log_level_critical = "CRITICAL"
    log_level_error = "ERROR"
    log_level_warning = "WARNING"
    log_level_info = "INFO"
    log_level_debug = "DEBUG"
    __available_log_maps = {
        log_level_critical: logging.CRITICAL,
        log_level_error: logging.ERROR,
        log_level_warning: logging.WARNING,
        log_level_info: logging.INFO,
        log_level_debug: logging.DEBUG,
    }

    def __init__(
        self,
        application_properties: Optional[ApplicationProperties] = None,
        show_stack_trace: bool = False,
        default_log_level: str = log_level_warning,
    ):
        self.__show_stack_trace = show_stack_trace
        self.__default_log_level = default_log_level
        self.__properties = application_properties
        self.__new_handler: Optional[logging.FileHandler] = None

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
        self.__show_stack_trace = show_stack_trace
        base_logger = logging.getLogger()
        base_logger.setLevel(logging.DEBUG if show_stack_trace else logging.WARNING)

    def __calculate_effective_levels(
        self, args: argparse.Namespace
    ) -> Tuple[str, Optional[str]]:
        effective_log_file = args.log_file
        if not effective_log_file and self.__properties:
            effective_log_file = self.__properties.get_string_property("log.file")

        effective_log_level = args.log_level
        if not effective_log_level and self.__properties:
            effective_log_level = self.__properties.get_string_property(
                "log.level",
                valid_value_fn=ApplicationLogging.validate_log_level_type,
            )
        if effective_log_level is None:
            effective_log_level = self.__default_log_level

        return effective_log_level, effective_log_file

    def initialize(self, args: argparse.Namespace) -> None:
        """
        Initialize the logging for the application.
        """

        try:
            effective_log_level, effective_log_file = self.__calculate_effective_levels(
                args
            )

            if effective_log_file:
                self.__new_handler = logging.FileHandler(effective_log_file)
                formatter = logging.Formatter("%(levelname)s %(asctime)s %(message)s")
                self.__new_handler.setFormatter(formatter)
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
        except ValueError:
            raise
        except Exception as this_exception:
            self.terminate()
            raise ApplicationLoggingException(
                "Failure initializing logging subsystem."
            ) from this_exception

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
            "--log-level",
            dest="log_level",
            action="store",
            help="minimum level required to log messages",
            type=ApplicationLogging.validate_log_level_type,
            choices=list(ApplicationLogging.__available_log_maps.keys()),
        )
        parser_to_add_to.add_argument(
            "--log-file",
            dest="log_file",
            action="store",
            help="destination file for log messages",
        )

    @staticmethod
    def get_valid_log_levels() -> List[str]:
        """
        Return a sorted list of the available log levels as strings.
        """
        return list(ApplicationLogging.__available_log_maps.keys())

    @staticmethod
    def is_valid_log_level_type(argument: str) -> bool:
        """
        Check to see if the supplied arguments is a valid log level.
        """
        try:
            ApplicationLogging.validate_log_level_type(argument)
            return True
        except ValueError:
            return False

    @staticmethod
    def validate_log_level_type(argument: str) -> str:
        """
        Function to help argparse limit the valid log levels.
        """
        if argument in ApplicationLogging.__available_log_maps:
            return argument
        raise ValueError(f"Value '{argument}' is not a valid log level.")

    @staticmethod
    def translate_log_level(value: str) -> int:
        """
        Translate a log string, such as "DEBUG" into the logging system's
        numeric values.
        """
        if value not in ApplicationLogging.__available_log_maps:
            return logging.NOTSET
        return ApplicationLogging.__available_log_maps[value]


class ApplicationLoggingException(Exception):
    """
    Class to provide for a specific
    """
