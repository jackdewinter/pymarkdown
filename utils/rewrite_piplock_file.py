"""
Module to provide for a simple script to remove packages from the Pipfile if their required version is not met.
"""

import argparse
import re
import sys
from typing import List, Optional


class RewritePiplockException(Exception):
    """Custom exception for errors during piplock file rewriting."""


# Load a file's entire content into a string safely
def __load_file_as_string(file_path: str, encoding: str = "utf-8") -> List[str]:
    try:
        with open(file_path, "r", encoding=encoding) as file:
            return file.read().splitlines()
    except FileNotFoundError as this_exception:
        raise RewritePiplockException(
            f"Error: File '{file_path}' not found."
        ) from this_exception
    except UnicodeDecodeError as this_exception:
        raise RewritePiplockException(
            f"Error: Could not decode file '{file_path}' with encoding '{encoding}'."
        ) from this_exception
    except Exception as this_exception:
        raise RewritePiplockException(
            f"Unexpected error: {this_exception}"
        ) from this_exception


def __is_valid_python_version(input_string: str) -> Optional[str]:
    input_string = input_string.strip()
    split_input_string = input_string.strip().split(".")
    if len(split_input_string) != 2 or " " in input_string:
        return f"Python versoin '{input_string}' must have 2 parts separated by a '.' character and no space characters."
    if split_input_string[0] != "3":
        return f"Python version '{input_string}' is not of the form '3.x'."
    if split_input_string[1] not in ["9", "10", "11", "12", "13"]:
        return f"Python version '{input_string}" + "' is not of the form '3.{9-13}'."
    return None


def __parse_python_version(versionx: str) -> List[int]:
    return list(map(int, versionx.split(".")))


def __python_version_type(input_string: str) -> str:
    if error_string := __is_valid_python_version(input_string):
        raise argparse.ArgumentTypeError(error_string)
    return input_string


def __remove_item_type(input_string: str) -> str:
    input_string = input_string.strip()
    split_input_string = input_string.strip().split(":")
    if len(split_input_string) != 2 or " " in input_string:
        raise argparse.ArgumentTypeError(
            f"Remove item '{input_string}' must have 2 parts separated by a ':' character and no space characters."
        )

    if error_string := __is_valid_python_version(split_input_string[0]):
        raise argparse.ArgumentTypeError(
            f"Remove item '{input_string}' does not specify a supported python version: {error_string}"
        )

    rr = r"[_a-z][0-9a-z_]*"
    if not re.match(rr, split_input_string[1]):
        raise argparse.ArgumentTypeError(
            f"Remove item '{input_string}' does not specify a valid package name."
        )
    return input_string


def __handle_arguments():
    parser = argparse.ArgumentParser(  # type: ignore
        description="Analyze PyTest tests to determine if extra coverage is present."
    )
    parser.add_argument(
        "-p",
        "--python-version",
        type=__python_version_type,
        dest="python_version",
        action="store",
        required=True,
        help="python version being targetted",
    )
    parser.add_argument(
        "-r",
        "--remove-package-if",
        dest="remove_items",
        type=__remove_item_type,
        action="append",
        help="packages to remove in 'version:package_name' format",
    )
    parser.add_argument(
        "-i", "--in-place", action="store_true", help="modify the file in place"
    )
    return parser.parse_args()


def __create_list_of_packages_to_remove(
    current_version: int, argument_list: List[str]
) -> List[str]:
    packages_to_remove: List[str] = []
    for next_argument in argument_list:
        split_next_argument = next_argument.split(":")
        remove_item_version = __parse_python_version(split_next_argument[0])[1]
        if remove_item_version > current_version:
            packages_to_remove.append(split_next_argument[1])
    return packages_to_remove


# pylint: disable=consider-using-with


def __process_and_output_file(
    do_perform_update_in_place: bool,
    loaded_file_contents: List[str],
    packages_to_remove: List[str],
) -> None:
    output_file_object = None
    try:
        if do_perform_update_in_place:
            output_file_object = open("Pipfile", "w", encoding="utf-8")
        else:
            output_file_object = sys.stdout

        in_dev_packages = False
        for next_line in loaded_file_contents:
            do_print_this_line = True
            if next_line.startswith("["):
                in_dev_packages = next_line.startswith("[dev-packages]")
            elif in_dev_packages:
                next_line = next_line.strip()
                if next_line:
                    split_next_line = next_line.split(" ")
                    if split_next_line[0] in packages_to_remove:
                        do_print_this_line = False
            if do_print_this_line:
                output_file_object.write(next_line + "\n")
    except Exception as this_exception:
        raise RewritePiplockException(
            f"Unexpected error: {this_exception}"
        ) from this_exception
    finally:
        if output_file_object and output_file_object != sys.stdout:
            output_file_object.close()


# pylint: enable=consider-using-with


def __main():
    args = __handle_arguments()

    try:
        my_current_version = __parse_python_version(args.python_version)[1]

        packages_to_remove = __create_list_of_packages_to_remove(
            my_current_version, args.remove_items
        )

        loaded_file_contents = __load_file_as_string("Pipfile")

        __process_and_output_file(
            args.in_place, loaded_file_contents, packages_to_remove
        )
    except RewritePiplockException as this_exception:
        print(f"Error processing piplock file: {this_exception}")
        sys.exit(1)


__main()
