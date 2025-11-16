#!/usr/bin/env bash

# Set the script mode to "strict".
# http://redsymbol.net/articles/unofficial-bash-strict-mode/ without the fail fast.
set -uo pipefail

# Perform any setup required by the script.
setup_function() {

	# Set up any required script variables.
	SCRIPT_NAME=$(basename -- "${BASH_SOURCE[0]}")
	SCRIPT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" &>/dev/null && pwd)

	# Create a temp file for use in the script.
	TEMP_FILE=$(mktemp /tmp/"${SCRIPT_NAME}".XXXXXXXXX)

	# Save the current directory and change to the script directory.
	if ! pushd "${SCRIPT_DIR}" >"${TEMP_FILE}" 2>&1; then
		cat "${TEMP_FILE}"
		echo "Script cannot save the current directory before proceeding."
		rm "${TEMP_FILE}"
		exit 1
	fi
}

# Perform any cleanup required by the script.
# shellcheck disable=SC2317  # Unreachable code
cleanup_function() {

	# If the temp file was used, get rid of it.
	if [ -f "${TEMP_FILE}" ]; then
		rm "${TEMP_FILE}"
	fi

	# Restore the current directory.
	popd >/dev/null 2>&1 || exit

	export PYTEST_ANNOTATE_USER_PROPERTIES=
}

# Give the user hints on how the script can be used.
show_usage() {
	echo "Usage:"
	echo "  ${SCRIPT_NAME} [flags]"
	echo ""
	echo "Summary:"
	echo "  Scan the test coverage for a specific rule module."
	echo ""
	echo "Flags:"
	echo "  -p,--prefix <prefix>        Specify the test function name prefix to use i.e. 'test_md001_'."
	echo "  -s,--source <module>        Module name of the rule's soruce, without extension i.e. 'rule_md_001'."
	echo "  -t,--test-report <file>     File name of the XML test report to use. Default is 'report/tests.xml'."
	echo "  -c,--coverage-report <file> File name of the XML coverage report to use. Default is 'report/coverage.xml'."
	echo "  -x,--debug                  Display debug information about the script as it executes."
	echo "  -h,--help                   Display this help text."
	echo ""
	exit 1
}

# Parse the command line.
parse_command_line() {

	DEBUG_MODE=0
	RULE_TEST_FUNCTION_NAME_PREFIX=""
	SOURCE_CLASS_MODULE_NAME=""
	TEST_REPORT_XML_PATH="report/tests.xml"
	TEST_COVERAGE_XML_PATH="report/coverage.xml"
	while (("$#")); do
		case "${1}" in
		-p | --prefix)
			if [[ -z ${2:-} ]]; then
				echo "Error: Argument ${1} must be followed by rule prefix." >&2
				show_usage
			fi
			RULE_TEST_FUNCTION_NAME_PREFIX="${2}"
			shift 2
			;;
		-s | --source)
			if [[ -z ${2:-} ]]; then
				echo "Error: Argument ${1} must be followed by the local name of the rule's source module." >&2
				show_usage
			fi
			SOURCE_CLASS_MODULE_NAME="${2}"
			shift 2
			;;
		-t | --test-report)
			if [[ -z ${2:-} ]]; then
				echo "Error: Argument ${1} must be followed by the path to the previously generated xml test file." >&2
				show_usage
			fi
			TEST_REPORT_XML_PATH="${2}"
			shift 2
			;;
		-c | --coverage-report)
			if [[ -z ${2:-} ]]; then
				echo "Error: Argument ${1} must be followed by the path to the previously generated xml coverage file." >&2
				show_usage
			fi
			TEST_COVERAGE_XML_PATH="${2}"
			shift 2
			;;
		-x | --debug)
			DEBUG_MODE=1
			shift
			;;
		-h | --help)
			show_usage
			;;
		-*) # unsupported flags
			echo "Error: Unsupported flag '${1}'." >&2
			show_usage
			;;
		*) # preserve positional arguments
			echo "Error: Unsupported positional argument '${1}'." >&2
			show_usage
			;;
		esac
	done

	if [[ ${DEBUG_MODE} -ne 0 ]]; then
		set -x
	fi

	if [[ -z ${RULE_TEST_FUNCTION_NAME_PREFIX} ]]; then
		echo "Error: Test function name prefix must be specified."
		show_usage
	fi

	if [[ -z ${TEST_REPORT_XML_PATH} ]]; then
		echo "Error: Test report XML file '${TEST_REPORT_XML_PATH}' must be specified."
		show_usage
	fi

	if [[ -z ${TEST_COVERAGE_XML_PATH} ]]; then
		echo "Error: Coverage report XML file '${TEST_COVERAGE_XML_PATH}' must be specified."
		show_usage
	fi
}

# Start the processing for the script.
setup_function
trap cleanup_function EXIT

# Parse any command line values.
parse_command_line "$@"

if [[ -f ${TEST_COVERAGE_XML_PATH} ]]; then
	echo "Removing old coverage report file..."
	if ! rm "${TEST_COVERAGE_XML_PATH}" >"${TEMP_FILE}" 2>&1; then
		cat "${TEMP_FILE}"
		echo "Failed to remove old coverage report file."
		exit 1
	fi
fi

echo "Generating specific coverage report file for rule module ${SOURCE_CLASS_MODULE_NAME}..."
export PYTEST_ANNOTATE_USER_PROPERTIES=1
# shellcheck disable=SC2086  # Double quote to prevent splitting and globbing.
if ! ./ptest.sh --full-report --coverage --keyword ${RULE_TEST_FUNCTION_NAME_PREFIX} >"${TEMP_FILE}" 2>&1; then
	cat "${TEMP_FILE}"
	echo "Specific coverage report was not generated."
	exit 1
fi

echo "Verifying required coverage for rule module ${SOURCE_CLASS_MODULE_NAME}..."
if ! pipenv run python utils/verify_rule_coverage.py "${SOURCE_CLASS_MODULE_NAME}" "${TEST_COVERAGE_XML_PATH}" >"${TEMP_FILE}" 2>&1; then
	cat "${TEMP_FILE}"
	echo "Required coverage was not met."
	exit 1
fi

echo "Rerunning specific tests for rule module ${SOURCE_CLASS_MODULE_NAME} to analyze coverage..."
if ! pipenv run python utils/scan_for_extra_code_coverage.py --test-report "${TEST_REPORT_XML_PATH}" -- -k "${RULE_TEST_FUNCTION_NAME_PREFIX}"; then
	echo "Rerun of specific tests failed."
	exit 1
fi

exit 0
