from dataclasses import field, dataclass
from typing import Optional

import scrapy

import os
import subprocess
from trafilatura import sitemaps, feeds
from ..web_tools import ignored_file_extensions

namespaces = {
    'sm': 'http://www.sitemaps.org/schemas/sitemap/0.9',
    'image': 'http://www.google.com/schemas/sitemap-image/1.1',
    'mobile': 'http://www.google.com/schemas/sitemap-mobile/1.0"'
}


def from_xml_response(response: scrapy.http.XmlResponse):
    for prefix, uri in namespaces.items():
        response.selector.register_namespace(prefix, uri)
    urls: scrapy.selector.SelectorList = response.selector.xpath('/sm:urlset/sm:url')
    for url in urls:
        yield SitemapEntry.from_xpath(url)


@dataclass
class SitemapImage:
    loc: str
    caption: Optional[str] = None
    geo_location: Optional[str] = None
    title: Optional[str] = None
    license: Optional[str] = None

    @classmethod
    def from_xpath(cls, image: scrapy.selector.Selector) -> 'SitemapImage':
        payload = dict()
        for _field in ('loc', 'caption', 'geo_location', 'title', 'license'):
            if text := image.xpath(f'image:{_field}/text()').get():
                payload[_field] = text
        return SitemapImage(**payload)


@dataclass
class SitemapEntry:
    loc: str
    lastmod: Optional[str] = None
    changefreq: Optional[str] = None
    priority: Optional[str] = None
    images: list[SitemapImage] = field(default_factory=list)

    @classmethod
    def from_xpath(cls, url: scrapy.selector.Selector) -> 'SitemapEntry':
        payload = dict()
        for _field in ('loc', 'lastmod', 'changefreq', 'priority'):
            if text := url.xpath(f'sm:{_field}/text()').get():
                payload[_field] = text
        if images := [SitemapImage.from_xpath(i) for i in url.xpath('image:image')]:
            payload['images'] = images
        return SitemapEntry(**payload)

def find_generate_sitemap(url, max_entries = 5):
    sitemap_list = sitemaps.sitemap_search(url, target_lang='de')
    feeds_list = feeds.find_feed_urls(url)

    sitemap_set = set(sitemap_list)
    feeds_set = set(feeds_list)
    all_urls_set = sitemap_set.union(feeds_set)
    all_urls = list(all_urls_set)
    if len(all_urls) == 0:
        all_urls = generate_sitemap(url, max_entries)

    ignore_urls = []
    for url in all_urls:
        for file_extension in ignored_file_extensions:
            if url.endswith(file_extension):
                ignore_urls.append(url)
                break
    ignore_urls_set = set(ignore_urls)
    all_urls_set = set(all_urls)
    valid_urls = list(all_urls_set.difference(ignore_urls_set))
    return valid_urls[:max_entries]

def generate_sitemap(url, max_entries):
    DEVNULL = open(os.devnull, 'wb')
    try:
        bytes_result = subprocess.check_output([f'npx',
                                                'sitemap-generator-cli',
                                                '--max-depth',
                                                '2',
                                                '--max-entries',
                                                str(max_entries),
                                                '--verbose',
                                                url,
                                                '>>',
                                                'sitemap.txt'],
                                               stderr=DEVNULL)
        str_result = bytes_result.decode('utf-8')
        str_result = str_result.replace('[ ADD ] ', '')
        str_result = str_result.replace('\n', ',')
        if str_result.index('Added ') == 0:
            return []
        else:
            str_result = str_result[:str_result.index(',Added ')]
        urls = str_result.split(",")
        return urls
    except (subprocess.CalledProcessError, Exception) as e:
        print("Error generating sitemap:", e)
        return []
