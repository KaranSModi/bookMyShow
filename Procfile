web: python manage.py migrate && gunicorn core.wsgi
celery: celery -A core worker -l info -B