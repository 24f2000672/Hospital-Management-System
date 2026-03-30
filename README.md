# Hospital Management System

This project is a full-stack Hospital Management System with:

- Backend: Flask + Flask-RESTful + SQLAlchemy + JWT
- Frontend: Vue 3 + Vite + Bootstrap

It supports role-based access for Admin, Doctor, and Patient.

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
