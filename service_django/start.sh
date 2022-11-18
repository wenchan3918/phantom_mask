#!/bin/bash

python manage.py makemigrations
python manage.py migrate

gunicorn phantom_mask.wsgi \
  --workers 3 \
  --bind=:8080 \
  --log-level=debug \
  --log-file='-' \
  --capture-output \
  --enable-stdio-inheritance
