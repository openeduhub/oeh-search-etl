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

class JobDescription(object):
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
        'name': 'str',
        'description': 'str',
        'params': 'list[JobFieldDescription]'
    }

    attribute_map = {
        'name': 'name',
        'description': 'description',
        'params': 'params'
    }

    def __init__(self, name=None, description=None, params=None):  # noqa: E501
        """JobDescription - a model defined in Swagger"""  # noqa: E501
        self._name = None
        self._description = None
        self._params = None
        self.discriminator = None
        if name is not None:
            self.name = name
        if description is not None:
            self.description = description
        if params is not None:
            self.params = params

    @property
    def name(self):
        """Gets the name of this JobDescription.  # noqa: E501


        :return: The name of this JobDescription.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this JobDescription.


        :param name: The name of this JobDescription.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def description(self):
        """Gets the description of this JobDescription.  # noqa: E501


        :return: The description of this JobDescription.  # noqa: E501
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this JobDescription.


        :param description: The description of this JobDescription.  # noqa: E501
        :type: str
        """

        self._description = description

    @property
    def params(self):
        """Gets the params of this JobDescription.  # noqa: E501


        :return: The params of this JobDescription.  # noqa: E501
        :rtype: list[JobFieldDescription]
        """
        return self._params

    @params.setter
    def params(self, params):
        """Sets the params of this JobDescription.


        :param params: The params of this JobDescription.  # noqa: E501
        :type: list[JobFieldDescription]
        """

        self._params = params

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
        if issubclass(JobDescription, dict):
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
        if not isinstance(other, JobDescription):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
