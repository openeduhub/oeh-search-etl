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
import logging
from pprint import pprint
from PIL import Image
from io import BytesIO
import requests
import base64
import html2text

THUMBNAIL_SMALL_SIZE = 250*250
THUMBNAIL_SMALL_QUALITY = 25
THUMBNAIL_LARGE_SIZE = 800*800
THUMBNAIL_LARGE_QUALITY = 60

class ScrapyPipeline(object):
    def process_item(self, item, spider):
        return item

class JoinLongWhiteSpaceStringsPipeline(object):
    def process_item(self, item, spider):
        if spider.name == "zoerr_spider":
            return item
        if spider.name == "hhu_spider":
            return item
        if item['author']:
            item['author'] = re.sub('  +', ', ', item['author'])
            item['tags'] = " ".join(item['tags'].split())
            return item
class LOMFillupPipeline:
    def process_item(self, item, spider):
        if not 'fulltext' in item:
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
class ConvertTimePipeline:
    def process_item(self, item, spider):
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
class ProcessThumbnailPipeline:
    def scaleImage(self, img, maxSize):
        w=float(img.width)
        h=float(img.height)
        while(w*h>maxSize):
            w*=0.9
            h*=0.9
        return img.resize((int(w),int(h)), Image.ANTIALIAS).convert("RGB")
    def process_item(self, item, spider):
        if 'thumbnail' in item:
            response = requests.get(item['thumbnail'])
            del item['thumbnail']
            img = Image.open(BytesIO(response.content))
            small = BytesIO()
            self.scaleImage(img, THUMBNAIL_SMALL_SIZE).save(small, 'JPEG', mode = 'RGB', quality = THUMBNAIL_SMALL_QUALITY)
            large = BytesIO()
            self.scaleImage(img, THUMBNAIL_LARGE_SIZE).save(large, 'JPEG', mode = 'RGB', quality = THUMBNAIL_LARGE_QUALITY)
            item['thumbnail']={}
            item['thumbnail']['small'] = base64.b64encode(small.getvalue()).decode()
            #item['thumbnail']['large'] = base64.b64encode(large.getvalue()).decode()
        return item
class PostgresPipeline:
    def __init__(self):
        self.create_connection()

    def create_connection(self):
        self.conn = psycopg2.connect(
            host = 'localhost',
            user = 'search',
            password = 'admin',
            database = 'search'
        )
        self.curr = self.conn.cursor()
    def findItem(self, item, spider):
        self.curr.execute("""SELECT uuid, hash FROM "references" WHERE source = %s AND source_id = %s""", (
            spider.name,
            item['sourceId']
        ))
        data = self.curr.fetchall()
        if(len(data)):
            return data[0]
        else:
            return None
    def findSource(self, spider):
        self.curr.execute("""SELECT * FROM "sources" WHERE id = %s""", (
            spider.name,
        ))
        data = self.curr.fetchall()
        if(len(data)):
            return data[0]
        else:
            return None
class PostgresCheckPipeline(PostgresPipeline):
    def process_item(self, item, spider):
        if(not 'hash' in item):
            raise ValueError('The spider did not provide a hash on the base object. The hash is required to detect changes on an element. May use the last modified date or something similar')
        
        # @TODO: May this can be done only once?
        if self.findSource(spider) == None:
            logging.info("create new source "+spider.name)
            self.createSource(spider)

        dbItem = self.findItem(item, spider)
        if dbItem:
            if(item['hash'] != dbItem[1]):
                logging.info("hash has changed, continuing pipelines")
            else:
                logging.info("hash unchanged, skip item")
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

class PostgresStorePipeline(PostgresPipeline):
    def process_item(self, item, spider):
        output = io.BytesIO()
        exporter = JsonItemExporter(output, fields_to_export = ['lom','fulltext','ranking','thumbnail'])
        exporter.export_item(item)
        json = output.getvalue().decode('UTF-8')
        dbItem = self.findItem(item, spider)
        #logging.info(json)
        if dbItem:
            uuid = dbItem[0]
            logging.info("Updating item "+uuid)
            self.curr.execute("""UPDATE "references" SET source = %s, source_id = %s, last_fetched = now(), last_modified = now(), hash = %s, data = %s WHERE uuid = %s""", (
                spider.name, # source name
                item['sourceId'], # source item identifier
                #date.today(), # last modified
                item['hash'], # hash
                json,
                uuid
            ))
        else:
            #todo build up uuid
            uuid = spider.name+'_'+item['sourceId']
            logging.info("creating item "+uuid)
            self.curr.execute("""INSERT INTO "references" VALUES (%s,%s,%s,now(),now(),now(),%s,%s)""", (
                uuid,
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

