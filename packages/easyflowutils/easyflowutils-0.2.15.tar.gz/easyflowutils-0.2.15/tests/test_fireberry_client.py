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
        res = 1

    def test_get_account_by_phone(self):
        account = self.client.get_account_id_by_phone("0528393372")
        self.assertTrue(account)

    def test_create_new_account(self):
        data = {'accountname': ' נדב1', 'emailaddress1': 'nadavnotexistsaccount1@gmail.com', 'telephone1': '0528393371'}
        # res = self.client.create_record("account", data)
        account_res = self.client.create_account(data)
        value = 1

    def test_query(self):
        account_id="80b58ee6-5a6c-4b5a-b1fe-e2d486ce5fae"
        # account_id = "80b58ee6-5a6c-4b5a-b1fe-e2d486ce5fa9"
        query = f"(accountid = '{account_id}')"

        res = self.client.query(1, query, fields="accountproductid,productid,status")
        value = 1
