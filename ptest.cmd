@echo off
setlocal EnableDelayedExpansion
pushd %~dp0

set COVERAGE_FILE=build/.coverage

rem Set needed environment variables.
set PTEST_TEMPFILE=temp_ptest.txt
set PTEST_SCRIPT_DIRECTORY=%~dp0
set PTEST_PYSCAN_SCRIPT_PATH=%PTEST_SCRIPT_DIRECTORY%..\pyscan\pyscan\main.py
set PTEST_TEST_RESULTS_PATH=report\tests.xml
set PTEST_TEST_COVERAGE_PATH=report\coverage.xml
set "PROJECT_DIRECTORY=%cd%"
set PYTHONPATH=%PROJECT_DIRECTORY%

rem Look for options on the command line.
set PTEST_PUBLISH_SUMMARIES=
set PTEST_FULL_REPORT=
set PTEST_QUIET_MODE=
set PTEST_COVERAGE_MODE=
:process_arguments
if "%1" == "-h" (
    echo Command: %0 [options]
    echo   Usage:
    echo     - Execute the tests for this project.
    echo   Options:
    echo     -h                This message.
    echo     -q                Quiet mode.
    echo     -c                Calculate the coverage for the tests.
	echo     -f                Produce a full report for the tests instead of a 'changes only' report.
	echo     -p                Publish project summaries instead of running tests.
	echo     -k [keyword]      Execute only the tests matching the specified keyword.
    GOTO real_end
) else if "%1" == "-p" (
	set PTEST_PUBLISH_SUMMARIES=1
) else if "%1" == "-f" (
	set PTEST_FULL_REPORT=1
) else if "%1" == "-q" (
	set PTEST_QUIET_MODE=1
) else if "%1" == "-c" (
	set PTEST_COVERAGE_MODE=1
) else if "%1" == "-k" (
	set PTEST_KEYWORD=%2
	if not defined PTEST_KEYWORD (
		echo Option -k requires a keyword argument to follow it.
		goto error_end
	)
	shift
) else if "%1" == "" (
    goto after_process_arguments
) else (
    echo Argument '%1' not understood.  Stopping.
	echo Type '%0 -h' to see valid arguments.
    goto error_end
)
shift
goto process_arguments
:after_process_arguments

if defined PTEST_PUBLISH_SUMMARIES (
	goto publish_start
)
if defined PTEST_KEYWORD (
	set PTEST_COVERAGE_MODE=
)

set PTEST_PYSCAN_OPTIONS=
if not defined PTEST_FULL_REPORT (
	set PTEST_PYSCAN_OPTIONS=--only-changes
)

if defined PTEST_KEYWORD (
	set PTEST_KEYWORD=-k %PTEST_KEYWORD%
)

rem Enter main part of script.
if defined PTEST_KEYWORD (
	echo {Executing partial test suite...}
	set PYTEST_ARGS=
) else (
	if defined PTEST_COVERAGE_MODE (
		echo {Executing full test suite with coverage...}
		set PYTEST_ARGS=--cov-fail-under=90 --cov --cov-branch --cov-report xml:report/coverage.xml --cov-report html:report/coverage 
	) else (
		echo {Executing full test suite...}
	)
)
set TEST_EXECUTION_FAILED=
if not defined PTEST_QUIET_MODE (
	pipenv run pytest %PYTEST_ARGS% %PTEST_KEYWORD%
	if ERRORLEVEL 1 (
		echo.
		echo {Executing test suite failed.}
		set TEST_EXECUTION_FAILED=1
	)
) else (
	pipenv run pytest %PYTEST_ARGS% %PTEST_KEYWORD% > %PTEST_TEMPFILE% 2>&1
	if ERRORLEVEL 1 (
		type %PTEST_TEMPFILE%
		echo.
		echo {Executing test suite failed.}
		set TEST_EXECUTION_FAILED=1
	)
)

if defined PTEST_KEYWORD (
	echo {Execution of partial test suite succeeded.}
	goto success_end
)

set PTEST_REPORT_OPTIONS=--junit %PTEST_TEST_RESULTS_PATH%
if defined PTEST_COVERAGE_MODE (
	if not defined TEST_EXECUTION_FAILED (
		set PTEST_REPORT_OPTIONS=%PTEST_REPORT_OPTIONS% --cobertura=%PTEST_TEST_COVERAGE_PATH%
	)
)

echo {Summarizing changes in execution of full test suite.}
pipenv run python %PTEST_PYSCAN_SCRIPT_PATH% %PTEST_PYSCAN_OPTIONS% %PTEST_REPORT_OPTIONS%
if ERRORLEVEL 1 (
	echo.
	echo {Summarizing changes in execution of full test suite failed.}
	goto error_end
)

if defined TEST_EXECUTION_FAILED (
	goto error_end
)

echo {Execution of full test suite succeeded.}
goto success_end

:publish_start
echo {Publishing summaries from last test runs.}
pipenv run python %PTEST_PYSCAN_SCRIPT_PATH% --publish
if ERRORLEVEL 1 (
	echo.
	echo {Publishing summaries from last test runs failed.}
	goto error_end
)
echo {Publishing summaries from last test runs succeeded.}

:success_end
rem Exit main part of script.
echo.
set PC_EXIT_CODE=0
goto real_end

:error_end
set PC_EXIT_CODE=1
if not defined PTEST_PUBLISH_SUMMARIES (
	echo {Execution of full test suite failed.}
)

:real_end
erase /f /q %PTEST_TEMPFILE% > nul 2>&1
popd
exit /B %PC_EXIT_CODE%