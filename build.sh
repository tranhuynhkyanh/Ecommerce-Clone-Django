#!/usr/bin/env bash
# exit on error
set -o errexit
python -m pip install --upgrade pip
pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py makemigrations
python manage.py migrate --run-syncdb
python -m celery -A Ecommerce worker -l info --pool=solo