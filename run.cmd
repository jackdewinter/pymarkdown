pipenv run python main.py %1 %2 %3 %4 %5 %6 %7 %8 %9
set RETURN_CODE=%ERRORLEVEL%
echo !RETURN_CODE!
echo %RETURN_CODE%
exit /b %RETURN_CODE%