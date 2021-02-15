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

class MdsForm(object):
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
        'panels': 'list[MdsFormPanel]'
    }

    attribute_map = {
        'id': 'id',
        'panels': 'panels'
    }

    def __init__(self, id=None, panels=None):  # noqa: E501
        """MdsForm - a model defined in Swagger"""  # noqa: E501
        self._id = None
        self._panels = None
        self.discriminator = None
        self.id = id
        self.panels = panels

    @property
    def id(self):
        """Gets the id of this MdsForm.  # noqa: E501


        :return: The id of this MdsForm.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this MdsForm.


        :param id: The id of this MdsForm.  # noqa: E501
        :type: str
        """
        if id is None:
            raise ValueError("Invalid value for `id`, must not be `None`")  # noqa: E501

        self._id = id

    @property
    def panels(self):
        """Gets the panels of this MdsForm.  # noqa: E501


        :return: The panels of this MdsForm.  # noqa: E501
        :rtype: list[MdsFormPanel]
        """
        return self._panels

    @panels.setter
    def panels(self, panels):
        """Sets the panels of this MdsForm.


        :param panels: The panels of this MdsForm.  # noqa: E501
        :type: list[MdsFormPanel]
        """
        if panels is None:
            raise ValueError("Invalid value for `panels`, must not be `None`")  # noqa: E501

        self._panels = panels

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
        if issubclass(MdsForm, dict):
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
        if not isinstance(other, MdsForm):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
