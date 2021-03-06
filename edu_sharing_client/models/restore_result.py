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


class RestoreResult(object):
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
        'archive_node_id': 'str',
        'node_id': 'str',
        'parent': 'str',
        'path': 'str',
        'name': 'str',
        'restore_status': 'str'
    }

    attribute_map = {
        'archive_node_id': 'archiveNodeId',
        'node_id': 'nodeId',
        'parent': 'parent',
        'path': 'path',
        'name': 'name',
        'restore_status': 'restoreStatus'
    }

    def __init__(self, archive_node_id=None, node_id=None, parent=None, path=None, name=None, restore_status=None):  # noqa: E501
        """RestoreResult - a model defined in Swagger"""  # noqa: E501
        self._archive_node_id = None
        self._node_id = None
        self._parent = None
        self._path = None
        self._name = None
        self._restore_status = None
        self.discriminator = None
        self.archive_node_id = archive_node_id
        self.node_id = node_id
        self.parent = parent
        self.path = path
        self.name = name
        self.restore_status = restore_status

    @property
    def archive_node_id(self):
        """Gets the archive_node_id of this RestoreResult.  # noqa: E501


        :return: The archive_node_id of this RestoreResult.  # noqa: E501
        :rtype: str
        """
        return self._archive_node_id

    @archive_node_id.setter
    def archive_node_id(self, archive_node_id):
        """Sets the archive_node_id of this RestoreResult.


        :param archive_node_id: The archive_node_id of this RestoreResult.  # noqa: E501
        :type: str
        """
        if archive_node_id is None:
            raise ValueError("Invalid value for `archive_node_id`, must not be `None`")  # noqa: E501

        self._archive_node_id = archive_node_id

    @property
    def node_id(self):
        """Gets the node_id of this RestoreResult.  # noqa: E501


        :return: The node_id of this RestoreResult.  # noqa: E501
        :rtype: str
        """
        return self._node_id

    @node_id.setter
    def node_id(self, node_id):
        """Sets the node_id of this RestoreResult.


        :param node_id: The node_id of this RestoreResult.  # noqa: E501
        :type: str
        """
        if node_id is None:
            raise ValueError("Invalid value for `node_id`, must not be `None`")  # noqa: E501

        self._node_id = node_id

    @property
    def parent(self):
        """Gets the parent of this RestoreResult.  # noqa: E501


        :return: The parent of this RestoreResult.  # noqa: E501
        :rtype: str
        """
        return self._parent

    @parent.setter
    def parent(self, parent):
        """Sets the parent of this RestoreResult.


        :param parent: The parent of this RestoreResult.  # noqa: E501
        :type: str
        """
        if parent is None:
            raise ValueError("Invalid value for `parent`, must not be `None`")  # noqa: E501

        self._parent = parent

    @property
    def path(self):
        """Gets the path of this RestoreResult.  # noqa: E501


        :return: The path of this RestoreResult.  # noqa: E501
        :rtype: str
        """
        return self._path

    @path.setter
    def path(self, path):
        """Sets the path of this RestoreResult.


        :param path: The path of this RestoreResult.  # noqa: E501
        :type: str
        """
        if path is None:
            raise ValueError("Invalid value for `path`, must not be `None`")  # noqa: E501

        self._path = path

    @property
    def name(self):
        """Gets the name of this RestoreResult.  # noqa: E501


        :return: The name of this RestoreResult.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this RestoreResult.


        :param name: The name of this RestoreResult.  # noqa: E501
        :type: str
        """
        if name is None:
            raise ValueError("Invalid value for `name`, must not be `None`")  # noqa: E501

        self._name = name

    @property
    def restore_status(self):
        """Gets the restore_status of this RestoreResult.  # noqa: E501


        :return: The restore_status of this RestoreResult.  # noqa: E501
        :rtype: str
        """
        return self._restore_status

    @restore_status.setter
    def restore_status(self, restore_status):
        """Sets the restore_status of this RestoreResult.


        :param restore_status: The restore_status of this RestoreResult.  # noqa: E501
        :type: str
        """
        if restore_status is None:
            raise ValueError("Invalid value for `restore_status`, must not be `None`")  # noqa: E501

        self._restore_status = restore_status

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
        if issubclass(RestoreResult, dict):
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
        if not isinstance(other, RestoreResult):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
