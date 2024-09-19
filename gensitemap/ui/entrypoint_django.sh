#!/bin/sh

cd /opt/scrapy/ui || exit

python3 manage.py runserver 0.0.0.0:8000