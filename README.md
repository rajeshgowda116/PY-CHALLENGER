# PY Challenger

Production-ready Django coding challenge platform with auth, dashboard, topics, submissions, and secure-by-default deployment settings.

## Production requirements

- Python 3.13
- PostgreSQL
- `pip install -r requirements.txt`
- Environment variables from `.env.example`

## Important security note

This project disables local code execution automatically when `DJANGO_DEBUG=False`.

That is intentional. Running untrusted Python inside the Django web process is not production-safe.
To deploy public code execution, replace the current runner with an isolated sandbox service or container worker.

## Production setup

1. Create and activate a virtual environment.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Configure environment variables using `.env.example`.
4. Use PostgreSQL in production.
5. Collect static files:

```bash
python manage.py collectstatic --noinput
```

6. Run migrations:

```bash
python manage.py migrate
```

7. Start the app with Gunicorn:

```bash
gunicorn config.wsgi:application --bind 0.0.0.0:8000
```

## Health check

Use:

```text
/health/
```

## Render deployment

Render supports Django deployments with a build command, Gunicorn start command, PostgreSQL, and optionally a `render.yaml` Blueprint. I added:

- [render.yaml](c:/Users/rajes/OneDrive/Desktop/Raj/render.yaml)
- [build.sh](c:/Users/rajes/OneDrive/Desktop/Raj/build.sh)
- [Procfile](c:/Users/rajes/OneDrive/Desktop/Raj/Procfile)

### Deploy on Render with Blueprint

1. Push this repository to GitHub.
2. In Render, click `New` -> `Blueprint`.
3. Connect the repository.
4. Render will detect [render.yaml](c:/Users/rajes/OneDrive/Desktop/Raj/render.yaml) and create:
   - one web service
   - one PostgreSQL database
5. Review the generated environment variables.
6. Update `DJANGO_CSRF_TRUSTED_ORIGINS` if your final Render hostname differs from the default in the blueprint.
7. Deploy.

### Deploy on Render manually

If you do not want to use Blueprint:

- Build command: `./build.sh`
- Start command: `gunicorn config.wsgi:application --bind 0.0.0.0:$PORT`

Set these environment variables in Render:

- `DJANGO_DEBUG=False`
- `DJANGO_SECRET_KEY=<generate a strong secret>`
- `DJANGO_ALLOWED_HOSTS=<your-render-hostname>`
- `DJANGO_CSRF_TRUSTED_ORIGINS=https://<your-render-hostname>`
- `DJANGO_LOG_LEVEL=INFO`
- `POSTGRES_DB`
- `POSTGRES_USER`
- `POSTGRES_PASSWORD`
- `POSTGRES_HOST`
- `POSTGRES_PORT`
- `ENABLE_LOCAL_CODE_EXECUTION=False`

### After first deploy

Open the Render shell and create an admin user:

```bash
python manage.py createsuperuser
```

Check health:

```text
https://<your-render-hostname>/health/
```

## Recommended reverse proxy

Use Nginx or a managed platform that terminates HTTPS and forwards `X-Forwarded-Proto`.

## Minimum environment variables

- `DJANGO_DEBUG=False`
- `DJANGO_SECRET_KEY`
- `DJANGO_ALLOWED_HOSTS`
- `DJANGO_CSRF_TRUSTED_ORIGINS`
- `POSTGRES_DB`
- `POSTGRES_USER`
- `POSTGRES_PASSWORD`
- `POSTGRES_HOST`
- `POSTGRES_PORT`
- `ENABLE_LOCAL_CODE_EXECUTION=False`
