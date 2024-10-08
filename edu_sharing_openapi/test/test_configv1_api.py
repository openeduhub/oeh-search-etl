# coding: utf-8

"""
    edu-sharing Repository REST API

    The public restful API of the edu-sharing repository.

    The version of the OpenAPI document: 1.1
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from edu_sharing_client.api.configv1_api import CONFIGV1Api


class TestCONFIGV1Api(unittest.TestCase):
    """CONFIGV1Api unit test stubs"""

    def setUp(self) -> None:
        self.api = CONFIGV1Api()

    def tearDown(self) -> None:
        pass

    def test_get_config1(self) -> None:
        """Test case for get_config1

        get repository config values
        """
        pass

    def test_get_dynamic_value(self) -> None:
        """Test case for get_dynamic_value

        Get a config entry (appropriate rights for the entry are required)
        """
        pass

    def test_get_language(self) -> None:
        """Test case for get_language

        get override strings for the current language
        """
        pass

    def test_get_language_defaults(self) -> None:
        """Test case for get_language_defaults

        get all inital language strings for angular
        """
        pass

    def test_get_variables(self) -> None:
        """Test case for get_variables

        get global config variables
        """
        pass

    def test_set_dynamic_value(self) -> None:
        """Test case for set_dynamic_value

        Set a config entry (admin rights required)
        """
        pass


if __name__ == '__main__':
    unittest.main()
