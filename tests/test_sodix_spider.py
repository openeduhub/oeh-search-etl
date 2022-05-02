from doctest import UnexpectedException
import unittest
from converter.spiders.sodix_spider import SodixSpider, UnexpectedResponseError

class TestSodixSpider(unittest.TestCase):

    def setUp(self):
        self.sodixSpider = SodixSpider()

    def test_placeholder(self):
        self.assertEqual("test1","test1")

    def test_login_statusCode200(self):
        self.sodixSpider.login()
        self.assertEqual(200, self.sodixSpider.getLoginRepsonseStatusCode())

    @unittest.expectedFailure
    def test_login_unexpected_response(self):
        self.sodixSpider.password='1'
        self.assertRaises(UnexpectedResponseError, self.sodixSpider.login())

    def test_login_accessToken(self):
        self.sodixSpider.login()
        self.assertTrue(self.sodixSpider.access_token)
        print(f'response: {self.sodixSpider.access_token}')

if __name__ == '__main__':
    unittest.main()