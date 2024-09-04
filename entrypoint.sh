#!/bin/sh

if [ -z "$ARGS" ]
then
  poetry run scrapy crawl "$CRAWLER"
else
  poetry run scrapy crawl -a "$ARGS" "$CRAWLER"
fi

