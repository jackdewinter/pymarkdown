"""
Module to provide for a simple implementation of a title case algorithm.
"""
import argparse
import os
import sys
import traceback
import logging

from pymarkdown.plugin_manager import BadPluginError, PluginManager
from pymarkdown.source_providers import FileSourceProvider
from pymarkdown.tokenized_markdown import TokenizedMarkdown


# https://github.com/hiddenillusion/example-code/commit/3e2daada652fe9b487574c784e0924bd5fcfe667
# TODO check
class PyMarkdownLint:
    """
    Class to provide for a simple implementation of a title case algorithm.
    """

    def __init__(self):
        self.version_number = "0.1.0"

        self.plugins = PluginManager()
        self.logger = logging.getLogger(__name__)

    def __parse_arguments(self):
        parser = argparse.ArgumentParser(description="Lint any found Markdown files.")

        parser.add_argument(
            "--version", action="version", version="%(prog)s " + self.version_number
        )

        parser.add_argument(
            "-l",
            "--list-files",
            dest="list_files",
            action="store_true",
            default=False,
            help="list the markdown files found and exit",
        )
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
            "--add-plugin",
            dest="add_plugin",
            action="append",
            default=None,
            help="path to a plugin containing a new rule to apply",
        )
        parser.add_argument(
            "--stack-trace",
            dest="show_stack_trace",
            action="store_true",
            default=False,
            help="if an error occurs, print out the stack trace for debug purposes",
        )
        parser.add_argument(
            "paths",
            metavar="path",
            type=str,
            nargs="+",
            help="One or more paths to scan for eligible files",
        )
        return parser.parse_args()

    @classmethod
    def is_file_eligible_to_scan(cls, path_to_test):
        """
        Determine if the presented path is one that we want to scan.
        """
        return path_to_test.endswith(".md")

    def __scan_file(self, next_file):
        """
        Scan a given file and call the plugin manager for any significant events.
        """

        source_provider = FileSourceProvider(next_file)

        line_number = 1
        next_line = source_provider.get_next_line()
        context = self.plugins.starting_new_file(next_file)
        while not next_line is None:
            self.plugins.next_line(context, line_number, next_line)
            line_number += 1
            next_line = source_provider.get_next_line()
        self.plugins.completed_file(context, line_number)

        tokenizer = TokenizedMarkdown()
        source_provider = FileSourceProvider(next_file)
        try:
            actual_tokens = tokenizer.transform_from_provider(source_provider)
            self.logger.debug(">>" + str(actual_tokens) + "<<")
        except Exception:
            print("Exception encountered parsing document:\n")
            traceback.print_exc(file=sys.stdout)

    @classmethod
    def __determine_files_to_scan(cls, eligible_paths):

        files_to_parse = set()
        for next_path in eligible_paths:

            if not os.path.exists(next_path):
                print(
                    "Provided path '" + next_path + "' does not exist. Skipping.",
                    file=sys.stderr,
                )
                continue
            if os.path.isdir(next_path):
                for root, _, files in os.walk(next_path):
                    for file in files:
                        rooted_file_path = root + "/" + file
                        if cls.is_file_eligible_to_scan(rooted_file_path):
                            files_to_parse.add(rooted_file_path)
            else:
                if cls.is_file_eligible_to_scan(next_path):
                    files_to_parse.add(next_path)
                else:
                    print(
                        "Provided file path '"
                        + next_path
                        + "' is not a valid markdown file. Skipping.",
                        file=sys.stderr,
                    )
        files_to_parse = list(files_to_parse)
        files_to_parse.sort()
        return files_to_parse

    @classmethod
    def __handle_list_files(cls, files_to_scan):

        if files_to_scan:
            print("\n".join(files_to_scan))
            return 0
        print("No Markdown files found.", file=sys.stderr)
        return 1

    def __initialize_plugins(self, args, plugin_dir):
        """
        Make sure all plugins are ready before being initialized.
        """

        try:
            self.plugins.initialize(
                plugin_dir, args.add_plugin, args.enable_rules, args.disable_rules
            )
        except BadPluginError as this_exception:
            print(
                "BadPluginError encountered while loading plugins:\n"
                + str(this_exception),
                file=sys.stderr,
            )
            if args.show_stack_trace:
                traceback.print_exc(file=sys.stderr)
            sys.exit(1)

    def main(self):
        """
        Main entrance point.
        """
        args = self.__parse_arguments()

        #logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)

        files_to_scan = self.__determine_files_to_scan(args.paths)
        if args.list_files:
            return_code = self.__handle_list_files(files_to_scan)
            sys.exit(return_code)

        plugin_dir = os.path.dirname(os.path.realpath(__file__))
        plugin_dir = os.path.join(plugin_dir, "plugins")
        self.__initialize_plugins(args, plugin_dir)

        for next_file in files_to_scan:
            try:
                self.__scan_file(next_file)
            except BadPluginError as this_exception:
                print(
                    "BadPluginError encountered while scanning '"
                    + next_file
                    + "':\n"
                    + str(this_exception),
                    file=sys.stderr,
                )
                if args.show_stack_trace:
                    traceback.print_exc(file=sys.stderr)
                sys.exit(1)

        if self.plugins.number_of_scan_failures:
            sys.exit(1)


if __name__ == "__main__":
    PyMarkdownLint().main()
