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
from pprint import pprint

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
            item['fulltext'] = item['response']['body']
        return item

class TagPipeline(object):
    def process_item(self, item, spider):
        if item['tags']:
            item['tags'] = item['tags'].replace(" ", ",")
            return item

class NormLinksPipeline(object):
    def process_item(self, item, spider):
        print("Items is: ", item)
        if spider.name == "zoerr_spider":
            return item
        elif item['url']:
            if not any(x in item['url'] for x in ["http://", "https://"]):
                item['url'] = "https://" + item['url']
                return item
            else:
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

class PostgresPipeline(object):

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
class PostgresCheckPipeline(PostgresPipeline):
    def process_item(self, item, spider):
        dbItem = self.findItem(item, spider)
        if dbItem:
            if(item['hash'] != dbItem[1]):
                print("hash has changed, continuing pipelines")
            else:
                self.update(dbItem[0])
                # for tests, we update everything for now
                # activate this later
                #raise DropItem()
        return item
    def update(self, uuid):
        self.curr.execute("""UPDATE "references" SET last_fetched = now() WHERE uuid = %s""", (
            uuid,
        ))
        self.conn.commit()

class PostgresStorePipeline(PostgresPipeline):
    def process_item(self, item, spider):
        output = io.BytesIO()
        exporter = JsonItemExporter(output, fields_to_export = ['lom','fulltext','ranking'])
        exporter.export_item(item)
        dbItem = self.findItem(item, spider)
        if dbItem:
            uuid = dbItem[0][0]
            self.curr.execute("""UPDATE "references" SET source = %s, source_id = %s, last_fetched = now(), last_modified = now(), hash = %s, data = %s WHERE uuid = %s""", (
                spider.name, # source name
                item['sourceId'], # source item identifier
                #date.today(), # last modified
                item['hash'], # hash
                output.getvalue().decode('UTF-8'), # json
                uuid
            ))
        else:
            #todo build up uuid
            uuid = spider.name+'_'+item['sourceId']
            self.curr.execute("""INSERT INTO "references" VALUES (%s,%s,%s,now(),now(),now(),%s,%s)""", (
                uuid,
                spider.name, # source name
                item['sourceId'], # source item identifier
                #date.today(), # first fetched
                #date.today(), # last fetched
                #date.today(), # last modified
                item['hash'], # hash
                output.getvalue().decode('UTF-8') # json
            ))
        output.close()
        self.conn.commit()
        return item

