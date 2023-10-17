#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate --run-syncdb
python manage.py loaddata data.json
daphne -p 8001 Ecommerce.asgi:application