@echo off
setlocal EnableDelayedExpansion
pushd %~dp0

rem Look for options on the command line.

set MY_VERBOSE=
:process_arguments
if "%1" == "-h" (
    echo Command: %0 [options]
    echo   Usage:
    echo     - Serve up the help documentation for the project for development.
    echo   Options:
    echo     -h                This message.
	echo     -v                Display verbose information.
    GOTO real_end
) else if "%1" == "-v" (
	set MY_VERBOSE=--verbose
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

rem Announce what this script does.

echo {Preparing to serve documentation for development purposes.}

rem Cleanly start the main part of the script

pipenv run mkdocs serve --config-file newdocs\mkdocs.yml %MY_VERBOSE%
if ERRORLEVEL 1 (
	echo.
	echo {Serving documentation for development failed.}
	goto error_end
)

rem Cleanly exit the script

:good_end
echo.
set PC_EXIT_CODE=0
echo {Serving documentation for development succeeded.}
goto real_end

:error_end
set PC_EXIT_CODE=1
echo {Serving documentation for development failed.}

:real_end
popd
exit /B %PC_EXIT_CODE%