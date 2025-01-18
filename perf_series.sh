#!/usr/bin/env bash

# Set the script mode to "strict".
# http://redsymbol.net/articles/unofficial-bash-strict-mode/ without the fail fast.
set -uo pipefail

# Set up any project based local script variables.
SCRIPT_NAME=$( basename -- "${BASH_SOURCE[0]}" )
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
TEMP_FILE=$(mktemp /tmp/$SCRIPT_NAME.XXXXXXXXX)

SCRIPT_TITLE="Batch profiling of application"

TEST_FILE_DIRECTORY="${SCRIPT_DIR}/build/ptest"

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
    if ! pushd . >"$TEMP_FILE" 2>&1;  then
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
    local SCRIPT_NAME=$0

    echo "Usage:"
    echo "  $(basename "$SCRIPT_NAME") [flags]"
    echo ""
    echo "Summary:"
    echo "  Executes a scan of a constructed document, capturing timing measurements."
    echo ""
    echo "Flags:"
    echo "  -s,--start              Repeat count to start at."
    echo "  -e,--end                Repeat count to end at."
    echo "  -l,--list               List of comma separated repeat counts to use instead of -s and -e."
    echo "  -c,--count              Count of times for each series of repeats."
    echo "  -o,--only-first         Only clear the Python cache at the start of the series."
    echo "  -t,--tag                Tag to associate with this series of tests."
    echo "  -nr,--no-rules          Take measurements without processing any rules {Parser only.}"
    echo "  -x,--debug              Display debug information about the script as it executes."
    echo "  -q,--quiet              Do not display detailed information during execution."
    echo "  -h,--help               Display this help text."
    echo ""
    echo "Example:"
    echo "  To run a series of tests, from 10 to 15 repeats:"
    echo "    $(basename "$SCRIPT_NAME") -s 10 -e 15"
    echo "  To run a series of tests, from 10 to 15 repeats, twice:"
    echo "    $(basename "$SCRIPT_NAME") -s 10 -e 15 --count 2"
    echo "  To run a series of tests, only 10 and 15 repeats, twice:"
    echo "    $(basename "$SCRIPT_NAME") -l 10_15 --count 2"
    exit 1
}

# Parse the command line.
parse_command_line() {

    NO_RULES_MODE=0
    DEBUG_MODE=0
    ONLY_FIRST=0
    VERBOSE_MODE=1
    TEST_SERIES_TAG=
    NUM_COUNT=1
    NUM_MINIMUM=1
    NUM_MAXIMUM=2
    ALTERNATE_REPEAT_LIST=
    PARAMS=()
    while (( "$#" )); do
    case "$1" in
        -s|--start)
            if [ -z "${2:-}" ] ; then
                echo "Error: Argument $1 must be followed by the number of repeats to start at." >&2
                show_usage
            fi
            NUM_MINIMUM=$2
            if ! [[ $NUM_MINIMUM =~ ^[1-9][0-9]*$ ]]; then
                echo "${NUM_MINIMUM} is not an integer"
                echo "Error: Argument $1 is not followed by a valid number: ${NUM_MINIMUM}" >&2
                show_usage
            fi
            shift
            shift
        ;;
        -e|--end)
            if [ -z "${2:-}" ] ; then
                echo "Error: Argument $1 must be followed by the number of repeats to start at." >&2
                show_usage
            fi
            NUM_MAXIMUM=$2
            if ! [[ $NUM_MAXIMUM =~ ^[1-9][0-9]*$ ]]; then
                echo "${NUM_MAXIMUM} is not an integer"
                echo "Error: Argument $1 is not followed by a valid number: ${NUM_MAXIMUM}" >&2
                show_usage
            fi
            shift
            shift
        ;;
        -c|--count)
            if [ -z "${2:-}" ] ; then
                echo "Error: Argument $1 must be followed by the number of series to execute." >&2
                show_usage
            fi
            NUM_COUNT=$2
            if ! [[ $NUM_COUNT =~ ^[1-9][0-9]*$ ]]; then
                echo "${NUM_COUNT} is not an integer"
                echo "Error: Argument $1 is not followed by a valid number: ${NUM_COUNT}" >&2
                show_usage
            fi
            shift
            shift
        ;;
        -l|--list)
            if [ -z "${2:-}" ] ; then
                echo "Error: Argument $1 must be followed by a list of repeat counts." >&2
                show_usage
            fi
            ALTERNATE_REPEAT_LIST=$2
            shift
            shift
        ;;
        -t|--tag)
            if [ -z "${2:-}" ] ; then
                echo "Error: Argument $1 must be followed by the tag to use." >&2
                show_usage
            fi
            TEST_SERIES_TAG=$2
            shift
            shift
        ;;
        -o|--only-first)
            ONLY_FIRST=1
            shift
        ;;
        -nr|--no-rules)
            NO_RULES_MODE=1
            shift
        ;;
        -x|--debug)
            DEBUG_MODE=1
            shift
        ;;
        -q|--quiet)
            VERBOSE_MODE=0
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

