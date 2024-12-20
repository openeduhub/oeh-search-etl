# coding: utf-8

"""
    edu-sharing Repository REST API

    The public restful API of the edu-sharing repository.

    The version of the OpenAPI document: 1.1
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from edu_sharing_client.models.notification_event_dto import NotificationEventDTO

class TestNotificationEventDTO(unittest.TestCase):
    """NotificationEventDTO unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> NotificationEventDTO:
        """Test NotificationEventDTO
            include_optional is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `NotificationEventDTO`
        """
        model = NotificationEventDTO()
        if include_optional:
            return NotificationEventDTO(
                timestamp = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'),
                creator = edu_sharing_client.models.user_data_dto.UserDataDTO(
                    id = '', 
                    first_name = '', 
                    last_name = '', 
                    mailbox = '', ),
                receiver = edu_sharing_client.models.user_data_dto.UserDataDTO(
                    id = '', 
                    first_name = '', 
                    last_name = '', 
                    mailbox = '', ),
                status = 'PENDING',
                id = '',
                var_class = ''
            )
        else:
            return NotificationEventDTO(
                var_class = '',
        )
        """

    def testNotificationEventDTO(self):
        """Test NotificationEventDTO"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()