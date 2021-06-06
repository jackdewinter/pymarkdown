@echo off
setlocal EnableDelayedExpansion
pushd %~dp0

rem Set needed environment variables.

rem Look for options on the command line.

set TEST_BLOG_VERBOSE=
set TEST_BLOG_PROFILE=
:process_arguments
if "%1" == "-h" (
    echo Command: %0 [options]
    echo   Usage:
    echo     - Execute a clean build for this project.
    echo   Options:
    echo     -h                This message.
	echo     -v                Display verbose information.
	echo     -p                Gather profile information while scanning.
    GOTO real_end
) else if "%1" == "-v" (
	set TEST_BLOG_VERBOSE=--verbose
) else if "%1" == "-p" (
	set TEST_BLOG_PROFILE=1
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

rem Properly set any environment variables to good known values.

if defined TEST_BLOG_PROFILE (
	set TEST_BLOG_PROFILE=-m cProfile -o p0.prof
)

rem Announce what this script does.

if defined TEST_BLOG_VERBOSE (
	echo {Scanning blog contents started.}
)

rem Cleanly start the main part of the script

pipenv run python %TEST_BLOG_PROFILE% main.py --set extensions.front-matter.enabled=$^^!True --set plugins.md024.siblings_only=$^^!True scan -r C:\enlistments\blog-content\website\content\articles
if ERRORLEVEL 1 (
	goto error_end
)

rem Cleanly exit the script

set PC_EXIT_CODE=0
if defined TEST_BLOG_VERBOSE (
	echo.
	echo {Scanning of blog contents succeeded.}
)
goto real_end

:error_end
set PC_EXIT_CODE=1
echo.
echo {Scanning of blog contents failed.}

:real_end
rem erase /f /q %CLEAN_TEMPFILE% > nul 2>&1
popd
exit /B %PC_EXIT_CODE%