# Parse any command line values.
parse_command_line "$@"

# Clean entrance into the script.
start_process

# Determine whether the CSV file will be written to and make sure that the directory exists.
if [[ -n "$TEST_SERIES_TAG" ]] ; then
    DEST_FILE="build/series-${TEST_SERIES_TAG}.csv"
else
    DEST_FILE=build/series.csv
fi

if ! mkdir -p $(dirname "${DEST_FILE}") > "${TEMP_FILE}" 2>&1 ; then
    cat "${TEMP_FILE}"
    complete_process 1 "{Creating test report directory failed.}"
fi
rm "${DEST_FILE}" > /dev/null 2>&1

# Set up so we can pass the '--no-rules' argument to the perf_sample.sh script.
PERF_SAMPLE_ARGS=
if [[ $NO_RULES_MODE -ne 0 ]] ; then
    PERF_SAMPLE_ARGS="--no-rules "
fi

# If asked to only clear the python cache for the first sample, do so before
# any samples are taken, and make sure any following calls do not clear the cache.
if [[ $ONLY_FIRST -ne 0 ]] ; then
    if ! $SCRIPT_DIR/perf_sample.sh -nr --repeats 1 > ${TEMP_FILE} 2>&1 ; then
        cat "${TEMP_FILE}"
        complete_process 1 "Executing warmup run before series failed."
    fi
    PERF_SAMPLE_ARGS="$PERF_SAMPLE_ARGS --no-clear-cache"
fi

# Repeat the samples NUM_COUNT times. 
for i in $(seq ${NUM_COUNT}); do
    echo "Times Through Series: $i"

    # If a comma separated repeat list, cycle through it...
    if [[ -n $ALTERNATE_REPEAT_LIST ]] ; then

        IFS=',' read -r -a repeat_array <<< "$ALTERNATE_REPEAT_LIST"
        for REPEAT_COUNT in "${repeat_array[@]}"; do

            echo "  Repeat Count: $REPEAT_COUNT"
            if ! $SCRIPT_DIR/perf_sample.sh ${PERF_SAMPLE_ARGS} --repeats $REPEAT_COUNT -c ${DEST_FILE}  > ${TEMP_FILE} 2>&1 ; then
                cat "${TEMP_FILE}"
                complete_process 1 "Executing profile run for $REPEAT_COUNT repeats failed."
            fi

        done    

    # ... otherwise, do a simple loop.
    else
        REPEAT_COUNT=$NUM_MINIMUM
        while [ $REPEAT_COUNT -le $NUM_MAXIMUM ] ; do

            echo "  Repeat Count: $REPEAT_COUNT"
            if ! $SCRIPT_DIR/perf_sample.sh ${PERF_SAMPLE_ARGS} --repeats $REPEAT_COUNT -c ${DEST_FILE}  > ${TEMP_FILE} 2>&1 ; then
                cat "${TEMP_FILE}"
                complete_process 1 "Executing profile run for $REPEAT_COUNT repeats failed."
            fi

            ((REPEAT_COUNT++))
        done
    fi
done


echo ""
echo "CSV file '${DEST_FILE}' written with sample timings."

complete_process 0
