from __future__ import annotations
import logging

from converter.pipelines.bases import BasicPipeline

log = logging.getLogger(__name__)


class DummyPipeline(BasicPipeline):
    def process_item(self, item, spider):
        return item
