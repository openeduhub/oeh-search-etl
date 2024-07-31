# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
#from crawls.models import Craw
from scrapy.spiders import Spider
from scrapy.item import Item

from crawls.models import CrawledURL, CrawlJob

from asgiref.sync import sync_to_async

class ScraperPipeline:
    @sync_to_async
    def process_item(self, item: Item, spider: Spider):
        request_url = item['request_url']
        url = item['url']

        job = CrawlJob.objects.get(id=item['job_id'])
        crawled_url = CrawledURL.objects.create(crawl_job=job, url=url)
        crawled_url.save()
        

