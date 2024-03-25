#!/bin/sh

cd /opt/scrapy || exit

if [ "$API_MODE" = true ]
then
  uvicorn web_service_plugin.main:create_app --host 0.0.0.0 --port 80
else
  echo "Crawler setted up for command line use"
  if [ -z "$ARGS" ]
  then
    scrapy crawl "$CRAWLER"
  else
    scrapy crawl -a "$ARGS" "$CRAWLER"
  fi
fi