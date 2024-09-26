@ECHO OFF

pushd %~dp0

REM Command file for ALogAnalyze

if "%1" == ""         goto all
if "%1" == "all"      goto all
if "%1" == "qt"       goto qt

echo.
echo.usage:
echo.	make
echo.	make all
echo.	make qt
echo.

goto end

:all
python3 main.py
goto end

:qt
python3 main.py qt
goto end

:end
popd
