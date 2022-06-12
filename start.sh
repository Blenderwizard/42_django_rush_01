#!/bin/sh

python3 -m venv venv
source ./venv/bin/activate
python3 -m pip install --upgrade pip
python3 -m pip install --log pip_log_$(echo $(date +%s)).log --upgrade --disable-pip-version-check --force-reinstall -r requirements.txt
python3 manage.py makemigrations member forum chat
python3 manage.py migrate
python3 manage.py collectstatic
nginx -s stop
nginx
python3 -m gunicorn rush01.wsgi
