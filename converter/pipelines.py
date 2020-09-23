# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy import Item
from scrapy.exceptions import DropItem
from scrapy.loader import ItemLoader
import csv
from fuzzywuzzy import fuzz
from converter.constants import *
from overrides import overrides
import json
import re
from w3lib.html import replace_escape_chars
from scrapy.exporters import JsonItemExporter, CsvItemExporter
import io
from datetime import date
import time
import dateutil.parser
import logging
from pprint import pprint
from PIL import Image
from io import BytesIO
import requests
import urllib
import base64
import html2text
import scrapy
import sys
import uuid
from nltk.tokenize import word_tokenize
from valuespace_converter.app.valuespaces import Valuespaces
from scrapy.utils.project import get_project_settings
from converter.es_connector import EduSharing
import nltk
from nltk.stem.snowball import SnowballStemmer
import re


# fillup missing props by "inferencing" or loading them if possible
class LOMFillupPipeline:
    def process_item(self, item, spider):
        if not "fulltext" in item and "text" in item["response"]:
            item["fulltext"] = item["response"]["text"]
        return item


class ValuespaceFillupPipeline:
    process = ['discipline', 'learningResourceType']
    stemmer = SnowballStemmer("german")
    minSimilarity = 0.9

    def process_item(self, item, spider):
        if not 'general' in item['lom']:
            return item
        # TODO: Only for testing
        item['valuespaces']['discipline'] = []
        item['valuespaces']['learningResourceType'] = []
        fieldsToCheck = [item['lom']['general']['title']]
        if 'keyword' in item['lom']['general']:
            fieldsToCheck += item['lom']['general']['keyword']
        textToCheck = ' '.join(fieldsToCheck)
        # stem words, so e.g. Übungen ==> Übung
        # wordsToCheckPrimary = [item for sublist in
        #                list(map(lambda x: list(map(lambda y: self.stemmer.stem(y),re.split('[ ,.:/]',x))),fieldsToCheck))
        #                for item in sublist
        #                ]
        wordsToCheckPrimary = [item for sublist in
                        list(map(lambda x: word_tokenize(x),fieldsToCheck))
                        for item in sublist
                        ]
        print(wordsToCheckPrimary)
        # to unclean results?
        if 'description' in item['lom']['general']:
            # only fallback?
            fieldsToCheck += [item['lom']['general']['description']]
        if 'fulltext' in item:
            fieldsToCheck += [item['fulltext']]
        wordsToCheckAll = [item for sublist in
                        list(map(lambda x: word_tokenize(x),fieldsToCheck))
                        for item in sublist
                        ]

        foundValues = False
        for v in self.process:
            # if v in item['valuespaces']:
            #    continue
            valuesToAdd = set()
            for key in Valuespaces.data[v]:
                for vword in key['words']:
                    if vword.casefold() in textToCheck.casefold():
                        valuesToAdd.add(key['id'])
                        break
                    #for word in wordsToCheckPrimary:
                    #    if self.wordsSimilar(word, vword):
                    #        valuesToAdd.add(key['id'])
                    #        break

            if len(valuesToAdd):
                foundValues = True
                if not v in item['valuespaces']:
                    item['valuespaces'][v] = []
                item['valuespaces'][v] += valuesToAdd

        systematics = self.getSystematics(wordsToCheckAll)
        print(systematics)
        if len(systematics) > 0:
            if not 'discipline' in item['valuespaces']:
                item['valuespaces']['discipline'] = []
            item['valuespaces']['discipline'] += list(systematics)

        return item
    def getSystematics(self, wordsToCheck, valuespace = 'EAF-Sachgebietssystematik'):
        systematics = []
        systematicsDiscipline = []
        systematicsCounts = {}
        for key in Valuespaces.data[valuespace]:
            discipline = key['prefLabel']['de']
            if 'narrower' in key:
                found = self.findInTree(key['narrower'], wordsToCheck)
                if len(found) > 0:
                    systematicsDiscipline.append(discipline)
                    systematics += found
        for k in systematics + systematicsDiscipline:
            if k in systematicsCounts:
                systematicsCounts[k] += 1
            else:
                systematicsCounts[k] = 1
        if len(systematicsCounts):
            maxValue = max(systematicsCounts.values())
            systematicsFiltered = set()
            print(systematicsCounts)
            for k in systematicsCounts:
                if systematicsCounts[k] > maxValue * 0.5:
                    systematicsFiltered.add(k)
            return systematicsFiltered
        return []
    def findInTree(self, key, wordsToCheck):
        #else:
        result = []
        for k in key:
            if 'narrower' in k:
                result += self.findInTree(k['narrower'], wordsToCheck)
            else:
                for vword in k['words']:
                    if vword.casefold() in ' '.join(wordsToCheck).casefold():
                        result.append(k['prefLabel']['de'])
                    #for word in wordsToCheck:
                    #    if self.wordsSimilar(word, vword):
                    #        result.append(k['prefLabel']['de'])
        return result

    def wordsSimilar(self, word, vword):
        # return word.similarity(nlp(vword)) > self.minSimilarity or \
        # return lemmatizer(word.text, NOUN)[0].casefold() == lemmatizer(vword, NOUN)[0].casefold()
        sim = fuzz.ratio(word.casefold(), vword.casefold())/100.
        return  sim > self.minSimilarity # or \
                #(
                        #self.stemmer.stem(word).casefold() == self.stemmer.stem(vword).casefold() and \
                        #sim > 0.6
                #)

