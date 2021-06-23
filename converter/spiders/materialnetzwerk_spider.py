import json
from typing import Optional

import scrapy.http
from scrapy.spiders import CrawlSpider

from converter.constants import Constants
from converter.items import BaseItemLoader, LomBaseItemloader, LomGeneralItemloader, LomTechnicalItemLoader, \
    LomLifecycleItemloader, LomEducationalItemLoader, ValuespaceItemLoader, LicenseItemLoader, ResponseItemLoader
from converter.spiders.base_classes import LomBase


class MaterialNetzwerkSpider(CrawlSpider, LomBase):
    name = "materialnetzwerk_spider"
    friendlyName = "Materialnetzwerk.org"
    version = "0.0.1"
    start_urls = [
        # 'https://editor.mnweg.org/?p=1&materialType=bundle',
        # this doesn't list any materials since they're loaded dynamically
        # response.xpath('/html/body/main/main/div[2]/div').get() shows items in the browser,
        # but only returns "Keine Sammlungen gefunden" with API REST clients or Scrapy
        'https://editor.mnweg.org/api/v1/share/bundle?groupSlug=mnw&page=0&pageSize=10000&q'
        # this API doesn't help either because while we get titles and really basic metadata here, there's no links
        # to follow and no material locations besides unique ids, it's not a public API for gathering, but rather
        # inward-facing
    ]
    custom_settings = {
        'ROBOTSTXT_OBEY': False
    }
    discipline_mapping = {
        'AES': 'http://w3id.org/openeduhub/vocabs/discipline/04006',  # Ernährung und Hauswirtschaft
        'Biologie': 'http://w3id.org/openeduhub/vocabs/discipline/080',  # Biologie
        'Deutsch': 'http://w3id.org/openeduhub/vocabs/discipline/120',  # Deutsch
        'Erdkunde': 'http://w3id.org/openeduhub/vocabs/discipline/220',  # Geografie
        'English': 'http://w3id.org/openeduhub/vocabs/discipline/20001',  # Englisch
        'Mathematik': 'http://w3id.org/openeduhub/vocabs/discipline/380',  # Mathematik
    }
    # debug_disciplines = set()

    def __init__(self, **kwargs):
        CrawlSpider.__init__(self, **kwargs)

    def getId(self, response=None) -> Optional[str]:
        pass

    def getHash(self, response=None) -> Optional[str]:
        pass

    def start_requests(self):
        for start_url in self.start_urls:
            yield scrapy.Request(url=start_url, callback=self.parse_start_url)

    def parse_start_url(self, response: scrapy.http.Response, **kwargs):
        api_response = json.loads(response.body)
        amount_of_bundles = api_response["total"]
        # print("Total amount of material bundles to crawl:", amount_of_bundles, type(amount_of_bundles))
        # the API returns a list of bundles and within each bundle object is a "slug"-key, whose value is part of the
        # unique URL that we need to parse later
        bundle_urls = list()
        for item in api_response["bundles"]:
            current_url = "https://editor.mnweg.org/mnw/sammlung/" + item["slug"]
            bundle_urls.append(current_url)
            yield scrapy.Request(url=current_url, callback=self.parse_bundle_overview)

        # for debugging only, to check if the urls are valid (and which urls were gathered)
        # bundle_urls.sort()
        # print(bundle_urls)

    def parse_bundle_overview(self, response: scrapy.http.Response):
        # a typical bundle_overview looks like this: https://editor.mnweg.org/mnw/sammlung/das-menschliche-skelett-m-78
        # there's minimal metadata to be found, but we can grab the descriptions of each worksheet and use the
        # accumulated strings as our description for the bundle page
        bundle_title = response.xpath('//div[@class="l-container content"]/h2/text()').get()
        bundle_description = response.xpath('/html/head/meta[@property="description"]/@content').get()
        # div class tutoryMark holds the same content as the description in the header
        # bundle_tutory_mark = response.xpath('//div[@class="tutoryMark"]/text()').getall()

        meta_values_fach = response.xpath('//dl[@class="metaValues"]/dt[1]/text()').get()
        bundle_discipline = str()
        education_level = list()
        if meta_values_fach == "Fach":
            meta_values_fach_value = response.xpath('//dl[@class="metaValues"]/dd[1]/text()').get()
            if meta_values_fach_value is not None:
                # self.debug_disciplines.add(meta_values_fach_value)
                bundle_discipline = meta_values_fach_value
        # "phase" is their term for "Klassenstufe"
        meta_values_phase = response.xpath('//dl[@class="metaValues"]/dt[2]/text()').get()
        if meta_values_phase == "Phase":
            meta_values_phase_value = response.xpath('//dl[@class="metaValues"]/dd[2]/text()').get()
            edu_level_temp = meta_values_phase_value.replace(" ", "")  # stripping empty spaces between the comma
            education_level = edu_level_temp.split(',')  # these values will be used for educationLevel
        # materialnetzwerk lists 3 "Niveaustufen": M, R, E
        # meta_values_niveaustufe = response.xpath('//dl[@class="metaValues"]/dt[3]/text()').get()
        # if meta_values_niveaustufe == "Niveaustufe":
        #     meta_values_niveaustufe_value = response.xpath('//dl[@class="metaValues"]/dd[3]/text()').get()

        # all worksheets that belong to the current url are listed within
        # /html/body/main/div/ul
        worksheet_descriptions = list()
        for worksheet in response.xpath('//a[@class="worksheet"]'):
            material_form_description = worksheet.xpath('label/span[@class="meta-materialFormShort"]/text()').get()
            if material_form_description is not None:
                worksheet_descriptions.append(material_form_description + " ")
            material_meta_name = worksheet.xpath('label/span[@class="meta-name"]/text()').get()
            if material_meta_name is not None:
                worksheet_descriptions.append(material_meta_name)
            worksheet_descriptions.append("\n")
            # TODO: use worksheet_url once we can link it to the bundle in our metadata model
            # worksheet_url = worksheet.xpath('@href').get()
        # print(worksheet_descriptions)
        worksheet_description_string: str = ''.join(worksheet_descriptions)

        # debug output to check if there are new disciplines that still need to be mapped:
        # debug_disciplines_sorted = list(self.debug_disciplines)
        # debug_disciplines_sorted.sort()

        # There are two "application/ld+json"-scripts on the website -> XPath: /html/body/script[1]
        # one is of @type Organization, the other of @type LocalBusiness
        # ld_json_string = response.xpath('/html/body/script[@type="application/ld+json"]/text()').get().strip()
        ld_json_organization = dict()
        ld_json_local_business = dict()
        for ld_json_block in response.xpath('/html/body/script[@type="application/ld+json"]/text()'):
            ld_json_string = ld_json_block.get().strip()
            ld_json_temp = json.loads(ld_json_string)
            if ld_json_temp.get("@type") == "Organization":
                ld_json_organization = json.loads(ld_json_string)
            elif ld_json_temp.get("@type") == "LocalBusiness":
                ld_json_local_business = json.loads(ld_json_string)

        # the publication date is only available on the individual worksheet page, but it seems like the individual
        # pages of a bundle are all carrying the same date, therefore it should be enough to only parse the first
        # worksheet (and reduce load on the website)
        first_worksheet_url = response.xpath('//a[@class="worksheet"]/@href').get()
        first_worksheet_thumbnail = response.xpath('/html/body/main/div/ul/a[1]/div[1]/img/@data-src').get()
        # there isn't a lot of metadata available on the bundle overview page, but we still need to carry it over to
        # the parse method since that's where the BaseItemLoader is built
        bundle_dict = {
            'bundle_title': bundle_title,
            'bundle_description': bundle_description,
            'bundle_url': response.url,
            'worksheet_description_summary': worksheet_description_string,
            'bundle_discipline': bundle_discipline,
            'bundle_education_level': education_level,
            'bundle_ld_json_organization': ld_json_organization,
            'bundle_ld_json_local_business': ld_json_local_business,
            'bundle_thumbnail': first_worksheet_thumbnail
        }
        if first_worksheet_url is not None:
            yield scrapy.Request(url=first_worksheet_url, callback=self.parse, cb_kwargs=bundle_dict)
        # print(debug_disciplines_sorted)
        pass

    def parse(self, response: scrapy.http.Response, **kwargs):
        # since we're only parsing the first worksheet for some additional metadata, the metadata object will be
        # centered around a bundle, not the individual pages

        # print("DEBUG parse_worksheet_page", response.url)
        date_published = response.xpath('//div[@class="meta"]/ul/li[3]/text()').get()

        base = BaseItemLoader()
        base.add_value("sourceId", kwargs.get('bundle_url'))
        hash_temp = str(date_published + self.version)
        base.add_value("hash", hash_temp)
        # this is a hacky solution: the thumbnail is the miniature preview of the bundle's first worksheet
        bundle_thumbnail = kwargs.get('bundle_thumbnail')
        if bundle_thumbnail is not None:
            base.add_value('thumbnail', bundle_thumbnail)
        base.add_value('type', Constants.TYPE_MATERIAL)
        base.add_value('lastModified', date_published)

        lom = LomBaseItemloader()
        general = LomGeneralItemloader()
        general.add_value('title', kwargs.get('bundle_title'))

        description_temp = str()
        bundle_desc_temp = kwargs.get('bundle_description')
        worksheet_desc_temp = kwargs.get('worksheet_description_summary')
        # not every bundle has a description, but there's always worksheet descriptions available:
        if bundle_desc_temp is not None:
            description_temp: str = bundle_desc_temp + "\n\n" + worksheet_desc_temp
        elif bundle_desc_temp is None and worksheet_desc_temp is not None:
            description_temp: str = worksheet_desc_temp
        # print(description_temp)
        general.add_value('description', description_temp)
        general.add_value('language', 'de')
        general.add_value('identifier', kwargs.get('bundle_url'))
        lom.add_value('general', general.load_item())

        technical = LomTechnicalItemLoader()
        technical.add_value("format", "text/html")
        technical.add_value('location', kwargs.get('bundle_url'))
        lom.add_value('technical', technical.load_item())

        lifecycle = LomLifecycleItemloader()
        bundle_organization = kwargs.get('bundle_ld_json_organization')
        if bundle_organization is not None:
            lifecycle.add_value('organization', bundle_organization)
        lifecycle.add_value('date', date_published)
        lom.add_value('lifecycle', lifecycle.load_item())

        educational = LomEducationalItemLoader()
        # TODO: educationalLevel is currently unsupported in the items.py backend?
        educational_level = kwargs.get('bundle_educational_level')
        if educational_level is not None:
            educational.add_value('educationalLevel', educational_level)
        lom.add_value('educational', educational.load_item())
        base.add_value('lom', lom.load_item())

        vs = ValuespaceItemLoader()
        vs.add_value('learningResourceType', 'http://w3id.org/openeduhub/vocabs/learningResourceType/teaching_module')
        bundle_discipline = kwargs.get('bundle_discipline')
        if bundle_discipline is not None:
            bundle_discipline = self.discipline_mapping.get(bundle_discipline)
            vs.add_value('discipline', bundle_discipline)
        vs.add_value('intendedEndUserRole', 'http://w3id.org/openeduhub/vocabs/intendedEndUserRole/teacher')
        #  logged in users can manipulate the worksheets and fit them to their needs,
        #  but there's no login required for just downloading the pdf of an available worksheet
        vs.add_value('conditionsOfAccess',
                     'http://w3id.org/openeduhub/vocabs/conditionsOfAccess/login_for_additional_features')
        vs.add_value('price', 'http://w3id.org/openeduhub/vocabs/price/no')

        lic = LicenseItemLoader()
        # everything is CC-BY-SA 3.0 according to the FAQs: https://mnweg.org/faqs
        lic.add_value('url', Constants.LICENSE_CC_BY_SA_30)
        base.add_value('license', lic.load_item())

        response_loader = ResponseItemLoader()
        response_loader.add_value('url', kwargs.get('bundle_url'))

        base.add_value('valuespaces', vs.load_item())
        base.add_value('response', response_loader.load_item())

        yield base.load_item()
