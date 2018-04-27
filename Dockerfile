FROM python:2-onbuild

RUN apt-get update
RUN apt-get -y install postgresql postgresql-contrib

COPY crypto_mediator /crypto_mediator
RUN pip install -e crypto_mediator

VOLUME ["/app"]

WORKDIR /app