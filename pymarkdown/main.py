"""
Module to provide for a simple implementation of a title case algorithm.
"""

import argparse
import logging
import os
import runpy
import traceback
from typing import List, Optional, Tuple, cast

from application_properties import ApplicationProperties
from application_properties.application_properties_utilities import (
    ApplicationPropertiesUtilities,
)

from pymarkdown.application_configuration_helper import ApplicationConfigurationHelper
from pymarkdown.application_file_scanner import (
    ApplicationFileScanner,
    ApplicationFileScannerOutputProtocol,
)
from pymarkdown.application_logging import ApplicationLogging
from pymarkdown.extension_manager.extension_manager import ExtensionManager
from pymarkdown.file_scan_helper import FileScanHelper
from pymarkdown.general.bad_tokenization_error import BadTokenizationError
from pymarkdown.general.main_presentation import MainPresentation
from pymarkdown.general.parser_logger import ParserLogger
from pymarkdown.general.tokenized_markdown import TokenizedMarkdown
from pymarkdown.plugin_manager.bad_plugin_error import BadPluginError
from pymarkdown.plugin_manager.plugin_manager import PluginManager
from pymarkdown.return_code_helper import ApplicationResult, ReturnCodeHelper

POGGER = ParserLogger(logging.getLogger(__name__))

LOGGER = logging.getLogger(__name__)


