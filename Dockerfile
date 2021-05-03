FROM python:3.9.1-slim-buster

ENV CRAWLER wirlernenonline_spider 

WORKDIR /

COPY . . 
RUN pip3 install -r requirements.txt


CMD scrapy crawl "$CRAWLER"
