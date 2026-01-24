"""
Module to handle the processing of configuration for the application.
"""

import argparse
import logging
from typing import Callable, Optional

from application_properties import ApplicationProperties
from application_properties.multisource_configuration_loader import (
    ConfigurationFileType,
    MultisourceConfigurationLoader,
    MultisourceConfigurationLoaderOptions,
)

LOGGER = logging.getLogger(__name__)


# pylint: disable=too-few-public-methods
class ApplicationConfigurationHelper:
    """
    Class to handle the processing of configuration for the application.
    """

    __pyproject_section_header = "tool.pymarkdown"
    __default_configuration_file = ".pymarkdown"

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

        options = MultisourceConfigurationLoaderOptions(
            load_json_files_as_json5=args.use_json5_for_configuration,
            section_header_if_toml=ApplicationConfigurationHelper.__pyproject_section_header,
        )
        loader = MultisourceConfigurationLoader(options)
        loader.add_local_pyproject_toml_file(
            ApplicationConfigurationHelper.__pyproject_section_header
        )
        loader.add_local_project_configuration_file(
            ApplicationConfigurationHelper.__default_configuration_file,
            ConfigurationFileType.JSON,
            [ConfigurationFileType.YAML, ConfigurationFileType.YML],
        )
        if args.configuration_file:
            loader.add_specified_configuration_file(
                args.configuration_file, ConfigurationFileType.NONE
            )
        loader.add_manually_set_properties(args.set_configuration)
        loader.process(properties, handle_error)

        if args.strict_configuration or properties.get_boolean_property(
            "mode.strict-config", strict_mode=True
        ):
            properties.enable_strict_mode()


# pylint: enable=too-few-public-methods
