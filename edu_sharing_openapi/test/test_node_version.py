# coding: utf-8

"""
    edu-sharing Repository REST API

    The public restful API of the edu-sharing repository.

    The version of the OpenAPI document: 1.1
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from edu_sharing_client.models.node_version import NodeVersion

class TestNodeVersion(unittest.TestCase):
    """NodeVersion unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> NodeVersion:
        """Test NodeVersion
            include_optional is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `NodeVersion`
        """
        model = NodeVersion()
        if include_optional:
            return NodeVersion(
                properties = {
                    'key' : [
                        ''
                        ]
                    },
                version = edu_sharing_client.models.node_version_ref.NodeVersionRef(
                    node = edu_sharing_client.models.node_ref.NodeRef(
                        repo = '', 
                        id = '', 
                        archived = True, 
                        is_home_repo = True, ), 
                    major = 56, 
                    minor = 56, ),
                comment = '',
                modified_at = '',
                modified_by = edu_sharing_client.models.person.Person(
                    profile = edu_sharing_client.models.user_profile.UserProfile(
                        primary_affiliation = '', 
                        skills = [
                            ''
                            ], 
                        types = [
                            ''
                            ], 
                        vcard = '', 
                        type = [
                            ''
                            ], 
                        first_name = '', 
                        last_name = '', 
                        email = '', 
                        avatar = '', 
                        about = '', ), 
                    first_name = '', 
                    last_name = '', 
                    mailbox = '', ),
                content_url = ''
            )
        else:
            return NodeVersion(
                version = edu_sharing_client.models.node_version_ref.NodeVersionRef(
                    node = edu_sharing_client.models.node_ref.NodeRef(
                        repo = '', 
                        id = '', 
                        archived = True, 
                        is_home_repo = True, ), 
                    major = 56, 
                    minor = 56, ),
                comment = '',
                modified_at = '',
                modified_by = edu_sharing_client.models.person.Person(
                    profile = edu_sharing_client.models.user_profile.UserProfile(
                        primary_affiliation = '', 
                        skills = [
                            ''
                            ], 
                        types = [
                            ''
                            ], 
                        vcard = '', 
                        type = [
                            ''
                            ], 
                        first_name = '', 
                        last_name = '', 
                        email = '', 
                        avatar = '', 
                        about = '', ), 
                    first_name = '', 
                    last_name = '', 
                    mailbox = '', ),
        )
        """

    def testNodeVersion(self):
        """Test NodeVersion"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
