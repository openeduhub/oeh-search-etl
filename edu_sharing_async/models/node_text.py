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

class NodeText(object):
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
        'text': 'str',
        'html': 'str',
        'raw': 'str'
    }

    attribute_map = {
        'text': 'text',
        'html': 'html',
        'raw': 'raw'
    }

    def __init__(self, text=None, html=None, raw=None):  # noqa: E501
        """NodeText - a model defined in Swagger"""  # noqa: E501
        self._text = None
        self._html = None
        self._raw = None
        self.discriminator = None
        if text is not None:
            self.text = text
        if html is not None:
            self.html = html
        if raw is not None:
            self.raw = raw

    @property
    def text(self):
        """Gets the text of this NodeText.  # noqa: E501


        :return: The text of this NodeText.  # noqa: E501
        :rtype: str
        """
        return self._text

    @text.setter
    def text(self, text):
        """Sets the text of this NodeText.


        :param text: The text of this NodeText.  # noqa: E501
        :type: str
        """

        self._text = text

    @property
    def html(self):
        """Gets the html of this NodeText.  # noqa: E501


        :return: The html of this NodeText.  # noqa: E501
        :rtype: str
        """
        return self._html

    @html.setter
    def html(self, html):
        """Sets the html of this NodeText.


        :param html: The html of this NodeText.  # noqa: E501
        :type: str
        """

        self._html = html

    @property
    def raw(self):
        """Gets the raw of this NodeText.  # noqa: E501


        :return: The raw of this NodeText.  # noqa: E501
        :rtype: str
        """
        return self._raw

    @raw.setter
    def raw(self, raw):
        """Sets the raw of this NodeText.


        :param raw: The raw of this NodeText.  # noqa: E501
        :type: str
        """

        self._raw = raw

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
        if issubclass(NodeText, dict):
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
        if not isinstance(other, NodeText):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other