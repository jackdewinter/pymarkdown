#!/usr/bin/env bash

# Set the script mode to "strict".
# http://redsymbol.net/articles/unofficial-bash-strict-mode/ without the fail fast.
set -uo pipefail

# Set up any project based local script variables.
SCRIPT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" &>/dev/null && pwd)

VERBOSE_MODE=1

load_properties_from_file() {

	if [ "${VERBOSE_MODE}" -ne 0 ]; then
		echo "{Loading 'project.properties file'...}"
	fi
	while IFS='=' read -r key_value; do
		if [[ ${key_value} == \#* ]]; then
			continue
		fi
		key=$(echo "${key_value}" | cut -d '=' -f1)
		value=$(echo "${key_value}" | cut -d '=' -f2-)
		export "${key}=${value}"
	done <"${SCRIPT_DIR}/project.properties"

	if [[ -z ${PYTHON_MODULE_NAME} ]]; then
		echo "Property 'PYTHON_MODULE_NAME' must be defined in the project.properties file."
		exit 1
	fi
}

load_properties_from_file

if ! python utils/verify_package_release.py "${PYTHON_MODULE_NAME}" "${SCRIPT_DIR}/dist"; then
	echo "Validation of 'dist' package directory failed.  Run 'package-release.sh' before trying again."
	exit 1
fi

if ! pipenv run python -m twine upload --config-file ../.pypirc --repository pypi dist/*; then
	echo "Publishig of package failed."
	exit 1
fi
