FROM python:3.9-slim-buster

WORKDIR /usr/src/app

COPY requirements.txt .

RUN python3.9 -m pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "bash", "-c", "python3.9 -m scrapy crawl $CRAWLER -s TELNETCONSOLE_ENABLED=0" ]
