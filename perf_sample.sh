#!/usr/bin/env bash

# Set the script mode to "strict".
# http://redsymbol.net/articles/unofficial-bash-strict-mode/ without the fail fast.
set -uo pipefail

# Set up any project based local script variables.
SCRIPT_NAME=$(basename -- "${BASH_SOURCE[0]}")
SCRIPT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" &>/dev/null && pwd)
TEMP_FILE=$(mktemp /tmp/"${SCRIPT_NAME}".XXXXXXXXX)
TEMP_PERF_OUTPUT=$(mktemp /tmp/"${SCRIPT_NAME}".XXXXXXXXX)

SCRIPT_TITLE="Profiling application constructed sample file"

TEST_FILE_DIRECTORY="${SCRIPT_DIR}/build/ptest"

# Perform any cleanup required by the script.
# shellcheck disable=SC2317  # Unreachable code
cleanup_function() {

	# If the temp file was used, get rid of it.
	if [ -f "${TEMP_FILE}" ]; then
		rm "${TEMP_FILE}"
	fi
	if [ -f "${TEMP_PERF_OUTPUT}" ]; then
		rm "${TEMP_PERF_OUTPUT}"
	fi

	# Restore the current directory.
	popd >/dev/null 2>&1 || exit
}

# Start the main part of the script off with a title.
start_process() {
	if [ "${VERBOSE_MODE}" -ne 0 ]; then
		echo "Saving current directory prior to execution."
	fi
	if ! pushd "${SCRIPT_DIR}" >"${TEMP_FILE}" 2>&1; then
		cat "${TEMP_FILE}"
		complete_process 1 "Script cannot save the current directory before proceeding."
	fi
	trap cleanup_function EXIT

	if [ "${VERBOSE_MODE}" -ne 0 ]; then
		echo "${SCRIPT_TITLE}..."
	fi
}

# Simple function to stop the process with information about why it stopped.
complete_process() {
	local SCRIPT_RETURN_CODE=${1}
	local COMPLETE_REASON=${2:-}

	if [ -n "${COMPLETE_REASON}" ]; then
		echo "${COMPLETE_REASON}"
	fi

	if [ "${SCRIPT_RETURN_CODE}" -ne 0 ]; then
		echo "${SCRIPT_TITLE} failed."
	else
		if [ "${VERBOSE_MODE}" -ne 0 ]; then
			echo "${SCRIPT_TITLE} succeeded."
		fi
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
	echo "  Executes a scan of a constructed document, capturing timing measurements."
	echo ""
	echo "Flags:"
	echo "  -c,--csv-file {file}    Append results to file in CSV format."
	echo "  -r,--repeats {num}      Number of repititions of the test document to merge together. Default 10."
	echo "  -nr,--no-rules          Take measurements without processing any rules {Parser only.}"
	echo "  -nc,--no-clear-cache    Do not clear the Python cache. Only recommended for repeated calls of this script."
	echo "  -v,--view               View the measured performance metrics."
	echo "  -x,--debug              Display debug information about the script as it executes."
	echo "  -q,--quiet              Do not display detailed information during execution."
	echo "  -h,--help               Display this help text."
	echo ""
	exit 1
}

# Parse the command line.
parse_command_line() {

	NO_RULES_MODE=0
	NO_CLEAR_MODE=0
	DEBUG_MODE=0
	VIEW_MODE=0
	VERBOSE_MODE=1
	NUM_REPEATS=10
	CSV_OUTPUT=
	PARAMS=()
	while (("$#")); do
		case "$1" in
		-c | --csv-file)
			if [ -z "${2:-}" ]; then
				echo "Error: Argument ${1} must be followed by the file to write to." >&2
				show_usage
			fi
			CSV_OUTPUT=${2}
			shift
			shift
			;;
		-r | --repeats)
			if [ -z "${2:-}" ]; then
				echo "Error: Argument ${1} must be followed by the number of repititions to use." >&2
				show_usage
			fi
			NUM_REPEATS=${2}
			if ! [[ ${NUM_REPEATS} =~ ^[1-9][0-9]*$ ]]; then
				echo "${NUM} is not an integer"
				echo "Error: Argument ${1} is not followed by a valid number: ${NUM_REPEATS}" >&2
				show_usage
			fi
			shift
			shift
			;;
		-v | --view)
			VIEW_MODE=1
			shift
			;;
		-nr | --no-rules)
			NO_RULES_MODE=1
			shift
			;;
		-nc | --no-clear-cache)
			NO_CLEAR_MODE=1
			shift
			;;
		-x | --debug)
			DEBUG_MODE=1
			shift
			;;
		-q | --quiet)
			VERBOSE_MODE=0
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

