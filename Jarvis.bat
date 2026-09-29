@echo off
title Jarvis Voice OS
echo ========================================================
echo          J.A.R.V.I.S. 100%% LOCAL VOICE OS
echo ========================================================

echo [1/2] Ollama yerel beyin kontrol ediliyor...
tasklist /FI "IMAGENAME eq ollama.exe" 2>NUL | find /I /N "ollama.exe">NUL
if "%ERRORLEVEL%"=="0" (
    echo [Ollama] Aktif.
) else (
    echo [Ollama] Baslatiliyor...
    start "" "C:\Users\taycore\AppData\Local\Programs\Ollama\ollama.exe" serve
    timeout /t 2 >nul
)

echo [2/2] AutoHotkey kisayol dinleyicisi kontrol ediliyor...
tasklist /FI "IMAGENAME eq AutoHotkey64.exe" 2>NUL | find /I /N "AutoHotkey64.exe">NUL
if "%ERRORLEVEL%"=="0" (
    echo [AHK] Aktif.
) else (
    echo [AHK] Kisayol baslatiliyor...
    start "" "C:\Projeler\HelperTools\Voice-OS\jarvis_hotkey.ahk"
)

echo.
echo [Jarvis] Voice OS calistiriliyor...
cd /d "C:\Projeler\HelperTools\Voice-OS"
python main.py
pause