"""
Module to handle the processing of configuration for the application.
"""

import argparse
import json
import logging
import os
from typing import Callable, Optional

import yaml
from application_properties import (
    ApplicationProperties,
    ApplicationPropertiesJsonLoader,
    ApplicationPropertiesUtilities,
    ApplicationPropertiesYamlLoader,
)

LOGGER = logging.getLogger(__name__)


# pylint: disable=too-few-public-methods
class ApplicationConfigurationHelper:
    """
    Class to handle the processing of configuration for the application.
    """

    __default_configuration_file = ".pymarkdown"
    __default_yaml_configuration_file_extension = ".yaml"
    __other_default_yaml_configuration_file_extension = ".yml"

    @staticmethod
    def apply_configuration_layers(
        args: argparse.Namespace,
        properties: ApplicationProperties,
        handle_error: Callable[[str, Optional[Exception]], None],
    ) -> None:
        """
        Apply any general python configuration files followed by any configuration
        files specific to this project.
        """
        LOGGER.debug("Looking for any standard python configuration files.")
        ApplicationPropertiesUtilities.process_standard_python_configuration_files(
            properties, handle_error
        )

        LOGGER.debug("Looking for application specific configuration files.")
        ApplicationConfigurationHelper.__process_project_specific_json_configuration(
            args,
            properties,
            handle_error,
        )

        if args.strict_configuration or properties.get_boolean_property(
            "mode.strict-config", strict_mode=True
        ):
            properties.enable_strict_mode()

    @staticmethod
    def __process_project_specific_json_configuration(
        args: argparse.Namespace,
        application_properties: ApplicationProperties,
        handle_error_fn: Callable[[str, Optional[Exception]], None],
    ) -> None:
        """
        Load configuration information from JSON configuration files.
        """

        # Look for the default configuration files in the current working directory.
        ApplicationConfigurationHelper.__process_default_configuration_files(
            application_properties, handle_error_fn
        )

        # A configuration file specified on the command line has a higher precedence
        # than anything except a specific setting applied on the command line.
        if args.configuration_file:
            if not os.path.isfile(args.configuration_file):
                handle_error_fn(
                    f"Specified configuration file `{args.configuration_file}` does not exist.",
                    None,
                )

            LOGGER.debug(
                "Determining file type for specified configuration file '%s'.",
                args.configuration_file,
            )
            try:
                with open(args.configuration_file, encoding="utf-8") as infile:
                    json.load(infile)
                did_load_as_json = True
            except json.decoder.JSONDecodeError:
                did_load_as_json = False

            try:
                with open(args.configuration_file, "rb") as infile:
                    loaded_document = yaml.safe_load(infile)
                did_load_as_yaml = not isinstance(loaded_document, str)
            except yaml.MarkedYAMLError:
                did_load_as_yaml = False

            if did_load_as_json:
                LOGGER.debug(
                    "Attempting to load configuration file '%s' as a JSON file.",
                    args.configuration_file,
                )
                ApplicationPropertiesJsonLoader.load_and_set(
                    application_properties,
                    args.configuration_file,
                    handle_error_fn=handle_error_fn,
                    clear_property_map=False,
                    check_for_file_presence=False,
                )
            elif did_load_as_yaml:
                LOGGER.debug(
                    "Attempting to load configuration file '%s' as a YAML file.",
                    args.configuration_file,
                )
                ApplicationPropertiesYamlLoader.load_and_set(
                    application_properties,
                    args.configuration_file,
                    handle_error_fn=handle_error_fn,
                    clear_property_map=False,
                    check_for_file_presence=False,
                )
            else:
                formatted_error = f"Specified configuration file '{args.configuration_file}' was not parseable as a JSON file or a YAML file."
                LOGGER.warning(formatted_error)
                handle_error_fn(formatted_error, None)

        # A specific setting applied on the command line has the highest precedence.
        if args.set_configuration:
            LOGGER.debug(
                "Attempting to set one or more provided manual properties '%s'.",
                args.set_configuration,
            )
            application_properties.set_manual_property(args.set_configuration)

    @staticmethod
    def __process_default_configuration_files(
        application_properties: ApplicationProperties,
        handle_error_fn: Callable[[str, Optional[Exception]], None],
    ) -> None:
        abs_file_name = os.path.abspath(
            ApplicationConfigurationHelper.__default_configuration_file
        )
        LOGGER.debug(
            "Attempting to find/load '%s' as a default JSON configuration file.",
            abs_file_name,
        )
        (
            did_apply_map,
            did_have_one_error,
        ) = ApplicationPropertiesJsonLoader.load_and_set(
            application_properties,
            abs_file_name,
            handle_error_fn=handle_error_fn,
            clear_property_map=False,
            check_for_file_presence=True,
        )
        if not did_apply_map and not did_have_one_error:
            new_file_name = (
                abs_file_name
                + ApplicationConfigurationHelper.__default_yaml_configuration_file_extension
            )
            LOGGER.debug(
                "Attempting to find/load '%s' as a default YAML configuration file.",
                new_file_name,
            )
            (
                did_apply_map,
                did_have_one_error,
            ) = ApplicationPropertiesYamlLoader.load_and_set(
                application_properties,
                new_file_name,
                handle_error_fn=handle_error_fn,
                clear_property_map=False,
                check_for_file_presence=True,
            )
        if not did_apply_map and not did_have_one_error:
            new_file_name = (
                abs_file_name
                + ApplicationConfigurationHelper.__other_default_yaml_configuration_file_extension
            )
            LOGGER.debug(
                "Attempting to find/load '%s' as a default YAML configuration file.",
                new_file_name,
            )
            (
                did_apply_map,
                did_have_one_error,
            ) = ApplicationPropertiesYamlLoader.load_and_set(
                application_properties,
                new_file_name,
                handle_error_fn=handle_error_fn,
                clear_property_map=False,
                check_for_file_presence=True,
            )
        if not did_apply_map:
            LOGGER.debug("No default configuration files were loaded.")


# pylint: enable=too-few-public-methods
