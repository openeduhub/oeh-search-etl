FROM python:3.10.13-bookworm

# ENV CRAWLER wirlernenonline_spider

WORKDIR /

RUN apt-get update && \
    apt-get install -y python3-lxml && \
    apt-get install -y libxml2-dev libxslt-dev;

COPY entrypoint.sh entrypoint.sh
COPY requirements.txt requirements.txt
COPY scrapy.cfg scrapy.cfg
COPY setup.cfg setup.cfg
COPY converter/ converter/
COPY csv/ csv/
COPY edu_sharing_client/ edu_sharing_client/
COPY valuespace_converter/ valuespace_converter/
RUN pip3 install -r requirements.txt

# Install OpenJDK-11 OR 21
RUN echo "Install Java 11 ---------------------------- "

# COPY jdk-21_linux-x64_bin.deb jdk-21_linux-x64_bin.deb
# RUN apt-get -qqy install ./jdk-21_linux-x64_bin.deb

RUN wget https://repo1.maven.org/maven2/org/openapitools/openapi-generator-cli/7.2.0/openapi-generator-cli-7.2.0.jar -O openapi-generator-cli.jar
COPY openapi-generator-cli.jar openapi-generator-cli.jar
# RUN java -jar openapi-generator-cli.jar

RUN apt-get update && \
    apt-get install -y default-jre-headless && \
    apt-get clean;

RUN echo "Install Z-API ---------------------------- "
COPY generate-z-api.sh generate-z-api.sh
RUN /bin/bash -c '/generate-z-api.sh'

COPY web_service_plugin/requirements.txt web_service_plugin/requirements.txt
RUN pip3 install -r web_service_plugin/requirements.txt
COPY web_service_plugin/ /web_service_plugin

EXPOSE 80

# ENTRYPOINT ["/entrypoint.sh"]
