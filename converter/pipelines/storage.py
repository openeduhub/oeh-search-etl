import csv
import io
import logging
import time
from typing import BinaryIO, TextIO

import scrapy
from scrapy.exporters import JsonItemExporter

from converter import env
from converter.es_connector import EduSharing
from converter.pipelines.bases import BasicPipeline, PipelineWithPerSpiderMethods
from valuespace_converter.app.valuespaces import Valuespaces
log = logging.getLogger(__name__)


class JSONStorePipeline(BasicPipeline, PipelineWithPerSpiderMethods):
    def __init__(self):
        self.files: dict[str, BinaryIO] = {}
        self.exporters: dict[str, JsonItemExporter] = {}

    def open_spider(self, spider):
        file = open(f'output_{spider.name}.json', 'wb')
        self.files[spider.name] = file
        exporter = JsonItemExporter(
            file,
            fields_to_export=[
                "sourceId",
                "lom",
                # "valuespaces",
                "license",
                # "type",
                # "origin",
                # "fulltext",
                # "ranking",
                # "lastModified",
                # "thumbnail",
            ],
            encoding='utf-8',
            indent=2,
            ensure_ascii=False)
        self.exporters[spider.name] = exporter
        exporter.start_exporting()

    def close_spider(self, spider):
        self.exporters[spider.name].finish_exporting()
        self.files[spider.name].close()

    def process_item(self, item, spider):
        self.exporters[spider.name].export_item(item)
        return item


class CSVStorePipeline(BasicPipeline, PipelineWithPerSpiderMethods):
    rows = []

    def __init__(self):
        self.files: dict[str, TextIO] = {}
        self.exporters: dict[str, csv.writer] = {}
        CSVStorePipeline.rows = env.get("CSV_ROWS", allow_null=False).split(",")

    def open_spider(self, spider):
        csv_file = open('output_' + spider.name + '.csv', 'w', newline='')
        spamwriter = csv.writer(
            csv_file,
            delimiter=',',
            quotechar='"',
            quoting=csv.QUOTE_MINIMAL)

        spamwriter.writerow(self.rows)
        self.files[spider.name] = csv_file
        self.exporters[spider.name] = spamwriter

    @staticmethod
    def get_value(item, value):
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
        # exporter closes automatically?
        self.files[spider.name].close()

    def process_item(self, item, spider):
        self.exporters[spider.name].writerow(list(map(lambda x: self.get_value(item, x), self.rows)))
        self.files[spider.name].flush()
        return item


class EduSharingStorePipeline(EduSharing, BasicPipeline):
    def __init__(self):
        super().__init__()

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
        log.info("item " + entryUUID + " inserted/updated")

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


class EduSharingCheckPipeline(EduSharing, BasicPipeline, PipelineWithPerSpiderMethods):
    def open_spider(self, spider: scrapy.Spider) -> None:
        if self.findSource(spider) is None:
            log.info("create new source " + spider.name)
            self.createSource(spider)

    def close_spider(self, spider: scrapy.Spider) -> None:
        pass

    def process_item(self, item, spider):
        if "hash" not in item:
            log.error(
                "The spider did not provide a hash on the base object. The hash is required to detect changes on an element. May use the last modified date or something similar"
            )
            item["hash"] = time.time()

        db_item = self.findItem(item["sourceId"], spider)
        if db_item:
            if item["hash"] != db_item[1]:
                log.debug("hash has changed, continuing pipelines")
            else:
                log.debug("hash unchanged, skip item")
                # self.update(item['sourceId'], spider)
                # for tests, we update everything for now
                # activate this later
                # raise DropItem()
        return item
