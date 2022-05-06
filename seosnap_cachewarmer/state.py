import logging
import os
from datetime import datetime, timedelta

import requests
from typing import Dict, Union, Iterable
import urllib.parse as urllib

from seosnap_cachewarmer.service import SeosnapService


class SeosnapState:
    website: dict
    website_id: int
    follow_next: bool
    recache: bool
    use_queue: bool
    load: bool
    mobile: bool
    errors: list
    clean_old_pages_after: bool

    cacheserver_url: str
    service: SeosnapService
    extract_fields: Dict[str, str]

    def __init__(
            self,
            website_id,
            follow_next=True,
            recache=True,
            use_queue=False,
            mobile=False,
            clean_old_pages_after=False
    ) -> None:
        self.service = SeosnapService()
        self.website_id = website_id
        self.use_queue = parse_bool(use_queue)
        self.clean_old_pages_after = parse_bool(clean_old_pages_after)
        self.follow_next = parse_bool(follow_next)
        self.recache = parse_bool(recache)
        self.mobile = parse_bool(mobile)
        self.errors = []

        self.cacheserver_url = os.getenv('CACHEWARMER_CACHE_SERVER_URL').rstrip('/')
        self.website = self.service.get_website(self.website_id)
        self.extract_fields = {field['name']: field["css_selector"] for field in self.website["extract_fields"]}

    def get_name(self) -> str:
        return f'Cachewarm: {self.website["name"]}'

    def sitemap_urls(self) -> Iterable[str]:
        if not self.use_queue:
            yield self.website["sitemap"]

    def extra_pages(self) -> Iterable[str]:
        if not self.use_queue:
            yield self.website["domain"]
        else:
            for url in self.get_queue(): yield url

    def get_queue(self) -> Iterable[str]:
        # Retrieve queue items while queue is not empty
        uri = urllib.urlparse(self.website['domain'])
        root_domain = f'{uri.scheme}://{uri.netloc}'
        while True:
            items = self.service.get_queue(self.website_id)
            # Empty queue
            if len(items) == 0: break

            for item in items:
                path = item['page']['address']
                yield f'{root_domain}{path}'

    def append_error(self, error):
        self.errors.append(error)
        max_range = datetime.now() - timedelta(seconds=self.website['notification_cooldown'])
        for i in reversed(range(len(self.errors))):
            if self.errors[i]['time'] < max_range:
                self.errors.pop(i)

        if len(self.errors) > self.website['notification_failure_rate']:
            logging.debug('Reporting errors to the dashboard')
            try:
                self.service.report_errors(self.website_id, self.errors)
            except Exception as e:
                logging.error(f'Failed reporting errors to the dashboard: {e}')
            self.errors = []


def parse_bool(s: Union[str, bool]) -> bool:
    if isinstance(s, bool): return s
    return s not in ['false', 'False', '0']