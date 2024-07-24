#!/bin/sh

cd /opt/scrapy || exit

if [ "$API_MODE" = true ]
then
  echo "Using Scrapyd for the generic crawler"
  scrapyd

else
  echo "Crawler setted up for command line use"
  if [ -z "$ARGS" ]
  then
    scrapy crawl "$CRAWLER"
  else
    scrapy crawl -a "$ARGS" "$CRAWLER"
  fi
fi