class FilterSparsePipeline:
    def process_item(self, item, spider):
        valid = False
        if not "location" in item["lom"]["technical"]:
            raise DropItem(
                "Entry "
                + item["lom"]["general"]["title"]
                + " has no technical location"
            )
        # pass through explicit uuid elements
        if "uuid" in item:
            return item
        try:
            valid = item["lom"]["general"]["keyword"]
        except:
            pass
        try:
            valid = valid or item["lom"]["general"]["description"]
        except:
            pass
        try:
            valid = valid or item["valuespaces"]["learningResourceType"]
        except:
            pass
        if not valid:
            raise DropItem(
                "Entry "
                + item["lom"]["general"]["title"]
                + " has neither keywords nor description"
            )
        return item


class NormLicensePipeline:
    def process_item(self, item, spider):
        if "url" in item["license"]:
            for key in Constants.LICENSE_MAPPINGS:
                if item["license"]["url"].startswith(key):
                    item["license"]["url"] = Constants.LICENSE_MAPPINGS[key]
                    break
        if "internal" in item["license"] and (
                not "url" in item["license"]
                or not item["license"]["url"] in Constants.VALID_LICENSE_URLS
        ):
            for key in Constants.LICENSE_MAPPINGS_INTERNAL:
                if item["license"]["internal"].casefold() == key.casefold():
                    item["license"]["url"] = Constants.LICENSE_MAPPINGS_INTERNAL[key]
                    break

        if "url" in item["license"] and not "oer" in item["license"]:
            if (
                    item["license"]["url"] == Constants.LICENSE_CC_BY_40
                    or item["license"]["url"] == Constants.LICENSE_CC_BY_SA_30
                    or item["license"]["url"] == Constants.LICENSE_CC_BY_SA_40
                    or item["license"]["url"] == Constants.LICENSE_CC_ZERO_10
            ):
                item["license"]["oer"] = OerType.ALL

        if "internal" in item["license"] and not "oer" in item["license"]:
            internal = item["license"]["internal"].lower()
            if "cc-by-sa" in internal or "cc-0" in internal or "pdm" in internal:
                item["license"]["oer"] = OerType.ALL
        return item


# convert typicalLearningTime into a integer representing seconds
class ConvertTimePipeline:
    def process_item(self, item, spider):
        # map lastModified
        if "lastModified" in item:
            try:
                item["lastModified"] = float(item["lastModified"])
            except:
                try:
                    date = dateutil.parser.parse(item["lastModified"])
                    item["lastModified"] = int(date.timestamp())
                except:
                    logging.warn(
                        "Unable to parse given lastModified date "
                        + item["lastModified"]
                    )
                    del item["lastModified"]

        if "typicalLearningTime" in item["lom"]["educational"]:
            time = item["lom"]["educational"]["typicalLearningTime"]
            mapped = None
            splitted = time.split(":")
            if len(splitted) == 3:
                mapped = (
                        int(splitted[0]) * 60 * 60
                        + int(splitted[1]) * 60
                        + int(splitted[2])
                )
            if mapped == None:
                logging.warn(
                    "Unable to map given typicalLearningTime "
                    + time
                    + " to numeric value"
                )
            item["lom"]["educational"]["typicalLearningTime"] = mapped
        return item


# generate de_DE / i18n strings for valuespace fields
class ProcessValuespacePipeline:
    valuespaces = None

    def __init__(self):
        self.valuespaces = Valuespaces()

    def process_item(self, item, spider):
        json = item["valuespaces"]
        delete = []
        for key in json:
            # remap to new i18n layout
            mapped = []
            for entry in json[key]:
                id = {}
                valuespace = self.valuespaces.data[key]
                found = False
                for v in valuespace:
                    labels = list(v["prefLabel"].values())
                    if "altLabel" in v:
                        labels = labels + list(
                            [x for y in list(v["altLabel"].values()) for x in y]
                        )
                    labels = list(map(lambda x: x.casefold(), labels))
                    if v["id"].endswith(entry) or entry.casefold() in labels:
                        id = v["id"]
                        found = True
                        break
                if found and len(list(filter(lambda x: x == id, mapped))) == 0:
                    mapped.append(id)
                elif not found:
                    logging.info('Not found valuespace ' + key + ' entry for value ' + entry)
            if len(mapped):
                json[key] = mapped
            else:
                delete.append(key)
        for key in delete:
            del json[key]
        item["valuespaces"] = json
        return item


