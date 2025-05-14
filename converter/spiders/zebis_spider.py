import datetime
import json
import re
from collections.abc import Generator, Iterable
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import scrapy
import trafilatura
from bs4 import BeautifulSoup
from scrapy import Request
from scrapy.http import Response
from scrapy.selector import Selector
from scrapy.spiders import XMLFeedSpider
from twisted.internet.defer import Deferred

from converter.constants import Constants
from converter.es_connector import EduSharing
from converter.items import (
    BaseItemLoader,
    LicenseItemLoader,
    LomAgeRangeItemLoader,
    LomBaseItemloader,
    LomClassificationItemLoader,
    LomEducationalItemLoader,
    LomGeneralItemloader,
    LomLifecycleItemloader,
    LomTechnicalItemLoader,
    PermissionItemLoader,
    ResponseItemLoader,
    ValuespaceItemLoader,
)
from converter.spiders.base_classes import LomBase
from converter.util.directories import get_project_root
from converter.util.license_mapper import LicenseMapper
from converter.web_tools import WebEngine


@dataclass
class ZebisXMLItem:
    """
    Holds the cleaned-up (and if necessary: separated) values which were parsed from each XML <record> element.
    """

    oai_identifier: str = None
    """XML <record/header/identifier> value. Contains an OAI identifier string."""
    datestamp: str = None
    """XML <record/header/datestamp> value. Contains the lastModified datetime."""
    dc_audience: list[str] = None
    """XML <record/metadata/dc/audience> value. 
    Contains multiple values describing the class level ("7. Klasse") 
    or educational context ("Kindergarten") of an item."""
    dc_creator: str = None
    """XML <record/metadata/dc/creator> value. Contains a contributor's name (person or organization). 
    The zebis frontend describes this person as "Erfasser/in des Materials"."""
    dc_contributor: str = None
    """XML <record/metadata/dc/contributor> value. Contains a contributor's name (person or organization)."""
    dc_date: str = None
    """XML <record/metadata/dc/date> value. Contains the publication date."""
    dc_description: str = None
    """XML <record/metadata/dc/description> value. Contains a description of the item."""
    dc_identifier: list[str] = None
    """XML <record/metadata/dc/identifier> value. Contains multiple URLs. 
    The first URL should always be the item's URL, while the second URL points toward a thumbnail URL."""
    dc_identifier_url: str = None
    """Stores the first URL from <dc:identifier>, which is the item's URL."""
    dc_identifier_thumbnail_url: str = None
    """Stores the second URL from <dc:identifier>, which points towards the thumbnail."""
    dc_language: str = None
    """XML <record/metadata/dc/language> value. Contains a 3-char language code."""
    dc_publisher: str = None
    """XML <record/metadata/dc/publisher> value. Contains a publisher name (organization or person)."""
    dc_rights: str = None
    """XML <record/metadata/dc/rights> value. Contains a string describing the item's license."""
    dc_subject: list[str] = None
    """XML <record/metadata/dc/subject> value. Contains a list of subjects, 
    which are predominantly keywords relating to the item, 
    but also contain values that can be mapped to disciplines."""
    dc_title: str = None
    """XML <record/metadata/dc/title> value. Contains a title of the item."""
    dc_type: list[str] = None
    """XML <record/metadata/dc/type> value. Describes the item's type (e.g. "Webseite" or "Arbeitsblatt")."""


