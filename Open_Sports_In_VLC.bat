@echo off
echo Launching US Sports Channels in VLC Media Player...
set "VLC=C:\Program Files\VideoLAN\VLC\vlc.exe"
if not exist "%VLC%" set "VLC=C:\Program Files (x86)\VideoLAN\VLC\vlc.exe"
if not exist "%VLC%" (
    start "" "%~dp0US_Sports_Channels.m3u8"
) else (
    start "" "%VLC%" "%~dp0US_Sports_Channels.m3u8"
)
