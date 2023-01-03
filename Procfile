web: python manage.py migrate && gunicorn core.wsgi
celery -A core worker -l info -B