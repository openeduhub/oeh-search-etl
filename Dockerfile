FROM python:3.12.4-slim-bookworm

# ENV CRAWLER wirlernenonline_spider

WORKDIR /

COPY entrypoint.sh entrypoint.sh
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY scrapy.cfg scrapy.cfg
COPY setup.cfg setup.cfg
COPY converter/ converter/
COPY csv/ csv/
COPY edu_sharing_openapi/ edu_sharing_openapi/
COPY valuespace_converter/ valuespace_converter/


ENTRYPOINT ["/entrypoint.sh"]
