"""
Module to control the return code of the application.
"""

import sys
import threading
from abc import ABC, abstractmethod
from argparse import ArgumentParser, Namespace
from enum import Enum
from typing import Dict

from application_properties import ApplicationProperties
from typing_extensions import override


class ApplicationResult(Enum):
    """
    Enumeration of all possible application results.
    """

    SUCCESS = 0
    NO_FILES_TO_SCAN = 1
    COMMAND_LINE_ERROR = 2
    FIXED_AT_LEAST_ONE_FILE = 3
    SCAN_TRIGGERED_AT_LEAST_ONCE = 4
    SYSTEM_ERROR = 5


class SchemeDefinition(ABC):
    """
    Abstract class for the scheme definitions.
    """

    @abstractmethod
    def get_scheme_mapping(self) -> Dict[ApplicationResult, int]:
        """
        Get the mapping to apply.
        """

    def apply_scheme(self, application_result: ApplicationResult) -> int:
        """
        Apply the scheme to the result to get the return code.
        """
        scheme_mapping = self.get_scheme_mapping()
        return scheme_mapping[application_result]


class DefaultScheme(SchemeDefinition):
    """
    Class to contain the default return code scheme.
    """

    @override
    def get_scheme_mapping(self) -> Dict[ApplicationResult, int]:
        return {
            ApplicationResult.SUCCESS: 0,
            ApplicationResult.NO_FILES_TO_SCAN: 1,
            ApplicationResult.COMMAND_LINE_ERROR: 2,
            ApplicationResult.FIXED_AT_LEAST_ONE_FILE: 3,
            ApplicationResult.SCAN_TRIGGERED_AT_LEAST_ONCE: 1,
            ApplicationResult.SYSTEM_ERROR: 1,
        }


class MinimalScheme(SchemeDefinition):
    """
    Class to contain the minimal return code scheme.
    """

    @override
    def get_scheme_mapping(self) -> Dict[ApplicationResult, int]:
        return {
            ApplicationResult.SUCCESS: 0,
            ApplicationResult.NO_FILES_TO_SCAN: 0,
            ApplicationResult.COMMAND_LINE_ERROR: 2,
            ApplicationResult.FIXED_AT_LEAST_ONE_FILE: 0,
            ApplicationResult.SCAN_TRIGGERED_AT_LEAST_ONCE: 0,
            ApplicationResult.SYSTEM_ERROR: 1,
        }


class ReturnCodeHelper:
    """
    Class to control the return code of the application.
    """

    __DEFAULT_SCHEME_NAME = "default"
    __MINIMAL_SCHEME_NAME = "minimal"

    __available_schemes: Dict[str, SchemeDefinition] = {
        __DEFAULT_SCHEME_NAME: DefaultScheme(),
        __MINIMAL_SCHEME_NAME: MinimalScheme(),
    }
    __helper_name = threading.local()

    @staticmethod
    def add_command_line_arguments(parser: ArgumentParser) -> None:
        """
        Function to add any command line arguments for this to the application.
        """
        parser.add_argument(
            "--return-code-scheme",
            dest="return_code_scheme",
            action="store",
            help="scheme to choose for selecting the application return code",
            type=ReturnCodeHelper.__validate_return_code_scheme,
            choices=list(ReturnCodeHelper.__available_schemes.keys()),
        )

    @staticmethod
    def reset() -> None:
        """
        Reset any mappings to their initial state.  Used to enforce strict mapping
        rules when called from within the same process.
        """
        ReturnCodeHelper.__helper_name.value = None

    @staticmethod
    def set_initial_state(args: Namespace, properties: ApplicationProperties) -> None:
        """
        Set the initial state, including the scheme for the return codes.
        """
        scheme_to_use = args.return_code_scheme
        if scheme_to_use is None:
            scheme_to_use = properties.get_string_property(
                "mode.return_code_scheme",
                strict_mode=True,
                valid_value_fn=ReturnCodeHelper.__validate_return_code_scheme,
            )
        if scheme_to_use is None:
            scheme_to_use = ReturnCodeHelper.__DEFAULT_SCHEME_NAME
        ReturnCodeHelper.__helper_name.value = scheme_to_use

    @staticmethod
    def exit_application(application_result: ApplicationResult) -> None:
        """
        Translate the ApplicationResult and exit the application.
        """
        scheme_name = (
            ReturnCodeHelper.__helper_name.value
            or ReturnCodeHelper.__DEFAULT_SCHEME_NAME
        )
        scheme_class = ReturnCodeHelper.__available_schemes[scheme_name]
        return_code = scheme_class.apply_scheme(application_result)
        sys.exit(return_code)

    @staticmethod
    def __validate_return_code_scheme(argument: str) -> str:
        """
        Function to help argparse limit the valid return code schemes.
        """
        if argument in ReturnCodeHelper.__available_schemes:
            return argument
        raise ValueError(f"Value '{argument}' is not a valid return code scheme.")
