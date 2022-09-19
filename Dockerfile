FROM ubuntu:focal

RUN apt-get update
RUN apt-get install -y software-properties-common
RUN apt-get install -y python3.9-minimal python3-dev python3-pip python3-venv libpq-dev

WORKDIR /usr/src/app

COPY requirements.txt .

RUN python3.9 -m pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "bash", "-c", "python3.9 -m scrapy crawl $CRAWLER -s TELNETCONSOLE_ENABLED=0" ]
