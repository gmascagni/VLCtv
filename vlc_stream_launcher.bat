@echo off
set "SCRIPT_DIR=%~dp0"
set "PYTHONW=C:\Users\gmasc\AppData\Local\Programs\Python\Python312\pythonw.exe"

if exist "%PYTHONW%" (
    start "" "%PYTHONW%" "%SCRIPT_DIR%vlc_stream_launcher.py" "%*"
    goto :eof
)

where pythonw >nul 2>nul
if %errorlevel% equ 0 (
    start "" pythonw "%SCRIPT_DIR%vlc_stream_launcher.py" "%*"
    goto :eof
)

where python >nul 2>nul
if %errorlevel% equ 0 (
    start "" python "%SCRIPT_DIR%vlc_stream_launcher.py" "%*"
    goto :eof
)

:: Direct fallback
set "VLC=C:\Program Files\VideoLAN\VLC\vlc.exe"
if not exist "%VLC%" set "VLC=C:\Program Files (x86)\VideoLAN\VLC\vlc.exe"
start "" "%VLC%" --network-caching=1500 "%~1"