# generate thumbnails
class ProcessThumbnailPipeline:
    def scaleImage(self, img, maxSize):
        w = float(img.width)
        h = float(img.height)
        while w * h > maxSize:
            w *= 0.9
            h *= 0.9
        return img.resize((int(w), int(h)), Image.ANTIALIAS).convert("RGB")

    def process_item(self, item, spider):
        response = None
        settings = get_project_settings()
        url = None
        if "thumbnail" in item:
            url = item["thumbnail"]
            response = requests.get(url)
            logging.debug(
                "Loading thumbnail took " + str(response.elapsed.total_seconds()) + "s"
            )
        elif (
                "location" in item["lom"]["technical"]
                and "format" in item["lom"]["technical"]
                and item["lom"]["technical"]["format"] == "text/html"
        ):
            if settings.get("SPLASH_URL"):
                response = requests.post(
                    settings.get("SPLASH_URL") + "/render.png",
                    json={
                        "url": item["lom"]["technical"]["location"],
                        "wait": settings.get("SPLASH_WAIT"),
                        "html5_media": 1,
                        "headers": settings.get("SPLASH_HEADERS"),
                    },
                )
            else:
                logging.warning(
                    "No thumbnail provided and SPLASH_URL was not configured for screenshots!"
                )
        if response == None:
            logging.error(
                "Neither thumbnail or technical.location provided! Please provide at least one of them"
            )
        else:
            try:
                if response.headers["Content-Type"] == "image/svg+xml":
                    if len(response.content) > settings.get("THUMBNAIL_MAX_SIZE"):
                        raise Exception(
                            "SVG images can't be converted, and the given image exceeds the maximum allowed size ("
                            + str(len(response.content))
                            + " > "
                            + str(settings.get("THUMBNAIL_MAX_SIZE"))
                            + ")"
                        )
                    item["thumbnail"] = {}
                    item["thumbnail"]["mimetype"] = response.headers["Content-Type"]
                    item["thumbnail"]["small"] = base64.b64encode(
                        response.content
                    ).decode()
                else:
                    img = Image.open(BytesIO(response.content))
                    small = BytesIO()
                    self.scaleImage(img, settings.get("THUMBNAIL_SMALL_SIZE")).save(
                        small,
                        "JPEG",
                        mode="RGB",
                        quality=settings.get("THUMBNAIL_SMALL_QUALITY"),
                    )
                    large = BytesIO()
                    self.scaleImage(img, settings.get("THUMBNAIL_LARGE_SIZE")).save(
                        large,
                        "JPEG",
                        mode="RGB",
                        quality=settings.get("THUMBNAIL_LARGE_QUALITY"),
                    )
                    item["thumbnail"] = {}
                    item["thumbnail"]["mimetype"] = "image/jpeg"
                    item["thumbnail"]["small"] = base64.b64encode(
                        small.getvalue()
                    ).decode()
                    item["thumbnail"]["large"] = base64.b64encode(
                        large.getvalue()
                    ).decode()
            except Exception as e:
                if url:
                    logging.warn(
                        "Could not read thumbnail at "
                        + url
                        + ": "
                        + str(e)
                        + " (falling back to screenshot)"
                    )
                if "thumbnail" in item:
                    del item["thumbnail"]
                    return self.process_item(item, spider)
                else:
                    # item['thumbnail']={}
                    raise DropItem(
                        "No thumbnail provided or ressource was unavailable for fetching"
                    )
        return item


class EduSharingCheckPipeline(EduSharing):
    def process_item(self, item, spider):
        if not "hash" in item:
            logging.error(
                "The spider did not provide a hash on the base object. The hash is required to detect changes on an element. May use the last modified date or something similar"
            )
            item["hash"] = time.time()

        # @TODO: May this can be done only once?
        if self.findSource(spider) == None:
            logging.info("create new source " + spider.name)
            self.createSource(spider)

        dbItem = self.findItem(item["sourceId"], spider)
        if dbItem:
            if item["hash"] != dbItem[1]:
                logging.debug("hash has changed, continuing pipelines")
            else:
                logging.debug("hash unchanged, skip item")
                # self.update(item['sourceId'], spider)
                # for tests, we update everything for now
                # activate this later
                # raise DropItem()
        return item

