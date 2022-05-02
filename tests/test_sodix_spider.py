import unittest
from converter.spiders.sodix_spider import SodixSpider

class TestSodixSpider(unittest.TestCase):

    def setUp(self):
        self.sodixSpider = SodixSpider()

    def test_placeholder(self):
        self.assertEqual("test1","test1")

    def test_login(self):
        self.sodixSpider.login()
        self.assertEqual(200, self.sodixSpider.getLoginRepsonseStatusCode())

if __name__ == '__main__':
    unittest.main()