import itertools
import logging
import os
import urllib.parse as urllib
from datetime import datetime
from typing import Dict, List
import json

from scrapy import Request
from scrapy.http import Response
from scrapy.spiders import SitemapSpider
from scrapy.selector import Selector

from seosnap_cachewarmer.state import SeosnapState


class SeosnapSpider(SitemapSpider):
    state: SeosnapState
    name = 'Seosnap'

    def __init__(self, *args, **kwargs) -> None:
        self.state = SeosnapState(*args, **kwargs)
        self.name = self.state.get_name()

        super().__init__(sitemap_urls=self.state.sitemap_urls())

    def headers(self):
        return {}

    def start_requests(self):
        extra_urls = (Request(url, self.parse, headers=self.headers()) for url in self.state.extra_pages())

        return itertools.chain(extra_urls, super().start_requests())

    def parse(self, response: Response):
        response_body_json = json.loads(response.body)

        data = {
            name: Selector(text=response_body_json['html']).css(selector).extract_first()
            for name, selector in self.state.extract_fields.items()
        }

        # Follow next links
        if self.state.follow_next:
            rel_next_url = Selector(text=response_body_json['html']).css('link[rel="next"]::attr(href), a[rel="next"]::attr(href)').extract_first()

            if rel_next_url is not None:
                rel_next_url = urllib.urlparse(rel_next_url)
                rel_next_url_query = urllib.parse_qs(rel_next_url.query)
                rel_next_url_query.pop('refreshCache', None)

                old_url_parsed = urllib.urlparse(response.url)
                old_url_query = urllib.parse_qs(old_url_parsed.query)

                if 'mobile' in old_url_query and old_url_query['mobile']:
                    rel_next_url_query.update({'mobile': '1'})

                rel_next_url = rel_next_url._replace(query=urllib.urlencode(rel_next_url_query, True))

                data['rel_next_url'] = rel_next_url.geturl()
                yield response.follow(rel_next_url.geturl(), callback=self.parse)

        # Strip cacheserver from the url if possible
        url = response.url[len(self.state.cacheserver_url):].lstrip('/')
        url = urllib.urlparse(url)
        query = urllib.parse_qs(url.query)
        query.pop('refreshCache', None)
        url = url._replace(query=urllib.urlencode(query, True))

        url = urllib.urlunparse(('', '', url.path, url.params, url.query, ''))

        # Build page entity for dashboard
        cached = bytes_to_str(response.headers.get('Rendertron-Cached', None))
        cached_at = bytes_to_str(response.headers.get('Rendertron-Cached-At', None))

        yield {
            'address': url,
            'content_type': 'text/html; charset=utf-8',
            'status_code': response.status,
            'x_magento_tags': response_body_json['tags'],
            'cache_status': 'cached' if cached == '1' or response.status == 200 else 'not-cached',
            'cached_at': cached_at,
            'extract_fields': data
        }


def bytes_to_str(o):
    if o is None: return o
    return o.decode("utf-8")
