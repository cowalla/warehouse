#!/usr/bin/env bash
# load in environment variables
source environment.sh

gunicorn warehouse.wsgi:application