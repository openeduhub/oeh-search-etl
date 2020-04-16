# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.exceptions import DropItem
import json
import re
from w3lib.html import replace_escape_chars
import psycopg2
from scrapy.exporters import JsonItemExporter
import io
from datetime import date
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
from scrapy.utils.project import get_project_settings
from converter.db_connector import Database

VALUESPACE_API = 'http://localhost:5000/'

# fillup missing props by "guessing" or loading them if possible
class LOMFillupPipeline:
    def process_item(self, item, spider):
        if not 'fulltext' in item and 'body' in item['response']:
            h = html2text.HTML2Text()
            h.ignore_links = True
            h.ignore_images = True
            item['fulltext'] = h.handle(item['response']['body'])
        return item
class NormLicensePipeline(object):
    def process_item(self, item, spider):
        if item['license']:
            if any(x in item["license"].lower() for x in ["cc_0", "cc 0" "cc0", "public domain", "publicdomain", "zero"]):
                item["license"] = "CC 0"
                return item
            elif all(x in item['license'].lower() for x in ["sa", "by"]) and not "nc" in item["license"].lower():
                item["license"] = "CC BY-SA"
                return item
            elif any(x in item['license'].lower() for x in ["sa", "nd", "nc"]) == False:
                item["license"] = "CC BY"
                return item
            elif all(x in item["license"].lower() for x in ["by","sa","nc"]) == True:
                item["license"] = "CC BY-SA-NC"
                return item
            elif all(x in item["license"].lower() for x in ["by", "nc", "nd"]) == True:
                item["license"] = "CC BY-NC-ND"
                return item
            elif "nd" and not "nc" in item["license"].lower():
                item["license"] = "CC BY-ND"
                return item
            elif "nc" in item['license'].lower() and (any(x in item['license'].lower() for x in ["nd", "sa"]) == False):
                item["license"] = "CC BY-NC"
                return item
            else:
                raise DropItem("Missing or unknown license in %s" % item)
# convert typicalLearningTime into a integer representing seconds
class ConvertTimePipeline:
    def process_item(self, item, spider):
        # map lastModified
        if 'lastModified' in item:
            try:
                item['lastModified'] = float(item['lastModified'])
            except:
                try:
                    date = dateutil.parser.parse(item['lastModified'])
                    item['lastModified'] = int(date.timestamp())
                except:
                    logging.warn('Unable to parse given lastModified date ' + item['lastModified'])
                    del item['lastModified']

        if 'typicalLearningTime' in item['lom']['educational']:
            time = item['lom']['educational']['typicalLearningTime']
            mapped = None
            splitted = time.split(':')
            if len(splitted) == 3:
                mapped = int(splitted[0])*60*60 + int(splitted[1])*60 + int(splitted[2])
            if mapped == None:
                logging.warn('Unable to map given typicalLearningTime '+time+' to numeric value')
            item['lom']['educational']['typicalLearningTime'] = mapped
        return item
# generate de_DE / i18n strings for valuespace fields
class ProcessValuespacePipeline:
    ids = ['intendedEndUserRole', 'discipline', 'educationalContext', 'learningResourceType']
    valuespaces = {}
    def __init__(self):
        for v in self.ids:
            r=requests.get(VALUESPACE_API+'vocab/'+v)
            ProcessValuespacePipeline.valuespaces[v] = r.json()['vocabs']
    def process(self, item):
        for key in item['valuespaces']:
            # remap to new i18n layout
            mapped = []
            for entry in item['valuespaces'][key]:
                i18n = {}
                i18n['key'] = entry            
                valuespace = ProcessValuespacePipeline.valuespaces[key]
                found = False
                for v in valuespace:
                    if v['id'] == entry or len(list(filter(lambda x: x['@value'].casefold() == entry.casefold(), v['altId']))) > 0 or len(list(filter(lambda x: x['@value'].casefold() == entry.casefold(), v['label']))) > 0:
                        i18n['key'] = v['id']
                        i18n['de'] = list(filter(lambda x: x['@language'] == 'de', v['label']))[0]['@value']
                        try:
                            i18n['en'] = list(filter(lambda x: x['@language'] == 'en', v['label']))[0]['@value']
                        except:
                            pass
                        logging.info('transforming ' + key + ': ' + v['id'] + ' => ' + i18n['de'])
                        found = True
                        break
                if found:
                    mapped.append(i18n)
                else:
                    logging.warn('unknown value ' + entry + ' for valuespace ' + key)

            item['valuespaces'][key] = mapped
        return item
    def process_item(self, item, spider):
        item = self.process(item)
        return item
