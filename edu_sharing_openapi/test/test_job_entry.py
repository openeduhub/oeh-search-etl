# coding: utf-8

"""
    edu-sharing Repository REST API

    The public restful API of the edu-sharing repository.

    The version of the OpenAPI document: 1.1
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from edu_sharing_client.models.job_entry import JobEntry

class TestJobEntry(unittest.TestCase):
    """JobEntry unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> JobEntry:
        """Test JobEntry
            include_optional is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `JobEntry`
        """
        model = JobEntry()
        if include_optional:
            return JobEntry(
                data = edu_sharing_client.models.job.Job(
                    id = '', 
                    status = '', )
            )
        else:
            return JobEntry(
                data = edu_sharing_client.models.job.Job(
                    id = '', 
                    status = '', ),
        )
        """

    def testJobEntry(self):
        """Test JobEntry"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
