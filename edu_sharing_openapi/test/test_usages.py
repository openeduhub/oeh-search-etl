# coding: utf-8

"""
    edu-sharing Repository REST API

    The public restful API of the edu-sharing repository.

    The version of the OpenAPI document: 1.1
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from edu_sharing_client.models.usages import Usages

class TestUsages(unittest.TestCase):
    """Usages unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> Usages:
        """Test Usages
            include_optional is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `Usages`
        """
        model = Usages()
        if include_optional:
            return Usages(
                usages = [
                    edu_sharing_client.models.usage.Usage(
                        from_used = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                        to_used = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                        usage_counter = 56, 
                        app_subtype = '', 
                        app_type = '', 
                        type = '', 
                        created = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                        modified = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                        app_user = '', 
                        app_user_mail = '', 
                        course_id = '', 
                        distinct_persons = 56, 
                        app_id = '', 
                        node_id = '', 
                        parent_node_id = '', 
                        usage_version = '', 
                        usage_xml_params = edu_sharing_client.models.parameters.Parameters(
                            general = edu_sharing_client.models.general.General(
                                referenced_in_name = '', 
                                referenced_in_type = '', 
                                referenced_in_instance = '', ), ), 
                        usage_xml_params_raw = '', 
                        resource_id = '', 
                        guid = '', )
                    ]
            )
        else:
            return Usages(
        )
        """

    def testUsages(self):
        """Test Usages"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
