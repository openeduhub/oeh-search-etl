# coding: utf-8

"""
    edu-sharing Repository REST API

    The public restful API of the edu-sharing repository.

    The version of the OpenAPI document: 1.1
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from edu_sharing_client.api.statisticv1_api import STATISTICV1Api


class TestSTATISTICV1Api(unittest.TestCase):
    """STATISTICV1Api unit test stubs"""

    def setUp(self) -> None:
        self.api = STATISTICV1Api()

    def tearDown(self) -> None:
        pass

    def test_get(self) -> None:
        """Test case for get

        Get statistics of repository.
        """
        pass

    def test_get_global_statistics(self) -> None:
        """Test case for get_global_statistics

        Get stats.
        """
        pass

    def test_get_node_data(self) -> None:
        """Test case for get_node_data

        get the range of nodes which had tracked actions since a given timestamp
        """
        pass

    def test_get_nodes_altered_in_range1(self) -> None:
        """Test case for get_nodes_altered_in_range1

        get the range of nodes which had tracked actions since a given timestamp
        """
        pass

    def test_get_statistics_node(self) -> None:
        """Test case for get_statistics_node

        get statistics for node actions
        """
        pass

    def test_get_statistics_user(self) -> None:
        """Test case for get_statistics_user

        get statistics for user actions (login, logout)
        """
        pass


if __name__ == '__main__':
    unittest.main()