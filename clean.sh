#!/usr/bin/env bash

# Set the script mode to "strict".
# http://redsymbol.net/articles/unofficial-bash-strict-mode/ without the fail fast.
set -uo pipefail

# Set up any project based local script variables.
SCRIPT_NAME=$(basename -- "${BASH_SOURCE[0]}")
SCRIPT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" &>/dev/null && pwd)
TEMP_FILE=$(mktemp /tmp/$SCRIPT_NAME.XXXXXXXXX)

SCRIPT_TITLE="Analyzing project cleanliness"

# Perform any cleanup required by the script.
cleanup_function() {

	if [[ $VERBOSE_MODE -ne 0 ]]; then
		echo "{Performing clean up for script '$SCRIPT_NAME'.}"
	fi

	# If the temp file was used, get rid of it.
	if [ -f "$TEMP_FILE" ]; then
		rm "$TEMP_FILE"
	fi

	# Restore the current directory.
	if [ "$DID_PUSHD" -eq 1 ]; then
		popd >/dev/null 2>&1 || exit
	fi
}

verbose_echo() {
	echo_text=${1:-}

	if [ "$VERBOSE_MODE" -ne 0 ]; then
		echo $echo_text
	fi
}

# Start the main part of the script off with a title.
start_process() {
	verbose_echo "$SCRIPT_TITLE..."
	verbose_echo ""
	verbose_echo "{Saving current directory prior to execution.}"
	if ! pushd . >"$TEMP_FILE" 2>&1; then
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

	if [ -n "$COMPLETE_REASON" ]; then
		echo "$COMPLETE_REASON"
	fi

	if [ "$SCRIPT_RETURN_CODE" -ne 0 ]; then
		echo ""
		echo "$SCRIPT_TITLE failed."
	else
		verbose_echo ""
		verbose_echo "$SCRIPT_TITLE succeeded."
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
	echo "  -f,--force-reset <ver>  Force a reset of the virtual environment, with an optional python version to reset to."
	echo "  -m,--mypy-only          Only run mypy checks and exit."
	echo "  -np,--no-publish        Do not publish project summaries if successful."
	echo "  -ns,--no-sourcery       Do not run any sourcery checks."
	echo "  -s,--sourcery-only      Only run sourcery checks and exit."
	echo "  --perf                  Collect standard performance metrics."
	echo "  --perf-only             Only collect standard performance metrics."
	echo "  -x,--debug              Display debug information about the script as it executes."
	echo "  -q,--quiet              Do not display detailed information during execution."
	echo "  -h,--help               Display this help text."
	echo ""
	exit 1
}

# Parse the command line.
parse_command_line() {

	PUBLISH_MODE=1
	VERBOSE_MODE=1
	PERFORMANCE_MODE=0
	PERFORMANCE_ONLY_MODE=0
	DEBUG_MODE=0
	MYPY_ONLY_MODE=0
	SOURCERY_ONLY_MODE=0
	NO_SOURCERY_MODE=0
	FORCE_RESET_MODE=0
	RESET_PYTHON_VERSION=
	PARAMS=()
	while (("$#")); do
		case "$1" in
		-f | --force-reset)
			FORCE_RESET_MODE=1
			x=${2:-0}
			if [[ $x == 3* ]]; then
				RESET_PYTHON_VERSION=$x
				shift
			fi
			shift
			;;
		-m | --mypy-only)
			MYPY_ONLY_MODE=1
			shift
			;;
		-np | --no-publish)
			PUBLISH_MODE=0
			shift
			;;
		-ns | --no-sourcery)
			NO_SOURCERY_MODE=1
			shift
			;;
		-s | --sourcery-only)
			SOURCERY_ONLY_MODE=1
			shift
			;;
		--perf)
			PERFORMANCE_MODE=1
			shift
			;;
		--perf-only)
			PERFORMANCE_ONLY_MODE=1
			PERFORMANCE_MODE=1
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

	if [[ $NO_SOURCERY_MODE -ne 0 ]] && [[ $SOURCERY_ONLY_MODE -ne 0 ]]; then
		echo "{Script's no-sourcery mode has precedence over the script's sourcery-only mode. Disabling sourcery only mode.}"
		SOURCERY_ONLY_MODE=0
	fi

	if [[ $SOURCERY_ONLY_MODE -ne 0 ]] && [[ $MYPY_ONLY_MODE -ne 0 ]] && [[ $$PERFORMANCE_ONLY_MODE -ne 0 ]]; then
		echo "Options '--perf-only', '-m|--mypy-only' and '-s,--sourcery-only' conflict with each other.  Please choose one and try again."
		exit 1
	fi
}

