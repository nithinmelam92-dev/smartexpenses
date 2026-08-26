# Smart Expenses Tracker

A student-focused Django expense tracker for recording, managing, and analyzing everyday spending.

## Run locally

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Open `http://127.0.0.1:8000/`.

## Deploy on Render

1. Open the repository on GitHub and choose **Deploy to Render** or create a new Blueprint from `render.yaml`.
2. Create a PostgreSQL database on Render and copy its internal connection string.
3. Set the web service `DATABASE_URL` environment variable to that connection string.
4. Set `DJANGO_CSRF_TRUSTED_ORIGINS` to the deployed HTTPS URL.
5. Deploy. Render runs `build.sh`, which applies migrations and collects static files.

The service uses Gunicorn and WhiteNoise in production. Keep `DJANGO_DEBUG=0`, use a generated `DJANGO_SECRET_KEY`, and never commit `.env` or database files.
