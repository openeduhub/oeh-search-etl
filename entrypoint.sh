#!/bin/sh

if [ -n "$API_MODE" ] && [ "$API_MODE" -eq 0 ]
then
  uvicorn web_service_plugin.main:create_app --host 127.0.0.1 --port 5500
elif [ "$API_MODE" -eq 1 ]
then
  echo "Crawler setted up for command line use"
elif [ -z "$ARGS" ]
then
  scrapy crawl "$CRAWLER"
else
  scrapy crawl -a "$ARGS" "$CRAWLER"
fi

