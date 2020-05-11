import xmltodict as xmltodict
from tqdm import tqdm
from lxml import etree
from scrapy.spiders import CrawlSpider
from converter.items import *
import time
from w3lib.html import remove_tags, replace_escape_chars
from converter.spiders.lom_base import LomBase
import json


class MerlinSpider(CrawlSpider, LomBase):
    """
    TODO description, add restricted content.
    """
    name = 'merlin_spider'
    url = 'http://merlin.nibis.de/index.php'  # the url which will be linked as the primary link to your source (should be the main url of your site)
    friendlyName = 'Merlin'  # name as shown in the search ui

    limit = 10
    page = 0

    def get_url(self, limit, page):
        """ Generate paginated URL """
        return 'http://merlin.nibis.de/index.php?action=resultXml&start=' + str(page * limit) + \
               '&anzahl=' + str(limit) + \
               '&query[stichwort]=*'  # * as in Regular expressions, to represent all possible values.

    start_urls = [get_url(None, limit, page)]

    version = '0.1'  # the version of your crawler, used to identify if a reimport is necessary

    def parse(self, response: scrapy.http.Response):
        print("Parsing URL: " + response.url)

        # We would use .fromstring(response.text) if the response did not include the XML declaration:
        # <?xml version="1.0" encoding="utf-8"?>
        root = etree.XML(response.body)
        tree = etree.ElementTree(root)

        if self.page == 0:
            total_elements = int(tree.xpath('/root/sum')[0].text)
            # self.pbar = tqdm(total=(total_elements / self.limit) + 1, desc="Downloading content: " + self.name)

        # self.pbar.update(1)

        # If results were returned.
        elements = tree.xpath('/root/items/*')
        if len(elements) > 0:
            for element in elements:
                copyResponse = response.copy()
                element_xml_str = etree.tostring(element, pretty_print=True, encoding='unicode')
                element_dict = xmltodict.parse(element_xml_str)

                # TODO: Ask Arne, as it's probably pointless.
                #del element_dict["data"]["score"]

                # So, what's the point of passing this?
                copyResponse.meta['item'] = element_dict["data"]
                # copyResponse._set_body(json.dumps(copyResponse.meta['item'], indent=1, ensure_ascii=False))
                copyResponse._set_body(element_xml_str)

                if self.hasChanged(copyResponse):
                    # TODO: What are exactly suppose to do if this has happened?
                    yield self.handleEntry(copyResponse)

                # LomBase.parse() has to be called for every individual instance that needs to be saved to the database.
                return LomBase.parse(self, copyResponse)

        # TODO: We do not want to stress the Rest APIs.
        # time.sleep(0.1)

        # If the number of returned results is equal to the imposed limit, it means that there are more to be returned.
        if len(elements) == self.limit:
            self.page += 1
            url = self.get_url(self.limit, self.page)
            yield scrapy.Request(url=url, callback=self.parse)

    def getId(self, response):
        return response.xpath('/data/id_local/text()').get()

    def getHash(self, response):
        """ Since we have no 'last_modified' date from the elements we cannot do something better. """
        return self.version + str(time.time())

    def handleEntry(self, response):
        # John: So if the Entry has changed we are just supposed to re-enter it? Why not ignore the "has_changed"
        # altogether?
        return LomBase.parse(self, response)

    def getBase(self, response):
        base = LomBase.getBase(self, response)

        # There exists also an animated thumbnail.
        base.replace_value('thumbnail', response.xpath('/data/thumbnail/text()').get())
        # John: This is not information we have for Merlin.
        #1.   base.replace_value('type', self.getType(response))
        #2.   fulltext = self.get('acf.long_text', json = response.meta['item'])
        #     base.replace_value('fulltext', HTMLParser().unescape(fulltext))  # Likewise.
        #3.   base.add_value('lastModified', response.xpath('//thumbnail//text()').get())  # Likewise
        return base

    def getLOMGeneral(self, response):
        general = LomBase.getLOMGeneral(self, response)
        general.add_value('title', response.xpath('/data/titel/text()').get())
        # general.add_value('language', response.xpath('//meta[@property="og:locale"]/@content').get())

        # John: Why is there a description in both general and educational?
        # general.add_value('description', response.xpath('//beschreibung//text()').get())

        if len(response.xpath('//fach//*')) > 0:
            element_dict = response.meta["item"]
            general.add_value('keywords', element_dict["fach"].values())

        return general

    def getLOMEducational(self, response):
        educational = LomBase.getLOMEducational(self, response)
        educational.add_value('description', response.xpath('/data/beschreibung/text()').get())
        # educational.add_value('description', "Example description")
        return educational

    def getLOMTechnical(self, response):
        technical = LomBase.getLOMTechnical(self, response)

        # TODO: Why replace_value() and not add_value()?

        # John: It is not HTML though. Am I wrong? Should we consider XML as HTML regardless?
        technical.replace_value('format', 'text/html')

        technical.replace_value('location', response.url)
        technical.replace_value('size', len(response.body))
        return technical

    def getValuespaces(self, response):
        valuespaces = LomBase.getValuespaces(self, response)
        # Provide valuespace data. This data will later get automatically mapped
        # Please take a look at the valuespaces here:
        # https://vocabs.openeduhub.de/
        # You can either use full identifiers or also labels. The system will auto-map them accordingly

        # Please also checkout the ValuespaceHelper class which provides usefull mappers for common data

        # valuespaces.add_value('educationalContext', context)
        # valuespaces.add_value('discipline',discipline)
        # valuespaces.add_value('learningResourceType', lrt)
        return valuespaces

    # You may override more functions here, please checkout LomBase class