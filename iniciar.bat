@echo off
start cmd /k "cd api && uvicorn main:app --reload --port 8080"
timeout /t 3
start cmd /k "cd frontend && python manage.py runserver"
echo Servidores iniciados!
echo FastAPI: http://localhost:8080
echo Django: http://localhost:8000