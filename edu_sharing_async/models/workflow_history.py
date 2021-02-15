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

class WorkflowHistory(object):
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
        'time': 'int',
        'editor': 'UserSimple',
        'receiver': 'list[Authority]',
        'status': 'str',
        'comment': 'str'
    }

    attribute_map = {
        'time': 'time',
        'editor': 'editor',
        'receiver': 'receiver',
        'status': 'status',
        'comment': 'comment'
    }

    def __init__(self, time=None, editor=None, receiver=None, status=None, comment=None):  # noqa: E501
        """WorkflowHistory - a model defined in Swagger"""  # noqa: E501
        self._time = None
        self._editor = None
        self._receiver = None
        self._status = None
        self._comment = None
        self.discriminator = None
        if time is not None:
            self.time = time
        if editor is not None:
            self.editor = editor
        if receiver is not None:
            self.receiver = receiver
        if status is not None:
            self.status = status
        if comment is not None:
            self.comment = comment

    @property
    def time(self):
        """Gets the time of this WorkflowHistory.  # noqa: E501


        :return: The time of this WorkflowHistory.  # noqa: E501
        :rtype: int
        """
        return self._time

    @time.setter
    def time(self, time):
        """Sets the time of this WorkflowHistory.


        :param time: The time of this WorkflowHistory.  # noqa: E501
        :type: int
        """

        self._time = time

    @property
    def editor(self):
        """Gets the editor of this WorkflowHistory.  # noqa: E501


        :return: The editor of this WorkflowHistory.  # noqa: E501
        :rtype: UserSimple
        """
        return self._editor

    @editor.setter
    def editor(self, editor):
        """Sets the editor of this WorkflowHistory.


        :param editor: The editor of this WorkflowHistory.  # noqa: E501
        :type: UserSimple
        """

        self._editor = editor

    @property
    def receiver(self):
        """Gets the receiver of this WorkflowHistory.  # noqa: E501


        :return: The receiver of this WorkflowHistory.  # noqa: E501
        :rtype: list[Authority]
        """
        return self._receiver

    @receiver.setter
    def receiver(self, receiver):
        """Sets the receiver of this WorkflowHistory.


        :param receiver: The receiver of this WorkflowHistory.  # noqa: E501
        :type: list[Authority]
        """

        self._receiver = receiver

    @property
    def status(self):
        """Gets the status of this WorkflowHistory.  # noqa: E501


        :return: The status of this WorkflowHistory.  # noqa: E501
        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, status):
        """Sets the status of this WorkflowHistory.


        :param status: The status of this WorkflowHistory.  # noqa: E501
        :type: str
        """

        self._status = status

    @property
    def comment(self):
        """Gets the comment of this WorkflowHistory.  # noqa: E501


        :return: The comment of this WorkflowHistory.  # noqa: E501
        :rtype: str
        """
        return self._comment

    @comment.setter
    def comment(self, comment):
        """Sets the comment of this WorkflowHistory.


        :param comment: The comment of this WorkflowHistory.  # noqa: E501
        :type: str
        """

        self._comment = comment

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
        if issubclass(WorkflowHistory, dict):
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
        if not isinstance(other, WorkflowHistory):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
