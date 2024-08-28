# coding: utf-8

"""
    edu-sharing Repository REST API

    The public restful API of the edu-sharing repository.

    The version of the OpenAPI document: 1.1
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from edu_sharing_client.models.job_info import JobInfo

class TestJobInfo(unittest.TestCase):
    """JobInfo unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> JobInfo:
        """Test JobInfo
            include_optional is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `JobInfo`
        """
        model = JobInfo()
        if include_optional:
            return JobInfo(
                job_data_map = {
                    'key' : None
                    },
                job_name = '',
                job_group = '',
                start_time = 56,
                finish_time = 56,
                status = 'Running',
                worst_level = edu_sharing_client.models.level.Level(
                    syslog_equivalent = 56, 
                    version2_level = edu_sharing_client.models.level.Level(
                        syslog_equivalent = 56, ), ),
                log = [
                    edu_sharing_client.models.log_entry.LogEntry(
                        class_name = '', 
                        level = edu_sharing_client.models.level.Level(
                            syslog_equivalent = 56, 
                            version2_level = edu_sharing_client.models.level.Level(
                                syslog_equivalent = 56, ), ), 
                        date = 56, 
                        message = '', )
                    ],
                job_detail = edu_sharing_client.models.job_detail.JobDetail(
                    key = edu_sharing_client.models.job_key.JobKey(
                        name = '', 
                        group = '', ), 
                    job_data_map = {
                        'key' : None
                        }, 
                    durable = True, 
                    persist_job_data_after_execution = True, 
                    concurrent_exection_disallowed = True, 
                    job_builder = edu_sharing_client.models.job_builder.JobBuilder(
                        job_data = edu_sharing_client.models.job_builder.JobBuilder(), ), 
                    description = '', )
            )
        else:
            return JobInfo(
        )
        """

    def testJobInfo(self):
        """Test JobInfo"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()