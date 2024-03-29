import json
import os
from typing import List

import coreapi


class SeosnapService:
    client: coreapi.Client
    schema: dict

    def __init__(self) -> None:
        super().__init__()
        self.client = coreapi.Client(auth=coreapi.auth.BasicAuthentication(
            username=os.getenv('API_NAME'),
            password=os.getenv('API_PASS')
        ))
        self.schema = self.client.get(os.getenv('API_URL'))

    def get_website(self, website_id: int) -> dict:
        action = ["api", "websites", "read"]
        params = {"version": os.getenv('API_VER'), "id": website_id}
        return self.client.action(self.schema, action, params=params)

    def update_pages(self, website_id: int, pages: List[dict]) -> List[dict]:
        action = ["api", "websites", "pages", "update_pages"]
        params = {"version": os.getenv('API_VER'), "website_id": website_id, "items": pages}
        return self.client.action(self.schema, action, params=params)

    def get_queue(self, website_id: int) -> dict:
        action = ["api", "websites", "queue_0"]
        params = {"version": os.getenv('API_VER'), "website_id": website_id}
        return self.client.action(self.schema, action, params=params)

    def update_queue(self, website_id: int, queue_items: List[dict]) -> List[dict]:
        action = ['api', 'websites', 'queue', 'update_queue']
        params = {"version": os.getenv('API_VER'), "website_id": website_id, "items": queue_items}
        return self.client.action(self.schema, action, params=params)

    def clean_queue(self, website_id: int) -> List[dict]:
        action = ['api', 'websites', 'queue', 'clean_queue']
        params = {"version": os.getenv('API_VER'), "website_id": website_id}
        return self.client.action(self.schema, action, params=params)

    def clean_pages(self, website_id: int, date) -> List[dict]:
        action = ['api', 'websites', 'pages', 'clean_pages']
        params = {"version": os.getenv('API_VER'), "website_id": website_id, "date": date}
        return self.client.action(self.schema, action, params=params)

    def report_errors(self, website_id: int, errors: List[dict]) -> List[dict]:
        errors = list(map(lambda x: {**x, 'time': x['time'].isoformat()}, errors))
        action = ['api', 'websites', 'report_failure']
        params = {"version": os.getenv('API_VER'), "website_id": website_id, "errors": errors}
        return self.client.action(self.schema, action, params=params)

    def sync_pages(self, website_id: int):
        action = ['api', 'websites', 'pages', 'sync']
        params = {"version": os.getenv('API_VER'), "website_id": website_id}
        return self.client.action(self.schema, action, params=params)

    def queue_old_redo(self, website_id: int):
        action = ['api', 'websites', 'queue', 'redo', 'old']
        params = {"version": os.getenv('API_VER'), "website_id": website_id}
        return self.client.action(self.schema, action, params=params)


