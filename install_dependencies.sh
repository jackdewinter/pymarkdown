#!/usr/bin/env bash

# Set the script mode to "strict".
# http://redsymbol.net/articles/unofficial-bash-strict-mode/ without the fail fast.
set -uo pipefail

# Set up any project based local script variables.
SCRIPT_NAME=$(basename -- "${BASH_SOURCE[0]}")
SCRIPT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" &>/dev/null && pwd)
TEMP_FILE=$(mktemp /tmp/"${SCRIPT_NAME}".XXXXXXXXX)

SCRIPT_TITLE="Verifying and installing project dependencies"

verbose_echo() {
	echo_text=${1:-}

	if [ "${VERBOSE_MODE}" -ne 0 ]; then
		echo "${echo_text}"
	fi
}

# Perform any cleanup required by the script.
# shellcheck disable=SC2317  # Unreachable code
# shellcheck disable=SC2329  # This function is never invoked. Check usage (or ignored if invoked indirectly).
cleanup_function() {

	if [[ ${VERBOSE_MODE} -ne 0 ]]; then
		echo "{Performing clean up for script '${SCRIPT_NAME}'.}"
	fi

	# If the temp file was used, get rid of it.
	if [ -f "${TEMP_FILE}" ]; then
		rm "${TEMP_FILE}"
	fi

	# Restore the current directory.
	popd >/dev/null 2>&1 || exit
}

# Start the main part of the script off with a title.
start_process() {
	verbose_echo "${SCRIPT_TITLE}..."
	verbose_echo ""
	verbose_echo "{Saving current directory prior to execution.}"
	if ! pushd "${SCRIPT_DIR}" >"${TEMP_FILE}" 2>&1; then
		cat "${TEMP_FILE}"
		complete_process 1 "Script cannot save the current directory before proceeding."
	fi

	trap cleanup_function EXIT
}

# Simple function to stop the process with information about why it stopped.
complete_process() {
	local SCRIPT_RETURN_CODE=${1}
	local COMPLETE_REASON=${2:-}

	if [ -n "${COMPLETE_REASON}" ]; then
		echo "${COMPLETE_REASON}"
	fi

	if [ "${SCRIPT_RETURN_CODE}" -ne 0 ]; then
		echo ""
		echo "${SCRIPT_TITLE} failed."
	else
		verbose_echo ""
		verbose_echo "${SCRIPT_TITLE} succeeded."
	fi

	exit "${SCRIPT_RETURN_CODE}"
}

# Give the user hints on how the script can be used.
show_usage() {
	local SCRIPT_NAME=$0

	echo "Usage:"
	echo "  $(basename "${SCRIPT_NAME}") [flags]"
	echo ""
	echo "Summary:"
	echo "  Installs the dependencies for the project."
	echo ""
	echo "Flags:"
	echo "  -f,--force-reset <ver>  Force a reset of the virtual environment, with an optional python version to reset to."
	echo "  -x,--debug              Display debug information about the script as it executes."
	echo "  -q,--quiet              Do not display detailed information during execution."
	echo "  -h,--help               Display this help text."
	echo ""
	exit 1
}

# Parse the command line.
parse_command_line() {

	VERBOSE_MODE=1
	DEBUG_MODE=0
	FORCE_RESET_MODE=0
	RESET_PYTHON_VERSION=
	while (("$#")); do
		case "$1" in
		-f | --force-reset)
			FORCE_RESET_MODE=1
			temp_version=${2:-0}
			if [[ ${temp_version} == 3* ]]; then
				RESET_PYTHON_VERSION=${temp_version}
				shift
			fi
			shift
			;;
		-q | --quiet)
			VERBOSE_MODE=0
			shift
			;;
		-x | --debug)
			DEBUG_MODE=1
			shift
			;;
		-h | --help)
			show_usage
			;;
		-*) # unsupported flags
			echo "Error: Unsupported flag ${1}" >&2
			show_usage
			;;
		*) # preserve positional arguments
			echo "Error: Unsupported positional argument ${1}" >&2
			show_usage
			;;
		esac
	done

	if [[ ${DEBUG_MODE} -ne 0 ]]; then
		set -x
	fi
}

