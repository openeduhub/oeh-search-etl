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

class Repo(object):
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
        'repository_type': 'str',
        'rendering_supported': 'bool',
        'id': 'str',
        'title': 'str',
        'icon': 'str',
        'logo': 'str',
        'is_home_repo': 'bool'
    }

    attribute_map = {
        'repository_type': 'repositoryType',
        'rendering_supported': 'renderingSupported',
        'id': 'id',
        'title': 'title',
        'icon': 'icon',
        'logo': 'logo',
        'is_home_repo': 'isHomeRepo'
    }

    def __init__(self, repository_type=None, rendering_supported=False, id=None, title=None, icon=None, logo=None, is_home_repo=False):  # noqa: E501
        """Repo - a model defined in Swagger"""  # noqa: E501
        self._repository_type = None
        self._rendering_supported = None
        self._id = None
        self._title = None
        self._icon = None
        self._logo = None
        self._is_home_repo = None
        self.discriminator = None
        if repository_type is not None:
            self.repository_type = repository_type
        if rendering_supported is not None:
            self.rendering_supported = rendering_supported
        if id is not None:
            self.id = id
        if title is not None:
            self.title = title
        if icon is not None:
            self.icon = icon
        if logo is not None:
            self.logo = logo
        if is_home_repo is not None:
            self.is_home_repo = is_home_repo

    @property
    def repository_type(self):
        """Gets the repository_type of this Repo.  # noqa: E501


        :return: The repository_type of this Repo.  # noqa: E501
        :rtype: str
        """
        return self._repository_type

    @repository_type.setter
    def repository_type(self, repository_type):
        """Sets the repository_type of this Repo.


        :param repository_type: The repository_type of this Repo.  # noqa: E501
        :type: str
        """

        self._repository_type = repository_type

    @property
    def rendering_supported(self):
        """Gets the rendering_supported of this Repo.  # noqa: E501


        :return: The rendering_supported of this Repo.  # noqa: E501
        :rtype: bool
        """
        return self._rendering_supported

    @rendering_supported.setter
    def rendering_supported(self, rendering_supported):
        """Sets the rendering_supported of this Repo.


        :param rendering_supported: The rendering_supported of this Repo.  # noqa: E501
        :type: bool
        """

        self._rendering_supported = rendering_supported

    @property
    def id(self):
        """Gets the id of this Repo.  # noqa: E501


        :return: The id of this Repo.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this Repo.


        :param id: The id of this Repo.  # noqa: E501
        :type: str
        """

        self._id = id

    @property
    def title(self):
        """Gets the title of this Repo.  # noqa: E501


        :return: The title of this Repo.  # noqa: E501
        :rtype: str
        """
        return self._title

    @title.setter
    def title(self, title):
        """Sets the title of this Repo.


        :param title: The title of this Repo.  # noqa: E501
        :type: str
        """

        self._title = title

    @property
    def icon(self):
        """Gets the icon of this Repo.  # noqa: E501


        :return: The icon of this Repo.  # noqa: E501
        :rtype: str
        """
        return self._icon

    @icon.setter
    def icon(self, icon):
        """Sets the icon of this Repo.


        :param icon: The icon of this Repo.  # noqa: E501
        :type: str
        """

        self._icon = icon

    @property
    def logo(self):
        """Gets the logo of this Repo.  # noqa: E501


        :return: The logo of this Repo.  # noqa: E501
        :rtype: str
        """
        return self._logo

    @logo.setter
    def logo(self, logo):
        """Sets the logo of this Repo.


        :param logo: The logo of this Repo.  # noqa: E501
        :type: str
        """

        self._logo = logo

    @property
    def is_home_repo(self):
        """Gets the is_home_repo of this Repo.  # noqa: E501


        :return: The is_home_repo of this Repo.  # noqa: E501
        :rtype: bool
        """
        return self._is_home_repo

    @is_home_repo.setter
    def is_home_repo(self, is_home_repo):
        """Sets the is_home_repo of this Repo.


        :param is_home_repo: The is_home_repo of this Repo.  # noqa: E501
        :type: bool
        """

        self._is_home_repo = is_home_repo

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
        if issubclass(Repo, dict):
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
        if not isinstance(other, Repo):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other