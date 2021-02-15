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

class TrackingAuthority(object):
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
        'hash': 'str',
        'organization': 'list[Organization]',
        'mediacenter': 'list[Group]'
    }

    attribute_map = {
        'hash': 'hash',
        'organization': 'organization',
        'mediacenter': 'mediacenter'
    }

    def __init__(self, hash=None, organization=None, mediacenter=None):  # noqa: E501
        """TrackingAuthority - a model defined in Swagger"""  # noqa: E501
        self._hash = None
        self._organization = None
        self._mediacenter = None
        self.discriminator = None
        if hash is not None:
            self.hash = hash
        if organization is not None:
            self.organization = organization
        if mediacenter is not None:
            self.mediacenter = mediacenter

    @property
    def hash(self):
        """Gets the hash of this TrackingAuthority.  # noqa: E501


        :return: The hash of this TrackingAuthority.  # noqa: E501
        :rtype: str
        """
        return self._hash

    @hash.setter
    def hash(self, hash):
        """Sets the hash of this TrackingAuthority.


        :param hash: The hash of this TrackingAuthority.  # noqa: E501
        :type: str
        """

        self._hash = hash

    @property
    def organization(self):
        """Gets the organization of this TrackingAuthority.  # noqa: E501


        :return: The organization of this TrackingAuthority.  # noqa: E501
        :rtype: list[Organization]
        """
        return self._organization

    @organization.setter
    def organization(self, organization):
        """Sets the organization of this TrackingAuthority.


        :param organization: The organization of this TrackingAuthority.  # noqa: E501
        :type: list[Organization]
        """

        self._organization = organization

    @property
    def mediacenter(self):
        """Gets the mediacenter of this TrackingAuthority.  # noqa: E501


        :return: The mediacenter of this TrackingAuthority.  # noqa: E501
        :rtype: list[Group]
        """
        return self._mediacenter

    @mediacenter.setter
    def mediacenter(self, mediacenter):
        """Sets the mediacenter of this TrackingAuthority.


        :param mediacenter: The mediacenter of this TrackingAuthority.  # noqa: E501
        :type: list[Group]
        """

        self._mediacenter = mediacenter

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
        if issubclass(TrackingAuthority, dict):
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
        if not isinstance(other, TrackingAuthority):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other