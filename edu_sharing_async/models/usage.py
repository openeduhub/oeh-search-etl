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

class Usage(object):
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
        'from_used': 'datetime',
        'to_used': 'datetime',
        'usage_counter': 'int',
        'app_subtype': 'str',
        'app_type': 'str',
        'type': 'str',
        'created': 'datetime',
        'modified': 'datetime',
        'app_user': 'str',
        'app_user_mail': 'str',
        'course_id': 'str',
        'distinct_persons': 'int',
        'app_id': 'str',
        'node_id': 'str',
        'parent_node_id': 'str',
        'usage_version': 'str',
        'usage_xml_params': 'Parameters',
        'usage_xml_params_raw': 'str',
        'resource_id': 'str',
        'guid': 'str'
    }

    attribute_map = {
        'from_used': 'fromUsed',
        'to_used': 'toUsed',
        'usage_counter': 'usageCounter',
        'app_subtype': 'appSubtype',
        'app_type': 'appType',
        'type': 'type',
        'created': 'created',
        'modified': 'modified',
        'app_user': 'appUser',
        'app_user_mail': 'appUserMail',
        'course_id': 'courseId',
        'distinct_persons': 'distinctPersons',
        'app_id': 'appId',
        'node_id': 'nodeId',
        'parent_node_id': 'parentNodeId',
        'usage_version': 'usageVersion',
        'usage_xml_params': 'usageXmlParams',
        'usage_xml_params_raw': 'usageXmlParamsRaw',
        'resource_id': 'resourceId',
        'guid': 'guid'
    }

    def __init__(self, from_used=None, to_used=None, usage_counter=None, app_subtype=None, app_type=None, type=None, created=None, modified=None, app_user=None, app_user_mail=None, course_id=None, distinct_persons=None, app_id=None, node_id=None, parent_node_id=None, usage_version=None, usage_xml_params=None, usage_xml_params_raw=None, resource_id=None, guid=None):  # noqa: E501
        """Usage - a model defined in Swagger"""  # noqa: E501
        self._from_used = None
        self._to_used = None
        self._usage_counter = None
        self._app_subtype = None
        self._app_type = None
        self._type = None
        self._created = None
        self._modified = None
        self._app_user = None
        self._app_user_mail = None
        self._course_id = None
        self._distinct_persons = None
        self._app_id = None
        self._node_id = None
        self._parent_node_id = None
        self._usage_version = None
        self._usage_xml_params = None
        self._usage_xml_params_raw = None
        self._resource_id = None
        self._guid = None
        self.discriminator = None
        if from_used is not None:
            self.from_used = from_used
        if to_used is not None:
            self.to_used = to_used
        if usage_counter is not None:
            self.usage_counter = usage_counter
        if app_subtype is not None:
            self.app_subtype = app_subtype
        if app_type is not None:
            self.app_type = app_type
        if type is not None:
            self.type = type
        if created is not None:
            self.created = created
        if modified is not None:
            self.modified = modified
        self.app_user = app_user
        self.app_user_mail = app_user_mail
        self.course_id = course_id
        if distinct_persons is not None:
            self.distinct_persons = distinct_persons
        self.app_id = app_id
        self.node_id = node_id
        self.parent_node_id = parent_node_id
        self.usage_version = usage_version
        if usage_xml_params is not None:
            self.usage_xml_params = usage_xml_params
        if usage_xml_params_raw is not None:
            self.usage_xml_params_raw = usage_xml_params_raw
        self.resource_id = resource_id
        if guid is not None:
            self.guid = guid

    @property
    def from_used(self):
        """Gets the from_used of this Usage.  # noqa: E501


        :return: The from_used of this Usage.  # noqa: E501
        :rtype: datetime
        """
        return self._from_used

    @from_used.setter
    def from_used(self, from_used):
        """Sets the from_used of this Usage.


        :param from_used: The from_used of this Usage.  # noqa: E501
        :type: datetime
        """

        self._from_used = from_used

    @property
    def to_used(self):
        """Gets the to_used of this Usage.  # noqa: E501


        :return: The to_used of this Usage.  # noqa: E501
        :rtype: datetime
        """
        return self._to_used

    @to_used.setter
    def to_used(self, to_used):
        """Sets the to_used of this Usage.


        :param to_used: The to_used of this Usage.  # noqa: E501
        :type: datetime
        """

        self._to_used = to_used

    @property
    def usage_counter(self):
        """Gets the usage_counter of this Usage.  # noqa: E501


        :return: The usage_counter of this Usage.  # noqa: E501
        :rtype: int
        """
        return self._usage_counter

    @usage_counter.setter
    def usage_counter(self, usage_counter):
        """Sets the usage_counter of this Usage.


        :param usage_counter: The usage_counter of this Usage.  # noqa: E501
        :type: int
        """

        self._usage_counter = usage_counter

    @property
    def app_subtype(self):
        """Gets the app_subtype of this Usage.  # noqa: E501


        :return: The app_subtype of this Usage.  # noqa: E501
        :rtype: str
        """
        return self._app_subtype

    @app_subtype.setter
    def app_subtype(self, app_subtype):
        """Sets the app_subtype of this Usage.


        :param app_subtype: The app_subtype of this Usage.  # noqa: E501
        :type: str
        """

        self._app_subtype = app_subtype

    @property
    def app_type(self):
        """Gets the app_type of this Usage.  # noqa: E501


        :return: The app_type of this Usage.  # noqa: E501
        :rtype: str
        """
        return self._app_type

    @app_type.setter
    def app_type(self, app_type):
        """Sets the app_type of this Usage.


        :param app_type: The app_type of this Usage.  # noqa: E501
        :type: str
        """

        self._app_type = app_type

    @property
    def type(self):
        """Gets the type of this Usage.  # noqa: E501


        :return: The type of this Usage.  # noqa: E501
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """Sets the type of this Usage.


        :param type: The type of this Usage.  # noqa: E501
        :type: str
        """

        self._type = type

    @property
    def created(self):
        """Gets the created of this Usage.  # noqa: E501


        :return: The created of this Usage.  # noqa: E501
        :rtype: datetime
        """
        return self._created

    @created.setter
    def created(self, created):
        """Sets the created of this Usage.


        :param created: The created of this Usage.  # noqa: E501
        :type: datetime
        """

        self._created = created

    @property
    def modified(self):
        """Gets the modified of this Usage.  # noqa: E501


        :return: The modified of this Usage.  # noqa: E501
        :rtype: datetime
        """
        return self._modified

    @modified.setter
    def modified(self, modified):
        """Sets the modified of this Usage.


        :param modified: The modified of this Usage.  # noqa: E501
        :type: datetime
        """

        self._modified = modified

    @property
    def app_user(self):
        """Gets the app_user of this Usage.  # noqa: E501


        :return: The app_user of this Usage.  # noqa: E501
        :rtype: str
        """
        return self._app_user

    @app_user.setter
    def app_user(self, app_user):
        """Sets the app_user of this Usage.


        :param app_user: The app_user of this Usage.  # noqa: E501
        :type: str
        """
        if app_user is None:
            raise ValueError("Invalid value for `app_user`, must not be `None`")  # noqa: E501

        self._app_user = app_user

    @property
    def app_user_mail(self):
        """Gets the app_user_mail of this Usage.  # noqa: E501


        :return: The app_user_mail of this Usage.  # noqa: E501
        :rtype: str
        """
        return self._app_user_mail

    @app_user_mail.setter
    def app_user_mail(self, app_user_mail):
        """Sets the app_user_mail of this Usage.


        :param app_user_mail: The app_user_mail of this Usage.  # noqa: E501
        :type: str
        """
        if app_user_mail is None:
            raise ValueError("Invalid value for `app_user_mail`, must not be `None`")  # noqa: E501

        self._app_user_mail = app_user_mail

    @property
    def course_id(self):
        """Gets the course_id of this Usage.  # noqa: E501


        :return: The course_id of this Usage.  # noqa: E501
        :rtype: str
        """
        return self._course_id

    @course_id.setter
    def course_id(self, course_id):
        """Sets the course_id of this Usage.


        :param course_id: The course_id of this Usage.  # noqa: E501
        :type: str
        """
        if course_id is None:
            raise ValueError("Invalid value for `course_id`, must not be `None`")  # noqa: E501

        self._course_id = course_id

    @property
    def distinct_persons(self):
        """Gets the distinct_persons of this Usage.  # noqa: E501


        :return: The distinct_persons of this Usage.  # noqa: E501
        :rtype: int
        """
        return self._distinct_persons

    @distinct_persons.setter
    def distinct_persons(self, distinct_persons):
        """Sets the distinct_persons of this Usage.


        :param distinct_persons: The distinct_persons of this Usage.  # noqa: E501
        :type: int
        """

        self._distinct_persons = distinct_persons

    @property
    def app_id(self):
        """Gets the app_id of this Usage.  # noqa: E501


        :return: The app_id of this Usage.  # noqa: E501
        :rtype: str
        """
        return self._app_id

    @app_id.setter
    def app_id(self, app_id):
        """Sets the app_id of this Usage.


        :param app_id: The app_id of this Usage.  # noqa: E501
        :type: str
        """
        if app_id is None:
            raise ValueError("Invalid value for `app_id`, must not be `None`")  # noqa: E501

        self._app_id = app_id

    @property
    def node_id(self):
        """Gets the node_id of this Usage.  # noqa: E501


        :return: The node_id of this Usage.  # noqa: E501
        :rtype: str
        """
        return self._node_id

    @node_id.setter
    def node_id(self, node_id):
        """Sets the node_id of this Usage.


        :param node_id: The node_id of this Usage.  # noqa: E501
        :type: str
        """
        if node_id is None:
            raise ValueError("Invalid value for `node_id`, must not be `None`")  # noqa: E501

        self._node_id = node_id

    @property
    def parent_node_id(self):
        """Gets the parent_node_id of this Usage.  # noqa: E501


        :return: The parent_node_id of this Usage.  # noqa: E501
        :rtype: str
        """
        return self._parent_node_id

    @parent_node_id.setter
    def parent_node_id(self, parent_node_id):
        """Sets the parent_node_id of this Usage.


        :param parent_node_id: The parent_node_id of this Usage.  # noqa: E501
        :type: str
        """
        if parent_node_id is None:
            raise ValueError("Invalid value for `parent_node_id`, must not be `None`")  # noqa: E501

        self._parent_node_id = parent_node_id

    @property
    def usage_version(self):
        """Gets the usage_version of this Usage.  # noqa: E501


        :return: The usage_version of this Usage.  # noqa: E501
        :rtype: str
        """
        return self._usage_version

    @usage_version.setter
    def usage_version(self, usage_version):
        """Sets the usage_version of this Usage.


        :param usage_version: The usage_version of this Usage.  # noqa: E501
        :type: str
        """
        if usage_version is None:
            raise ValueError("Invalid value for `usage_version`, must not be `None`")  # noqa: E501

        self._usage_version = usage_version

    @property
    def usage_xml_params(self):
        """Gets the usage_xml_params of this Usage.  # noqa: E501


        :return: The usage_xml_params of this Usage.  # noqa: E501
        :rtype: Parameters
        """
        return self._usage_xml_params

    @usage_xml_params.setter
    def usage_xml_params(self, usage_xml_params):
        """Sets the usage_xml_params of this Usage.


        :param usage_xml_params: The usage_xml_params of this Usage.  # noqa: E501
        :type: Parameters
        """

        self._usage_xml_params = usage_xml_params

    @property
    def usage_xml_params_raw(self):
        """Gets the usage_xml_params_raw of this Usage.  # noqa: E501


        :return: The usage_xml_params_raw of this Usage.  # noqa: E501
        :rtype: str
        """
        return self._usage_xml_params_raw

    @usage_xml_params_raw.setter
    def usage_xml_params_raw(self, usage_xml_params_raw):
        """Sets the usage_xml_params_raw of this Usage.


        :param usage_xml_params_raw: The usage_xml_params_raw of this Usage.  # noqa: E501
        :type: str
        """

        self._usage_xml_params_raw = usage_xml_params_raw

    @property
    def resource_id(self):
        """Gets the resource_id of this Usage.  # noqa: E501


        :return: The resource_id of this Usage.  # noqa: E501
        :rtype: str
        """
        return self._resource_id

    @resource_id.setter
    def resource_id(self, resource_id):
        """Sets the resource_id of this Usage.


        :param resource_id: The resource_id of this Usage.  # noqa: E501
        :type: str
        """
        if resource_id is None:
            raise ValueError("Invalid value for `resource_id`, must not be `None`")  # noqa: E501

        self._resource_id = resource_id

    @property
    def guid(self):
        """Gets the guid of this Usage.  # noqa: E501


        :return: The guid of this Usage.  # noqa: E501
        :rtype: str
        """
        return self._guid

    @guid.setter
    def guid(self, guid):
        """Sets the guid of this Usage.


        :param guid: The guid of this Usage.  # noqa: E501
        :type: str
        """

        self._guid = guid

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
        if issubclass(Usage, dict):
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
        if not isinstance(other, Usage):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
