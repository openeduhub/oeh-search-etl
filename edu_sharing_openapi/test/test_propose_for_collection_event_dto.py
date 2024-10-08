# coding: utf-8

"""
    edu-sharing Repository REST API

    The public restful API of the edu-sharing repository.

    The version of the OpenAPI document: 1.1
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from edu_sharing_client.models.propose_for_collection_event_dto import ProposeForCollectionEventDTO

class TestProposeForCollectionEventDTO(unittest.TestCase):
    """ProposeForCollectionEventDTO unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> ProposeForCollectionEventDTO:
        """Test ProposeForCollectionEventDTO
            include_optional is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `ProposeForCollectionEventDTO`
        """
        model = ProposeForCollectionEventDTO()
        if include_optional:
            return ProposeForCollectionEventDTO(
                node = edu_sharing_client.models.node_data_dto.NodeDataDTO(
                    type = '', 
                    aspects = [
                        ''
                        ], 
                    properties = {
                        'key' : None
                        }, ),
                collection = edu_sharing_client.models.collection_dto.CollectionDTO(
                    type = '', 
                    aspects = [
                        ''
                        ], 
                    properties = {
                        'key' : None
                        }, )
            )
        else:
            return ProposeForCollectionEventDTO(
        )
        """

    def testProposeForCollectionEventDTO(self):
        """Test ProposeForCollectionEventDTO"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
