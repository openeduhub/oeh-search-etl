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

class ConfigWorkflowList(object):
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
        'color': 'str',
        'has_receiver': 'bool',
        'next': 'list[str]'
    }

    attribute_map = {
        'id': 'id',
        'color': 'color',
        'has_receiver': 'hasReceiver',
        'next': 'next'
    }

    def __init__(self, id=None, color=None, has_receiver=False, next=None):  # noqa: E501
        """ConfigWorkflowList - a model defined in Swagger"""  # noqa: E501
        self._id = None
        self._color = None
        self._has_receiver = None
        self._next = None
        self.discriminator = None
        if id is not None:
            self.id = id
        if color is not None:
            self.color = color
        if has_receiver is not None:
            self.has_receiver = has_receiver
        if next is not None:
            self.next = next

    @property
    def id(self):
        """Gets the id of this ConfigWorkflowList.  # noqa: E501


        :return: The id of this ConfigWorkflowList.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this ConfigWorkflowList.


        :param id: The id of this ConfigWorkflowList.  # noqa: E501
        :type: str
        """

        self._id = id

    @property
    def color(self):
        """Gets the color of this ConfigWorkflowList.  # noqa: E501


        :return: The color of this ConfigWorkflowList.  # noqa: E501
        :rtype: str
        """
        return self._color

    @color.setter
    def color(self, color):
        """Sets the color of this ConfigWorkflowList.


        :param color: The color of this ConfigWorkflowList.  # noqa: E501
        :type: str
        """

        self._color = color

    @property
    def has_receiver(self):
        """Gets the has_receiver of this ConfigWorkflowList.  # noqa: E501


        :return: The has_receiver of this ConfigWorkflowList.  # noqa: E501
        :rtype: bool
        """
        return self._has_receiver

    @has_receiver.setter
    def has_receiver(self, has_receiver):
        """Sets the has_receiver of this ConfigWorkflowList.


        :param has_receiver: The has_receiver of this ConfigWorkflowList.  # noqa: E501
        :type: bool
        """

        self._has_receiver = has_receiver

    @property
    def next(self):
        """Gets the next of this ConfigWorkflowList.  # noqa: E501


        :return: The next of this ConfigWorkflowList.  # noqa: E501
        :rtype: list[str]
        """
        return self._next

    @next.setter
    def next(self, next):
        """Sets the next of this ConfigWorkflowList.


        :param next: The next of this ConfigWorkflowList.  # noqa: E501
        :type: list[str]
        """

        self._next = next

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
        if issubclass(ConfigWorkflowList, dict):
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
        if not isinstance(other, ConfigWorkflowList):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
