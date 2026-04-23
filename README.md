# Hospital Management System

A comprehensive hospital management system built with Django.

## Features
- **User Management**: Admin, Doctor, Receptionist, and Patient roles.
- **Patient Records**: Track admissions, medical history, and doctor visits.
- **Billing**: Automatic bill generation based on ward charges and doctor visits.
- **Reporting**: Upload and view patient health reports (PDF).
- **Security**: Robust role-based access control (RBAC).

## Local Setup
1. Clone the repository.
2. Create a virtual environment: `python -m venv venv`.
3. Activate the venv: `.\venv\Scripts\activate` (Windows) or `source venv/bin/activate` (Mac/Linux).
4. Install dependencies: `pip install -r requirements.txt`.
5. Create a `.env` file based on the environment variables needed.
6. Run migrations: `python manage.py migrate`.
7. Seed initial data: `python manage.py seed_data`.
8. Start the server: `python manage.py runserver`.

## Deployment (Render)
This project is configured for one-click deployment on Render using `render.yaml`.
1. Push the code to GitHub.
2. On Render, create a new **Blueprint**.
3. Connect your repository.
4. Render will automatically setup the Web Service and PostgreSQL database.

## Environment Variables
- `SECRET_KEY`: Django secret key.
- `DEBUG`: Set to `False` in production.
- `DATABASE_URL`: Connection string for PostgreSQL.
- `EMAIL_USER`: Gmail address for automated notifications.
- `EMAIL_PASSWORD`: Gmail App Password.
