#!/bin/sh

if [ -n "$API_MODE" ]
then
  uvicorn web_service_plugin.main:create_app --host 0.0.0.0 --port 5500
elif [ -z "$ARGS" ]
then
  scrapy crawl "$CRAWLER"
else
  scrapy crawl -a "$ARGS" "$CRAWLER"
fi

