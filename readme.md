
### Docker

Build base docker image with crypto_mediator:
  - ./build.sh

Specify run configs in secret.env (SECRET_KEY and database configs are absolutely necessary)

Run services with docker
  - docker-compose up -d

Create a superuser
  - docker exec -it warehouse_warehouse_1 python manage.py createsuperuser

Without docker:

example startup:
python manage.py runserver

celery beat:
python manage.py celery beat

celery worker:
python manage.py celery worker --loglevel=info
