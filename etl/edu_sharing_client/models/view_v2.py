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


class ViewV2(object):
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
        'caption': 'str',
        'icon': 'str',
        'html': 'str',
        'rel': 'str',
        'hide_if_empty': 'bool'
    }

    attribute_map = {
        'id': 'id',
        'caption': 'caption',
        'icon': 'icon',
        'html': 'html',
        'rel': 'rel',
        'hide_if_empty': 'hideIfEmpty'
    }

    def __init__(self, id=None, caption=None, icon=None, html=None, rel=None, hide_if_empty=False):  # noqa: E501
        """ViewV2 - a model defined in Swagger"""  # noqa: E501
        self._id = None
        self._caption = None
        self._icon = None
        self._html = None
        self._rel = None
        self._hide_if_empty = None
        self.discriminator = None
        if id is not None:
            self.id = id
        if caption is not None:
            self.caption = caption
        if icon is not None:
            self.icon = icon
        if html is not None:
            self.html = html
        if rel is not None:
            self.rel = rel
        if hide_if_empty is not None:
            self.hide_if_empty = hide_if_empty

    @property
    def id(self):
        """Gets the id of this ViewV2.  # noqa: E501


        :return: The id of this ViewV2.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this ViewV2.


        :param id: The id of this ViewV2.  # noqa: E501
        :type: str
        """

        self._id = id

    @property
    def caption(self):
        """Gets the caption of this ViewV2.  # noqa: E501


        :return: The caption of this ViewV2.  # noqa: E501
        :rtype: str
        """
        return self._caption

    @caption.setter
    def caption(self, caption):
        """Sets the caption of this ViewV2.


        :param caption: The caption of this ViewV2.  # noqa: E501
        :type: str
        """

        self._caption = caption

    @property
    def icon(self):
        """Gets the icon of this ViewV2.  # noqa: E501


        :return: The icon of this ViewV2.  # noqa: E501
        :rtype: str
        """
        return self._icon

    @icon.setter
    def icon(self, icon):
        """Sets the icon of this ViewV2.


        :param icon: The icon of this ViewV2.  # noqa: E501
        :type: str
        """

        self._icon = icon

    @property
    def html(self):
        """Gets the html of this ViewV2.  # noqa: E501


        :return: The html of this ViewV2.  # noqa: E501
        :rtype: str
        """
        return self._html

    @html.setter
    def html(self, html):
        """Sets the html of this ViewV2.


        :param html: The html of this ViewV2.  # noqa: E501
        :type: str
        """

        self._html = html

    @property
    def rel(self):
        """Gets the rel of this ViewV2.  # noqa: E501


        :return: The rel of this ViewV2.  # noqa: E501
        :rtype: str
        """
        return self._rel

    @rel.setter
    def rel(self, rel):
        """Sets the rel of this ViewV2.


        :param rel: The rel of this ViewV2.  # noqa: E501
        :type: str
        """

        self._rel = rel

    @property
    def hide_if_empty(self):
        """Gets the hide_if_empty of this ViewV2.  # noqa: E501


        :return: The hide_if_empty of this ViewV2.  # noqa: E501
        :rtype: bool
        """
        return self._hide_if_empty

    @hide_if_empty.setter
    def hide_if_empty(self, hide_if_empty):
        """Sets the hide_if_empty of this ViewV2.


        :param hide_if_empty: The hide_if_empty of this ViewV2.  # noqa: E501
        :type: bool
        """

        self._hide_if_empty = hide_if_empty

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
        if issubclass(ViewV2, dict):
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
        if not isinstance(other, ViewV2):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
