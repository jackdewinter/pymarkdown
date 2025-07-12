@echo off
setlocal EnableDelayedExpansion
pushd %~dp0

rem Set needed environment variables.
set PROPERTIES_FILE=project.properties

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

if "%PYTHON_MODULE_NAME%" == "cookieslicer" (
	set PTEST_SLICER_SCRIPT_PATH="main.py"
) else (
	set PTEST_SLICER_SCRIPT_PATH="cookieslicer"
)

rem Look for options on the command line.
set PTEST_VERBOSE_MODE=
set PTEST_FORCE_MODE=
set PTEST_LIST_MODE=
set PTEST_GENERATE_MODE=
:process_arguments
if "%1" == "-h" (
    echo Command: %0 [options]
    echo   Usage:
    echo     - Reapply the templating if required.
    echo   Options:
    echo     -h                This message.
    echo     -v                Verbose mode.
    echo     -g                Generate default configuration file.
    echo     -l                List mode.
	echo     -f				   Force the template to be re-applied, even if synced.
    GOTO real_end
) else if "%1" == "-v" (
	set PTEST_VERBOSE_MODE=1
) else if "%1" == "-f" (
	set PTEST_FORCE_MODE=-f
) else if "%1" == "-l" (
	set PTEST_LIST_MODE=--list
) else if "%1" == "-g" (
	set PTEST_GENERATE_MODE=--generate-config
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

rem ADD WARNING TO MAKE SURE ALL FILES COMMITTTED BEFORE, ASK FOR YES, EXPLAIN WHY

rem Capture the Hashes for the two Pipfiles before any changes.
@For /F Delims^= %%G In ('""%__AppDir__%certutil.exe" -HashFile "Pipfile"|"%__AppDir__%find.exe" /V ":""')Do @Set "PIPFILE_SHA1=%%G"

if defined PTEST_VERBOSE_MODE (
    echo {Applying re-template operation to project.}
)

echo {Applying template.}
pipenv run "%PTEST_SLICER_SCRIPT_PATH%" --output-directory . --source-directory c:\enlistments\template\applications %PTEST_LIST_MODE% %PTEST_FORCE_MODE% %PTEST_GENERATE_MODE% --project-name %PYTHON_MODULE_NAME%
if ERRORLEVEL 1 (
	echo.
	echo {Applying template to existing directory failed.}
	goto error_end
)

rem Capture the Hashes for the two Pipfiles after any changes.
@For /F Delims^= %%G In ('""%__AppDir__%certutil.exe" -HashFile "Pipfile"|"%__AppDir__%find.exe" /V ":""')Do @Set "NEW_PIPFILE_SHA1=%%G"

if defined PTEST_VERBOSE_MODE (
    echo {PipFile hash before !PIPFILE_SHA1! and after !NEW_PIPFILE_SHA1!.}
)
if not [!PIPFILE_SHA1!] == [!NEW_PIPFILE_SHA1!] (
    goto need_sync
)

if defined PTEST_VERBOSE_MODE (
    echo {Pipfile hash has not changed.  Recreation and resync of packages not required.}
)
goto success_end

:need_sync
echo {Pipfile hashes have changed.  Recreation and resync of packages required.}
echo {Please exit any open instances of VSCode before pressing a key.}
echo {Failure to exit any such Python instances will cause the recreate and resync to fail.}
timeout /t -1

if defined PTEST_VERBOSE_MODE (
	echo {Clearing old lock file and virtual environment.}
)
erase Pipfile.lock
pipenv --rm

if defined PTEST_VERBOSE_MODE (
	echo {Creating new lock file and virtual environment.}
)
pipenv lock
pipenv sync -d

if defined PTEST_VERBOSE_MODE (
	echo {Restarting VSCode.}
)
code c:\enlistments\%PYTHON_MODULE_NAME%

:success_end
rem Exit main part of script.
@REM echo.
set PC_EXIT_CODE=0
goto real_end

:error_end
set PC_EXIT_CODE=1
if not defined PTEST_PUBLISH_SUMMARIES (
	echo {Execution of re-template operation failed.}
)

:real_end
erase /f /q %PTEST_TEMPFILE% > nul 2>&1
popd
exit /B %PC_EXIT_CODE%
