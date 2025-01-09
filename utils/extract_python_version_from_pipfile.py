import re
import sys

try:
    with open("Pipfile", "r", encoding="utf-8") as readme_file:
        line_in_file = readme_file.read().split("\n")

    requires_index = line_in_file.index("[requires]")

    python_version_regex = r"^python_version\s=\s\"3\.(\d+)\"$"
    version_regex_match = re.match(
        python_version_regex, line_in_file[requires_index + 1]
    )
    assert (
        version_regex_match is not None
    ), "Python version line did not follow the requires line."
    print(f"3.{version_regex_match.group(1)}")

except BaseException as this_exception:  # noqa: B036
    print(f"Exception: {this_exception}")
    sys.exit(1)

sys.exit(0)
