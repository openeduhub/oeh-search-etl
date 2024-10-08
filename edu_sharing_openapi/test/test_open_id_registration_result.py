# coding: utf-8

"""
    edu-sharing Repository REST API

    The public restful API of the edu-sharing repository.

    The version of the OpenAPI document: 1.1
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from edu_sharing_client.models.open_id_registration_result import OpenIdRegistrationResult

class TestOpenIdRegistrationResult(unittest.TestCase):
    """OpenIdRegistrationResult unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> OpenIdRegistrationResult:
        """Test OpenIdRegistrationResult
            include_optional is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `OpenIdRegistrationResult`
        """
        model = OpenIdRegistrationResult()
        if include_optional:
            return OpenIdRegistrationResult(
                client_id = '',
                response_types = [
                    ''
                    ],
                jwks_uri = '',
                initiate_login_uri = '',
                grant_types = [
                    ''
                    ],
                redirect_uris = [
                    ''
                    ],
                application_type = '',
                token_endpoint_auth_method = '',
                client_name = '',
                logo_uri = '',
                scope = '',
                https__purl_imsglobal_org_spec_lti_tool_configuration = edu_sharing_client.models.lti_tool_configuration.LTIToolConfiguration(
                    version = '', 
                    deployment_id = '', 
                    target_link_uri = '', 
                    domain = '', 
                    description = '', 
                    claims = [
                        ''
                        ], )
            )
        else:
            return OpenIdRegistrationResult(
        )
        """

    def testOpenIdRegistrationResult(self):
        """Test OpenIdRegistrationResult"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
