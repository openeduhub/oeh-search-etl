# coding: utf-8

"""
    edu-sharing Repository REST API

    The public restful API of the edu-sharing repository.

    The version of the OpenAPI document: 1.1
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from edu_sharing_client.models.about import About

class TestAbout(unittest.TestCase):
    """About unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> About:
        """Test About
            include_optional is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `About`
        """
        model = About()
        if include_optional:
            return About(
                plugins = [
                    edu_sharing_client.models.plugin_info.PluginInfo(
                        id = '', )
                    ],
                features = [
                    edu_sharing_client.models.feature_info.FeatureInfo(
                        id = 'handleService', )
                    ],
                themes_url = '',
                last_cache_update = 56,
                version = edu_sharing_client.models.service_version.ServiceVersion(
                    repository = '', 
                    renderservice = '', 
                    major = 56, 
                    minor = 56, ),
                services = [
                    edu_sharing_client.models.about_service.AboutService(
                        name = '', 
                        instances = [
                            edu_sharing_client.models.service_instance.ServiceInstance(
                                version = edu_sharing_client.models.service_version.ServiceVersion(
                                    repository = '', 
                                    renderservice = '', 
                                    major = 56, 
                                    minor = 56, ), 
                                endpoint = '', )
                            ], )
                    ]
            )
        else:
            return About(
                version = edu_sharing_client.models.service_version.ServiceVersion(
                    repository = '', 
                    renderservice = '', 
                    major = 56, 
                    minor = 56, ),
                services = [
                    edu_sharing_client.models.about_service.AboutService(
                        name = '', 
                        instances = [
                            edu_sharing_client.models.service_instance.ServiceInstance(
                                version = edu_sharing_client.models.service_version.ServiceVersion(
                                    repository = '', 
                                    renderservice = '', 
                                    major = 56, 
                                    minor = 56, ), 
                                endpoint = '', )
                            ], )
                    ],
        )
        """

    def testAbout(self):
        """Test About"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
