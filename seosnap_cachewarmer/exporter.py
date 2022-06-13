import os
from typing import List

from scrapy.exporters import BaseItemExporter

from seosnap_cachewarmer.service import SeosnapService


class SeosnapItemExporter(BaseItemExporter):
    website_id: int
    service: SeosnapService
    use_queue: bool
    buffer: List[dict]
    buffer_size: int = int(os.getenv('CACHEWARMER_BUFFER_SIZE', 2))

    def __init__(self, website_id, use_queue=False, buffer_size=None, **kwargs):
        super().__init__(**kwargs)
        self.use_queue = use_queue
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
            if self.use_queue: self.flush_queue()
            self.service.update_pages(self.website_id, self.buffer)
            self.buffer = []

    def flush_queue(self):
        items = [
            {
                'page': {
                    'address': item['address']
                },
                'status': 'completed' if item['status_code'] // 200 == 1 else 'failed'
            }
            for item in self.buffer
        ]
        self.service.update_queue(self.website_id, items)
