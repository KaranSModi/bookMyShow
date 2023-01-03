web: python manage.py migrate && gunicorn core.wsgi
worker1: celery -A core beat -l info
worker2: celery -A core worker -l info