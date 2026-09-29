@echo off
title Ollama Sunucusu
echo ========================================================
echo           Ollama Yerel Yapay Zeka Motoru
echo ========================================================

tasklist /FI "IMAGENAME eq ollama.exe" 2>NUL | find /I /N "ollama.exe">NUL
if "%ERRORLEVEL%"=="0" (
    echo [Ollama] Motor zaten arka planda calisiyor!
) else (
    echo [Ollama] Motor baslatiliyor...
    start "" "C:\Users\taycore\AppData\Local\Programs\Ollama\ollama.exe" serve
    echo [Ollama] Baslatildi! Modeller hazir.
)

timeout /t 3 >nul
