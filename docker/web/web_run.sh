#!/bin/sh
# wait for postgres
sleep 5
cd /srv/project/
python3 manage.py migrate
python3 manage.py loaddata admin
python3 manage.py runserver 0.0.0.0:8000