# Get the executable path for the current bash shell.
BASH_EXEC=${BASH}
if [[ ${MSYSTEM:-} =~ ^MINGW(64|32)$ ]]; then
	WINPID=$(ps -p $$ | awk 'NR ==2{print $4}')
	if [[ -z ${WINPID} ]]; then
		echo "Cannot get Windows PID for Bash shell."
		exit 1
	fi
	BASH_EXEC="$(wmic process where "ProcessID=${WINPID}" get ExecutablePath | sed -n 2p | sed 's/\\/\\\\/g')"
fi

# Parse any command line values.
parse_command_line "$@"

# Clean entrance into the script.
start_process

SINGLE_TEST_SOURCE_FILE=test/resources/performance/sample.md
SINGLE_TEST_DESTINATION_FILE="${TEST_FILE_DIRECTORY}"/test.md

# Make sure we have a directory to create the test files for profiling in, and ensure
# that it is empty before we start processing.
if ! mkdir -p "${TEST_FILE_DIRECTORY}" >"${TEMP_FILE}" 2>&1; then
	cat "${TEMP_FILE}"
	complete_process 1 "{Creating test report directory failed.}"
fi
rm -r "${TEST_FILE_DIRECTORY:?}"/* >/dev/null 2>&1

# Create a composite document with NUM_REPEATS copies of the source document.
echo "Creating single document with ${NUM_REPEATS} copies of '${SINGLE_TEST_SOURCE_FILE}'."
for _ in $(seq "${NUM_REPEATS}"); do
	cat "${SINGLE_TEST_SOURCE_FILE}" >>"${SINGLE_TEST_DESTINATION_FILE}"
done

# Remove any __pycache__ related files unless asked not to.
if [[ ${NO_CLEAR_MODE} -eq 0 ]]; then
	echo "Resetting Python caches..."
	PYTHONPYCACHEPREFIX="${SCRIPT_DIR}"/.pycache
	rm -r "${PYTHONPYCACHEPREFIX}" >/dev/null 2>&1
	if ! python3 -Bc "import pathlib; [p.unlink() for p in pathlib.Path('.').rglob('*.py[co]')]" >"${TEMP_FILE}" 2>&1; then
		cat "${TEMP_FILE}"
		complete_process 1 "{Creating test report directory failed.}"
	fi
	if ! python3 -Bc "import pathlib; [p.rmdir() for p in pathlib.Path('.').rglob('__pycache__')]" >"${TEMP_FILE}" 2>&1; then
		cat "${TEMP_FILE}"
		complete_process 1 "{Creating test report directory failed.}"
	fi

	# ... and then take the steps to properly create any needed caching by running through a single pass once.
	if ! python -m compileall pymarkdown >"${TEMP_FILE}" 2>&1; then
		cat "${TEMP_FILE}"
		complete_process 1 "{Pre-compilation of project failed.}"
	fi
	if ! python -OO -c "import subprocess; subprocess.run(['${BASH_EXEC}','run.sh','scan','${SINGLE_TEST_SOURCE_FILE}'])" >"${TEMP_FILE}" 2>&1; then
		cat "${TEMP_FILE}"
		complete_process 1 "{Pre-measurement pass of project failed.}"
	fi
else
	echo "Resetting Python caches skipped by request."
fi

NO_RULES_ARGS=
if [[ ${NO_RULES_MODE} -ne 0 ]]; then
	NO_RULES_ARGS="'--disable-rules','*',"
fi

echo "Scanning created document..."
python -OO -c "import subprocess,os,time; \
    my_env = os.environ.copy();\
    my_env['PYMARKDOWNLINT__PERFRUN'] = '1';\
    start_time = time.time();\
    subprocess.run(['${BASH_EXEC}','run.sh',${NO_RULES_ARGS}'scan','${SINGLE_TEST_DESTINATION_FILE}'], env=my_env);\
    value = time.time() - start_time;\
    print(f'{value:.3f}');\
    " >"${TEMP_PERF_OUTPUT}" 2>&1
echo "Document scanning completed."

EXECUTION_TIME=$(tail -n 1 "${TEMP_PERF_OUTPUT}")
LINES_IN_PROF_OUTPUT=$(sed -n '$=' "${TEMP_PERF_OUTPUT}")

if [[ -n ${CSV_OUTPUT} ]]; then
	echo "${NUM_REPEATS},${LINES_IN_PROF_OUTPUT},${EXECUTION_TIME}" >>"${CSV_OUTPUT}"
else
	echo ""
	echo "Repeats in File: ${NUM_REPEATS}"
	echo "Lines in output: ${LINES_IN_PROF_OUTPUT}"
	echo "Execution time:  ${EXECUTION_TIME}"
	echo ""
fi

# If in view mode, use SnakeViz to visualize.
if [[ ${VIEW_MODE} -ne 0 ]]; then
	echo ""
	echo "Starting SnakeViz to view performance profile..."
	pipenv run snakeviz p0.prof
fi

complete_process 0
