from datetime import datetime

import xmltodict as xmltodict
from tqdm import tqdm
from lxml import etree
from scrapy.spiders import CrawlSpider
from converter.items import *
import time
from w3lib.html import remove_tags, replace_escape_chars
from converter.spiders.lom_base import LomBase
import json


class MerlinDebuggingSpider(CrawlSpider, LomBase):
    """
    TODO description, add restricted content.
    """
    name = 'merlin_debugging_spider'
    url = 'http://merlin.nibis.de/index.php'  # the url which will be linked as the primary link to your source (should be the main url of your site)
    friendlyName = 'Merlin'  # name as shown in the search ui
    version = '0.1'  # the version of your crawler, used to identify if a reimport is necessary
    apiUrl = 'http://merlin.nibis.de/index.php?action=resultXml&start=%start&anzahl=%anzahl&query[stichwort]=*'     # * regular expression, to represent all possible values.

    limit = 100
    page = 0

    def start_requests(self):
        yield scrapy.Request(url=self.apiUrl.replace('%start', str(self.page * self.limit))
                              .replace('%anzahl', str(self.limit)),
                              callback=self.parse, headers={
                'Accept': 'application/xml',
                'Content-Type': 'application/xml'
            })

    def parse(self, response: scrapy.http.Response):
        print("Parsing URL: " + response.url)

        # We would use .fromstring(response.text) if the response did not include the XML declaration:
        # <?xml version="1.0" encoding="utf-8"?>
        root = etree.XML(response.body)
        tree = etree.ElementTree(root)

        if self.page == 0:
            total_elements = int(tree.xpath('/root/sum')[0].text)
            self.pbar = tqdm(total=(total_elements), desc=self.name + " downloading progress: ")

        # If results were returned.
        elements = tree.xpath('/root/items/*')
        if len(elements) > 0:
            for element in elements:
                self.pbar.update(1)

                start = time.time()
                copyResponse = response.copy()
                element_xml_str = etree.tostring(element, pretty_print=True, encoding='unicode')
                element_dict = xmltodict.parse(element_xml_str)
                finish = time.time()
                print(finish-start, " to parse XML content.")

                # TODO: Ask Arne, as it's probably a pointless attribute.
                #del element_dict["data"]["score"]

                copyResponse.meta['item'] = element_dict["data"]  # Passing the dictionary for easier access to attributes.
                # In case JSON string representation is preferred:
                # copyResponse._set_body(json.dumps(copyResponse.meta['item'], indent=1, ensure_ascii=False))
                copyResponse._set_body(element_xml_str)

                if self.hasChanged(copyResponse):
                    # TODO: What are we exactly supposed to do if this happens?
                    yield self.handleEntry(copyResponse)

                # LomBase.parse() has to be called for every individual instance that needs to be saved to the database.
                LomBase.parse(self, copyResponse)

        # TODO: We do not want to stress the Rest APIs.
        # time.sleep(0.1)

        # If the number of returned results is equal to the imposed limit, it means that there are more to be returned.
        if len(elements) == self.limit:
            self.page += 1
            url = self.get_url(self.limit, self.page)
            yield scrapy.Request(url=url, callback=self.parse)

    def getId(self, response):
        # return response.xpath('/data/id_local/text()').get()
        return response.meta["item"]["id_local"]

    def getHash(self, response):
        """ Since we have no 'last_modified' date from the elements we cannot do something better. """
        # return self.version + str(time.time())
        return self.version + str(datetime.date(datetime.now()))

    def handleEntry(self, response):
        # John: So if the Entry has changed we are just supposed to re-enter it? Why not ignore the "has_changed"
        # altogether?
        return LomBase.parse(self, response)

    def getBase(self, response):
        base = LomBase.getBase(self, response)

        element_dict = response.meta["item"]
        # thumbnail = response.xpath('/data/thumbnail/text()').get()
        # base.add_value('thumbnail', thumbnail)
        base.add_value('thumbnail', element_dict["thumbnail"])

        return base

    def getLOMGeneral(self, response):
        general = LomBase.getLOMGeneral(self, response)
        element_dict = response.meta["item"]
        general.add_value('title', element_dict["titel"])
        # general.add_value('title', response.xpath('/data/titel/text()').get())
        # general.add_value('language', response.xpath('//meta[@property="og:locale"]/@content').get())

        # John: Why is there a description in both general and educational?
        # general.add_value('description', response.xpath('//beschreibung//text()').get())

        # if len(response.xpath('/data/fach/*')) > 0:
        if len(element_dict["fach"]) > 0:
            # element_dict = response.meta["item"]
            general.add_value('keyword', element_dict["fach"].values())

        return general

    def getLOMEducational(self, response):
        educational = LomBase.getLOMEducational(self, response)
        element_dict = response.meta["item"]

        # educational.add_value('description', response.xpath('/data/beschreibung/text()').get())
        # educational.add_value('intendedEndUserRole', response.xpath('/data/bildungsebene/text()').get().split(';'))

        educational.add_value('description', element_dict["beschreibung"])
        educational.add_value('intendedEndUserRole', element_dict["bildungsebene"].split(';'))
        return educational

    def getLOMTechnical(self, response):
        technical = LomBase.getLOMTechnical(self, response)

        element_dict = response.meta["item"]

        # technical.add_value('format', 'application/xml')
        # location = response.xpath('/data/media_url/text()').get()
        # technical.add_value('location', location)
        # technical.add_value('size', len(response.body))

        technical.add_value('format', "application/xml")
        technical.add_value('location', "http://merlin.nibis.de" + element_dict["media_url"])
        technical.add_value('size', len(response.body))
        return technical

    def getValuespaces(self, response):
        valuespaces = LomBase.getValuespaces(self, response)

        element_dict = response.meta["item"]

        # valuespaces.add_value('educationalContext', response.xpath('/data/bildungsebene/text()').get().split(';'))
        valuespaces.add_value('educationalContext', element_dict["bildungsebene"].split(';'))

        # Consider https://vocabs.openeduhub.de/w3id.org/openeduhub/vocabs/learningResourceType/index.html
        # if len(response.xpath('/data/ressource/*')) > 0:
        if len(element_dict["ressource"]) > 0:
            resource_types = element_dict["ressource"].values()

            # Convert non-LOM (not known to OEH) resource types, to LOM resource types.
            merlin_to_oeh_types = {
                "Film": "video",
                "Menü": "menu",
            }
            resource_types = [merlin_to_oeh_types[rt] if rt in merlin_to_oeh_types else rt.lower() for rt in resource_types]

            valuespaces.add_value('learningResourceType', resource_types)
        return valuespaces