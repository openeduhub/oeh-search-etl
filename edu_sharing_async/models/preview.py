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

class Preview(object):
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
        'is_icon': 'bool',
        'is_generated': 'bool',
        'type': 'str',
        'url': 'str',
        'width': 'int',
        'height': 'int'
    }

    attribute_map = {
        'is_icon': 'isIcon',
        'is_generated': 'isGenerated',
        'type': 'type',
        'url': 'url',
        'width': 'width',
        'height': 'height'
    }

    def __init__(self, is_icon=False, is_generated=False, type=None, url=None, width=None, height=None):  # noqa: E501
        """Preview - a model defined in Swagger"""  # noqa: E501
        self._is_icon = None
        self._is_generated = None
        self._type = None
        self._url = None
        self._width = None
        self._height = None
        self.discriminator = None
        self.is_icon = is_icon
        if is_generated is not None:
            self.is_generated = is_generated
        if type is not None:
            self.type = type
        self.url = url
        self.width = width
        self.height = height

    @property
    def is_icon(self):
        """Gets the is_icon of this Preview.  # noqa: E501


        :return: The is_icon of this Preview.  # noqa: E501
        :rtype: bool
        """
        return self._is_icon

    @is_icon.setter
    def is_icon(self, is_icon):
        """Sets the is_icon of this Preview.


        :param is_icon: The is_icon of this Preview.  # noqa: E501
        :type: bool
        """
        if is_icon is None:
            raise ValueError("Invalid value for `is_icon`, must not be `None`")  # noqa: E501

        self._is_icon = is_icon

    @property
    def is_generated(self):
        """Gets the is_generated of this Preview.  # noqa: E501


        :return: The is_generated of this Preview.  # noqa: E501
        :rtype: bool
        """
        return self._is_generated

    @is_generated.setter
    def is_generated(self, is_generated):
        """Sets the is_generated of this Preview.


        :param is_generated: The is_generated of this Preview.  # noqa: E501
        :type: bool
        """

        self._is_generated = is_generated

    @property
    def type(self):
        """Gets the type of this Preview.  # noqa: E501


        :return: The type of this Preview.  # noqa: E501
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """Sets the type of this Preview.


        :param type: The type of this Preview.  # noqa: E501
        :type: str
        """

        self._type = type

    @property
    def url(self):
        """Gets the url of this Preview.  # noqa: E501


        :return: The url of this Preview.  # noqa: E501
        :rtype: str
        """
        return self._url

    @url.setter
    def url(self, url):
        """Sets the url of this Preview.


        :param url: The url of this Preview.  # noqa: E501
        :type: str
        """
        if url is None:
            raise ValueError("Invalid value for `url`, must not be `None`")  # noqa: E501

        self._url = url

    @property
    def width(self):
        """Gets the width of this Preview.  # noqa: E501


        :return: The width of this Preview.  # noqa: E501
        :rtype: int
        """
        return self._width

    @width.setter
    def width(self, width):
        """Sets the width of this Preview.


        :param width: The width of this Preview.  # noqa: E501
        :type: int
        """
        if width is None:
            raise ValueError("Invalid value for `width`, must not be `None`")  # noqa: E501

        self._width = width

    @property
    def height(self):
        """Gets the height of this Preview.  # noqa: E501


        :return: The height of this Preview.  # noqa: E501
        :rtype: int
        """
        return self._height

    @height.setter
    def height(self, height):
        """Sets the height of this Preview.


        :param height: The height of this Preview.  # noqa: E501
        :type: int
        """
        if height is None:
            raise ValueError("Invalid value for `height`, must not be `None`")  # noqa: E501

        self._height = height

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
        if issubclass(Preview, dict):
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
        if not isinstance(other, Preview):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other