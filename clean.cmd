@echo off
setlocal EnableDelayedExpansion
pushd %~dp0

rem Set needed environment variables.
set PROPERTIES_FILE=project.properties
set CLEAN_TEMPFILE=%TEMP%\temp_clean_%RANDOM%.txt

rem Read properties from the properties file and set in the current environment.
FOR /f %%N IN (%PROPERTIES_FILE%) DO (
	set TEST_LINE=%%N
	IF NOT "!TEST_LINE:~0,1!"=="#" (
		SET %%N
	)
)
if not defined PYTHON_MODULE_NAME (
	echo "Property 'PYTHON_MODULE_NAME' must be set in the %PROPERTIES_FILE% file."
	goto error_end
)

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

echo {Executing pre-commit hooks on Python code.}
pipenv run pre-commit run --all
if ERRORLEVEL 1 (
	echo.
	echo {Executing pre-commit hooks on Python code failed.}
	goto error_end
)

if "%SOURCERY_USER_KEY%" == "" (
	echo {Sourcery user key not defined.  Skipping Sourcery static analyzer.}
) else (
	echo {Executing Sourcery static analyzer on Python code.}
	pipenv run sourcery login --token %SOURCERY_USER_KEY%
	if ERRORLEVEL 1 (
		echo.
		echo {Logging into Sourcery failed.}
		goto error_end
	)
	
	if defined MY_PUBLISH (
		echo {  Executing Sourcery against full project contents.}
		set SOURCERY_LIMIT=
	) else (
		echo {  Executing Sourcery against changed project contents.}
		set "SOURCERY_LIMIT=--diff ^"git diff^""
	)

	pipenv run sourcery review --check pymarkdown !SOURCERY_LIMIT!
	if ERRORLEVEL 1 (
		echo.
		echo {Executing Sourcery on Python code failed.}
		goto error_end
	)
)

echo {Executing flake8 static analyzer on Python code.}
pipenv run flake8 -j 4 --exclude dist,build %MY_VERBOSE%
if ERRORLEVEL 1 (
	echo.
	echo {Executing static analyzer on Python code failed.}
	goto error_end
)

echo {Executing pylint static analyzer on Python source code.}
set TEST_EXECUTION_FAILED=
pipenv run pylint -j 1 --rcfile=setup.cfg --recursive=y %MY_VERBOSE% %PYTHON_MODULE_NAME%
if ERRORLEVEL 1 (
	echo.
	echo {Executing pylint static analyzer on Python source code failed.}
	goto error_end
)

echo {Executing mypy static analyzer on Python source code.}
pipenv run mypy --strict %PYTHON_MODULE_NAME% stubs
if ERRORLEVEL 1 (
	echo.
	echo {Executing mypy static analyzer on Python source code failed.}
	goto error_end
)
rem pipenv run stubgen --output stubs -p columnar
rem pipenv run stubgen --output stubs -p wcwidth

echo {Executing pylint utils analyzer on Python source code to verify suppressions and document them.}
pipenv run python ..\pylint_utils\main.py --config setup.cfg --recurse -r publish\pylint_suppression.json %PYTHON_MODULE_NAME%
if ERRORLEVEL 1 (
	echo.
	echo {Executing reporting of pylint suppressions in Python source code failed.}
	goto error_end
)

echo {Executing pylint static analyzer on test Python code.}
pipenv run pylint -j 1 --rcfile=setup.cfg --ignore test\resources --recursive=y %MY_VERBOSE% test
if ERRORLEVEL 1 (
	echo.
	echo {Executing pylint static analyzer on test Python code failed.}
	goto error_end
)	

git diff --name-only --staged > %CLEAN_TEMPFILE%
set ALL_FILES=
for /f "tokens=*" %%x in (%CLEAN_TEMPFILE%) do (
	set TEST_FILE=%%x
	if /i [!TEST_FILE:~-3!]==[.py] (
		if EXIST !TEST_FILE! (
			echo {Adding !TEST_FILE! to pylint suppression list.}
			set ALL_FILES=!ALL_FILES! !TEST_FILE!
		) else (
			echo {Skipping scan of !TEST_FILE! as it no longer exists.}
		)
	)
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