# pylint: disable=too-many-instance-attributes
class PyMarkdownLint:
    """
    Class to provide for a simple implementation of a title case algorithm.
    """

    def __init__(
        self,
        presentation: Optional[MainPresentation] = None,
        show_stack_trace: bool = False,
        inherit_logging: bool = False,
        string_to_scan: Optional[str] = None,
    ) -> None:
        self.__presentation = presentation or MainPresentation()
        self.__show_stack_trace = show_stack_trace
        self.__string_to_scan = string_to_scan

        self.__version_number = PyMarkdownLint.__get_semantic_version()
        self.__properties: ApplicationProperties = ApplicationProperties()
        self.__logging = (
            None
            if inherit_logging
            else ApplicationLogging(
                self.__properties,
                default_log_level="CRITICAL",
                show_stack_trace=show_stack_trace,
            )
        )
        self.__tokenizer: Optional[TokenizedMarkdown] = None
        self.__plugins: PluginManager = PluginManager(self.__presentation)
        self.__extensions: ExtensionManager = ExtensionManager(self.__presentation)

    @property
    def application_version(self) -> str:
        """
        Return the version of the application.
        """
        return self.__version_number

    @staticmethod
    def __get_semantic_version() -> str:
        file_path = __file__
        assert os.path.isabs(file_path)
        file_path = file_path.replace(os.sep, "/")
        last_index = file_path.rindex("/")
        file_path = f"{file_path[: last_index + 1]}version.py"
        version_meta = runpy.run_path(file_path)
        return str(version_meta["__version__"])

    def __initialize_subsystems(
        self, direct_args: Optional[List[str]]
    ) -> argparse.Namespace:
        ReturnCodeHelper.reset()

        args = self.__parse_arguments(direct_args=direct_args)
        self.__set_initial_state(args)

        self.__show_stack_trace = args.show_stack_trace
        if not self.__show_stack_trace and self.__properties:
            self.__show_stack_trace = self.__properties.get_boolean_property(
                "log.stack-trace"
            )

        if self.__logging:
            self.__logging.initialize(args)
        ParserLogger.sync_on_next_call()

        if direct_args is None:
            LOGGER.debug("Using supplied command line arguments.")
        else:
            LOGGER.debug("Using direct arguments: %s", str(direct_args))

        self.__initialize_plugins_and_extensions(args)
        return args

    def __parse_arguments(self, direct_args: Optional[List[str]]) -> argparse.Namespace:
        parser = argparse.ArgumentParser(description="Lint any found Markdown files.")

        parser.add_argument(
            "-e",
            "--enable-rules",
            dest="enable_rules",
            action="store",
            default="",
            help="comma separated list of rules to enable",
        )
        parser.add_argument(
            "-d",
            "--disable-rules",
            dest="disable_rules",
            action="store",
            default="",
            help="comma separated list of rules to disable",
        )

        parser.add_argument(
            "-x-stdin",
            dest="x_test_stdin_fault",
            action="store_true",
            default="",
            help=argparse.SUPPRESS,
        )
        parser.add_argument(
            "-x-fix-debug",
            dest="x_fix_debug",
            action="store_true",
            default="",
            help=argparse.SUPPRESS,
        )
        parser.add_argument(
            "-x-fix-file-debug",
            dest="x_fix_file_debug",
            action="store_true",
            default="",
            help=argparse.SUPPRESS,
        )
        parser.add_argument(
            "-x-fix-no-rescan-log",
            dest="x_fix_no_rescan_log",
            action="store_true",
            default="",
            help=argparse.SUPPRESS,
        )

        parser.add_argument(
            "--add-plugin",
            dest="add_plugin",
            action="append",
            default=None,
            help="path to a plugin containing a new rule to apply",
        )
        ApplicationPropertiesUtilities.add_default_command_line_arguments(parser)
        parser.add_argument(
            "--stack-trace",
            dest="show_stack_trace",
            action="store_true",
            default=False,
            help="if an error occurs, print out the stack trace for debug purposes",
        )
        parser.add_argument(
            "--continue-on-error",
            dest="continue_on_error",
            action="store_true",
            default=False,
            help="if a tokenization or plugin error occurs, allow processing to continue",
        )
        ApplicationLogging.add_default_command_line_arguments(parser)
        ReturnCodeHelper.add_command_line_arguments(parser)

        subparsers = parser.add_subparsers(dest="primary_subparser")
        ExtensionManager.add_argparse_subparser(subparsers)
        FileScanHelper.add_argparse_subparser(subparsers, True)
        PluginManager.add_argparse_subparser(subparsers)
        FileScanHelper.add_argparse_subparser(subparsers, False)

        subparsers.add_parser("version", help="version of the application")

        parse_arguments = parser.parse_args(args=direct_args)

        if not parse_arguments.primary_subparser:
            parser.print_help()
            ReturnCodeHelper.exit_application(ApplicationResult.COMMAND_LINE_ERROR)
        elif parse_arguments.primary_subparser == "version":
            print(f"{self.__version_number}")
            ReturnCodeHelper.exit_application(ApplicationResult.SUCCESS)
        return parse_arguments

    def __set_initial_state(self, args: argparse.Namespace) -> None:
        if self.__logging:
            self.__logging.pre_initialize_with_args(args)

        ApplicationConfigurationHelper.apply_configuration_layers(
            args, self.__properties, self.__handle_error
        )

        ReturnCodeHelper.set_initial_state(args, self.__properties)

        LOGGER.info("Configuration loaded and applied.  Initial state setup completed.")

    def __initialize_plugins_and_extensions(self, args: argparse.Namespace) -> None:
        self.__initialize_plugins(args)
        self.__initialize_extensions(args)

        if args.primary_subparser == PluginManager.argparse_subparser_name():
            ReturnCodeHelper.exit_application(
                self.__plugins.handle_argparse_subparser(args)
            )
        if args.primary_subparser == ExtensionManager.argparse_subparser_name():
            ReturnCodeHelper.exit_application(
                self.__extensions.handle_argparse_subparser(args)
            )

    def __initialize_plugins(self, args: argparse.Namespace) -> None:
        try:
            plugin_dir = os.path.dirname(os.path.realpath(__file__))
            plugin_dir = os.path.join(plugin_dir, "plugins")
            self.__initialize_plugin_manager(args, plugin_dir)
            self.__apply_configuration_to_plugins()
        except ValueError as this_exception:
            formatted_error = (
                f"{type(this_exception).__name__} encountered while initializing plugins:\n"
                + f"{this_exception}"
            )
            self.__handle_error(formatted_error, this_exception)

    def __initialize_plugin_manager(
        self, args: argparse.Namespace, plugin_dir: str
    ) -> None:
        """
        Make sure all plugins are ready before being initialized.
        """

        try:
            self.__plugins.initialize(
                plugin_dir,
                args.add_plugin,
                args.enable_rules,
                args.disable_rules,
                self.__properties,
                self.__show_stack_trace,
                args.x_fix_debug,
            )
        except BadPluginError as this_exception:
            formatted_error = (
                f"BadPluginError encountered while loading plugins:\n{this_exception}"
            )
            self.__handle_error(formatted_error, this_exception)

    # pylint: disable=broad-exception-caught
    def __apply_configuration_to_plugins(self) -> None:
        try:
            self.__plugins.apply_configuration(self.__properties)
        except Exception as this_exception:
            formatted_error = (
                f"{type(this_exception).__name__} encountered while configuring plugins:\n"
                + f"{this_exception}"
            )
            self.__handle_error(formatted_error, this_exception)

    # pylint: enable=broad-exception-caught

    # pylint: disable=broad-exception-caught
    def __initialize_extensions(self, args: argparse.Namespace) -> None:
        try:
            self.__extensions.initialize(
                args,
                self.__properties,
            )
            self.__extensions.apply_configuration()

        except ValueError as this_exception:
            formatted_error = (
                f"Configuration error {type(this_exception).__name__} encountered "
                + f"while initializing extensions:\n{this_exception}"
            )
            self.__handle_error(formatted_error, this_exception)
        except Exception as this_exception:
            formatted_error = (
                f"Error {type(this_exception).__name__} encountered while initializing extensions:\n"
                + f"{this_exception}"
            )
            self.__handle_error(formatted_error, this_exception)

    # pylint: enable=broad-exception-caught

    def __initialize_parser(self) -> None:
        try:
            self.__tokenizer = TokenizedMarkdown()
            self.__tokenizer.apply_configuration(self.__properties, self.__extensions)
        except BadTokenizationError as this_exception:
            formatted_error = (
                f"{type(this_exception).__name__} encountered while initializing tokenizer:\n"
                + f"{this_exception}"
            )
            self.__handle_error(formatted_error, this_exception)

    def __handle_error(
        self,
        formatted_error: str,
        thrown_error: Optional[Exception],
        exit_on_error: bool = True,
        print_prefix: str = "\n\n",
    ) -> None:
        LOGGER.warning(formatted_error, exc_info=thrown_error)

        stack_trace = (
            "\n" + traceback.format_exc()
            if self.__show_stack_trace
            and thrown_error
            and not isinstance(thrown_error, ValueError)
            else ""
        )
        self.__presentation.print_system_error(
            f"{print_prefix}{formatted_error}{stack_trace}"
        )
        if exit_on_error:
            ReturnCodeHelper.exit_application(ApplicationResult.SYSTEM_ERROR)

    def __handle_file_scanner_output(self, formatted_output: str) -> None:
        self.__presentation.print_system_output(formatted_output)

    def __handle_file_scanner_error(self, formatted_error: str) -> None:
        self.__handle_error(formatted_error, None, exit_on_error=False)

    def __scan_files_if_no_errors(
        self,
        args: argparse.Namespace,
        use_standard_in: bool,
        files_to_scan: List[str],
        did_error_scanning_files: bool,
    ) -> ApplicationResult:  # sourcery skip: extract-method
        scan_result = ApplicationResult.SUCCESS
        did_fix_any_files = False
        if did_error_scanning_files:
            self.__handle_error("No matching files found.", None, exit_on_error=False)
            scan_result = ApplicationResult.NO_FILES_TO_SCAN
        else:
            POGGER.info("Initializing parser.")
            self.__initialize_parser()

            POGGER.info("Processing files with parser.")
            assert self.__tokenizer
            fsh = FileScanHelper(
                self.__tokenizer,
                self.__plugins,
                self.__presentation,
                self.__show_stack_trace,
                self.__handle_error,
            )
            did_fix_any_files, did_fail_any_file = fsh.process_files_to_scan(
                args, use_standard_in, files_to_scan, self.__string_to_scan
            )
            if did_fail_any_file:
                scan_result = ApplicationResult.SYSTEM_ERROR
            elif did_fix_any_files:
                scan_result = ApplicationResult.FIXED_AT_LEAST_ONE_FILE
            elif self.__plugins.number_of_scan_failures:
                scan_result = ApplicationResult.SCAN_TRIGGERED_AT_LEAST_ONCE
            POGGER.info("Files have been processed.")

        return scan_result

    def __find_files_to_scan(
        self, args: argparse.Namespace
    ) -> Tuple[bool, List[str], bool, bool]:
        files_to_scan: List[str] = []
        did_error_scanning_files = False
        did_only_list_files = False

        use_standard_in = FileScanHelper.is_scan_stdin_specified(args)
        if not use_standard_in:
            POGGER.info("Determining files to scan.")
            (
                files_to_scan,
                did_error_scanning_files,
                did_only_list_files,
            ) = ApplicationFileScanner.determine_files_to_scan_with_args(
                args,
                cast(
                    ApplicationFileScannerOutputProtocol,
                    self.__handle_file_scanner_output,
                ),
                cast(
                    ApplicationFileScannerOutputProtocol,
                    self.__handle_file_scanner_error,
                ),
            )
        return (
            use_standard_in,
            files_to_scan,
            did_error_scanning_files,
            did_only_list_files,
        )

    # pylint: disable=broad-exception-caught
    def main(self, direct_args: Optional[List[str]] = None) -> None:
        """
        Main entrance point.
        """
        scan_result = ApplicationResult.SUCCESS
        try:
            args = self.__initialize_subsystems(direct_args)

            (
                use_standard_in,
                files_to_scan,
                did_error_scanning_files,
                did_only_list_files,
            ) = self.__find_files_to_scan(args)
            if did_only_list_files:
                if not files_to_scan:
                    scan_result = ApplicationResult.NO_FILES_TO_SCAN
                ReturnCodeHelper.exit_application(scan_result)
            else:
                scan_result = self.__scan_files_if_no_errors(
                    args, use_standard_in, files_to_scan, did_error_scanning_files
                )
        except ValueError as this_exception:
            formatted_error = f"Configuration Error: {this_exception}"
            self.__handle_error(formatted_error, this_exception)
        except Exception as this_exception:
            formatted_error = (
                f"Unexpected Error({type(this_exception).__name__}): {this_exception}"
            )
            self.__handle_error(formatted_error, this_exception)
        finally:
            if self.__logging:
                self.__logging.terminate()
            self.__logging = None

        ReturnCodeHelper.exit_application(scan_result)

    # pylint: enable=broad-exception-caught


# pylint: enable=too-many-instance-attributes


if __name__ == "__main__":
    PyMarkdownLint().main()