remove_virtual_environment() {

	RESET_PIPFILE=0
	verbose_echo "{Forcing a hard reset of the virtual environment.}"
	if ! VENV_DIR=$(pipenv --venv); then
		verbose_echo "{Virtual environment was not established.  Reset not required. Proceeding to setup virtual environment.}"
		RESET_PIPFILE=1
	fi

	if [[ ${RESET_PIPFILE} -eq 0 ]]; then
		if ! [[ -d "${VENV_DIR}/S2" ]]; then
			verbose_echo "{Creating temporary directory '${VENV_DIR}/S2' for move test.}"
			if ! mkdir "${VENV_DIR}/S2"; then
				complete_process 1 "{Cannot mkdir test directory for virtual environment lock test.}"
			fi
		fi

		verbose_echo "{Executing move test to see if one or more files in directory '${VENV_DIR}' are locked.}"
		if ! mv "${VENV_DIR}/Scripts" "${VENV_DIR}/S2" >"${TEMP_FILE}"; then
			cat "${TEMP_FILE}"
			echo "  {One or more directories in ${VENV_DIR} are locked.}"
			echo "  {Close any open IDEs or shells in that directory and try again.}"
			echo "  {If lock persists, try pipenv --rm to try and force the lock to be released.}"
			complete_process 1
		fi

		verbose_echo "{Removing previous PipEnv environment.}"
		if ! rm -rf "${VENV_DIR}"; then
			complete_process 1 "bad rmdir"
		fi

		if ! [[ -d ${VENV_DIR} ]]; then
			verbose_echo "{Virtual environment directory has been removed successfully.}"
			RESET_PIPFILE=1
		else
			echo "  {One or more directories in ${VENV_DIR} are locked.}"
			echo "  {Close any open IDEs or shells in that directory and try again.}"
			echo "  {If lock persists, try pipenv --rm to try and force the lock to be released.}"
			complete_process 1
		fi
	fi

	mkdir -p .venv

	if [[ -z ${RESET_PYTHON_VERSION} ]]; then
		RESET_PYTHON_VERSION=$(python utils/extract_python_version_from_pipfile.py)
	fi
}

check_for_unsychronized_virtual_environment() {

	RESET_PIPFILE=0

	# To allow for the possibility of the virtual environment being moved,
	# check the provenance of the virtual environment against the current provenance.
	# If they do not match, then we will reset the virtual environment to be safe.
	CURRENT_PROVENANCE="$(pwd)"
	VENV_PROVENANCE=""
	if [[ -f ${PROVENENCE_PATH} ]]; then
		VENV_PROVENANCE=$(<"${PROVENENCE_PATH}")
	fi
	if [[ "${VENV_PROVENANCE}" != "${CURRENT_PROVENANCE}" ]]; then
		verbose_echo "{Location of virtual environment changed.}"
		RESET_PIPFILE=1
	fi

	# Check to see if the Pipfile and Pipfile.lock files are in sync with each other.
	# If not, we will reset the virtual environment to be safe.
	if [[ ${RESET_PIPFILE} -eq 0 ]]; then
		python utils/find_outdated_piplock_file.py >"${TEMP_FILE}" 2>&1
		OUTDATED_PIPLOCK_RETCODE=$?
		if [[ ${OUTDATED_PIPLOCK_RETCODE} -eq 2 ]]; then
			cat "${TEMP_FILE}"
			complete_process 1 "{Analysis of project cannot proceed without a Pipfile.}"
		fi
		if [[ ${OUTDATED_PIPLOCK_RETCODE} -ne 0 ]]; then
			verbose_echo "{Virtual environment files 'Pipfile' and 'Pipfile.lock' are not in sync with each other.}"
			RESET_PIPFILE=1
		fi
	fi

	if [[ ${RESET_PIPFILE} -ne 0 ]]; then
		RESET_PYTHON_VERSION=$(pipenv run python -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
	fi
}

synchronize_virtual_environment() {

	verbose_echo "{Syncing python packages in virtual environment.}"
	rm Pipfile.lock >/dev/null 2>&1
	if ! pipenv lock --python "${RESET_PYTHON_VERSION}" >"${TEMP_FILE}" 2>&1; then
		cat "${TEMP_FILE}"
		complete_process 1 "{Creating new Pipfile.lock file failed.}"
	fi
	if ! pipenv update -d >"${TEMP_FILE}" 2>&1; then
		cat "${TEMP_FILE}"
		complete_process 1 "{Updating with new Pipfile.lock file failed.}"
	fi

	pwd >"${PROVENENCE_PATH}"

	verbose_echo "{Python packages in virtual environment synced.}"
}

# Parse any command line values.
parse_command_line "$@"

# Clean entrance into the script.
start_process

PROVENENCE_PATH="${SCRIPT_DIR}/.venv/.provenence"

if [[ ${FORCE_RESET_MODE} -ne 0 ]]; then
	remove_virtual_environment
else
	check_for_unsychronized_virtual_environment
fi

if [[ ${RESET_PIPFILE} -ne 0 ]]; then
	synchronize_virtual_environment
fi

# Normal exit from the script.
complete_process 0
