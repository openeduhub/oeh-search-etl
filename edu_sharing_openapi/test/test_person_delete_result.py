# coding: utf-8

"""
    edu-sharing Repository REST API

    The public restful API of the edu-sharing repository.

    The version of the OpenAPI document: 1.1
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from edu_sharing_client.models.person_delete_result import PersonDeleteResult

class TestPersonDeleteResult(unittest.TestCase):
    """PersonDeleteResult unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> PersonDeleteResult:
        """Test PersonDeleteResult
            include_optional is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `PersonDeleteResult`
        """
        model = PersonDeleteResult()
        if include_optional:
            return PersonDeleteResult(
                authority_name = '',
                deleted_name = '',
                home_folder = {
                    'key' : edu_sharing_client.models.counts.Counts(
                        elements = [
                            edu_sharing_client.models.element.Element(
                                id = '', 
                                name = '', 
                                type = '', )
                            ], )
                    },
                shared_folders = {
                    'key' : edu_sharing_client.models.counts.Counts(
                        elements = [
                            edu_sharing_client.models.element.Element(
                                id = '', 
                                name = '', 
                                type = '', )
                            ], )
                    },
                collections = edu_sharing_client.models.collection_counts.CollectionCounts(
                    refs = [
                        edu_sharing_client.models.element.Element(
                            id = '', 
                            name = '', 
                            type = '', )
                        ], 
                    collections = [
                        edu_sharing_client.models.element.Element(
                            id = '', 
                            name = '', 
                            type = '', )
                        ], ),
                comments = 56,
                ratings = 56,
                collection_feedback = 56,
                stream = 56
            )
        else:
            return PersonDeleteResult(
        )
        """

    def testPersonDeleteResult(self):
        """Test PersonDeleteResult"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()