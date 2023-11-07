FROM python:3.10.9-slim-buster

# ENV CRAWLER wirlernenonline_spider

WORKDIR /

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY entrypoint.sh entrypoint.sh
COPY scrapy.cfg scrapy.cfg
COPY setup.cfg setup.cfg
COPY converter/ converter/
COPY csv/ csv/
COPY edu_sharing_client/ edu_sharing_client/
COPY valuespace_converter/ valuespace_converter/
COPY z_api/ z_api/


ENTRYPOINT ["/entrypoint.sh"]
