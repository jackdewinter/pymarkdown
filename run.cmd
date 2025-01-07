@ echo off

@REM If we are doing a performance run, make sure to use optimized python.
set PYTHON_PERFORMANCE_ARGUMENTS=
if "%PYMARKDOWNLINT__PERFRUN%" == "1" (
    set PYTHON_PERFORMANCE_ARGUMENTS=-OO
)

pipenv run python %PYTHON_PERFORMANCE_ARGUMENTS% main.py %1 %2 %3 %4 %5 %6 %7 %8 %9

set RETURN_CODE=%ERRORLEVEL%
exit /b %RETURN_CODE%