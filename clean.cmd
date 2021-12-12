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

rem Announce what this script does.

echo {Analysis of project started.}

rem Cleanly start the main part of the script

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
pipenv run flake8 -j 4 --exclude dist,build %MY_VERBOSE%
if ERRORLEVEL 1 (
	echo.
	echo {Executing static analyzer on Python code failed.}
	goto error_end
)

echo {Executing pylint static analyzer on Python source code.}
pipenv run pylint -j 4 --rcfile=setup.cfg %MY_VERBOSE% %PYTHON_MODULE_NAME% %PYTHON_MODULE_NAME%/extensions %PYTHON_MODULE_NAME%/plugins
if ERRORLEVEL 1 (
	echo.
	echo {Executing pylint static analyzer on Python source code failed.}
	goto error_end
)

echo {Executing pylint utils analyzer on Python source code to verify suppressions and document them.}
pipenv run python ..\pylint_utils\main.py --config setup.cfg -r publish\pylint_suppression.json  pymarkdown
if ERRORLEVEL 1 (
	echo.
	echo {Executing reporting of pylint suppressions in Python source code failed.}
	goto error_end
)

git diff --name-only --staged > %CLEAN_TEMPFILE%
set ALL_FILES=
for /f "tokens=*" %%x in (%CLEAN_TEMPFILE%) do (
	set TEST_FILE=%%x
	if /i [!TEST_FILE:~-3!]==[.py] set ALL_FILES=!ALL_FILES! !TEST_FILE!
)
if "%ALL_FILES%" == "" (
	echo {Not executing pylint suppression checker on Python source code. No eligible Python files staged.}
) else (
	echo {Executing pylint suppression checker on Python source code.}
	pipenv run python ..\pylint_utils\main.py --config setup.cfg -s %ALL_FILES%
	if ERRORLEVEL 1 (
		echo.
		echo {Executing reporting of unused pylint suppressions in modified Python source code failed.}
		goto error_end
	)
)

echo {Executing pylint static analyzer on test Python code.}
pipenv run pylint -j 4 --rcfile=setup.cfg test %MY_VERBOSE%
if ERRORLEVEL 1 (
	echo.
	echo {Executing pylint static analyzer on test Python code failed.}
	goto error_end
)

echo {Executing PyMarkdown scan on Markdown documents.}
pipenv run python main.py --config clean.json scan . ./docs
if ERRORLEVEL 1 (
	echo.
	echo {PyMarkdown scan on Markdown documents failed.}
	goto error_end
)

echo {Executing unit tests on Python code.}
call ptest.cmd -c -m
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

rem Cleanly exit the script

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