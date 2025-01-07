@echo off
setlocal EnableDelayedExpansion
pushd %~dp0

rem Set needed environment variables.
set PBOY_TEMPFILE=%TEMP%\temp_pboy_%RANDOM%.txt

rem Look for options on the command line.

set VIEW_MODE=
set NUM_MINIMUM=1
set NUM_MAXIMUM=2
set NUM_COUNT=1
set ALTERNATE_REPEAT_LIST=
set WAS_0=%0
set NO_RULES_MODE=
set TEST_SERIES_TAG=
:process_arguments
if "%1" == "-h" (
    echo Command: %WAS_0% [options]
    echo   Usage:
    echo     - Execute a clean build for this project.
    echo   Options:
    echo     -h                This message.
    echo     -s                Repeat count to start at.
    echo     -e                Repeat count to end at.
    echo     -l                List of _ separated repeat counts to use instead of -s and -e.
    echo     -c                Count of times for each series of repeats.
    echo     -t                Tag to associate with this series of tests.
    echo     -nr               Take measurements without processing any rules {Parser only.}
    echo.
    echo   Example:
    echo     To run a series of tests, from 10 to 15 repeats:
    echo       %WAS_0% -s 10 -e 15
    echo     To run a series of tests, from 10 to 15 repeats, twice:
    echo       %WAS_0% -s 10 -e 15 -c 2
    echo     To run a series of tests, only 10 and 15 repeats, twice:
    echo       %WAS_0% -l 10_15 -c 2
    GOTO real_end
) else if "%1" == "-t" (
	set TEST_SERIES_TAG=%2
	if not defined TEST_SERIES_TAG (
		echo Option -t requires a alphabetic argument to follow it.
		goto error_end
	)
	shift
) else if "%1" == "-s" (
	set NUM_MINIMUM=%2
	if not defined NUM_MINIMUM (
		echo Option -s requires a positive integer argument to follow it.
		goto error_end
	)
	shift
) else if "%1" == "-e" (
	set NUM_MAXIMUM=%2
	if not defined NUM_MAXIMUM (
		echo Option -e requires a positive integer argument to follow it.
		goto error_end
	)
	shift
) else if "%1" == "-c" (
	set NUM_COUNT=%2
	if not defined NUM_COUNT (
		echo Option -c requires a positive integer argument to follow it.
		goto error_end
	)
	shift
) else if "%1" == "-l" (
	set ALTERNATE_REPEAT_LIST=%2
	if not defined ALTERNATE_REPEAT_LIST (
		echo Option -l requires a underscore separated list of repeat counts to follow it.
		goto error_end
	)
	shift
) else if "%1" == "-nr" (
	set NO_RULES_MODE=1
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

if defined TEST_SERIES_TAG (
    SET "var="&for /f "delims=abcdefghijklmnopqrstuvwxyz" %%i in ("%TEST_SERIES_TAG%") do set var=%%i
    if defined var (
        echo Option -t is followed by '%TEST_SERIES_TAG%' which is not an alphabetic tag.
        goto error_end
    )
)

SET "var="&for /f "delims=0123456789" %%i in ("%NUM_MINIMUM%") do set var=%%i
if defined var (
    echo Option -s is followed by '%NUM_MINIMUM%' which is not an integer.
    goto error_end
)

if %NUM_MINIMUM% lss 1 (
    echo Option -s is followed by '%NUM_MINIMUM%' which is not a positive integer.
    goto error_end
)

SET "var="&for /f "delims=0123456789" %%i in ("%NUM_MAXIMUM%") do set var=%%i
if defined var (
    echo Option -e is followed by '%NUM_MAXIMUM%' which is not an integer.
    goto error_end
)

if %NUM_MAXIMUM% lss 1 (
    echo Option -e is followed by '%NUM_MAXIMUM%' which is not a positive integer.
    goto error_end
)

SET "var="&for /f "delims=0123456789" %%i in ("%NUM_COUNT%") do set var=%%i
if defined var (
    echo Option -c is followed by '%NUM_COUNT%' which is not an integer.
    goto error_end
)

if %NUM_COUNT% lss 1 (
    echo Option -c is followed by '%NUM_COUNT%' which is not a positive integer.
    goto error_end
)

@REM echo on
if not defined ALTERNATE_REPEAT_LIST goto no_alternate_repeat_list
set WHATS_LEFT_OF_ALTERNATE_REPEAT_LIST=%ALTERNATE_REPEAT_LIST%
:grab_next_count_test
for /f "tokens=1,* delims=_" %%a in ("%WHATS_LEFT_OF_ALTERNATE_REPEAT_LIST%") do (
    set NEXT_ITEM=%%a
    set WHATS_LEFT_OF_ALTERNATE_REPEAT_LIST=%%b

    SET "var="&for /f "delims=0123456789" %%i in ("!NEXT_ITEM!") do set var=%%i
    if defined var (
        echo Option -l has an element '!NEXT_ITEM!' which is not an integer.
        goto error_end
    )

    if !NEXT_ITEM! lss 1 (
        echo Option -c has an element '!NEXT_ITEM!' which is not a positive integer.
        goto error_end
    )
)
if "%WHATS_LEFT_OF_ALTERNATE_REPEAT_LIST%" neq "" goto grab_next_count_test
:no_alternate_repeat_list

rem Announce what this script does.
echo {Batch profiling of project started.}

if defined TEST_SERIES_TAG (
    set DEST_FILE=build\series-%TEST_SERIES_TAG%.csv
) else (
    set DEST_FILE=build\series.csv
)

set PERF_SAMPLE_OPTIONS=
if defined NO_RULES_MODE (
    set PERF_SAMPLE_OPTIONS=-nr
)

erase /f /q %DEST_FILE% > nul 2>&1

set PASS_NUMBER=1
:skip_to_next_pass

if not defined ALTERNATE_REPEAT_LIST goto exec_by_repeat_count

set WHATS_LEFT_OF_ALTERNATE_REPEAT_LIST=%ALTERNATE_REPEAT_LIST%
:grab_next_count
for /f "tokens=1,* delims=_" %%a in ("%WHATS_LEFT_OF_ALTERNATE_REPEAT_LIST%") do (
    set WHATS_LEFT_OF_ALTERNATE_REPEAT_LIST=%%b

    echo Sample Pass %PASS_NUMBER%, Repititions Count %%a
    call perf_sample.cmd -r %%a %PERF_SAMPLE_OPTIONS% -c %DEST_FILE% > %PBOY_TEMPFILE%
    if ERRORLEVEL 1 (
        type %PBOY_TEMPFILE%
        echo.
        echo {Executing profile run failed.}
        goto error_end
    )

)
if "%WHATS_LEFT_OF_ALTERNATE_REPEAT_LIST%" neq "" goto grab_next_count
goto pass_completed

:exec_by_repeat_count
set REPEAT_COUNT=%NUM_MINIMUM%

:skip_to_next_repeat_count
call perf_sample.cmd -r %REPEAT_COUNT% %XXXXXXX% -c fred.csv > %PBOY_TEMPFILE%
if ERRORLEVEL 1 (
    type %PBOY_TEMPFILE%
    echo.
    echo {Executing profile run failed.}
    goto error_end
)

set /a REPEAT_COUNT +=1
if %REPEAT_COUNT% leq %NUM_MAXIMUM% (
    goto skip_to_next_repeat_count
)

:pass_completed
set /a PASS_NUMBER +=1
if %PASS_NUMBER% leq %NUM_COUNT% (
    goto skip_to_next_pass
)

rem Cleanly exit the script
:good_end

echo.
set PC_EXIT_CODE=0
echo {Batch profiling of project succeeded.}
echo CSV file '%DEST_FILE%' written with sample timings.
goto real_end

:error_end
set PC_EXIT_CODE=1
echo {Batch profiling of project failed.}

:real_end
erase /f /q %PBOY_TEMPFILE% > nul 2>&1
set PBOY_TEMPFILE=
popd
exit /B %PC_EXIT_CODE%
