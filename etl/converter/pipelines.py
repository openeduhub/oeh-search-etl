# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.exceptions import DropItem
from converter.constants import *
import json
import re
from w3lib.html import replace_escape_chars
import psycopg2
from scrapy.exporters import JsonItemExporter
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
from scrapy.utils.project import get_project_settings
from converter.db_connector import Database

VALUESPACE_API = 'http://localhost:5000/'

# fillup missing props by "guessing" or loading them if possible
class LOMFillupPipeline:
    def process_item(self, item, spider):
        if not 'fulltext' in item and 'text' in item['response']:
            item['fulltext'] = item['response']['text']
        return item
class FilterSparsePipeline:
    def process_item(self, item, spider):
        valid = False
        if not 'location' in item['lom']['technical']:
            raise DropItem('Entry ' + item['lom']['general']['title'] + ' has no technical location')            
        # pass through explicit uuid elements
        if 'uuid' in item:
            return item
        try:
            valid = item['lom']['general']['keyword']
        except:
            pass
        try:
            valid = valid or item['lom']['general']['description']
        except:
            pass
        try:
            valid = valid or item['valuespaces']['learningResourceType']
        except:
            pass
        if not valid:
            raise DropItem('Entry ' + item['lom']['general']['title'] + ' has neither keywords nor description')            
        return item
        
class NormLicensePipeline(object):
    def process_item(self, item, spider):
        if 'url' in item['license'] and not 'oer' in item['license']:
            if(
                item['license']['url'] == Constants.LICENSE_CC_BY_40 or 
                item['license']['url'] == Constants.LICENSE_CC_BY_SA_30 or
                item['license']['url'] == Constants.LICENSE_CC_BY_SA_40
            ):
                item['license']['oer'] = OerType.ALL
       
        if 'internal' in item['license'] and not 'oer' in item['license']:
            internal = item['license']['internal'].lower()
            if(
                'cc-by-sa' in internal or
                'cc-0' in internal
            ):
                item['license']['oer'] = OerType.ALL
        return item
            

            
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
    ids = ['intendedEndUserRole', 'discipline', 'educationalContext', 'learningResourceType', 'sourceContentType']
    valuespaces = {}
    def __init__(self):
        for v in self.ids:
            url = VALUESPACE_API + 'vocab/' + v
            try:
                r = requests.get(url)
                ProcessValuespacePipeline.valuespaces[v] = r.json()['vocabs']
            except:
                logging.error('Can not access the valuespace api at ' + url + ', exception: ' + str(sys.exc_info()[0]) + ' The system will continue, but valuespace mapping will not work!')
                ProcessValuespacePipeline.valuespaces[v] = {}
    def process_item(self, item, spider):
        delete = []
        for key in item['valuespaces']:
            # remap to new i18n layout
            mapped = []
            for entry in item['valuespaces'][key]:
                i18n = {}
                i18n['key'] = entry
                valuespace = ProcessValuespacePipeline.valuespaces[key]
                found = False
                for v in valuespace:
                    if v['id'].endswith(entry) or len(list(filter(lambda x: x['@value'].casefold() == entry.casefold(), v['altId']))) > 0 or len(list(filter(lambda x: x['@value'].casefold() == entry.casefold(), v['label']))) > 0:
                        i18n['key'] = v['id']
                        i18n['de'] = list(filter(lambda x: x['@language'] == 'de', v['label']))[0]['@value']
                        try:
                            i18n['en'] = list(filter(lambda x: x['@language'] == 'en', v['label']))[0]['@value']
                        except:
                            pass
                        logging.info('transforming ' + key + ': ' + v['id'] + ' => ' + i18n['de'])
                        found = True
                        break
                if found and len(list(filter(lambda x: x['key'] == i18n['key'], mapped))) == 0:
                    mapped.append(i18n)
                else:
                    logging.warn('unknown value ' + entry + ' for valuespace ' + key)
            if len(mapped):
                item['valuespaces'][key] = mapped
            else:
                delete.append(key)
        for key in delete:
            del item['valuespaces'][key]
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
        if 'thumbnail' in item:
            url = item['thumbnail']
            response = requests.get(url)
        elif 'location' in item['lom']['technical'] and 'format' in item['lom']['technical'] and item['lom']['technical']['format'] == 'text/html':
            response = requests.post(settings.get('SPLASH_URL')+'/render.png', json={
                'url': item['lom']['technical']['location'],
                'wait': settings.get('SPLASH_WAIT'),
                'html5_media': 1,
                'headers': settings.get('SPLASH_HEADERS')
            })
        if response == None:
            logging.error('Neither thumbnail or technical.location provided! Please provie at least one of them')
        else:
            try:
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
                logging.warn('Could not read thumbnail at ' + url + ': ' + str(e) + ' (falling back to screenshot)')
                if 'thumbnail' in item:
                    del item['thumbnail']
                    return self.process_item(item, spider)
                else:
                    #item['thumbnail']={}
                    raise DropItem('No thumbnail provided or ressource was unavailable for fetching')
        return item

class PostgresCheckPipeline(Database):
    def process_item(self, item, spider):
        if(not 'hash' in item):
            logging.error('The spider did not provide a hash on the base object. The hash is required to detect changes on an element. May use the last modified date or something similar')
            item['hash'] = time.time()
        
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
                # self.update(item['sourceId'], spider)
                # for tests, we update everything for now
                # activate this later
                #raise DropItem()
        return item
    def createSource(self, spider):
        self.curr.execute("""INSERT INTO "sources" VALUES(%s,%s,%s,%s,%s)""", (
            spider.name,
            Constants.SOURCE_TYPE_SPIDER,
            spider.friendlyName,
            spider.url,
            spider.ranking,
        ))
        self.conn.commit()

class PostgresStorePipeline(Database):
    def process_item(self, item, spider):
        output = io.BytesIO()
        exporter = JsonItemExporter(output, fields_to_export = ['lom','valuespaces','license','type','fulltext','ranking','lastModified','thumbnail'])
        exporter.export_item(item)
        json = output.getvalue().decode('UTF-8')
        dbItem = self.findItem(item['sourceId'], spider)
        title = '<no title>'
        if 'title' in item['lom']['general']:
            title = str(item['lom']['general']['title'])
        #logging.info(item['lom'])
        if dbItem:
            entryUUID = dbItem[0]
            logging.info('Updating item ' + title + ' (' + entryUUID + ')')
            self.curr.execute("""UPDATE "references_metadata" SET last_seen = now(), last_updated = now(), hash = %s, data = %s WHERE source = %s AND source_id = %s""", (
                item['hash'], # hash
                json,
                spider.name,
                str(item['sourceId']),
            ))
        else:
            entryUUID = self.buildUUID(item['response']['url'])
            if 'uuid' in item:
                entryUUID = item['uuid']
            logging.info('Creating item ' + title + ' (' + entryUUID + ')')
            if self.uuidExists(entryUUID):
                logging.warn('Possible duplicate detected for ' + entryUUID)
            else:
                self.curr.execute("""INSERT INTO "references" VALUES (%s,true,now())""", (
                    entryUUID,
                ))
            self.curr.execute("""INSERT INTO "references_metadata" VALUES (%s,%s,%s,%s,now(),now(),%s)""", (
                spider.name, # source name
                str(item['sourceId']), # source item identifier
                entryUUID,
                item['hash'], # hash
                json,
            ))
        if 'collection' in item:
            for collection in item['collection']:
                logging.info('adding object ' + entryUUID + 'into collection ' + collection)
                self.addCollectionReference(entryUUID, collection)
        output.close()
        self.conn.commit()
        return item

