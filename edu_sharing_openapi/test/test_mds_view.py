# coding: utf-8

"""
    edu-sharing Repository REST API

    The public restful API of the edu-sharing repository.

    The version of the OpenAPI document: 1.1
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from edu_sharing_client.models.mds_view import MdsView

class TestMdsView(unittest.TestCase):
    """MdsView unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> MdsView:
        """Test MdsView
            include_optional is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `MdsView`
        """
        model = MdsView()
        if include_optional:
            return MdsView(
                id = '',
                caption = '',
                icon = '',
                html = '',
                rel = 'suggestions',
                hide_if_empty = True,
                is_extended = True
            )
        else:
            return MdsView(
        )
        """

    def testMdsView(self):
        """Test MdsView"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
