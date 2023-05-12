FROM python:3.9-slim-buster

RUN apt-get install ca-certificates

WORKDIR /oeh-search-etl

COPY requirements.txt .
RUN python3.9 -m pip install --no-cache-dir -r requirements.txt

COPY . .
COPY .env.docker .env

CMD [ "bash", "-c", "python3.9 run.py" ]
