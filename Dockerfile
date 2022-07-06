FROM python:3.9.1-slim-buster

ENV CRAWLER wirlernenonline_spider 

WORKDIR /

COPY requirements.txt requirements.txt
COPY scrapy.cfg scrapy.cfg
COPY setup.cfg setup.cfg
COPY converter/ converter/
COPY csv/ csv/
COPY edu_sharing_client/ edu_sharing_client/
COPY valuespace_converter/ valuespace_converter/
RUN pip3 install -r requirements.txt


CMD scrapy crawl "$CRAWLER"
