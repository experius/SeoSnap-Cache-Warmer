from scrapy import signals

from seosnap_cachewarmer.exporter import SeosnapItemExporter
from seosnap_cachewarmer.spider import SeosnapSpider


class SeosnapPipeline(object):
    exporter: SeosnapItemExporter

    @classmethod
    def from_crawler(cls, crawler):
        pipeline = cls()
        crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
        crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
        return pipeline

    def spider_opened(self, spider: SeosnapSpider):
        self.exporter = SeosnapItemExporter(spider.state.website_id, spider.state.use_queue)
        self.exporter.start_exporting()

    def spider_closed(self, spider):
        self.exporter.finish_exporting()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item
