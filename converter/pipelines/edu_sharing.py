import time

import scrapy

from converter.es_connector_async import AsyncEsApiClient
from converter.es_connector_common import build_uuid
from converter.pipelines.bases import BasicAsyncPipeline, PipelineWithFactoryMethod, T, log


class EduSharingCheckAsyncPipeline(BasicAsyncPipeline, PipelineWithFactoryMethod):
    @classmethod
    def from_crawler(cls: T, crawler: scrapy.crawler.Crawler) -> T:
        client = AsyncEsApiClient.get_instance_blocking()
        return cls(client)

    def __init__(self, client: AsyncEsApiClient):
        print('__init__ check')
        self.client = client

    async def process_item(self, item, spider):
        if "hash" not in item:
            log.error(
                "The spider did not provide a hash on the base object. The hash is required to detect changes on an element. May use the last modified date or something similar"
            )
            item["hash"] = time.time()

        db_item = await self.client.find_item(spider, item["sourceId"])
        # db_item = self.findItem(item["sourceId"], spider)
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


class EduSharingStoreAsyncPipeline(BasicAsyncPipeline, PipelineWithFactoryMethod):
    @classmethod
    def from_crawler(cls: T, crawler: scrapy.crawler.Crawler) -> T:
        client = AsyncEsApiClient.get_instance_blocking()
        return cls(client)

    def __init__(self, client: AsyncEsApiClient):
        print('init store')
        self.client = client

    async def process_item(self, item, spider):
        if 0 == self.counter % 50:
            print('')
        # self.exporter.export_item(item)
        # title = "<no title>"
        # if "title" in item["lom"]["general"]:
        #     title = str(item["lom"]["general"]["title"])
        entry_uuid = build_uuid(item["response"]["url"])
        await self.client.insert_item(spider, entry_uuid, item)
        log.info(f"item {entry_uuid} inserted/updated")
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
        # output.close()
        return item
