# coding: utf-8

"""
    edu-sharing Repository REST API

    The public restful API of the edu-sharing repository.

    The version of the OpenAPI document: 1.1
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from edu_sharing_client.models.comment import Comment

class TestComment(unittest.TestCase):
    """Comment unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> Comment:
        """Test Comment
            include_optional is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `Comment`
        """
        model = Comment()
        if include_optional:
            return Comment(
                ref = edu_sharing_client.models.node_ref.NodeRef(
                    repo = '', 
                    id = '', 
                    archived = True, 
                    is_home_repo = True, ),
                reply_to = edu_sharing_client.models.node_ref.NodeRef(
                    repo = '', 
                    id = '', 
                    archived = True, 
                    is_home_repo = True, ),
                creator = edu_sharing_client.models.user_simple.UserSimple(
                    properties = {
                        'key' : [
                            ''
                            ]
                        }, 
                    editable = True, 
                    status = edu_sharing_client.models.user_status.UserStatus(
                        date = 56, ), 
                    organizations = [
                        edu_sharing_client.models.organization.Organization(
                            editable = True, 
                            signup_method = 'simple', 
                            ref = edu_sharing_client.models.node_ref.NodeRef(
                                repo = '', 
                                id = '', 
                                archived = True, 
                                is_home_repo = True, ), 
                            aspects = [
                                ''
                                ], 
                            authority_name = '', 
                            authority_type = 'USER', 
                            group_name = '', 
                            profile = edu_sharing_client.models.group_profile.GroupProfile(
                                group_email = '', 
                                display_name = '', 
                                group_type = '', 
                                scope_type = '', ), 
                            administration_access = True, 
                            shared_folder = edu_sharing_client.models.node_ref.NodeRef(
                                repo = '', 
                                id = '', 
                                archived = True, 
                                is_home_repo = True, ), )
                        ], 
                    authority_name = '', 
                    authority_type = 'USER', 
                    user_name = '', 
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
                        about = '', ), ),
                created = 56,
                comment = ''
            )
        else:
            return Comment(
        )
        """

    def testComment(self):
        """Test Comment"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
