#!/bin/sh

cd /opt/scrapy || exit

if [ -n "$API_MODE" ] && [ "$API_MODE" -eq 0 ]
then
  uvicorn web_service_plugin.main:create_app --host 0.0.0.0 --port 80
elif [ "$API_MODE" -eq 1 ]
then
  echo "Crawler setted up for command line use"
elif [ -z "$ARGS" ]
then
  scrapy crawl "$CRAWLER"
else
  scrapy crawl -a "$ARGS" "$CRAWLER"
fi

