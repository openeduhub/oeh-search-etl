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

class Tracking(object):
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
        'counts': 'dict(str, int)',
        '_date': 'str',
        'fields': 'dict(str, Serializable)',
        'groups': 'dict(str, dict(str, dict(str, int)))',
        'authority': 'TrackingAuthority'
    }

    attribute_map = {
        'counts': 'counts',
        '_date': 'date',
        'fields': 'fields',
        'groups': 'groups',
        'authority': 'authority'
    }

    def __init__(self, counts=None, _date=None, fields=None, groups=None, authority=None):  # noqa: E501
        """Tracking - a model defined in Swagger"""  # noqa: E501
        self._counts = None
        self.__date = None
        self._fields = None
        self._groups = None
        self._authority = None
        self.discriminator = None
        if counts is not None:
            self.counts = counts
        if _date is not None:
            self._date = _date
        if fields is not None:
            self.fields = fields
        if groups is not None:
            self.groups = groups
        if authority is not None:
            self.authority = authority

    @property
    def counts(self):
        """Gets the counts of this Tracking.  # noqa: E501


        :return: The counts of this Tracking.  # noqa: E501
        :rtype: dict(str, int)
        """
        return self._counts

    @counts.setter
    def counts(self, counts):
        """Sets the counts of this Tracking.


        :param counts: The counts of this Tracking.  # noqa: E501
        :type: dict(str, int)
        """

        self._counts = counts

    @property
    def _date(self):
        """Gets the _date of this Tracking.  # noqa: E501


        :return: The _date of this Tracking.  # noqa: E501
        :rtype: str
        """
        return self.__date

    @_date.setter
    def _date(self, _date):
        """Sets the _date of this Tracking.


        :param _date: The _date of this Tracking.  # noqa: E501
        :type: str
        """

        self.__date = _date

    @property
    def fields(self):
        """Gets the fields of this Tracking.  # noqa: E501


        :return: The fields of this Tracking.  # noqa: E501
        :rtype: dict(str, Serializable)
        """
        return self._fields

    @fields.setter
    def fields(self, fields):
        """Sets the fields of this Tracking.


        :param fields: The fields of this Tracking.  # noqa: E501
        :type: dict(str, Serializable)
        """

        self._fields = fields

    @property
    def groups(self):
        """Gets the groups of this Tracking.  # noqa: E501


        :return: The groups of this Tracking.  # noqa: E501
        :rtype: dict(str, dict(str, dict(str, int)))
        """
        return self._groups

    @groups.setter
    def groups(self, groups):
        """Sets the groups of this Tracking.


        :param groups: The groups of this Tracking.  # noqa: E501
        :type: dict(str, dict(str, dict(str, int)))
        """

        self._groups = groups

    @property
    def authority(self):
        """Gets the authority of this Tracking.  # noqa: E501


        :return: The authority of this Tracking.  # noqa: E501
        :rtype: TrackingAuthority
        """
        return self._authority

    @authority.setter
    def authority(self, authority):
        """Sets the authority of this Tracking.


        :param authority: The authority of this Tracking.  # noqa: E501
        :type: TrackingAuthority
        """

        self._authority = authority

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
        if issubclass(Tracking, dict):
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
        if not isinstance(other, Tracking):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
