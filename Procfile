web: python manage.py migrate && gunicorn core.wsgi
worker: celery -A core worker -l info -B