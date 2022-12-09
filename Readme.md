# Open Edu Hub Search ETL

This repository is forked from openeduhub. Only a few spiders are directly in use
with oeh being the main one. Others are mediothek_pixiothek, merlin, sodix.
Notable differences to the original repository are schulcloud/ and run.py.

The terms "spider" and "crawler" may be used interchangeable.

## Requirements
Before doing anything in this repository, make sure you meet the following requirements:

- docker and docker-compose
- Python 3.9
- a python virtual environment
- an .env file containing all the necessary credentials and settings
- splash service for crawlers

Debian-based systems:
```bash
sudo apt install python3.9 python3-dev python3-pip python3-venv libpq-dev
python3.9 -m venv .venv
source .venv/bin/activate
pip3 install -r requirements.txt
cp .env.example .env
# adjust .env according to your use case
```

For windows, go to python.org to download and install the proper python version. After that:
```commandline
python3.9 -m venv .venv
.venv\Scripts\activate.bat
pip3 install -r requirements.txt
copy .env.example .env
REM adjust .env according to your use case
```

Run splash service:
```commandline
docker-compose up -d
```
Splash creates screenshots from web pages when thumbnails are not available.

There is another service for use at crawl time called "pyppeteer" which is currently not in use by our crawlers.


## Run a crawler
(Activate your virtual environment as in requirements above, if not already done.)
```commandline
scrapy crawl oeh_spider
```

If a crawler has [Scrapy Spider Contracts](https://docs.scrapy.org/en/latest/topics/contracts.html#spiders-contracts) implemented, you can test those by running `scrapy check <spider-name>`

Or using the docker image:
```bash
docker build --tag oeh-search-etl .
./docker_run.sh oeh_spider
```
From the docker image respectively run.py, there are also other options one can execute like H5P upload or sodix permission script.

## Writing a spider/crawler

- We use scrapy, a framework for crawling metadata from the web
- To create a new spider, inside `converter/spiders/`, copy `sample_spider.py` to `<yourname>_spider.py`
- Inherit `LomBase` class in order to get out-of-the-box support for oeh's metadata model
- You may also inherit a base class for crawling data, e.g.
  - `LrmiBase` for crawling LRMI metadata
  - `OAIBase` for OAI interfaces
- Please take a look at the `sample_spider.py` for a template
- To learn more about the LOM standard we're using, you'll find useful information at https://en.wikipedia.org/wiki/Learning_object_metadata
- For more information, have a look into Confluence ("Using OpenEduHub (OEH) spiders")

## Still have questions? Check out our GitHub-Wiki!
If you need help getting started or setting up your work environment, please don't hesitate to visit our GitHub Wiki at https://github.com/openeduhub/oeh-search-etl/wiki
