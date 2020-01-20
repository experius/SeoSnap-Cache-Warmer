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

    def get_website(self, website_id: int):
        action = ["api", "websites", "read"]
        params = {"version": os.getenv('API_VER'), "id": website_id}
        return self.client.action(self.schema, action, params=params)

    def update_pages(self, website_id: int, pages: List[dict]):
        action = ["api", "websites", "pages", "update_pages"]
        params = {"version": os.getenv('API_VER'), "website_id": website_id, "items": pages}
        return self.client.action(self.schema, action, params=params)
