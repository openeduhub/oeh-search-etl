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

class ServerUpdateInfo(object):
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
        'id': 'str',
        'description': 'str',
        'executed_at': 'int'
    }

    attribute_map = {
        'id': 'id',
        'description': 'description',
        'executed_at': 'executedAt'
    }

    def __init__(self, id=None, description=None, executed_at=None):  # noqa: E501
        """ServerUpdateInfo - a model defined in Swagger"""  # noqa: E501
        self._id = None
        self._description = None
        self._executed_at = None
        self.discriminator = None
        if id is not None:
            self.id = id
        if description is not None:
            self.description = description
        if executed_at is not None:
            self.executed_at = executed_at

    @property
    def id(self):
        """Gets the id of this ServerUpdateInfo.  # noqa: E501


        :return: The id of this ServerUpdateInfo.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this ServerUpdateInfo.


        :param id: The id of this ServerUpdateInfo.  # noqa: E501
        :type: str
        """

        self._id = id

    @property
    def description(self):
        """Gets the description of this ServerUpdateInfo.  # noqa: E501


        :return: The description of this ServerUpdateInfo.  # noqa: E501
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this ServerUpdateInfo.


        :param description: The description of this ServerUpdateInfo.  # noqa: E501
        :type: str
        """

        self._description = description

    @property
    def executed_at(self):
        """Gets the executed_at of this ServerUpdateInfo.  # noqa: E501


        :return: The executed_at of this ServerUpdateInfo.  # noqa: E501
        :rtype: int
        """
        return self._executed_at

    @executed_at.setter
    def executed_at(self, executed_at):
        """Sets the executed_at of this ServerUpdateInfo.


        :param executed_at: The executed_at of this ServerUpdateInfo.  # noqa: E501
        :type: int
        """

        self._executed_at = executed_at

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
        if issubclass(ServerUpdateInfo, dict):
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
        if not isinstance(other, ServerUpdateInfo):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other