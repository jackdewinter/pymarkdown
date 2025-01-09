#!/usr/bin/env bash

# Set the script mode to "strict".
# http://redsymbol.net/articles/unofficial-bash-strict-mode/ without the fail fast.
set -uo pipefail

# Set up any project based local script variables.
SCRIPT_NAME=$( basename -- "${BASH_SOURCE[0]}" )
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

# Give the user hints on how the script can be used.
show_usage() {
    echo "Usage:"
    echo "  $SCRIPT_NAME [flags]"
    echo ""
    echo "Summary:"
    echo "  Launch the project's application."
    echo ""
    echo "Flags:"
    echo "  --                      Used to separate this script's arguments from the application's arguments."
    echo "  -x,--debug              Display debug information about the script as it executes."
    echo "  -h,--help               Display this help text."
    echo ""
    exit 1
}

# Parse the command line.
parse_command_line() {

    DEBUG_MODE=0
    PARAMS=()
    CAPTURE_MODE=0
    while (( "$#" )); do
        if [[ $CAPTURE_MODE -eq 0 ]] ; then
            case "$1" in
                -x|--debug)
                    DEBUG_MODE=1
                    shift
                ;;
                -h|--help)
                    show_usage
                ;;
                --)
                    CAPTURE_MODE=1
                    shift
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
        else
            PARAMS+=("$1")
            shift
        fi
    done

    if [[ $DEBUG_MODE -ne 0 ]] ; then
        set -x
    fi
}

# Parse any command line values.
parse_command_line "$@"

# @REM If we are doing a performance run, make sure to use optimized python.
PYTHON_PERFORMANCE_ARGUMENTS=
if [[ $PYMARKDOWNLINT__PERFRUN -ne 0 ]] ; then
    PYTHON_PERFORMANCE_ARGUMENTS=-OO
fi

pipenv run python $PYTHON_PERFORMANCE_ARGUMENTS main.py ${PARAMS[*]}
EXIT_CODE=$?
exit $EXIT_CODE
