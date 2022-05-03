import unittest
from converter.spiders.sodix_spider import SodixSpider, UnexpectedResponseError
import converter.env as env

class TestSodixSpider(unittest.TestCase):

    def setUp(self):
        self.sodixSpider = SodixSpider()
        self.unexpectedResponseError = UnexpectedResponseError()

    def test_placeholder(self):
        self.assertEqual("test1","test1")

    def test_login_statusCode200(self):
        self.sodixSpider.login()
        self.assertEqual(200, self.sodixSpider.getLoginRepsonseStatusCode())

    def test_login_unexpected_response(self):
        self.sodixSpider.password='1'
        with self.assertRaises(UnexpectedResponseError):
            self.sodixSpider.login()

    def test_login_accessToken(self):
        self.sodixSpider.login()
        self.assertTrue(self.sodixSpider.access_token)

if __name__ == '__main__':
    unittest.main()