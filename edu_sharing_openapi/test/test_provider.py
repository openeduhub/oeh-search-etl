# coding: utf-8

"""
    edu-sharing Repository REST API

    The public restful API of the edu-sharing repository.

    The version of the OpenAPI document: 1.1
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from edu_sharing_client.models.provider import Provider

class TestProvider(unittest.TestCase):
    """Provider unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> Provider:
        """Test Provider
            include_optional is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `Provider`
        """
        model = Provider()
        if include_optional:
            return Provider(
                legal_name = '',
                url = '',
                email = '',
                area_served = 'Organization',
                location = edu_sharing_client.models.location.Location(
                    geo = edu_sharing_client.models.geo.Geo(
                        longitude = 1.337, 
                        latitude = 1.337, 
                        address_country = '', ), )
            )
        else:
            return Provider(
        )
        """

    def testProvider(self):
        """Test Provider"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
