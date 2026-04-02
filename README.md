# Hospital Management System

This project is a full-stack Hospital Management System with:

- Backend: Flask + Flask-RESTful + SQLAlchemy + JWT
- Frontend: Vue 3 + Vite + Bootstrap

It supports role-based access for Admin, Doctor, and Patient.

## Quick Start (Copy-paste these in 5 terminals)

**Terminal 1 - Redis:**
```bash
redis-server --daemonize yes && redis-cli ping
```

**Terminal 2 - Backend API:**
```bash
cd /workspaces/Hospital-Management-System/backend
source mad2venv/bin/activate
python app.py
```
Backend runs on `http://127.0.0.1:5000`

**Terminal 3 - Frontend Dashboard:**
```bash
cd /workspaces/Hospital-Management-System/frontend
npm run dev
```
Frontend runs on `http://localhost:5173`

**Terminal 4 - Celery Worker (for daily email reminders):**
```bash
cd /workspaces/Hospital-Management-System/backend
source mad2venv/bin/activate
export SMTP_HOST=127.0.0.1
export SMTP_PORT=1025
export SMTP_FROM_EMAIL=admin@hospital.local
export SMTP_USE_TLS=false
docker start mailhog || docker run -d --name mailhog -p 1025:1025 -p 8025:8025 mailhog/mailhog
celery -A celery_app.celery worker --loglevel=info
```
**Terminal 5 - Celery Beat (scheduler):**
```bash
cd /workspaces/Hospital-Management-System/backend
source mad2venv/bin/activate
celery -A celery_app.celery beat --loglevel=info
```

**View captured emails at:** `http://127.0.0.1:8025`
**Login:** Admin@123 / hospiadmin123

## Project Structure

- `backend/` contains the Flask API and database models.
- `frontend/` contains the Vue application.

## Prerequisites

- Python 3.10+ (3.12 works)
- Node.js 18+ and npm

## Backend Setup

1. Move to the backend folder:

    ```bash
    cd backend
    ```

2. Create a virtual environment (if needed):

    ```bash
    python -m venv mad2venv
    ```

3. Activate the virtual environment:

    ```bash
    source mad2venv/bin/activate
    ```

4. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

5. Run the backend server:

    ```bash
    python app.py
    ```

The backend runs on `http://127.0.0.1:5000`.

## Frontend Setup

1. Open a new terminal and move to frontend:

    ```bash
    cd frontend
    ```

2. Install dependencies:

    ```bash
    npm install
    ```

3. Start the development server:

    ```bash
    npm run dev
    ```

The frontend usually runs on `http://localhost:5173`.

## Authentication and Roles

- JWT authentication is enabled.
- Role-based dashboards:
  - Admin
  - Doctor
  - Patient

When the backend starts for the first time, it creates a default admin user:

- Email: `Admin@123`
- Password: `hospiadmin123`

## Useful Notes

- If you run commands from the project root, the backend venv path is:

  ```bash
  source backend/mad2venv/bin/activate
  ```

- To regenerate Python requirements after new installs:

  ```bash
  pip freeze > requirements.txt
  ```

## Background Jobs (Celery + Redis)

This project now includes background jobs for:

- Daily same-day appointment reminders (Email/GChat/SMS placeholders)
- Monthly doctor reports (HTML files)
- Patient-triggered async CSV export for treatment history

### Install backend job dependencies

```bash
cd backend
source mad2venv/bin/activate
pip install celery redis
```

### Start Redis

If Redis is installed locally:

```bash
redis-server
```

### Run Celery Worker

From `backend/`:

```bash
celery -A celery_app.celery worker --loglevel=info
```

### Run Celery Beat (Scheduler)

From `backend/` in a separate terminal:

```bash
celery -A celery_app.celery beat --loglevel=info
```

### Automatic Daily Appointment Reminders

To send appointment reminders automatically every day:

1. Start the Celery worker (processes jobs):
   ```bash
   cd backend
   source mad2venv/bin/activate
   celery -A celery_app.celery worker --loglevel=info
   ```

2. Start the Celery beat scheduler (triggers jobs on schedule):
   ```bash
   cd backend
   source mad2venv/bin/activate
   celery -A celery_app.celery beat --loglevel=info
   ```

3. (Optional) Configure SMTP and reminder time:
   ```bash
   export SMTP_HOST=127.0.0.1
   export SMTP_PORT=1025
   export SMTP_FROM_EMAIL=admin@hospital.local
   export DAILY_REMINDER_HOUR=8
   export DAILY_REMINDER_MINUTE=0
   export REMINDER_DAYS_AHEAD=1
   ```

**Scheduled Jobs**

- Daily reminder job: `tasks.send_same_day_appointment_reminders` (every day at 8:00 AM)
  - Sends emails to patients with appointments **tomorrow** (default: `REMINDER_DAYS_AHEAD=1`)
  - Change to `REMINDER_DAYS_AHEAD=0` for today's appointments
- Monthly report job: `tasks.generate_monthly_doctor_reports` (1st of each month, 2:00 AM)

### SMTP Email Configuration for Daily Reminders

To send real emails from reminder jobs, set before starting worker/beat:

```bash
export SMTP_HOST=smtp.gmail.com
export SMTP_PORT=587
export SMTP_USER=admin@example.com
export SMTP_PASSWORD=your_app_password
export SMTP_FROM_EMAIL=admin@example.com
export SMTP_USE_TLS=true
export SMTP_USE_SSL=false
```

Or use MailHog (fake inbox for testing):

```bash
# Start MailHog
docker run -d --name mailhog -p 1025:1025 -p 8025:8025 mailhog/mailhog

# Set SMTP to MailHog
export SMTP_HOST=127.0.0.1
export SMTP_PORT=1025
export SMTP_FROM_EMAIL=admin@hospital.local
export SMTP_USE_TLS=false
export SMTP_USE_SSL=false
```

View captured emails at `http://127.0.0.1:8025`

Monthly reports are generated under:

- `backend/instance/reports/<YYYY-MM>/`

### Async CSV Export API (Patient)

- Start export: `POST /patient/export-treatment-history`
- Check status: `GET /patient/export-treatment-history/<job_id>`
- Download when completed: `GET /patient/export-treatment-history/<job_id>/download`

The Patient Dashboard includes an "Export Treatment History (CSV)" button that starts the job and polls until completion.
