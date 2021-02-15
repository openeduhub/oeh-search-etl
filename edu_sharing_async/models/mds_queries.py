# coding: utf-8

"""
    edu-sharing Repository REST API

    The public restful API of the edu-sharing repository.  # noqa: E501

    OpenAPI spec version: 1.1
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

import pprint
import re  # noqa: F401

import six

class MdsQueries(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'base_query': 'str',
        'queries': 'list[MdsQuery]'
    }

    attribute_map = {
        'base_query': 'baseQuery',
        'queries': 'queries'
    }

    def __init__(self, base_query=None, queries=None):  # noqa: E501
        """MdsQueries - a model defined in Swagger"""  # noqa: E501
        self._base_query = None
        self._queries = None
        self.discriminator = None
        self.base_query = base_query
        self.queries = queries

    @property
    def base_query(self):
        """Gets the base_query of this MdsQueries.  # noqa: E501


        :return: The base_query of this MdsQueries.  # noqa: E501
        :rtype: str
        """
        return self._base_query

    @base_query.setter
    def base_query(self, base_query):
        """Sets the base_query of this MdsQueries.


        :param base_query: The base_query of this MdsQueries.  # noqa: E501
        :type: str
        """
        if base_query is None:
            raise ValueError("Invalid value for `base_query`, must not be `None`")  # noqa: E501

        self._base_query = base_query

    @property
    def queries(self):
        """Gets the queries of this MdsQueries.  # noqa: E501


        :return: The queries of this MdsQueries.  # noqa: E501
        :rtype: list[MdsQuery]
        """
        return self._queries

    @queries.setter
    def queries(self, queries):
        """Sets the queries of this MdsQueries.


        :param queries: The queries of this MdsQueries.  # noqa: E501
        :type: list[MdsQuery]
        """
        if queries is None:
            raise ValueError("Invalid value for `queries`, must not be `None`")  # noqa: E501

        self._queries = queries

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.swagger_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value
        if issubclass(MdsQueries, dict):
            for key, value in self.items():
                result[key] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, MdsQueries):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