load_properties_from_file() {

	verbose_echo "{Loading 'project.properties file'...}"
	while IFS='=' read -r key_value; do
		if [[ $key_value == \#* ]]; then
			continue
		fi
		key=$(echo "$key_value" | cut -d '=' -f1)
		value=$(echo "$key_value" | cut -d '=' -f2-)
		export "$key=$value"
	done <$SCRIPT_DIR/project.properties

	if [[ -z $PYTHON_MODULE_NAME ]]; then
		complete_process 1 "Property 'PYTHON_MODULE_NAME' must be defined in the project.properties file."
	fi
}

remove_virtual_environment() {

	verbose_echo "{Forcing a hard reset of the virtual environment.}"
	if ! VENV_DIR=$(pipenv --venv); then
		verbose_echo "{Virtual environment was not established.  Reset not required. Proceeding to setup virtual environment.}"
		RESET_PIPFILE=1
	fi

	if [[ $RESET_PIPFILE -eq 0 ]]; then
		if ! [[ -d $VENV_DIR/S2 ]]; then
			verbose_echo "{Creating temporary directory '$VENV_DIR/S2' for move test.}"
			if ! mkdir $VENV_DIR/S2; then
				complete_process 1 "{Cannot mkdir test directory for virtual environment lock test.}"
			fi
		fi

		verbose_echo "{Executing move test to see if one or more files in directory '$VENV_DIR' are locked.}"
		if ! mv "$VENV_DIR\Scripts" "$VENV_DIR\S2" >$TEMP_FILE; then
			cat $TEMP_FILE
			echo "  {One or more directories in $VENV_DIR are locked.}"
			echo "  {Close any open IDEs or shells in that directory and try again.}"
			echo "  {If lock persists, try pipenv --rm to try and force the lock to be released.}"
			complete_process 1
		fi

		verbose_echo "{Removing previous PipEnv environment.}"
		if ! rm -rf "$VENV_DIR"; then
			complete_process 1 "bad rmdir"
		fi

		if ! [[ -d $VENV_DIR ]]; then
			verbose_echo "{Virtual environment directory has been removed successfully.}"
			RESET_PIPFILE=1
		else
			echo "  {One or more directories in $VENV_DIR are locked.}"
			echo "  {Close any open IDEs or shells in that directory and try again.}"
			echo "  {If lock persists, try pipenv --rm to try and force the lock to be released.}"
			complete_process 1
		fi
	fi

	if [[ -z $RESET_PYTHON_VERSION ]]; then
		RESET_PYTHON_VERSION=$(python utils/extract_python_version_from_pipfile.py)
	fi
}

check_for_unsychronized_virtual_environment() {

	python utils/find_outdated_piplock_file.py >"$TEMP_FILE" 2>&1
	OUTDATED_PIPLOCK_RETCODE=$?
	if [[ $OUTDATED_PIPLOCK_RETCODE -eq 2 ]]; then
		cat "$TEMP_FILE"
		complete_process 1 "{Analysis of project cannot proceed without a Pipfile.}"
	fi
	if [[ $OUTDATED_PIPLOCK_RETCODE -ne 0 ]]; then
		verbose_echo "{Virtual environment files 'Pipfile' and 'Pipfile.lock' are not in sync with each other.}"
		RESET_PIPFILE=1

		RESET_PYTHON_VERSION=$(pipenv run python -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
	fi
}

synchronize_virtual_environment() {

	verbose_echo "{Syncing python packages in virtual environment.}"
	rm Pipfile.lock >/dev/null 2>&1
	if ! pipenv lock --python $RESET_PYTHON_VERSION >"$TEMP_FILE" 2>&1; then
		cat "$TEMP_FILE"
		complete_process 1 "{Creating new Pipfile.lock file failed.}"
	fi
	if ! pipenv update -d >"$TEMP_FILE" 2>&1; then
		cat "$TEMP_FILE"
		complete_process 1 "{Updating with new Pipfile.lock file failed.}"
	fi

	verbose_echo "{Python packages in virtual environment synced.}"
}

execute_pre_commit() {

	verbose_echo ""
	verbose_echo "{Executing pre-commit hooks on Python code.}"
	PRE_COMMIT_ARGS=
	if [[ $PUBLISH_MODE -ne 0 ]]; then
		PRE_COMMIT_ARGS="--all"
	fi
	if [[ $MYPY_ONLY_MODE -ne 0 ]]; then
		PRE_COMMIT_ARGS="$PRE_COMMIT_ARGS mypy"
	fi
	echo ""
	if ! pipenv run pre-commit run $PRE_COMMIT_ARGS; then
		complete_process 1 "{Executing pre-commit hooks on Python code failed.}"
	fi
	echo ""
}

load_sourcery_configuration() {

	echo ""
	if [[ -z ${SOURCERY_USER_KEY:-} ]]; then
		SOURCERY_BATCH_FILE_PATH=$SCRIPT_DIR/../sourcery.bat
		if [[ -f $SOURCERY_BATCH_FILE_PATH ]]; then
			verbose_echo "{Variable 'SOURCERY_USER_KEY' not defined, but Windows '$SOURCERY_BATCH_FILE_PATH' script detected.}"
			verbose_echo "{Attempting to load variable 'SOURCERY_USER_KEY' from '$SOURCERY_BATCH_FILE_PATH' script.}"
			while IFS='=' read -r key_value; do
				key=$(echo "$key_value" | cut -d '=' -f1)
				value=$(echo "$key_value" | cut -d '=' -f2-)
				if [[ $key == "set SOURCERY_USER_KEY" ]]; then
					export SOURCERY_USER_KEY="$value"
				fi
			done <$SCRIPT_DIR/../sourcery.bat
			if [[ -z $SOURCERY_USER_KEY ]]; then
				complete_process 1 "{Unable to load SOURCERY_USER_KEY value from file.}"
			fi
		else
			complete_process 1 "{Variable 'SOURCERY_USER_KEY' is not defined and no sourceable script detected.}"
		fi
	fi
}

execute_sourcery() {

	verbose_echo "{Executing Sourcery static analyzer on Python code.}"
	if ! pipenv run sourcery login --token $SOURCERY_USER_KEY; then
		complete_process 1 "{Login to Sourcery failed.}"
	fi

	if [[ $PUBLISH_MODE -ne 0 ]]; then
		verbose_echo "{  Executing Sourcery against full project contents.}"
		SOURCERY_LIMIT=
	else
		verbose_echo "{  Executing Sourcery against changed project contents.}"
		SOURCERY_LIMIT='--diff "git diff"'
	fi

	if ! pipenv run sourcery review --check pymarkdown $SOURCERY_LIMIT; then
		complete_process 1 "{Executing Sourcery on Python code failed.}"
	fi
}

find_unused_pylint_suppressions() {

	SCAN_FILES=
	git diff --name-only --staged >"$TEMP_FILE"
	while IFS= read -r line; do
		if [[ $line == *.py ]] && [[ $line != "pytest_execute.py" ]]; then
			SCAN_FILES="$SCAN_FILES $line"
		fi
	done <"$TEMP_FILE"

	echo ""
	if [[ -z $SCAN_FILES ]]; then
		verbose_echo "{Not executing pylint suppression checker on Python source code. No eligible Python files staged.}"
	else
		verbose_echo "{Executing pylint suppression checker on Python source code.}"
		if ! pipenv run pylint_utils -s $SCAN_FILES; then
			complete_process 1 "{Executing reporting of unused pylint suppressions in modified Python source code failed.}"
		fi
	fi
}

publish_analysis_results_if_requested() {

	echo ""
	if [[ $PUBLISH_MODE -ne 0 ]]; then
		if [[ $NO_SOURCERY_MODE -ne 0 ]]; then
			complete_process 1 "Publish mode requires that all scans are performed, but the sourcery scan was disabled.  Please re-enable sourcery and try again."
		fi

		verbose_echo "{Publishing summaries after successful analysis of project.}"
		if ! ./ptest.sh -p; then
			complete_process 1 "{Publishing summaries failed.}"
		fi
	fi
}

analyze_pylint_suppressions() {

	echo ""
	verbose_echo "{Executing pylint utils analyzer on Python source code to verify suppressions and document them.}"
	if ! pipenv run pylint_utils --recurse -r $SCRIPT_DIR/publish/pylint_suppression.json $PYTHON_MODULE_NAME; then
		complete_process 1 "{Executing reporting of pylint suppressions in Python source code failed.}"
	fi
}

execute_test_suite() {

	echo ""
	verbose_echo "{Executing unit tests on Python code.}"
	if ! ./ptest.sh --coverage --workers; then
		complete_process 1 "{Executing application tests failed.}"
	fi
}

execute_performance_suite() {

	echo ""
	verbose_echo "{Executing performance tests on application.}"
	rm -f $SCRIPT_DIR/build/series.csv
	./perf_series.sh --count 5 --list 1,2,3,4,5,10,15,20,25,30,35,40,45,50,60,70,80,90,100 --only-first
	cp $SCRIPT_DIR/build/series.csv $SCRIPT_DIR/publish/perf-with-rules.csv
	./perf_series.sh --no-rules --count 5 --list 1,2,3,4,5,10,15,20,25,30,35,40,45,50,60,70,80,90,100 --only-first
	cp $SCRIPT_DIR/build/series.csv $SCRIPT_DIR/publish/perf-without-rules.csv
}

# Parse any command line values.
parse_command_line "$@"

# Clean entrance into the script.
start_process

load_properties_from_file

RESET_PIPFILE=0
if [[ $FORCE_RESET_MODE -ne 0 ]]; then
	remove_virtual_environment
else
	check_for_unsychronized_virtual_environment
fi

if [[ $RESET_PIPFILE -ne 0 ]]; then
	synchronize_virtual_environment
fi

if [[ $SOURCERY_ONLY_MODE -eq 0 ]] && [[ $PERFORMANCE_ONLY_MODE -eq 0 ]]; then
	execute_pre_commit

	if [[ $MYPY_ONLY_MODE -ne 0 ]]; then
		complete_process 0
	fi
fi

if [[ $NO_SOURCERY_MODE -ne 0 ]] || [[ $PERFORMANCE_ONLY_MODE -ne 0 ]]; then
	echo "{Skipping Sourcery static analyzer by request.}"
else
	load_sourcery_configuration

	execute_sourcery

	if [[ $SOURCERY_ONLY_MODE -ne 0 ]]; then
		complete_process 0
	fi
fi

if [[ $PERFORMANCE_ONLY_MODE -eq 0 ]]; then
	analyze_pylint_suppressions

	find_unused_pylint_suppressions

	execute_test_suite
fi

if [[ $PERFORMANCE_MODE -ne 0 ]]; then
	execute_performance_suite
fi

publish_analysis_results_if_requested

# Normal exit from the script.
complete_process 0
