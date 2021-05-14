import json

from django.test import TestCase

from store.orders.parsers import JsonParser, XMLParser
from store.orders.exceptions import ApiError


class JsonParserTest(TestCase):
    def setUp(self):
        self.parser = JsonParser()

    def test_should_raise_api_error_when_wrong_json_in_response(self):
        wrong_json = "<wrong></wrong>"
        with self.assertRaises(ApiError) as error:
            self.parser.parse_response(wrong_json)
        self.assertIn('Api returned wrong JSON: Expecting value: line 1 column 1 (char 0)', str(error.exception))

    def test_should_raise_api_error_when_errors_in_response(self):
        wrong_auth_response = json.dumps({
            "Response": {
                "ErrorCode": -1,
                "ErrorMessage": "The authentication provided is not valid"
            }
        })
        with self.assertRaises(ApiError) as error:
            self.parser.parse_response(wrong_auth_response)
        self.assertIn('Api Error The authentication provided is not valid', str(error.exception))


class XMLParserTest(TestCase):
    def setUp(self):
        self.parser = XMLParser()

    def test_should_raise_error_when_wrong_response(self):
        wrong_order_number_response = """<?xml version="1.0" encoding="UTF-8" ?>
            <Errors>
                <ErrorMessage>Order 1 does not belong to an account for this client</ErrorMessage>
            </Errors>
        """
        with self.assertRaises(ApiError) as error:
            self.parser.parse_response(wrong_order_number_response)
        self.assertIn('Api Error Order 1 does not belong to an account for this client', str(error.exception))
