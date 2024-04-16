@echo off
setlocal EnableDelayedExpansion
pushd %~dp0

rem Set needed environment variables.
set SCAN_DOCS_SCRIPT_DIRECTORY=%~dp0

rem Look for options on the command line.

set MY_VERBOSE=
:process_arguments
if "%1" == "-h" (
    echo Command: %0 [options]
    echo   Usage:
    echo     - Scan the help documentation for the project.
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
echo {Scanning the documentation directory for warnings.}

rem Cleanly start the main part of the script

cd %SCAN_DOCS_SCRIPT_DIRECTORY%\newdocs
if defined MY_VERBOSE (
    echo {Scanning the documentation using PyMarkdown.}
)
pipenv run python ..\main.py -d Md030 -e pml101 --set "plugins.line-length.code_block_line_length=$#160" --set "extensions.linter-pragmas.enabled=true" scan src
if ERRORLEVEL 1 (
	echo.
	echo {Scanning the documentation using PyMarkdown failed.}
	goto error_end
)

@REM if defined MY_VERBOSE (
@REM     echo {Reformatting the documentation using MdFormat.}
@REM )
@REM pipenv run mdformat --align-semantic-breaks-in-lists --end-of-line keep --wrap 80 .
@REM if ERRORLEVEL 1 (
@REM 	echo.
@REM 	echo {Reformatting the documentation using MdFormat failed.}
@REM 	goto error_end
@REM )

rem Cleanly exit the script

:good_end
echo.
set PC_EXIT_CODE=0
if defined MY_VERBOSE (
    echo {Scanning the documentation directory succeeded.}
)
goto real_end

:error_end
set PC_EXIT_CODE=1
echo {Scanning the documentation directory failed.}

:real_end
popd
exit /B %PC_EXIT_CODE%