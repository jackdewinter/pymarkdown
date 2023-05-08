import configparser
import sys
from typing import Dict

__requirements_file_name = "install-requirements.txt"
__pipfile_file_name = "Pipfile"


def __read_pipfile() -> Dict[str, str]:
    config_parser = configparser.ConfigParser(allow_no_value=False)
    try:
        config_parser.read(__pipfile_file_name)
        return {i[0]: i[1] for i in config_parser.items("packages")}
    except configparser.Error as this_exception:
        formatted_error = (
            f"Specified file '{__pipfile_file_name}' "
            + f"is not a valid config file: {str(this_exception)}."
        )
        print(formatted_error, file=sys.stderr)
        sys.exit(1)


def __read_requirements_file() -> Dict[str, str]:
    try:
        with open(__requirements_file_name, "rt", encoding="utf-8") as input_file:
            all_lines = input_file.readlines()
        requirements_map = {}
        for next_line in all_lines:
            if next_line.endswith("\n"):
                next_line = next_line[:-1]
            separator_index = next_line.index("==")
            requirements_map[next_line[:separator_index]] = next_line[separator_index:]
        return requirements_map
    except OSError as this_exception:
        formatted_error = (
            f"Specified file '{__pipfile_file_name}' "
            + f"is not a valid requirements file: {str(this_exception)}."
        )
        print(formatted_error, file=sys.stderr)
        sys.exit(1)


install_map = __read_requirements_file()
pipfile_map = __read_pipfile()

errors_found = 0
for next_requirement_name, next_requirement_value in install_map.items():
    if next_requirement_name not in pipfile_map:
        print(f"Install requirement '{next_requirement_name}' not in Pipfile.")
        errors_found += 1
    else:
        pipfile_value = pipfile_map[next_requirement_name]
        pipfile_value = pipfile_value[1:-1]
        if pipfile_value != install_map[next_requirement_name]:
            print(
                f"Pipfile value '{pipfile_value}' does not equal the install requirement '{next_requirement_value}'."
            )
            errors_found += 1

if errors_found > 0:
    print(f"Errors found: {errors_found}")
    sys.exit(1)
