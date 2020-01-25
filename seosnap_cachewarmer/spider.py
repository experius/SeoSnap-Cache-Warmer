import os
import urllib.parse as urllib
from typing import Dict

from scrapy.http import Response
from scrapy.spiders import SitemapSpider

from seosnap_cachewarmer.service import SeosnapService


class SeosnapSpider(SitemapSpider):
    website_id: int
    follow_next: bool
    recache: bool
    cacheserver_url: str
    service: SeosnapService
    extract_fields: Dict[str, str]
    name = 'Seosnap'

    def __init__(self, website_id, follow_next=True, recache=True) -> None:
        self.service = SeosnapService()
        self.website_id = website_id
        self.follow_next = follow_next
        self.recache = recache
        self.cacheserver_url = os.getenv('CACHEWARMER_CACHE_SERVER_URL').rstrip('/')
        website = self.service.get_website(self.website_id)

        self.name = f'Cachewarm: {website["name"]}'
        self.extract_fields = {field['name']: field["css_selector"] for field in website["extract_fields"]}
        sitemap_urls = [website["sitemap"]]
        super().__init__(sitemap_urls=sitemap_urls)

    def parse(self, response: Response):
        data = {
            name: response.css(selector).extract_first()
            for name, selector in self.extract_fields.items()
        }

        # Follow next links
        if self.follow_next:
            rel_next_url = response.css('link[rel="next"]::attr(href), a[rel="next"]::attr(href)').extract_first()
            if rel_next_url is not None:
                data['rel_next_url'] = rel_next_url
                yield response.follow(rel_next_url, callback=self.parse)

        # Strip cacheserver from the url if possible
        url = response.url[len(self.cacheserver_url):].lstrip('/')
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
