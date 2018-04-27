
### Docker

Set important host environment variables,

 - source docker.env

Build base docker image with crypto_mediator,
  - ./build.sh

Specify run configs in environment.env (SECRET_KEY and database configs are absolutely necessary)

Run services with docker
  - docker-compose -f docker/warehouse/docker-compose.yml up -d
  - docker-compose -f docker/celery/docker-compose.yml up -d

Create a superuser
  - docker exec -it warehouse_warehouse_1 python manage.py createsuperuser

Without docker:

example startup:
python manage.py runserver

celery beat:
python manage.py celery beat

celery worker:
python manage.py celery worker --loglevel=info


# OTHER

helpful: git update-index --assume-unchanged environment.env
