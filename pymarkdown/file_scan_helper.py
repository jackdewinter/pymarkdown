"""
Module to specifically deal with handling the file scanning
for the application.
"""

import argparse
import copy
import logging
import os
import shutil
import sys
import tempfile
from typing import Callable, Dict, List, Optional, Tuple, Union, cast

from pymarkdown.application_file_scanner import ApplicationFileScanner
from pymarkdown.extensions.pragma_token import PragmaToken
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
from pymarkdown.return_code_helper import ApplicationResult, ReturnCodeHelper
from pymarkdown.tokens.markdown_token import MarkdownToken
from pymarkdown.transform_markdown.transform_to_markdown import TransformToMarkdown

POGGER = ParserLogger(logging.getLogger(__name__))


class FileScanHelper:
    """
    Class to specifically deal with handling the file scanning
    for the application.
    """

    __normal_scan_subcommand = "scan"
    __stdin_scan_subcommand = "scan-stdin"

    # pylint: disable=too-many-arguments
    def __init__(
        self,
        tokenizer: TokenizedMarkdown,
        plugins: PluginManager,
        presentation: MainPresentation,
        show_stack_trace: bool,
        handle_error: Callable[[str, Exception], None],
    ):
        self.__tokenizer = tokenizer
        self.__plugins = plugins
        self.__presentation = presentation
        self.__show_stack_trace = show_stack_trace
        self.__handle_error = handle_error

    # pylint: enable=too-many-arguments

    def process_files_to_scan(
        self,
        args: argparse.Namespace,
        use_standard_in: bool,
        files_to_scan: List[str],
        string_to_scan: Optional[str],
    ) -> bool:
        """
        Process the specified files to scan, or the string to scan.
        """

        # sourcery skip: raise-specific-error
        did_fix_any_file = False
        if use_standard_in:
            POGGER.debug("Scanning from: (stdin)")
            self.__scan_from_stdin(args, string_to_scan)
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
                        args.x_fix_no_rescan_log,
                    ):
                        self.__presentation.print_fix_message(next_file)
                        did_fix_any_file = True
                else:
                    self.__scan_specific_file(next_file, next_file)
        return did_fix_any_file

    def __scan_from_stdin(
        self, args: argparse.Namespace, string_to_scan: Optional[str]
    ) -> None:
        temporary_file = None
        scan_exception = None
        scan_id = "stdin" if string_to_scan is None else "in-memory"
        try:
            if args.x_test_stdin_fault:
                raise IOError("made up")

            with tempfile.NamedTemporaryFile("wt", delete=False) as outfile:
                temporary_file = outfile.name

                if string_to_scan:
                    outfile.write(string_to_scan)
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

    def __scan_specific_file(self, next_file: str, next_file_name: str) -> None:
        try:
            source_provider = FileSourceProvider(next_file)
            self.__scan_file(source_provider, next_file_name)
        except BadPluginError as this_exception:
            self.__handle_scan_error(next_file, this_exception)

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

        POGGER.info("Completed scanning tokens in file '$'.", next_file_name)

        POGGER.info("Scanning file '$' line-by-line.", next_file_name)
        self.__process_lines_in_file(source_provider, context, next_file_name)

    # pylint: disable=too-many-arguments
    def __fix_specific_file(
        self,
        next_file: str,
        next_file_name: str,
        fix_debug: bool,
        fix_file_debug: bool,
        fix_nolog_rescan: bool,
    ) -> bool:
        did_fix_file = False
        try:
            try:
                POGGER.info("Starting file to fix '$'.", next_file_name)

                did_fix_file = self.__process_file_fix(
                    next_file,
                    next_file_name,
                    fix_debug,
                    fix_file_debug,
                    fix_nolog_rescan,
                )

                POGGER.info("Ending file to fix '$'.", next_file_name)
            except Exception:
                POGGER.info("Ending file to fix '$' with exception.", next_file_name)
                raise
        except (BadPluginError, BadPluginFixError) as this_exception:
            self.__handle_scan_error(next_file, this_exception)
        return did_fix_file

    # pylint: enable=too-many-arguments

    def __handle_scan_error(self, next_file: str, this_exception: Exception) -> None:
        if formatted_error := self.__presentation.format_scan_error(
            next_file, this_exception, self.__show_stack_trace
        ):
            self.__handle_error(formatted_error, this_exception)

        # If the `format_scan_error` call above returned None, it meant that
        # it handled any required output.  However, the application still needs
        # to terminate to respect that the error was called.
        ReturnCodeHelper.exit_application(ApplicationResult.SYSTEM_ERROR)

    def __process_file_fix_rescan(
        self, fix_debug: bool, fix_nolog_rescan: bool, next_file_two: str
    ) -> List[MarkdownToken]:
        if fix_debug:
            print(f"scan: {next_file_two}")
        POGGER.info("Rescanning file '$' before line-by-line fixes.", next_file_two)
        source_provider = FileSourceProvider(next_file_two)
        assert self.__tokenizer is not None

        if fix_nolog_rescan:
            saved_log_level = logging.WARNING
            if POGGER.is_enabled_for(logging.DEBUG):
                saved_log_level = logging.DEBUG
            elif POGGER.is_enabled_for(logging.INFO):
                saved_log_level = logging.INFO
            logging.getLogger().setLevel(logging.WARNING)
            ParserLogger.sync_on_next_call()
            logging.getLogger().warning(
                "Setting logging level to WARN during rescan upon request."
            )

        try:
            actual_tokens = self.__tokenizer.transform_from_provider(
                source_provider, do_add_end_of_stream_token=True
            )
        finally:
            if fix_nolog_rescan:
                saved_log_level_name = logging.getLevelName(saved_log_level)
                logging.getLogger().warning(
                    "Restoring log level to %s.", saved_log_level_name
                )
                logging.getLogger().setLevel(saved_log_level)
                ParserLogger.sync_on_next_call()
        return actual_tokens

    # pylint: disable=too-many-arguments
    def __process_file_fix(
        self,
        next_file: str,
        next_file_name: str,
        fix_debug: bool,
        fix_file_debug: bool,
        fix_nolog_rescan: bool,
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
            actual_tokens = self.__process_file_fix_rescan(
                fix_debug, fix_nolog_rescan, next_file_two
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
            POGGER.info("Scanning before line-by-line fixes.")
            context = self.__plugins.starting_new_file(
                next_file_name,
                fix_mode=True,
                temp_output=source_file,
                fix_token_map=None,
            )

            # Due to context required to process the line requirements, we need go
            # through all the tokens first, before processing the lines.
            #
            # Basically, to allow any of the rules to build context applicable to
            # the line being scanned, we rescan the tokens to present an updated
            # picture of the tokens.
            for next_token in actual_tokens:
                POGGER.info("Processing tokens: $", next_token)
                self.__plugins.next_token(context, next_token)

            POGGER.info("Completed token scanning.")
            self.__process_lines_in_file(source_provider, context, next_file_name)
            this_file_fix_line_records = context.fix_line_records
            if this_file_fix_line_records and fix_debug:
                for next_record in context.fix_line_records:
                    print(next_record)

        self.__print_file_in_debug_mode(fix_debug, fix_file_debug, temporary_file_name)
        return this_file_fix_line_records, temporary_file_name

    # pylint: enable=too-many-arguments

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
        fix_map: Dict[str, Tuple[Union[str, int], str]] = {}
        for next_fix_record in requested_fixes:
            map_key = str(next_fix_record.token_to_fix) + str(
                next_fix_record.field_name
            )
            if map_key in fix_map:
                recorded_value = next_fix_record.field_value
                fix_value = fix_map[map_key]

                current_plugin_id = next_fix_record.plugin_id.upper()
                previous_plugin_id = fix_value[1].upper()

                POGGER.info(
                    "Previous plugin ($) wants to set field $ to '$'",
                    previous_plugin_id,
                    next_fix_record.field_name,
                    recorded_value,
                )
                POGGER.info(
                    "Current plugin ($) wants to set field $ to '$'",
                    current_plugin_id,
                    next_fix_record.field_name,
                    fix_value[0],
                )

                raise BadPluginFixError(
                    f"Multiple plugins ({current_plugin_id} and {previous_plugin_id}) have requested a fix for the same field of the same token."
                )
            fix_map[map_key] = (next_fix_record.field_value, next_fix_record.plugin_id)

        for next_fix_record in requested_fixes:
            before_instance = copy.deepcopy(token_instance)
            if not token_instance.modify_token(
                context, next_fix_record.field_name, next_fix_record.field_value
            ):
                POGGER.debug(
                    "Token $ fix for plugin $ in action $ on field $ failed.",
                    next_fix_record.plugin_id,
                    next_fix_record.plugin_action,
                    next_fix_record.field_name,
                )
                raise BadPluginFixError(
                    formatted_message=f"Plugin id '{next_fix_record.plugin_id.upper()}'s '{next_fix_record.plugin_action}' action requested a token adjustment to field '{next_fix_record.field_name}' that failed."
                )
            POGGER.debug(
                "Token fix for plugin $ in action $ on field $ succeeded.",
                next_fix_record.plugin_id,
                next_fix_record.plugin_action,
                next_fix_record.field_name,
            )
            POGGER.debug(
                "Token before <$> and after <$>.", before_instance, token_instance
            )

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

        POGGER.info("Completed scanning lines in file '$'.", next_file_name)
        self.__plugins.completed_file(context, line_number)

    @staticmethod
    def is_scan_stdin_specified(args: argparse.Namespace) -> bool:
        """
        Specifies whether scanning from stdin was specified.
        """
        return FileScanHelper.__stdin_scan_subcommand == args.primary_subparser  # type: ignore

    @staticmethod
    def add_argparse_subparser(subparsers: argparse._SubParsersAction) -> None:  # type: ignore
        """
        Add the subparser for scanning.
        """
        new_sub_parser = subparsers.add_parser(
            FileScanHelper.__normal_scan_subcommand,
            help="scan the Markdown files in the specified paths",
        )
        ApplicationFileScanner.add_default_command_line_arguments(
            new_sub_parser, ".md", "Markdown"
        )

        subparsers.add_parser(
            FileScanHelper.__stdin_scan_subcommand,
            help="scan the standard input as a Markdown file",
        )
