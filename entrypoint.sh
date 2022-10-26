#!/bin/sh

if [ -z "$ARGS" ]
then
  scrapy crawl "$CRAWLER"
else
  scrapy crawl -a "$ARGS" "$CRAWLER"
fi

