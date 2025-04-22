@echo off
for /f "tokens=1,* delims==" %%A in (.env) do set %%A=%%B
python -m bot
pause
