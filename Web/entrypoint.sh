#!/bin/bash
APP_PORT=${PORT:-8000}
cd /app/
/opt/venv/bin/gunicorn --worker-tmp-dir /dev/shm rdxSolutionsBackendProject.wsgi:application --bind "0.0.0.0:${APP_PORT}"

/opt/venv/bin/python3 manage.py migrate
/opt/venv/bin/python3 manage.py runserver
/opt/venv/bin/python3 manage.py collectstatic --noinput 