import os
from unittest import TestCase

from dotenv import load_dotenv

from easyflowutils import FireberryClient

load_dotenv()


class TestFireberryClient(TestCase):
    token = os.getenv("FIREBERRY_TOKEN")

    def setUp(self):
        self.client = FireberryClient(token=self.token)

    def test_metadata(self):
        metadata = self.client.get_metadata_field_values_dict("33", "statuscode")
        self.assertTrue(metadata)

    def test_get_record(self):
        record = self.client.get_record_data("AccountProduct", "dfbb8275-d293-4808-95f7-5902252a880f")
        self.assertTrue(record)

    def test_create_recorself(self):
        data = {"accountname": "Nadav",
                "emailaddress1": "nadavtest1@gmail.com",
                "telephone1": "0528393372"}

        record = self.client.create_account(data)
        res=1

    def test_get_account_by_phone(self):
        account = self.client.get_account_id_by_phone("0528393372")
        self.assertTrue(account)