class ZebisSpider(XMLFeedSpider, LomBase):
    name = "zebis_spider"
    friendlyName = "Zebis"
    start_urls = ["https://www.zebis.ch/export/oai"]
    version = "0.0.2"  # last update: 2025-05-14
    custom_settings = {
        "AUTOTHROTTLE_ENABLED": True,
        "AUTOTHROTTLE_DEBUG": True,
        # "AUTOTHROTTLE_TARGET_CONCURRENCY": 0.75,
        # "CONCURRENT_REQUESTS_PER_DOMAIN": 4,
        # "DOWNLOAD_DELAY": 2.0,
        # "ROBOTSTXT_OBEY": False,
        "HTTPCACHE_ENABLED": False,
        "HTTPCACHE_EXPIRATION_SECS": 3600,
        "HTTPCACHE_DIR": "httpcache",
        "WEB_TOOLS": WebEngine.Playwright,
        "PLAYWRIGHT_ADBLOCKER": True,
    }

    iterator = "iternodes"
    itertag = "record"

    # set to True if you want to dump the range of values to ``logs/zebis_range_of_values.json`` at the end of a crawl:
    debug_range_of_values: bool = False
    # the following sets are used to determine the range of values which Zebis provides for specific metadata properties
    DEBUG_AUDIENCE: set[str] = set()
    DEBUG_LANGUAGES: set[str] = set()
    DEBUG_RIGHTS: set[str] = set()
    DEBUG_SUBJECTS: set[str] = set()
    DEBUG_TYPES: set[str] = set()

    # mapping from Zebis <dc:audience> to "educationalContext"-Vocab values
    MAPPING_AUDIENCE_TO_EDUCATIONAL_CONTEXT: dict = {
        "1. Zyklus": ["elementarbereich", "grundschule"],
        "2. Zyklus": ["grundschule", "sekundarstufe_1"],
        "3. Zyklus": ["sekundarstufe_1"],
        "Kindergarten": ["elementarbereich"],
    }
    # mapping from Zebis <dc:type> to "new_lrt"-Vocab values
    MAPPING_DC_TYPE_TO_NEW_LRT: dict = {
        "Animation": ["2e67ce4e-49ce-468b-bd94-96a74e4832aa"],  # Animation
        "App": ["e5ed8ec2-2c7e-4f46-aba9-e67148ef6656"],  # Lern-App
        "Arbeitsblatt": ["36e68792-6159-481d-a97b-2c00901f4f78"],  # Arbeitsblatt
        "Atlas": ["b6ceade0-58d3-4179-af71-d53ebc6e49d4"],  # Karte
        "Audio": ["ec2682af-08a9-4ab1-a324-9dca5151e99f"],  # Audio
        "Bibliografie": ["c022c920-c236-4234-bae1-e264a3e2bdf6"],  # "Nachschlagewerk und Glossareintrag"
        "Bild / Grafik": ["a6d1ac52-c557-4151-bc6f-0d99b0b96fb9"],  # "Bild (Material)"
        "Buch / Broschüre": ["01551356-a6a3-44fc-9662-7d366d7af0ac"],  # "sonstiges Buch und E-Book"
        "CD-ROM / DVD": ["4665caac-99d7-4da3-b9fb-498d8ece034f"],  # "Interaktives Medium"
        "Karte": ["b6ceade0-58d3-4179-af71-d53ebc6e49d4"],  # Karte
        "Lieder-/Notensammlung": ["f7e92628-4132-4985-bcf5-93c285e300a8"],  # Noten
        "Nachschlagewerk / Glossar": ["c022c920-c236-4234-bae1-e264a3e2bdf6"],  # "Nachschlagewerk und Glossareintrag"
        "Präsentationsfolien": ["92c7a50c-6243-45d9-8b11-e79cbbda6305"],  # Präsentation
        "Software / Programm": ["e5ed8ec2-2c7e-4f46-aba9-e67148ef6656"],  # Lern-App?
        "Tabellenkalkulation": ["933ceef8-c7ae-4af3-9229-4bd86334dfea"],  # Tabellen
        "Textdokument": ["0cef3ce9-e106-47ae-836a-48f9ed04384e"],  # "Dokumente und textbasierte Inhalte"
        "Video": ["7a6e9608-2554-4981-95dc-47ab9ba924de"],  # "Video (Material)"
        "Webseite": ["d8c3ef03-b3ab-4a5e-bcc9-5a546fefa2e9"],  # Webseite
        "Zeitschrift / Zeitung": ["0cef3ce9-e106-47ae-836a-48f9ed04384e"],  # "Dokumente und textbasierte Inhalte"
    }
    # mapping from <dc:subject> to "discipline"-Vocab:
    # as long as all "Fachbereich"-values (see right sidebar: https://www.zebis.ch/unterrichtsmaterial) are covered,
    # most disciplines should be matched within the pipeline / es_connector.
    MAPPING_DC_SUBJECT_TO_DISCIPLINE: dict = {
        "BNE": ["64018"],  # Nachhaltigkeit
        "Berufsbildung": ["040"],  # Berufliche Bildung
        "Berufskunde": ["040"],  # Berufliche Bildung
        "Berufliche Orientierung": ["040"],  # Berufliche Bildung
        "Bewegung und Sport": ["600"],  # Sport
        "Bildnerisches Gestalten": ["060"],  # Kunst
        "Deutschunterricht": ["120"],  # Deutsch
        "Ethik, Religionen, Gemeinschaft": ["160", "520"],  # Ethik ; Religion
        "Frühenglisch": ["20001"],  # Englisch
        "Frühfranzösisch": ["20002"],  # Französisch
        "Interkulturelles Lernen": ["340"],  # Interkulturelle Bildung
        "Medien und Informatik": ["900", "320"],  # Medienbildung; Informatik
        "Medien & Informatik": ["900", "320"],  # Medienbildung; Informatik
        "Medien im Alltag": ["900"],  # Medienbildung
        "Medienpädagogik": ["900"],  # Medienbildung
        "Metallbearbeitung": ["04011"],  # Metalltechnik
        "Metallwerken": ["04011"],  # Metalltechnik
        "Natur, Mensch, Gesellschaft": ["28010"],  # Sachunterricht
        "Natur und Technik": ["28010", "080", "100", "460"],  # Sachunterricht; Biologie; Chemie; Physik
        # Sex-related subjects must be manually mapped because they're covered in "Natur, Mensch, Gesellschaft",
        # but mapping that "Fachbereich" directly to Sexualkunde would lead to too many false mappings
        "Sex": ["560"],  # Sexualerziehung
        "Sexting": ["560"],  # Sexualerziehung
        "Sextortion": ["560"],  # Sexualerziehung
        "Sexualität": ["560"],  # Sexualerziehung
        "Sexualpädagogik": ["560"],  # Sexualerziehung
        "Textiles Gestalten": ["04012"],  # Textiltechnik und Bekleidung
        "Textiles und Technisches Gestalten": ["04012", "50005", "060", "28010"],
        # "TTG" cannot be mapped to one specific discipline. It's roughly equivalent to:
        # Textiltechnik und Bekleidung; Werken; Kunst; Sachunterricht
        "Velofahren": ["660"],  # Verkehrserziehung
        "Verkehrsregeln": ["660"],  # Verkehrserziehung
        "Verkehrssicherheit": ["660"],  # Verkehrserziehung
        "Wirtschaft, Arbeit, Haushalt": ["700", "020", "50001"],  # Wirtschaftskunde; Arbeitslehre; Hauswirtschaft
    }

    # ToDo:
    #  - figure out how to bypass zebis bot protection:
    #    - the API endpoint is protected by Cloudflare and returns a 403 response for anything but a real browser.
    #    - GET requests via requests/Scrapy/playwright get intercepted by Cloudflare's "Just a moment..."-page

    def __init__(self, **kwargs):
        LomBase.__init__(self, **kwargs)

    def start_requests(self) -> Iterable[Request]:
        for _url in self.start_urls:
            yield scrapy.Request(
                url=_url,
                meta={
                    "playwright": True,
                    "autothrottle_dont_adjust_delay": True,
                    "is_start_request": True,
                },
                # attention: Zebis.ch is protected by Cloudflare!
                # Making requests without the scrapy-playwright middleware results in HTTP-Status 403 responses!
                callback=self.parse_oai_pmh_xml,
                # Normally, we wouldn't have to use a callback method here because XMLFeedSpider would call
                # the parse_node() method by itself
                # (using the defined ``iterator`` and ``itertag`` attributes).
                # But since scrapy-playwright delivers an HTML response,
                # where the (required) positional ``selector``-argument is missing,
                # a manual implementation of the XML node iteration is necessary.
                # This workaround might be obsolete with a future scrapy-playwright update,
                # see: https://github.com/scrapy-plugins/scrapy-playwright/issues/334
            )

    def close(self, reason: str) -> Deferred[None] | None:
        # Debug setting: if enabled, dumps the range of values to the specified .json file within "oeh-search-etl/logs/"
        if self.debug_range_of_values:
            _root: Path = get_project_root()
            _zebis_values: dict = {}
            with open(f"{_root}/logs/zebis_range_of_values.json", "w") as file_writer:
                if self.DEBUG_AUDIENCE:
                    _audience_values = list(self.DEBUG_AUDIENCE)
                    _audience_values.sort()
                    _zebis_values.update({"dc_audience": _audience_values})
                if self.DEBUG_LANGUAGES:
                    _language_values = list(self.DEBUG_LANGUAGES)
                    _language_values.sort()
                    _zebis_values.update({"dc_language": _language_values})
                if self.DEBUG_RIGHTS:
                    _right_values = list(self.DEBUG_RIGHTS)
                    _right_values.sort()
                    _zebis_values.update({"dc_rights": _right_values})
                if self.DEBUG_SUBJECTS:
                    _subject_values = list(self.DEBUG_SUBJECTS)
                    _subject_values.sort()
                    _zebis_values.update({"dc_subject": _subject_values})
                if self.DEBUG_TYPES:
                    _type_values = list(self.DEBUG_TYPES)
                    _type_values.sort()
                    _zebis_values.update({"dc_type": _type_values})
                json.dump(_zebis_values, file_writer, indent=4)

    def parse_oai_pmh_xml(self, response: Response) -> Generator[Any]:
        """
        Iterate over the OAI-PMH XML file and yield a request to each <record>.

        :param response: Zebis XML API response
        :return: scrapy.Request or None
        """
        xml_body: str = response.text
        xml_selector: Selector = Selector(text=xml_body, type="xml")
        xml_selector.remove_namespaces()
        _records = xml_selector.xpath("//record").getall()
        self.logger.info(f"Total amount of OAI-PMH XML <record>-elements retrieved: {len(_records)}")
        _records_deleted = xml_selector.xpath("//record/header[@status='deleted']").getall()
        # the zebis API provides <record>-items which are marked as deleted.
        # example:
        # <record>
        # 	<header status="deleted">
        # 		<identifier>oai:www.zebis.ch:node-35821</identifier>
        # 		<datestamp>2019-08-23T07:03:21Z</datestamp>
        # 		<setSpec>umat_oai:entity_reference_1</setSpec>
        # 	</header>
        # 	<metadata/>
        # </record>
        self.logger.info(f"Total amount of inactive (deleted) <record>-elements: {len(_records_deleted)}")
        if _records and isinstance(_records, list):
            for _record in _records:
                _selector: Selector = Selector(text=_record, type="xml")
                yield from self.parse_node(response=response, selector=_selector)
        else:
            self.logger.error(
                "Failed to read <record> elements from Zebis OAI-PMH XML. "
                "Please check the validity / structure of the API Response!"
            )
            return None

    def parse_node(self, response: Response, selector: Selector) -> Any:
        """
        Parse each <record> element and clean up each property before yielding a request to the ``parse()``-method.

        :param response: Zebis OAI-PMH XML API response
        :param selector: ``scrapy.Selector``-object
        :return: ``scrapy.Request`` or ``None``
        """
        # each <record> contains a
        # <header> with the following elements:
        # <identifier>          -> sourceId / LOM General identifier
        # <datestamp>           -> lastModified date
        # <setSpec>             -> ?

        # see: https://www.openarchives.org/OAI/2.0/oai_dc.xsd
        # a <record> might contain the following <metadata> elements:
        # <dc:title>            -> LOM General title
        # <dc:creator>          -> LOM Lifecycle metadata creator
        # <dc:subject>          -> multiple <dc:subject> elements per record! -> keywords / discipline
        # <dc:description>      -> LOM General description
        # <dc:publisher>        -> LOM Lifecycle publisher?
        # <dc:contributor>      -> LOM Lifecycle contributor unknown?
        # <dc:date>             -> creation date
        # <dc:type>             -> new_lrt
        # <dc:format>           -> not available
        # <dc:identifier>       -> (multiple) URLs separated by |
        # <dc:source>           -> not available
        # <dc:language>         -> LOM General language (example: "ger")
        # <dc:relation>         -> not available
        # <dc:coverage>         -> not available
        # <dc:rights>           -> license description

        # see: https://www.dublincore.org/specifications/dublin-core/dcmi-terms/
        # DCMI terms that are used by zebis:
        # <dc:audience>         -> educationalContext
        # question: are there any further DCMI terms used by zebis?

        _cleaned_record: ZebisXMLItem = ZebisXMLItem()

        _oai_identifier: str | None = selector.xpath("//header/identifier/text()").get()
        if _oai_identifier and isinstance(_oai_identifier, str):
            _oai_identifier = _oai_identifier.strip()
            # stripping whitespaces, just in case
            if _oai_identifier:
                _cleaned_record.oai_identifier = _oai_identifier

        _item_is_marked_as_deleted: str | None = selector.xpath("//header[@status='deleted']").get()
        if _item_is_marked_as_deleted:
            self.logger.info(f"XML <record> {_cleaned_record.oai_identifier} is marked as deleted. Skipping item...")
            return None

        _datestamp: str | None = selector.xpath("//header/datestamp/text()").get()
        if _datestamp and isinstance(_datestamp, str):
            # <datestamp>-values are generally more recent than <dc:date>,
            # which leads us to the assumption that <datestamp> indicates an item's ``lastModified`` date
            _datestamp = _datestamp.strip()
            if _datestamp:
                _cleaned_record.datestamp = _datestamp
            pass

        _dc_audience_raw: str | None = selector.xpath("//metadata/dc/audience/text()").get()
        if _dc_audience_raw and isinstance(_dc_audience_raw, str):
            # example value:
            # <dc:audience>Kindergarten, 1. Klasse, 2. Klasse, 3. Klasse, 4. Klasse, 5. Klasse, 6. Klasse, 7. Klasse,
            # 8. Klasse, 9. Klasse</dc:audience>
            _audience_set: set[str] = set()  # this set will hold the final audience items
            if "," in _dc_audience_raw:
                # if a comma exists, it must be a multi-value string
                _audience_list_raw: list[str] = _dc_audience_raw.split(",")
                if _audience_list_raw and isinstance(_audience_list_raw, list):
                    for _audience_item in _audience_list_raw:  # type: str
                        _audience_item = _audience_item.strip()
                        if _audience_item:
                            _audience_set.add(_audience_item)
            else:
                # if there was no comma in the string, it must be a single-value entry
                _dc_audience_raw = _dc_audience_raw.strip()
                if _dc_audience_raw:
                    _audience_set.add(_dc_audience_raw)
            if _audience_set:
                _audience_list: list[str] = list(_audience_set)
                _audience_list.sort()
                _cleaned_record.dc_audience = _audience_list

        _dc_creator: str | None = selector.xpath("//metadata/dc/creator/text()").get()
        if _dc_creator and isinstance(_dc_creator, str):
            # there can be a single <dc:creator> element that contains a person- or organization-related string:
            # - person: "<lastname> <middle name> <firstname>"
            # - organization, e.g.: "zebis redaktion"
            _dc_creator = _dc_creator.strip()
            if _dc_creator:
                _cleaned_record.dc_creator = _dc_creator

        _dc_contributor: str | None = selector.xpath("//metadata/dc/contributor/text()").get()
        if _dc_contributor and isinstance(_dc_contributor, str):
            # contributors can be either natural persons or organizations (e.g.: "zebis Redaktion")
            _dc_contributor = _dc_contributor.strip()
            if _dc_contributor:
                _cleaned_record.dc_contributor = _dc_contributor

        _dc_date: str | None = selector.xpath("//metadata/dc/date/text()").get()
        if _dc_date and isinstance(_dc_date, str):
            # <dc:date> contains older timestamps than <datestamp>,
            # which leads us to the assumption that <dc:date> indicates an item's creation date.
            _dc_date = _dc_date.strip()
            if _dc_date:
                _cleaned_record.dc_date = _dc_date

        _dc_description: str | None = selector.xpath("//metadata/dc/description/text()").get()
        if _dc_description and isinstance(_dc_description, str):
            _dc_description = _dc_description.strip()
            if _dc_description:
                _raw_description_soup = BeautifulSoup(_dc_description, "html.parser")
                _dc_description_clean: str = _raw_description_soup.get_text()
                if _dc_description_clean:
                    _cleaned_record.dc_description = _dc_description_clean

        _dc_identifiers_raw: str | None = selector.xpath("//metadata/dc/identifier/text()").get()
        if _dc_identifiers_raw and isinstance(_dc_identifiers_raw, str):
            _dc_id_set: set[str] = set()
            if "|" in _dc_identifiers_raw:
                # typically, Zebis provides two identifier URIs separated by a "|"-symbol:
                # - the first URL points towards the main URL of an item
                # - the second URL points towards the thumbnail URL
                _dc_identifiers: list[str] = _dc_identifiers_raw.split("|")
                if _dc_identifiers and isinstance(_dc_identifiers, list):
                    # to make handling of identifier URIs a bit easier, we'll save them to their own dataclass attribute
                    if 0 < len(_dc_identifiers) <= 2:
                        # happy case:
                        # the first entry is the item's URL
                        _dc_identifier_url: str = _dc_identifiers[0]
                        _dc_identifier_url = _dc_identifier_url.strip()
                        if _dc_identifier_url:
                            _cleaned_record.dc_identifier_url = _dc_identifier_url
                        if len(_dc_identifiers) > 1:
                            # the second entry should be its thumbnail URL
                            _dc_identifier_thumbnail_url: str = _dc_identifiers[1]
                            _dc_identifier_thumbnail_url = _dc_identifier_thumbnail_url.strip()
                            if _dc_identifier_thumbnail_url:
                                _cleaned_record.dc_identifier_thumbnail_url = _dc_identifier_thumbnail_url
                    else:
                        # if the item has either 0 identifiers (-> can't be scraped) or too many,
                        # we might have to handle more edge-cases
                        self.logger.warning(
                            f"Item {_oai_identifier} has an unexpected amount of <dc:identifier> values: "
                            f"Expected length of two, but received {len(_cleaned_record.dc_identifier)}. "
                            f"dc_identifier values: {_cleaned_record.dc_identifier}"
                        )
                    for _id_string in _dc_identifiers:
                        _id_string = _id_string.strip()
                        if _id_string:
                            _dc_id_set.add(_id_string)
            else:
                # if no "|"-symbol was found in the string, there should be only one URI
                _dc_identifiers_raw = _dc_identifiers_raw.strip()
                if _dc_identifiers_raw and isinstance(_dc_identifiers_raw, str):
                    _dc_id_set.add(_dc_identifiers_raw)
            if _dc_id_set:
                _cleaned_record.dc_identifier = list(_dc_id_set)

        _dc_language: str | None = selector.xpath("//metadata/dc/language/text()").get()
        if _dc_language and isinstance(_dc_language, str):
            # <dc:language> elements typically contain 3-char language codes
            _dc_language = _dc_language.strip()
            if _dc_language:
                _cleaned_record.dc_language = _dc_language

        _dc_publisher: str | None = selector.xpath("//metadata/dc/publisher/text()").get()
        if _dc_publisher and isinstance(_dc_publisher, str):
            _dc_publisher = _dc_publisher.strip()
            if _dc_publisher:
                _cleaned_record.dc_publisher = _dc_publisher

        _dc_rights: str | None = selector.xpath("//metadata/dc/rights/text()").get()
        if _dc_rights and isinstance(_dc_rights, str):
            # <dc:rights> typically contains license descriptions which need to be mapped
            # examples from the current range of values (as of 2025-05-09):
            # "CC BY (Namensnennung)",
            # "CC BY-NC (Namensnennung - nicht kommerziell)",
            # "CC BY-NC-ND (Namensnennung - nicht kommerziell - keine Bearbeitung)",
            # "CC BY-NC-SA (Namensnennung - nicht kommerziell - Weitergabe unter gleichen Bedingungen)",
            # "CC BY-ND (Namensnennung - keine Bearbeitung)",
            # "CC BY-SA (Namensnennung - Weitergabe unter gleichen Bedingungen)",
            # "Keine Einschränkung"
            # "Nicht definiert"
            _dc_rights = _dc_rights.strip()
            if _dc_rights:
                if "Nicht definiert" in _dc_rights:
                    _dc_rights = None
                _cleaned_record.dc_rights = _dc_rights

        _dc_subjects: list[str] | None = selector.xpath("//metadata/dc/subject/text()").getall()
        if _dc_subjects and isinstance(_dc_subjects, list):
            # one <record> can have multiple <dc:subject> elements, which
            # - often contain the discipline ("Deutsch", "Medien und Informatik")
            # - but also contains keywords
            # example:
            # <dc:subject>Märchen</dc:subject>
            # <dc:subject>Rotkäppchen</dc:subject>
            # <dc:subject>Deutsch</dc:subject>
            _subject_set: set[str] = set()
            for _subject in _dc_subjects:
                _subject = _subject.strip()
                if _subject:
                    _subject_set.add(_subject)
            if _subject_set:
                _cleaned_record.dc_subject = list(_subject_set)

        _dc_title: str | None = selector.xpath("//metadata/dc/title/text()").get()
        if _dc_title and isinstance(_dc_title, str):
            _dc_title = _dc_title.strip()
            if _dc_title:
                _cleaned_record.dc_title = _dc_title

        _dc_type_raw: str | None = selector.xpath("//metadata/dc/type/text()").get()
        if _dc_type_raw and isinstance(_dc_type_raw, str):
            # <dc:type> contains a single string, but within that string,
            # there can be multiple values that need to be split up.
            # example:
            # <dc:type>Arbeitsblatt, Lieder-/Notensammlung, Textdokument</dc:type>
            _dc_type_set: set[str] = set()
            if "," in _dc_type_raw:
                # if a comma exists in the string, it must contain multiple type values
                _type_list: list[str] = _dc_type_raw.split(",")
                if _type_list and isinstance(_type_list, list):
                    for _type in _type_list:
                        _type = _type.strip()
                        if _type:
                            _dc_type_set.add(_type)
            else:
                # if no comma exists, the string must be a single-value string
                _dc_type_raw = _dc_type_raw.strip()
                if _dc_type_raw:
                    _dc_type_set.add(_dc_type_raw)
            if _dc_type_set:
                _dc_types: list[str] = list(_dc_type_set)
                _dc_types.sort()
                _cleaned_record.dc_type = _dc_types

        if _cleaned_record.dc_identifier_url and isinstance(_cleaned_record.dc_identifier_url, str):
            yield scrapy.Request(
                url=_cleaned_record.dc_identifier_url,
                meta={"playwright": True},
                callback=self.parse,
                cb_kwargs={"cleaned_record": _cleaned_record},
            )
        return None

    def getId(self, response=None, cleaned_record: ZebisXMLItem = None) -> str:
        if cleaned_record and cleaned_record.oai_identifier:
            return cleaned_record.oai_identifier
        else:
            self.logger.warning(
                f"getId() failed: The item did not provide an OAI identifier. Falling back to {response.url}"
            )
            return response.url

    def getHash(self, response=None, cleaned_record: ZebisXMLItem = None) -> str:
        if cleaned_record and cleaned_record.datestamp:
            # the <datestamp> can be interpreted as the lastModified date
            return f"{cleaned_record.datestamp}v{self.version}"
        elif cleaned_record and cleaned_record.dc_date:
            # if no <datestamp> was available, we'll resort to <dc:date> as our fallback (creation date)
            return f"{cleaned_record.dc_date}v{self.version}"
        else:
            # if neither datestamps were available, we'll use the current datetime as a final fallback
            _hash_fallback: str = f"{datetime.datetime.now().isoformat()}v{self.version}"
            return _hash_fallback

    def getUUID(self, response=None, cleaned_record: ZebisXMLItem = None) -> str:
        _source_id: str = self.getId(response=response, cleaned_record=cleaned_record)
        return EduSharing.build_uuid(_source_id)

    def check_if_item_should_be_dropped(self, response=None, cleaned_record: ZebisXMLItem = None) -> bool:
        drop_item_flag: bool = False
        _identifier: str = self.getId(response=response, cleaned_record=cleaned_record)
        _hash_str: str = self.getHash(response=response, cleaned_record=cleaned_record)
        if self.shouldImport(response=response) is False:
            self.logger.debug(f"Skipping entry {_identifier} because shouldImport() returned False")
            drop_item_flag = True
            return drop_item_flag
        if _identifier is not None and _hash_str is not None:
            if not self.hasChanged(response=response, cleaned_record=cleaned_record):
                drop_item_flag = True
            return drop_item_flag
        return drop_item_flag

    def hasChanged(self, response=None, cleaned_record: ZebisXMLItem = None) -> bool:
        _identifier: str = self.getId(response=response, cleaned_record=cleaned_record)
        _hash_str: str = self.getHash(response=response, cleaned_record=cleaned_record)
        _uuid_str: str = self.getId(response=response, cleaned_record=cleaned_record)
        if self.forceUpdate:
            return True
        if self.uuid:
            if _uuid_str == self.uuid:
                self.logger.info(f"Matching requested id: {self.uuid}")
                return True
            return False
        if self.remoteId:
            if _identifier == self.remoteId:
                self.logger.info(f"Matching requested id: {self.remoteId}")
                return True
            return False
        db = EduSharing().find_item(id=_identifier, spider=self)
        changed = db is None or db[1] != _hash_str
        if not changed:
            self.logger.info(f"Item {_identifier} (uuid: {db[0]} has not changed.")
        return changed

    def parse(self, response: Response, **kwargs: Any) -> Any:
        self.logger.debug(f"Current item in parse: {response.url}")  # ToDo: remove after debugging
        cleaned_record: ZebisXMLItem = kwargs.get("cleaned_record")
        if not cleaned_record:
            self.logger.error(f"Could not access XML metadata <record> for item {response.url}. Skipping item...")
            return None
        _drop_item: bool = self.check_if_item_should_be_dropped(response=response, cleaned_record=cleaned_record)
        if _drop_item:
            return None

        if self.debug_range_of_values:
            if cleaned_record.dc_audience:
                self.DEBUG_AUDIENCE.update(cleaned_record.dc_audience)
            if cleaned_record.dc_subject:
                self.DEBUG_SUBJECTS.update(cleaned_record.dc_subject)
            if cleaned_record.dc_rights:
                self.DEBUG_RIGHTS.add(cleaned_record.dc_rights)
            if cleaned_record.dc_language:
                self.DEBUG_LANGUAGES.add(cleaned_record.dc_language)
            if cleaned_record.dc_type:
                self.DEBUG_TYPES.update(cleaned_record.dc_type)

        base_itemloader: BaseItemLoader = BaseItemLoader()
        # TODO: fill "base"-keys with values for
        #  - origin             optional    (only necessary if items need to be sorted into a specific sub-folder)
        #  - ai_allow_usage     optional    (filled automatically by the ``RobotsTxtPipeline`` and expects a boolean)
        #                                   indicates if an item is allowed to be used in AI training.
        base_itemloader.add_value("sourceId", self.getId(response=response, cleaned_record=cleaned_record))
        base_itemloader.add_value("hash", self.getHash(response=response, cleaned_record=cleaned_record))
        if cleaned_record.dc_identifier_thumbnail_url and isinstance(cleaned_record.dc_identifier_thumbnail_url, str):
            base_itemloader.add_value("thumbnail", cleaned_record.dc_identifier_thumbnail_url)
        if cleaned_record.datestamp and isinstance(cleaned_record.datestamp, str):
            base_itemloader.add_value("lastModified", cleaned_record.datestamp)

        lom_base_itemloader: LomBaseItemloader = LomBaseItemloader()

        lom_educational_itemloader: LomEducationalItemLoader = LomEducationalItemLoader()
        if cleaned_record.dc_language:
            lom_educational_itemloader.add_value("language", cleaned_record.dc_language)
        if cleaned_record.dc_audience:
            # Zebis provides different metadata categories within <dc:audience>:
            # - class levels (examples range from "1. Klasse" to "9. Klasse")
            # - educational context values ("Kindergarten")
            _class_level_pattern: re.Pattern = re.compile(r"""(?P<class_level>\d{1,2}).\s*Klasse""")
            # this RegEx looks for all strings containing "<digit>. Klasse"
            _class_values: list[int] | None = list()
            for _audience_item in cleaned_record.dc_audience:
                _class_match: re.Match = _class_level_pattern.search(_audience_item)
                if _class_match:
                    _class_value: str = _class_match.group("class_level")
                    if _class_value and _class_value.isdigit():
                        # typecast the string to int before adding it to the list
                        _class_values.append(int(_class_value))

            if _class_values and isinstance(_class_values, list) and len(_class_values) >= 2:
                # determine the typicalAgeRange by using the formula
                # <class_level> + 5 = <typical age for that class level>
                # example conversions:
                # input: "1. Klasse" -> 6 years old
                # input: "7. Klasse" -> 12 years old

                _age_min: int | None = min(_class_values) + 5
                _age_max: int | None = max(_class_values) + 5

                if _age_min and _age_max:
                    lom_age_range_itemloader: LomAgeRangeItemLoader = LomAgeRangeItemLoader()
                    lom_age_range_itemloader.add_value("fromRange", _age_min)
                    lom_age_range_itemloader.add_value("toRange", _age_max)
                    lom_educational_itemloader.add_value("typicalAgeRange", lom_age_range_itemloader.load_item())

        lom_general_itemloader: LomGeneralItemloader = LomGeneralItemloader()
        if cleaned_record.oai_identifier:
            # the OAI identifier will always be the most useful identifier
            # example: <identifier>oai:www.zebis.ch:node-30270</identifier>
            lom_general_itemloader.add_value("identifier", cleaned_record.oai_identifier)
        if cleaned_record.oai_identifier and cleaned_record.dc_identifier_url:
            if cleaned_record.oai_identifier != cleaned_record.dc_identifier_url:
                # the <dc:identifier> might be useful in recognizing duplicate URLs as well
                # example:
                # https://www.zebis.ch/unterrichtsmaterial/unterrichtseinheit-mit-film-charlie-and-chocolate-factory
                lom_general_itemloader.add_value("identifier", cleaned_record.dc_identifier_url)
            if cleaned_record.dc_identifier_url != response.url:
                # in case the resolved URL is different from the <dc:identifier>
                lom_general_itemloader.add_value("identifier", response.url)
        if cleaned_record.dc_title:
            lom_general_itemloader.add_value("title", cleaned_record.dc_title)
        if cleaned_record.dc_subject:
            # <dc:subject> elements are mostly keywords
            # (as of 2025-05-09, the API provides over 2500 unique strings for this field)
            lom_general_itemloader.add_value("keyword", cleaned_record.dc_subject)
        if cleaned_record.dc_description:
            lom_general_itemloader.add_value("description", cleaned_record.dc_description)
        if cleaned_record.dc_language:
            # Zebis provides 3-char values for languages, which are automatically mapped by our LanguageMapper
            # when the item passes through the pipelines
            lom_general_itemloader.add_value("language", cleaned_record.dc_language)

        lom_technical_itemloader: LomTechnicalItemLoader = LomTechnicalItemLoader()
        if cleaned_record.dc_identifier_url:
            lom_technical_itemloader.add_value("location", cleaned_record.dc_identifier_url)
            if response.url != cleaned_record.dc_identifier_url:
                # if the resolved URL is different from the one provided by the Zebis API
                lom_technical_itemloader.add_value("location", response.url)

        if cleaned_record.dc_publisher:
            lifecycle_publisher_itemloader: LomLifecycleItemloader = LomLifecycleItemloader()
            lifecycle_publisher_itemloader.add_value("role", "publisher")
            lifecycle_publisher_itemloader.add_value("organization", cleaned_record.dc_publisher)
            if cleaned_record.dc_date:
                lifecycle_publisher_itemloader.add_value("date", cleaned_record.dc_date)
            lom_base_itemloader.add_value("lifecycle", lifecycle_publisher_itemloader.load_item())

        # ToDo: refactor dc_creator and dc_contributor itemloaders into one method

        # Attention - there can be an author-information mismatch between the OAI-PMH API values
        # and the metadata which is displayed below "Autor/innen"!
        # example: oai:www.zebis.ch:node-77284
        # https://www.zebis.ch/unterrichtsmaterial/informationen-zum-einstieg-den-3d-druck

        if cleaned_record.dc_creator and isinstance(cleaned_record.dc_creator, str):
            # the <dc:creator> is displayed in the Zebis frontend as "Erfasser/in dieses Eintrags":
            # the person is therefore not the author of the item, but rather the metadata creator
            _creator_name: str = cleaned_record.dc_creator
            lifecycle_metadata_creator_itemloader: LomLifecycleItemloader = LomLifecycleItemloader()
            lifecycle_metadata_creator_itemloader.add_value("role", "metadata_creator")
            if "zebis" in _creator_name.lower():
                lifecycle_metadata_creator_itemloader.add_value("organization", _creator_name)
            elif " " in _creator_name:
                _creator_name_split: list[str] = _creator_name.split(sep=" ", maxsplit=1)
                _creator_first_name: str = _creator_name_split[0]
                _creator_last_name: str = _creator_name_split[1]
                lifecycle_metadata_creator_itemloader.add_value("firstName", _creator_first_name)
                lifecycle_metadata_creator_itemloader.add_value("lastName", _creator_last_name)
            else:
                lifecycle_metadata_creator_itemloader.add_value("firstName", _creator_name)
            if cleaned_record.dc_date:
                lifecycle_metadata_creator_itemloader.add_value("date", cleaned_record.dc_date)
            _creator_url: str = response.xpath('//div[@class="user__information--data"]/a/@href').get()
            if _creator_url:
                # the href path points towards a zebis user profile, but needs to be joined with the URL root
                _zebis_user_profile: str | None = response.urljoin(_creator_url)
                if _zebis_user_profile:
                    lifecycle_metadata_creator_itemloader.add_value("url", _zebis_user_profile)

        if cleaned_record.dc_contributor and isinstance(cleaned_record.dc_contributor, str):
            _contributor_name: str = cleaned_record.dc_contributor
            lifecycle_contributor_itemloader: LomLifecycleItemloader = LomLifecycleItemloader()
            lifecycle_contributor_itemloader.add_value("role", "unknown")
            if "zebis" in _contributor_name.lower():
                lifecycle_contributor_itemloader.add_value("organization", _contributor_name)
            elif " " in _contributor_name:
                # split the string into firstName and lastName values
                _contributor_name_split: list[str] = _contributor_name.split(sep=" ", maxsplit=1)
                _contributor_firstname: str = _contributor_name_split[0]
                _contributor_lastname: str = _contributor_name_split[1]
                lifecycle_contributor_itemloader.add_value("firstName", _contributor_firstname)
                lifecycle_contributor_itemloader.add_value("lastName", _contributor_lastname)
            else:
                lifecycle_contributor_itemloader.add_value("firstName", _contributor_name)
            if cleaned_record.dc_date:
                lifecycle_contributor_itemloader.add_value("date", cleaned_record.dc_date)
            lom_base_itemloader.add_value("lifecycle", lifecycle_contributor_itemloader.load_item())

        lom_classification_itemloader: LomClassificationItemLoader = LomClassificationItemLoader()

        vs_itemloader: ValuespaceItemLoader = ValuespaceItemLoader()

        # by default, every item is considered a learning material
        vs_itemloader.add_value("new_lrt", Constants.NEW_LRT_MATERIAL)
        if cleaned_record.dc_type and isinstance(cleaned_record.dc_type, str):
            # <dc:type> -> new_lrt mapping
            _new_lrt_set: set[str] | None = None
            for _dc_type_value in cleaned_record.dc_type:
                if _dc_type_value in self.MAPPING_DC_TYPE_TO_NEW_LRT:
                    _mapped_new_lrt: list[str] = self.MAPPING_DC_TYPE_TO_NEW_LRT.get(_dc_type_value)
                    if _mapped_new_lrt:
                        _new_lrt_set.update(_mapped_new_lrt)
            if _new_lrt_set:
                _new_lrt_list: list[str] = list(_new_lrt_set)
                _new_lrt_list.sort()
                vs_itemloader.add_value("new_lrt", _new_lrt_list)

        vs_itemloader.add_value("containsAdvertisement", "no")
        # zebis doesn't serve ads on their platform (confirmed by looking at random samples on 2025-05-13)
        vs_itemloader.add_value("conditionsOfAccess", "no_login")
        # zebis doesn't require an account for viewing / downloading most of its materials.
        # only a subset of items ("Orientierungshilfen" / "Lingualevel")
        # seem to be account-restricted due to regional license restrictions.

        if cleaned_record.dc_subject and isinstance(cleaned_record.dc_subject, list):
            # the <dc:subject> range of values contains over 2500 strings.
            # most values are considered keywords,
            # but Swiss "Fachbereich"-values need to be mapped manually to their German equivalents
            # since the terminology is too different from our German vocab values most of the time.
            _discipline_set: set[str] = set()
            for _subject in cleaned_record.dc_subject:
                if _subject and isinstance(_subject, str):
                    if _subject in self.MAPPING_DC_SUBJECT_TO_DISCIPLINE:
                        _mapped_discipline: list[str] = self.MAPPING_DC_SUBJECT_TO_DISCIPLINE.get(_subject)
                        if _mapped_discipline:
                            _discipline_set.update(_mapped_discipline)
                    elif _subject:
                        _discipline_set.add(_subject)
            if _discipline_set:
                _discipline_list: list[str] = list(_discipline_set)
                _discipline_list.sort()
                vs_itemloader.add_value("discipline", _discipline_list)

        if cleaned_record.dc_audience and isinstance(cleaned_record.dc_audience, list):
            mapped_educational_context_set: set[str] | None = set()
            for _audience in cleaned_record.dc_audience:  # type: str
                if _audience in self.MAPPING_AUDIENCE_TO_EDUCATIONAL_CONTEXT:
                    # one <dc:audience> maps to several educationalContext values
                    _audience_mapped: list[str] = self.MAPPING_AUDIENCE_TO_EDUCATIONAL_CONTEXT.get(_audience)
                    # collect all mapped values in a set
                    mapped_educational_context_set.update(_audience_mapped)
                else:
                    mapped_educational_context_set.add(_audience)
            if mapped_educational_context_set:
                _educational_context_list: list[str] = list(mapped_educational_context_set)
                _educational_context_list.sort()
                vs_itemloader.add_value("educationalContext", _educational_context_list)

        vs_itemloader.add_value("intendedEndUserRole", "teacher")
        # "Zebis richtet sich hauptsächlich an die 12'000 Lehrerinnen und -lehrer in den Kantonen [...]"
        # see: https://www.zebis.ch/info/hilfe → FAQ: "An wen richtet sich zebis?"

        vs_itemloader.add_value("price", "no")
        # see: https://www.zebis.ch/info/hilfe → FAQ: "Ist zebis kostenpflichtig?"
        # → "Nein, zebis ist ein kostenloses Angebot [...]"
        # but there are exceptions to this rule: "Orientierungsaufgaben" and "Lingualevel" items
        # see: https://www.zebis.ch/info/informationen-zu-den-lizenzpflichtigen-angeboten
        if cleaned_record.dc_subject and "Orientierungsaufgaben" in cleaned_record.dc_subject:
            # see: https://www.zebis.ch/orientierungsaufgaben
            vs_itemloader.replace_value("price", "yes")
            # these materials require an active login / license
            vs_itemloader.replace_value("conditionsOfAccess", "login")
        if cleaned_record.dc_subject and "Lingualevel" in cleaned_record.dc_subject:
            # "Lingualeel"-items are not (yet) provided by the Zebis API,
            # but we assume that those items will be marked in a similar way to "Orientierungsaufgaben",
            # which have their own <dc:subject> value
            # see: https://www.zebis.ch/lingualevel
            vs_itemloader.replace_value("price", "yes")
            vs_itemloader.replace_value("conditionsOfAccess", "login")

        license_itemloader: LicenseItemLoader = LicenseItemLoader()
        # for reference: Zebis Nutzungsbedingungen -> https://www.zebis.ch/node/27345

        _authors_sidebar_clean: str | None = None
        _authors_sidebar_raw: list[str] = response.xpath(
            '//div[@class="zebis-sidebar"]/div[@class="sidebar__information"][h3[text()="Autor/innen"]]/text()'
        ).getall()
        # some materials carry the author information in the zebis sidebar, e.g.
        # https://www.zebis.ch/unterrichtsmaterial/digital-storybook-paz-curious-penguin
        if _authors_sidebar_raw and isinstance(_authors_sidebar_raw, list):
            # the sidebar provides two strings:
            # - one empty string consisting of newlines and whitespaces
            # - one string containing the actual author names (separated by comma if there are multiple authors)
            _authors_sidebar_clean: str = "".join(_authors_sidebar_raw)
            # since there's only one "valid" string within the XPath results, we simply join the strings first
            _authors_sidebar_clean = _authors_sidebar_clean.strip()
            # and then get rid of all the unnecessary whitespaces and newline chars

        _authors_main_clean: str | None = None
        _authors_main_raw: list[str] = response.xpath(
            '//div[contains(text(),"Autor/in")]/following-sibling::div[@class="field__item"]/text()'
        ).getall()
        # some items carry the author information in the main content <div class="zebis-content">
        # https://www.zebis.ch/unterrichtsmaterial/der-vernetzte-wald-zyklus-2
        if _authors_main_raw and isinstance(_authors_main_raw, list):
            _authors_main_clean: str = "".join(_authors_main_raw)
            _authors_main_clean = _authors_main_clean.strip()

        if _authors_sidebar_clean and isinstance(_authors_sidebar_clean, str):
            # the Zebis API does not provide the author names which are found in the sidebar of the DOM
            # the <dc:creator> is described as "Erfasser/in dieses Eintrags"
            # while the actual authors of the item are listed separately
            license_itemloader.add_value("author", _authors_sidebar_clean)
        elif _authors_main_clean and isinstance(_authors_main_clean, str):
            license_itemloader.add_value("author", _authors_main_clean)

        # map from Zebis <dc:rights> strings to edu-sharing "internal"-values:
        if cleaned_record.dc_rights and isinstance(cleaned_record.dc_rights, str):
            _license_mapper: LicenseMapper = LicenseMapper()
            _mapped_license: str | None = _license_mapper.get_license_internal_key(cleaned_record.dc_rights)
            if _mapped_license:
                license_itemloader.add_value("internal", _mapped_license)

        permission_itemloader: PermissionItemLoader = self.getPermissions(response)

        response_itemloader: ResponseItemLoader = ResponseItemLoader()
        response_itemloader.add_value("url", response.url)
        response_itemloader.add_value("status", response.status)
        response_itemloader.add_value("html", response.body)
        _html_body: bytes = response.body
        if _html_body and isinstance(_html_body, bytes):
            trafilatura_text: str | None = trafilatura.extract(_html_body)
            if trafilatura_text:
                response_itemloader.add_value("text", trafilatura_text)
        response_itemloader.add_value("headers", response.headers)

        lom_base_itemloader.add_value("general", lom_general_itemloader.load_item())
        lom_base_itemloader.add_value("classification", lom_classification_itemloader.load_item())
        lom_base_itemloader.add_value("educational", lom_educational_itemloader.load_item())
        lom_base_itemloader.add_value("technical", lom_technical_itemloader.load_item())

        base_itemloader.add_value("lom", lom_base_itemloader.load_item())
        base_itemloader.add_value("license", license_itemloader.load_item())
        base_itemloader.add_value("valuespaces", vs_itemloader.load_item())
        base_itemloader.add_value("permissions", permission_itemloader.load_item())
        base_itemloader.add_value("response", response_itemloader.load_item())
        return base_itemloader.load_item()
