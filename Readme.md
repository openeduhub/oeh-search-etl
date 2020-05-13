# Open Edu Hub

## Database, Logstash & Elasticsearch
- make sure you have docker-compose installed
- go to project
- `docker-compose build && docker-compose up`

## ETL

- make sure you have python3 installed (<https://docs.python-guide.org/starting/install3/osx/>)
- go to project root
- Run
```
cd etl
sudo apt install python3-dev libpq-dev -y
python3 -m venv .venv
```

`source .venv/bin/activate` (on Linux Unix)

`.venv\Scripts\activate.bat` (on Windows)

`pip3 install -r requirements.txt`

- crawler can be run with `scrapy crawl <spider-name>`. It assumes that you have the postgres database running, so you should run the `docker-compose up` command from before.

## Building a Crawler

- We use Scrapy as a framework. Please check out the guides for Scrapy spider (https://docs.scrapy.org/en/latest/intro/tutorial.html)
- To create a new spider, create a file inside `converter/spiders/<myname>_spider.py`
- We recommend to inherit the `LomBase` class in order to get out-of-the-box support for our metadata model
- You may also Inherit a Base Class for crawling data, if your site provides LRMI metadata, the `LrmiBase` is a good start, if your system provides an OAI interface, you may use the `OAIBase`
- As a sample/template, may check out the `sample_spider.py`
- To learn more about the LOM standard we're using, may checkout https://en.wikipedia.org/wiki/Learning_object_metadata

## Frontend

The frontend is started together with the backend via `docker-compose`. However, Docker images for
the frontend are be built separately. See https://github.com/openeduhub/oeh-search-frontend.

### Update Deployment

After building a new frontend, run

```bash
docker-compose up -d --no-deps elasticsearch-relay frontend
```

### Routing

The frontend requires to be routed to the ElasticSearch relay on the same URL the frontend is
served. This can be achieved with a reverse proxy. A config for Apache could look like this:

```apacheconf
<VirtualHost *:80>
    # ...
    ProxyPass "/api" "http://localhost:3000/api"
    ProxyPass "/" "http://localhost:8080/"
</VirtualHost>
```
