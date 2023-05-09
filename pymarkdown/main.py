"""
Module to provide for a simple implementation of a title case algorithm.
"""
import argparse
import logging
import os
import runpy
import sys
import tempfile
import traceback
from typing import List, Optional, cast

from application_properties import ApplicationProperties

from pymarkdown.application_file_scanner import ApplicationFileScanner
from pymarkdown.application_logging import ApplicationLogging
from pymarkdown.bad_tokenization_error import BadTokenizationError
from pymarkdown.extension_manager.extension_manager import ExtensionManager
from pymarkdown.extensions.pragma_token import PragmaToken
from pymarkdown.main_presentation import MainPresentation
from pymarkdown.markdown_token import MarkdownToken
from pymarkdown.my_application_properties import MyApplicationProperties
from pymarkdown.parser_logger import ParserLogger
from pymarkdown.plugin_manager.bad_plugin_error import BadPluginError
from pymarkdown.plugin_manager.plugin_manager import PluginManager
from pymarkdown.plugin_manager.plugin_scan_context import PluginScanContext
from pymarkdown.source_providers import FileSourceProvider
from pymarkdown.tokenized_markdown import TokenizedMarkdown

POGGER = ParserLogger(logging.getLogger(__name__))

LOGGER = logging.getLogger(__name__)

# pylint: disable=too-few-public-methods


