#!/usr/bin/env bash

# Set the script mode to "strict".
# http://redsymbol.net/articles/unofficial-bash-strict-mode/ without the fail fast.
set -uo pipefail

# Set up any project based local script variables.
SCRIPT_NAME=$(basename -- "${BASH_SOURCE[0]}")
SCRIPT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" &>/dev/null && pwd)

# Give the user hints on how the script can be used.
show_usage() {
	echo "Usage:"
	echo "  $SCRIPT_NAME [flags]"
	echo ""
	echo "Summary:"
	echo "  Create a webserver hosting for the documentation from the project's 'newdocs' directory."
	echo ""
	echo "Flags:"
	echo "  -v,--verbose            Display detailed information during execution."
	echo "  -x,--debug              Display debug information about the script as it executes."
	echo "  -h,--help               Display this help text."
	echo ""
	exit 1
}

# Parse the command line.
parse_command_line() {

	VERBOSE_ARGS=
	DEBUG_MODE=0
	PARAMS=()
	while (("$#")); do
		case "$1" in
		-v | --verbose)
			VERBOSE_ARGS=--verbose
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
pipenv run mkdocs serve --config-file $SCRIPT_DIR/newdocs/mkdocs.yml $VERBOSE_ARGS

exit 1
