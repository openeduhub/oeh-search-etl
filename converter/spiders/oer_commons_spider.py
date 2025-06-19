import csv
import datetime
from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import dateparser
import scrapy
import trafilatura
from bs4 import BeautifulSoup
from loguru import logger
from playwright.async_api import Page
from scrapy import Request
from scrapy.http import Response

from converter.constants import Constants
from converter.es_connector import EduSharing
from converter.items import (
    BaseItemLoader,
    LicenseItemLoader,
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
from converter.util.fake_user_agent import generate_random_user_agent
from converter.util.license_mapper import LicenseMapper
from converter.web_tools import WebEngine


@dataclass
class OERCommonsCleanedItem:
    date_created: str = None
    description: str = None
    educational_use: list[str] = None
    grade_sublevels: list[str] = None
    keywords: list[str] = None
    languages: list[str] = None
    license_title: str = None
    license_url: str = None
    material_types: list[str] = None
    primary_user: list[str] = None
    provider: str = None
    provider_set: str = None
    subjects: list[str] = None
    title: str = None
    url: str = None


def strip_html_from_text(raw_string: str) -> str | None:
    if raw_string and isinstance(raw_string, str):
        raw_soup = BeautifulSoup(raw_string, "html.parser")
        clean_string: str = raw_soup.get_text(separator=" ", strip=True)
        if clean_string:
            # only return a string if the result is valid (e.g. do not return empty strings)
            return clean_string
        else:
            logger.debug(f"Failed to return a valid, clean string for the provided input:\n{raw_string}")
            return None
    else:
        return None


def clean_and_split_up_string(raw_string: str, separator: str = "|") -> list[str] | None:
    clean_list: list[str] = []
    if raw_string and isinstance(raw_string, str):
        # strip whitespace first
        raw_string = raw_string.strip()
        # individual items are most commonly separated by "|"
        if separator in raw_string:
            items: list[str] = raw_string.split(sep=separator)
            for item in items:
                item = item.strip()
                if item:
                    clean_list.append(item)
            return clean_list
        else:
            # sad case: if no separator was found, we'll return the singular string wrapped in a list
            return [raw_string]
    else:
        logger.debug(
            f"Couldn't split up the provided input into individual strings because of unhandled input type. "
            f"Expected a string, but received {type(raw_string)}. "
            f"Provided value: {raw_string}"
        )
        return None


MAPPING_GRADE_SUBLEVELS_TO_EDU_CONTEXT: dict = {
    "adult-education": "erwachsenenbildung",
    "career-technical": "berufliche_bildung",
    "college-upper-division": "hochschule",
    "community-college-lower-division": "hochschule",
    "graduate-professional": "hochschule",
    "high-school": "sekundarstufe_2",
    "lower-primary": "grundschule",
    "middle-school": "sekundarstufe_1",
    "preschool": "elementarbereich",
    "upper-primary": "grundschule",
}

MAPPING_EDU_USE_TO_EDU_CONTEXT: dict = {
    # "assessment": "",  # ToDo: no mapping possible since this value doesn't translate to educationalContext
    # "curriculum-instruction": "",  # ToDo: no mapping possible
    "informal-education": "informelles_lernen",
    "other": "informelles_lernen",
    "professional-development": "fortbildung",
}

MAPPING_PRIMARY_USERS_TO_INTENDED_ENDUSER_ROLE: dict = {
    "administrator": "manager",
    "librarian": "manager",
}

MAPPING_MATERIAL_TYPES_TO_NEW_LRT: dict = {
    "Activity/Lab": "68a43516-889e-4ce9-8e03-248307bd99ff",  # "offene und kreative Aktivität"
    "Assessment": "9cf3c183-f37c-4b6b-8beb-65f530595dff",  # "Klausur, Klassenarbeit und Test"
    "Case Study": "88da6c0d-e0f9-4f37-a382-5ed7e609de8d",  # Fallstudie
    "Data Set": "345cba59-9fa0-4ec8-ba93-2c75f4a40003",  # Daten
    "Diagram/Illustration": "f7228fb5-105d-4313-afea-66dd59b1b6f8",  # "Graph, Diagramm und Charts"
    "Full Course": "4e16015a-7862-49ed-9b5e-6c1c6e0ffcd1",  # Kurs
    "Game": "a120ce77-59f5-4564-8d49-73f4a0de1594",  # "Lernen, Quiz und Spiel"
    "Homework/Assignment": "1cac68e6-dafe-4ce4-a52f-f33cde26da59",  # "Recherche- und Lernauftrag"
    "Interactive": "4665caac-99d7-4da3-b9fb-498d8ece034f",  # "interaktives Medium"
    "Lecture": "facc2239-a827-462a-b2d2-bbab6cfb1178",  # "Vortrags- und Unterrichtsaufzeichnung"
    "Lecture Notes": "588efe4f-976f-48eb-84aa-8bcb45679f85",  # "Lehr- und Lernmaterial"
    "Lesson": "0d23ff13-9d92-4944-92fa-2b5fe1dde80b",  # Stundenentwurf
    "Lesson Plan": "7381f17f-50a6-4ce1-b3a0-9d85a482eec0",  # Unterrichtsplanung
    "Module": "5098cf0b-1c12-4a1b-a6d3-b3f29621e11d",  # Unterrichtsbaustein
    "Primary Source": "ab5b99ea-551c-42f3-995b-e4b5f469ad7e",  # Primärmaterial
    "Reading": "6a15628c-0e59-43e3-9fc5-9a7f7fa261c4",  # Skript, Handout und Handreichung
    "Simulation": "2e4157ad-e29a-4f10-b4e6-370e0fd59d26",  # Simulation
    "Student Guide": "776652a6-de35-4d2f-817e-6130dd2fa248",  # "Handbuch, Dokumentation und Regularien"
    "Syllabus": "c9fb123f-bd85-4e6e-80c0-96629ece7248",  # "Studien-/Ausbildungsordnung"
    "Teaching/Learning Strategy": "94222751-6c90-4623-9c7e-09e21d885599",  # "Strategie, Aktionsplan"
    "Textbook": "a5897142-bf57-4cd0-bcd9-7d0f1932e87a",  # "Lehrbuch und Grundlagenwerk (auch E-Book)"
    "Unit of Study": "ef58097d-c1de-4e6a-b4da-6f10e3716d3d",  # "Unterrichtseinheit und -sequenz"
}

MAPPING_SUBJECTS_TO_HOCHSCHULFAECHERSYSTEMATIK: dict = {
    "accounting": "n30",  # Business and Economics
    "agriculture": "n58",  # Agricultural Science, Food- and Beverage Technology
    "algebra": "n37",  # Mathematics
    "anatomy-physiology": "n5",  # Humane Medicine / Health Sciences
    "anthropology": "n009",  # Anthropology (Human Biology)
    "applied-science": "n36",  # Mathematics, Natural Sciences (general)
    "archaeology": "n012",  # Archaeology
    "architecture-and-design": "n66",  # Architecture, Interior Architecture
    "art-history": "n092",  # Art History, Art Theory
    "arts-and-humanities": "n1",  # Humanities
    "astronomy": "n014",  # Astrophysics, Astronomy
    "atmospheric-science": "n43",  # Geosciences (excl. Geography)
    "automotive-technology-and-repair": "n235",  #  Automotive Technology
    "biology": "n42",  # Biology
    "botany": "n42",  # Biology
    "business-and-communication": "n30",  # Business and Economics
    "calculus": "n37",  # Mathematics
    "career-and-technical-education": "n0",  # Interdisciplinary
    "chemistry": "n40",  # Chemistry
    "communication": "n34",  # Communication Science/Journalism
    "composition-and-rhetoric": "n10",  # English Studies, American Studies
    "computer-science": "n71",  # Computer Science
    "computing-and-information": "n71",  # Computer Science
    "criminal-justice": "n28",  # Law
    "culinary-arts": "n60",  # Nutritional and Domestic Science
    "cultural-geography": "n44",  # Geography
    "early-childhood-development": "n365",  # Early Childhood Education
    "ecology": "n42",  # Biology
    "economics": "n30",  # Business and Economics
    "education": "n33",  # Educational Sciences
    "educational-technology": "n33",  # Educational Sciences
    "electronic-technology": "n64",  # Electrical Engineering and Information Engineering
    "elementary-education": "n115",  # Primary School Education / Primary Level Education
    "engineering": "n8",  # Engineering Sciences
    "english-language-arts": "n10",  # English Studies, American Studies
    "environmental-science": "n36",  # Mathematics, Natural Sciences (general)
    "environmental-studies": "n44",  # Geography
    "ethnic-studies": "n14",  # Cultural Studies in the narrower sense
    "film-and-music-production": "n77",  # Performing Arts, Film and Television Studies, Theatre Studies
    "finance": "n30",  # Business and Economics
    "forestry-and-agriculture": ["n58", "n59"],
    # "Agricultural Science, Food- and Beverage Technology" / "Forestry, Wood Science"
    "gender-and-sexuality-studies": "n13",  # Other linguistic and cultural studies
    "general-law": "n28",  # Law
    "genetics": "n42",  # Biology
    "geology": "n065",  # Geology/Palaeontology
    "geoscience": "n039",  # Geosciences (general)
    "graphic-arts": "n76",  # Design
    "graphic-design": "n069",  # Graphic Design / Communication Design
    "health-medicine-and-nursing": "n5",  # Human Medicine / Health Sciences
    "higher-education": "n33",  # Educational Sciences
    "history": "n05",  # History
    "history-law-politics": "n25",  # Political Science
    "hydrology": "n43",  # Geosciences (excl. Geography)
    "information-science": "n06",  # Information and Library Sciences
    "intellectual-property-law": "n28",  # Law
    "journalism": "n34",  # Communication Science / Journalism
    "language-education-esl": "n07",  # General and Comparative Literary Studies and Linguistics
    "language-grammar-and-vocabulary": "n07",  # General and Comparative Literary Studies and Linguistics
    "languages": "n07",  # General and Comparative Literary Studies and Linguistics
    "law": "n28",  # Law
    "life-science": "n42",  # Biology
    "linguistics": "n07",  # General and Comparative Literary Studies and Linguistics
    "literature": "n07",  # General and Comparative Literary Studies and Linguistics
    "management": "n30",  # Business and Economics
    "manufacturing": "n202",  # Manufacturing Technology / Production Engineering
    "maritime-science": "n233",  # Nautical Science / Maritime Studies
    "marketing": "n30",  # Business and Economics
    "mathematics": "n37",  # Mathematics
    "measurement-and-data": "n36",  # Mathematics, Natural Sciences (general)
    "numbers-and-operations": "n37",  # Mathematics
    "nutrition": "n60",  # Nutritional Science
    "oceanography": "n124",  # Oceanography
    "performing-arts": "n77",  # Performing Arts, Film and Television Studies, Theatre Studies
    "philosophy": "n04",  # Philosophy
    "physical-geography": "n44",  # Geography
    "physical-science": "n36",  # Mathematics, Natural Sciences (general)
    "physics": "n0128",  # Physics
    "political-science": "n129",  # Political Science
    "psychology": "n132",  # Psychology
    "public-relations": "n34",  # Communication Science / Journalism
    "ratios-and-proportions": "n37",  # Mathematics
    "reading-foundation-skills": "n33",  # Educational Sciences
    "reading-informational-text": "n33",  # Educational Sciences
    "reading-literature": "n07",  # General and Comparative Literary Studies and Linguistics
    "religious-studies": "n136",  # Religious Studies
    "social-science": "n23",  # Law, Economics and Social Sciences (general)
    "social-work": "n208",  # Social Work
    "sociology": "n149",  # Sociology
    "space-science": "n39",  # Physics, Astronomy
    "speaking-and-listening": "n10",  # English Studies, American Studies
    "special-education": "n190",  # Special Needs Education
    "statistics-and-probability": "n312",  # Statistics
    "technology": "n8",  # Engineering Sciences
    "u-s-history": "n273",  # Medieval and Modern History
    "visual-arts": "n023",  # Fine Arts / Graphics
    "world-cultures": "n14",  # Cultural Studies in the narrower sense
    "world-history": "n068",  # History
    "zoology": "n42",
}


class OERCommonsSpider(scrapy.Spider, LomBase):
    name = "oer_commons_spider"
    friendlyName = "OER Commons"
    version = "0.0.3"  # last update: 2025-06-19
    custom_settings = {
        "AUTOTHROTTLE_ENABLED": True,
        "AUTOTHROTTLE_DEBUG": True,
        "AUTOTHROTTLE_TARGET_CONCURRENCY": 2,
        # "CONCURRENT_REQUESTS_PER_DOMAIN": 2,
        "AUTOTHROTTLE_START_DELAY": 3,
        "WEB_TOOLS": WebEngine.Playwright,
        "USER_AGENT": generate_random_user_agent(),
    }

    def __init__(self, **kwargs):
        LomBase.__init__(self, **kwargs)

    def start_requests(self) -> Iterable[Request]:
        yield scrapy.Request(
            url="https://oercommons.org",
            callback=self.read_oer_commons_csv_and_clean_up_items,
            meta={
                "playwright": True,
            },
        )

    async def read_oer_commons_csv_and_clean_up_items(self, response: scrapy.http.Response):
        _cleaned_items: list[OERCommonsCleanedItem] = []
        _root: Path = get_project_root()
        with open(f"{_root}/csv/oer_commons_clean.csv", newline="") as csvfile:
            reader = csv.DictReader(csvfile, delimiter=";")
            for row in reader:
                cleaned_item = OERCommonsCleanedItem()
                try:
                    title: str | None = row["NAME"]
                    if title and isinstance(title, str):
                        title = title.strip()
                    cleaned_item.title = title
                except KeyError:
                    pass

                try:
                    grade_sublevels_raw: str | None = row["GRADE_SUBLEVELS"]
                    if grade_sublevels_raw and isinstance(grade_sublevels_raw, str):
                        grade_sublevels_clean: list[str] = clean_and_split_up_string(raw_string=grade_sublevels_raw)
                        if grade_sublevels_clean:
                            # ToDo: map grade_sublevels!
                            cleaned_item.grade_sublevels = grade_sublevels_clean
                except KeyError:
                    pass

                try:
                    subjects_raw: str | None = row["SUBJECTS"]
                    if subjects_raw and isinstance(subjects_raw, str):
                        subjects_clean: list[str] | None = clean_and_split_up_string(raw_string=subjects_raw)
                        if subjects_clean:
                            cleaned_item.subjects = subjects_clean
                except KeyError:
                    pass

                try:
                    educational_use_raw: str | None = row["EDUCATIONAL_USE"]
                    if educational_use_raw and isinstance(educational_use_raw, str):
                        edu_use_clean: list[str] | None = clean_and_split_up_string(raw_string=educational_use_raw)
                        if edu_use_clean:
                            cleaned_item.educational_use = edu_use_clean
                except KeyError:
                    pass

                try:
                    # language values are 2-char language codes
                    languages_raw: str | None = row["LANGUAGES"]
                    if languages_raw and isinstance(languages_raw, str):
                        languages_clean: list[str] | None = clean_and_split_up_string(raw_string=languages_raw)
                        if languages_clean:
                            cleaned_item.languages = languages_clean
                except KeyError:
                    pass

                try:
                    license_url: str | None = row["LICENSE_URL"]
                    if license_url and isinstance(license_url, str):
                        license_url: str = license_url.strip()
                        cleaned_item.license_url = license_url
                except KeyError:
                    pass

                try:
                    license_title: str | None = row["LICENSE_TITLE"]
                    if license_title and isinstance(license_title, str):
                        license_title: str = license_title.strip()
                        cleaned_item.license_title = license_title
                except KeyError:
                    pass

                try:
                    provider: str | None = row["PROVIDER"]
                    if provider and isinstance(provider, str):
                        provider: str = provider.strip()
                        if provider:
                            cleaned_item.provider = provider
                except KeyError:
                    pass

                try:
                    provider_set: str | None = row["PROVIDER_SET"]
                    if provider_set and isinstance(provider_set, str):
                        provider_set: str = provider_set.strip()
                        if provider_set:
                            # provider_set is empty in >99% of cases
                            # ToDo: map provider_set to ...?
                            cleaned_item.provider_set = provider_set
                except KeyError:
                    pass

                try:
                    material_types_raw: str | None = row["MATERIAL_TYPES"]
                    if material_types_raw and isinstance(material_types_raw, str):
                        material_types_clean: list[str] | None = clean_and_split_up_string(
                            raw_string=material_types_raw
                        )
                        if material_types_clean:
                            cleaned_item.material_types = material_types_clean
                except KeyError:
                    pass

                try:
                    # the PRIMARY_USER column can be understood as the target group (-> intendedEndUserRole)
                    primary_user_raw: str | None = row["PRIMARY_USER"]
                    if primary_user_raw and isinstance(primary_user_raw, str):
                        primary_user_clean: list[str] | None = clean_and_split_up_string(raw_string=primary_user_raw)
                        if primary_user_clean:
                            cleaned_item.primary_user = primary_user_clean
                except KeyError:
                    pass

                try:
                    date_created_raw: str = row["CREATE_DATE"]
                    if date_created_raw and isinstance(date_created_raw, str):
                        date_created_raw: str = date_created_raw.strip()
                        if date_created_raw:
                            date_created_dt = dateparser.parse(date_string=date_created_raw)
                            if date_created_dt:
                                date_created = date_created_dt.isoformat()
                                cleaned_item.date_created = date_created
                except KeyError:
                    pass

                try:
                    # teacher_overview consists of the basic description
                    teacher_overview_raw: str | None = row["TEACHER_OVERVIEW"]
                    if teacher_overview_raw and isinstance(teacher_overview_raw, str):
                        teacher_overview_cleaned: str | None = strip_html_from_text(raw_string=teacher_overview_raw)
                        teacher_description = f"Overview:\n{teacher_overview_cleaned}"

                    # description: lesson preparation (optional)
                    teacher_lesson_prep_raw: str | None = row["TEACHER_LESSON_PREPARATION"]
                    if teacher_lesson_prep_raw and isinstance(teacher_lesson_prep_raw, str):
                        teacher_lesson_prep_clean = strip_html_from_text(raw_string=teacher_lesson_prep_raw)
                        if teacher_lesson_prep_clean:
                            teacher_description = (
                                f"{teacher_description}\n\nLesson Preparation:\n{teacher_lesson_prep_clean}"
                            )

                    # description: teacher materials, e.g.: a reading list of relevant books (optional)
                    teacher_materials_raw: str | None = row["TEACHER_MATERIALS"]
                    if teacher_materials_raw and isinstance(teacher_materials_raw, str):
                        teacher_materials_cleaned: str = strip_html_from_text(raw_string=teacher_materials_raw)
                        if teacher_materials_cleaned:
                            teacher_description = (
                                f"{teacher_description}\n\nTeacher Materials:\n{teacher_materials_cleaned}"
                            )

                    # after all 3 descriptions have been combined, the description is ready to be saved:
                    teacher_description: str = teacher_description.strip()
                    cleaned_item.description = teacher_description
                except KeyError:
                    pass

                try:
                    keywords_raw: str | None = row["KEYWORDS"]
                    if keywords_raw and isinstance(keywords_raw, str):
                        keywords_clean: str = strip_html_from_text(raw_string=keywords_raw)
                        if keywords_clean and isinstance(keywords_clean, str):
                            keywords_list: list[str] | None = clean_and_split_up_string(raw_string=keywords_clean)
                            cleaned_item.keywords = keywords_list
                except KeyError:
                    pass

                try:
                    url_raw: str | None = row["URL"]
                    if url_raw and isinstance(url_raw, str):
                        url_clean: str = url_raw.strip()
                        if url_clean:
                            cleaned_item.url = url_clean
                except KeyError:
                    pass

                _cleaned_items.append(cleaned_item)
                # ToDo: remove _cleaned_items list after debugging to save RAM?
                # final_item = await self.parse(cleaned_item=cleaned_item)
                # yield final_item
                yield scrapy.Request(
                    url=url_clean,
                    callback=self.parse,
                    cb_kwargs={"cleaned_item": cleaned_item},
                    meta={
                        "playwright": True,
                        "playwright_include_page": True,
                    },
                    errback=self.errback_close_page,
                )
        logger.debug(f"Total amount of CSV items (after clean up): {len(_cleaned_items)}")

    def getId(self, response=None, cleaned_item: OERCommonsCleanedItem = None) -> str | None:
        if response.url and isinstance(response.url, str):
            return response.url
        elif cleaned_item.url and isinstance(cleaned_item.url, str):
            return cleaned_item.url
        else:
            logger.error(f"getId() failed because the item didn't contain a URL: {cleaned_item}")
            return None

    def getHash(self, response=None, cleaned_item: OERCommonsCleanedItem = None) -> str | None:
        if cleaned_item.date_created and isinstance(cleaned_item.date_created, str):
            _hash: str = f"{cleaned_item.date_created}v{self.version}"
            return _hash
        else:
            logger.warning(f"getHash() failed because the item didn't contain a date: {cleaned_item}")
            _hash: str = f"{datetime.datetime.now().isoformat()}v{self.version}"
            return _hash

    def getUUID(self, response=None, cleaned_item: OERCommonsCleanedItem = None) -> str:
        # this method has been re-implemented since we cannot use a scrapy.http.Response to determine the URL
        _source_id: str = self.getId(response=response, cleaned_item=cleaned_item)
        return EduSharing.build_uuid(_source_id)

    def hasChanged(self, response=None, cleaned_item: OERCommonsCleanedItem = None) -> bool:
        # this method has been re-implemented since we don't have a valid ``scrapy.http.Response`` to work with,
        # which breaks the inherited methods from ``LomBase``
        _identifier: str = self.getId(response=response, cleaned_item=cleaned_item)
        _hash_str: str = self.getHash(response=response, cleaned_item=cleaned_item)
        _uuid_str: str = self.getUUID(response=response, cleaned_item=cleaned_item)
        if self.forceUpdate:
            return True
        if self.uuid:
            if _uuid_str == self.uuid:
                logger.info(f"Matching requested id: {self.uuid}")
                return True
            return False
        if self.remoteId:
            if _identifier == self.remoteId:
                logger.info(f"Matching requested id: {self.remoteId}")
                return True
            return False
        db = EduSharing().find_item(id=_identifier, spider=self)
        changed = db is None or db[1] != _hash_str
        if not changed:
            logger.info(f"Item {_identifier} (uuid: {db[0]} has not changed.")
        return changed

    def check_if_item_should_be_dropped(self, response=None, cleaned_item: OERCommonsCleanedItem = None) -> bool:
        """
        Check if item should be dropped (before making any further HTTP Requests).
        This could happen for reasons like "the hash has not changed"
        (= the object has not changed since the last crawling process),
        or if the ``shouldImport``-attribute was set to ``False``.

        :param response: Typically, this would be a ``scrapy.http.Response``,
            but in this case we expect it to be ``None``
            (due to OERCommons blocking any HTTP requests made by scrapy).
        :param cleaned_item: the cleaned-up CSV item ``OERCommonsCleanedItem``
        :return: return ``True`` if the item needs to be dropped.
            Otherwise, return ``False``
        """
        drop_item_flag: bool = False
        _identifier: str = self.getId(response=response, cleaned_item=cleaned_item)
        _hash_str: str = self.getHash(response=response, cleaned_item=cleaned_item)
        if self.shouldImport(response=response) is False:
            logger.debug(f"Skipping entry {_identifier} because shouldImport() returned False")
            drop_item_flag = True
            return drop_item_flag
        if _identifier is not None and _hash_str is not None:
            if not self.hasChanged(response=response, cleaned_item=cleaned_item):
                drop_item_flag = True
            return drop_item_flag
        return drop_item_flag

    async def errback_close_page(self, failure):
        # close the Playwright Page object in case of exceptions (to mitigate open tabs causing the spider to freeze)
        page: Page = failure.request.meta["playwright_page"]
        await page.close()

    async def parse(self, response: Response, **kwargs: Any) -> Any:
        _cleaned_item: OERCommonsCleanedItem = kwargs.get("cleaned_item")
        _page: Page | None = None  # the playwright Page object (if available)
        # see: https://github.com/scrapy-plugins/scrapy-playwright?tab=readme-ov-file#playwright_page
        try:
            _page: Page = response.meta["playwright_page"]
        except KeyError:
            logger.debug(f"Playwright Page object was not available for {response.url}")
            pass

        # to minimize the amount of HTTP requests caused by our crawler, we check first if the item needs to be dropped
        _drop_item: bool = self.check_if_item_should_be_dropped(response=response, cleaned_item=_cleaned_item)
        if _drop_item:
            return

        _source_id: str | None = self.getId(response=response, cleaned_item=_cleaned_item)
        if not _source_id:
            # drop item if the item has no URL
            return

        base_itemloader: BaseItemLoader = BaseItemLoader()
        base_itemloader.add_value("sourceId", _source_id)
        _hash: str | None = self.getHash(response=response, cleaned_item=_cleaned_item)
        base_itemloader.add_value("hash", _hash)

        # author metadata is only available in the "Details"-Tab of an OERCommons item
        # and consists of one single author name string
        _author_names: str | None = None
        _author_urls: str | None = None
        html_body = None
        if _page:
            html_body = await _page.content()
            if html_body and isinstance(html_body, bytes):
                trafilatura_text: str | None = trafilatura.extract(html_body)
                if trafilatura_text:
                    base_itemloader.add_value("fulltext", trafilatura_text)
            screenshot_bytes = await _page.screenshot()
            if screenshot_bytes:
                base_itemloader.add_value("screenshot_bytes", screenshot_bytes)

        # some items have multiple authors mentioned in the info box on the right,
        # e.g.: https://oercommons.org/courseware/lesson/116317/overview
        _author_names: list[str] | None = response.xpath(
            '//dt[contains(text(),"Author:")]/following-sibling::dd/a/text()'
        ).getall()
        _author_urls: list[str] | None = response.xpath(
            '//dt[contains(text(),"Author:")]/following-sibling::dd/a/@href'
        ).getall()

        lom_base_itemloader: LomBaseItemloader = LomBaseItemloader()

        lom_general_itemloader: LomGeneralItemloader = LomGeneralItemloader()
        lom_general_itemloader.add_value("identifier", _source_id)
        if _cleaned_item.title and isinstance(_cleaned_item.title, str):
            lom_general_itemloader.add_value("title", _cleaned_item.title)
        if _cleaned_item.description and isinstance(_cleaned_item.description, str):
            lom_general_itemloader.add_value("description", _cleaned_item.description)
        if _cleaned_item.languages and isinstance(_cleaned_item.languages, list):
            lom_general_itemloader.add_value("language", _cleaned_item.languages)

        lom_technical_itemloader: LomTechnicalItemLoader = LomTechnicalItemLoader()
        lom_technical_itemloader.add_value("location", _source_id)
        # lom_technical_itemloader.add_value("format", "text/html")

        if _cleaned_item.provider and isinstance(_cleaned_item.provider, str):
            # provider and provider_set are empty in 99% of cases
            lifecycle_provider_itemloader: LomLifecycleItemloader = LomLifecycleItemloader()
            lifecycle_provider_itemloader.add_value("role", "metadata_provider")
            lifecycle_provider_itemloader.add_value("organization", _cleaned_item.provider)
            if _cleaned_item.date_created and isinstance(_cleaned_item.date_created, str):
                lifecycle_provider_itemloader.add_value("date", _cleaned_item.date_created)
            lom_base_itemloader.add_value("lifecycle", lifecycle_provider_itemloader.load_item())

        # LOM Lifecycle author metadata:
        if _author_names and _author_urls:
            _zipped_authors_and_urls = zip(_author_names, _author_urls, strict=False)
            # we expect each author to have its own profile page at OER Commons
            _authors_and_urls: list[tuple] = list(_zipped_authors_and_urls)
            if _authors_and_urls:
                for _author_name, _author_url in _authors_and_urls:
                    if _author_name and isinstance(_author_name, str):
                        lifecycle_author_itemloader: LomLifecycleItemloader = LomLifecycleItemloader()
                        lifecycle_author_itemloader.add_value("role", "author")
                        # split author name by firstName / lastname:
                        author_split: list[str] = _author_name.split(sep=" ", maxsplit=1)
                        if author_split and len(author_split) == 2:
                            # since we cannot cover each edge case individually
                            # (there are persons with multiple names, organizations with multiple nouns etc.)
                            # we assume that the whitespace separates an author's first and last name
                            lifecycle_author_itemloader.add_value("firstName", author_split[0])
                            lifecycle_author_itemloader.add_value("lastName", author_split[1])
                        else:
                            # if splitting the name isn't possible, fallback to saving the whole name in one field
                            lifecycle_author_itemloader.add_value("firstName", _author_name)
                        if _author_url:
                            lifecycle_author_itemloader.add_value("url", _author_url)
                        if _cleaned_item.date_created and isinstance(_cleaned_item.date_created, str):
                            lifecycle_author_itemloader.add_value("date", _cleaned_item.date_created)
                        lom_base_itemloader.add_value("lifecycle", lifecycle_author_itemloader.load_item())

        # hard-coded OERCommons.org metadata:
        lifecycle_publisher_itemloader: LomLifecycleItemloader = LomLifecycleItemloader()
        lifecycle_publisher_itemloader.add_value("role", "publisher")
        lifecycle_publisher_itemloader.add_value("organization", "OER Commons")
        lifecycle_publisher_itemloader.add_value("url", "https://oercommons.org/")
        lom_base_itemloader.add_value("lifecycle", lifecycle_publisher_itemloader.load_item())

        lom_educational_itemloader: LomEducationalItemLoader = LomEducationalItemLoader()
        if _cleaned_item.languages and isinstance(_cleaned_item.languages, list):
            lom_educational_itemloader.add_value("language", _cleaned_item.languages)

        lom_classification_itemloader: LomClassificationItemLoader = LomClassificationItemLoader()

        valuespace_itemloader: ValuespaceItemLoader = ValuespaceItemLoader()
        # TODO: fill "valuespaces"-keys with values for
        #  - conditionsOfAccess             recommended
        #  (see: https://github.com/openeduhub/oeh-metadata-vocabs/blob/master/conditionsOfAccess.ttl)
        #  - containsAdvertisement          recommended
        #  (see: https://github.com/openeduhub/oeh-metadata-vocabs/blob/master/containsAdvertisement.ttl)
        #  - price                          recommended
        #  (see: https://github.com/openeduhub/oeh-metadata-vocabs/blob/master/price.ttl)

        # these sets are necessary because OERCommons uses a different range of values for different properties,
        # which end up in singular fields of our crawler and the edu-sharing backend
        _new_lrt_mapped: set = set()
        _educational_context_mapped: set = set()

        # EDUCATIONAL_USE / GRADE_SUBLEVELS -> educationalContext vocab
        if _cleaned_item.educational_use and isinstance(_cleaned_item.educational_use, list):
            for edu_use_item in _cleaned_item.educational_use:
                if edu_use_item in MAPPING_EDU_USE_TO_EDU_CONTEXT:
                    _educational_context_mapped.add(MAPPING_EDU_USE_TO_EDU_CONTEXT.get(edu_use_item))
                if edu_use_item == "assessment":
                    _new_lrt_mapped.add(edu_use_item)
        if _cleaned_item.grade_sublevels and isinstance(_cleaned_item.grade_sublevels, list):
            for grade_item in _cleaned_item.grade_sublevels:
                if grade_item in MAPPING_GRADE_SUBLEVELS_TO_EDU_CONTEXT:
                    _educational_context_mapped.add(MAPPING_GRADE_SUBLEVELS_TO_EDU_CONTEXT.get(grade_item))
        if _educational_context_mapped:
            valuespace_itemloader.add_value("educationalContext", list(_educational_context_mapped))

        # PRIMARY_USER -> intendedEndUserRole ("Zielgruppe") vocab
        if _cleaned_item.primary_user and isinstance(_cleaned_item.primary_user, list):
            for primary_user_item in _cleaned_item.primary_user:
                if primary_user_item in MAPPING_PRIMARY_USERS_TO_INTENDED_ENDUSER_ROLE:
                    # save the mapped value
                    valuespace_itemloader.add_value(
                        "intendedEndUserRole", MAPPING_PRIMARY_USERS_TO_INTENDED_ENDUSER_ROLE.get(primary_user_item)
                    )
                else:
                    # if the OER Commons value doesn't differ from our vocab
                    valuespace_itemloader.add_value("intendedEndUserRole", primary_user_item)

        if _cleaned_item.material_types and isinstance(_cleaned_item.material_types, list):
            for material_type_item in _cleaned_item.material_types:
                if material_type_item in MAPPING_MATERIAL_TYPES_TO_NEW_LRT:
                    # save mapped value to new_lrt if possible
                    valuespace_itemloader.add_value(
                        "new_lrt", MAPPING_MATERIAL_TYPES_TO_NEW_LRT.get(material_type_item)
                    )
                else:
                    # if there's no mapping, add the unmapped string to the list of keywords
                    lom_general_itemloader.add_value("keyword", material_type_item)
        else:
            valuespace_itemloader.add_value("new_lrt", Constants.NEW_LRT_MATERIAL)

        _hochschulfaecher_mapped: set = set()
        _subjects_as_additional_keywords: set = set()
        # the names of the subjects have their own meaning, which might get lost in translation;
        # therefore, we clean up the subject strings and save them as keywords
        if _cleaned_item.subjects and isinstance(_cleaned_item.subjects, list):
            for subject_item in _cleaned_item.subjects:
                if subject_item in MAPPING_SUBJECTS_TO_HOCHSCHULFAECHERSYSTEMATIK:
                    mapped_subject: str | list[str] = MAPPING_SUBJECTS_TO_HOCHSCHULFAECHERSYSTEMATIK.get(subject_item)
                    if mapped_subject and isinstance(mapped_subject, str):
                        _hochschulfaecher_mapped.add(mapped_subject)
                    if mapped_subject and isinstance(mapped_subject, list):
                        _hochschulfaecher_mapped.update(mapped_subject)
                if subject_item and isinstance(subject_item, str) and "-" in subject_item:
                    auxiliary_keyword: str = subject_item.replace("-", " ")
                    if auxiliary_keyword:
                        auxiliary_keyword = auxiliary_keyword.strip()
                        _subjects_as_additional_keywords.add(auxiliary_keyword)
        if _hochschulfaecher_mapped:
            hochschulfaecher: list[str] = list(_hochschulfaecher_mapped)
            hochschulfaecher.sort()
            valuespace_itemloader.add_value("hochschulfaechersystematik", hochschulfaecher)

        # the imported tags from the .csv are incomplete, which is why we need to check the DOM as well
        _tags: list[str] | None = response.xpath('//li[@class="tag-instance keyword"]/a/text()').getall()
        # merge keywords
        _keyword_set: set[str] = set()
        if _cleaned_item.keywords and isinstance(_cleaned_item.keywords, list):
            _keyword_set.update(_cleaned_item.keywords)
        if _subjects_as_additional_keywords:
            _keyword_set.update(_subjects_as_additional_keywords)
        if _tags and isinstance(_tags, list):
            _keyword_set.update(_tags)
        if _keyword_set:
            keywords: list[str] = list(_keyword_set)
            keywords.sort()
            lom_general_itemloader.add_value("keyword", keywords)

        license_itemloader: LicenseItemLoader = LicenseItemLoader()
        if _author_names and isinstance(_author_names, list):
            _authors_combined: str = ", ".join(_author_names)
            license_itemloader.add_value("author", _authors_combined)
        if _cleaned_item.license_url and isinstance(_cleaned_item.license_url, str):
            _mapped_license_url: str = LicenseMapper().get_license_url(license_string=_cleaned_item.license_url)
            license_itemloader.add_value("url", _mapped_license_url)
        elif _cleaned_item.license_title and isinstance(_cleaned_item.license_title, str):
            _mapped_license: str | None = LicenseMapper().get_license_internal_key(
                license_string=_cleaned_item.license_title
            )
            if _mapped_license:
                license_itemloader.add_value("internal", _mapped_license)

        permission_itemloader: PermissionItemLoader = self.getPermissions(response)

        response_itemloader: ResponseItemLoader = ResponseItemLoader()
        response_itemloader.add_value("url", _source_id)
        if html_body:
            response_itemloader.replace_value("html", html_body)
        if response.text:
            response_itemloader.replace_value("text", response.text)

        lom_base_itemloader.add_value("general", lom_general_itemloader.load_item())
        lom_base_itemloader.add_value("technical", lom_technical_itemloader.load_item())
        lom_base_itemloader.add_value("educational", lom_educational_itemloader.load_item())
        lom_base_itemloader.add_value("classification", lom_classification_itemloader.load_item())

        base_itemloader.add_value("lom", lom_base_itemloader.load_item())
        base_itemloader.add_value("license", license_itemloader.load_item())
        base_itemloader.add_value("valuespaces", valuespace_itemloader.load_item())
        base_itemloader.add_value("permissions", permission_itemloader.load_item())
        base_itemloader.add_value("response", response_itemloader.load_item())

        return base_itemloader.load_item()


if __name__ == "__main__":
    # ToDo: oercommons.org blocks both scrapy and playwright with a 403 response!
    #   - find a workaround for thumbnails
    pass
