FROM ubuntu:focal

RUN apt-get update
RUN apt-get install -y software-properties-common
RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt-get install -y python3.9
RUN apt-get install -y python3-dev python3-pip python3-venv libpq-dev

WORKDIR /usr/src/app

COPY requirements.txt .

RUN python3.9 -m pip install --no-cache-dir -r requirements.txt

COPY . .

RUN cp converter/.env.docker converter/.env

CMD [ "python3.9", "-m", "scrapy", "crawl", "sodix_spider" ]
