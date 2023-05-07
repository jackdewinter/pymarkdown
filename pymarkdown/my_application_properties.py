"""
Module to provide a proving ground before moving into ApplicationProperties.
"""

import argparse
import os
from argparse import ArgumentParser
from typing import Callable, Optional

from application_properties import (
    ApplicationProperties,
    ApplicationPropertiesJsonLoader,
    ApplicationPropertiesTomlLoader,
)


class MyApplicationProperties:
    """
    Class to provide a proving ground before moving into ApplicationProperties.
    """

    __pyproject_toml_file = "pyproject.toml"
    __pyproject_section_header = "tool.pymarkdown"

    @staticmethod
    def add_default_command_line_arguments(parser: ArgumentParser) -> None:
        """
        Add command line arguments usually used with the application_properties package.
        """

        parser.add_argument(
            "--config",
            "-c",
            dest="configuration_file",
            action="store",
            default=None,
            help="path to the configuration file to use",
        )
        parser.add_argument(
            "--set",
            "-s",
            dest="set_configuration",
            action="append",
            default=None,
            help="manually set an individual configuration property",
            type=ApplicationProperties.verify_manual_property_form,
        )
        parser.add_argument(
            "--strict-config",
            dest="strict_configuration",
            action="store_true",
            default=False,
            help="throw an error if configuration is bad, instead of assuming default",
        )

    @staticmethod
    def process_standard_python_configuration_files(
        application_properties: ApplicationProperties,
        handle_error_fn: Optional[Callable[[str, Optional[Exception]], None]] = None,
    ) -> None:
        """
        Load configuration information from standard Python project files.
        """

        # Currently, we only support the pyproject.toml file.
        project_configuration_file = os.path.abspath(
            MyApplicationProperties.__pyproject_toml_file
        )
        ApplicationPropertiesTomlLoader.load_and_set(
            application_properties,
            project_configuration_file,
            MyApplicationProperties.__pyproject_section_header,
            handle_error_fn,
            clear_property_map=False,
            check_for_file_presence=True,
        )

    @staticmethod
    def process_project_specific_json_configuration(
        default_configuration_file_name: str,
        args: argparse.Namespace,
        application_properties: ApplicationProperties,
        handle_error_fn: Optional[Callable[[str, Optional[Exception]], None]] = None,
    ) -> None:
        """
        Load configuration information from JSON configuration files.
        """

        # Look for the default configuration file in the current working directory.
        ApplicationPropertiesJsonLoader.load_and_set(
            application_properties,
            os.path.abspath(default_configuration_file_name),
            handle_error_fn,
            clear_property_map=False,
            check_for_file_presence=True,
        )

        # A configuration file specified on the command line has a higher precedence
        # than anything except a specific setting applied on the command line.
        if args.configuration_file:
            ApplicationPropertiesJsonLoader.load_and_set(
                application_properties,
                args.configuration_file,
                handle_error_fn,
                clear_property_map=False,
                check_for_file_presence=False,
            )

        # A specific setting applied on the command line has the highest precedence.
        if args.set_configuration:
            application_properties.set_manual_property(args.set_configuration)
