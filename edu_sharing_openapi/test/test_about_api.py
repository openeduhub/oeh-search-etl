# coding: utf-8

"""
    edu-sharing Repository REST API

    The public restful API of the edu-sharing repository.

    The version of the OpenAPI document: 1.1
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from edu_sharing_client.api.about_api import ABOUTApi


class TestABOUTApi(unittest.TestCase):
    """ABOUTApi unit test stubs"""

    def setUp(self) -> None:
        self.api = ABOUTApi()

    def tearDown(self) -> None:
        pass

    def test_about(self) -> None:
        """Test case for about

        Discover the API.
        """
        pass

    def test_licenses(self) -> None:
        """Test case for licenses

        License information.
        """
        pass

    def test_status(self) -> None:
        """Test case for status

        status of repo services
        """
        pass


if __name__ == '__main__':
    unittest.main()
