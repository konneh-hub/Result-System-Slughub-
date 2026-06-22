University Result Management System (URMS) - Backend

This folder contains the Django backend for the URMS project.

Setup (development):

1. Create a virtual environment and activate it.

```bash
python -m venv .venv
# Windows
.\.venv\Scripts\Activate.ps1
# macOS / Linux
source .venv/bin/activate
```

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Create `.env` (copy `.env.example` if present) and set environment variables.

4. Run migrations and seed roles

```bash
python manage.py migrate
python manage.py seed_roles
```

5. Create a superuser

```bash
python manage.py createsuperuser
```

6. Run server

```bash
python manage.py runserver
```

Notes:
- The project supports `DATABASE_URL` env var for PostgreSQL; otherwise it falls back to SQLite.
- Password reset emails use the console backend by default in development. Configure SMTP env vars for production.
