from scrapy.exporters import JsonLinesItemExporter

from scrapy.extensions.feedexport import BlockingFeedStorage, build_storage


class EduSharingStorage(BlockingFeedStorage):
    """
    this would be a cool mechanism to use,
    if the crawling host hase enough temporary storage, to store all the crawled content.

    This Storage implementation would use the exporter below and:
      - write meta-data to disk
      - write images/screenshots/thumbnains to disk
    the _store_in_thread will be called once the crawls is completely finished
    """
    def __init__(self, uri, *, feed_options=None):
        from converter.es_connector_async import AsyncEsApiClient
        self.client = AsyncEsApiClient.get_instance_blocking()

    @classmethod
    def from_crawler(cls, crawler, uri, *, feed_options=None):
        return build_storage(
            cls,
            uri,
            feed_options=feed_options,
        )

    def _store_in_thread(self, file):
        """
        the file is the file descriptor that is used by the exporter below.
        hence, it contains all the meta-data as jsonlines and could be read linewise to
        put the items into edu-sharing.
        :param file:
        :return:
        """
        file.seek(0)

        file.close()



class EduSharingExporter(JsonLinesItemExporter):
    """
    this is an unfinished exporter.
    it was started to be used with the FEEDS setting.
    But FEEDS will store the content on the local disk, and might take up more space than available.

    The exporter should be aware of where to write binary files.
    """

    def __init__(self, file, **kwargs):
        """
        :param file: the file will be given by the exporter storage and is used when writing it to the storage backend.
        :param kwargs:
        """
        super().__init__(file, **kwargs)

    def export_item(self, item):
        """
        if the item contains binary fields, they should be written to a temporary dir or
        IMAGE_DIR/FILE_DIR from the project settings.
        They should be referenced within the metadata so they can be recovered by the storage plugin.

        :param item:
        :return:
        """
        print('exporting')
        itemdict = dict(self._get_serialized_fields(item))
        self.loop.run_until_complete(self.client.insert_item(itemdict))
