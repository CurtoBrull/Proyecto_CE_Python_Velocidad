Start-Process powershell -ArgumentList "-Command", "uvicorn main:app --reload --port 8080"
Start-Process powershell -ArgumentList "-Command", "cd frontend; python manage.py runserver 8000"