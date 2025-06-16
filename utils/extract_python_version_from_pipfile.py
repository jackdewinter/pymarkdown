"""
Module to extract the Python version from a Pipfile.
"""

import re
import sys

# pylint: disable=broad-exception-caught
try:
    with open("Pipfile", "r", encoding="utf-8") as readme_file:
        line_in_file = readme_file.read().split("\n")

    requires_index = line_in_file.index("[requires]")

    PYTHON_VERSION_REGEX = r"^python_version\s=\s\"3\.(\d+)\"$"
    version_regex_match = re.match(
        PYTHON_VERSION_REGEX, line_in_file[requires_index + 1]
    )
    assert (
        version_regex_match is not None
    ), "Python version line did not follow the requires line."
    print(f"3.{version_regex_match.group(1)}")

except BaseException as this_exception:  # noqa: B036
    print(f"Exception: {this_exception}")
    sys.exit(1)
# pylint: enable=broad-exception-caught

sys.exit(0)
