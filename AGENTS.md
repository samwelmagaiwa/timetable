# Project Commands

## Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
# Install MySQL server and create database 'timetable'
python -m uvicorn app.main:app --reload  # Run backend
```

## Frontend Setup
```bash
cd frontend
npm install
ng serve  # Run frontend on http://localhost:4200
```

## Database Setup (MySQL)
```sql
CREATE DATABASE timetable;
CREATE USER 'user'@'localhost' IDENTIFIED BY 'password';
GRANT ALL PRIVILEGES ON timetable.* TO 'user'@'localhost';
FLUSH PRIVILEGES;
```

## Lint & Typecheck
```bash
cd backend
flake8 app/  # Lint Python code
mypy app/   # Type check (requires mypy: pip install mypy)
```

## Run Tests
```bash
cd backend
pytest tests/
```

## Deployment (Linux)
```bash
# Using systemd and Nginx
# See docker/docker-compose.yml for containerized deployment
```
