### Database, Logstash & Elasticsearch
- make sure you have docker-compose installed
- go to project
- `docker-compose build && docker-compose up`

### ETL

- make sure you have python3 installed (<https://docs.python-guide.org/starting/install3/osx/>)
- go to project root
- `cd etl`
- `sudo apt install libpq-dev -y`
- `python3 -m venv etl`
- `pip3 install -r requirements.txt`

- crawler can be run with `scrapy crawl <spider-name>`. It assumes that you have the postgres database running, so you should run the `docker-compose up` command from before.
