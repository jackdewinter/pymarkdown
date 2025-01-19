#!/usr/bin/env bash

# Set the script mode to "strict".
# http://redsymbol.net/articles/unofficial-bash-strict-mode/ without the fail fast.
set -uo pipefail

# Set up any project based local script variables.
SCRIPT_NAME=$(basename -- "${BASH_SOURCE[0]}")
SCRIPT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" &>/dev/null && pwd)
TEMP_FILE=$(mktemp /tmp/$SCRIPT_NAME.XXXXXXXXX)

SCRIPT_TITLE="Running project tests"

TEST_RESULTS_XML_PATH=report/tests.xml
TEST_COVERAGE_XML_PATH=report/coverage.xml

PYSCAN_SCRIPT_PATH=project_summarizer

# Perform any cleanup required by the script.
cleanup_function() {

	# If the temp file was used, get rid of it.
	if [ -f "$TEMP_FILE" ]; then
		rm "$TEMP_FILE"
	fi

	# Restore the current directory.
	if [ "$DID_PUSHD" -eq 1 ]; then
		popd >/dev/null 2>&1 || exit
	fi
}

# Start the main part of the script off with a title.
start_process() {
	if [ "$VERBOSE_MODE" -ne 0 ]; then
		echo "Saving current directory prior to execution."
	fi
	if ! pushd . >"$TEMP_FILE" 2>&1; then
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

	if [ -n "$COMPLETE_REASON" ]; then
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
	echo "  Executes the tests for the project."
	echo ""
	echo "Flags:"
	echo "  -a,--all                Show all errors.  Otherwise, pytest will stop after the first 5 failures."
	echo "  -c,--coverage           Calculate the coverage for the tests."
	echo "  -d,--capture-directory  Capture the markdown for the test cases in the specified directory."
	echo "  -f,--full-report        Produce a full report for the executed tests instead of a 'changes only' report."
	echo "  -w,--workers            Enabled testing with multiple workers."
	echo "  -k,--keyword [keyword]  Execute only the tests matching the specified keyword."
	echo "  -p,--publish            Publish the project summaries of previously executed tests."
	echo "  -x,--debug              Display debug information about the script as it executes."
	echo "  -q,--quiet              Do not display detailed information during execution."
	echo "  -h,--help               Display this help text."
	echo ""
	exit 1
}

# Parse the command line.
parse_command_line() {

	PYSCAN_FULL_REPORT_MODE=0
	VERBOSE_MODE=1
	DEBUG_MODE=0
	COVERAGE_MODE=0
	PUBLISH_MODE=0
	MULTIPLE_WORKER_ARGS=
	KEYWORD_ARG=
	FAILURE_ARGS="--maxfail=5"
	CAPTURE_DIRECTORY=
	PARAMS=()
	while (("$#")); do
		case "$1" in
		-a | --all)
			FAILURE_ARGS=
			shift
			;;
		-c | --coverage)
			COVERAGE_MODE=1
			shift
			;;
		-d | --capture-directory)
			if [[ -z ${2:-} ]]; then
				echo "Error: Argument $1 must be followed by the path to the directory to use." >&2
				show_usage
			fi
			CAPTURE_DIRECTORY=$2
			if ! [[ -d $CAPTURE_DIRECTORY ]]; then
				echo "Error: Argument $1 must be followed by a path to an existing directory." >&2
				show_usage
			fi
			shift
			shift
			;;
		-f | --full-report)
			PYSCAN_FULL_REPORT_MODE=1
			shift
			;;
		-w | --workers)
			MULTIPLE_WORKER_ARGS=100
			shift
			;;
		-k | --keyword)
			if [ -z "${2:-}" ]; then
				echo "Error: Argument $1 must be followed by the keyword to use." >&2
				show_usage
			fi
			KEYWORD_ARG=$2
			shift
			shift
			;;
		-p | --publish)
			PUBLISH_MODE=1
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

# Handle the publishing mode, as it publishes previous tests results, not run new tests.
handle_publish_mode() {

	if [[ $PUBLISH_MODE -ne 0 ]]; then
		echo {Publishing summaries from last test run.}
		if ! pipenv run $PYSCAN_SCRIPT_PATH --publish; then
			complete_process 1 "{Publishing of test run summaries failed.}"
		fi
		complete_process 0 "{Publishing of test run summaries succeeded.}"
	fi
}

