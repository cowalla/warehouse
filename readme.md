
example startup:
source secret.sh; source environment.sh; python manage.py runserver

celery beat:
python manage.py celery beat

celery worker:
python manage.py celery worker --loglevel=info