web: python manage.py migrate && gunicorn core.wsgi
celery: celery -A core beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler
celery: celery -A core.celery worker -l info
