#!/bin/bash
python manage.py makemigrations                  # Apply database migrations
python manage.py migrate                  # Apply database migrations
python manage.py collectstatic --noinput  # Collect static files