class CSVStorePipeline():

    def open_spider(self, spider):
        self.csvFile = open('output_'+spider.name+'.csv', 'w', newline='')
        self.spamwriter = csv.writer(self.csvFile, delimiter=',',
                                quotechar='"', quoting=csv.QUOTE_MINIMAL)
        self.spamwriter.writerow([
            'title',
            'description',
            'fulltext',
            'keywords',
            'location',
            'discipline',
            'learningResourceType',
        ])

    def getValue(self, item, value):
        container = item
        tokens = value.split('.')
        for v in tokens:
            if v in container:
                container = container[v]
            else:
                return None
        if tokens[0] == 'valuespaces':
            return list(map(lambda x: Valuespaces.findKey(tokens[1], x)['prefLabel']['de'], container))
        return container

    def close_spider(self, spider):
        self.csvFile.close()
    def process_item(self, item, spider):
        self.spamwriter.writerow([
            self.getValue(item,'lom.general.title'),
            self.getValue(item,'lom.general.description'),
            self.getValue(item,'fulltext'),
            self.getValue(item,'lom.general.keyword'),
            self.getValue(item,'lom.technical.location'),
            self.getValue(item,'valuespaces.discipline'),
            self.getValue(item,'valuespaces.learningResourceType'),
        ])
        self.csvFile.flush()
        print('processing csv')
        return item

class EduSharingStorePipeline(EduSharing):
    def process_item(self, item, spider):
        output = io.BytesIO()
        exporter = JsonItemExporter(
            output,
            fields_to_export=[
                "lom",
                "valuespaces",
                "license",
                "type",
                "origin",
                "fulltext",
                "ranking",
                "lastModified",
                "thumbnail",
            ],
        )
        exporter.export_item(item)
        title = "<no title>"
        if "title" in item["lom"]["general"]:
            title = str(item["lom"]["general"]["title"])
        entryUUID = self.buildUUID(item["response"]["url"])
        self.insertItem(spider, entryUUID, item)
        logging.info("item " + entryUUID + " inserted/updated")

        # @TODO: We may need to handle Collections
        # if 'collection' in item:
        #    for collection in item['collection']:
        # if dbItem:
        #     entryUUID = dbItem[0]
        #     logging.info('Updating item ' + title + ' (' + entryUUID + ')')
        #     self.curr.execute("""UPDATE "references_metadata" SET last_seen = now(), last_updated = now(), hash = %s, data = %s WHERE source = %s AND source_id = %s""", (
        #         item['hash'], # hash
        #         json,
        #         spider.name,
        #         str(item['sourceId']),
        #     ))
        # else:
        #     entryUUID = self.buildUUID(item['response']['url'])
        #     if 'uuid' in item:
        #         entryUUID = item['uuid']
        #     logging.info('Creating item ' + title + ' (' + entryUUID + ')')
        #     if self.uuidExists(entryUUID):
        #         logging.warn('Possible duplicate detected for ' + entryUUID)
        #     else:
        #         self.curr.execute("""INSERT INTO "references" VALUES (%s,true,now())""", (
        #             entryUUID,
        #         ))
        #     self.curr.execute("""INSERT INTO "references_metadata" VALUES (%s,%s,%s,%s,now(),now(),%s)""", (
        #         spider.name, # source name
        #         str(item['sourceId']), # source item identifier
        #         entryUUID,
        #         item['hash'], # hash
        #         json,
        #     ))
        output.close()
        return item


class DummyPipeline:
    # Scrapy will print the item on log level DEBUG anyway

    # class Printer:
    #     def write(self, byte_str: bytes) -> None:
    #         logging.debug(byte_str.decode("utf-8"))

    # def open_spider(self, spider):
    #     self.exporter = JsonItemExporter(
    #         DummyOutPipeline.Printer(),
    #         fields_to_export=[
    #             "collection",
    #             "fulltext",
    #             "hash",
    #             "lastModified",
    #             "license",
    #             "lom",
    #             "origin",
    #             "permissions",
    #             "publisher",
    #             "ranking",
    #             # "response",
    #             "sourceId",
    #             # "thumbnail",
    #             "type",
    #             "uuid",
    #             "valuespaces",
    #         ],
    #         indent=2,
    #         encoding="utf-8",
    #     )
    #     self.exporter.start_exporting()

    # def close_spider(self, spider):
    #     self.exporter.finish_exporting()

    def process_item(self, item, spider):
        logging.info("DRY RUN scraped {}".format(item["response"]["url"]))
        # self.exporter.export_item(item)
        return item