# generate thumbnails
class ProcessThumbnailPipeline:
    def scaleImage(self, img, maxSize):
        w=float(img.width)
        h=float(img.height)
        while(w*h>maxSize):
            w*=0.9
            h*=0.9
        return img.resize((int(w),int(h)), Image.ANTIALIAS).convert("RGB")
    def process_item(self, item, spider):
        response = None
        settings = get_project_settings()
        url = None
        if 'thumbnail' in item:
            url = item['thumbnail']
        elif 'location' in item['lom']['technical'] and 'format' in item['lom']['technical'] and item['lom']['technical']['format'] == 'text/html':
            url = settings.get('SPLASH_URL') + '/render.png?wait='  + str(settings.get('SPLASH_WAIT')) + '&url=' + urllib.parse.quote(item['lom']['technical']['location'], safe = '')
        if url != None:
            try:
                response = requests.get(url)
                if response.headers['Content-Type'] == 'image/svg+xml':
                    if len(response.content) > settings.get('THUMBNAIL_MAX_SIZE'):
                        raise Exception('SVG images can\'t be converted, and the given image exceeds the maximum allowed size (' + str(len(response.content)) + ' > ' + str(settings.get('THUMBNAIL_MAX_SIZE')) + ')')
                    item['thumbnail']={}
                    item['thumbnail']['mimetype'] = response.headers['Content-Type']
                    item['thumbnail']['small'] = base64.b64encode(response.content).decode()
                else:
                    img = Image.open(BytesIO(response.content))
                    small = BytesIO()
                    self.scaleImage(img, settings.get('THUMBNAIL_SMALL_SIZE')).save(small, 'JPEG', mode = 'RGB', quality = settings.get('THUMBNAIL_SMALL_QUALITY'))
                    large = BytesIO()
                    self.scaleImage(img, settings.get('THUMBNAIL_LARGE_SIZE')).save(large, 'JPEG', mode = 'RGB', quality = settings.get('THUMBNAIL_LARGE_QUALITY'))
                    item['thumbnail']={}
                    item['thumbnail']['mimetype'] = 'image/jpeg'
                    item['thumbnail']['small'] = base64.b64encode(small.getvalue()).decode()
                    item['thumbnail']['large'] = base64.b64encode(large.getvalue()).decode()
            except Exception as e:
                logging.warn('Could not read thumbnail at ' + url + ': ' + str(e))
                item['thumbnail']={}
        return item

class PostgresCheckPipeline(Database):
    def process_item(self, item, spider):
        if(not 'hash' in item):
            raise ValueError('The spider did not provide a hash on the base object. The hash is required to detect changes on an element. May use the last modified date or something similar')
        
        # @TODO: May this can be done only once?
        if self.findSource(spider) == None:
            logging.info("create new source "+spider.name)
            self.createSource(spider)

        dbItem = self.findItem(item['sourceId'], spider)
        if dbItem:
            if(item['hash'] != dbItem[1]):
                logging.debug("hash has changed, continuing pipelines")
            else:
                logging.debug("hash unchanged, skip item")
                self.update(dbItem[0])
                # for tests, we update everything for now
                # activate this later
                #raise DropItem()
        return item
    def createSource(self, spider):
        self.curr.execute("""INSERT INTO "sources" VALUES(%s,%s,%s)""", (
            spider.name,
            spider.friendlyName,
            spider.ranking
        ))
        self.conn.commit()
    def update(self, uuid):
        self.curr.execute("""UPDATE "references" SET last_fetched = now() WHERE uuid = %s""", (
            uuid,
        ))
        self.conn.commit()

class PostgresStorePipeline(Database):
    def process_item(self, item, spider):
        output = io.BytesIO()
        exporter = JsonItemExporter(output, fields_to_export = ['lom','valuespaces','fulltext','ranking','lastModified','thumbnail'])
        exporter.export_item(item)
        json = output.getvalue().decode('UTF-8')
        dbItem = self.findItem(item['sourceId'], spider)
        title = item['lom']['general']['title']
        #logging.info(json)
        if dbItem:
            entryUUID = dbItem[0]
            logging.info('Updating item ' + title + ' (' + entryUUID + ')')
            self.curr.execute("""UPDATE "references" SET source = %s, source_id = %s, last_fetched = now(), last_modified = now(), hash = %s, data = %s WHERE uuid = %s""", (
                spider.name, # source name
                item['sourceId'], # source item identifier
                #date.today(), # last modified
                item['hash'], # hash
                json,
                entryUUID
            ))
        else:
            entryUUID = str(uuid.uuid5(uuid.NAMESPACE_URL, item['response']['url']))
            logging.info('Creating item ' + title + ' (' + entryUUID + ')')
            self.curr.execute("""INSERT INTO "references" VALUES (%s,%s,%s,now(),now(),now(),%s,%s)""", (
                entryUUID,
                spider.name, # source name
                item['sourceId'], # source item identifier
                #date.today(), # first fetched
                #date.today(), # last fetched
                #date.today(), # last modified
                item['hash'], # hash
                json
            ))
        output.close()
        self.conn.commit()
        return item

