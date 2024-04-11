import scrapy
from scrapy.spiders import CrawlSpider

from converter.constants import Constants
from converter.items import BaseItemLoader, LomBaseItemloader, LomGeneralItemloader, LomTechnicalItemLoader, \
    LomLifecycleItemloader, LomEducationalItemLoader, ValuespaceItemLoader, LicenseItemLoader, ResponseItemLoader, \
    PermissionItemLoader, LomClassificationItemLoader
from converter.spiders.base_classes import LomBase
from converter.web_tools import WebEngine, WebTools


# This is an alternative approach to our previous "sample_spider.py" that might be easier to read and understand
# for web crawling beginners. Use whichever approach is more convenient for you.
# LAST UPDATE: 2021-08-20
# please also consult converter/items.py for all currently available keys/values in our crawler data model


class SampleSpiderAlternative(CrawlSpider, LomBase):
    name = "sample_spider_alternative"
    friendlyName = "Sample Source (alternative Method)"  # how your crawler should appear in the "Supplier"-list
    start_urls = ["https://edu-sharing.com"]  # starting point of your crawler, e.g. a sitemap, index, rss-feed etc.
    version = "0.0.1"  # this is used for timestamping your crawler results (if a source changes its layout/data,
    # make sure to increment this value to force a clear distinction between old and new crawler results)
    custom_settings = {
        'WEB_TOOLS': WebEngine.Playwright  # OPTIONAL: this attribute controls which tool is used for taking Screenshots
        # you can skip this attribute altogether if you want to use the default Settings (Splash)
    }

    def getId(self, response=None) -> str:
        # You have two choices here:
        # - either implement this method and return the current url of a material as a string
        # - or look into the parse()-method for base.add_value('sourceId', response.url) is set manually
        pass

    def getHash(self, response=None) -> str:
        # The hash should always be unique, e.g. by string-concatenating using the publicationDate + self.version
        # you can implement this method here or simply look at the parse()-method where
        # base.add_value('hash', hash_temp)
        # is set manually.
        pass

    def start_requests(self):
        for start_url in self.start_urls:
            yield scrapy.Request(url=start_url, callback=self.parse)

    async def parse(self, response: scrapy.http.Response, **kwargs) -> BaseItemLoader:
        # OPTIONAL: If you need to use playwright to crawl a website, this is how you can access the data provided
        # by Playwright's headless browser
        playwright_dict: dict = await WebTools.getUrlData(response.url, WebEngine.Playwright)
        html_body = playwright_dict.get("html")
        screenshot_bytes = playwright_dict.get("screenshot_bytes")  # to be used in base.screenshot_bytes

        base = BaseItemLoader()
        # ALL possible keys for the different Item and ItemLoader-classes can be found inside converter/items.py

        # TODO: fill "base"-keys with values for
        #  - sourceId           required    (see: getId()-method above)
        #  - hash               required    (see: getHash()-method above)
        #  - lom                required    (see: LomBaseItemLoader below)
        #  - valuespaces        required    (see: ValueSpacesItemLoader below)
        #  - permissions        required    (see: PermissionItemLoader below)
        #  - license            required    (see: LicenseItemLoader below)
        #  - lastModified       recommended
        #  - origin             optional    (only necessary if items need to be sorted into a specific sub-folder)
        #  - thumbnail          recommended
        #  - publisher          optional
        #  - binary             optional    (only needed if you're working with binary files (e.g. .pdf-files),
        #                                   if you want to see an example, check out "niedersachsen_abi_spider.py")
        #  - fulltext           optional    (if 'full text' content is provided by a source (e.g. raw HTML or a
        #                                   human readable string of text) store its within the 'fulltext' field.)
        #                                   If no 'fulltext' value was provided, the pipelines will try to fetch
        #                                   'full text' content from "ResponseItem.text" and save it here.
        base.add_value('sourceId', response.url)
        # if the source doesn't have a "datePublished" or "lastModified"-value in its header or JSON_LD,
        # you might have to help yourself with a unique string consisting of the datetime of the crawl + self.version
        hash_temp: str = "This string should consist of a date (publication date, preferably)" + self.version
        base.add_value('hash', hash_temp)
        last_modified = None
        base.add_value('lastModified', last_modified)
        thumbnail_url: str = "This string should hold the thumbnail URL"
        base.add_value('origin', 'premium_only')  # the OPTIONAL value for "origin" controls the subfolder-name
        # in the edu-sharing repository (e.g. if you need to make a distinction between learning objects that are free
        # to access or premium_only). in this example, items that have the "premium_only"-value will be sent to the
        # "SYNC_OBJ/<crawler_name>/premium_only/"-folder.
        # (This field is used in two different use-cases, both in "youtube_spider" and "lehreronline_spider")
        base.add_value('thumbnail', thumbnail_url)  # the thumbnail field expects an URL (as a String)
        base.add_value('screenshot_bytes', screenshot_bytes)  # this is an OPTIONAL field that will be CONSUMED within
        # the thumbnail pipeline to create a small/large thumbnail of the website itself

        lom = LomBaseItemloader()
        # TODO: afterwards fill up the LomBaseItem with
        #  - LomGeneralItem                 required
        #  - LomTechnicalItem               required
        #  - LomLifeCycleItem               required (multiple possible)
        #  - LomEducationalItem             required
        #  - LomClassificationItem          optional

        general = LomGeneralItemloader()
        # TODO: fill "general"-keys with values for
        #  - identifier                     required
        #  - title                          required
        #  - keyword                        required
        #  - description                    required
        #  - language                       recommended (edu-sharing expects underscores in language-codes, e.g. 'en-US'
        #                                               needs to be replaced by 'en_US')
        #  - coverage                       optional
        #  - structure                      optional
        #  - aggregationLevel               optional
        # e.g.: the unique identifier might be the URL to a material
        general.add_value('identifier', response.url)
        # TODO: don't forget to add key-value-pairs for 'title', 'keyword' and 'description'!

        technical = LomTechnicalItemLoader()
        # TODO: fill "technical"-keys with values for
        #  - format                         required (expected: MIME-type, e.g. 'text/html' for web-sites)
        #  - location                       required (expected: URI / URL of a learning object / material)
        #  - size                           optional
        #  - requirement                    optional
        #  - installationRemarks            optional
        #  - otherPlatformRequirements      optional
        #  - duration                       optional (only applies to audiovisual content like videos/podcasts)
        # similar to how the "general"-LomGeneralItemLoader was filled with Items, individual values can be set with
        # technical.add_value('key','value')
        # or replaced with:
        # technical.replace_value('key', 'value')
        technical.add_value('format', 'text/html')  # e.g. if the learning object is a web-page
        technical.add_value('location', response.url)  # if the learning object has a unique URL that's being
        # navigated by the crawler

        lifecycle = LomLifecycleItemloader()
        # TODO: fill "lifecycle"-keys with values for
        #  - role                           recommended
        #  - firstName                      recommended
        #  - lastName                       recommended
        #  - url                            recommended
        #  - date                           recommended
        #  - organization                   optional
        #  - email                          optional
        #  - uuid                           optional
        #  - title                          optional (academic title)
        #  - id_gnd                         optional (expected: URI)
        #  - id_orcid                       optional (expected: URI)
        #  - id_ror                         optional (expected: URI)
        #  - id_wikidata                    optional (expected: URI)
        lifecycle.add_value('role', 'author')
        # supported roles:
        #   "author" / "editor" / "publisher" / "metadata_contributor" / "metadata_provider" / "unknown"
        # for further available role mappings, please take a look at converter/es_connector.py

        educational = LomEducationalItemLoader()
        # TODO: fill "educational"-keys with values for
        #  - description                    recommended (= "Comments on how this learning object is to be used")
        #  - language                       recommended
        #  - interactivityType              optional
        #  - interactivityLevel             optional
        #  - semanticDensity                optional
        #  - typicalAgeRange                optional
        #  - difficulty                     optional
        #  - typicalLearningTime            optional

        classification = LomClassificationItemLoader()
        # TODO: fill "classification"-keys with values for
        #  - cost                           optional
        #  - purpose                        optional
        #  - taxonPath                      optional
        #  - description                    optional
        #  - keyword                        optional

        # once you've filled "general", "technical", "lifecycle" and "educational" with values,
        # the LomBaseItem is loaded into the "base"-BaseItemLoader

        vs = ValuespaceItemLoader()
        # for possible values, either consult https://vocabs.openeduhub.de
        # or take a look at https://github.com/openeduhub/oeh-metadata-vocabs
        # wherever possible, please use the skos:Concept <key> instead of literal strings
        # (since they are more stable over a longer period of time)
        # TODO: fill "valuespaces"-keys with values for
        #  - discipline                     recommended
        #  (see: https://github.com/openeduhub/oeh-metadata-vocabs/blob/master/discipline.ttl)
        #   (please set discipline-values by their unique vocab-identifier: e.g. '060' for "Art education")
        #  - intendedEndUserRole            recommended
        #  (see: https://github.com/openeduhub/oeh-metadata-vocabs/blob/master/intendedEndUserRole.ttl)
        #  - learningResourceType           recommended
        #  (see: https://github.com/openeduhub/oeh-metadata-vocabs/blob/master/learningResourceType.ttl)
        #  - new_lrt                        recommended
        #  (see: https://github.com/openeduhub/oeh-metadata-vocabs/blob/master/new_lrt.ttl)
        #  - conditionsOfAccess             recommended
        #  (see: https://github.com/openeduhub/oeh-metadata-vocabs/blob/master/conditionsOfAccess.ttl)
        #  - containsAdvertisement          recommended
        #  (see: https://github.com/openeduhub/oeh-metadata-vocabs/blob/master/containsAdvertisement.ttl)
        #  - price                          recommended
        #  (see: https://github.com/openeduhub/oeh-metadata-vocabs/blob/master/price.ttl)
        #  - educationalContext             optional
        #  (see: https://github.com/openeduhub/oeh-metadata-vocabs/blob/master/educationalContext.ttl)
        #  - toolCategory                   optional
        #  (see: https://github.com/openeduhub/oeh-metadata-vocabs/blob/master/toolCategory.ttl)
        #  - accessibilitySummary           optional
        #  (see: https://github.com/openeduhub/oeh-metadata-vocabs/blob/master/accessibilitySummary.ttl)
        #  - dataProtectionConformity       optional
        #  (see: https://github.com/openeduhub/oeh-metadata-vocabs/blob/master/dataProtectionConformity.ttl)
        #  - fskRating                      optional
        #  (see: https://github.com/openeduhub/oeh-metadata-vocabs/blob/master/fskRating.ttl)
        #  - languageLevel                  optional
        #  (see: https://github.com/openeduhub/oeh-metadata-vocabs/blob/master/languageLevel.ttl)
        #  - oer                            optional
        #  (see: https://github.com/openeduhub/oeh-metadata-vocabs/blob/master/oer.ttl)
        vs.add_value('new_lrt', Constants.NEW_LRT_MATERIAL)

        lic = LicenseItemLoader()
        # TODO: fill "license"-keys with values for
        #  - url                            required
        #  - oer                            recommended ('oer' is automatically set if the 'url'-field above
        #  is recognized in LICENSE_MAPPINGS: for possible url-mapping values, please take a look at
        #  LICENSE_MAPPINGS in converter/constants.py)
        #  - author                         recommended
        #  - internal                       optional
        #  - description                    optional
        #  - expirationDate                 optional (for content that expires, e.g. ÖR-Mediatheken)

        # Either fill the PermissionItemLoader manually (not necessary most of the times)
        permissions = PermissionItemLoader()
        # or (preferably) call the inherited getPermissions(response)-method
        #   from converter/spiders/base_classes/lom_base.py by using super().:
        # permissions = super().getPermissions(response)
        # TODO: if necessary, add/replace values for the following "permissions"-keys
        #  - public                         optional
        #  - groups                         optional
        #  - mediacenters                   optional
        #  - autoCreateGroups               optional
        #  - autoCreateMediacenters         optional

        # Either fill the ResponseItemLoader manually (not necessary most of the time)
        response_loader = ResponseItemLoader()
        # or (preferably) call the inherited mapResponse(response)-method
        #   from converter/spiders/base_classes/lom_base.py by using super().:
        # response_loader = super().mapResponse(response)
        # TODO: if necessary, add/replace values for the following "response"-keys
        #  - url                            required
        #  - status                         unused
        #  - html                           unused
        #  - text                           optional (use this field for 'full text' data)
        #  - headers                        unused
        #  - cookies                        unused
        #  - har                            unused

        # once we've added all available values to the necessary keys in our LomGeneralItemLoader,
        # we call the load_item()-method to return a (now filled) LomGeneralItem to the LomBaseItemLoader.
        # We do the same for every other nested Item within LomBaseItem as well:
        lom.add_value('general', general.load_item())
        lom.add_value('technical', technical.load_item())
        lom.add_value('lifecycle', lifecycle.load_item())
        lom.add_value('educational', educational.load_item())
        lom.add_value('classification', classification.load_item())
        # after LomBaseItem is filled with metadata, we build and return it to our BaseItem
        base.add_value('lom', lom.load_item())
        base.add_value('license', lic.load_item())
        base.add_value('valuespaces', vs.load_item())
        base.add_value('permissions', permissions.load_item())
        base.add_value('response', response_loader.load_item())
        # once all scrapy.Items are loaded into our "base", we yield the BaseItem by calling the .load_item() method
        yield base.load_item()
