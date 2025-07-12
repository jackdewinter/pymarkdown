#!/usr/bin/env bash

tests_to_execute="1,2,3,4,5,10,15,20,25,30,35,40,45,50,60,70,80,90,100"
# shorter list for now
tests_to_execute="1,2,3,4,5,10,15,20,25,30,35,40,45,50"
sample_size=5

verbose_echo ""
verbose_echo "{Executing performance tests on application with rules enabled.}"
rm -f "${SCRIPT_DIR}/build/series.csv" >/dev/null 2>&1
rm -f "${SCRIPT_DIR}/build/series.json" >/dev/null 2>&1
if ! ./perf_series.sh --count ${sample_size} --list ${tests_to_execute} --only-first; then
	complete_process 1 "{Executing of performance tests with rules enabled failed.}"
fi
if ! cp "${SCRIPT_DIR}/build/series.csv" "${SCRIPT_DIR}/publish/perf-with-rules.csv" >"${TEMP_FILE}" 2>&1; then
	complete_process 1 "{Publishing of performance test times with rules enabled failed.}"
fi
if ! cp "${SCRIPT_DIR}/build/series.json" "${SCRIPT_DIR}/publish/perf-with-rules.json" >"${TEMP_FILE}" 2>&1; then
	complete_process 1 "{Publishing of performance test profile with rules enabled failed.}"
fi
verbose_echo "{Results of performance tests on application with rules enabled have been published.}"

verbose_echo ""
verbose_echo "{Executing performance tests on application with rules disabled.}"
rm -f "${SCRIPT_DIR}/build/series.csv" >/dev/null 2>&1
rm -f "${SCRIPT_DIR}/build/series.json" >/dev/null 2>&1
if ! ./perf_series.sh --no-rules --count ${sample_size} --list ${tests_to_execute} --only-first; then
	complete_process 1 "{Executing of performance tests with rules disabled failed.}"
fi
if ! cp "${SCRIPT_DIR}/build/series.csv" "${SCRIPT_DIR}/publish/perf-without-rules.csv" >"${TEMP_FILE}" 2>&1; then
	complete_process 1 "{Publishing of performance test times with rules disabled failed.}"
fi
if ! cp "${SCRIPT_DIR}/build/series.json" "${SCRIPT_DIR}/publish/perf-without-rules.json" >"${TEMP_FILE}" 2>&1; then
	complete_process 1 "{Publishing of performance test profile with rules disabled failed.}"
fi
verbose_echo "{Results of performance tests on application with rules disabled have been published.}"
