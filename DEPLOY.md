# Deploy to Railway

## Prerequisites

- GitHub repo connected to Railway
- Railway project with this app and (optionally) PostgreSQL + Volume

## Environment variables (Railway service → Variables)

| Variable | Required | Notes |
|----------|----------|--------|
| `DJANGO_ENV` | Yes | Set to `production` |
| `DJANGO_SECRET_KEY` | Yes | Generate a strong random secret (e.g. `python -c "import secrets; print(secrets.token_urlsafe(50))"`) |
| `DATABASE_URL` | Yes (if using Postgres) | Set automatically when you add a PostgreSQL service and reference it (e.g. `${{Postgres.DATABASE_URL}}`) |
| `RAILWAY_VOLUME_MOUNT_PATH` | Auto | Set automatically when you add a Volume to the app service; used for `MEDIA_ROOT` (uploaded images) |
| `ALLOWED_HOSTS` | Optional | Comma-separated hosts; default includes `.railway.app` |

## PostgreSQL (Railway)

1. In the project, click **+ Add** → **Database** → **PostgreSQL**.
2. In the **app service** Variables, add reference to Postgres (e.g. `DATABASE_URL` = `${{Postgres.DATABASE_URL}}`), or use the individual `PGHOST`, `PGPORT`, `PGUSER`, `PGPASSWORD`, `PGDATABASE` if your app expects them (this project uses `dj-database-url` with `DATABASE_URL`).

## Volume for media (images)

1. Open the **app service** → **Settings** → **Volumes**.
2. Click **Add Volume** (e.g. name: `media-volume`, mount path: `/data` or leave default).
3. Railway sets `RAILWAY_VOLUME_MOUNT_PATH` automatically; the app uses it as `MEDIA_ROOT`.

## Build and run

- **Start command**: Railway can use the Procfile (`web: gunicorn config.wsgi:application`) or set a custom start command: `gunicorn config.wsgi:application`.
- **Migrations**: Run in build or as a release command, e.g. `python manage.py migrate --noinput`.
- **Static files**: `python manage.py collectstatic --noinput` should run in build (or add to start script). WhiteNoise serves them in production.

## Create superuser (first deploy)

Because `postgres.railway.internal` is only reachable from inside Railway, you cannot run `createsuperuser` from your local machine. Use optional env vars so the app creates a superuser on startup:

1. In the **web** service → **Variables**, add (temporarily):
   - `DJANGO_SUPERUSER_USERNAME` = your admin username
   - `DJANGO_SUPERUSER_EMAIL` = your email
   - `DJANGO_SUPERUSER_PASSWORD` = your password
2. Redeploy (or push a commit). On startup, the app will run `createsuperuser --noinput` once.
3. After logging in to `/admin/`, **remove** these variables (especially the password) from Railway Variables and redeploy.

## After deploy

- Generate a **public domain** in the app service (Settings → Networking).
- Optionally add a custom domain and include it in `ALLOWED_HOSTS`.
