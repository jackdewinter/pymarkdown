#!/usr/bin/env bash

# Set the script mode to "strict".
# http://redsymbol.net/articles/unofficial-bash-strict-mode/ without the fail fast.
set -uo pipefail

# Set up any project based local script variables.
SCRIPT_NAME=$( basename -- "${BASH_SOURCE[0]}" )
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
TEMP_FILE=$(mktemp /tmp/$SCRIPT_NAME.XXXXXXXXX)

SCRIPT_TITLE="Creation of application package"

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
    if [ "$VERBOSE_MODE" -ne 0 ]; then
        echo "Saving current directory prior to execution."
    fi
    if ! pushd . >"$TEMP_FILE" 2>&1 ;  then
        cat "$TEMP_FILE"
        complete_process 1 "Script cannot save the current directory before proceeding."
    fi
    DID_PUSHD=1

    trap cleanup_function EXIT

    if [ "$VERBOSE_MODE" -ne 0 ]; then
        echo "$SCRIPT_TITLE..."
    fi
}

# Simple function to stop the process with information about why it stopped.
complete_process() {
    local SCRIPT_RETURN_CODE=$1
    local COMPLETE_REASON=${2:-}

    if [ -n "$COMPLETE_REASON" ] ; then
        echo "$COMPLETE_REASON"
    fi

    if [ "$SCRIPT_RETURN_CODE" -ne 0 ]; then
        echo "$SCRIPT_TITLE failed."
    else
        if [ "$VERBOSE_MODE" -ne 0 ]; then
            echo "$SCRIPT_TITLE succeeded."
        fi
    fi

    exit "$SCRIPT_RETURN_CODE"
}

# Give the user hints on how the script can be used.
show_usage() {
    echo "Usage:"
    echo "  $SCRIPT_NAME [flags]"
    echo ""
    echo "Summary:"
    echo "  Package up the application into a wheel suitable for publishing."
    echo ""
    echo "Flags:"
    echo "  -q,--quiet              Do not display detailed information during execution."
    echo "  -x,--debug              Display debug information about the script as it executes."
    echo "  -h,--help               Display this help text."
    echo ""
    exit 1
}

# Parse the command line.
parse_command_line() {

    VERBOSE_MODE=1
    DEBUG_MODE=0
    PARAMS=()
    while (( "$#" )); do
    case "$1" in
        -q|--quiet)
            VERBOSE_MODE=0
            shift
        ;;
        -x|--debug)
            DEBUG_MODE=1
            shift
        ;;
        -h|--help)
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

    if [[ $DEBUG_MODE -ne 0 ]] ; then
        set -x
    fi
}

# Check the packaging before we use it.
check_with_pyroma() {

    if [ "$VERBOSE_MODE" -ne 0 ]; then
        echo "Checking the application packaging against standards."
    fi
    if ! pipenv run pyroma -q -n 10 $SCRIPT_DIR > "$TEMP_FILE" 2>&1 ; then
        cat "$TEMP_FILE"
        complete_process 1 "Packaging script did not pass 'pyroma' inspection."
    fi
}

# Remove the previous artifacts to allow us to do this cleanly and predictably.
remove_previous_packaging_directories() {

    if [ "$VERBOSE_MODE" -ne 0 ]; then
        echo "Removing old directories."
    fi
    rm -rf  $SCRIPT_DIR/dist
    rm -rf  $SCRIPT_DIR/build
    rm -rf  $SCRIPT_DIR/PyMarkdown.egg-info
}

# Create the packaging required to be able to publish the application.
create_package() {

    if [ "$VERBOSE_MODE" -ne 0 ]; then
        echo "Creating package tarball. Logging output to '$SCRIPT_DIR/report/dist.log'."
    fi
    if ! pipenv run python setup.py sdist > "$SCRIPT_DIR/report/dist.log" ; then
        cat "$SCRIPT_DIR/report/dist.log"
        complete_process 1 "Package tarball creation failed."
    fi

    if [ "$VERBOSE_MODE" -ne 0 ]; then
        echo "Creating package wheel. Logging output to '$SCRIPT_DIR/report/wheel.log'."
    fi
    if ! pipenv run python setup.py bdist_wheel > "$SCRIPT_DIR/report/wheel.log" ; then
        cat "$SCRIPT_DIR/report/wheel.log"
        complete_process 1 "Package wheel creation failed."
    fi
}

# Inspect the built package with twine to make sure it follows standards.
check_package_with_twine() {

    if [ "$VERBOSE_MODE" -ne 0 ]; then
        echo "Checking the application package against standards."
    fi
    if ! pipenv run twine check dist/* > "$TEMP_FILE" 2>&1 ; then
        cat "$TEMP_FILE"
        complete_process 1 "Application package did not pass 'twine' inspection."
    fi
}

# Parse any command line values.
parse_command_line "$@"

start_process

# Main body of the script.

check_with_pyroma

remove_previous_packaging_directories

create_package

check_package_with_twine

complete_process 0
