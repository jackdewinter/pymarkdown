import os
import re
import subprocess
import sys
from typing import List

WHEEL_REGEX = r"^(.*)-(.*)-py3-none-any\.whl$"
TARBALL_REGEX = r"^(.*)-(.*)\.tar\.gz$"

PACKAGE_NAME = "pymarkdownlnt"


def __get_versions_from_pip() -> List[str]:
    pip_response = str(
        subprocess.run(
            [sys.executable, "-m", "pip", "install", f"{PACKAGE_NAME}==99.99.99"],
            capture_output=True,
            text=True,
        )
    )
    pip_response = pip_response[pip_response.find("(from versions:") + 15 :]
    pip_response = pip_response[: pip_response.find(")")]
    return pip_response.replace(" ", "").split(",")


# Verify that the specified directory exists.
dist_directory = sys.argv[1]
if not os.path.isdir(dist_directory):
    print(f"Path '{dist_directory}' is not an existing directory.")
    sys.exit(1)

# That `dist` directory should have EXACTLY 2 files.
files_in_directory = os.listdir(dist_directory)
if len(files_in_directory) != 2:
    print(f"Directory '{dist_directory}' must contain exactly two files.")
    sys.exit(1)
files_in_directory = sorted(files_in_directory)

# Those two files must match the expected file names...
wheel_match = re.match(WHEEL_REGEX, files_in_directory[0])
if not wheel_match:
    print(
        f"First file '{files_in_directory[0]}' does not match expected expression '{WHEEL_REGEX}'."
    )
    sys.exit(1)
tarball_match = re.match(TARBALL_REGEX, files_in_directory[1])
if not tarball_match:
    print(
        f"Second file '{files_in_directory[1]}' does not match expected expression '{TARBALL_REGEX}'."
    )
    sys.exit(1)

# ... and have the package name and version portions of the file names match.
if wheel_match.group(1) != tarball_match.group(1):
    print(
        f"Wheel package name '{wheel_match.group(1)}' and tarball package name '{tarball_match.group(1)}' are not equal."
    )
    sys.exit(1)
if wheel_match.group(2) != tarball_match.group(2):
    print(
        f"Wheel version '{wheel_match.group(2)}' and tarball version '{tarball_match.group(2)}' are not equal."
    )
    sys.exit(1)

available_versions = set(__get_versions_from_pip())
if wheel_match.group(2) in available_versions:
    print(
        f"Package version '{wheel_match.group(2)}' already exists in the package repository."
    )
    sys.exit(1)

# current_version = str(subprocess.run([sys.executable, '-m', 'pip', 'show', f'{PACKAGE_NAME}'], capture_output=True, text=True))

sys.exit(0)
