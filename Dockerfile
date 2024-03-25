FROM python:3.10.13-bookworm

# ENV CRAWLER wirlernenonline_spider

RUN mkdir /opt/scrapy

WORKDIR /opt/scrapy

RUN apt-get update && \
    apt-get install -y wget && \
    apt-get install -y python3-lxml && \
    apt-get install -y libxml2-dev libxslt-dev && \
    apt-get install -y openjdk-17-jre-headless && \
    apt-get clean;

COPY entrypoint.sh entrypoint.sh
COPY requirements.txt requirements.txt
COPY scrapy.cfg scrapy.cfg
COPY setup.cfg setup.cfg
COPY converter/ converter/
COPY csv/ csv/
COPY edu_sharing_client/ edu_sharing_client/
COPY valuespace_converter/ valuespace_converter/
RUN pip3 install -r requirements.txt

RUN echo "Install Z-API ---------------------------- "
COPY generate-z-api.sh generate-z-api.sh
RUN ./generate-z-api.sh

COPY web_service_plugin/requirements.txt web_service_plugin/requirements.txt
RUN pip3 install -r web_service_plugin/requirements.txt
COPY web_service_plugin/ /web_service_plugin

EXPOSE 80

# ENTRYPOINT ["/entrypoint.sh"]
