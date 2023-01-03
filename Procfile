web: python manage.py migrate && gunicorn core.wsgi
celery: elery -A core worker -l info -B
