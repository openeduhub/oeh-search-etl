FROM python:3.10.9-slim-buster

# ENV CRAWLER wirlernenonline_spider

WORKDIR /

COPY entrypoint.sh entrypoint.sh
COPY requirements.txt requirements.txt
COPY scrapy.cfg scrapy.cfg
COPY setup.cfg setup.cfg
COPY converter/ converter/
COPY csv/ csv/
COPY edu_sharing_client/ edu_sharing_client/
COPY valuespace_converter/ valuespace_converter/
RUN pip3 install -r requirements.txt


ENTRYPOINT ["/entrypoint.sh"]
