"""
Module to provide for a simple implementation of a title case algorithm.
"""
import argparse
import logging
import os
import runpy
import shutil
import sys
import tempfile
import traceback
from typing import Dict, List, Optional, Tuple, cast

from application_properties import ApplicationProperties
from application_properties.application_properties_utilities import (
    ApplicationPropertiesUtilities,
)

from pymarkdown.application_file_scanner import (
    ApplicationFileScanner,
    ApplicationFileScannerOutputProtocol,
)
from pymarkdown.application_logging import ApplicationLogging
from pymarkdown.extension_manager.extension_manager import ExtensionManager
from pymarkdown.extensions.pragma_token import PragmaToken
from pymarkdown.general.bad_tokenization_error import BadTokenizationError
from pymarkdown.general.main_presentation import MainPresentation
from pymarkdown.general.parser_logger import ParserLogger
from pymarkdown.general.source_providers import FileSourceProvider
from pymarkdown.general.tokenized_markdown import TokenizedMarkdown
from pymarkdown.plugin_manager.bad_plugin_error import BadPluginError
from pymarkdown.plugin_manager.bad_plugin_fix_error import BadPluginFixError
from pymarkdown.plugin_manager.fix_line_record import FixLineRecord
from pymarkdown.plugin_manager.fix_token_record import FixTokenRecord
from pymarkdown.plugin_manager.plugin_manager import PluginManager
from pymarkdown.plugin_manager.plugin_scan_context import PluginScanContext
from pymarkdown.tokens.markdown_token import MarkdownToken
from pymarkdown.transform_markdown.transform_to_markdown import TransformToMarkdown

POGGER = ParserLogger(logging.getLogger(__name__))

LOGGER = logging.getLogger(__name__)


