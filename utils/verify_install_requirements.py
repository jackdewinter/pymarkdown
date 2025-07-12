"""
Module to verify that the install-requirements.txt file and the Pipfile are synced.

Used in .pre-commit-config.yaml.
"""

import configparser
import sys
from typing import Dict, Tuple

__REQUIREMENTS_FILE_NAME = "install-requirements.txt"
__PIPFILE_FILE_NAME = "Pipfile"


def __read_pipfile() -> Dict[str, str]:
    config_parser = configparser.ConfigParser(allow_no_value=False)
    try:
        config_parser.read(__PIPFILE_FILE_NAME)
        return {i[0]: i[1] for i in config_parser.items("packages")}
    except configparser.Error as this_exception:
        formatted_error = (
            f"Specified file '{__PIPFILE_FILE_NAME}' "
            + f"is not a valid config file: {str(this_exception)}."
        )
        print(formatted_error, file=sys.stderr)
        sys.exit(1)


def __read_requirements_file() -> Dict[str, Tuple[str, str]]:
    try:
        with open(__REQUIREMENTS_FILE_NAME, "rt", encoding="utf-8") as input_file:
            all_lines = input_file.readlines()
        file_map = {}
        for next_line in all_lines:
            if next_line.endswith("\n"):
                next_line = next_line[:-1]
            if next_line := next_line.strip():
                separator_index = next_line.find("==")
                if separator_index == -1:
                    separator_index = next_line.index(">=")
                separator_text = next_line[separator_index : separator_index + 2]
                version_text = next_line[separator_index + 2 :]
                file_map[next_line[:separator_index]] = (
                    separator_text,
                    version_text,
                )
        return file_map
    except OSError as this_exception:
        formatted_error = (
            f"Specified file '{__PIPFILE_FILE_NAME}' "
            + f"is not a valid requirements file: {str(this_exception)}."
        )
        print(formatted_error, file=sys.stderr)
        sys.exit(1)


requirements_map = __read_requirements_file()
print(requirements_map)
pipfile_map = __read_pipfile()
print(pipfile_map)

ERRORS_FOUND = 0
for next_requirement_name, next_requirement_value in requirements_map.items():
    print(f"Verifying install requirement package '{next_requirement_name}'.")
    if next_requirement_name not in pipfile_map:
        print(
            f"  Install requirement package '{next_requirement_name}' not found in Pipfile."
        )
        ERRORS_FOUND += 1
    else:
        pipfile_value = pipfile_map[next_requirement_name]
        pipfile_value = pipfile_value[1:-1]
        pipfile_value = pipfile_value[:2], pipfile_value[2:]
        if pipfile_value != next_requirement_value:
            print(
                f"  Pipfile package '{next_requirement_name}' has a value of '{pipfile_value}' that does not equal the install requirement package of '{next_requirement_value}'."
            )
            ERRORS_FOUND += 1
        else:
            print(f"  Install requirement package '{next_requirement_name}' verified.")

for next_pipfile_name in pipfile_map:
    print(f"Verifying pipfile package '{next_pipfile_name}'.")
    if next_pipfile_name not in requirements_map:
        print(
            f"  Pipfile package '{next_pipfile_name}' not found in install requirements."
        )
        ERRORS_FOUND += 1
    else:
        print(f"  Pipfile package '{next_pipfile_name}' verified.")

print(f"Errors found: {ERRORS_FOUND}")
if ERRORS_FOUND > 0:
    sys.exit(1)
