@echo off
for /f "usebackq tokens=1,* delims==" %%A in (".env") do (
    set "value=%%B"
    call set %%A=%%value:"=%%
)
python -m bot
pause
