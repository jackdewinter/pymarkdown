"""Module to generate a combined dependencies file from pre-commit and Pipfile."""

import json
import os
import subprocess
import sys
from dataclasses import dataclass
from typing import Dict, List, Optional, cast

from pip_check_updates.parser import load_dependencies


@dataclass
class Icons:
    """Dataclass to hold the different strings that pre-commit-update can output for the current state."""

    icon: str
    icon_alt: str
    text: str


icons_map = {
    "exclude": Icons(icon="★", icon_alt="*", text="[exclude]"),
    "keep": Icons(icon="◉", icon_alt="●", text="[keep]"),
    "no_update": Icons(icon="✔", icon_alt="√", text="[no-update]"),
    "update": Icons(icon="✘", icon_alt="×", text="[update]"),
    "warning": Icons(icon="⚠", icon_alt="▲", text="[warning]"),
}


def __match_icons(first_column_value: str) -> Optional[str]:
    return next(
        (
            i
            for i, matching_icons in icons_map.items()
            if first_column_value
            in (matching_icons.icon, matching_icons.icon_alt, matching_icons.text)
        ),
        None,
    )


def __load_precommit_packages_and_versions(error_messages: List[str]) -> Dict[str, str]:

    package_version_list: List[List[str]] = []
    try:
        with subprocess.Popen(
            ["pre-commit-update", "--dry-run", "--verbose"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        ) as p:
            status_code = p.wait()
            if status_code in [0, 1]:
                __load_precommit_packages_and_versions_translate_ouptut(
                    p.stdout.read(), package_version_list
                )
            else:
                formatted_error = (
                    f"Pre-commit update command failed with status code {status_code}:"
                )
                for i in p.stderr.read().split("\n"):
                    i = i.strip()
                    formatted_error += f"\n  {i}"
                error_messages.append(formatted_error)

    except OSError as this_exception:
        formatted_error = (
            f"Pre-commit update command failed to run: {str(this_exception)}."
        )
        error_messages.append(formatted_error)

    package_version_map: Dict[str, str] = {}
    for i in package_version_list:
        package_name = i[1]
        old_version = i[2]
        if package_name in package_version_map:
            registered_version = package_version_map[package_name]
            if registered_version != old_version:
                error_messages.append(
                    f"Pre-commit Conflict detected within file `.pre-commit-config.yaml` for package '{package_name}': '{registered_version}' vs '{old_version}'"
                )
        else:
            package_version_map[package_name] = old_version

    return package_version_map


def __load_precommit_packages_and_versions_translate_ouptut(
    data: str, version_list: List[List[str]]
) -> None:

    for next_line in data.split("\n"):
        next_line = next_line.strip()
        if not next_line:
            continue
        split_line = list(next_line.split(" "))
        matched_icon = __match_icons(split_line[0])
        assert (
            matched_icon
        ), f"Unrecognized icon in pre-commit output: '{split_line[0]}'"
        split_line[0] = matched_icon
        assert split_line[2] == "-"
        del split_line[2]
        if len(split_line) > 3 and split_line[3] == "->":
            del split_line[3]
        version_list.append(split_line)


# pylint: disable=broad-exception-caught
def __load_pipfile_packages_and_versions(error_messages: List[str]) -> Dict[str, str]:
    pipfile_map: Dict[str, str] = {}
    try:
        pipfile_dependencies = cast(
            List[List[str]], load_dependencies("Pipfile", False, [])
        )
        for next_dependency in pipfile_dependencies:
            pipfile_map[next_dependency[1]] = next_dependency[2]
    except BaseException as this_exception:  # noqa: B036
        error_messages.append(f"Failed to load Pipfile: {str(this_exception)}")
    return pipfile_map


# pylint: enable=broad-exception-caught

# pylint: disable=broad-exception-caught


def __abc():
    error_messages: List[str] = []

    pre_commit_map = __load_precommit_packages_and_versions(error_messages)
    pipefile_map = __load_pipfile_packages_and_versions(error_messages)
    if error_messages:
        error_messages.append(
            "Errors detected during load.  Unable to continue with merge."
        )
    else:
        for pre_commit_key, pre_commit_value in pre_commit_map.items():
            if (
                pre_commit_key in pipefile_map
                and pre_commit_value != pipefile_map[pre_commit_key]
            ):
                error_messages.append(
                    f"Conflict detected for package '{pre_commit_key}': pre-commit version '{pre_commit_value}' vs Pipfile version '{pipefile_map[pre_commit_key]}'"
                )
            pipefile_map[pre_commit_key] = pre_commit_value
        if error_messages:
            error_messages.append(
                "Errors detected during merge.  Unable to continue with output."
            )
    if not error_messages:
        try:
            with open(
                os.path.join(".", "publish", "dependencies.json"),
                "wt",
                encoding="utf-8",
            ) as output_file:
                json.dump(pipefile_map, output_file, indent=4)
        except BaseException as this_exception:  # noqa: B036
            error_messages.append(
                f"Failed to write combined dependencies file: {str(this_exception)}"
            )

    if error_messages:
        print("\n".join(error_messages))
        sys.exit(1)


# pylint: enable=broad-exception-caught


if __name__ == "__main__":
    __abc()
