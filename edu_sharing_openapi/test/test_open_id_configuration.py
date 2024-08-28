# coding: utf-8

"""
    edu-sharing Repository REST API

    The public restful API of the edu-sharing repository.

    The version of the OpenAPI document: 1.1
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from edu_sharing_client.models.open_id_configuration import OpenIdConfiguration

class TestOpenIdConfiguration(unittest.TestCase):
    """OpenIdConfiguration unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> OpenIdConfiguration:
        """Test OpenIdConfiguration
            include_optional is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `OpenIdConfiguration`
        """
        model = OpenIdConfiguration()
        if include_optional:
            return OpenIdConfiguration(
                issuer = '',
                token_endpoint = '',
                token_endpoint_auth_methods_supported = [
                    ''
                    ],
                token_endpoint_auth_signing_alg_values_supported = [
                    ''
                    ],
                jwks_uri = '',
                authorization_endpoint = '',
                registration_endpoint = '',
                scopes_supported = [
                    ''
                    ],
                response_types_supported = [
                    ''
                    ],
                subject_types_supported = [
                    ''
                    ],
                id_token_signing_alg_values_supported = [
                    ''
                    ],
                claims_supported = [
                    ''
                    ],
                https__purl_imsglobal_org_spec_lti_platform_configuration = edu_sharing_client.models.lti_platform_configuration.LTIPlatformConfiguration(
                    product_family_code = '', 
                    version = '', 
                    messages_supported = [
                        edu_sharing_client.models.message.Message(
                            type = '', 
                            placements = [
                                ''
                                ], )
                        ], 
                    variables = [
                        ''
                        ], )
            )
        else:
            return OpenIdConfiguration(
        )
        """

    def testOpenIdConfiguration(self):
        """Test OpenIdConfiguration"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()