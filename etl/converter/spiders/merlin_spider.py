import xmltodict as xmltodict
from tqdm import tqdm
from lxml import etree
from scrapy.spiders import CrawlSpider
from converter.items import *
import time
from w3lib.html import remove_tags, replace_escape_chars
from converter.spiders.lom_base import LomBase;
import json


# Sample Spider, using a SitemapSpider to crawl your web page
# Can be used as a template for your custom spider
class MerlinSpider(CrawlSpider, LomBase):
    name = 'merlin_spider'
    url = 'http://merlin.nibis.de/index.php'  # the url which will be linked as the primary link to your source (should be the main url of your site)
    friendlyName = 'Merlin'  # name as shown in the search ui

    limit = 100
    page = 0

    def get_url(self, limit, page):
        return 'http://merlin.nibis.de/index.php?action=resultXml&start=' + str(page * limit) + \
               '&anzahl=' + str(limit) + \
               '&query[stichwort]=*'  # * as in Regular expressions, to represent all possible values.

    start_urls = [get_url(None, limit, page)]
    # start_urls = ['https://edu-sharing.com']

    version = '0.1'  # the version of your crawler, used to identify if a reimport is necessary

    def parse(self, response: scrapy.http.Response):
        # John: I think this parse has to be done for every single (individual) element.
        #return LomBase.parse(self, response)
        # We would use .fromstring(response.text) if the response did not include the XML declaration:
        # <?xml version="1.0" encoding="utf-8"?>
        root = etree.XML(response.body)
        tree = etree.ElementTree(root)

        if self.page == 0:
            total_elements = int(tree.xpath('/root/sum')[0].text)
            # self.pbar = tqdm(total=(total_elements / self.limit) + 1, desc="Downloading content: " + self.name)

        # self.pbar.update(1)

        if len(tree.xpath('/root/items/*')) > 0:
            instances = self.xml_tree_to_instances_list(tree)

            # for instance in instances:
            instance = instances[0]

            rsp = response.copy()
            # rsp = rsp.replace("body", instance)
            # rsp = rsp.replace("body", etree.tostring(instance, pretty_print=True, encoding='unicode'))
            xml_str = etree.tostring(instance, pretty_print=True, encoding='unicode')
            xml_str = xml_str.encode('utf-8')
            rsp._set_body(xml_str)
            return LomBase.parse(self, rsp)

        # # We do not want to stress the Rest APIs.
        # # time.sleep(0.1)
        #
        # # If the number of returned results is equal to the imposed limit, it means that there are more to be returned.
        # if len(tree.xpath('/root/items/*')) == self.limit:
        #     self.page += 1
        #     url = self.get_url(self.limit, self.page)
        #     print("new URL: " + url)
        #
        #     # If we have cached the following response, there is no need to redo the call.
        #     next_tree = self.import_from_disk(url)
        #     while next_tree is not None:
        #         self.pbar.update(1)
        #         self.page += 1
        #         url = self.get_url(self.limit, self.page)
        #         print("new URL: " + url)
        #         next_tree = self.import_from_disk(url)
        #     yield scrapy.Request(url=url, callback=self.parse)

    def xml_tree_to_instances_list(self, tree):
        """
        Converting an instance of XML tree to a list of tuples: [(ID:str, json representation:str)]

        :param tree:
        :return:
        """
        instances = []
        for item in tree.xpath('/root/items/*'):
            """ 
            Convert to JSON: XML -> XML string -> Python dictionary -> [Pretty printed] JSON string
            """
            # item_xml_str = etree.tostring(item, pretty_print=True, encoding='unicode')


            # item_dict = xmltodict.parse(item_xml_str)
            # # TODO: Add further attributes? e.g., content_source, date_imported, and so on.
            #
            # # indent=1 for pretty printing, ensure_ascii=False to keep umlauts etc.
            # item_json_str = json.dumps(item_dict, indent=1, ensure_ascii=False)
            # id = item_dict["data"]["id_local"]

            # instances.append((id, item_json_str))
            instances.append(item)
        return instances

    # return a (stable) id of the source
    def getId(self, response):
        return response.xpath('//data//id_local//text()').get()
        # return response.xpath('//id_local//text()').get()

    # return a stable hash to detect content changes
    # if there is no hash available, may use the current time as "always changing" info
    # Please include your crawler version as well
    def getHash(self, response):
        return self.version + str(time.time())

    def getBase(self, response):
        base = LomBase.getBase(self, response)
        # optionlly provide thumbnail. If empty, it will tried to be generated from the getLOMTechnical 'location' (if format is 'text/html')
        # base.add_value('thumbnail', 'https://url/to/thumbnail')
        return base

    def getLOMGeneral(self, response):
        general = LomBase.getLOMGeneral(self, response)
        general.add_value('title', response.xpath('//data//titel//text()').get())
        general.add_value('language', response.xpath('//meta[@property="og:locale"]/@content').get())

        # general.add_value('description', response.xpath('//data//beschreibung//text()').get())
        # general.add_value('keywords', 'TODO_REPLACE')

        return general

    def getLOMEducational(self, response):
        educational = LomBase.getLOMEducational(self, response)
        educational.add_value('description', response.xpath('//data//beschreibung//text()').get())
        return educational
    

    # def getLOMTechnical(self, response):
    #     technical = LomBase.getLOMTechnical(self, response)
    #     technical.add_value('location', response.url)
    #     technical.add_value('format', 'text/html')
    #     technical.add_value('size', len(response.body))
    #     return technical
    def getLOMTechnical(self, response):
        technical = LomBase.getLOMTechnical(self, response)
        technical.replace_value('format', 'text/html')
        technical.replace_value('location', response.url)
        return technical

    # def getLOMGeneral(self, response):
    #     general = LomBase.getLOMGeneral(self, response)
    #     general.add_value('title', response.xpath('//data//titel//text()').get())
    #     general.add_value('language', response.xpath('//meta[@property="og:locale"]/@content').get())
    #     return general

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