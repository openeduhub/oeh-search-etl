# Open Edu Hub Search ETL

## Requirements
Before doing *anything* in this repository, make sure you meet the following requirements.

- Python 3.9
- a python virtual environment
- an .env file containing all the necessary credentials and settings

Debian-based systems:
```bash
sudo apt install python3.9 python3-dev python3-pip python3-venv libpq-dev
python3.9 -m venv .venv
source .venv/bin/activate
pip3 install -r requirements.txt
cp .env.example .env
# edit to your liking
```

For windows, go to python.org to download the proper python version.
```commandline
python3.9 -m venv .venv
.venv\Scripts\activate.bat
pip3 install -r requirements.txt
copy .env.example .env
REM edit to your liking
```

## Run a crawler
```bash
scrapy crawl oeh_spider 
```

If you have Docker installed, use `docker-compose up` to start up the multi-container for `Splash` and `Pyppeteer`-integration.

If a crawler has [Scrapy Spider Contracts](https://docs.scrapy.org/en/latest/topics/contracts.html#spiders-contracts) implemented, you can test those by running `scrapy check <spider-name>`

## Building a docker image
```bash
docker build --tag oeh-search-etl .
```

## Building a crawler

- We use Scrapy as a framework. Please check out the guides for Scrapy spider (https://docs.scrapy.org/en/latest/intro/tutorial.html)
- To create a new spider, create a file inside `converter/spiders/<myname>_spider.py`
- We recommend inheriting the `LomBase` class in order to get out-of-the-box support for our metadata model
- You may also Inherit a Base Class for crawling data, if your site provides LRMI metadata, the `LrmiBase` is a good start. If your system provides an OAI interface, you may use the `OAIBase`
- As a sample/template, please take a look at the `sample_spider.py`
- To learn more about the LOM standard we're using, you'll find useful information at https://en.wikipedia.org/wiki/Learning_object_metadata

## Using scripts in schulcloud/*
```bash
set -a
source .env
# cd into the script's directory and execute it
```

## Still have questions? Check out our GitHub-Wiki!
If you need help getting started or setting up your work environment, please don't hesitate to visit our GitHub Wiki at https://github.com/openeduhub/oeh-search-etl/wiki
