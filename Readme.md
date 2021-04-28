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

As a last step, set up your config variables by copying the example and modify it if necessary `cp converter/.env.example converter/.env`

- crawler can be run with `scrapy crawl <spider-name>`. It assumes that you have an edu-sharing 6.0 instance in your `.env` settings configured which can accept the data.

## Building a Crawler

- We use Scrapy as a framework. Please check out the guides for Scrapy spider (https://docs.scrapy.org/en/latest/intro/tutorial.html)
- To create a new spider, create a file inside `converter/spiders/<myname>_spider.py`
- We recommend to inherit the `LomBase` class in order to get out-of-the-box support for our metadata model
- You may also Inherit a Base Class for crawling data, if your site provides LRMI metadata, the `LrmiBase` is a good start, if your system provides an OAI interface, you may use the `OAIBase`
- As a sample/template, may check out the `sample_spider.py`
- To learn more about the LOM standard we're using, may checkout https://en.wikipedia.org/wiki/Learning_object_metadata
