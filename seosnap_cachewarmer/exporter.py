from typing import List

from scrapy.exporters import BaseItemExporter

from seosnap_cachewarmer.service import SeosnapService


class SeosnapItemExporter(BaseItemExporter):
    website_id: int
    service: SeosnapService
    buffer: List[dict]
    buffer_size: int = 30

    def __init__(self, website_id, buffer_size=None, **kwargs):
        super().__init__(**kwargs)
        if buffer_size: self.buffer_size = buffer_size
        self.website_id = website_id

    def start_exporting(self):
        self.service = SeosnapService()
        self.buffer = []

    def finish_exporting(self):
        self.flush()

    def export_item(self, item):
        self.buffer.append(item)
        if len(self.buffer) > self.buffer_size:
            self.flush()

    def flush(self):
        if len(self.buffer) > 0:
            self.service.update_pages(self.website_id, self.buffer)
            self.buffer = []
