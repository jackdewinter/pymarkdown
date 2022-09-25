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

from application_properties import (
    ApplicationProperties,
    ApplicationPropertiesJsonLoader,
)

from pymarkdown.application_file_scanner import ApplicationFileScanner
from pymarkdown.bad_tokenization_error import BadTokenizationError
from pymarkdown.extension_manager.extension_manager import ExtensionManager
from pymarkdown.extensions.pragma_token import PragmaToken
from pymarkdown.parser_logger import ParserLogger
from pymarkdown.plugin_manager.bad_plugin_error import BadPluginError
from pymarkdown.plugin_manager.plugin_manager import PluginManager
from pymarkdown.source_providers import FileSourceProvider
from pymarkdown.tokenized_markdown import TokenizedMarkdown

POGGER = ParserLogger(logging.getLogger(__name__))

LOGGER = logging.getLogger(__name__)


class PyMarkdownLint:
    """
    Class to provide for a simple implementation of a title case algorithm.
    """

    available_log_maps = {
        "CRITICAL": logging.CRITICAL,
        "ERROR": logging.ERROR,
        "WARNING": logging.WARNING,
        "INFO": logging.INFO,
        "DEBUG": logging.DEBUG,
    }

    __normal_scan_subcommand = "scan"
    __stdin_scan_subcommand = "scan-stdin"

    def __init__(self) -> None:
        (
            self.__version_number,
            self.__show_stack_trace,
            self.default_log_level,
        ) = (PyMarkdownLint.__get_semantic_version(), False, "CRITICAL")
        self.__tokenizer: Optional[TokenizedMarkdown] = None

        self.__properties: ApplicationProperties = ApplicationProperties()
        self.__plugins: PluginManager = PluginManager()
        self.__extensions: ExtensionManager = ExtensionManager()

    @staticmethod
    def __get_semantic_version() -> str:
        file_path = __file__
        assert os.path.isabs(file_path)
        file_path = file_path.replace(os.sep, "/")
        last_index = file_path.rindex("/")
        file_path = f"{file_path[: last_index + 1]}version.py"
        version_meta = runpy.run_path(file_path)
        return str(version_meta["__version__"])

    @staticmethod
    def log_level_type(argument: str) -> str:
        """
        Function to help argparse limit the valid log levels.
        """
        if argument in PyMarkdownLint.available_log_maps:
            return argument
        raise ValueError(f"Value '{argument}' is not a valid log level.")

    def __parse_arguments(self) -> argparse.Namespace:
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
        parser.add_argument(
            "--stack-trace",
            dest="show_stack_trace",
            action="store_true",
            default=False,
            help="if an error occurs, print out the stack trace for debug purposes",
        )
        parser.add_argument(
            "--log-level",
            dest="log_level",
            action="store",
            help="minimum level required to log messages",
            type=PyMarkdownLint.log_level_type,
            choices=list(PyMarkdownLint.available_log_maps.keys()),
        )
        parser.add_argument(
            "--log-file",
            dest="log_file",
            action="store",
            help="destination file for log messages",
        )

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

        parse_arguments = parser.parse_args()

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
            POGGER.info("Scanning file '$' token-by-token.", next_file_name)
            source_provider = (
                None if args.x_test_scan_fault else FileSourceProvider(next_file)
            )
            assert self.__tokenizer
            actual_tokens = self.__tokenizer.transform_from_provider(source_provider)

            if actual_tokens and actual_tokens[-1].is_pragma:
                pragma_token = cast(PragmaToken, actual_tokens[-1])
                self.__plugins.compile_pragmas(
                    next_file_name, pragma_token.pragma_lines
                )
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

            context.report_on_triggered_rules()
        except Exception:
            context.report_on_triggered_rules()
            raise

    # pylint: disable=broad-except
    def __apply_configuration_to_plugins(self) -> None:

        try:
            self.__plugins.apply_configuration(self.__properties)
        except Exception as this_exception:
            formatted_error = (
                f"{type(this_exception).__name__} encountered while configuring plugins:\n"
                + f"{this_exception}"
            )
            self.__handle_error(formatted_error, this_exception)

    # pylint: enable=broad-except

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
                self.__show_stack_trace,
            )
        except BadPluginError as this_exception:
            formatted_error = (
                f"BadPluginError encountered while loading plugins:\n{this_exception}"
            )
            self.__handle_error(formatted_error, this_exception)

    def __handle_error(self, formatted_error: str, thrown_error: Exception) -> None:

        show_error = self.__show_stack_trace or not isinstance(thrown_error, ValueError)
        LOGGER.warning(formatted_error, exc_info=show_error)

        print(f"\n\n{formatted_error}", file=sys.stderr)
        if self.__show_stack_trace:
            traceback.print_exc(file=sys.stderr)
        sys.exit(1)

    def __handle_scan_error(self, next_file: str, this_exception: Exception) -> None:

        formatted_error = f"{type(this_exception).__name__} encountered while scanning '{next_file}':\n{this_exception}"
        self.__handle_error(formatted_error, this_exception)

    def __set_initial_state(self, args: argparse.Namespace) -> None:

        self.__show_stack_trace = args.show_stack_trace
        base_logger = logging.getLogger()
        base_logger.setLevel(
            logging.DEBUG if self.__show_stack_trace else logging.WARNING
        )

        if args.configuration_file:
            LOGGER.debug("Loading configuration file: %s", args.configuration_file)
            ApplicationPropertiesJsonLoader.load_and_set(
                self.__properties, args.configuration_file, self.__handle_error
            )
        if args.set_configuration:
            self.__properties.set_manual_property(args.set_configuration)

    def __initialize_strict_mode(self, args: argparse.Namespace) -> None:
        if args.strict_configuration or self.__properties.get_boolean_property(
            "mode.strict-config", strict_mode=True
        ):
            self.__properties.enable_strict_mode()

    def __initialize_logging(
        self, args: argparse.Namespace
    ) -> Optional[logging.FileHandler]:

        self.__show_stack_trace = args.show_stack_trace
        if not self.__show_stack_trace:
            self.__show_stack_trace = self.__properties.get_boolean_property(
                "log.stack-trace"
            )

        effective_log_file = (
            self.__properties.get_string_property("log.file")
            if args.log_file is None
            else args.log_file
        )
        new_handler = None
        if effective_log_file:
            new_handler = logging.FileHandler(effective_log_file)
            logging.getLogger().addHandler(new_handler)
        else:
            temp_log_level = (
                logging.DEBUG if self.__show_stack_trace else logging.CRITICAL
            )
            logging.basicConfig(stream=sys.stdout, level=temp_log_level)

        effective_log_level = args.log_level or None
        if effective_log_level is None:
            effective_log_level = self.__properties.get_string_property(
                "log.level", valid_value_fn=PyMarkdownLint.log_level_type
            )
        if effective_log_level is None:
            effective_log_level = self.default_log_level

        log_level_to_enact = PyMarkdownLint.available_log_maps[effective_log_level]

        logging.getLogger().setLevel(log_level_to_enact)
        ParserLogger.sync_on_next_call()
        return new_handler

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

    # pylint: disable=broad-except
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

    # pylint: enable=broad-except

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
            for next_file in files_to_scan:
                self.__scan_specific_file(args, next_file, next_file)

    def main(self) -> None:
        """
        Main entrance point.
        """
        args = self.__parse_arguments()
        self.__set_initial_state(args)

        new_handler, total_error_count = None, 0
        try:
            self.__initialize_strict_mode(args)
            new_handler = self.__initialize_logging(args)

            self.__handle_plugins_and_extensions(args)

            use_standard_in = (
                args.primary_subparser == PyMarkdownLint.__stdin_scan_subcommand
            )
            files_to_scan: List[str] = []
            did_error_scanning_files = False

            if not use_standard_in:
                POGGER.info("Determining files to scan.")
                (
                    files_to_scan,
                    did_error_scanning_files,
                ) = ApplicationFileScanner.determine_files_to_scan_with_args(args)
            if did_error_scanning_files:
                total_error_count = 1
            else:
                self.__initialize_parser(args)

                self.__process_files_to_scan(args, use_standard_in, files_to_scan)
        except ValueError as this_exception:
            formatted_error = f"Configuration Error: {this_exception}"
            self.__handle_error(formatted_error, this_exception)
        finally:
            if new_handler:
                new_handler.close()

        if self.__plugins.number_of_scan_failures or total_error_count:
            sys.exit(1)


if __name__ == "__main__":
    PyMarkdownLint().main()
