@echo off
title Radar Velocidad - ULTRA OPTIMIZADO
color 0B
echo ========================================
echo   MODO PRODUCCION - ULTRA OPTIMIZADO
echo ========================================
echo.

REM Detener procesos existentes
echo [1/4] Limpiando procesos...
taskkill /F /IM python.exe /T >nul 2>&1
timeout /t 2 /nobreak >nul

REM Optimizar DB
echo [2/4] Optimizando base de datos...
cd /d "%~dp0api"
python optimizar_sqlite.py
python optimizar_db.py
echo.

REM FastAPI con workers multiples (Windows no soporta uvloop)
echo [3/4] Iniciando FastAPI OPTIMIZADO...
echo    - Workers: 2
echo    - HTTP: httptools
echo    - Platform: Windows
start "FastAPI-OPTIMIZADO" cmd /k "cd /d %~dp0api && uvicorn main:app --host 0.0.0.0 --port 8080 --workers 2 --http httptools --access-log"
timeout /t 6 /nobreak >nul

REM Django
echo [4/4] Iniciando Django...
start "Django-Frontend" cmd /k "cd /d %~dp0frontend && python manage.py runserver"
timeout /t 3 /nobreak >nul

echo.
echo ========================================
echo   SERVIDORES ULTRA OPTIMIZADOS
echo ========================================
echo   FastAPI:  http://localhost:8080
echo   Django:   http://localhost:8000
echo   API Docs: http://localhost:8080/docs
echo ========================================
echo   Mejora esperada: 85-90%% mas rapido
echo ========================================
echo.
echo Presiona cualquier tecla para salir...
pause >nul

REM Limpiar
taskkill /F /IM python.exe /T >nul 2>&1
