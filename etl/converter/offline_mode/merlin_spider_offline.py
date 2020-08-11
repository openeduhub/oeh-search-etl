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

class MerlinSpiderOffline(CrawlSpider):
    name = 'merlin_spider_offline'
    domain = 'https://merlin.nibis.de'
    url = 'https://merlin.nibis.de/index.php'  # the url which will be linked as the primary link to your source (should be the main url of your site)
    friendlyName = 'Merlin'  # name as shown in the search ui
    version = '0.1'  # the version of your crawler, used to identify if a reimport is necessary
    apiUrl = 'https://merlin.nibis.de/index.php?action=resultXml&start=%start&anzahl=%anzahl&query[stichwort]=*'  # * regular expression, to represent all possible values.

    limit = 100
    page = 0

    elements_count = 0

    data_dir = "/data/projects/schul_cloud/workspace/content_sources/merlin/cache"

    thumbnails_dir = data_dir + "/thumbnails"

    def __init__(self, *a, **kwargs):
        # LomBase.__init__(self, **kwargs)
        super().__init__(*a, **kwargs)

    def encode_url_for_local(self, url):
        return url[:url.find("?action")] + urllib.parse.quote(url[url.find("?action"):])

    def start_requests(self):
        response = 1
        while response is not None:
            yield scrapy.Request(url=self.apiUrl.replace('%start', str(self.page * self.limit))
                                      .replace('%anzahl', str(self.limit)),
                                      callback=self.parse_offline, headers={
                        'Accept': 'application/xml',
                        'Content-Type': 'application/xml'
                    })


    def parse_offline(self, response: scrapy.http.Response):
        # Avoid stressing the API.
        # time.sleep(0.5)
        print(response.url)

        text_response = response.body

        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
        if not os.path.exists(self.thumbnails_dir):
            os.makedirs(self.thumbnails_dir)



        resource_path = response.url.replace("https://merlin.nibis.de/", "")

        with open(self.data_dir + "/" + resource_path, "wb") as fout:
            fout.write(text_response)

        # We would use .fromstring(response.text) if the response did not include the XML declaration:
        # <?xml version="1.0" encoding="utf-8"?>
        root = etree.XML(response.body)
        tree = etree.ElementTree(root)

        # Get the total number of possible elements
        elements_total = int(tree.xpath('/root/sum')[0].text)

        # If results are returned.
        elements = tree.xpath('/root/items/*')

        self.elements_count += len(elements)

        if len(elements) > 0:
            for element in elements:
                time.sleep(0.5)
                # copyResponse = response.copy()

                element_xml_str = etree.tostring(element, pretty_print=True, encoding='unicode')
                element_dict = xmltodict.parse(element_xml_str)["data"]

                if "thumbnail" in element_dict:
                    self.store_thumbnails(element_dict["thumbnail"])
                    self.store_thumbnails(self.domain + element_dict["srcLogoUrl"])
                    # self.store_thumbnails(self.domain + element_dict["logo"])


        # If the number of returned results is equal to the imposed limit, it means that there are more to be returned.
        # if len(elements) == self.limit:
        if self.elements_count < elements_total:
            self.page += 1
            url = self.apiUrl.replace('%start', str(self.page * self.limit)).replace('%anzahl', str(self.limit))
            yield scrapy.Request(url=url, callback=self.parse_offline, headers={
                'Accept': 'application/xml',
                'Content-Type': 'application/xml'
            })


    def store_thumbnails(self, thumbnail_url):

        urlparse_result = urlparse(thumbnail_url)
        thumbnail_path = urlparse_result.path
        if urlparse_result.query != "":
            thumbnail_path += "&" + urlparse_result.query

        # Create the subdirectories
        directories = self.thumbnails_dir + os.path.dirname(os.path.abspath(thumbnail_path))
        if not os.path.exists(directories):
            os.makedirs(directories)

        # local_path = self.thumbnails_dir + thumbnail_url.replace("https://thumbnails.merlin.nibis.de/", "")
        local_path = self.thumbnails_dir + thumbnail_path

        if not os.path.exists(local_path):
            # urllib.request.urlretrieve(thumbnail_url, local_path)
            self.download_and_save_image(thumbnail_url, local_path)


    def download_and_save_image(self, pic_url, local_path):
        with open(local_path, 'wb') as handle:
            response = requests.get(pic_url, stream=True)

            if not response.ok:
                print(response)

            for block in response.iter_content(1024):
                if not block:
                    break

                handle.write(block)