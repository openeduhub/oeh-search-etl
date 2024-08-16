# coding: utf-8

"""
    edu-sharing Repository REST API

    The public restful API of the edu-sharing repository.

    The version of the OpenAPI document: 1.1
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from edu_sharing_client.models.query import Query

class TestQuery(unittest.TestCase):
    """Query unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> Query:
        """Test Query
            include_optional is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `Query`
        """
        model = Query()
        if include_optional:
            return Query(
                condition = edu_sharing_client.models.condition.Condition(
                    type = 'TOOLPERMISSION', 
                    negate = True, 
                    value = '', ),
                query = ''
            )
        else:
            return Query(
        )
        """

    def testQuery(self):
        """Test Query"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
