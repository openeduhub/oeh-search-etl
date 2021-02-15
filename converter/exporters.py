import asyncio
from scrapy.exporters import JsonLinesItemExporter
from scrapy.utils.python import to_bytes
from scrapy.utils.serialize import ScrapyJSONEncoder

from converter.es_connector_async import AsyncEsApiClient


class EduSharingExporter(JsonLinesItemExporter):
    def __init__(self, **kwargs):
        super().__init__(dont_fail=True, **kwargs)
        self.client: AsyncEsApiClient = None
        self.loop = None
        self._kwargs.setdefault('ensure_ascii', not self.encoding)
        self.encoder = ScrapyJSONEncoder(**self._kwargs)

    def start_exporting(self):
        super().start_exporting()
        self.client = AsyncEsApiClient.get_instance_blocking()
        self.loop = asyncio.get_event_loop()

    def export_item(self, item):
        itemdict = dict(self._get_serialized_fields(item))
        self.loop.run_until_complete(self.client.insert_item(itemdict))
