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

class Authority(object):
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
        'properties': 'dict(str, list[str])',
        'authority_name': 'str',
        'authority_type': 'str'
    }

    attribute_map = {
        'properties': 'properties',
        'authority_name': 'authorityName',
        'authority_type': 'authorityType'
    }

    def __init__(self, properties=None, authority_name=None, authority_type=None):  # noqa: E501
        """Authority - a model defined in Swagger"""  # noqa: E501
        self._properties = None
        self._authority_name = None
        self._authority_type = None
        self.discriminator = None
        if properties is not None:
            self.properties = properties
        self.authority_name = authority_name
        if authority_type is not None:
            self.authority_type = authority_type

    @property
    def properties(self):
        """Gets the properties of this Authority.  # noqa: E501


        :return: The properties of this Authority.  # noqa: E501
        :rtype: dict(str, list[str])
        """
        return self._properties

    @properties.setter
    def properties(self, properties):
        """Sets the properties of this Authority.


        :param properties: The properties of this Authority.  # noqa: E501
        :type: dict(str, list[str])
        """

        self._properties = properties

    @property
    def authority_name(self):
        """Gets the authority_name of this Authority.  # noqa: E501


        :return: The authority_name of this Authority.  # noqa: E501
        :rtype: str
        """
        return self._authority_name

    @authority_name.setter
    def authority_name(self, authority_name):
        """Sets the authority_name of this Authority.


        :param authority_name: The authority_name of this Authority.  # noqa: E501
        :type: str
        """
        if authority_name is None:
            raise ValueError("Invalid value for `authority_name`, must not be `None`")  # noqa: E501

        self._authority_name = authority_name

    @property
    def authority_type(self):
        """Gets the authority_type of this Authority.  # noqa: E501


        :return: The authority_type of this Authority.  # noqa: E501
        :rtype: str
        """
        return self._authority_type

    @authority_type.setter
    def authority_type(self, authority_type):
        """Sets the authority_type of this Authority.


        :param authority_type: The authority_type of this Authority.  # noqa: E501
        :type: str
        """
        allowed_values = ["USER", "GROUP", "OWNER", "EVERYONE", "GUEST"]  # noqa: E501
        if authority_type not in allowed_values:
            raise ValueError(
                "Invalid value for `authority_type` ({0}), must be one of {1}"  # noqa: E501
                .format(authority_type, allowed_values)
            )

        self._authority_type = authority_type

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
        if issubclass(Authority, dict):
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
        if not isinstance(other, Authority):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
