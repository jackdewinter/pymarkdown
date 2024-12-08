@echo off
setlocal EnableDelayedExpansion

rem Set needed environment variables.

:uniqLoop
set "XX_TEMPFILE=%tmp%\xx_~%RANDOM%.tmp"
if exist "%XX_TEMPFILE%" goto :uniqLoop

set disable_list="extensions.markdown-task-list-items.enabled=@True"
set disable_list=%disable_list%;"extensions.markdown-strikethrough.enabled=@True"
set disable_list=%disable_list%;"extensions.markdown-extended-autolinks.enabled=@True"
set disable_list=%disable_list%;"extensions.markdown-disallow-raw-html.enabled=@True"
set disable_list=%disable_list%;"extensions.front-matter.enabled=@True"

set filesCount=0 & for %%f in (ff\*) do @(set /a filesCount+=1 > nul)

set "bool_replace=$^!"
for %%a in (%disable_list%) do ( 
    set temp_path=%%a
    call set next_path=%%temp_path:@=!bool_replace!%%
    echo.
    echo Scanning with setting: !next_path!
    set /a count = 0
    for %%i in (ff\*) do (
        set file_to_scan=%%i
        set /a count += 1
        FOR /F "delims=" %%j IN ('python -c "print((!count! %% 10))"') DO set mcount=%%j
        if "!mcount!"=="0" (
            echo !count! out of %filesCount%
        )
        pipenv run python main.py --strict --set "!next_path!" --return-code-scheme minimal scan !file_to_scan! > %XX_TEMPFILE%
        if ERRORLEVEL 1 (
            type %XX_TEMPFILE%
            echo pipenv run python main.py --strict --set "!next_path!" --return-code-scheme minimal scan !file_to_scan!
            echo BADD !file_to_scan!
        )
    )
    echo !count! out of %filesCount%
)

set xx=
erase %XX_TEMPFILE%