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


class Language(object):
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
        '_global': 'dict(str, str)',
        'current': 'dict(str, str)',
        'current_language': 'str'
    }

    attribute_map = {
        '_global': 'global',
        'current': 'current',
        'current_language': 'currentLanguage'
    }

    def __init__(self, _global=None, current=None, current_language=None):  # noqa: E501
        """Language - a model defined in Swagger"""  # noqa: E501
        self.__global = None
        self._current = None
        self._current_language = None
        self.discriminator = None
        if _global is not None:
            self._global = _global
        if current is not None:
            self.current = current
        if current_language is not None:
            self.current_language = current_language

    @property
    def _global(self):
        """Gets the _global of this Language.  # noqa: E501


        :return: The _global of this Language.  # noqa: E501
        :rtype: dict(str, str)
        """
        return self.__global

    @_global.setter
    def _global(self, _global):
        """Sets the _global of this Language.


        :param _global: The _global of this Language.  # noqa: E501
        :type: dict(str, str)
        """

        self.__global = _global

    @property
    def current(self):
        """Gets the current of this Language.  # noqa: E501


        :return: The current of this Language.  # noqa: E501
        :rtype: dict(str, str)
        """
        return self._current

    @current.setter
    def current(self, current):
        """Sets the current of this Language.


        :param current: The current of this Language.  # noqa: E501
        :type: dict(str, str)
        """

        self._current = current

    @property
    def current_language(self):
        """Gets the current_language of this Language.  # noqa: E501


        :return: The current_language of this Language.  # noqa: E501
        :rtype: str
        """
        return self._current_language

    @current_language.setter
    def current_language(self, current_language):
        """Sets the current_language of this Language.


        :param current_language: The current_language of this Language.  # noqa: E501
        :type: str
        """

        self._current_language = current_language

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
        if issubclass(Language, dict):
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
        if not isinstance(other, Language):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
