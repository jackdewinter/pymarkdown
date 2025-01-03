@echo off
setlocal EnableDelayedExpansion
pushd %~dp0

rem Set needed environment variables.
set PLONG_TEMPFILE=%TEMP%\temp_plong_%RANDOM%.txt
set TEST_FILE_DIRECTORY=build\ptest
set PERF_OUTPUT=%TEMP%\temp_pout_%RANDOM%.txt

rem Look for options on the command line.

set VIEW_MODE=
set NUM_REPEATS=10
set CSV_OUTPUT=
set NO_RULES_MODE=
:process_arguments
if "%1" == "-h" (
    echo Command: %0 [options]
    echo   Usage:
    echo     - Execute a clean build for this project.
    echo   Options:
    echo     -h                This message.
    echo     -c {file}         Append results to file in CSV format.
    echo     -r {num}          Number of repititions of the test document to merge together as a positive integer.
    echo     -nr               Take measurements without processing any rules.
	echo     -v                View the measured performance metrics.
    GOTO real_end
) else if "%1" == "-v" (
	set VIEW_MODE=1
) else if "%1" == "-nr" (
	set NO_RULES_MODE=1
) else if "%1" == "-r" (
	set NUM_REPEATS=%2
	if not defined NUM_REPEATS (
		echo Option -r requires a positive integer argument to follow it.
		goto error_end
	)
	shift
) else if "%1" == "-c" (
	set CSV_OUTPUT=%2
	if not defined CSV_OUTPUT (
		echo Option -c requires a filename argument to follow it.
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

SET "var="&for /f "delims=0123456789" %%i in ("%NUM_REPEATS%") do set var=%%i
if defined var (
    echo Option -r is followed by '%NUM_REPEATS%' which is not an integer.
    goto error_end
)

if %NUM_REPEATS% lss 1 (
    echo Option -r is followed by '%NUM_REPEATS%' which is not a positive integer.
    goto error_end
)

set SINGLE_TEST_SOURCE_FILE=test\resources\performance\sample.md
set SINGLE_TEST_DESTINATION_FILE=%TEST_FILE_DIRECTORY%\test.md

rem Announce what this script does.
echo {Profiling of project started.}

rem Make sure we have a directory to create the test files for profiling in.
if not exist "%TEST_FILE_DIRECTORY%" (
    mkdir "%TEST_FILE_DIRECTORY%" > %PLONG_TEMPFILE% 2>&1 
    if ERRORLEVEL 1 (
        type %PLONG_TEMPFILE%
        echo.
        echo {Creating test directory failed.}
        goto error_end
    )
)

rem Erase all existing contents of the profiling test directory.
erase /s /q %TEST_FILE_DIRECTORY%\* > %PLONG_TEMPFILE% 2>&1 
if ERRORLEVEL 1 (
    type %PLONG_TEMPFILE%
    echo.
    echo {Removing files in test directory failed.}
    goto error_end
)

rem Create a composite document with NUM_REPEATS copies of the source document. 
echo Creating single document with %NUM_REPEATS% copies of '%SINGLE_TEST_SOURCE_FILE%'.
FOR /L %%A IN (1,1,%NUM_REPEATS%) DO (
    type %SINGLE_TEST_SOURCE_FILE% >> %SINGLE_TEST_DESTINATION_FILE%
)

rem Remove any __pycache__ related files...
echo Resetting Python caches...
set PYTHONPYCACHEPREFIX=C:\enlistments\pymarkdown\.pycache
python3 -Bc "import pathlib; [p.unlink() for p in pathlib.Path('.').rglob('*.py[co]')]"
python3 -Bc "import pathlib; [p.rmdir() for p in pathlib.Path('.').rglob('__pycache__')]"

rem ... and then take the steps to properly create any needed caching.
python -m compileall pymarkdown > nul 2>&1
set SINGLE_TEST_SOURCE_FILE=%SINGLE_TEST_SOURCE_FILE:\=\\%
python -OO -c "import subprocess; subprocess.run(['run.cmd','scan','%SINGLE_TEST_SOURCE_FILE%'])" > %PERF_OUTPUT%

if defined NO_RULES_MODE (
    set "XNO_RULES_MODE='--disable-rules','*',"
)

echo Scanning created document...
set SINGLE_TEST_DESTINATION_FILE=%SINGLE_TEST_DESTINATION_FILE:\=\\%
python -OO -c "import subprocess,os,time; my_env = os.environ.copy(); my_env['PYMARKDOWNLINT__PERFRUN'] = '1'; start_time = time.time(); subprocess.run(['run.cmd',%XNO_RULES_MODE%'scan','%SINGLE_TEST_DESTINATION_FILE%'], env=my_env); print(time.time() - start_time)" > %PERF_OUTPUT%

echo Document scanning completed.

rem Calculate the statistics to report for this profiling run
type %PERF_OUTPUT% | find /c /v "" > %PLONG_TEMPFILE%
for /f "delims=" %%x in (%PLONG_TEMPFILE%) do set LINES_IN_PROF_OUTPUT=%%x
set OLD_LINES_IN_PROF_OUTPUT=%LINES_IN_PROF_OUTPUT%
set /a LINES_IN_PROF_OUTPUT -=1
more +%LINES_IN_PROF_OUTPUT% %PERF_OUTPUT% > %PLONG_TEMPFILE%
for /f "delims=" %%x in (%PLONG_TEMPFILE%) do set FRANK=%%x
if %LINES_IN_PROF_OUTPUT% LEQ 0 goto bob
set /a OLD_LINES_IN_PROF_OUTPUT -= 3
:bob

rem Generate the CSV output to append to the file, or just report the stats to the console.
if defined CSV_OUTPUT (
    echo %NUM_REPEATS%,%OLD_LINES_IN_PROF_OUTPUT%,%FRANK% >> !CSV_OUTPUT!
) else (
    echo Repeats in File: %NUM_REPEATS%
    echo Lines in output: %OLD_LINES_IN_PROF_OUTPUT%
    echo Execution time:  %FRANK%
)

rem If in view mode, use SnakeViz to visualize.
if defined VIEW_MODE (
    snakeviz p0.prof
)

rem Cleanly exit the script
:good_end

echo.
set PC_EXIT_CODE=0
echo {Profiling of project succeeded.}
goto real_end

:error_end
set PC_EXIT_CODE=1
echo {Profiling of project failed.}

:real_end
erase /f /q %PLONG_TEMPFILE% > nul 2>&1
erase /f /q %PERF_OUTPUT% > nul 2>&1
set PLONG_TEMPFILE=
popd
exit /B %PC_EXIT_CODE%
