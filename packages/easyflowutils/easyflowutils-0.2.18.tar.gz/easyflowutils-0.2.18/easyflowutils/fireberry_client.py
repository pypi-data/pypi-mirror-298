from typing import Any, Optional

import requests

ACCOUNT_OBJECT_CODE = 1


class FireberryClient:
    BASE_URL = "https://api.fireberry.com"
    API_URL = f"{BASE_URL}/api"
    APP_URL = "https://app.fireberry.com"

    def __init__(self, token: str):
        self.token = token
        self.headers = {
            "tokenid": self.token,
            "Content-Type": "application/json"
        }

    def get(self, endpoint: str, params: Optional[dict[str, Any]] = None, prefix=API_URL) -> dict[str, Any]:
        url = f"{prefix}/{endpoint}"
        response = requests.get(url, headers=self.headers, params=params or {})
        response.raise_for_status()
        return response.json()

    def post(self, endpoint: str, data: dict[str, Any]) -> dict[str, Any] | list[dict[str, Any]]:
        url = f"{self.API_URL}/{endpoint}"
        response = requests.post(url, headers=self.headers, json=data)
        response.raise_for_status()
        return response.json()

    def put(self, endpoint: str, data: dict[str, Any]) -> dict[str, Any]:
        url = f"{self.API_URL}/{endpoint}"
        response = requests.put(url, headers=self.headers, json=data)
        response.raise_for_status()
        return response.json()

    def query(self, object_type_code: int, query: str, fields: Optional[str]) -> list[dict[str, Any]]:
        data = {
            "objecttype": object_type_code,
            "query": query,
        }
        if fields:
            data["fields"] = fields
        return self.post('query', data).get("data", {}).get("Data", [])

    def get_metadata_field_values(self, object_type_code: str, field_name: str) -> dict[str, Any]:
        return self.get(f"metadata/records/{object_type_code}/fields/{field_name}/values", prefix=self.BASE_URL)

    def get_metadata_field_names_dict(self, object_type_code: str, field_name: str) -> dict[str, Any]:
        field_values = self.get_metadata_field_values(object_type_code, field_name)
        return {item['name']: item for item in field_values.get("data", {}).get("values", {})}

    def get_metadata_field_values_dict(self, object_type_code: str, field_name: str) -> dict[str, Any]:
        field_values = self.get_metadata_field_values(object_type_code, field_name)
        return {item['value']: item for item in field_values.get("data", {}).get("values", {})}

    def get_record(self, object_type: str | int, record_id: str) -> dict[str, Any]:
        return self.get(f"record/{object_type}/{record_id}")

    def get_record_data(self, object_type: str | int, record_id: str) -> dict[str, Any]:
        return self.get_record(object_type, record_id).get("data", {}).get("Record", {})

    def create_record(self, object_type: str | int, data: dict[str, Any]) -> dict[str, Any]:
        return self.post(f"record/{object_type}", data).get("data", {}).get("Record", {})

    def update_record(self, object_type: str | int, record_id: str, data: dict[str, Any]) -> dict[str, Any]:
        return self.put(f"record/{object_type}/{record_id}", data)

    def batch_update(self, object_type: str, data: list[dict[str, Any]]) -> dict[str, Any]:
        url = f"{self.API_URL}/v3/record/{object_type}/batch/update"
        payload = {"data": data}
        return self.post(url, payload)

    def add_note_to_object(self, object_type_code: int, object_id: str, note_text: str) -> dict[str, Any]:
        body = {
            "objectid": object_id,
            "notetext": note_text,
            "objecttypecode": object_type_code,
        }
        return self.create_record("note", body)

    def create_account(self, data: dict[str, Any]) -> dict[str, Any]:
        return self.create_record("account", data)

    def get_account_id_by_email(self, email: str) -> Optional[str]:
        query = f"(emailaddress1 = '{email}')"
        account_id_key = 'accountid'
        data = self.query(ACCOUNT_OBJECT_CODE, query, fields=account_id_key)
        if data:
            return data[0].get(account_id_key)
        return None

    def get_account_id_by_phone(self, phone: str) -> Optional[str]:
        query = f"(telephone1 = '{phone}')"
        account_id_key = 'accountid'
        data = self.query(ACCOUNT_OBJECT_CODE, query, fields=account_id_key)
        if data:
            return data[0].get(account_id_key)
        return None

    def get_record_url_of_object(self, object_type_code: int, object_id: str) -> str:
        return f"{self.APP_URL}/record/{object_type_code}/{object_id}"
