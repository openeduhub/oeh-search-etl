# coding: utf-8

"""
    edu-sharing Repository REST API

    The public restful API of the edu-sharing repository.

    The version of the OpenAPI document: 1.1
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from edu_sharing_client.models.suggestion import Suggestion

class TestSuggestion(unittest.TestCase):
    """Suggestion unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> Suggestion:
        """Test Suggestion
            include_optional is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `Suggestion`
        """
        model = Suggestion()
        if include_optional:
            return Suggestion(
                replacement_string = '',
                display_string = '',
                key = ''
            )
        else:
            return Suggestion(
                replacement_string = '',
                display_string = '',
        )
        """

    def testSuggestion(self):
        """Test Suggestion"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
