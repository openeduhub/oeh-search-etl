# coding: utf-8

"""
    edu-sharing Repository REST API

    The public restful API of the edu-sharing repository.

    The version of the OpenAPI document: 1.1
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from edu_sharing_client.models.search_parameters import SearchParameters

class TestSearchParameters(unittest.TestCase):
    """SearchParameters unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> SearchParameters:
        """Test SearchParameters
            include_optional is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `SearchParameters`
        """
        model = SearchParameters()
        if include_optional:
            return SearchParameters(
                permissions = [
                    ''
                    ],
                resolve_collections = True,
                resolve_usernames = True,
                return_suggestions = True,
                excludes = [
                    ''
                    ],
                facets = [
                    ''
                    ],
                facet_min_count = 56,
                facet_limit = 56,
                facet_suggest = '',
                criteria = [
                    edu_sharing_client.models.mds_query_criteria.MdsQueryCriteria(
                        property = '', 
                        values = [
                            ''
                            ], )
                    ]
            )
        else:
            return SearchParameters(
                criteria = [
                    edu_sharing_client.models.mds_query_criteria.MdsQueryCriteria(
                        property = '', 
                        values = [
                            ''
                            ], )
                    ],
        )
        """

    def testSearchParameters(self):
        """Test SearchParameters"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
