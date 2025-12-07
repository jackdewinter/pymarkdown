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
from typing import Callable, Dict, List, Optional, Set, Tuple, Union, cast

from pymarkdown.application_file_scanner import ApplicationFileScanner
from pymarkdown.extensions.pragma_token import PragmaToken
from pymarkdown.general.bad_tokenization_error import BadTokenizationError
from pymarkdown.general.main_presentation import MainPresentation
from pymarkdown.general.parser_helper import ParserHelper
from pymarkdown.general.parser_logger import ParserLogger
from pymarkdown.general.source_providers import FileSourceProvider
from pymarkdown.general.tokenized_markdown import TokenizedMarkdown
from pymarkdown.plugin_manager.bad_plugin_error import BadPluginError
from pymarkdown.plugin_manager.bad_plugin_fix_error import BadPluginFixError
from pymarkdown.plugin_manager.fix_line_record import FixLineRecord
from pymarkdown.plugin_manager.fix_token_record import FixTokenRecord
from pymarkdown.plugin_manager.found_plugin import FoundPlugin
from pymarkdown.plugin_manager.plugin_manager import PluginManager
from pymarkdown.plugin_manager.plugin_scan_context import PluginScanContext
from pymarkdown.plugin_manager.replace_tokens_record import ReplaceTokensRecord
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
    __normal_fix_subcommand = "fix"

    # pylint: disable=too-many-arguments
    def __init__(
        self,
        tokenizer: TokenizedMarkdown,
        plugins: PluginManager,
        presentation: MainPresentation,
        show_stack_trace: bool,
        handle_error: Callable[[str, Optional[Exception], bool, str], None],
    ):
        self.__tokenizer = tokenizer
        self.__plugins = plugins
        self.__presentation = presentation
        self.__show_stack_trace = show_stack_trace
        self.__handle_error = handle_error
        self.__continue_on_error = False

    # pylint: enable=too-many-arguments

    def process_files_to_scan(
        self,
        args: argparse.Namespace,
        use_standard_in: bool,
        files_to_scan: List[str],
        string_to_scan: Optional[str],
    ) -> Tuple[bool, bool]:
        """
        Process the specified files to scan, or the string to scan.
        """

        self.__continue_on_error = args.continue_on_error
        in_fix_mode = args.primary_subparser == FileScanHelper.__normal_fix_subcommand

        # sourcery skip: raise-specific-error
        did_fix_any_file = False
        did_fail_any_file = False
        if use_standard_in:
            assert not in_fix_mode, "Standard-in cannot be used with fix mode."
            POGGER.debug("Scanning from: (stdin)")
            self.__scan_from_stdin(args, string_to_scan)

        else:
            POGGER.debug("Scanning from: $", files_to_scan)
            for next_file in files_to_scan:
                if in_fix_mode:
                    did_fix_file, did_succeed = self.__fix_specific_file(
                        next_file,
                        next_file,
                        args.x_fix_debug,
                        args.x_fix_file_debug,
                        args.x_fix_no_rescan_log,
                    )
                    if did_fix_file:
                        self.__presentation.print_fix_message(next_file)
                        did_fix_any_file = True
                else:
                    did_succeed = self.__scan_specific_file(next_file, next_file)
                if not did_succeed:
                    did_fail_any_file = True
        return did_fix_any_file, did_fail_any_file

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

    def __scan_specific_file(self, next_file: str, next_file_name: str) -> bool:
        try:
            source_provider = FileSourceProvider(next_file)
            self.__scan_file(source_provider, next_file_name)
            return True
        except BadPluginError as this_exception:
            self.__handle_scan_error(next_file, this_exception, allow_shortcut=True)
        except BadTokenizationError as this_exception:
            if not self.__continue_on_error:
                raise
            self.__handle_scan_error(next_file, this_exception, allow_shortcut=True)
        return False

    def __scan_file(
        self, source_provider: FileSourceProvider, next_file_name: str
    ) -> None:  # sourcery skip: extract-method
        """
        Scan a given file and call the plugin manager for any significant events.
        """

        POGGER.info("Scanning file '$'.", next_file_name)
        context = None

        try:
            POGGER.info("Starting file '$'.", next_file_name)

            POGGER.info("Scanning file '$' token-by-token.", next_file_name)
            actual_tokens = self.__tokenizer.transform_from_provider(
                source_provider, do_add_end_of_stream_token=True
            )
            context = self.__plugins.starting_new_file(next_file_name, actual_tokens)

            source_provider.reset_to_start()
            self.__process_file_scan(
                context, source_provider, next_file_name, actual_tokens
            )

            context.report_on_triggered_rules()
            POGGER.info("Ending file '$'.", next_file_name)
        except Exception:
            if context:
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
    ) -> Tuple[bool, bool]:
        did_fix_file = False
        did_succeed = False
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
                did_succeed = True
            except Exception:
                POGGER.info("Ending file to fix '$' with exception.", next_file_name)
                raise
        except (BadPluginError, BadPluginFixError) as this_exception:
            self.__handle_scan_error(next_file, this_exception, allow_shortcut=True)
        except BadTokenizationError as this_exception:
            if not self.__continue_on_error:
                raise
            self.__handle_scan_error(next_file, this_exception, allow_shortcut=True)
        return did_fix_file, did_succeed

    # pylint: enable=too-many-arguments

    def __handle_scan_error(
        self, next_file: str, this_exception: Exception, allow_shortcut: bool = False
    ) -> None:
        if not self.__continue_on_error:
            allow_shortcut = False

        if allow_shortcut:
            show_extended_information = False
            print_prefix = ""
        else:
            show_extended_information = self.__show_stack_trace
            print_prefix = "\n\n"

        if formatted_error := self.__presentation.format_scan_error(
            next_file, this_exception, show_extended_information, allow_shortcut
        ):
            self.__handle_error(
                formatted_error, this_exception, not allow_shortcut, print_prefix
            )

        # If the `format_scan_error` call above returned None, it meant that
        # it handled any required output.  However, the application still needs
        # to terminate to respect that the error was called.
        #
        # update: the allow_shortcut variable allows for a shorter error to be
        #   logged to allow processing to continue.  When that happens, the
        #   application is not exitted.
        if not allow_shortcut:
            ReturnCodeHelper.exit_application(ApplicationResult.SYSTEM_ERROR)

    def __process_file_fix_rescan(
        self, fix_debug: bool, fix_nolog_rescan: bool, next_file_two: str
    ) -> List[MarkdownToken]:
        _ = fix_debug
        # if fix_debug:
        #     print(f"scan: {next_file_two}")
        POGGER.info("Rescanning file '$' before line-by-line fixes.", next_file_two)
        source_provider = FileSourceProvider(next_file_two)

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

    # pylint: disable=too-many-arguments, too-many-locals
    def __process_file_fix_pass(
        self,
        next_file: str,
        next_file_name: str,
        fix_debug: bool,
        fix_file_debug: bool,
        fix_nolog_rescan: bool,
        fix_list: List[str],
        collect_list: List[str],
    ) -> Tuple[bool, Set[str], Set[str]]:
        # Scan the provided file for any token fixes.
        (
            next_file_two,
            actual_tokens,
            did_any_tokens_get_fixed,
            collected_token_triggers,
        ) = self.__process_file_fix_tokens(
            next_file, next_file_name, fix_debug, fix_file_debug, fix_list, collect_list
        )

        # If tokens are returned, then no changes were made due to tokens and the
        # tokenized list can be reused without any worry of changes.
        if actual_tokens:
            assert (
                not did_any_tokens_get_fixed
            ), "Reusing tokens assumes that no tokens were fixed/changed."
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
            collected_line_triggers,
        ) = self.__process_file_fix_lines(
            next_file_two,
            next_file_name,
            actual_tokens,
            fix_debug,
            fix_file_debug,
            fix_list,
            collect_list,
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

        return did_anything_get_fixed, collected_token_triggers, collected_line_triggers

    # pylint: enable=too-many-arguments, too-many-locals

    # pylint: disable=too-many-arguments, too-many-locals
    def __process_file_fix_next_level(
        self,
        plugins_by_fix_level: Dict[int, List[str]],
        minimum_fix_level: int,
        fixes_by_id: Dict[str, FoundPlugin],
        next_file: str,
        next_file_name: str,
        fix_debug: bool,
        fix_file_debug: bool,
        fix_nolog_rescan: bool,
    ) -> Tuple[bool, bool, int]:
        keep_processing = False
        collect_list = []
        fix_list = []
        for fix_level, level_list in plugins_by_fix_level.items():
            if fix_level == minimum_fix_level:
                fix_list = level_list[:]
            elif fix_level > minimum_fix_level:
                collect_list.extend(level_list)
        assert fix_list is not None

        (
            did_anything_get_fixed_this_time,
            collected_token_triggers,
            collected_line_triggers,
        ) = self.__process_file_fix_pass(
            next_file,
            next_file_name,
            fix_debug,
            fix_file_debug,
            fix_nolog_rescan,
            fix_list,
            collect_list,
        )

        trigger_set = collected_token_triggers | collected_line_triggers
        new_minimum_fix_level: Optional[int] = None
        for next_triggered_plugin_id in trigger_set:
            triggered_plugin_fix_level = fixes_by_id[
                next_triggered_plugin_id
            ].plugin_fix_level
            assert (
                triggered_plugin_fix_level > minimum_fix_level
            ), "Triggered plugin levels should only increase."
            new_minimum_fix_level = (
                triggered_plugin_fix_level
                if new_minimum_fix_level is None
                else min(new_minimum_fix_level, triggered_plugin_fix_level)
            )
        if new_minimum_fix_level is not None:
            keep_processing = True
            minimum_fix_level = new_minimum_fix_level

        return keep_processing, did_anything_get_fixed_this_time, minimum_fix_level

    # pylint: enable=too-many-arguments, too-many-locals

    # pylint: disable=too-many-arguments, too-many-locals
    def __process_file_fix(
        self,
        next_file: str,
        next_file_name: str,
        fix_debug: bool,
        fix_file_debug: bool,
        fix_nolog_rescan: bool,
    ) -> bool:
        enabled_plugins_with_fixes = filter(
            lambda x: x.plugin_supports_fix, self.__plugins.enabled_plugins
        )
        fixes_by_id: Dict[str, FoundPlugin] = {
            i.plugin_id.lower(): i for i in enabled_plugins_with_fixes
        }

        enabled_plugins_with_fixes = filter(
            lambda x: x.plugin_supports_fix, self.__plugins.enabled_plugins
        )
        fix_plugins_with_levels = [
            (i.plugin_id, i.plugin_fix_level) for i in enabled_plugins_with_fixes
        ]

        plugins_by_fix_level: Dict[int, List[str]] = {}
        for next_pair in fix_plugins_with_levels:
            pair_plugin_id = next_pair[0]
            pair_fix_level = next_pair[1]
            if pair_fix_level in plugins_by_fix_level:
                level_list = plugins_by_fix_level[pair_fix_level]
            else:
                level_list = []
                plugins_by_fix_level[pair_fix_level] = level_list
            level_list.append(pair_plugin_id)
        minimum_fix_level = min(plugins_by_fix_level.keys())
        did_anything_get_fixed = False
        keep_processing = True

        while keep_processing:
            (
                keep_processing,
                did_anything_get_fixed_this_time,
                minimum_fix_level,
            ) = self.__process_file_fix_next_level(
                plugins_by_fix_level,
                minimum_fix_level,
                fixes_by_id,
                next_file,
                next_file_name,
                fix_debug,
                fix_file_debug,
                fix_nolog_rescan,
            )
            did_anything_get_fixed = (
                did_anything_get_fixed or did_anything_get_fixed_this_time
            )

        return did_anything_get_fixed

    # pylint: enable=too-many-arguments, too-many-locals

    # pylint: disable=too-many-arguments, too-many-locals
    def __process_file_fix_lines(
        self,
        next_file: str,
        next_file_name: str,
        actual_tokens: List[MarkdownToken],
        fix_debug: bool,
        fix_file_debug: bool,
        fix_list: List[str],
        collect_list: List[str],
    ) -> Tuple[List[FixLineRecord], str, Set[str]]:
        source_provider = FileSourceProvider(next_file)
        with tempfile.NamedTemporaryFile() as temp_output:
            temporary_file_name = temp_output.name
        with open(temporary_file_name, "wt", encoding="utf-8") as source_file:
            POGGER.info("Scanning before line-by-line fixes.")
            fix_context = self.__plugins.starting_new_file(
                next_file_name,
                actual_tokens,
                fix_mode=True,
                temp_output=source_file,
                fix_token_map=None,
            )
            report_context = self.__plugins.starting_new_file(
                next_file_name, actual_tokens, constraint_id_list=collect_list
            )
            context_map: Dict[str, PluginScanContext] = {
                i: fix_context for i in fix_list
            }
            for i in collect_list:
                context_map[i] = report_context

            # Due to context required to process the line requirements, we need go
            # through all the tokens first, before processing the lines.
            #
            # Basically, to allow any of the rules to build context applicable to
            # the line being scanned, we rescan the tokens to present an updated
            # picture of the tokens.
            for next_token in actual_tokens:
                POGGER.info("Processing tokens: $", next_token)
                self.__plugins.next_token(fix_context, next_token, context_map)

            POGGER.info("Completed token scanning.")
            self.__process_lines_in_file(
                source_provider, fix_context, next_file_name, context_map
            )
            this_file_fix_line_records = fix_context.fix_line_records
            if this_file_fix_line_records and fix_debug:
                for next_record in fix_context.fix_line_records:
                    print(next_record)

        self.__print_file_in_debug_mode(fix_debug, fix_file_debug, temporary_file_name)
        return (
            this_file_fix_line_records,
            temporary_file_name,
            report_context.get_triggered_rules(),
        )

    # pylint: enable=too-many-arguments, too-many-locals

    # pylint: disable=too-many-arguments, too-many-locals
    def __process_file_fix_tokens(
        self,
        next_file: str,
        next_file_name: str,
        fix_debug: bool,
        fix_file_debug: bool,
        fix_list: List[str],
        collect_list: List[str],
    ) -> Tuple[str, List[MarkdownToken], bool, Set[str]]:
        self.__print_file_in_debug_mode(fix_debug, fix_file_debug, next_file)

        POGGER.info("Scanning file to fix '$' token-by-token.", next_file_name)
        source_provider = FileSourceProvider(next_file)
        actual_tokens = self.__tokenizer.transform_from_provider(
            source_provider, do_add_end_of_stream_token=True
        )

        fix_token_map: Dict[MarkdownToken, List[FixTokenRecord]] = {}
        replace_tokens_list: List[ReplaceTokensRecord] = []
        fix_context = self.__plugins.starting_new_file(
            next_file_name,actual_tokens,
            fix_mode=True,
            temp_output=None,
            fix_token_map=fix_token_map,
            constraint_id_list=fix_list,
            replace_tokens_list=replace_tokens_list,
        )
        report_context = self.__plugins.starting_new_file(
            next_file_name, actual_tokens, constraint_id_list=collect_list
        )

        context_map = {i: fix_context for i in fix_list}
        for i in collect_list:
            context_map[i] = report_context

        for next_token in actual_tokens:
            POGGER.info("Processing token: $", next_token)
            self.__plugins.next_token(fix_context, next_token, context_map)

        POGGER.info("Completed scanning file '$' for fixes.", next_file_name)
        self.__plugins.completed_file(fix_context, -1, context_map)

        did_any_tokens_get_fixed = False
        if fix_context.get_fix_token_map() or fix_context.get_replace_tokens_list():
            (
                next_file,
                actual_tokens,
                did_any_tokens_get_fixed,
            ) = self.__process_file_fix_tokens_apply_fixes(
                fix_context,
                next_file,
                actual_tokens,
                fix_token_map,
                fix_debug,
                fix_file_debug,
                replace_tokens_list,
            )
        return (
            next_file,
            actual_tokens,
            did_any_tokens_get_fixed,
            report_context.get_triggered_rules(),
        )

    # pylint: enable=too-many-arguments, too-many-locals

    def __look_for_collisions(
        self,
        next_replacement: ReplaceTokensRecord,
        actual_tokens: List[MarkdownToken],
        fixed_token_indices: Dict[int, List[str]],
        replaced_token_indices: Dict[int, str],
    ) -> None:
        start_index = actual_tokens.index(next_replacement.start_token)
        end_index = actual_tokens.index(next_replacement.end_token)
        next_match_with_fixed_tokens = next(
            (i for i in range(start_index, end_index + 1) if i in fixed_token_indices),
            None,
        )
        if next_match_with_fixed_tokens is not None:
            previous_plugin_ids = ",".join(
                fixed_token_indices[next_match_with_fixed_tokens]
            )
            POGGER.info(
                "Previous plugins ($) set one or more fields for the current token.",
                previous_plugin_ids,
            )
            POGGER.info(
                "Current plugin ($) wants to replace the token with another token.",
                next_replacement.plugin_id,
            )

            raise BadPluginFixError(
                f"Multiple plugins ({previous_plugin_ids} and {next_replacement.plugin_id}) are in conflict about fixing the token."
            )
        for next_index in range(start_index, end_index + 1):
            if next_index in replaced_token_indices:
                POGGER.info(
                    "Previous plugin ($) replaced the token.",
                    replaced_token_indices[next_index],
                )
                POGGER.info(
                    "Current plugin ($) wants to replace the same token with another token.",
                    next_replacement.plugin_id,
                )

                raise BadPluginFixError(
                    f"Multiple plugins ({replaced_token_indices[next_index]} and {next_replacement.plugin_id}) are in conflict about replacing the token."
                )
            replaced_token_indices[next_index] = next_replacement.plugin_id

    def __apply_replacement_fix(
        self,
        context: PluginScanContext,
        next_replacement: ReplaceTokensRecord,
        actual_tokens: List[MarkdownToken],
    ) -> None:
        start_index = actual_tokens.index(next_replacement.start_token)
        end_index = actual_tokens.index(next_replacement.end_token)
        actual_start_index = start_index
        while (
            actual_start_index < end_index
            and actual_tokens[actual_start_index].is_end_token
        ):
            actual_start_index += 1
        line_number_delta_1 = (
            next_replacement.end_token.line_number
            - actual_tokens[actual_start_index].line_number
        ) + 1
        line_number_delta_2 = (
            next_replacement.replacement_tokens[-1].line_number
            - next_replacement.replacement_tokens[0].line_number
        ) + 1
        line_number_delta = line_number_delta_2 - line_number_delta_1

        new_tokens = actual_tokens[:start_index]
        new_tokens.extend(next_replacement.replacement_tokens)
        end_tokens = actual_tokens[end_index + 1 :]
        for next_token in end_tokens:
            next_token.adjust_line_number(context, line_number_delta)
        new_tokens.extend(end_tokens)

        if new_tokens[-1].is_pragma:
            pragma_token = cast(PragmaToken, new_tokens[-1])
            for pragma_line_number in sorted(pragma_token.pragma_lines.keys())[::-1]:
                if pragma_line_number > next_replacement.end_token.line_number:
                    pragma_token.adjust_pragma_line_number(
                        pragma_line_number, pragma_line_number + line_number_delta
                    )

        actual_tokens.clear()
        actual_tokens.extend(new_tokens)

    # pylint: disable=too-many-arguments
    def __apply_replacements(
        self,
        fix_debug: bool,
        context: PluginScanContext,
        did_any_tokens_get_fixed: bool,
        replace_tokens_list: List[ReplaceTokensRecord],
        actual_tokens: List[MarkdownToken],
        fixed_token_indices: Dict[int, List[str]],
        replaced_token_indices: Dict[int, str],
    ) -> bool:
        for next_replace_index in replace_tokens_list:
            self.__look_for_collisions(
                next_replace_index,
                actual_tokens,
                fixed_token_indices,
                replaced_token_indices,
            )

        # did_fix = False
        if fix_debug:
            print("TOKENS-----")
            for i, j in enumerate(actual_tokens):
                print(f" {i:02}:{ParserHelper.make_value_visible(j)}")
            print("TOKENS-----")
        for next_replace_index in replace_tokens_list:
            did_any_tokens_get_fixed = True
            # if fix_debug and not did_fix:
            #     did_fix = True
            #     print("BEFORE-XXX-----")
            #     for i,j in enumerate(actual_tokens):
            #         print(f" {i:02}:{ParserHelper.make_value_visible(j)}")
            #     print("BEFORE-XXX-----")
            if fix_debug:
                print(f" {ParserHelper.make_value_visible(next_replace_index)}")
            self.__apply_replacement_fix(context, next_replace_index, actual_tokens)
        if fix_debug:
            print("TOKENS-----")
            for i, j in enumerate(actual_tokens):
                print(f" {i:02}:{ParserHelper.make_value_visible(j)}")
            print("TOKENS-----")
        return did_any_tokens_get_fixed

    # pylint: enable=too-many-arguments

    # pylint: disable=too-many-arguments
    def __process_file_fix_tokens_apply_fixes(
        self,
        context: PluginScanContext,
        next_file: str,
        actual_tokens: List[MarkdownToken],
        fix_token_map: Dict[MarkdownToken, List[FixTokenRecord]],
        fix_debug: bool,
        fix_file_debug: bool,
        replace_tokens_list: List[ReplaceTokensRecord],
    ) -> Tuple[str, List[MarkdownToken], bool]:

        did_any_tokens_get_fixed = self.__process_file_fix_tokens_apply_fixes_inner(
            context, fix_debug, actual_tokens, replace_tokens_list, fix_token_map
        )

        transformer = TransformToMarkdown()
        markdown_from_tokens = transformer.transform(actual_tokens)

        if fix_debug:
            print(f"MARKDOWN:{ParserHelper.make_value_visible(markdown_from_tokens)}")
        with tempfile.NamedTemporaryFile() as temp_output:
            temporary_file_name = temp_output.name
        with open(temporary_file_name, "wt", encoding="utf-8") as source_file:
            source_file.write(markdown_from_tokens)
            next_file = temporary_file_name
            actual_tokens.clear()

        self.__print_file_in_debug_mode(fix_debug, fix_file_debug, temporary_file_name)
        return next_file, actual_tokens, did_any_tokens_get_fixed

    # pylint: enable=too-many-arguments

    # pylint: disable=too-many-arguments
    def __process_file_fix_tokens_apply_fixes_inner(
        self,
        context: PluginScanContext,
        fix_debug: bool,
        actual_tokens: List[MarkdownToken],
        replace_tokens_list: List[ReplaceTokensRecord],
        fix_token_map: Dict[MarkdownToken, List[FixTokenRecord]],
    ) -> bool:
        fixed_token_indices: Dict[int, List[str]] = {}
        replaced_token_indices: Dict[int, str] = {}

        did_any_tokens_get_fixed = False
        if fix_debug:
            print("--")
        for token_instance, requested_fixes in context.get_fix_token_map().items():
            if fix_debug:
                print(f"APPLY:{ParserHelper.make_value_visible(requested_fixes)}")
                print(f"BEFORE:{ParserHelper.make_value_visible(token_instance)}")
            self.__apply_token_fix(
                context, token_instance, requested_fixes, actual_tokens
            )
            actual_token_index = actual_tokens.index(token_instance)
            fixed_token_indices[actual_token_index] = [
                i.plugin_id for i in requested_fixes
            ]
            if fix_debug:
                print(f" AFTER:{ParserHelper.make_value_visible(token_instance)}")
        if fix_debug:
            print("--")
        did_any_tokens_get_fixed = self.__apply_replacements(
            fix_debug,
            context,
            did_any_tokens_get_fixed,
            replace_tokens_list,
            actual_tokens,
            fixed_token_indices,
            replaced_token_indices,
        )
        if fix_debug:
            print("--")

        did_any_tokens_get_fixed = did_any_tokens_get_fixed or bool(fix_token_map)
        return did_any_tokens_get_fixed

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
        context_map: Optional[Dict[str, PluginScanContext]] = None,
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
                context_map,
            )
            line_number += 1
            next_line = source_provider.get_next_line()

        POGGER.info("Completed scanning lines in file '$'.", next_file_name)
        self.__plugins.completed_file(context, line_number, context_map)

    @staticmethod
    def is_scan_stdin_specified(args: argparse.Namespace) -> bool:
        """
        Specifies whether scanning from stdin was specified.
        """
        return FileScanHelper.__stdin_scan_subcommand == args.primary_subparser  # type: ignore

    @staticmethod
    def add_argparse_subparser(subparsers: argparse._SubParsersAction, is_fix_mode: bool) -> None:  # type: ignore
        """
        Add the subparser for scanning.
        """
        subparser_action = "fix" if is_fix_mode else "scan"
        subparser_command = (
            FileScanHelper.__normal_fix_subcommand
            if is_fix_mode
            else FileScanHelper.__normal_scan_subcommand
        )

        new_sub_parser = subparsers.add_parser(
            subparser_command,
            help=f"{subparser_action} the Markdown files in any specified paths",
        )
        ApplicationFileScanner.add_default_command_line_arguments(
            new_sub_parser, ".md", "Markdown"
        )

        if not is_fix_mode:
            subparsers.add_parser(
                FileScanHelper.__stdin_scan_subcommand,
                help="scan the standard input as a Markdown file",
            )