class PyMarkdownLint:
    """
    Class to provide for a simple implementation of a title case algorithm.
    """

    __default_configuration_file = ".pymarkdown"
    __pyproject_toml_file = "pyproject.toml"
    __pyproject_section_header = "tool.pymarkdown"

    __normal_scan_subcommand = "scan"
    __stdin_scan_subcommand = "scan-stdin"

    def __init__(self, presentation: Optional[MainPresentation] = None) -> None:
        self.__version_number = PyMarkdownLint.__get_semantic_version()

        self.__presentation = presentation or MainPresentation()
        self.__properties: ApplicationProperties = ApplicationProperties()
        self.__logging = ApplicationLogging(
            self.__properties, default_log_level="CRITICAL"
        )
        self.__tokenizer: Optional[TokenizedMarkdown] = None
        self.__plugins: PluginManager = PluginManager(self.__presentation)
        self.__extensions: ExtensionManager = ExtensionManager(self.__presentation)

    @staticmethod
    def __get_semantic_version() -> str:
        file_path = __file__
        assert os.path.isabs(file_path)
        file_path = file_path.replace(os.sep, "/")
        last_index = file_path.rindex("/")
        file_path = f"{file_path[: last_index + 1]}version.py"
        version_meta = runpy.run_path(file_path)
        return str(version_meta["__version__"])

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
            "-x-scan",
            dest="x_test_scan_fault",
            action="store_true",
            default="",
            help=argparse.SUPPRESS,
        )
        parser.add_argument(
            "-x-init",
            dest="x_test_init_fault",
            action="store_true",
            default="",
            help=argparse.SUPPRESS,
        )
        parser.add_argument(
            "-x-stdin",
            dest="x_test_stdin_fault",
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
        MyApplicationProperties.add_default_command_line_arguments(parser)
        ApplicationLogging.add_default_command_line_arguments(parser)

        subparsers = parser.add_subparsers(dest="primary_subparser")

        PluginManager.add_argparse_subparser(subparsers)
        ExtensionManager.add_argparse_subparser(subparsers)

        new_sub_parser = subparsers.add_parser(
            PyMarkdownLint.__normal_scan_subcommand,
            help="scan the Markdown files in the specified paths",
        )
        ApplicationFileScanner.add_default_command_line_arguments(
            new_sub_parser, ".md", "Markdown"
        )

        subparsers.add_parser(
            PyMarkdownLint.__stdin_scan_subcommand,
            help="scan the standard input as a Markdown file",
        )

        subparsers.add_parser("version", help="version of the application")

        parse_arguments = parser.parse_args(args=direct_args)

        if not parse_arguments.primary_subparser:
            parser.print_help()
            sys.exit(2)
        elif parse_arguments.primary_subparser == "version":
            print(f"{self.__version_number}")
            sys.exit(0)
        return parse_arguments

    def __scan_file(
        self, args: argparse.Namespace, next_file: str, next_file_name: str
    ) -> None:
        """
        Scan a given file and call the plugin manager for any significant events.
        """

        POGGER.info("Scanning file '$'.", next_file_name)
        context = self.__plugins.starting_new_file(next_file_name)

        try:
            POGGER.info("Starting file '$'.", next_file_name)

            POGGER.info("Scanning file '$' token-by-token.", next_file_name)
            source_provider = (
                None if args.x_test_scan_fault else FileSourceProvider(next_file)
            )
            assert self.__tokenizer
            actual_tokens = self.__tokenizer.transform_from_provider(source_provider)

            self.__process_file_scan(context, next_file, next_file_name, actual_tokens)

            context.report_on_triggered_rules()
            POGGER.info("Ending file '$'.", next_file_name)
        except Exception:
            context.report_on_triggered_rules()
            POGGER.info("Ending file '$' with exception.", next_file_name)
            raise

    def __process_file_scan(
        self,
        context: PluginScanContext,
        next_file: str,
        next_file_name: str,
        actual_tokens: List[MarkdownToken],
    ) -> None:
        if actual_tokens and actual_tokens[-1].is_pragma:
            pragma_token = cast(PragmaToken, actual_tokens[-1])
            self.__plugins.compile_pragmas(next_file_name, pragma_token.pragma_lines)
            actual_tokens = actual_tokens[:-1]

        POGGER.info("Scanning file '$' tokens.", next_file_name)
        for next_token in actual_tokens:
            POGGER.info("Processing token: $", next_token)
            self.__plugins.next_token(context, next_token)

        POGGER.info("Scanning file '$' line-by-line.", next_file_name)
        source_provider = FileSourceProvider(next_file)
        line_number, next_line = 1, source_provider.get_next_line()
        while next_line is not None:
            POGGER.info("Processing line $: $", line_number, next_line)
            self.__plugins.next_line(context, line_number, next_line)
            line_number += 1
            next_line = source_provider.get_next_line()

        POGGER.info("Completed scanning file '$'.", next_file_name)
        self.__plugins.completed_file(context, line_number)

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

    def __initialize_parser(self, args: argparse.Namespace) -> None:
        resource_path = "fredo" if args.x_test_init_fault else None
        try:
            self.__tokenizer = TokenizedMarkdown(resource_path)
            self.__tokenizer.apply_configuration(self.__properties, self.__extensions)
        except BadTokenizationError as this_exception:
            formatted_error = (
                f"{type(this_exception).__name__} encountered while initializing tokenizer:\n"
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
                self.__logging.show_stack_trace,
            )
        except BadPluginError as this_exception:
            formatted_error = (
                f"BadPluginError encountered while loading plugins:\n{this_exception}"
            )
            self.__handle_error(formatted_error, this_exception)

    def __handle_error(
        self, formatted_error: str, thrown_error: Optional[Exception]
    ) -> None:
        show_error = self.__logging.show_stack_trace or (
            thrown_error and not isinstance(thrown_error, ValueError)
        )
        LOGGER.warning(formatted_error, exc_info=show_error)

        stack_trace = (
            "\n" + traceback.format_exc() if self.__logging.show_stack_trace else ""
        )
        self.__presentation.print_system_error(f"\n\n{formatted_error}{stack_trace}")
        sys.exit(1)

    def __handle_scan_error(self, next_file: str, this_exception: Exception) -> None:
        if formatted_error := self.__presentation.format_scan_error(
            next_file, this_exception
        ):
            self.__handle_error(formatted_error, this_exception)
        sys.exit(1)

    def __apply_configuration_layers(self, args: argparse.Namespace) -> None:
        MyApplicationProperties.process_standard_python_configuration_files(
            self.__properties, self.__handle_error
        )

        MyApplicationProperties.process_project_specific_json_configuration(
            PyMarkdownLint.__default_configuration_file,
            args,
            self.__properties,
            self.__handle_error,
        )

    def __set_initial_state(self, args: argparse.Namespace) -> None:
        self.__logging.pre_initialize_with_args(args)

        self.__apply_configuration_layers(args)

        if args.strict_configuration or self.__properties.get_boolean_property(
            "mode.strict-config", strict_mode=True
        ):
            self.__properties.enable_strict_mode()

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

    def __handle_plugins_and_extensions(self, args: argparse.Namespace) -> None:
        self.__initialize_plugins(args)
        self.__initialize_extensions(args)

        if args.primary_subparser == PluginManager.argparse_subparser_name():
            sys.exit(self.__plugins.handle_argparse_subparser(args))
        if args.primary_subparser == ExtensionManager.argparse_subparser_name():
            sys.exit(self.__extensions.handle_argparse_subparser(args))

    def __scan_specific_file(
        self, args: argparse.Namespace, next_file: str, next_file_name: str
    ) -> None:
        try:
            self.__scan_file(args, next_file, next_file_name)
        except BadPluginError as this_exception:
            self.__handle_scan_error(next_file, this_exception)
        except BadTokenizationError as this_exception:
            self.__handle_scan_error(next_file, this_exception)

    def __process_files_to_scan(
        self, args: argparse.Namespace, use_standard_in: bool, files_to_scan: List[str]
    ) -> None:
        # sourcery skip: raise-specific-error
        if use_standard_in:
            POGGER.debug("Scanning from: (stdin)")

            temporary_file = None
            scan_exception = None
            try:
                if args.x_test_stdin_fault:
                    raise IOError("made up")

                with tempfile.NamedTemporaryFile("wt", delete=False) as outfile:
                    temporary_file = outfile.name

                    for line in sys.stdin:
                        outfile.write(line)

                self.__scan_specific_file(args, temporary_file, "stdin")

            except IOError as this_exception:
                scan_exception = this_exception
            finally:
                if temporary_file and os.path.exists(temporary_file):
                    os.remove(temporary_file)

            if scan_exception:
                try:
                    raise IOError(
                        f"Temporary file to capture stdin was not written ({scan_exception})."
                    ) from scan_exception
                except IOError as this_exception:
                    self.__handle_scan_error("stdin", this_exception)
        else:
            POGGER.debug("Scanning from: $", files_to_scan)
            for next_file in files_to_scan:
                self.__scan_specific_file(args, next_file, next_file)

    def __initialize_subsystems(
        self, direct_args: Optional[List[str]]
    ) -> argparse.Namespace:
        args = self.__parse_arguments(direct_args=direct_args)
        self.__set_initial_state(args)

        self.__logging.initialize(args)
        ParserLogger.sync_on_next_call()

        if direct_args is None:
            LOGGER.debug("Using supplied command line arguments.")
        else:
            LOGGER.debug("Using direct arguments: %s", str(direct_args))

        self.__handle_plugins_and_extensions(args)
        return args

    def main(self, direct_args: Optional[List[str]] = None) -> None:
        """
        Main entrance point.
        """
        total_error_count = 0
        try:
            args = self.__initialize_subsystems(direct_args)

            files_to_scan: List[str] = []
            did_error_scanning_files = False

            use_standard_in = (
                args.primary_subparser == PyMarkdownLint.__stdin_scan_subcommand
            )
            if not use_standard_in:
                POGGER.info("Determining files to scan.")
                (
                    files_to_scan,
                    did_error_scanning_files,
                ) = ApplicationFileScanner.determine_files_to_scan_with_args(args)
            if did_error_scanning_files:
                total_error_count = 1
            else:
                POGGER.info("Initializing parser.")
                self.__initialize_parser(args)

                POGGER.info("Processing files with parser.")
                self.__process_files_to_scan(args, use_standard_in, files_to_scan)
                POGGER.info("Files have been processed.")
        except ValueError as this_exception:
            formatted_error = f"Configuration Error: {this_exception}"
            self.__handle_error(formatted_error, this_exception)
        finally:
            self.__logging.terminate()

        if self.__plugins.number_of_scan_failures or total_error_count:
            sys.exit(1)


# pylint: enable=too-few-public-methods

if __name__ == "__main__":
    PyMarkdownLint().main()
