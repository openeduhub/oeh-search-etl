# Open Edu Hub Search ETL

- make sure you have python3 installed (<https://docs.python-guide.org/starting/installation/>)
- (Python 3.9.1 or newer is required)
- go to project root
- Run
```
sudo apt install python3-dev python3-pip python3-venv libpq-dev -y
python3 -m venv .venv
```

`source .venv/bin/activate` (on Linux Unix)

`.venv\Scripts\activate.bat` (on Windows)

`pip3 install -r requirements.txt`

If you have Docker installed, use `docker-compose up` to start up the multi-container for `Splash` and `Pyppeteer`-integration. 

As a last step, set up your config variables by copying the `.env.example`-file and modifying it if necessary: 

`cp converter/.env.example converter/.env`

- A crawler can be run with `scrapy crawl <spider-name>`. It assumes that you have an edu-sharing 6.0 instance in your `.env` settings configured which can accept the data.
- If a crawler has [Scrapy Spider Contracts](https://docs.scrapy.org/en/latest/topics/contracts.html#spiders-contracts) implemented, you can test those by running `scrapy check <spider-name>`


## Run via Docker
```bash
git clone https://github.com/openeduhub/oeh-search-etl
cd oeh-search-etl
cp .env.example .env
# modify .env with your edu sharing instance
docker compose build scrapy
export CRAWLER=your_crawler_id_spider # i.e. wirlernenonline_spider
docker compose up
```

## Building a Crawler

- We use Scrapy as a framework. Please check out the guides for Scrapy spider (https://docs.scrapy.org/en/latest/intro/tutorial.html)
- To create a new spider, create a file inside `converter/spiders/<myname>_spider.py`
- We recommend inheriting the `LomBase` class in order to get out-of-the-box support for our metadata model
- You may also Inherit a Base Class for crawling data, if your site provides LRMI metadata, the `LrmiBase` is a good start. If your system provides an OAI interface, you may use the `OAIBase`
- As a sample/template, please take a look at the `sample_spider.py`
- To learn more about the LOM standard we're using, you'll find useful information at https://en.wikipedia.org/wiki/Learning_object_metadata

## Run the web service for the generic crawler

A web service that implements the FastAPI web framework is added to the project. In order to start the web service it is enough setting API_MODE=True for that new variable.
The web service is started at localhost at the 5500 port.
```bash
git clone https://github.com/openeduhub/oeh-search-etl
cd oeh-search-etl
cp converter/.env.example .env
# modify .env with your edu sharing instance
docker compose build scrapy
export $API_MODE=True
docker compose up
```


## Still have questions? Check out our GitHub-Wiki!
If you need help getting started or setting up your work environment, please don't hesitate to visit our GitHub Wiki at https://github.com/openeduhub/oeh-search-etl/wiki
