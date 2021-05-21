from dataclasses import field, dataclass
from typing import Optional

import scrapy

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


