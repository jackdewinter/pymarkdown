@echo off
setlocal EnableDelayedExpansion
pushd %~dp0

rem Set needed environment variables.
set CLEAN_TEMPFILE=temp_clean.txt
set PYTHON_MODULE_NAME=pymarkdown
set "PROJECT_DIRECTORY=%cd%"
set PYTHONPATH=%PROJECT_DIRECTORY%

rem Look for options on the command line.

set MY_VERBOSE=
set MY_PUBLISH=
:process_arguments
if "%1" == "-h" (
    echo Command: %0 [options]
    echo   Usage:
    echo     - Execute a clean build for this project.
    echo   Options:
    echo     -h                This message.
	echo     -v                Display verbose information.
	echo     -p				   Publish project summaries if successful.
    GOTO real_end
) else if "%1" == "-v" (
	set MY_VERBOSE=--verbose
) else if "%1" == "-p" (
	set MY_PUBLISH=1
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

echo {Analysis of project started.}

echo {Executing black formatter on Python code.}
pipenv run black %MY_VERBOSE% .
if ERRORLEVEL 1 (
	echo.
	echo {Executing black formatter on Python code failed.}
	goto error_end
)

echo {Executing import sorter on Python code.}
pipenv run isort %MY_VERBOSE% .
if ERRORLEVEL 1 (
	echo.
	echo {Executing import sorter on Python code failed.}
	goto error_end
)

echo {Executing flake8 static analyzer on Python code.}
pipenv run flake8 %MY_VERBOSE%
if ERRORLEVEL 1 (
	echo.
	echo {Executing static analyzer on Python code failed.}
	goto error_end
)

echo {Executing pylint static analyzer on source Python code.}
pipenv run pylint -j 1 --rcfile=setup.cfg %PYTHON_MODULE_NAME% %MY_VERBOSE%
if ERRORLEVEL 1 (
	echo.
	echo {Executing pylint static analyzer on source Python code failed.}
	goto error_end
)

echo {Executing pylint static analyzer on test Python code.}
pipenv run pylint -j 1 --rcfile=setup.cfg test %MY_VERBOSE%
if ERRORLEVEL 1 (
	echo.
	echo {Executing pylint static analyzer on test Python code failed.}
	goto error_end
)

echo {Executing unit tests on Python code.}
call ptest.cmd
if ERRORLEVEL 1 (
	echo.
	echo {Executing unit tests on Python code failed.}
	goto error_end
)

if defined MY_PUBLISH (
	echo {Publishing summaries after successful analysis of project.}
	call ptest.cmd -p
	if ERRORLEVEL 1 (
		echo.
		echo {Publishing summaries failed.}
		goto error_end
	)
)

echo.
set PC_EXIT_CODE=0
echo {Analysis of project succeeded.}
goto real_end

:error_end
set PC_EXIT_CODE=1
echo {Analysis of project failed.}

:real_end
erase /f /q %CLEAN_TEMPFILE% > nul 2>&1
set CLEAN_TEMPFILE=
popd
exit /B %PC_EXIT_CODE%