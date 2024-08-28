# coding: utf-8

"""
    edu-sharing Repository REST API

    The public restful API of the edu-sharing repository.

    The version of the OpenAPI document: 1.1
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from edu_sharing_client.models.rendering import Rendering

class TestRendering(unittest.TestCase):
    """Rendering unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> Rendering:
        """Test Rendering
            include_optional is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `Rendering`
        """
        model = Rendering()
        if include_optional:
            return Rendering(
                show_preview = True,
                show_download_button = True,
                prerender = True,
                gdpr = [
                    edu_sharing_client.models.rendering_gdpr.RenderingGdpr(
                        matcher = '', 
                        name = '', 
                        privacy_information_url = '', )
                    ]
            )
        else:
            return Rendering(
        )
        """

    def testRendering(self):
        """Test Rendering"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()