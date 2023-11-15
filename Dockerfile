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

# Install OpenJDK-11
RUN echo "Install Java 11 ---------------------------- "
RUN apt-get update && \
    apt-get install -y openjdk-11-jre-headless && \
    apt-get clean;
RUN echo "Install Z-API ---------------------------- "
COPY generate-z-api.sh generate-z-api.sh
RUN /bin/bash -c '/generate-z-api.sh'

COPY web_service_plugin/requirements.txt web_service_plugin/requirements.txt
RUN pip3 install -r web_service_plugin/requirements.txt
COPY web_service_plugin/ /web_service_plugin

ENTRYPOINT ["/entrypoint.sh"]
