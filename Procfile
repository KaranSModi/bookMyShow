web: python manage.py migrate && gunicorn core.wsgi
worker: celery worker --app=bookMyShowApp.tasks.app
beat: celery --app=bookMyShowApp.tasks.app