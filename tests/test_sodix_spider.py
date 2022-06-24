import unittest
from converter.spiders.sodix_spider import SodixSpider, UnexpectedResponseError


# To run this test_sodix_spider, use the following command line : python -m unittest tests/test_sodix_spider.py
# To test parse_sodix function and lomBase functions in sodix_spider.py, it is recommended to run sodix_spider.py. 
# If Scrapy's response is parsed correctly, it will return the sorted Metadata in JSON or CSV file.
class TestSodixSpider(unittest.TestCase):

    def setUp(self):
        self.sodixSpider = SodixSpider()
        self.unexpectedResponseError = UnexpectedResponseError()

    def test_login_unexpected_response(self):
        self.sodixSpider.password = '1'
        with self.assertRaises(UnexpectedResponseError):
            self.sodixSpider.login()

    def test_login_access_token(self):
        self.sodixSpider.login()
        self.assertTrue(self.sodixSpider.access_token)


if __name__ == '__main__':
    unittest.main()
