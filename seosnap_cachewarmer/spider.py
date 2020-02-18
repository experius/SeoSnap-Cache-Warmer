import itertools
import os
import urllib.parse as urllib
from typing import Dict, List

from scrapy import Request
from scrapy.http import Response
from scrapy.spiders import SitemapSpider

from seosnap_cachewarmer.state import SeosnapState


class SeosnapSpider(SitemapSpider):
    state: SeosnapState
    name = 'Seosnap'

    def __init__(self, *args, **kwargs) -> None:
        self.state = SeosnapState(*args, **kwargs)
        self.name = self.state.get_name()
        super().__init__(sitemap_urls=self.state.sitemap_urls())

    def start_requests(self):
        if self.state.load:
            return (Request(url, self.parse) for url in self.state.get_load_urls())
        else:
            extra_urls = (Request(url, self.parse) for url in self.state.extra_pages())
            return itertools.chain(extra_urls, super().start_requests())

    def parse(self, response: Response):
        data = {
            name: response.css(selector).extract_first()
            for name, selector in self.state.extract_fields.items()
        }

        # Follow next links
        if self.state.follow_next:
            rel_next_url = response.css('link[rel="next"]::attr(href), a[rel="next"]::attr(href)').extract_first()
            if rel_next_url is not None:
                data['rel_next_url'] = rel_next_url
                yield response.follow(rel_next_url, callback=self.parse)

        # Strip cacheserver from the url if possible
        url = response.url[len(self.state.cacheserver_url):].lstrip('/')
        url = urllib.urlparse(url)
        url = urllib.urlunparse(('', '', url.path, url.params, url.query, ''))

        # Build page entity for dashboard
        cached = bytes_to_str(response.headers.get('Rendertron-Cached', None))
        cached_at = bytes_to_str(response.headers.get('Rendertron-Cached-At', None))
        yield {
            'address': url,
            'content_type': bytes_to_str(response.headers.get('Content-Type', None)),
            'status_code': response.status,
            'cache_status': 'cached' if cached == '1' or response.status == 200 else 'not-cached',
            'cached_at': cached_at,
            'extract_fields': data
        }


def bytes_to_str(o):
    if o is None: return o
    return o.decode("utf-8")
