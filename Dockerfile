FROM python:2-onbuild

COPY crypto_mediator /crypto_mediator
RUN pip install -e crypto_mediator
