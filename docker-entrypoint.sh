#!/bin/sh

flask db upgrade

exec gunicorn --bind 0.0.0.0:80  app:app --preload

find . -name "*.pyc" -exec rm -f {} \;
