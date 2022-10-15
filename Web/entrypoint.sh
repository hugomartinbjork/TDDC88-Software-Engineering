#!/bin/bash
# APP_PORT=${PORT:-8000}
SUPERUSER_EMAIL=${DJANGO_SUPERUSER_EMAIL:-"admin@rdx.com"}
cd /app/
# /opt/venv/bin/gunicorn --worker-tmp-dir /dev/shm rdxSolutionsBackendProject.wsgi:application --bind "0.0.0.0:${APP_PORT}"
/opt/venv/bin/python3 manage.py migrate --noinput
/opt/venv/bin/python3 manage.py collectstatic --noinput
/opt/venv/bin/python manage.py createsuperuser --email $SUPERUSER_EMAIL --noinput || true
/opt/venv/bin/python3 manage.py runserver 0.0.0.0:8000