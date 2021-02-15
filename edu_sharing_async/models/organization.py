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

class Organization(object):
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
        'properties': 'dict(str, list[str])',
        'signup_method': 'str',
        'ref': 'NodeRef',
        'editable': 'bool',
        'aspects': 'list[str]',
        'organizations': 'list[Organization]',
        'authority_name': 'str',
        'authority_type': 'str',
        'group_name': 'str',
        'profile': 'GroupProfile',
        'administration_access': 'bool',
        'shared_folder': 'NodeRef'
    }

    attribute_map = {
        'properties': 'properties',
        'signup_method': 'signupMethod',
        'ref': 'ref',
        'editable': 'editable',
        'aspects': 'aspects',
        'organizations': 'organizations',
        'authority_name': 'authorityName',
        'authority_type': 'authorityType',
        'group_name': 'groupName',
        'profile': 'profile',
        'administration_access': 'administrationAccess',
        'shared_folder': 'sharedFolder'
    }

    def __init__(self, properties=None, signup_method=None, ref=None, editable=False, aspects=None, organizations=None, authority_name=None, authority_type=None, group_name=None, profile=None, administration_access=False, shared_folder=None):  # noqa: E501
        """Organization - a model defined in Swagger"""  # noqa: E501
        self._properties = None
        self._signup_method = None
        self._ref = None
        self._editable = None
        self._aspects = None
        self._organizations = None
        self._authority_name = None
        self._authority_type = None
        self._group_name = None
        self._profile = None
        self._administration_access = None
        self._shared_folder = None
        self.discriminator = None
        if properties is not None:
            self.properties = properties
        if signup_method is not None:
            self.signup_method = signup_method
        if ref is not None:
            self.ref = ref
        if editable is not None:
            self.editable = editable
        if aspects is not None:
            self.aspects = aspects
        if organizations is not None:
            self.organizations = organizations
        self.authority_name = authority_name
        if authority_type is not None:
            self.authority_type = authority_type
        if group_name is not None:
            self.group_name = group_name
        if profile is not None:
            self.profile = profile
        if administration_access is not None:
            self.administration_access = administration_access
        if shared_folder is not None:
            self.shared_folder = shared_folder

    @property
    def properties(self):
        """Gets the properties of this Organization.  # noqa: E501


        :return: The properties of this Organization.  # noqa: E501
        :rtype: dict(str, list[str])
        """
        return self._properties

    @properties.setter
    def properties(self, properties):
        """Sets the properties of this Organization.


        :param properties: The properties of this Organization.  # noqa: E501
        :type: dict(str, list[str])
        """

        self._properties = properties

    @property
    def signup_method(self):
        """Gets the signup_method of this Organization.  # noqa: E501


        :return: The signup_method of this Organization.  # noqa: E501
        :rtype: str
        """
        return self._signup_method

    @signup_method.setter
    def signup_method(self, signup_method):
        """Sets the signup_method of this Organization.


        :param signup_method: The signup_method of this Organization.  # noqa: E501
        :type: str
        """
        allowed_values = ["simple", "password", "list"]  # noqa: E501
        if signup_method not in allowed_values:
            raise ValueError(
                "Invalid value for `signup_method` ({0}), must be one of {1}"  # noqa: E501
                .format(signup_method, allowed_values)
            )

        self._signup_method = signup_method

    @property
    def ref(self):
        """Gets the ref of this Organization.  # noqa: E501


        :return: The ref of this Organization.  # noqa: E501
        :rtype: NodeRef
        """
        return self._ref

    @ref.setter
    def ref(self, ref):
        """Sets the ref of this Organization.


        :param ref: The ref of this Organization.  # noqa: E501
        :type: NodeRef
        """

        self._ref = ref

    @property
    def editable(self):
        """Gets the editable of this Organization.  # noqa: E501


        :return: The editable of this Organization.  # noqa: E501
        :rtype: bool
        """
        return self._editable

    @editable.setter
    def editable(self, editable):
        """Sets the editable of this Organization.


        :param editable: The editable of this Organization.  # noqa: E501
        :type: bool
        """

        self._editable = editable

    @property
    def aspects(self):
        """Gets the aspects of this Organization.  # noqa: E501


        :return: The aspects of this Organization.  # noqa: E501
        :rtype: list[str]
        """
        return self._aspects

    @aspects.setter
    def aspects(self, aspects):
        """Sets the aspects of this Organization.


        :param aspects: The aspects of this Organization.  # noqa: E501
        :type: list[str]
        """

        self._aspects = aspects

    @property
    def organizations(self):
        """Gets the organizations of this Organization.  # noqa: E501


        :return: The organizations of this Organization.  # noqa: E501
        :rtype: list[Organization]
        """
        return self._organizations

    @organizations.setter
    def organizations(self, organizations):
        """Sets the organizations of this Organization.


        :param organizations: The organizations of this Organization.  # noqa: E501
        :type: list[Organization]
        """

        self._organizations = organizations

    @property
    def authority_name(self):
        """Gets the authority_name of this Organization.  # noqa: E501


        :return: The authority_name of this Organization.  # noqa: E501
        :rtype: str
        """
        return self._authority_name

    @authority_name.setter
    def authority_name(self, authority_name):
        """Sets the authority_name of this Organization.


        :param authority_name: The authority_name of this Organization.  # noqa: E501
        :type: str
        """
        if authority_name is None:
            raise ValueError("Invalid value for `authority_name`, must not be `None`")  # noqa: E501

        self._authority_name = authority_name

    @property
    def authority_type(self):
        """Gets the authority_type of this Organization.  # noqa: E501


        :return: The authority_type of this Organization.  # noqa: E501
        :rtype: str
        """
        return self._authority_type

    @authority_type.setter
    def authority_type(self, authority_type):
        """Sets the authority_type of this Organization.


        :param authority_type: The authority_type of this Organization.  # noqa: E501
        :type: str
        """
        allowed_values = ["USER", "GROUP", "OWNER", "EVERYONE", "GUEST"]  # noqa: E501
        if authority_type not in allowed_values:
            raise ValueError(
                "Invalid value for `authority_type` ({0}), must be one of {1}"  # noqa: E501
                .format(authority_type, allowed_values)
            )

        self._authority_type = authority_type

    @property
    def group_name(self):
        """Gets the group_name of this Organization.  # noqa: E501


        :return: The group_name of this Organization.  # noqa: E501
        :rtype: str
        """
        return self._group_name

    @group_name.setter
    def group_name(self, group_name):
        """Sets the group_name of this Organization.


        :param group_name: The group_name of this Organization.  # noqa: E501
        :type: str
        """

        self._group_name = group_name

    @property
    def profile(self):
        """Gets the profile of this Organization.  # noqa: E501


        :return: The profile of this Organization.  # noqa: E501
        :rtype: GroupProfile
        """
        return self._profile

    @profile.setter
    def profile(self, profile):
        """Sets the profile of this Organization.


        :param profile: The profile of this Organization.  # noqa: E501
        :type: GroupProfile
        """

        self._profile = profile

    @property
    def administration_access(self):
        """Gets the administration_access of this Organization.  # noqa: E501


        :return: The administration_access of this Organization.  # noqa: E501
        :rtype: bool
        """
        return self._administration_access

    @administration_access.setter
    def administration_access(self, administration_access):
        """Sets the administration_access of this Organization.


        :param administration_access: The administration_access of this Organization.  # noqa: E501
        :type: bool
        """

        self._administration_access = administration_access

    @property
    def shared_folder(self):
        """Gets the shared_folder of this Organization.  # noqa: E501


        :return: The shared_folder of this Organization.  # noqa: E501
        :rtype: NodeRef
        """
        return self._shared_folder

    @shared_folder.setter
    def shared_folder(self, shared_folder):
        """Sets the shared_folder of this Organization.


        :param shared_folder: The shared_folder of this Organization.  # noqa: E501
        :type: NodeRef
        """

        self._shared_folder = shared_folder

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
        if issubclass(Organization, dict):
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
        if not isinstance(other, Organization):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other