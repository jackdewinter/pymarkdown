#!/usr/bin/env bash

set -x

process_number() {
	local formatted_num
	formatted_num=$(printf "%03d" "${1}")

	df="pymarkdown/plugins/rule_md_${formatted_num}.py"
	if [ ! -f "${df}" ]; then
		echo "File ${df} does not exist. Skipping."
		return
	fi

	dd="--prefix test_md${formatted_num}_ --source rule_md_${formatted_num}"
	# shellcheck disable=SC2086  # Double quote to prevent splitting and globbing.
	if ! ./scan_rule_for_extra_code_coverage.sh ${dd} --test-report report/tests.xml --coverage-report report/coverage.xml; then

		echo "./scan_rule_for_extra_code_coverage.sh ${dd} --test-report report/tests.xml --coverage-report report/coverage.xml"
		echo "Rerun of specific tests failed."
		exit 1
	fi
}

# Define start and end values
start_md_test=1
end_md_test=4

# Validate that start <= end
if ((start_md_test > end_md_test)); then
	echo "Error: start (${start_md_test}) is greater than end (${end_md_test})." >&2
	exit 1
fi

for ((i = start_md_test; i <= end_md_test; i++)); do
	process_number "${i}"
done

exit 0
