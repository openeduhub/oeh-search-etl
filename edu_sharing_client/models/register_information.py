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


class RegisterInformation(object):
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
        'first_name': 'str',
        'last_name': 'str',
        'email': 'str',
        'password': 'str',
        'organization': 'str',
        'allow_notifications': 'bool',
        'authority_name': 'str'
    }

    attribute_map = {
        'first_name': 'firstName',
        'last_name': 'lastName',
        'email': 'email',
        'password': 'password',
        'organization': 'organization',
        'allow_notifications': 'allowNotifications',
        'authority_name': 'authorityName'
    }

    def __init__(self, first_name=None, last_name=None, email=None, password=None, organization=None, allow_notifications=False, authority_name=None):  # noqa: E501
        """RegisterInformation - a model defined in Swagger"""  # noqa: E501
        self._first_name = None
        self._last_name = None
        self._email = None
        self._password = None
        self._organization = None
        self._allow_notifications = None
        self._authority_name = None
        self.discriminator = None
        if first_name is not None:
            self.first_name = first_name
        if last_name is not None:
            self.last_name = last_name
        if email is not None:
            self.email = email
        if password is not None:
            self.password = password
        if organization is not None:
            self.organization = organization
        if allow_notifications is not None:
            self.allow_notifications = allow_notifications
        if authority_name is not None:
            self.authority_name = authority_name

    @property
    def first_name(self):
        """Gets the first_name of this RegisterInformation.  # noqa: E501


        :return: The first_name of this RegisterInformation.  # noqa: E501
        :rtype: str
        """
        return self._first_name

    @first_name.setter
    def first_name(self, first_name):
        """Sets the first_name of this RegisterInformation.


        :param first_name: The first_name of this RegisterInformation.  # noqa: E501
        :type: str
        """

        self._first_name = first_name

    @property
    def last_name(self):
        """Gets the last_name of this RegisterInformation.  # noqa: E501


        :return: The last_name of this RegisterInformation.  # noqa: E501
        :rtype: str
        """
        return self._last_name

    @last_name.setter
    def last_name(self, last_name):
        """Sets the last_name of this RegisterInformation.


        :param last_name: The last_name of this RegisterInformation.  # noqa: E501
        :type: str
        """

        self._last_name = last_name

    @property
    def email(self):
        """Gets the email of this RegisterInformation.  # noqa: E501


        :return: The email of this RegisterInformation.  # noqa: E501
        :rtype: str
        """
        return self._email

    @email.setter
    def email(self, email):
        """Sets the email of this RegisterInformation.


        :param email: The email of this RegisterInformation.  # noqa: E501
        :type: str
        """

        self._email = email

    @property
    def password(self):
        """Gets the password of this RegisterInformation.  # noqa: E501


        :return: The password of this RegisterInformation.  # noqa: E501
        :rtype: str
        """
        return self._password

    @password.setter
    def password(self, password):
        """Sets the password of this RegisterInformation.


        :param password: The password of this RegisterInformation.  # noqa: E501
        :type: str
        """

        self._password = password

    @property
    def organization(self):
        """Gets the organization of this RegisterInformation.  # noqa: E501


        :return: The organization of this RegisterInformation.  # noqa: E501
        :rtype: str
        """
        return self._organization

    @organization.setter
    def organization(self, organization):
        """Sets the organization of this RegisterInformation.


        :param organization: The organization of this RegisterInformation.  # noqa: E501
        :type: str
        """

        self._organization = organization

    @property
    def allow_notifications(self):
        """Gets the allow_notifications of this RegisterInformation.  # noqa: E501


        :return: The allow_notifications of this RegisterInformation.  # noqa: E501
        :rtype: bool
        """
        return self._allow_notifications

    @allow_notifications.setter
    def allow_notifications(self, allow_notifications):
        """Sets the allow_notifications of this RegisterInformation.


        :param allow_notifications: The allow_notifications of this RegisterInformation.  # noqa: E501
        :type: bool
        """

        self._allow_notifications = allow_notifications

    @property
    def authority_name(self):
        """Gets the authority_name of this RegisterInformation.  # noqa: E501


        :return: The authority_name of this RegisterInformation.  # noqa: E501
        :rtype: str
        """
        return self._authority_name

    @authority_name.setter
    def authority_name(self, authority_name):
        """Sets the authority_name of this RegisterInformation.


        :param authority_name: The authority_name of this RegisterInformation.  # noqa: E501
        :type: str
        """

        self._authority_name = authority_name

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
        if issubclass(RegisterInformation, dict):
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
        if not isinstance(other, RegisterInformation):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
