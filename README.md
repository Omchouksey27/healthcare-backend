# Healthcare Backend with Django, DRF, PostgreSQL, JWT, and Frontend

A full-stack healthcare assignment project built with Django, Django REST Framework, PostgreSQL, SimpleJWT, and a Django-served frontend dashboard. No Docker is required.

The system lets users register, log in, manage their own patient records, manage a shared doctor catalog, and assign doctors to patients.

## What Is Included

- JWT authentication with `djangorestframework-simplejwt`
- Custom email-based user model
- PostgreSQL configuration through environment variables
- Patient CRUD APIs scoped to the authenticated user
- Doctor CRUD APIs protected by authentication
- Patient-doctor mapping APIs protected by authentication
- Validation and consistent DRF error responses
- Django ORM models, indexes, constraints, admin setup, and migrations
- Modern frontend dashboard served from Django templates/static files
- Swagger/OpenAPI docs at `/api/docs/`
- Local PostgreSQL setup instructions
- Beginner guide, company handoff guide, API reference, and interview Q&A

## Project Structure

```text
healthcare-backend/
  apps/
    accounts/       Email user model, register API, login API
    patients/       Patient model and owner-scoped CRUD API
    doctors/        Doctor model and protected CRUD API
    mappings/       Patient-doctor assignment model and API
    frontend/       Django view that serves the dashboard
  config/           Django settings, URLs, ASGI, WSGI
  static/           Frontend CSS and JavaScript
  templates/        Frontend HTML template
  requirements.txt
  .env.example
```

## Quick Start

```powershell
cd outputs/healthcare-backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
psql -U postgres -c "CREATE DATABASE healthcare_db;"
psql -U postgres -c "CREATE USER healthcare_user WITH PASSWORD 'healthcare_password';"
psql -U postgres -c "GRANT ALL PRIVILEGES ON DATABASE healthcare_db TO healthcare_user;"
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

If the user already exists, PostgreSQL will report an error. That is fine; just make sure `.env` uses the correct username, password, host, port, and database name.

Open:

- Frontend dashboard: `http://127.0.0.1:8000/`
- Swagger API docs: `http://127.0.0.1:8000/api/docs/`
- Django admin: `http://127.0.0.1:8000/admin/`

## API Summary

| Method | Endpoint | Purpose | Auth |
| --- | --- | --- | --- |
| POST | `/api/auth/register/` | Register user | No |
| POST | `/api/auth/login/` | Login and receive JWT | No |
| POST | `/api/patients/` | Add patient | Yes |
| GET | `/api/patients/` | List own patients | Yes |
| GET | `/api/patients/<id>/` | Patient detail | Yes |
| PUT | `/api/patients/<id>/` | Update patient | Yes |
| DELETE | `/api/patients/<id>/` | Delete patient | Yes |
| POST | `/api/doctors/` | Add doctor | Yes |
| GET | `/api/doctors/` | List doctors | Yes |
| GET | `/api/doctors/<id>/` | Doctor detail | Yes |
| PUT | `/api/doctors/<id>/` | Update doctor | Yes |
| DELETE | `/api/doctors/<id>/` | Delete doctor | Yes |
| POST | `/api/mappings/` | Assign doctor to patient | Yes |
| GET | `/api/mappings/` | List mappings for own patients | Yes |
| GET | `/api/mappings/<patient_id>/` | List doctors for one patient | Yes |
| DELETE | `/api/mappings/<id>/` | Remove assignment by mapping id | Yes |

Read [API_REFERENCE.md](API_REFERENCE.md) for request and response examples.

## Security Notes

- All patient, doctor, and mapping endpoints require a Bearer access token.
- Patient queries are filtered by `owner=request.user`.
- A user cannot view or assign doctors to another user's patient.
- Passwords are hashed by Django's password hashing system.
- Secrets and database credentials are read from `.env`.
- JWT access tokens expire after 30 minutes by default.

## Documentation

- [README_COMPANY.md](README_COMPANY.md): professional evaluator/company handoff
- [README_BEGINNER.md](README_BEGINNER.md): beginner-friendly guide to Django, setup, run, and debug
- [POSTGRES_LOCAL_SETUP.md](POSTGRES_LOCAL_SETUP.md): local PostgreSQL setup without Docker
- [API_REFERENCE.md](API_REFERENCE.md): endpoints, payloads, and curl examples
- [INTERVIEW_QA.md](INTERVIEW_QA.md): interview questions and answers

## Testing

```powershell
python manage.py test
python manage.py check
```

Tests cover authentication, patient privacy, doctor access, and patient-doctor mapping behavior.
