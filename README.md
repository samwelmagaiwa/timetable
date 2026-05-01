# Timetable Scheduling System

Automated staff scheduling system built with Python + FastAPI (backend) and Angular (frontend).

## Project Structure

```
timetable/
├── backend/          # FastAPI backend
├── frontend/         # Angular frontend
├── docker/           # Docker configuration
├── docs/             # Documentation
└── README.md
```

## Technology Stack

- **Backend**: Python, FastAPI, MySQL
- **Frontend**: Angular
- **Deployment**: Docker, Nginx, systemd

## Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Setup MySQL database
mysql -u root -p
CREATE DATABASE timetable;
CREATE USER 'user'@'localhost' IDENTIFIED BY 'password';
GRANT ALL PRIVILEGES ON timetable.* TO 'user'@'localhost';
FLUSH PRIVILEGES;

# Run backend
python run.py
```

## Frontend Setup

```bash
cd frontend
npm install
ng serve  # Runs on http://localhost:4200
```

## Docker Deployment

```bash
docker-compose -f docker/docker-compose.yml up --build
```

## API Documentation

Once running, visit: http://localhost:8000/docs

## Key Features

- Automatic schedule generation with strict rule enforcement
- Manual schedule adjustments with validation
- Fair distribution of night shifts (min 8, max 10 per staff)
- Staff management UI
- Monthly calendar view
- Editable schedule grid
