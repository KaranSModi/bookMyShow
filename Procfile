web: python manage.py migrate && gunicorn core.wsgi
celery: celery -A core.celery worker -l info
celerybeat: celery -A core beat -l INFO