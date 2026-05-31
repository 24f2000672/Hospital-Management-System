# Health Guardian+

Health Guardian+ is a smart healthcare, emergency assistance, and accessibility platform built with a Flask backend and a Vue frontend. It supports three user roles and combines healthcare management with emergency response, health monitoring, and inclusive access features.

## Core Users

- Patient: appointments, medical records, SOS alerts, reminders, health reports, and accessibility tools
- Doctor: appointment handling, prescriptions, treatment history, patient tracking, and telemedicine support
- Administrator: user management, analytics, SOS monitoring, security, and hospital oversight

## Key Capabilities

- Smart appointment booking and slot management
- Emergency SOS with GPS sharing and contact notifications
- Personal health records and document storage
- AI-assisted symptom checking and basic health recommendations
- Medicine reminders and adherence tracking
- Accessibility support for blind, deaf, mute, elderly, and specially-abled users
- Telemedicine workflows and digital prescriptions
- Analytics dashboards for appointments, treatment trends, and performance tracking

## Tech Stack

- Backend: Python, Flask, Flask RESTful, SQLAlchemy, JWT authentication
- Database: SQLite now, PostgreSQL later
- Frontend: Vue.js, Ionic Framework, HTML, CSS, JavaScript
- Mobile: Ionic Vue, Capacitor, Android Studio
- Services: GPS, SMS, push notifications, accessibility APIs, AI assistant integration

## Project Structure

- `backend/` contains the Flask API, models, tasks, and background jobs.
- `frontend/` contains the Vue application and UI views.

## Prerequisites

- Python 3.10+
- Node.js 18+ and npm
- Redis if you want Celery reminders and scheduled jobs

## Backend Setup

1. Go to the backend folder.

  ```bash
  cd backend
  ```

2. Create and activate a virtual environment if needed.

  ```bash
  python -m venv mad2venv
  source mad2venv/bin/activate
  ```

3. Install Python dependencies.

  ```bash
  pip install -r requirements.txt
  ```

4. Start the backend.

  ```bash
  python app.py
  ```

The API runs at `http://127.0.0.1:5000`.

## Frontend Setup

1. Go to the frontend folder.

  ```bash
  cd frontend
  ```

2. Install dependencies.

  ```bash
  npm install
  ```

3. Start the development server.

  ```bash
  npm run dev
  ```

The frontend usually runs at `http://localhost:5173`.

## Background Jobs

The backend includes Celery-based background jobs for reminders, monthly reports, and async exports.

### Redis

```bash
redis-server
```

### Celery Worker

```bash
cd backend
source mad2venv/bin/activate
celery -A celery_app.celery worker --loglevel=info
```

### Celery Beat

```bash
cd backend
source mad2venv/bin/activate
celery -A celery_app.celery beat --loglevel=info
```

### MailHog for local email testing

```bash
docker run -d --name mailhog -p 1025:1025 -p 8025:8025 mailhog/mailhog
```

View captured mail at `http://127.0.0.1:8025`.

## Default Admin Login

- Email: `Admin@123`
- Password: `hospiadmin123`

## Notes

- If you run commands from the repo root, activate the backend venv with `source backend/mad2venv/bin/activate`.
- Celery jobs are configured in `backend/celery_app.py` and task handlers live in `backend/tasks.py`.
