import logging
from datetime import datetime

import scrapy.selector.unified
import w3lib.html
from scrapy.spiders import XMLFeedSpider

from converter import env
from converter.constants import Constants
from converter.es_connector import EduSharing
from converter.items import (
    BaseItemLoader,
    LomBaseItemloader,
    LomGeneralItemloader,
    LomTechnicalItemLoader,
    LomLifecycleItemloader,
    LomEducationalItemLoader,
    ValuespaceItemLoader,
    LicenseItemLoader,
    ResponseItemLoader,
)
from converter.spiders.base_classes import LomBase


class LehrerOnlineSpider(XMLFeedSpider, LomBase):
    name = "lehreronline_spider"
    friendlyName = "Lehrer-Online"
    start_urls = [
        "https://www.lehrer-online.de/?type=3030&limit=10000"
        # the limit parameter controls the amount of results PER CATEGORY (NOT the total amount of results)
        # API response with a "limit"-value set to 10.000 might take more than 90s (17.7 MB, 5912 URLs to crawl)
    ]
    version = "0.0.7"  # last update: 2023-08-10
    custom_settings = {
        "ROBOTSTXT_OBEY": False,
        "AUTOTHROTTLE_ENABLED": True,
        "AUTOTHROTTLE_DEBUG": True,
        # "DUPEFILTER_DEBUG": True
    }
    iterator = "iternodes"
    itertag = "datensatz"

    MAPPING_EDU_CONTEXT = {
        "Elementarbildung": "elementarbereich",
        "Fort- und Weiterbildung": "fortbildung",
        "Spezieller Förderbedarf": "foerderschule",
    }

    MAPPING_LO_LRT_TO_NEW_LRT = {
        # Lehrer-Online uses a different vocabulary for their "lernressourcentyp"
        "Ablaufplan": "7381f17f-50a6-4ce1-b3a0-9d85a482eec0",  # "Unterrichtsplanung" # ToDo: confirm this mapping
        "Arbeitsblatt": "36e68792-6159-481d-a97b-2c00901f4f78",  # Arbeitsblatt
        "Arbeitsblatt interaktiv": "36e68792-6159-481d-a97b-2c00901f4f78",  # Arbeitsblatt
        # "Arbeitsheft": "",
        "Außerschulischer Lernort": "92dcc3ec-fe94-451c-95ac-ea305e0e7597",  # "außerschulisches Angebot"
        "Didaktik/Methodik": "477115fd-5042-4174-ac39-7c05f8a24766",  # "pädagogische Methode, Konzept"
        "Diskussion": "61462395-8303-44bf-95a4-6a4297013283",
        # "Argumentation, Plattformen für strukturierte Diskussion" # ToDo: this is a "Tool"
        # "Einzelarbeit": "",
        "Experiment": "4735c61a-429b-4909-9f3c-cbf975e2aa0e",  # "Experiment"
        "Folien": "92c7a50c-6243-45d9-8b11-e79cbbda6305",  # "Präsentation"
        # "Hausaufgabe": "",
        "Interaktives Quiz": "a120ce77-59f5-4564-8d49-73f4a0de1594",
        "Lernen, Quiz und Spiel"
        # "Internetressource": "",
        "Kurs": "4e16015a-7862-49ed-9b5e-6c1c6e0ffcd1",  # "Kurs"
        "Lehrer-Begleitheft": "6a15628c-0e59-43e3-9fc5-9a7f7fa261c4",  # "Skript, Handout und Handreichung"
        "Lehrerhandreichung": "6a15628c-0e59-43e3-9fc5-9a7f7fa261c4",  # "Skript, Handout und Handreichung"
        # "Lehrerheft": "",
        "Lernkontrolle": "9cf3c183-f37c-4b6b-8beb-65f530595dff",  # "Klausur, Klassenarbeit und Test"
        "Lernspiel": "b0495f44-b05d-4bde-9dc5-34d7b5234d76",  # "Lernspiel"
        "Nachrichten": "dc5763ab-6f47-4aa3-9ff3-1303efbeef6e",  # "Nachrichten und Neuigkeiten"
        "Nachschlagewerk": "c022c920-c236-4234-bae1-e264a3e2bdf6",  # "Nachschlagewerk und Glossar"
        "Poster": "c382a478-74e0-42f1-96dd-fcfb5c27f746",  # "Poster und Plakat"
        "Primärmaterial": "ab5b99ea-551c-42f3-995b-e4b5f469ad7e",  # "Primärmaterial und Quelle"
        "Projekt": "22823ca9-7175-4b24-892e-19ebbf5fe0e7",  # "Projekt (Lehr- und Lernmaterial)"
        "Präsentation": "92c7a50c-6243-45d9-8b11-e79cbbda6305",  # "Präsentation"
        "Quiz": "7d591b84-9171-47cb-809a-74ef07f07261",  # "Quiz" # ToDo: this is a "Tool", not a "Material"
        "Recherche-Auftrag": "1cac68e6-dafe-4ce4-a52f-f33cde26da59",  # "Recherche und Lernauftrag"
        "Rollenspiel": "ac82dc13-3be1-464d-9cdc-88e608d99c39",  # "Rollenspiel"
        "Schaubild": "1dc4ed81-718c-4b76-86cb-947a86875973",  # "Veranschaulichung, Schaubild und Tafelbild"
        "Schülerheft": "a33ef73d-9210-4305-97f9-7357bbf43486",  # Übungsmaterial
        # "Schülermagazin": "",
        "Software": "cefccf75-cba3-427d-9a0f-35b4fedcbba1",  # Tool
        "Stationenlernen": "ee738203-44af-4150-986f-ef01fb883f00",  # "Stationenlernen"
        "Tondokument": "ec2682af-08a9-4ab1-a324-9dca5151e99f",  # "Audio"
        "Video": "7a6e9608-2554-4981-95dc-47ab9ba924de",  # Video
        "Webquest": "1cac68e6-dafe-4ce4-a52f-f33cde26da59",  # "Recherche- und Lernauftrag"
        "entdeckendes Lernen": "9a86beb5-1a65-48ca-99c8-e8c789cfe2f8",  # "Entdeckendes Lernen (Lehr- und Lernmaterial)"
        # "kooperatives Lernen": "",
        "Übung": "a33ef73d-9210-4305-97f9-7357bbf43486",  # Übungsmaterial
    }

    MAPPING_MATERIAL_TYPE_TO_NEW_LRT = {
        "Blog": "5204fc81-5dac-4cc4-a28b-aad5c241fa19",  # "Webblog (dynamisch)"
        "Cartoon": "667f5063-70b9-400c-b1f7-7702ec9487f1",  # "Cartoon, Comic"
        "Dossier": "7381f17f-50a6-4ce1-b3a0-9d85a482eec0",  # "Unterrichtsplanung"
        # Dossiers are hard to categorize, they typically consist of several types (news, "Unterrichtseinheit" etc.)
        # that are put together as a "Fokusthema", similar to how Umwelt-im-Unterricht.de groups together several
        # articles into a "Thema der Woche"
        "Fachartikel": "b98c0c8c-5696-4537-82fa-dded7236081e",  # "Artikel und Einzelpublikation"
        "Fundstueck": "dc5763ab-6f47-4aa3-9ff3-1303efbeef6e",  # "Nachrichten und Neuigkeiten
        "Interaktives": "4665caac-99d7-4da3-b9fb-498d8ece034f",  # "Interaktives Medium"
        "Kopiervorlage": "6a15628c-0e59-43e3-9fc5-9a7f7fa261c4",  # "Skript, Handout und Handreichung"
        "News": "dc5763ab-6f47-4aa3-9ff3-1303efbeef6e",  # "Nachrichten und Neuigkeiten"
        "Rechtsfall": "dc5763ab-6f47-4aa3-9ff3-1303efbeef6e",  # "Nachrichten und Neuigkeiten"
        # ToDo: could this be mapped to either "Fachliche News", "Alltags News" or "Pädagogische News"?
        "Unterrichtseinheit": "ef58097d-c1de-4e6a-b4da-6f10e3716d3d",  # "Unterrichtseinheit"
        "Videos": "7a6e9608-2554-4981-95dc-47ab9ba924de",  # "Video (Material)"
    }

    MAPPING_RIGHTS_TO_URLS = {
        "CC-by": Constants.LICENSE_CC_BY_30,
        "CC-by-nc": Constants.LICENSE_CC_BY_NC_30,
        "CC-by-nc-nd": Constants.LICENSE_CC_BY_NC_ND_30,
        "CC-by-nc-nd 4.0": Constants.LICENSE_CC_BY_NC_ND_40,
        "CC-by-nc-sa": Constants.LICENSE_CC_BY_NC_SA_30,
        "CC-by-nc-sa 4.0": Constants.LICENSE_CC_BY_NC_SA_40,
        "CC-by-nd": Constants.LICENSE_CC_BY_ND_30,
        "CC-by-sa": Constants.LICENSE_CC_BY_SA_30,
        "CC-by-sa 4.0": Constants.LICENSE_CC_BY_SA_40,
    }

    MAPPING_FACH_TO_DISCIPLINES = {
        "Arbeitsschutz und Arbeitssicherheit": "Arbeitssicherheit",
        "Berufs- und Arbeitswelt": "Arbeitslehre",
        "Berufsvorbereitung, Berufsalltag, Arbeitsrecht": "Arbeitslehre",
        "Ernährung und Gesundheit": ["Ernährung und Hauswirtschaft", "Gesundheit"],
        "Fächerübergreifender Unterricht": "Allgemein",
        "Geschichte, Politik und Gesellschaftswissenschaften": ["Geschichte", "Politik", "Gesellschaftskunde"],
        "Gesundheit und Gesundheitsschutz": "Gesundheit",
        "Informationstechnik": "Informatik",
        "Klima, Umwelt, Nachhaltigkeit": "Nachhaltigkeit",
        "MINT: Mathematik, Informatik, Naturwissenschaften und Technik": "MINT",
        "Natur und Umwelt": ["Environmental education", "Homeland lessons"],  # Umwelterziehung, Sachunterricht
        "Religion und Ethik": ["Religion", "Ethik"],
        "Sport und Bewegung": "Sport",
        "SoWi": ["Social education", "Economics"],
        "WiSo": ["Economics", "Social education"],
        "Wirtschaftslehre": "Economics",
    }

    def getId(self, response=None, **kwargs) -> str:
        # By the time we call this method, there is no usable 'response.url' available (the URL would point to the API
        # for each item), which is why we need to use the metadata dictionary from the API Response here.
        try:
            material_url = kwargs["kwargs"]["metadata_dict"]["url"]
            return material_url
        except KeyError:
            logging.error(f"'getId'-method could not retrieve metadata_dict['url']. Falling back to 'response.url'")

    def getHash(self, response=None, **kwargs) -> str:
        if "kwargs" in kwargs:
            if "metadata_dict" in kwargs["kwargs"]:
                metadata_dict: dict = kwargs["kwargs"]["metadata_dict"]
                hash_value: str = f"{metadata_dict.get('date_published')}v{self.version}"
                return hash_value
            else:
                logging.error(
                    f"Could not create 'hash' for item. (Failed to retrieve 'metadata_dict' in kwargs of "
                    f"getHash()-method.)"
                )

    def parse_node(self, response, selector: scrapy.selector.unified.Selector) -> scrapy.Request:
        """
        Parses the Lehrer-Online API for individual <datensatz>-nodes and yields URLs found within <url_ressource>-tags
        to the parse()-method. Additionally, this method builds a "cleaned up" metadata_dict that gets handed over
        within cb_kwargs.

        :param response:
        :param selector: scrapy.selector.unified.Selector
        :return: scrapy.Request

        Scrapy Contracts:
        @url https://www.lehrer-online.de/?type=3030
        @returns item 250
        """
        # an individual <datensatz> can hold the following elements:
        # <element-name>                            availability
        # - titel                                   always
        # - sprache                                 always (currently: 100% "Deutsch")
        # - beschreibung                            always
        # - beschreibung_lang                       sometimes (>50 %)
        # - bild_url                                sometimes (<5 %)
        # - schlagwort                              sometimes (unpredictable)
        # - kostenpflichtig                         always
        # - autor                                   sometimes
        # - autor_email                             always ("redaktion@lehrer-online.de")
        # - anbieter_herkunft                       always (Impressum)
        # - einsteller                              always ("Redaktion Lehrer-Online")
        # - einsteller_email                        always ("redaktion@lehrer-online.de")
        # - letzte_aenderung                        sometimes ("2022-02-18")
        # - publikationsdatum                       always ("2022-02-18")
        # - verfallsdatum                           never
        # - fach                                    sometimes (often: multiple <fach>-elements)
        # - bildungsebene                           sometimes (>50 %, sometimes completely empty)
        # - material_type                           always
        # - material_id_location                    always
        # - url_ressource                           always
        # - lernressourcentyp                       always?
        # - zielgruppe                              always
        # - rechte                                  sometimes
        # - frei_zugaenglich                        always
        # - quelle_id                               always (currently holds "LO" 100% of the time)
        # - quelle_logo_url                         always
        # - quelle_homepage_url                     always
        # - quelle_pfad                             always

        # self.logger.info(f"Currently crawling {self.itertag.join(selector.getall())}")
        metadata_dict = dict()
        new_lrts = set()

        title_raw: str = selector.xpath("titel/text()").get()
        if title_raw:
            metadata_dict.update({"title": title_raw})

        in_language: str = selector.xpath("sprache/text()").get()
        if in_language:
            if in_language == "Deutsch":
                metadata_dict.update({"language": "de"})

        description_short: str = selector.xpath("beschreibung/text()").get()
        if description_short:
            metadata_dict.update({"description_short": description_short})

        description_long: str = selector.xpath("beschreibung_lang/text()").get()
        if description_long:
            description_long = w3lib.html.replace_tags(description_long)
            description_long = w3lib.html.replace_entities(description_long)
            metadata_dict.update({"description_long": description_long})

        thumbnail_url: str = selector.xpath("bild_url/text()").get()
        # ToDo: the "bild_url"-field is rarely useful and only appears in <5% of items, revisit this later
        if thumbnail_url:
            metadata_dict.update({"thumbnail_url": thumbnail_url})

        keyword_list: list = selector.xpath("schlagwort/text()").getall()
        if keyword_list:
            metadata_dict.update({"keywords": keyword_list})
        # self.logger.info(f"the keywords are: {keyword_list}")

        with_costs_string: str = selector.xpath("kostenpflichtig/text()").get()
        # with_costs_string can be either "ja" or "nein"
        if with_costs_string == "ja":
            metadata_dict.update({"price": "yes"})
        elif with_costs_string == "nein":
            metadata_dict.update({"price": "no"})

        author_raw: str = selector.xpath("autor/text()").get()
        if author_raw:
            metadata_dict.update({"author": author_raw})

        author_email: str = selector.xpath("autor_email/text()").get()
        if author_email:
            metadata_dict.update({"author_email": author_email})

        provider_address: str = selector.xpath("anbieter_herkunft/text()").get()
        # provider_address is (currently?) always the address found in the Impressum
        if provider_address:
            metadata_dict.update({"provider_address": provider_address})
        provider_name: str = selector.xpath("einsteller/text()").get()
        # the value for "einsteller" is currently "Redaktion Lehrer-Online" in 100% of cases
        if provider_name:
            metadata_dict.update({"provider_name": provider_name})
        provider_email: str = selector.xpath("einsteller_email/text()").get()
        # the value for "einsteller_email" is currently "redaktion@lehrer-online.de" in 100% of cases
        if provider_email:
            metadata_dict.update({"provider_email": provider_email})

        # both last_modified and date_published will be surrounded by lots of whitespace, tabs and newlines
        # therefore we need to clean up the string before saving it into our dictionary
        last_modified: str = selector.xpath("letzte_aenderung/text()").get()
        if last_modified is not None:
            last_modified = w3lib.html.strip_html5_whitespace(last_modified)
            if last_modified:
                # last_modified is not always available, sometimes it's an empty string
                last_modified_datetime: datetime = datetime.strptime(last_modified, "%Y-%m-%d")
                last_modified = last_modified_datetime.isoformat()
                metadata_dict.update({"last_modified": last_modified})

        date_published: str = selector.xpath("publikationsdatum/text()").get()
        if date_published is not None:
            date_published = w3lib.html.strip_html5_whitespace(date_published)
            if date_published:
                # date_published is not always available in the API, but when it is, it follows a strict syntax
                date_published: str = w3lib.html.strip_html5_whitespace(date_published)
                date_published_datetime: datetime = datetime.strptime(date_published, "%Y-%m-%d")
                date_published = date_published_datetime.isoformat()
                metadata_dict.update({"date_published": date_published})
            else:
                # since date_published is used for our hash, we need this fallback in case it isn't available in the API
                metadata_dict.update({"date_published": datetime.now().isoformat()})

        # ToDo: there is a <verfallsdatum>-Element, that is (in the API) currently empty 100% of the time, check again
        #  during the next crawler-update if this data is available in the API by then
        # expiration_date = selector.xpath('verfallsdatum/text()').get()
        # if expiration_date:
        #     metadata_dict.update({'expiration_date': expiration_date})

        # <fach> can either be completely empty or there can be several <fach>-elements within a <datensatz>
        disciplines_or_additional_keywords: list = selector.xpath("fach/text()").getall()
        individual_disciplines_or_keywords = set()
        for potential_discipline_or_keyword in disciplines_or_additional_keywords:
            # to make mapping more precise, we're separating strings like "Politik / WiSo / SoWi / Wirtschaft" into its
            # individual parts
            if " / " in potential_discipline_or_keyword:
                disciplines_or_keywords_separated = potential_discipline_or_keyword.split(" / ")
                for each_string in disciplines_or_keywords_separated:
                    each_string_stripped = each_string.strip()
                    individual_disciplines_or_keywords.add(each_string_stripped)
            else:
                individual_disciplines_or_keywords.add(potential_discipline_or_keyword)
        disciplines_or_additional_keywords = list(individual_disciplines_or_keywords)

        disciplines_mapped = set()
        additional_keywords_from_disciplines = set()
        if disciplines_or_additional_keywords:
            for potential_discipline_item in disciplines_or_additional_keywords:
                if potential_discipline_item in self.MAPPING_FACH_TO_DISCIPLINES:
                    # since not every "fach"-value is the same as our discipline-vocabs, mapping is necessary
                    discipline = self.MAPPING_FACH_TO_DISCIPLINES.get(potential_discipline_item)
                    if type(discipline) is list:
                        disciplines_mapped.update(discipline)
                    else:
                        disciplines_mapped.add(discipline)
                elif potential_discipline_item:
                    disciplines_mapped.add(potential_discipline_item)
                    # not all "fach"-values are valid disciplines, but they can be used as additional keywords
                    # basically: everything that's not a correct discipline is treated as an additional keyword
                    additional_keywords_from_disciplines.add(potential_discipline_item)
                    # values that don't need to be mapped (or can't be mapped) end up in the additional keywords list
            # once we iterated through all <fach>-elements, we can set/update the actual fields in metadata_dict
            if disciplines_mapped:
                metadata_dict.update({"discipline": list(disciplines_mapped)})
            if additional_keywords_from_disciplines:
                keyword_set = set(keyword_list)
                keyword_set.update(additional_keywords_from_disciplines)
                keyword_list = list(keyword_set)
                metadata_dict.update({"keywords": keyword_list})

        educational_context_raw: str = selector.xpath("bildungsebene/text()").get()
        educational_context_cleaned_up = set()
        if educational_context_raw is not None:
            # if this metadata-field is left empty by Lehrer-Online, it will hold a string full of whitespaces, e.g.
            # '\n\t\t\t\t\n\t\t\t\t\t\t\n\t\t\t\t\t\n\t\t\t' gets filtered out here:
            educational_context_raw: str = w3lib.html.strip_html5_whitespace(educational_context_raw)
            if ";" in educational_context_raw:
                # if there's multiple values, they are surrounded by whitespaces and separated by a semicolon
                educational_level_list: list = educational_context_raw.split(sep=";")
                for educational_level_item in educational_level_list:
                    edu_level_temp: str = w3lib.html.strip_html5_whitespace(educational_level_item)
                    educational_context_cleaned_up.add(edu_level_temp)
            elif educational_context_raw:
                # if there's only one entry it needs to be longer than an empty string
                educational_context_raw: str = w3lib.html.strip_html5_whitespace(educational_context_raw)
                educational_context_cleaned_up.add(educational_context_raw)
        if educational_context_cleaned_up:
            educational_context_cleaned_up = list(educational_context_cleaned_up)
            educational_context = list()
            # we need to map some values to our educationalContext vocabulary
            for edu_context_item in educational_context_cleaned_up:
                if edu_context_item in self.MAPPING_EDU_CONTEXT.keys():
                    edu_context_temp = self.MAPPING_EDU_CONTEXT.get(edu_context_item)
                    educational_context.append(edu_context_temp)
                else:
                    educational_context.append(edu_context_item)
            metadata_dict.update({"educational_context": educational_context})

        material_type_raw: str = selector.xpath("material_type/text()").get()
        if material_type_raw:
            if material_type_raw in self.MAPPING_MATERIAL_TYPE_TO_NEW_LRT:
                new_lrt = self.MAPPING_MATERIAL_TYPE_TO_NEW_LRT.get(material_type_raw)
                new_lrts.add(new_lrt)
                metadata_dict.update({"new_lrt": new_lrt})
            metadata_dict.update({"material_type_raw": material_type_raw})

        material_id_local: str = selector.xpath("material_id_local/text()").get()
        if material_id_local:
            # the material_id_local seems to be a stable string (including an uuid) that is suitable for our sourceId
            metadata_dict.update({"source_id": material_id_local})

        material_url: str = selector.xpath("url_ressource/text()").get()
        if material_url is not None:
            material_url = w3lib.html.strip_html5_whitespace(material_url)
            if material_url:
                # checking explicitly for an empty URL-string (2 out of 5688 <url_ressource>-tags were empty)
                # see: https://docs.python.org/3/library/stdtypes.html#truth-value-testing
                metadata_dict.update({"url": material_url})

        lrt_raw = selector.xpath("lernressourcentyp/text()").getall()
        # there can be SEVERAL "lernressourcentyp"-elements per item
        if lrt_raw:
            additional_keywords_from_lo_lrt = set()
            for lrt_possible_value in lrt_raw:
                if lrt_possible_value in self.MAPPING_LO_LRT_TO_NEW_LRT:
                    new_lrt = self.MAPPING_LO_LRT_TO_NEW_LRT.get(lrt_possible_value)
                    new_lrts.add(new_lrt)
                else:
                    additional_keywords_from_lo_lrt.add(lrt_possible_value)
            metadata_dict.update({"new_lrt": list(new_lrts)})
            keyword_set = set(keyword_list)
            keyword_set.update(additional_keywords_from_lo_lrt)
            keyword_list = list(keyword_set)
            metadata_dict.update({"keywords": keyword_list})

        intended_end_user_role: str = selector.xpath("zielgruppe/text()").get()
        if intended_end_user_role:
            metadata_dict.update({"intended_end_user": intended_end_user_role})

        rights_raw: str = selector.xpath("rechte/text()").get()
        if rights_raw:
            rights_raw: str = w3lib.html.strip_html5_whitespace(rights_raw)
            if rights_raw:
                # after stripping the whitespace characters, we need to make sure that strings aren't empty
                if rights_raw in self.MAPPING_RIGHTS_TO_URLS:
                    license_url = self.MAPPING_RIGHTS_TO_URLS.get(rights_raw)
                    if license_url:
                        metadata_dict.update({"license_url": license_url})
                else:
                    metadata_dict.update({"license_description": rights_raw})

        free_to_access: str = selector.xpath("frei_zugaenglich/text()").get()
        # can be either 'ja' or 'nein', but it has a different meaning when "kostenpflichtig"-element is set to "ja":
        # frei_zugaenglich (ja) & kostenpflichtig (nein)        = truly free to access, no log-in required
        # frei_zugaenglich (nein) & kostenpflichtig (nein)      = available for free, but log-in required (free)
        # frei_zugaenglich (nein) & kostenpflichtig (ja)        = login required, paywalled (premium) content
        if free_to_access == "ja":
            if metadata_dict.get("price") == "no":
                metadata_dict.update({"conditions_of_access": "no_login"})
                metadata_dict.update({"origin_folder_name": "free"})
        elif free_to_access == "nein":
            if metadata_dict.get("price") == "yes":
                metadata_dict.update({"conditions_of_access": "login"})
                metadata_dict.update({"origin_folder_name": "premium_only"})
            elif metadata_dict.get("price") == "no":
                metadata_dict.update({"conditions_of_access": "login_for_additional_features"})
                metadata_dict.update({"origin_folder_name": "free_account_required"})

        # quelle_id currently holds just the abbreviation "LO" for all elements, check again later
        # quelle_logo_url is different from bild_url, always holds (the same) URL to the Lehrer-Online logo

        source_homepage_url: str = selector.xpath("quelle_homepage_url/text()").get()
        # Lehrer-Online offers several sub-portals to topic-specific materials. Distinction is possible by using the
        # quelle_homepage_url field in the API. Possible values:
        # "https://www.lehrer-online.de" (main website)
        # "https://lo-recht.lehrer-online.de" (Schulrecht)
        # "https://www.handwerk-macht-schule.de"
        # "https://pubertaet.lehrer-online.de" (is a "cooperation" with "Always" (Procter & Gamble) for sex education,
        # needs to be individually checked for advertorials or other product placement)
        match source_homepage_url:
            case "https://www.handwerk-macht-schule.de":
                origin_prefixed = f"Themenportal_Handwerk_-_{metadata_dict.get('origin_folder_name')}"
                metadata_dict.update({"origin_folder_name": origin_prefixed})
            case "https://pubertaet.lehrer-online.de":
                origin_prefixed = f"Themenportal_Pubertaet_-_{metadata_dict.get('origin_folder_name')}"
                metadata_dict.update({"origin_folder_name": origin_prefixed})

        # self.logger.info(f"metadata_dict = {metadata_dict}")
        if material_url:
            # not every <datensatz>-element actually holds a valid URL to parse for us - we need to skip those empty
            # strings otherwise the parse_node() method throws an error on that entry (and skips the rest)
            drop_item_flag: bool = self.check_if_item_should_be_dropped(response, metadata_dict=metadata_dict)
            if drop_item_flag is True:
                # if the flag is set to True, the item will be dropped and no 'scrapy.Request' shall be yielded
                # (this reduces the amount of unnecessary HTTP requests)
                pass
            else:
                skip_portal_setting: str = env.get(key="LO_SKIP_PORTAL", allow_null=True, default="false")
                # possible settings:
                # - "hwm" (= skip handwerk-macht-schule URLs)
                # - "pubertaet" (= skip Themenportal 'Pubertät' URLs)
                # - "false" (= default behaviour, crawl everything)
                if "hwm" in skip_portal_setting or "pubertaet" in skip_portal_setting:
                    if "handwerk-macht-schule.de" in material_url and "hwm" in skip_portal_setting:
                        # this workaround was requested by Romy on 2023-08-10 to (temporarily) avoid the problem of
                        # crawling duplicates on WLO prod (since some editors have already uploaded
                        # "Handwerk-macht-Schule"-learning-objects by hand)
                        # ToDo: revert this workaround in the next version of the crawler
                        #  (after the "Herkunft des Inhalts"-topic has been resolved)
                        logging.info(
                            f"Temporarily skipping {material_url} from crawling (due to Team4-decision on "
                            f"2023-08-10)."
                        )
                        pass
                    elif "pubertaet.lehrer-online.de" in material_url and "pubertaet" in skip_portal_setting:
                        logging.info(
                            f"Temporarily skipping {material_url} due to chosen '.env'-Setting for "
                            f"'LO_SKIP_PORTAL'."
                        )
                        pass
                    else:
                        yield scrapy.Request(
                            url=material_url, callback=self.parse, cb_kwargs={"metadata_dict": metadata_dict}
                        )
                else:
                    # default behaviour: everything from the Lehrer-Online API should be crawled
                    yield scrapy.Request(
                        url=material_url, callback=self.parse, cb_kwargs={"metadata_dict": metadata_dict}
                    )
        else:
            # if no material_url is provided, we cannot crawl anything, therefore skip the item
            logging.debug(f"Lehrer-Online API returned a node without a 'material_url'-value. (The title of the node "
                          f"was '{title_raw}'.")
            pass

    def getUri(self, response=None, **kwargs) -> str:
        try:
            metadata_dict: dict = kwargs["kwargs"]["metadata_dict"]
        except KeyError as ke:
            logging.error("getUri()-method could not access 'metadata_dict'.")
            raise ke
        return metadata_dict["url"]

    def getUUID(self, response=None, **kwargs) -> str:
        try:
            metadata_dict: dict = kwargs["kwargs"]["metadata_dict"]
        except KeyError as ke:
            logging.error("getUUID()-method could not access 'metadata_dict'.")
            raise ke
        return EduSharing.build_uuid(self.getUri(response, kwargs={"metadata_dict": metadata_dict}))

    def hasChanged(self, response=None, **kwargs) -> bool:
        """Re-implements LomBase's hasChanged()-method for Lehrer-Online."""
        try:
            metadata_dict: dict = kwargs["kwargs"]["metadata_dict"]
            identifier: str = self.getId(response, kwargs={"metadata_dict": metadata_dict})
            hash_str: str = self.getHash(response, kwargs={"metadata_dict": metadata_dict})
            uuid_str: str = self.getUUID(response, kwargs={"metadata_dict": metadata_dict})
        except KeyError as ke:
            logging.error("hasChanged()-method could not access 'metadata_dict'.")
            raise ke
        if self.forceUpdate:
            return True
        if self.uuid:
            if uuid_str == self.uuid:
                logging.info(f"matching requested id: {self.uuid}")
                return True
            return False
        if self.remoteId:
            if identifier == self.remoteId:
                logging.info(f"matching requested id: {self.remoteId}")
                return True
            return False
        db = EduSharing().find_item(identifier, self)
        changed = db is None or db[1] != hash_str
        if not changed:
            logging.info(f"Item {identifier} (uuid: {db[0]}) has not changed")
        return changed

    def check_if_item_should_be_dropped(self, response, metadata_dict: dict) -> bool:
        """
        Re-implements the check at the beginning of LomBase parse()-method to determine if an item needs to be dropped.
        This could happen for reasons like "the hash has not changed" (= the object has not changed since the last
        crawl) or if the 'shouldImport'-attribute was set to False.

        :param response: scrapy Response
        :param metadata_dict: metadata dictionary from the Lehrer-Online API
        :return: True if item needs to be dropped. Defaults to: False
        """
        drop_item_flag: bool = False  # by default, we assume that all items should be crawled
        identifier_url: str = self.getId(response, kwargs={"metadata_dict": metadata_dict})
        hash_str: str = self.getHash(response, kwargs={"metadata_dict": metadata_dict})
        if self.shouldImport(response) is False:
            logging.debug(f"Skipping entry {identifier_url} because shouldImport() returned false")
            drop_item_flag = True
        if identifier_url is not None and hash_str is not None:
            if not self.hasChanged(response, kwargs={"metadata_dict": metadata_dict}):
                drop_item_flag = True
        return drop_item_flag

    def parse(self, response: scrapy.http.Response, **kwargs) -> BaseItemLoader:
        """
        Uses the metadata_dict that was built in parse_node() and extracts additional metadata from the DOM itself to
        create and fill a BaseItem with the gathered metadata.
        :param response: scrapy.http.Response
        :param kwargs: a dictionary that always holds a "metadata_dict"-key (which itself holds a dictionary)
        :return: BaseItemLoader
        """
        metadata_dict: dict = kwargs.get("metadata_dict")

        base = BaseItemLoader()

        base.add_value("sourceId", self.getId(response, kwargs={"metadata_dict": metadata_dict}))
        base.add_value("hash", self.getHash(response, kwargs={"metadata_dict": metadata_dict}))
        if "last_modified" in metadata_dict:
            last_modified = metadata_dict.get("last_modified")
            base.add_value("lastModified", last_modified)
        else:
            # if last_modified is not available in the API, we use the publication date instead as a workaround
            base.add_value("lastModified", metadata_dict.get("date_published"))
        if "provider_address" in metadata_dict:
            base.add_value("publisher", metadata_dict.get("provider_address"))
        if "thumbnail_url" in metadata_dict:
            thumbnail_url: str = metadata_dict.get("thumbnail_url")
            if thumbnail_url:
                base.add_value("thumbnail", thumbnail_url)
        if "origin_folder_name" in metadata_dict:
            base.replace_value("origin", metadata_dict.get("origin_folder_name"))

        lom = LomBaseItemloader()

        general = LomGeneralItemloader()
        general.add_value("identifier", response.url)
        general.add_value("title", metadata_dict.get("title"))
        if "keywords" in metadata_dict:
            general.add_value("keyword", metadata_dict.get("keywords"))
        if "description_long" in metadata_dict:
            general.add_value("description", metadata_dict.get("description_long"))
        elif "description_short" in metadata_dict:
            general.add_value("description", metadata_dict.get("description_short"))
        if "language" in metadata_dict:
            general.add_value("language", metadata_dict.get("language"))

        # noinspection DuplicatedCode
        lom.add_value("general", general.load_item())

        technical = LomTechnicalItemLoader()
        technical.add_value("format", "text/html")
        if "url" in metadata_dict and metadata_dict["url"] != response.url:
            # in case the resolved URL might be different from the URL that we received by the API: save both
            material_url: str = metadata_dict["url"]
            technical.add_value("location", material_url)
        technical.add_value("location", response.url)
        lom.add_value("technical", technical.load_item())

        lifecycle_publisher = LomLifecycleItemloader()
        lifecycle_publisher.add_value("role", "publisher")
        lifecycle_publisher.add_value("date", metadata_dict.get("date_published"))
        if "provider_name" in metadata_dict:
            lifecycle_publisher.add_value("organization", metadata_dict.get("provider_name"))
        if "provider_email" in metadata_dict:
            lifecycle_publisher.add_value("email", metadata_dict.get("provider_email"))
        lom.add_value("lifecycle", lifecycle_publisher.load_item())

        educational = LomEducationalItemLoader()
        if "description_short" in metadata_dict:
            educational.add_value("description", metadata_dict.get("description_short"))
        #  - typicalLearningTime            optional
        if "language" in metadata_dict:
            educational.add_value("language", metadata_dict.get("language"))
        # ToDo: RegEx-extract typicalLearningTime? (needs to be a duration; LO serves this metadata as a string)
        # the time-format on the DOM is a wildly irregular String (from "3 Unterrichtsstunden" to "3x90 Minuten",
        # "mindestens 12 Unterrichtsstunden plus Lektüre" etc.); maybe consider this for later crawler-versions
        # learning_time_string =  response.xpath('//li[@class="icon-count-hours"]/span/text()').get()
        lom.add_value("educational", educational.load_item())

        # classification = super().getLOMClassification()
        # lom.add_value('classification', classification.load_item())

        base.add_value("lom", lom.load_item())

        vs = ValuespaceItemLoader()
        vs.add_value("containsAdvertisement", "yes")
        vs.add_value("dataProtectionConformity", "generalDataProtectionRegulation")
        # see: https://www.eduversum.de/datenschutz/
        if "conditions_of_access" in metadata_dict:
            vs.add_value("conditionsOfAccess", metadata_dict.get("conditions_of_access"))
        if "discipline" in metadata_dict:
            vs.add_value("discipline", metadata_dict.get("discipline"))
        if "educational_context" in metadata_dict:
            vs.add_value("educationalContext", metadata_dict.get("educational_context"))
        if "intended_end_user" in metadata_dict:
            vs.add_value("intendedEndUserRole", metadata_dict.get("intended_end_user"))
            vs.add_value("intendedEndUserRole", "teacher")  # ToDo: remove this hard-coded value as soon
            # as the SKOS vocabs altLabel generation is fixed (see: ITSJOINTLY-332)
        if "new_lrt" in metadata_dict:
            vs.add_value("new_lrt", metadata_dict.get("new_lrt"))
        else:
            vs.add_value("new_lrt", Constants.NEW_LRT_MATERIAL)
        if "price" in metadata_dict:
            vs.add_value("price", metadata_dict.get("price"))
        base.add_value("valuespaces", vs.load_item())

        license_loader = LicenseItemLoader()
        if "license_url" in metadata_dict:
            license_url = metadata_dict.get("license_url")
            license_loader.add_value("url", license_url)
        elif "license_description" in metadata_dict:
            license_description = metadata_dict.get("license_description")
            if license_description == "Frei nutzbares Material":
                license_loader.add_value("internal", Constants.LICENSE_CUSTOM)
                # just in case the license-description changes over time, we're gathering the description from the DOM
                license_title: str = response.xpath('//div[@class="license-title"]/text()').get()
                license_text: str = response.xpath('//div[@class="license-text"]/text()').get()
                if license_text and license_title:
                    license_full_desc: str = license_text.join(license_title)
                    license_loader.add_value("description", license_full_desc)
                else:
                    license_loader.add_value("description", license_description)
        else:
            license_loader.add_value("internal", Constants.LICENSE_COPYRIGHT_LAW)
        # noinspection DuplicatedCode
        if "author" in metadata_dict:
            license_loader.add_value("author", metadata_dict.get("author"))
        # if "expiration_date" in metadata_dict:
        #     # ToDo: activate gathering of expiration_date once the data is available in the API
        #     #  - make sure that the dateparser correctly recognizes the date
        #     expiration_date = metadata_dict.get("expiration_date")
        #     license_loader.add_value('expirationDate', expiration_date)
        base.add_value("license", license_loader.load_item())

        permissions = super().getPermissions(response)
        base.add_value("permissions", permissions.load_item())

        response_loader = ResponseItemLoader()
        response_loader.add_value("headers", response.headers)
        response_loader.add_value("url", self.getUri(response, kwargs={"metadata_dict": metadata_dict}))
        base.add_value("response", response_loader.load_item())

        yield base.load_item()
