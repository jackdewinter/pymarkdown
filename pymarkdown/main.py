"""
Module to provide for a simple implementation of a title case algorithm.
"""
import argparse
import glob
import logging
import os
import runpy
import sys
import traceback

from pymarkdown.application_properties import (
    ApplicationProperties,
    ApplicationPropertiesJsonLoader,
)
from pymarkdown.bad_tokenization_error import BadTokenizationError
from pymarkdown.parser_logger import ParserLogger
from pymarkdown.plugin_manager import BadPluginError, PluginManager
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

    def __init__(self):
        self.__version_number = PyMarkdownLint.__get_semantic_version()
        self.__show_stack_trace = False

        self.__properties = ApplicationProperties()

        self.__plugins = PluginManager()
        self.__tokenizer = None
        self.default_log_level = "CRITICAL"

    @staticmethod
    def __get_semantic_version():
        file_path = __file__
        if not os.path.isabs(file_path):
            assert False
        file_path = file_path.replace(os.sep, "/")
        last_index = file_path.rindex("/")
        file_path = file_path[0 : last_index + 1] + "version.py"
        version_meta = runpy.run_path(file_path)
        return version_meta["__version__"]

    @staticmethod
    def log_level_type(argument):
        """
        Function to help argparse limit the valid log levels.
        """
        if argument in PyMarkdownLint.available_log_maps:
            return argument
        raise ValueError(f"Value '{argument}' is not a valid log level.")

    def __parse_arguments(self):
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

        new_sub_parser = subparsers.add_parser(
            "scan", help="scan the Markdown files in the specified paths"
        )
        new_sub_parser.add_argument(
            "-l",
            "--list-files",
            dest="list_files",
            action="store_true",
            default=False,
            help="list the markdown files found and exit",
        )
        new_sub_parser.add_argument(
            "-r",
            "--recurse",
            dest="recurse_directories",
            action="store_true",
            default=False,
            help="recursively scan directories",
        )
        new_sub_parser.add_argument(
            "paths",
            metavar="path",
            type=str,
            nargs="+",
            help="one or more paths to scan for eligible Markdown files",
        )

        subparsers.add_parser("version", help="version of the application")

        print("args:" + str(sys.argv))
        parse_arguments = parser.parse_args()

        if not parse_arguments.primary_subparser:
            parser.print_help()
            sys.exit(2)
        elif parse_arguments.primary_subparser == "version":
            print(f"{self.__version_number}")
            sys.exit(0)
        return parse_arguments

    @classmethod
    def __is_file_eligible_to_scan(cls, path_to_test):
        """
        Determine if the presented path is one that we want to scan.
        """
        return path_to_test.endswith(".md")

    # pylint: disable=broad-except
    def __scan_file(self, args, next_file):
        """
        Scan a given file and call the plugin manager for any significant events.
        """

        POGGER.info("Scanning file '$'.", next_file)
        context = self.__plugins.starting_new_file(next_file)

        POGGER.info("Scanning file '$' token-by-token.", next_file)
        source_provider = FileSourceProvider(next_file)
        if args.x_test_scan_fault:
            source_provider = None
        actual_tokens = self.__tokenizer.transform_from_provider(source_provider)

        if actual_tokens and actual_tokens[-1].is_pragma:
            self.__plugins.compile_pragmas(next_file, actual_tokens[-1])
            actual_tokens = actual_tokens[:-1]

        POGGER.info("Scanning file '$' tokens.", next_file)
        for next_token in actual_tokens:
            POGGER.info("Processing token: $", next_token)
            self.__plugins.next_token(context, next_token)

        POGGER.info("Scanning file '$' line-by-line.", next_file)
        source_provider = FileSourceProvider(next_file)
        line_number = 1
        next_line = source_provider.get_next_line()
        while next_line is not None:
            POGGER.info("Processing line $: $", line_number, next_line)
            self.__plugins.next_line(context, line_number, next_line)
            line_number += 1
            next_line = source_provider.get_next_line()

        POGGER.info("Completed scanning file '$'.", next_file)
        self.__plugins.completed_file(context, line_number)

    # pylint: enable=broad-except

    def __process_next_path(self, next_path, files_to_parse, recurse_directories):

        did_find_any = False
        POGGER.info("Determining files to scan for path '$'.", next_path)
        if not os.path.exists(next_path):
            print(
                f"Provided path '{next_path}' does not exist.",
                file=sys.stderr,
            )
            POGGER.debug("Provided path '$' does not exist.", next_path)
        elif os.path.isdir(next_path):
            POGGER.debug(
                "Provided path '$' is a directory. Walking directory.", next_path
            )
            did_find_any = True
            normalized_next_path = next_path.replace("\\", "/")
            for root, _, files in os.walk(next_path):
                normalized_root = root.replace("\\", "/")
                if not recurse_directories and normalized_root != normalized_next_path:
                    continue
                normalized_root = (
                    normalized_root[0:-1]
                    if normalized_root.endswith("/")
                    else normalized_root
                )
                for file in files:
                    rooted_file_path = f"{normalized_root}/{file}"
                    if self.__is_file_eligible_to_scan(rooted_file_path):
                        files_to_parse.add(rooted_file_path)
        else:
            if self.__is_file_eligible_to_scan(next_path):
                POGGER.debug(
                    "Provided path '$' is a valid file. Adding.",
                    next_path,
                )
                files_to_parse.add(next_path)
                did_find_any = True
            else:
                POGGER.debug(
                    "Provided path '$' is not a valid file. Skipping.",
                    next_path,
                )
                print(
                    f"Provided file path '{next_path}' is not a valid file. Skipping.",
                    file=sys.stderr,
                )
        return did_find_any

    def __determine_files_to_scan(self, eligible_paths, recurse_directories):

        did_error_scanning_files = False
        files_to_parse = set()
        for next_path in eligible_paths:
            if "*" in next_path or "?" in next_path:
                globbed_paths = glob.glob(next_path)
                if not globbed_paths:
                    print(
                        f"Provided glob path '{next_path}' did not match any files.",
                        file=sys.stderr,
                    )
                    did_error_scanning_files = True
                    break
                for next_globbed_path in globbed_paths:
                    next_globbed_path = next_globbed_path.replace("\\", "/")
                    self.__process_next_path(
                        next_globbed_path, files_to_parse, recurse_directories
                    )
            else:
                if not self.__process_next_path(
                    next_path, files_to_parse, recurse_directories
                ):
                    did_error_scanning_files = True
                    break

        files_to_parse = list(files_to_parse)
        files_to_parse.sort()

        POGGER.info("Number of files found: $", len(files_to_parse))
        return files_to_parse, did_error_scanning_files

    @classmethod
    def __handle_list_files(cls, files_to_scan):

        if files_to_scan:
            print("\n".join(files_to_scan))
            return 0
        print("No matching files found.", file=sys.stderr)
        return 1

    def __apply_configuration_to_plugins(self):

        try:
            self.__plugins.apply_configuration(self.__properties)
        except BadPluginError as this_exception:
            formatted_error = f"{str(type(this_exception).__name__)} encountered while configuring plugins:\n{str(this_exception)}"
            self.__handle_error(formatted_error, this_exception)

    def __initialize_parser(self, args):

        resource_path = None
        if args.x_test_init_fault:
            resource_path = "fredo"

        try:
            self.__tokenizer = TokenizedMarkdown(resource_path)
            self.__tokenizer.apply_configuration(self.__properties)
        except ValueError as this_exception:
            formatted_error = "Configuration Error: " + str(this_exception)
            self.__handle_error(formatted_error, this_exception)
        except BadTokenizationError as this_exception:
            formatted_error = f"{str(type(this_exception).__name__)} encountered while initializing tokenizer:\n{str(this_exception)}"
            self.__handle_error(formatted_error, this_exception)

    def __initialize_plugin_manager(self, args, plugin_dir):
        """
        Make sure all plugins are ready before being initialized.
        """

        self.__plugins = PluginManager()
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
            formatted_error = f"BadPluginError encountered while loading plugins:\n{str(this_exception)}"
            self.__handle_error(formatted_error, this_exception)

    def __handle_error(self, formatted_error, thrown_error):

        show_error = self.__show_stack_trace or not isinstance(thrown_error, ValueError)
        LOGGER.warning(formatted_error, exc_info=show_error)

        print(f"\n\n{formatted_error}", file=sys.stderr)
        if self.__show_stack_trace:
            traceback.print_exc(file=sys.stderr)
        sys.exit(1)

    def __handle_scan_error(self, next_file, this_exception):

        formatted_error = f"{str(type(this_exception).__name__)} encountered while scanning '{next_file}':\n{str(this_exception)}"
        self.__handle_error(formatted_error, this_exception)

    def __set_initial_state(self, args):

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

    def __initialize_strict_mode(self, args):
        effective_strict_configuration = args.strict_configuration
        if not effective_strict_configuration:
            effective_strict_configuration = self.__properties.get_boolean_property(
                "mode.strict-config", strict_mode=True
            )

        if effective_strict_configuration:
            self.__properties.enable_strict_mode()

    def __initialize_logging(self, args):

        new_handler = None

        effective_log_file = args.log_file
        if effective_log_file is None:
            effective_log_file = self.__properties.get_string_property("log.file")

        if effective_log_file:
            new_handler = logging.FileHandler(effective_log_file)
            logging.getLogger().addHandler(new_handler)
        else:
            temp_log_level = (
                logging.DEBUG if self.__show_stack_trace else logging.CRITICAL
            )
            logging.basicConfig(stream=sys.stdout, level=temp_log_level)

        effective_log_level = args.log_level if args.log_level else None
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

    def __initialize_plugins(self, args):
        try:
            plugin_dir = os.path.dirname(os.path.realpath(__file__))
            plugin_dir = os.path.join(plugin_dir, "plugins")
            self.__initialize_plugin_manager(args, plugin_dir)
            self.__apply_configuration_to_plugins()
        except ValueError as this_exception:
            formatted_error = f"{str(type(this_exception).__name__)} encountered while initializing plugins:\n{str(this_exception)}"
            self.__handle_error(formatted_error, this_exception)

    def main(self):
        """
        Main entrance point.
        """
        args = self.__parse_arguments()
        print(">>init_state>" + str(args))
        self.__set_initial_state(args)

        new_handler = None
        total_error_count = 0
        try:
            print(">>__initialize_strict_mode")
            self.__initialize_strict_mode(args)
            print(">>__initialize_logging")
            new_handler = self.__initialize_logging(args)

            if args.primary_subparser == PluginManager.argparse_subparser_name():
                self.__initialize_plugins(args)
                return_code = self.__plugins.handle_argparse_subparser(args)
                sys.exit(return_code)

            POGGER.info("Determining files to scan.")
            files_to_scan, did_error_scanning_files = self.__determine_files_to_scan(
                args.paths, args.recurse_directories
            )
            if did_error_scanning_files:
                total_error_count = 1
            else:
                self.__initialize_plugins(args)
                self.__initialize_parser(args)

                if args.list_files:
                    POGGER.info(
                        "Sending list of files that would have been scanned to stdout."
                    )
                    return_code = self.__handle_list_files(files_to_scan)
                    sys.exit(return_code)

                for next_file in files_to_scan:
                    try:
                        self.__scan_file(args, next_file)
                    except BadPluginError as this_exception:
                        self.__handle_scan_error(next_file, this_exception)
                    except BadTokenizationError as this_exception:
                        self.__handle_scan_error(next_file, this_exception)
        except ValueError as this_exception:
            formatted_error = f"Configuration Error: {this_exception}"
            self.__handle_error(formatted_error, this_exception)
        finally:
            if new_handler:
                new_handler.close()

        # TODO self.__plugins.number_of_pragma_failures
        if self.__plugins.number_of_scan_failures or total_error_count:
            sys.exit(1)


if __name__ == "__main__":
    PyMarkdownLint().main()
