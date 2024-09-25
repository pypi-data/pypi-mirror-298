from typing import Any, Optional

import requests


class FireberryClient:
    BASE_URL = "https://api.fireberry.com/api"

    def __init__(self, token: str):
        self.token = token
        self.headers = {
            "tokenid": self.token,
            "Content-Type": "application/json"
        }

    def get(self, endpoint: str, params: Optional[dict[str, Any]] = None) -> dict[str, Any]:
        url = f"{self.BASE_URL}/{endpoint}"
        response = requests.get(url, headers=self.headers, params=params or {})
        response.raise_for_status()
        return response.json()

    def post(self, endpoint: str, data: dict[str, Any]) -> dict[str, Any]:
        url = f"{self.BASE_URL}/{endpoint}"
        response = requests.post(url, headers=self.headers, json=data)
        response.raise_for_status()
        return response.json()

    def put(self, endpoint: str, data: dict[str, Any]) -> dict[str, Any]:
        url = f"{self.BASE_URL}/{endpoint}"
        response = requests.put(url, headers=self.headers, json=data)
        response.raise_for_status()
        return response.json()

    def query(self, object_type: int, query: str, fields: Optional[str] = None) -> dict[str, Any]:
        url = f"{self.BASE_URL}/query"
        data = {
            "objecttype": object_type,
            "query": query,
        }
        if fields:
            data["fields"] = fields
        return self.post(url, data)

    def get_record(self, object_type: str, record_id: str) -> dict[str, Any]:
        return self.get(f"record/{object_type}/{record_id}").get("data", {}).get("Record", {})

    def create_record(self, object_type: str, data: dict[str, Any]) -> dict[str, Any]:
        return self.post(f"record/{object_type}", data)

    def update_record(self, object_type: str, record_id: str, data: dict[str, Any]) -> dict[str, Any]:
        return self.put(f"record/{object_type}/{record_id}", data)

    def batch_update(self, object_type: str, data: list[dict[str, Any]]) -> dict[str, Any]:
        url = f"{self.BASE_URL}/v3/record/{object_type}/batch/update"
        payload = {"data": data}
        return self.post(url, payload)

    def add_note_to_object(self, object_type_code: int, object_id: str, note_text: str) -> dict[str, Any]:
        url = f"{self.BASE_URL}/note"
        body = {
            "objectid": object_id,
            "notetext": note_text,
            "objecttypecode": object_type_code,
        }
        return self.post(url, body)
