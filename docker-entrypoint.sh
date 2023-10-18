#!/bin/sh

flask db upgrade

exec gunicorn --bind 0.0.0.0:80 --reload app:app 

find . -name "*.pyc" -exec rm -f {} \;
