@echo off
title VLC 1-Click Protocol Setup
cls
echo ========================================================
echo       VLC 1-Click Browser Protocol Registration
echo ========================================================
echo.
echo This registers the "vlc://" protocol for your user account
echo so clicking "Open in VLC" in any browser opens VLC directly!
echo No administrator rights required.
echo.

set "SCRIPT_DIR=%~dp0"
set "LAUNCHER=%SCRIPT_DIR%vlc_stream_launcher.bat"

if not exist "%LAUNCHER%" (
    echo Error: %LAUNCHER% not found!
    pause
    exit /b 1
)

:: Register in HKCU (Current User)
reg add "HKCU\Software\Classes\vlc" /ve /d "URL:VLC Protocol" /f >nul
reg add "HKCU\Software\Classes\vlc" /v "URL Protocol" /d "" /f >nul
reg add "HKCU\Software\Classes\vlc\shell\open\command" /ve /d "\"%LAUNCHER%\" \"%%1\"" /f >nul

if %errorlevel% equ 0 (
    echo [SUCCESS] The vlc:// protocol has been successfully registered!
    echo.
    echo Next time you click "Open in VLC" in Chrome, Edge, or Firefox,
    echo your browser will prompt you once:
    echo   "Always allow file:// to open links of this type"
    echo Check that box, and channels will open directly in VLC!
    echo.
) else (
    echo [ERROR] Failed to update registry.
)

echo Press any key to exit...
pause >nul
