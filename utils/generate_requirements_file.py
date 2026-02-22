"""
Module to generate a targetted requirements.txt file from a Pipfile.  Only the [packages] sectopmn
or [dev-packages] section is exported, and only the package names listed in the file are exported.

Other tools will export all packages (listed and discovered) to a requirements.txt file.
"""

import argparse
import configparser
from typing import Dict, List, Tuple, cast

import toml
from pip_check_updates.parser import load_dependencies

# pylint: disable=broad-exception-caught


def __load_pipfile_packages_and_versions(
    error_list: List[str],
) -> Tuple[Dict[str, str], List[str], List[str]]:
    pipfile_map: Dict[str, str] = {}
    package_list = []
    dev_package_list = []
    try:
        pipfile_dependencies = cast(
            List[List[str]], load_dependencies("Pipfile", False, [])
        )
        for next_dependency in pipfile_dependencies:
            pipfile_map[next_dependency[1]] = next_dependency[2]

        with open("Pipfile", "rt", encoding="utf-8") as f:
            config = toml.load(f)
        package_list: List[str] = list(config["packages"].keys())
        dev_package_list: List[str] = list(config["dev-packages"].keys())
    except BaseException as this_exception:  # noqa: B036
        error_list.append(f"Failed to load Pipfile: {str(this_exception)}")
    return pipfile_map, package_list, dev_package_list


# pylint: enable=broad-exception-caught


def __handle_arguments():
    parser = argparse.ArgumentParser(
        description="Analyze PyTest tests to determine if extra coverage is present."
    )
    parser.add_argument(
        "-d",
        "--dev",
        dest="export_dev_packages",
        action="store_true",
        default=False,
        help="output the dev-packages section instead of packages section",
    )

    return parser.parse_args()


def __load_package_exclude_list_from_properties_file(use_dev_list: bool) -> List[str]:

    with open("project.properties", "r", encoding="utf-8") as file:
        text = file.read()
    config = configparser.RawConfigParser()
    config.read_string(f"[main]\n{text}")
    ss = config.get(
        "main",
        (
            "PACKAGE_UPDATE_DEV_EXCLUDE_LIST"
            if use_dev_list
            else "PACKAGE_UPDATE_EXCLUDE_LIST"
        ),
        fallback="",
    ).split(",")
    return [i.strip() for i in ss]


if __name__ == "__main__":
    error_messages: List[str] = []

    parsed_args = __handle_arguments()

    tt = __load_package_exclude_list_from_properties_file(
        parsed_args.export_dev_packages
    )

    pipefile_map, package_name_list, dev_package_name_list = (
        __load_pipfile_packages_and_versions(error_messages)
    )

    for package_name in (
        dev_package_name_list if parsed_args.export_dev_packages else package_name_list
    ):
        if package_name in tt:
            continue
        print(f"{package_name}=={pipefile_map[package_name]}")
    print("", flush=True)
