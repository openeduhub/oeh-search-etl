import json
import os
import ssl
import time
import urllib
import urllib.request
from urllib.parse import urlencode, urlparse

import requests
import scrapy
import xmltodict
from lxml import etree
from scrapy.spiders import CrawlSpider

# TODO: find a better solution.
import ssl
ssl._create_default_https_context = ssl._create_unverified_context


def encode_url_for_local(url):
    return url[:url.find("?action")] + urllib.parse.quote(url[url.find("?action"):])

class MediothekPixiothekSpiderOffline(CrawlSpider):
    name = 'mediothek_pixiothek_spider_offline'
    url = 'https://www.schulportal-thueringen.de/'  # the url which will be linked as the primary link to your source (should be the main url of your site)
    friendlyName = 'MediothekPixiothek'  # name as shown in the search ui
    version = '0.1'  # the version of your crawler, used to identify if a reimport is necessary
    # start_urls = ['https://www.schulportal-thueringen.de/tip-ms/api/public_mediothek_metadatenexport/publicMediendatei']
    start_urls = ['file:///data/projects/schul_cloud/workspace/content_sources/mediothek_pixiothek/cache/tip-ms/api/public_mediothek_metadatenexport/publicMediendatei']


    limit = 100
    page = 0

    elements_count = 0

    data_dir = "/data/projects/schul_cloud/workspace/content_sources/mediothek_pixiothek/cache"

    thumbnails_dir = data_dir + "/thumbnails"

    def __init__(self, *a, **kwargs):
        # LomBase.__init__(self, **kwargs)
        super().__init__(*a, **kwargs)

    def encode_url_for_local(self, url):
        return url[:url.find("?action")] + urllib.parse.quote(url[url.find("?action"):])

    def parse(self, response: scrapy.http.Response):
        # Avoid stressing the API.
        # time.sleep(0.5)
        print(response.url)

        text_response = response.body

        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
        if not os.path.exists(self.thumbnails_dir):
            os.makedirs(self.thumbnails_dir)

        self.save_json_array_data(text_response)

        elements = json.loads(response.body_as_unicode())
        for i, element in enumerate(elements):
            if "previewImageUrl" in element:
                time.sleep(0.5)
                self.store_thumbnails(element['previewImageUrl'])


    def save_json_array_data(self, text_response):
        # Save the JSON array data file.
        resource_path = "/tip-ms/api/public_mediothek_metadatenexport/publicMediendatei"
        # Create the subdirectories
        directories = self.data_dir + "/tip-ms/api/public_mediothek_metadatenexport"
        if not os.path.exists(directories):
            os.makedirs(directories)
        with open(self.data_dir + resource_path, "wb") as fout:
            fout.write(text_response)

    def store_thumbnails(self, thumbnail_url):
        urlparse_result = urlparse(thumbnail_url)
        thumbnail_path = urlparse_result.path
        if urlparse_result.query != "":
            thumbnail_path += "&" + urlparse_result.query

        # Create the subdirectories
        directories = self.thumbnails_dir + os.path.dirname(os.path.abspath(thumbnail_path))
        if not os.path.exists(directories):
            os.makedirs(directories)

        local_path = self.thumbnails_dir + thumbnail_path

        if not os.path.exists(local_path):
            # urllib.request.urlretrieve(thumbnail_url, local_path)
            self.download_and_save_image(thumbnail_url, local_path)

    def download_and_save_image(self, pic_url, local_path):
        with open(local_path, 'wb') as handle:
            response = requests.get(pic_url, stream=True, allow_redirects=True)

            if not response.ok:
                print(response)

            for block in response.iter_content(1024):
                if not block:
                    break

                handle.write(block)