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
        record = self.client.get_record_data("33", "dfbb8275-d293-4808-95f7-5902252a880f")
        self.assertTrue(record)