# pylint: disable=too-many-instance-attributes
class PyMarkdownLint:
    """
    Class to provide for a simple implementation of a title case algorithm.
    """

    __default_configuration_file = ".pymarkdown"

    __normal_scan_subcommand = "scan"
    __stdin_scan_subcommand = "scan-stdin"

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
            "-x-fix",
            dest="x_fix",
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
        self, source_provider: FileSourceProvider, next_file_name: str
    ) -> None:  # sourcery skip: extract-method
        """
        Scan a given file and call the plugin manager for any significant events.
        """

        POGGER.info("Scanning file '$'.", next_file_name)
        context = self.__plugins.starting_new_file(
            next_file_name, False, None, fix_token_map=None
        )

        try:
            POGGER.info("Starting file '$'.", next_file_name)

            POGGER.info("Scanning file '$' token-by-token.", next_file_name)
            assert self.__tokenizer
            actual_tokens = self.__tokenizer.transform_from_provider(
                source_provider, do_add_end_of_stream_token=True
            )

            source_provider.reset_to_start()
            self.__process_file_scan(
                context, source_provider, next_file_name, actual_tokens
            )

            context.report_on_triggered_rules()
            POGGER.info("Ending file '$'.", next_file_name)
        except Exception:
            context.report_on_triggered_rules()
            POGGER.info("Ending file '$' with exception.", next_file_name)
            raise

    def __process_lines_in_file(
        self,
        source_provider: FileSourceProvider,
        context: PluginScanContext,
        next_file_name: str,
    ) -> None:
        line_number, next_line = 1, source_provider.get_next_line()
        while next_line is not None:
            POGGER.info("Processing line $: $", line_number, next_line)
            self.__plugins.next_line(
                context,
                line_number,
                next_line,
                source_provider.is_at_end_of_file,
                source_provider.did_final_line_end_with_newline,
            )
            line_number += 1
            next_line = source_provider.get_next_line()

        POGGER.info("Completed scanning file '$'.", next_file_name)
        self.__plugins.completed_file(context, line_number)

    def __apply_token_fix(
        self,
        context: PluginScanContext,
        token_instance: MarkdownToken,
        requested_fixes: List[FixTokenRecord],
        actual_tokens: List[MarkdownToken],
    ) -> None:
        # TODO figure out if we have to copy and replace, or if modifying the token in place is enough.
        _ = actual_tokens

        # TODO Simple scan for now, in future, want to check and allow 2 names that set to the same value.
        fix_map = {}
        for next_fix_record in requested_fixes:
            map_key = str(next_fix_record.token_to_fix) + str(
                next_fix_record.field_name
            )
            if map_key in fix_map:
                raise BadPluginFixError(
                    "More than one plugin has requested a fix for the same field of the same token."
                )
            fix_map[map_key] = next_fix_record.field_value

        for next_fix_record in requested_fixes:
            if not token_instance.modify_token(
                context, next_fix_record.field_name, next_fix_record.field_value
            ):
                POGGER.debug(
                    "Token fix for plugin %s in action %s on field %s failed.",
                    next_fix_record.plugin_id,
                    next_fix_record.plugin_action,
                    next_fix_record.field_name,
                )
                raise BadPluginFixError(
                    formatted_message=f"Plugin id '{next_fix_record.plugin_id.upper()}'s '{next_fix_record.plugin_action}' action requested a token adjustment to field '{next_fix_record.field_name}' that failed."
                )

    def __print_file_in_debug_mode(
        self, fix_debug: bool, fix_file_debug: bool, next_file: str
    ) -> None:
        if fix_debug and fix_file_debug:
            with open(next_file, "rt", encoding="utf-8") as source_file:
                file_contents = source_file.read()
                print(
                    "\n--"
                    + next_file
                    + "--\n"
                    + file_contents.replace("\n", "\\n")
                    + "\n--"
                )

    def __process_file_fix_tokens(
        self, next_file: str, next_file_name: str, fix_debug: bool, fix_file_debug: bool
    ) -> Tuple[str, List[MarkdownToken], Dict[MarkdownToken, List[FixTokenRecord]]]:
        self.__print_file_in_debug_mode(fix_debug, fix_file_debug, next_file)

        POGGER.info("Scanning file to fix '$' token-by-token.", next_file_name)
        assert self.__tokenizer
        source_provider = FileSourceProvider(next_file)
        actual_tokens = self.__tokenizer.transform_from_provider(
            source_provider, do_add_end_of_stream_token=True
        )

        fix_token_map: Dict[MarkdownToken, List[FixTokenRecord]] = {}
        context = self.__plugins.starting_new_file(
            next_file_name, fix_mode=True, temp_output=None, fix_token_map=fix_token_map
        )
        for next_token in actual_tokens:
            POGGER.info("Processing token: $", next_token)
            self.__plugins.next_token(context, next_token)

        POGGER.info("Completed scanning file '$' for fixes.", next_file_name)
        self.__plugins.completed_file(context, -1)

        if context.get_fix_token_map():
            (
                next_file,
                actual_tokens,
                fix_token_map,
            ) = self.__process_file_fix_tokens_apply_fixes(
                context,
                next_file,
                actual_tokens,
                fix_token_map,
                fix_debug,
                fix_file_debug,
            )
        return next_file, actual_tokens, fix_token_map

    # pylint: disable=too-many-arguments
    def __process_file_fix_tokens_apply_fixes(
        self,
        context: PluginScanContext,
        next_file: str,
        actual_tokens: List[MarkdownToken],
        fix_token_map: Dict[MarkdownToken, List[FixTokenRecord]],
        fix_debug: bool,
        fix_file_debug: bool,
    ) -> Tuple[str, List[MarkdownToken], Dict[MarkdownToken, List[FixTokenRecord]]]:
        for token_instance, requested_fixes in context.get_fix_token_map().items():
            if fix_debug:
                print(f"BEFORE:{str(token_instance)}:{str(requested_fixes)}")
            self.__apply_token_fix(
                context, token_instance, requested_fixes, actual_tokens
            )
            if fix_debug:
                print(f" AFTER:{str(token_instance)}:{str(requested_fixes)}")
        if fix_debug:
            print("--")

        transformer = TransformToMarkdown()
        markdown_from_tokens = transformer.transform(actual_tokens)

        with tempfile.NamedTemporaryFile() as temp_output:
            temporary_file_name = temp_output.name
        with open(temporary_file_name, "wt", encoding="utf-8") as source_file:
            source_file.write(markdown_from_tokens)
            next_file = temporary_file_name
            actual_tokens.clear()

        self.__print_file_in_debug_mode(fix_debug, fix_file_debug, temporary_file_name)
        return next_file, actual_tokens, fix_token_map

    # pylint: enable=too-many-arguments

    # pylint: disable=too-many-arguments
    def __process_file_fix_lines(
        self,
        next_file: str,
        next_file_name: str,
        actual_tokens: List[MarkdownToken],
        fix_debug: bool,
        fix_file_debug: bool,
    ) -> Tuple[List[FixLineRecord], str]:
        source_provider = FileSourceProvider(next_file)
        with tempfile.NamedTemporaryFile() as temp_output:
            temporary_file_name = temp_output.name
        with open(temporary_file_name, "wt", encoding="utf-8") as source_file:
            POGGER.info("Scanning file '$' for line-by-line fixes.", next_file_name)
            context = self.__plugins.starting_new_file(
                next_file_name,
                fix_mode=True,
                temp_output=source_file,
                fix_token_map=None,
            )

            # Due to context required to process the line requirements, we need go
            # through all the tokens first, before processing the lines.
            for next_token in actual_tokens:
                POGGER.info("Processing token: $", next_token)
                self.__plugins.next_token(context, next_token)

            self.__process_lines_in_file(source_provider, context, next_file_name)
            this_file_fix_line_records = context.fix_line_records
            if this_file_fix_line_records and fix_debug:
                for next_record in context.fix_line_records:
                    print(next_record)

        self.__print_file_in_debug_mode(fix_debug, fix_file_debug, temporary_file_name)
        return this_file_fix_line_records, temporary_file_name

    # pylint: enable=too-many-arguments

    def __process_file_fix(
        self, next_file: str, next_file_name: str, fix_debug: bool, fix_file_debug: bool
    ) -> bool:
        # TODO add more protections around fixing i.e. IOError handling

        # Scan the provided file for any token fixes.
        next_file_two, actual_tokens, fix_token_map = self.__process_file_fix_tokens(
            next_file, next_file_name, fix_debug, fix_file_debug
        )
        did_any_tokens_get_fixed = bool(fix_token_map)

        # If tokens are returned, then no changes were made due to tokens and the
        # tokenized list can be reused without any worry of changes.
        if actual_tokens:
            assert not did_any_tokens_get_fixed
            POGGER.info(
                "Scanning for token fixes did not change file.  Reusing tokens for line-by-line fixes."
            )
        else:
            if fix_debug:
                print(f"scan: {next_file_two}")
            POGGER.info("Scanning file '$' for line-by-line fixes.", next_file_two)
            source_provider = FileSourceProvider(next_file_two)
            assert self.__tokenizer is not None
            actual_tokens = self.__tokenizer.transform_from_provider(
                source_provider, do_add_end_of_stream_token=True
            )

        # As the lines are processed, a new temporary line file is written to. If either
        # tokens were fixed or lines were fixed, the file contents of the file
        # temporary_line_file_name will contain the updated document.
        (
            this_file_fix_line_records,
            temporary_line_file_name,
        ) = self.__process_file_fix_lines(
            next_file_two, next_file_name, actual_tokens, fix_debug, fix_file_debug
        )

        # If anything was fixed, copy the temporary file on top of the original file
        # that was scanned.
        did_any_lines_get_fixed = bool(this_file_fix_line_records)
        did_anything_get_fixed = did_any_lines_get_fixed or did_any_tokens_get_fixed
        if did_anything_get_fixed:
            if fix_debug and fix_file_debug:
                print(f"Copy {temporary_line_file_name} to {next_file}")
            shutil.copyfile(temporary_line_file_name, next_file)
        if fix_debug and fix_file_debug:
            print(f"Remove:{temporary_line_file_name}")
        os.remove(temporary_line_file_name)
        if next_file_two != next_file:
            if fix_debug and fix_file_debug:
                print(f"Remove:{next_file_two}")
            os.remove(next_file_two)
        return did_anything_get_fixed

    def __process_file_scan(
        self,
        context: PluginScanContext,
        source_provider: FileSourceProvider,
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
        self.__process_lines_in_file(source_provider, context, next_file_name)

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

    def __handle_error(
        self,
        formatted_error: str,
        thrown_error: Optional[Exception],
        exit_on_error: bool = True,
    ) -> None:
        LOGGER.warning(formatted_error, exc_info=thrown_error)

        stack_trace = (
            "\n" + traceback.format_exc()
            if self.__show_stack_trace
            and thrown_error
            and not isinstance(thrown_error, ValueError)
            else ""
        )
        self.__presentation.print_system_error(f"\n\n{formatted_error}{stack_trace}")
        if exit_on_error:
            sys.exit(1)

    def __handle_scan_error(self, next_file: str, this_exception: Exception) -> None:
        if formatted_error := self.__presentation.format_scan_error(
            next_file, this_exception, self.__show_stack_trace
        ):
            self.__handle_error(formatted_error, this_exception)
        sys.exit(1)

    def __handle_file_scanner_output(self, formatted_output: str) -> None:
        self.__presentation.print_system_output(formatted_output)

    def __handle_file_scanner_error(self, formatted_error: str) -> None:
        self.__handle_error(formatted_error, None, exit_on_error=False)

    def __fix_specific_file(
        self, next_file: str, next_file_name: str, fix_debug: bool, fix_file_debug: bool
    ) -> bool:
        did_fix_file = False
        try:
            try:
                POGGER.info("Starting file to fix '$'.", next_file_name)

                did_fix_file = self.__process_file_fix(
                    next_file, next_file_name, fix_debug, fix_file_debug
                )

                POGGER.info("Ending file to fix '$'.", next_file_name)
            except Exception:
                POGGER.info("Ending file to fix '$' with exception.", next_file_name)
                raise
        except BadPluginError as this_exception:
            self.__handle_scan_error(next_file, this_exception)
        except BadPluginFixError as this_exception:
            self.__handle_scan_error(next_file, this_exception)
        # except BadTokenizationError as this_exception:
        #     self.__handle_scan_error(next_file, this_exception)
        return did_fix_file

    def __scan_specific_file(self, next_file: str, next_file_name: str) -> None:
        try:
            source_provider = FileSourceProvider(next_file)
            self.__scan_file(source_provider, next_file_name)
        except BadPluginError as this_exception:
            self.__handle_scan_error(next_file, this_exception)
        # except BadTokenizationError as this_exception:
        #     self.__handle_scan_error(next_file, this_exception)

    def __scan_from_stdin(self, args: argparse.Namespace) -> None:
        temporary_file = None
        scan_exception = None
        scan_id = "stdin" if self.__string_to_scan is None else "in-memory"
        try:
            if args.x_test_stdin_fault:
                raise IOError("made up")

            with tempfile.NamedTemporaryFile("wt", delete=False) as outfile:
                temporary_file = outfile.name

                if self.__string_to_scan:
                    outfile.write(self.__string_to_scan)
                else:
                    for line in sys.stdin:
                        outfile.write(line)

            self.__scan_specific_file(temporary_file, scan_id)

        except IOError as this_exception:
            scan_exception = this_exception
        finally:
            if temporary_file and os.path.exists(temporary_file):
                os.remove(temporary_file)

        if scan_exception:
            try:
                raise IOError(
                    f"Temporary file to capture {scan_id} was not written ({scan_exception})."
                ) from scan_exception
            except IOError as this_exception:
                self.__handle_scan_error(scan_id, this_exception)

    def __process_files_to_scan(
        self, args: argparse.Namespace, use_standard_in: bool, files_to_scan: List[str]
    ) -> bool:
        # sourcery skip: raise-specific-error
        did_fix_any_file = False
        if use_standard_in:
            POGGER.debug("Scanning from: (stdin)")
            self.__scan_from_stdin(args)
            assert not args.x_fix

        else:
            POGGER.debug("Scanning from: $", files_to_scan)
            for next_file in files_to_scan:
                if args.x_fix:
                    if self.__fix_specific_file(
                        next_file,
                        next_file,
                        args.x_fix_debug,
                        args.x_fix_file_debug,
                    ):
                        self.__presentation.print_fix_message(next_file)
                        did_fix_any_file = True
                else:
                    self.__scan_specific_file(next_file, next_file)
        return did_fix_any_file

    def __initialize_subsystems(
        self, direct_args: Optional[List[str]]
    ) -> argparse.Namespace:
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

    def __set_initial_state(self, args: argparse.Namespace) -> None:
        if self.__logging:
            self.__logging.pre_initialize_with_args(args)

        self.__apply_configuration_layers(args)

        if args.strict_configuration or self.__properties.get_boolean_property(
            "mode.strict-config", strict_mode=True
        ):
            self.__properties.enable_strict_mode()

    def __apply_configuration_layers(self, args: argparse.Namespace) -> None:
        ApplicationPropertiesUtilities.process_standard_python_configuration_files(
            self.__properties, self.__handle_error
        )

        ApplicationPropertiesUtilities.process_project_specific_json_configuration(
            PyMarkdownLint.__default_configuration_file,
            args,
            self.__properties,
            self.__handle_error,
        )

    def __initialize_plugins_and_extensions(self, args: argparse.Namespace) -> None:
        self.__initialize_plugins(args)
        self.__initialize_extensions(args)

        if args.primary_subparser == PluginManager.argparse_subparser_name():
            sys.exit(self.__plugins.handle_argparse_subparser(args))
        if args.primary_subparser == ExtensionManager.argparse_subparser_name():
            sys.exit(self.__extensions.handle_argparse_subparser(args))

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

    # pylint: disable=broad-exception-caught
    def main(self, direct_args: Optional[List[str]] = None) -> None:
        """
        Main entrance point.
        """
        total_error_count = 0
        did_fix_any_files = False
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
            if did_error_scanning_files:
                self.__handle_error(
                    "No matching files found.", None, exit_on_error=False
                )
                total_error_count = 1
            else:
                POGGER.info("Initializing parser.")
                self.__initialize_parser()

                POGGER.info("Processing files with parser.")
                did_fix_any_files = self.__process_files_to_scan(
                    args, use_standard_in, files_to_scan
                )
                POGGER.info("Files have been processed.")
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

        if self.__plugins.number_of_scan_failures or total_error_count:
            sys.exit(1)
        if did_fix_any_files:
            sys.exit(3)

    # pylint: enable=broad-exception-caught


# pylint: enable=too-many-instance-attributes


if __name__ == "__main__":
    PyMarkdownLint().main()
