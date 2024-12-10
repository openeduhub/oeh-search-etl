FROM python:3.13-slim-bookworm

# ENV CRAWLER wirlernenonline_spider

WORKDIR /

COPY entrypoint.sh entrypoint.sh
COPY edu_sharing_openapi/ edu_sharing_openapi/
COPY pyproject.toml poetry.lock Readme.md ./
COPY scrapy.cfg scrapy.cfg
COPY setup.cfg setup.cfg
COPY converter/ converter/
COPY csv/ csv/
COPY valuespace_converter/ valuespace_converter/
RUN pip3 install poetry
RUN poetry install


ENTRYPOINT ["/entrypoint.sh"]
