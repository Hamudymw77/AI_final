@echo off
echo ===================================================
echo     Spoustim projekt: Rozpoznavac Ronalda (AI)
echo ===================================================

:: Chytry vyber Pythonu (hleda stabilni verzi, jinak vezme vychozi)
py -3.11 -V >nul 2>&1
if %errorlevel% equ 0 (
    set PYTHON_CMD=py -3.11
) else (
    set PYTHON_CMD=python
)

echo Vytvarim ciste virtualni prostredi...
if not exist venv (
    %PYTHON_CMD% -m venv venv
)

echo Instaluji knihovny (tohle ted potrva trochu dele, stahuje se AI)...
venv\Scripts\python.exe -m pip install -r requirements.txt

echo Nacitam umelou inteligenci do pameti...
start "" cmd /c "timeout /t 10 >nul && start http://127.0.0.1:5000"

echo Spoustim server!
venv\Scripts\python.exe app.py

pause