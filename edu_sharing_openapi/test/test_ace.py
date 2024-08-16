# coding: utf-8

"""
    edu-sharing Repository REST API

    The public restful API of the edu-sharing repository.

    The version of the OpenAPI document: 1.1
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from edu_sharing_client.models.ace import ACE

class TestACE(unittest.TestCase):
    """ACE unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> ACE:
        """Test ACE
            include_optional is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `ACE`
        """
        model = ACE()
        if include_optional:
            return ACE(
                editable = True,
                authority = edu_sharing_client.models.authority.Authority(
                    properties = {
                        'key' : [
                            ''
                            ]
                        }, 
                    editable = True, 
                    authority_name = '', 
                    authority_type = 'USER', ),
                user = edu_sharing_client.models.user_profile.UserProfile(
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
                group = edu_sharing_client.models.group_profile.GroupProfile(
                    group_email = '', 
                    display_name = '', 
                    group_type = '', 
                    scope_type = '', ),
                permissions = [
                    ''
                    ]
            )
        else:
            return ACE(
                authority = edu_sharing_client.models.authority.Authority(
                    properties = {
                        'key' : [
                            ''
                            ]
                        }, 
                    editable = True, 
                    authority_name = '', 
                    authority_type = 'USER', ),
                permissions = [
                    ''
                    ],
        )
        """

    def testACE(self):
        """Test ACE"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
