@echo off
title Jarvis Kapat
echo ========================================================
echo          Jarvis ve Ollama Kapatiliyor...
echo ========================================================

taskkill /F /IM ollama.exe /T 2>nul
taskkill /F /IM ollama_llama_server.exe /T 2>nul

echo.
echo [Jarvis] Tum yapay zeka ve sunucu islemleri durduruldu.
echo [Bellek] RAM ve VRAM tamamen serbest birakildi!
timeout /t 3 >nul
