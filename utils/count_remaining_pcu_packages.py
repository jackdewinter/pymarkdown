"""
Module to count the number of packages that can be updated, as output from 'pcu'.
"""

import argparse
import configparser
from typing import List


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
    parser.add_argument(
        "-l",
        "--list",
        dest="list_items",
        action="store_true",
        default=False,
        help="output the dev-packages section instead of packages section",
    )
    parser.add_argument("file_name", action="store", help="file_to_consume")

    return parser.parse_args()


def __load_package_exclude_list_from_properties_file(use_dev_list: bool) -> List[str]:

    with open("project.properties", "r", encoding="utf-8") as properties_file:
        properties_text = properties_file.read()
    config = configparser.RawConfigParser()
    config.read_string(f"[main]\n{properties_text}")
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


parsed_args = __handle_arguments()
exclude_list = __load_package_exclude_list_from_properties_file(
    parsed_args.export_dev_packages
)

with open(parsed_args.file_name, "r", encoding="utf-8") as file:
    text = file.read()
has_extra_parameters = parsed_args.list_items

file_lines = text.splitlines()
have_seen_start = False
non_excluded_packages: List[str] = []
for line in file_lines:
    line = line.strip()
    if line.startswith("In "):
        have_seen_start = True
        continue
    if not have_seen_start or not line:
        continue
    if line.startswith("All dependencies match") or line.startswith("Run pcu"):
        break
    while "  " in line:
        line = line.replace("  ", " ")
    x = line.split(" ")
    if x[0] not in exclude_list:
        if has_extra_parameters:
            print(
                f"      Package '{x[0]}' has version '{x[1]}' and can be updated to version '{x[3]}'"
            )
        non_excluded_packages.append(x[0])

if not has_extra_parameters:
    print(len(non_excluded_packages))
