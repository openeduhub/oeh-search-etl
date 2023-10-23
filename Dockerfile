FROM python:3.11.6-slim-bookworm

# ENV CRAWLER wirlernenonline_spider

WORKDIR /

COPY entrypoint.sh entrypoint.sh
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY scrapy.cfg scrapy.cfg
COPY setup.cfg setup.cfg
COPY converter/ converter/
COPY csv/ csv/
COPY edu_sharing_client/ edu_sharing_client/
COPY valuespace_converter/ valuespace_converter/

COPY web_service_plugin/requirements.txt web_service_plugin/requirements.txt
RUN pip3 install -r web_service_plugin/requirements.txt
COPY web_service_plugin/ /web_service_plugin

ENTRYPOINT ["/entrypoint.sh"]
