import json
from typing import Optional

import scrapy.http
from scrapy.spiders import CrawlSpider

from converter.constants import Constants
from converter.items import BaseItemLoader, LomBaseItemloader, LomGeneralItemloader, LomTechnicalItemLoader, \
    LomLifecycleItemloader, LomEducationalItemLoader, ValuespaceItemLoader, LicenseItemLoader, ResponseItemLoader, \
    LomClassificationItemLoader
from converter.spiders.base_classes import LomBase
from converter.web_tools import WebTools, WebEngine


class MaterialNetzwerkSpider(CrawlSpider, LomBase):
    name = "materialnetzwerk_spider"
    friendlyName = "Materialnetzwerk.org"
    version = "0.0.7"  # last update: 2022-08-16
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
        'CONCURRENT_REQUESTS': 32,
        'CONCURRENT_REQUESTS_PER_DOMAIN': 12,
        # 'AUTOTHROTTLE_ENABLED': True,
        # 'AUTOTHROTTLE_DEBUG': True,
        # 'AUTOTHROTTLE_START_DELAY': 0.25,
        # 'AUTOTHROTTLE_MAX_DELAY': 5,
        # 'AUTOTHROTTLE_TARGET_CONCURRENCY': 2,
        'RETRY_TIMES_3': 3,
        'RETRY_PRIORITY_ADJUST': 1,
    }
    discipline_mapping = {
        'AES': "Ernährung und Hauswirtschaft",  # Ernährung und Hauswirtschaft
        'Erdkunde, Gemeinschaftskunde, Geschichte': ['Erdkunde', 'Gesellschaftskunde', 'Sozialkunde', 'Geschichte'],
        # Gemeinschaftskunde can be either "Gesellschaftskunde" or "Sozialkunde" (depending on the county)
        'Erdkunde': "Geography",  # mapping "Erdkunde" shouldn't be necessary, but the Vocab's altLabel for this entry
        # needs a bugfix.
        # ToDo: remove this workaround/hotfix in v0.0.8 and see if "Erdkunde" gets properly mapped by the pipeline
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
        """
        Parses the API for all available bundles and yields exactly one scrapy.Request per bundle-overview-page for
        further metadata extraction (with a callback to the parse_bundle_overview()-method).

        Spider Contracts:
        @url https://editor.mnweg.org/api/v1/share/bundle?groupSlug=mnw&page=0&pageSize=10000&q
        @returns requests 48

        :param response: scrapy.http.Response
        :return: scrapy.Request
        """
        api_response = json.loads(response.body)
        # amount_of_bundles = api_response["total"]
        # print("Total amount of material bundles to crawl:", amount_of_bundles, type(amount_of_bundles))
        # the API returns a list of bundles and within each bundle object is a "slug"-key, whose value is part of the
        # unique URL that we need to parse later
        bundle_urls = list()
        for item in api_response["bundles"]:
            current_url = "https://editor.mnweg.org/mnw/sammlung/" + item["slug"]
            bundle_urls.append(current_url)
            yield scrapy.Request(url=current_url, callback=self.parse_bundle_overview)

    async def parse_bundle_overview(self, response: scrapy.http.Response):
        """

        Spider Contracts:
        @url https://editor.mnweg.org/mnw/sammlung/das-menschliche-skelett-m-78
        @returns requests 1

        :param response: scrapy.http.Response
        :return: yields a scrapy.Request for the first worksheet
        """

        bundle_dict = dict()
        bundle_dict["bundle_url"] = response.url
        # render the web page to execute js and copy to the response
        body = await WebTools.getUrlData(response.url, WebEngine.Playwright)
        response = response.replace(body=body['html'])

        # a typical bundle_overview looks like this: https://editor.mnweg.org/mnw/sammlung/das-menschliche-skelett-m-78
        # there's minimal metadata to be found, but we can grab the descriptions of each worksheet and use the
        # accumulated strings as our description for the bundle page
        bundle_title = response.xpath('//*[@class="l-container content"]/header/h2/text()').get()
        if bundle_title is None:
            # if we can't get the (clean) title, we need to grab the title from the header and clean it up manually
            bundle_title: str = response.xpath('//head/meta[@property="og:title"]/@content').get()
            if bundle_title.endswith("  — mnweg.org"):
                bundle_title = bundle_title.replace("— mnweg.org", "").strip()
        bundle_dict["bundle_title"] = bundle_title
        bundle_dict["bundle_description"] = response.xpath('//head/meta[@property="description"]/@content').get()
        # div class tutoryMark holds the same content as the description in the header
        # bundle_tutory_mark = response.xpath('//div[@class="tutoryMark"]/text()').getall()

        # there are some basic metadata values in a "metaValues" container, keys differ from topic to topic
        # keys could be: "Fach", "Kompetenzbereich", "Phase" or "Niveaustufe"
        mv_keys = response.xpath('//dl[@class="metaValues"]/dt/text()').getall()
        mv_values = response.xpath('//dl[@class="metaValues"]/dd/text()').getall()
        meta_values_dict = dict(zip(mv_keys, mv_values))

        if "Fach" in meta_values_dict:
            meta_values_fach_value = meta_values_dict.get("Fach")
            if meta_values_fach_value is not None:
                # self.debug_disciplines.add(meta_values_fach_value)
                bundle_dict["bundle_discipline"] = meta_values_fach_value
        # "phase" is their term for "Klassenstufe"
        if "Phase" in meta_values_dict:
            meta_values_phase_value = meta_values_dict.get("Phase")
            edu_level_temp = meta_values_phase_value.replace(" ", "")  # stripping empty spaces between the comma
            educational_level = edu_level_temp.split(',')  # these values will be used for educationLevel
            bundle_dict["bundle_educational_level"] = educational_level
        if "Kompetenzbereich" in meta_values_dict:
            meta_values_competency_value = meta_values_dict.get("Kompetenzbereich")
            bundle_dict["bundle_competency"] = meta_values_competency_value
        if "Niveaustufe" in meta_values_dict:
            meta_values_niveau = meta_values_dict.get("Niveaustufe")
            bundle_dict["bundle_niveau"] = meta_values_niveau

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
        bundle_dict["worksheet_description_summary"] = worksheet_description_string

        # debug output to check if there are new disciplines that still need to be mapped:
        # debug_disciplines_sorted = list(self.debug_disciplines)
        # debug_disciplines_sorted.sort()

        # There are two "application/ld+json"-scripts on the website -> XPath: /html/body/script[1]
        # one is of @type Organization, the other of @type LocalBusiness
        # ld_json_string = response.xpath('/html/body/script[@type="application/ld+json"]/text()').get().strip()

        for ld_json_block in response.xpath('/html/body/script[@type="application/ld+json"]/text()'):
            ld_json_string = ld_json_block.get().strip()
            ld_json_temp = json.loads(ld_json_string)
            if ld_json_temp.get("@type") == "Organization":
                ld_json_organization = json.loads(ld_json_string)
                bundle_dict["bundle_ld_json_organization"] = ld_json_organization
            elif ld_json_temp.get("@type") == "LocalBusiness":
                ld_json_local_business = json.loads(ld_json_string)
                bundle_dict["bundle_ld_json_local_business"] = ld_json_local_business

        # the publication date is only available on the individual worksheet page, but it seems like the individual
        # pages of a bundle are all carrying the same date, therefore it should be enough to only parse the first
        # worksheet (and reduce load on the website)
        first_worksheet_url = response.xpath('//a[@class="worksheet"]/@href').get()
        first_worksheet_thumbnail = response.xpath('/html/body/main/div/ul/a[1]/div[1]/img/@data-src').get()
        bundle_dict["bundle_thumbnail"] = first_worksheet_thumbnail
        # there isn't a lot of metadata available on the bundle overview page, but we still need to carry it over to
        # the parse method since that's where the BaseItemLoader is built

        # bundle_dict contains the following keys:
        # - bundle_description
        # - bundle_competency                       (optional)
        # - bundle_discipline                       (optional)
        # - bundle_educational_level                  (optional)
        # - bundle_ld_json_organization
        # - bundle_ld_json_local_business
        # - bundle_niveau                           (optional, currently unmapped in edu-sharing)
        # - bundle_thumbnail
        # - bundle_title
        # - bundle_url
        # - worksheet_description_summary

        if first_worksheet_url is not None:
            yield scrapy.Request(url=first_worksheet_url, callback=self.parse, cb_kwargs=bundle_dict)

    def parse(self, response: scrapy.http.Response, **kwargs):
        """
        Parses an individual 'worksheet' and combines the metadata with data from its 'bundle'-dictionary.

        Spider Contracts:
        @url https://editor.mnweg.org/mnw/dokument/vocabulary-around-the-world-3
        @returns items 1

        :return: yields a BaseItemLoader
        """
        # since we're only parsing the first worksheet for some additional metadata, the metadata object will be
        # centered around a bundle, not the individual pages

        # print("DEBUG parse_worksheet_page", response.url)
        date_published = response.xpath('//ul[@class="meta"]/li[3]/text()').get()

        base = BaseItemLoader()
        base.add_value("sourceId", kwargs.get('bundle_url'))
        hash_temp = str(date_published + self.version)
        base.add_value("hash", hash_temp)
        # this is a hacky solution: the thumbnail is the miniature preview of the bundle's first worksheet
        bundle_thumbnail = kwargs.get('bundle_thumbnail')
        if bundle_thumbnail is not None:
            base.add_value('thumbnail', bundle_thumbnail)
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
        bundle_organization: dict = kwargs.get('bundle_ld_json_organization')
        # the dictionary that we can parse from the website itself looks like this:
        # 'organization': {'@context': 'http://schema.org',
        #                   '@type': 'Organization',
        #                   'name': 'Materialnetzwerk e. G.',
        #                   'sameAs': ['http://twitter.com/materialnw',
        #                              'https://www.facebook.com/materialnetzwerk'],
        #                   'url': 'https://editor.mnweg.org'}}
        # TODO: once its possible to parse a 'organization'-schema-type as a dictionary by the back-end, use
        #   lifecycle.add_value('organization', bundle_organization)
        if bundle_organization is not None:
            lifecycle.add_value('organization', bundle_organization.get("name"))
            lifecycle.add_value('url', bundle_organization.get("url"))
        lifecycle.add_value('date', date_published)
        lom.add_value('lifecycle', lifecycle.load_item())

        classification = LomClassificationItemLoader()
        competency_description = kwargs.get("bundle_competency")
        if competency_description is not None:
            classification.add_value('description', competency_description)
        lom.add_value('classification', classification.load_item())

        educational = LomEducationalItemLoader()
        educational_level = kwargs.get('bundle_educational_level')

        # TODO: educationalLevel is currently unsupported in the items.py backend? (there exists a vocab for it, though:
        # https://github.com/openeduhub/oeh-metadata-vocabs/blob/master/educationalLevel.ttl
        # if educational_level is not None:
        #     educational.add_value('educationalLevel', educational_level)

        lom.add_value('educational', educational.load_item())
        base.add_value('lom', lom.load_item())

        vs = ValuespaceItemLoader()
        # ToDo: learningResourceType ("teaching module") -> new_lrt "Unterrichtsbaustein" & "Arbeitsblatt"?
        # vs.add_value('learningResourceType', 'teaching module')
        vs.add_value('new_lrt', ["5098cf0b-1c12-4a1b-a6d3-b3f29621e11d",
                                 "d8c3ef03-b3ab-4a5e-bcc9-5a546fefa2e9"
                                 "36e68792-6159-481d-a97b-2c00901f4f78"])
        # "Unterrichtsbaustein", "Webseite und Portal (stabil)", "Arbeitsblatt
        bundle_discipline = kwargs.get('bundle_discipline')
        if bundle_discipline is not None:
            if self.discipline_mapping.get(bundle_discipline) is not None:
                bundle_discipline = self.discipline_mapping.get(bundle_discipline)
            vs.add_value('discipline', bundle_discipline)
        vs.add_value('intendedEndUserRole', 'teacher')
        #  logged in users can manipulate the worksheets and fit them to their needs,
        #  but there's no login required for just downloading the pdf of an available worksheet
        vs.add_value('conditionsOfAccess',
                     "login required for additional features")
        vs.add_value('price', 'no')
        # we can map "Phase" to our educationalContext with the following ValuespaceHelper method:
        if educational_level is not None:
            for educational_level_item in educational_level:
                if int(educational_level_item) <= 4:
                    vs.add_value("educationalContext", "grundschule")
                if 4 < int(educational_level_item) <= 10:
                    vs.add_value("educationalContext", "sekundarstufe_1")
                if 10 < int(educational_level_item) <= 13:
                    vs.add_value("educationalContext", "sekundarstufe_2")

        lic = LicenseItemLoader()
        # everything is CC-BY-SA 3.0 according to the FAQs: https://mnweg.org/faqs
        lic.add_value('url', Constants.LICENSE_CC_BY_SA_30)
        base.add_value('license', lic.load_item())

        response_loader = ResponseItemLoader()
        response_loader.add_value('url', kwargs.get('bundle_url'))

        base.add_value('valuespaces', vs.load_item())
        base.add_value('response', response_loader.load_item())

        yield base.load_item()
