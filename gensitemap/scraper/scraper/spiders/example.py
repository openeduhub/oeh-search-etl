import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from urllib.parse import urlparse
import re

from crawls.models import CrawlJob, CrawledURL

class CustomItem(scrapy.Item):
    job_id = scrapy.Field()
    # The url of this item
    url = scrapy.Field()
    # The url that this item was found on
    request_url = scrapy.Field()
    # The url that linked to this page, None if it is the start page
    from_url = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()

class ExampleSpider(scrapy.Spider):
    name = "example"
    #allowed_domains = ["example.com"]
    start_urls = ["https://example.com"]
    # rules = [
    #     Rule(LinkExtractor())
    # ]

    def __init__(self, start_url, follow_links=False, *args, **kwargs):
        super(ExampleSpider, self).__init__(*args, **kwargs)
        self.start_urls = [start_url]
        self.follow_links = to_bool(follow_links)
        self.link_extractor = LinkExtractor()

        crawl_job = CrawlJob.objects.create(start_url=start_url, follow_links=self.follow_links)
        self.crawl_job = crawl_job
        crawl_job.save()


    def parse(self, response: scrapy.http.Response, from_url=None):
        """
            from_url: the url that linked to this page, None if it is the start page
            respose.request.url: the url of this page
        """
        request_origin = get_origin(response.request.url)
        # If these are base urls, scrapy *should* fill in the correct
        # base url (https://weltderphysik.de)
        for link in self.link_extractor.extract_links(response):
            if get_origin(link.url) != request_origin:
                print(f"Skipping {link.url}")
                continue
            item = CustomItem()
            item['job_id'] = self.crawl_job.id
            item['request_url'] = response.request.url
            item['url'] = link.url
            if from_url:
                item['from_url'] = from_url
            yield item
            if self.follow_links:
                yield scrapy.Request(link.url, callback=self.parse, cb_kwargs={'from_url': response.url})
                #yield response.follow(link, self.parse)

        # # find all links on the page that are to the same origin
        # origin = get_origin(response.url)
        # links = response.css('a::attr(href)').extract()



def get_origin(url: str):
    """
    Returns the scheme (http, https), domain and port of a given url.

    >>> get_origin('https://example.com:8080/blah/blub')
    'https://example.com:8080'
    >>> get_origin('blah.com/test')
    'http://blah.com'
    """
    parsed = urlparse(url)
    if parsed.scheme == '':
        parsed = urlparse(f'http://{url}')
    return f"{parsed.scheme}://{parsed.netloc}"


def to_bool(value: str|bool) -> bool:
    if isinstance(value, bool):
        return value
    if value.lower() in ['true', '1']:
        return True
    if value.lower() in ['false', '0']:
        return False
    raise ValueError(f"Cannot convert {value} to boolean")


