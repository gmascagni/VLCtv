@echo off
echo Launching Adult Channels in VLC Media Player...
set "VLC=C:\Program Files\VideoLAN\VLC\vlc.exe"
if not exist "%VLC%" set "VLC=C:\Program Files (x86)\VideoLAN\VLC\vlc.exe"
if not exist "%VLC%" (
    start "" "%~dp0Adult_XXX_Channels.m3u8"
) else (
    start "" "%VLC%" "%~dp0Adult_XXX_Channels.m3u8"
)
