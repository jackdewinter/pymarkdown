#!/usr/bin/env bash

# Set the script mode to "strict".
# http://redsymbol.net/articles/unofficial-bash-strict-mode/ without the fail fast.
set -uo pipefail

# Set up any project based local script variables.
SCRIPT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" &>/dev/null && pwd)

if ! python utils/verify_package_release.py "${SCRIPT_DIR}/dist"; then
	echo "Validation of 'dist' package directory failed.  Run 'package-release.sh' before trying again."
	exit 1
fi

if ! pipenv run python -m twine upload --config-file ../.pypirc --repository pypi "${SCRIPT_DIR}"/dist/*; then
	echo "Publishig of package failed."
	exit 1
fi
