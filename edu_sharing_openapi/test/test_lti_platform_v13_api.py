# coding: utf-8

"""
    edu-sharing Repository REST API

    The public restful API of the edu-sharing repository.

    The version of the OpenAPI document: 1.1
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from edu_sharing_client.api.lti_platform_v13_api import LTIPlatformV13Api


class TestLTIPlatformV13Api(unittest.TestCase):
    """LTIPlatformV13Api unit test stubs"""

    def setUp(self) -> None:
        self.api = LTIPlatformV13Api()

    def tearDown(self) -> None:
        pass

    def test_auth(self) -> None:
        """Test case for auth

        LTI Platform oidc endpoint. responds to a login authentication request
        """
        pass

    def test_auth_token_endpoint(self) -> None:
        """Test case for auth_token_endpoint

        LTIPlatform auth token endpoint
        """
        pass

    def test_change_content(self) -> None:
        """Test case for change_content

        Custom edu-sharing endpoint to change content of node.
        """
        pass

    def test_convert_to_resourcelink(self) -> None:
        """Test case for convert_to_resourcelink

        manual convertion of an io to an resource link without deeplinking
        """
        pass

    def test_deep_linking_response(self) -> None:
        """Test case for deep_linking_response

        receiving deeplink response messages.
        """
        pass

    def test_generate_login_initiation_form(self) -> None:
        """Test case for generate_login_initiation_form

        generate a form used for Initiating Login from a Third Party. Use thes endpoint when starting a lti deeplink flow.
        """
        pass

    def test_generate_login_initiation_form_resource_link(self) -> None:
        """Test case for generate_login_initiation_form_resource_link

        generate a form used for Initiating Login from a Third Party. Use thes endpoint when starting a lti resourcelink flow.
        """
        pass

    def test_get_content(self) -> None:
        """Test case for get_content

        Custom edu-sharing endpoint to get content of node.
        """
        pass

    def test_manual_registration(self) -> None:
        """Test case for manual_registration

        manual registration endpoint for registration of tools.
        """
        pass

    def test_open_id_registration(self) -> None:
        """Test case for open_id_registration

        registration endpoint the tool uses to register at platform.
        """
        pass

    def test_openid_configuration(self) -> None:
        """Test case for openid_configuration

        LTIPlatform openid configuration
        """
        pass

    def test_start_dynamic_registration(self) -> None:
        """Test case for start_dynamic_registration

        starts lti dynamic registration.
        """
        pass

    def test_start_dynamic_registration_get(self) -> None:
        """Test case for start_dynamic_registration_get

        starts lti dynamic registration.
        """
        pass

    def test_test_token(self) -> None:
        """Test case for test_token

        test creates a token signed with homeapp.
        """
        pass

    def test_tools(self) -> None:
        """Test case for tools

        List of tools registered
        """
        pass


if __name__ == '__main__':
    unittest.main()