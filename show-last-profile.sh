#!/usr/bin/env bash

# Set the script mode to "strict".
# http://redsymbol.net/articles/unofficial-bash-strict-mode/ without the fail fast.
set -uo pipefail

# Set up any project based local script variables.
SCRIPT_NAME=$(basename -- "${BASH_SOURCE[0]}")
SCRIPT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" &>/dev/null && pwd)

PROFILE_PATH="$SCRIPT_DIR/p0.prof"

# Give the user hints on how the script can be used.
show_usage() {

	echo "Usage:"
	echo "  $SCRIPT_NAME [flags]"
	echo ""
	echo "Summary:"
	echo "  Shows the last performance-timing profile taken by one of the 'perf_*.sh' scripts."
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
		case "$1" in
		-x | --debug)
			DEBUG_MODE=1
			shift
			;;
		-h | --help)
			show_usage
			;;
		-*) # unsupported flags
			echo "Error: Unsupported flag $1" >&2
			show_usage
			;;
		*) # preserve positional arguments
			PARAMS+=("$1")
			shift
			;;
		esac
	done

	if [[ $DEBUG_MODE -ne 0 ]]; then
		set -x
	fi
}

# Parse any command line values.
parse_command_line "$@"

# Main body of the script.
if ! [[ -f $PROFILE_PATH ]]; then
	echo "Profile file '$PROFILE_PATH' does not exist. Run one of the 'perf_*.sh' scripts first."
	exit 1
fi

if ! pipenv run snakeviz "$PROFILE_PATH"; then
	echo "Unable to execute the snakeviz visualizer on profile '$PROFILE_PATH'."
	exit 1
fi

exit 1
