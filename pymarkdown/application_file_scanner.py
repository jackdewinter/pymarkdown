"""
Module to provide for a simplified way to scan for files.
"""

import argparse
import glob
import logging
import os
from typing import List, Optional, Set, Tuple

from typing_extensions import Protocol

LOGGER = logging.getLogger(__name__)


# pylint: disable=too-few-public-methods
class ApplicationFileScannerOutputProtocol(Protocol):
    """
    Protocol to provide for redirection of output (standard or error).
    """

    def __call__(
        self,
        output_string: str,
    ) -> None: ...  # pragma: no cover


# pylint: enable=too-few-public-methods


class ApplicationFileScanner:
    """
    Class to provide for a simplified way to scan for files.
    """

    @staticmethod
    def determine_files_to_scan_with_args(
        args: argparse.Namespace,
        handle_output: ApplicationFileScannerOutputProtocol,
        handle_error: ApplicationFileScannerOutputProtocol,
    ) -> Tuple[List[str], bool, bool]:
        """
        Determine the files to scan based on the arguments provided by the `add_default_command_line_arguments` function.
        """
        return ApplicationFileScanner.determine_files_to_scan(
            args.paths,
            args.recurse_directories,
            args.alternate_extensions,
            args.list_files,
            handle_output,
            handle_error,
        )

    # pylint: disable=too-many-arguments
    @staticmethod
    def determine_files_to_scan(
        eligible_paths: List[str],
        recurse_directories: bool,
        eligible_extensions: str,
        only_list_files: bool,
        handle_output: ApplicationFileScannerOutputProtocol,
        handle_error: ApplicationFileScannerOutputProtocol,
    ) -> Tuple[List[str], bool, bool]:
        """
        Determine the files to scan, and how to scan for those files.
        """
        split_eligible_extensions: List[str] = eligible_extensions.split(",")

        did_error_scanning_files = False
        files_to_parse: Set[str] = set()
        for next_path in eligible_paths:
            if "*" in next_path or "?" in next_path:
                globbed_paths = glob.glob(next_path)
                if not globbed_paths:
                    handle_error(
                        f"Provided glob path '{next_path}' did not match any files."
                    )
                    did_error_scanning_files = True
                    break
                for next_globbed_path in globbed_paths:
                    ApplicationFileScanner.__process_next_path(
                        next_globbed_path,
                        files_to_parse,
                        recurse_directories,
                        split_eligible_extensions,
                        handle_error,
                    )
            elif not ApplicationFileScanner.__process_next_path(
                next_path,
                files_to_parse,
                recurse_directories,
                split_eligible_extensions,
                handle_error,
            ):
                did_error_scanning_files = True
                break

        sorted_files_to_parse = sorted(files_to_parse)
        LOGGER.info("Number of files found: %d", len(sorted_files_to_parse))
        did_only_list_files = ApplicationFileScanner.__handle_main_list_files(
            only_list_files, sorted_files_to_parse, handle_output, handle_error
        )
        return sorted_files_to_parse, did_error_scanning_files, did_only_list_files

    # pylint: enable=too-many-arguments

    @staticmethod
    def __process_next_path(
        next_path: str,
        files_to_parse: Set[str],
        recurse_directories: bool,
        eligible_extensions: List[str],
        handle_error: ApplicationFileScannerOutputProtocol,
    ) -> bool:
        did_find_any = False
        LOGGER.info("Determining files to scan for path '%s'.", next_path)
        if not os.path.exists(next_path):
            handle_error(f"Provided path '{next_path}' does not exist.")
            LOGGER.debug("Provided path '%s' does not exist.", next_path)
        elif os.path.isdir(next_path):
            ApplicationFileScanner.__process_next_path_directory(
                next_path, files_to_parse, recurse_directories, eligible_extensions
            )
            did_find_any = True
        elif ApplicationFileScanner.__is_file_eligible_to_scan(
            next_path, eligible_extensions
        ):
            LOGGER.debug(
                "Provided path '%s' is a valid file. Adding.",
                next_path,
            )
            normalized_path = (
                next_path.replace(os.altsep, os.sep) if os.altsep else next_path
            )
            files_to_parse.add(normalized_path)
            did_find_any = True
        else:
            LOGGER.debug(
                "Provided path '%s' is not a valid file. Skipping.",
                next_path,
            )
            handle_error(
                f"Provided file path '{next_path}' is not a valid file. Skipping."
            )
        return did_find_any

    @staticmethod
    def __process_next_path_directory(
        next_path: str,
        files_to_parse: Set[str],
        recurse_directories: bool,
        eligible_extensions: List[str],
    ) -> None:
        LOGGER.debug("Provided path '%s' is a directory. Walking directory.", next_path)
        normalized_next_path = (
            next_path.replace(os.altsep, os.sep) if os.altsep else next_path
        )
        for root, _, files in os.walk(normalized_next_path):
            normalized_root = root.replace(os.altsep, os.sep) if os.altsep else root
            if not recurse_directories and normalized_root != normalized_next_path:
                continue
            normalized_root = (
                normalized_root[:-1]
                if normalized_root.endswith(os.sep)
                else normalized_root
            )
            for file in files:
                rooted_file_path = f"{normalized_root}{os.sep}{file}"
                if ApplicationFileScanner.__is_file_eligible_to_scan(
                    rooted_file_path, eligible_extensions
                ):
                    files_to_parse.add(rooted_file_path)

    @staticmethod
    def __is_file_eligible_to_scan(
        path_to_test: str, eligible_extensions: List[str]
    ) -> bool:
        """
        Determine if the presented path is one that we want to scan.
        """
        return os.path.isfile(path_to_test) and any(
            path_to_test.endswith(next_extension)
            for next_extension in eligible_extensions
        )

    # pylint: disable=too-many-arguments
    @staticmethod
    def add_default_command_line_arguments(
        parser_to_add_to: argparse.ArgumentParser,
        extension_to_look_for: str,
        file_type_name: Optional[str] = None,
        show_list_files: bool = True,
        show_recurse_directories: bool = True,
        show_alternate_extensions: bool = True,
    ) -> None:
        """
        Add a set of default command line arguments to an argparse styled command line.
        """
        if argument_error := ApplicationFileScanner.__is_valid_extension(
            extension_to_look_for
        ):
            raise argparse.ArgumentTypeError(
                f"Extension '{extension_to_look_for}' is not a valid extension: {argument_error}"
            )

        specific_file_type_name = ""
        if file_type_name is not None:
            if file_type_name := file_type_name.strip():
                specific_file_type_name = f"{file_type_name} "

        if show_list_files:
            parser_to_add_to.add_argument(
                "-l",
                "--list-files",
                dest="list_files",
                action="store_true",
                default=False,
                help=f"list any eligible {specific_file_type_name}files found on the specified paths and exit",
            )

        if show_recurse_directories:
            parser_to_add_to.add_argument(
                "-r",
                "--recurse",
                dest="recurse_directories",
                action="store_true",
                default=False,
                help="recursively traverse any found directories for matching files",
            )

        if show_alternate_extensions:
            parser_to_add_to.add_argument(
                "-ae",
                "--alternate-extensions",
                dest="alternate_extensions",
                action="store",
                default=extension_to_look_for,
                type=ApplicationFileScanner.is_valid_comma_separated_extension_list,
                help="provide an alternate set of file extensions to match against",
            )

        parser_to_add_to.add_argument(
            "paths",
            metavar="path",
            type=str,
            nargs="+",
            default=None,
            help=f"one or more paths to examine for eligible {specific_file_type_name}files",
        )

    # pylint: enable=too-many-arguments

    @staticmethod
    def __is_valid_extension(possible_extension: str) -> Optional[str]:
        """
        Determine if the parameter is a string that has the form of a valid extension.
        """
        if not possible_extension.startswith("."):
            return f"Extension '{possible_extension}' must start with a period."
        return (
            next(
                (
                    f"Extension '{possible_extension}' must only contain alphanumeric characters after the period."
                    for clean_split_char in clean_split
                    if not clean_split_char.isalnum()
                ),
                None,
            )
            if (clean_split := possible_extension[1:])
            else f"Extension '{possible_extension}' must have at least one character after the period."
        )

    @staticmethod
    def is_valid_comma_separated_extension_list(argument: str) -> str:
        """
        Function to help argparse verify whether a comma separated list contains valid extensions.
        """
        split_argument = argument.split(",")
        for next_split in split_argument:
            if error_string := ApplicationFileScanner.__is_valid_extension(next_split):
                raise argparse.ArgumentTypeError(error_string)
        return argument.lower()

    @staticmethod
    def __handle_main_list_files(
        only_list_files: bool,
        files_to_scan: List[str],
        handle_output: ApplicationFileScannerOutputProtocol,
        handle_error: ApplicationFileScannerOutputProtocol,
    ) -> bool:
        if did_list_files := only_list_files:
            LOGGER.info("Sending list of files that would have been scanned to stdout.")
            if files_to_scan:
                handle_output("\n".join(files_to_scan))
            else:
                handle_error("No matching files found.")
        return did_list_files
