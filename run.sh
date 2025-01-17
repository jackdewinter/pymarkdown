#!/usr/bin/env bash

# Set the script mode to "strict".
# http://redsymbol.net/articles/unofficial-bash-strict-mode/ without the fail fast.
set -uo pipefail

# Set up any project based local script variables.
SCRIPT_NAME=$( basename -- "${BASH_SOURCE[0]}" )
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
TEMP_FILE=$(mktemp /tmp/$SCRIPT_NAME.XXXXXXXXX)

# Perform any cleanup required by the script.
cleanup_function(){

    # If the temp file was used, get rid of it.
    if [ -f "$TEMP_FILE" ]; then
        rm "$TEMP_FILE"
    fi

    # Restore the current directory.
    if [ "$DID_PUSHD" -eq 1 ]; then
        popd > /dev/null 2>&1 || exit
    fi
}

# Start the main part of the script off with a title.
start_process() {
    if ! pushd . > "$TEMP_FILE" 2>&1 ; then
        cat "$TEMP_FILE"
        complete_process 1 "Script cannot save the current directory before proceeding."
    fi
    DID_PUSHD=1

    trap cleanup_function EXIT
}

# Simple function to stop the process with information about why it stopped.
complete_process() {
    local SCRIPT_RETURN_CODE=$1
    local COMPLETE_REASON=${2:-}

    if [ -n "$COMPLETE_REASON" ] ; then
        echo "$COMPLETE_REASON"
    fi

    exit "$SCRIPT_RETURN_CODE"
}

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

start_process

# If we are doing a performance run, make sure to use optimized python.
PYTHON_PERFORMANCE_ARGUMENTS=
if [[ ${PYMARKDOWNLINT__PERFRUN:-0} -ne 0 ]] ; then
    PYTHON_PERFORMANCE_ARGUMENTS=-OO
fi

pipenv run python $PYTHON_PERFORMANCE_ARGUMENTS "${SCRIPT_DIR}/main.py" ${PARAMS[*]}
EXIT_CODE=$?
complete_process $EXIT_CODE
