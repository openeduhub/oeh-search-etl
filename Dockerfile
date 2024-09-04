FROM python:3.12.5-slim-bookworm

# ENV CRAWLER wirlernenonline_spider

WORKDIR /

COPY entrypoint.sh entrypoint.sh
COPY edu_sharing_openapi/ edu_sharing_openapi/
COPY pyproject.toml poetry.lock ./
RUN pip3 install poetry
RUN poetry install
COPY scrapy.cfg scrapy.cfg
COPY setup.cfg setup.cfg
COPY converter/ converter/
COPY csv/ csv/
COPY valuespace_converter/ valuespace_converter/


ENTRYPOINT ["/entrypoint.sh"]
