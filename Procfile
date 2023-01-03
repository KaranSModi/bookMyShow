web: python manage.py migrate && gunicorn core.wsgi
celery: celery -A core beat -l INFO
