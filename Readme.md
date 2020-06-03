# Open Edu Hub

## Build

### Database, Logstash, and Elasticsearch

Docker images can be built using docker compose:

```bash
docker-compose pull --ignore-pull-failures
docker-compose build
```

### Frontend

Docker images for the frontend and its dependencies are be built separately. See
https://github.com/openeduhub/oeh-search-frontend.

## Run

Run `docker-compose up` to start all required containers.

### Runtime Configuration

Some variables have to be defined in a `.env` file.
Copy `.env.example` to `.env` and adapt the values to your configuration.

### HTTP Server and Routing

The frontend requires routes to the ElasticSearch relay and the editor backend
under the same URL the frontend is served. This can be achieved with a reverse
proxy. A config for Nginx could look like this:

```nginx
server {
    # ...
    location / {
            proxy_pass http://localhost:8080;
    }
    location /relay/ { 
            proxy_pass http://localhost:3000/; 
    } 
    location /editor/ { 
            proxy_pass http://localhost:3001/;
    }
}
```

### Update Deployment

Individual components can be updated independently, e.g.,

```bash
docker-compose up -d --no-deps elasticsearch-relay frontend
```

## ETL

- make sure you have python3 installed (<https://docs.python-guide.org/starting/install3/osx/>)
- go to project root
- Run
```
cd etl
sudo apt install python3-dev python3-pip python3-venv libpq-dev -y
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
