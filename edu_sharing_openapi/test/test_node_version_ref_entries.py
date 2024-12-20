# coding: utf-8

"""
    edu-sharing Repository REST API

    The public restful API of the edu-sharing repository.

    The version of the OpenAPI document: 1.1
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from edu_sharing_client.models.node_version_ref_entries import NodeVersionRefEntries

class TestNodeVersionRefEntries(unittest.TestCase):
    """NodeVersionRefEntries unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> NodeVersionRefEntries:
        """Test NodeVersionRefEntries
            include_optional is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `NodeVersionRefEntries`
        """
        model = NodeVersionRefEntries()
        if include_optional:
            return NodeVersionRefEntries(
                versions = [
                    edu_sharing_client.models.node_version_ref.NodeVersionRef(
                        node = edu_sharing_client.models.node_ref.NodeRef(
                            repo = '', 
                            id = '', 
                            archived = True, 
                            is_home_repo = True, ), 
                        major = 56, 
                        minor = 56, )
                    ]
            )
        else:
            return NodeVersionRefEntries(
                versions = [
                    edu_sharing_client.models.node_version_ref.NodeVersionRef(
                        node = edu_sharing_client.models.node_ref.NodeRef(
                            repo = '', 
                            id = '', 
                            archived = True, 
                            is_home_repo = True, ), 
                        major = 56, 
                        minor = 56, )
                    ],
        )
        """

    def testNodeVersionRefEntries(self):
        """Test NodeVersionRefEntries"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()