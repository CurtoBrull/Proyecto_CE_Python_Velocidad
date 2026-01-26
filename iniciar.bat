@echo off
title Radar Velocidad - Servidores
color 0A
echo ========================================
echo   RADAR DE VELOCIDAD - OPTIMIZADO
echo ========================================
echo.

REM Detener procesos previos
echo [1/4] Deteniendo procesos anteriores...
taskkill /F /IM python.exe /T >nul 2>&1
timeout /t 2 /nobreak >nul

REM Optimizar base de datos
echo [2/4] Optimizando SQLite con WAL mode...
cd /d "%~dp0api"
python optimizar_sqlite.py
echo.

REM Iniciar FastAPI optimizado (sin uvloop en Windows)
echo [3/4] Iniciando FastAPI optimizado (puerto 8080)...
start "FastAPI-Radar" cmd /k "cd /d %~dp0api && uvicorn main:app --host 0.0.0.0 --port 8080 --http httptools --reload"
echo     Esperando inicio de FastAPI...
timeout /t 5 /nobreak >nul

REM Iniciar Django
echo [4/4] Iniciando Django (puerto 8000)...
start "Django-Frontend" cmd /k "cd /d %~dp0frontend && python manage.py runserver"
echo     Esperando inicio de Django...
timeout /t 3 /nobreak >nul

echo.
echo ========================================
echo   SERVIDORES ACTIVOS
echo ========================================
echo   FastAPI:  http://localhost:8080
echo   Django:   http://localhost:8000
echo   Docs:     http://localhost:8080/docs
echo ========================================
echo.
echo   Los servidores estan ejecutandose
echo   en ventanas separadas.
echo.
echo   Accede a: http://localhost:8000
echo.
echo   Presiona cualquier tecla para salir.
echo ========================================
echo.
pause >nul
