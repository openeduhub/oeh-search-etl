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

class Application(object):
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
        'title': 'str',
        'webserver_url': 'str',
        'client_base_url': 'str',
        'type': 'str',
        'subtype': 'str',
        'repository_type': 'str',
        'xml': 'str',
        'file': 'str',
        'content_url': 'str',
        'config_url': 'str'
    }

    attribute_map = {
        'id': 'id',
        'title': 'title',
        'webserver_url': 'webserverUrl',
        'client_base_url': 'clientBaseUrl',
        'type': 'type',
        'subtype': 'subtype',
        'repository_type': 'repositoryType',
        'xml': 'xml',
        'file': 'file',
        'content_url': 'contentUrl',
        'config_url': 'configUrl'
    }

    def __init__(self, id=None, title=None, webserver_url=None, client_base_url=None, type=None, subtype=None, repository_type=None, xml=None, file=None, content_url=None, config_url=None):  # noqa: E501
        """Application - a model defined in Swagger"""  # noqa: E501
        self._id = None
        self._title = None
        self._webserver_url = None
        self._client_base_url = None
        self._type = None
        self._subtype = None
        self._repository_type = None
        self._xml = None
        self._file = None
        self._content_url = None
        self._config_url = None
        self.discriminator = None
        if id is not None:
            self.id = id
        if title is not None:
            self.title = title
        if webserver_url is not None:
            self.webserver_url = webserver_url
        if client_base_url is not None:
            self.client_base_url = client_base_url
        if type is not None:
            self.type = type
        if subtype is not None:
            self.subtype = subtype
        if repository_type is not None:
            self.repository_type = repository_type
        if xml is not None:
            self.xml = xml
        if file is not None:
            self.file = file
        if content_url is not None:
            self.content_url = content_url
        if config_url is not None:
            self.config_url = config_url

    @property
    def id(self):
        """Gets the id of this Application.  # noqa: E501


        :return: The id of this Application.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this Application.


        :param id: The id of this Application.  # noqa: E501
        :type: str
        """

        self._id = id

    @property
    def title(self):
        """Gets the title of this Application.  # noqa: E501


        :return: The title of this Application.  # noqa: E501
        :rtype: str
        """
        return self._title

    @title.setter
    def title(self, title):
        """Sets the title of this Application.


        :param title: The title of this Application.  # noqa: E501
        :type: str
        """

        self._title = title

    @property
    def webserver_url(self):
        """Gets the webserver_url of this Application.  # noqa: E501


        :return: The webserver_url of this Application.  # noqa: E501
        :rtype: str
        """
        return self._webserver_url

    @webserver_url.setter
    def webserver_url(self, webserver_url):
        """Sets the webserver_url of this Application.


        :param webserver_url: The webserver_url of this Application.  # noqa: E501
        :type: str
        """

        self._webserver_url = webserver_url

    @property
    def client_base_url(self):
        """Gets the client_base_url of this Application.  # noqa: E501


        :return: The client_base_url of this Application.  # noqa: E501
        :rtype: str
        """
        return self._client_base_url

    @client_base_url.setter
    def client_base_url(self, client_base_url):
        """Sets the client_base_url of this Application.


        :param client_base_url: The client_base_url of this Application.  # noqa: E501
        :type: str
        """

        self._client_base_url = client_base_url

    @property
    def type(self):
        """Gets the type of this Application.  # noqa: E501


        :return: The type of this Application.  # noqa: E501
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """Sets the type of this Application.


        :param type: The type of this Application.  # noqa: E501
        :type: str
        """

        self._type = type

    @property
    def subtype(self):
        """Gets the subtype of this Application.  # noqa: E501


        :return: The subtype of this Application.  # noqa: E501
        :rtype: str
        """
        return self._subtype

    @subtype.setter
    def subtype(self, subtype):
        """Sets the subtype of this Application.


        :param subtype: The subtype of this Application.  # noqa: E501
        :type: str
        """

        self._subtype = subtype

    @property
    def repository_type(self):
        """Gets the repository_type of this Application.  # noqa: E501


        :return: The repository_type of this Application.  # noqa: E501
        :rtype: str
        """
        return self._repository_type

    @repository_type.setter
    def repository_type(self, repository_type):
        """Sets the repository_type of this Application.


        :param repository_type: The repository_type of this Application.  # noqa: E501
        :type: str
        """

        self._repository_type = repository_type

    @property
    def xml(self):
        """Gets the xml of this Application.  # noqa: E501


        :return: The xml of this Application.  # noqa: E501
        :rtype: str
        """
        return self._xml

    @xml.setter
    def xml(self, xml):
        """Sets the xml of this Application.


        :param xml: The xml of this Application.  # noqa: E501
        :type: str
        """

        self._xml = xml

    @property
    def file(self):
        """Gets the file of this Application.  # noqa: E501


        :return: The file of this Application.  # noqa: E501
        :rtype: str
        """
        return self._file

    @file.setter
    def file(self, file):
        """Sets the file of this Application.


        :param file: The file of this Application.  # noqa: E501
        :type: str
        """

        self._file = file

    @property
    def content_url(self):
        """Gets the content_url of this Application.  # noqa: E501


        :return: The content_url of this Application.  # noqa: E501
        :rtype: str
        """
        return self._content_url

    @content_url.setter
    def content_url(self, content_url):
        """Sets the content_url of this Application.


        :param content_url: The content_url of this Application.  # noqa: E501
        :type: str
        """

        self._content_url = content_url

    @property
    def config_url(self):
        """Gets the config_url of this Application.  # noqa: E501


        :return: The config_url of this Application.  # noqa: E501
        :rtype: str
        """
        return self._config_url

    @config_url.setter
    def config_url(self, config_url):
        """Sets the config_url of this Application.


        :param config_url: The config_url of this Application.  # noqa: E501
        :type: str
        """

        self._config_url = config_url

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
        if issubclass(Application, dict):
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
        if not isinstance(other, Application):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other