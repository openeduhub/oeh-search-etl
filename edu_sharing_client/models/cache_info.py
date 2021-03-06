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


class CacheInfo(object):
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
        'size': 'int',
        'statistic_hits': 'int',
        'name': 'str',
        'backup_count': 'int',
        'backup_entry_count': 'int',
        'backup_entry_memory_cost': 'int',
        'heap_cost': 'int',
        'owned_entry_count': 'int',
        'get_owned_entry_memory_cost': 'int',
        'size_in_memory': 'int',
        'member': 'str',
        'group_name': 'str',
        'max_size': 'int'
    }

    attribute_map = {
        'size': 'size',
        'statistic_hits': 'statisticHits',
        'name': 'name',
        'backup_count': 'backupCount',
        'backup_entry_count': 'backupEntryCount',
        'backup_entry_memory_cost': 'backupEntryMemoryCost',
        'heap_cost': 'heapCost',
        'owned_entry_count': 'ownedEntryCount',
        'get_owned_entry_memory_cost': 'getOwnedEntryMemoryCost',
        'size_in_memory': 'sizeInMemory',
        'member': 'member',
        'group_name': 'groupName',
        'max_size': 'maxSize'
    }

    def __init__(self, size=None, statistic_hits=None, name=None, backup_count=None, backup_entry_count=None, backup_entry_memory_cost=None, heap_cost=None, owned_entry_count=None, get_owned_entry_memory_cost=None, size_in_memory=None, member=None, group_name=None, max_size=None):  # noqa: E501
        """CacheInfo - a model defined in Swagger"""  # noqa: E501
        self._size = None
        self._statistic_hits = None
        self._name = None
        self._backup_count = None
        self._backup_entry_count = None
        self._backup_entry_memory_cost = None
        self._heap_cost = None
        self._owned_entry_count = None
        self._get_owned_entry_memory_cost = None
        self._size_in_memory = None
        self._member = None
        self._group_name = None
        self._max_size = None
        self.discriminator = None
        if size is not None:
            self.size = size
        if statistic_hits is not None:
            self.statistic_hits = statistic_hits
        if name is not None:
            self.name = name
        if backup_count is not None:
            self.backup_count = backup_count
        if backup_entry_count is not None:
            self.backup_entry_count = backup_entry_count
        if backup_entry_memory_cost is not None:
            self.backup_entry_memory_cost = backup_entry_memory_cost
        if heap_cost is not None:
            self.heap_cost = heap_cost
        if owned_entry_count is not None:
            self.owned_entry_count = owned_entry_count
        if get_owned_entry_memory_cost is not None:
            self.get_owned_entry_memory_cost = get_owned_entry_memory_cost
        if size_in_memory is not None:
            self.size_in_memory = size_in_memory
        if member is not None:
            self.member = member
        if group_name is not None:
            self.group_name = group_name
        if max_size is not None:
            self.max_size = max_size

    @property
    def size(self):
        """Gets the size of this CacheInfo.  # noqa: E501


        :return: The size of this CacheInfo.  # noqa: E501
        :rtype: int
        """
        return self._size

    @size.setter
    def size(self, size):
        """Sets the size of this CacheInfo.


        :param size: The size of this CacheInfo.  # noqa: E501
        :type: int
        """

        self._size = size

    @property
    def statistic_hits(self):
        """Gets the statistic_hits of this CacheInfo.  # noqa: E501


        :return: The statistic_hits of this CacheInfo.  # noqa: E501
        :rtype: int
        """
        return self._statistic_hits

    @statistic_hits.setter
    def statistic_hits(self, statistic_hits):
        """Sets the statistic_hits of this CacheInfo.


        :param statistic_hits: The statistic_hits of this CacheInfo.  # noqa: E501
        :type: int
        """

        self._statistic_hits = statistic_hits

    @property
    def name(self):
        """Gets the name of this CacheInfo.  # noqa: E501


        :return: The name of this CacheInfo.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this CacheInfo.


        :param name: The name of this CacheInfo.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def backup_count(self):
        """Gets the backup_count of this CacheInfo.  # noqa: E501


        :return: The backup_count of this CacheInfo.  # noqa: E501
        :rtype: int
        """
        return self._backup_count

    @backup_count.setter
    def backup_count(self, backup_count):
        """Sets the backup_count of this CacheInfo.


        :param backup_count: The backup_count of this CacheInfo.  # noqa: E501
        :type: int
        """

        self._backup_count = backup_count

    @property
    def backup_entry_count(self):
        """Gets the backup_entry_count of this CacheInfo.  # noqa: E501


        :return: The backup_entry_count of this CacheInfo.  # noqa: E501
        :rtype: int
        """
        return self._backup_entry_count

    @backup_entry_count.setter
    def backup_entry_count(self, backup_entry_count):
        """Sets the backup_entry_count of this CacheInfo.


        :param backup_entry_count: The backup_entry_count of this CacheInfo.  # noqa: E501
        :type: int
        """

        self._backup_entry_count = backup_entry_count

    @property
    def backup_entry_memory_cost(self):
        """Gets the backup_entry_memory_cost of this CacheInfo.  # noqa: E501


        :return: The backup_entry_memory_cost of this CacheInfo.  # noqa: E501
        :rtype: int
        """
        return self._backup_entry_memory_cost

    @backup_entry_memory_cost.setter
    def backup_entry_memory_cost(self, backup_entry_memory_cost):
        """Sets the backup_entry_memory_cost of this CacheInfo.


        :param backup_entry_memory_cost: The backup_entry_memory_cost of this CacheInfo.  # noqa: E501
        :type: int
        """

        self._backup_entry_memory_cost = backup_entry_memory_cost

    @property
    def heap_cost(self):
        """Gets the heap_cost of this CacheInfo.  # noqa: E501


        :return: The heap_cost of this CacheInfo.  # noqa: E501
        :rtype: int
        """
        return self._heap_cost

    @heap_cost.setter
    def heap_cost(self, heap_cost):
        """Sets the heap_cost of this CacheInfo.


        :param heap_cost: The heap_cost of this CacheInfo.  # noqa: E501
        :type: int
        """

        self._heap_cost = heap_cost

    @property
    def owned_entry_count(self):
        """Gets the owned_entry_count of this CacheInfo.  # noqa: E501


        :return: The owned_entry_count of this CacheInfo.  # noqa: E501
        :rtype: int
        """
        return self._owned_entry_count

    @owned_entry_count.setter
    def owned_entry_count(self, owned_entry_count):
        """Sets the owned_entry_count of this CacheInfo.


        :param owned_entry_count: The owned_entry_count of this CacheInfo.  # noqa: E501
        :type: int
        """

        self._owned_entry_count = owned_entry_count

    @property
    def get_owned_entry_memory_cost(self):
        """Gets the get_owned_entry_memory_cost of this CacheInfo.  # noqa: E501


        :return: The get_owned_entry_memory_cost of this CacheInfo.  # noqa: E501
        :rtype: int
        """
        return self._get_owned_entry_memory_cost

    @get_owned_entry_memory_cost.setter
    def get_owned_entry_memory_cost(self, get_owned_entry_memory_cost):
        """Sets the get_owned_entry_memory_cost of this CacheInfo.


        :param get_owned_entry_memory_cost: The get_owned_entry_memory_cost of this CacheInfo.  # noqa: E501
        :type: int
        """

        self._get_owned_entry_memory_cost = get_owned_entry_memory_cost

    @property
    def size_in_memory(self):
        """Gets the size_in_memory of this CacheInfo.  # noqa: E501


        :return: The size_in_memory of this CacheInfo.  # noqa: E501
        :rtype: int
        """
        return self._size_in_memory

    @size_in_memory.setter
    def size_in_memory(self, size_in_memory):
        """Sets the size_in_memory of this CacheInfo.


        :param size_in_memory: The size_in_memory of this CacheInfo.  # noqa: E501
        :type: int
        """

        self._size_in_memory = size_in_memory

    @property
    def member(self):
        """Gets the member of this CacheInfo.  # noqa: E501


        :return: The member of this CacheInfo.  # noqa: E501
        :rtype: str
        """
        return self._member

    @member.setter
    def member(self, member):
        """Sets the member of this CacheInfo.


        :param member: The member of this CacheInfo.  # noqa: E501
        :type: str
        """

        self._member = member

    @property
    def group_name(self):
        """Gets the group_name of this CacheInfo.  # noqa: E501


        :return: The group_name of this CacheInfo.  # noqa: E501
        :rtype: str
        """
        return self._group_name

    @group_name.setter
    def group_name(self, group_name):
        """Sets the group_name of this CacheInfo.


        :param group_name: The group_name of this CacheInfo.  # noqa: E501
        :type: str
        """

        self._group_name = group_name

    @property
    def max_size(self):
        """Gets the max_size of this CacheInfo.  # noqa: E501


        :return: The max_size of this CacheInfo.  # noqa: E501
        :rtype: int
        """
        return self._max_size

    @max_size.setter
    def max_size(self, max_size):
        """Sets the max_size of this CacheInfo.


        :param max_size: The max_size of this CacheInfo.  # noqa: E501
        :type: int
        """

        self._max_size = max_size

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
        if issubclass(CacheInfo, dict):
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
        if not isinstance(other, CacheInfo):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
