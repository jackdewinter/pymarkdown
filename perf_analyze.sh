#!/usr/bin/env bash

# Set the script mode to "strict".
# http://redsymbol.net/articles/unofficial-bash-strict-mode/ without the fail fast.
set -uo pipefail

# Set up any project based local script variables.
SCRIPT_NAME=$(basename -- "${BASH_SOURCE[0]}")
SCRIPT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" &>/dev/null && pwd)
TEMP_FILE=$(mktemp /tmp/"${SCRIPT_NAME}".XXXXXXXXX)

# Perform any cleanup required by the script.
# shellcheck disable=SC2317  # Unreachable code
cleanup_function() {

	# If the temp file was used, get rid of it.
	if [ -f "${TEMP_FILE}" ]; then
		rm "${TEMP_FILE}"
	fi

	# Restore the current directory.
	popd >/dev/null 2>&1 || exit
}

# Give the user hints on how the script can be used.
show_usage() {

	echo "Usage:"
	echo "  ${SCRIPT_NAME} [flags]"
	echo ""
	echo "Summary:"
	echo "  Visually display the results of the perf_series.sh script as invoked by the clean.sh script."
	echo ""
	echo "Flags:"
	echo "  -x,--debug              Display debug information about the script as it executes."
	echo "  -h,--help               Display this help text."
	echo ""
	exit 1
}

# Parse the command line.
parse_command_line() {

	DEBUG_MODE=0
	PARAMS=()
	while (("$#")); do
		case "${1}" in
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
			PARAMS+=("${1}")
			shift
			;;
		esac
	done

	if [[ ${DEBUG_MODE} -ne 0 ]]; then
		set -x
	fi
}

# Parse any command line values.
parse_command_line "$@"

trap cleanup_function EXIT

# Main body of the script.

if ! pipenv run streamlit run "${SCRIPT_DIR}/utils/streamlit_performance_analysis.py"; then
	echo "Unable to execute the streamlist visualizer of timed profiles."
	exit 1
fi

exit 0