# Set test variables and their dependencies here, to keep the mainline cleaner.
set_test_variables() {

	# If we are testing by keyword, coverage and multi-core do not make sense.
	if [[ -n $KEYWORD_ARG ]]; then
		COVERAGE_MODE=
		MULTIPLE_WORKER_ARGS=
		KEYWORD_ARG="-k $KEYWORD_ARG"
	fi

	# If we are not told to do a full report, only do the changes.
	PYSCAN_OPTIONS=
	if [[ $PYSCAN_FULL_REPORT_MODE -eq 0 ]]; then
		PYSCAN_OPTIONS="--only-changes"
	fi

	# For multiple workers, default to half of the existing cores.
	if [[ -n $MULTIPLE_WORKER_ARGS ]]; then
		CORES_TO_USE=$MULTIPLE_WORKER_ARGS
		PROCESSOR_COUNT=$(python -c "import multiprocessing; print(multiprocessing.cpu_count())")
		if [[ $MULTIPLE_WORKER_ARGS -gt $PROCESSOR_COUNT ]]; then
			CORES_TO_USE=$((PROCESSOR_COUNT / 2))
		fi
		if [ $CORES_TO_USE -lt 1 ]; then
			CORES_TO_USE=1
		fi
		MULTIPLE_WORKER_ARGS="-n $CORES_TO_USE --dist loadscope"
	fi
}

# Execute the tests themselves.
execute_tests() {

	local pytest_args=
	TEST_EXECUTION_SUCCEEDED=1

	# Setup the args to reflect the mode in which the tests are to be invoked.
	if [[ -n $KEYWORD_ARG ]]; then
		echo "{Executing partial test suite...}"
	else
		pytest_args="--strict-markers -ra --junitxml=$TEST_RESULTS_XML_PATH --html=report/report.html"
		if [[ $COVERAGE_MODE -ne 0 ]]; then
			echo "{Executing full test suite with coverage...}"
			pytest_args="$pytest_args --cov --cov-branch --cov-report xml:$TEST_COVERAGE_XML_PATH --cov-report html:report/coverage"
		else
			echo "{Executing full test suite...}"
		fi
	fi

	# If asked to capture input markdown documents, set the environment variable to allow the
	# testing of the application to know to write them out to that directory.
	if [[ -n $CAPTURE_DIRECTORY ]]; then
		export PTEST_KEEP_DIRECTORY="$CAPTURE_DIRECTORY"
		rm $PTEST_KEEP_DIRECTORY/*.md >$TEMP_FILE 2>&1
	fi

	# Run the tests.
	if [[ $VERBOSE_MODE -ne 0 ]]; then
		if ! pipenv run pytest $MULTIPLE_WORKER_ARGS $FAILURE_ARGS $KEYWORD_ARG $pytest_args; then
			TEST_EXECUTION_SUCCEEDED=0
		fi
	else
		if ! pipenv run pytest $MULTIPLE_WORKER_ARGS $FAILURE_ARGS $KEYWORD_ARG $pytest_args >$TEMP_FILE 2>&1; then
			TEST_EXECUTION_SUCCEEDED=0
		fi
	fi

	# If there are "incomplete" testcases in the file, then we were interupted.
	if grep "<testcase time=" report/tests.xml >$TEMP_FILE 2>&1; then
		complete_process 1 "{Execution of full tests was interupted. Additional processing skipped.}"
	fi
}

# Summarize the test executions, and if coverage is enabled, any change in coverage.
summarize_test_executions() {

	# Determine if we report on the tests, or tests + coverage.
	PYSCAN_REPORT_OPTIONS="--junit $TEST_RESULTS_XML_PATH"
	if [[ $COVERAGE_MODE -ne 0 ]]; then
		if [[ $TEST_EXECUTION_SUCCEEDED -ne 0 ]]; then
			PYSCAN_REPORT_OPTIONS="$PYSCAN_REPORT_OPTIONS --cobertura $TEST_COVERAGE_XML_PATH"
		else
			echo "{Coverage was specified, but one or more tests failed.  Skipping reporting of coverage.}"
		fi
	fi

	echo "{Summarizing changes in execution of full test suite.}"
	if ! pipenv run "$PYSCAN_SCRIPT_PATH" $PYSCAN_OPTIONS $PYSCAN_REPORT_OPTIONS; then
		echo ""
		complete_process 1 "{Summarizing changes in execution of full test suite failed.}"
	fi
}

# Parse any command line values.
parse_command_line "$@"

# Clean entrance into the script.
start_process

handle_publish_mode

set_test_variables

execute_tests

if [[ -n $KEYWORD_ARG ]]; then
	if [[ $TEST_EXECUTION_SUCCEEDED -eq 0 ]]; then
		complete_process 1 "{Execution of partial test suite failed.}"
	fi
	complete_process 0 "{Execution of partial test suite succeeded.}"
fi

summarize_test_executions

if [[ $TEST_EXECUTION_SUCCEEDED -eq 0 ]]; then
	complete_process 1 "{Execution of full test suite failed.}"
fi
complete_process 0 "{Execution of full test suite succeeded.}"
