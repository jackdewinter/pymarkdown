@echo off
setlocal EnableDelayedExpansion
pushd %~dp0

rem Set needed environment variables.
set CLEAN_TEMPFILE=temp_clean.txt

rem Look for options on the command line.

rem set MY_VERBOSE=--verbose
set MY_VERBOSE=

echo Analysis of project started.

echo Executing black formatter on Python code.
pipenv run black %MY_VERBOSE% .
if ERRORLEVEL 1 (
	echo.
	echo Executing black formatter on Python code failed.
	goto error_end
)

echo Executing import sorter on Python code.
pipenv run isort %MY_VERBOSE% --apply
if ERRORLEVEL 1 (
	echo.
	echo Executing import sorter on Python code failed.
	goto error_end
)

echo Executing flake8 static analyzer on Python code.
pipenv run flake8 %MY_VERBOSE%
if ERRORLEVEL 1 (
	echo.
	echo Executing static analyzer on Python code failed.
	goto error_end
)

echo Executing pylint static analyzer on source Python code.
pipenv run pylint --rcfile=setup.cfg pymarkdown %MY_VERBOSE%
if ERRORLEVEL 1 (
	echo.
	echo Executing pylint static analyzer on source Python code failed.
	goto error_end
)

echo Executing pylint static analyzer on test Python code.
pipenv run pylint --rcfile=setup.cfg test %MY_VERBOSE%
if ERRORLEVEL 1 (
	echo.
	echo Executing pylint static analyzer on test Python code failed.
	goto error_end
)

echo Executing unit tests on Python code.
set COVERAGE_FILE=build/.coverage
pipenv run pytest
if ERRORLEVEL 1 (
	echo.
	echo Executing unit tests on Python code failed.
	goto error_end
)

echo.
set PC_EXIT_CODE=0
echo Analysis of project succeeded.
goto real_end

:error_end
set PC_EXIT_CODE=1
echo Analysis of project failed.

:real_end
erase /f /q %CLEAN_TEMPFILE%
set CLEAN_TEMPFILE=
popd
exit /B %PC_EXIT_CODE%