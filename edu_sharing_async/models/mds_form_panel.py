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

class MdsFormPanel(object):
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
        'name': 'str',
        'style_name': 'str',
        'label': 'str',
        'layout': 'str',
        'on_create': 'bool',
        'on_update': 'bool',
        'multi_upload': 'bool',
        'order': 'str',
        'properties': 'list[MdsFormProperty]'
    }

    attribute_map = {
        'name': 'name',
        'style_name': 'styleName',
        'label': 'label',
        'layout': 'layout',
        'on_create': 'onCreate',
        'on_update': 'onUpdate',
        'multi_upload': 'multiUpload',
        'order': 'order',
        'properties': 'properties'
    }

    def __init__(self, name=None, style_name=None, label=None, layout=None, on_create=False, on_update=False, multi_upload=False, order=None, properties=None):  # noqa: E501
        """MdsFormPanel - a model defined in Swagger"""  # noqa: E501
        self._name = None
        self._style_name = None
        self._label = None
        self._layout = None
        self._on_create = None
        self._on_update = None
        self._multi_upload = None
        self._order = None
        self._properties = None
        self.discriminator = None
        self.name = name
        self.style_name = style_name
        self.label = label
        self.layout = layout
        self.on_create = on_create
        self.on_update = on_update
        self.multi_upload = multi_upload
        self.order = order
        self.properties = properties

    @property
    def name(self):
        """Gets the name of this MdsFormPanel.  # noqa: E501


        :return: The name of this MdsFormPanel.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this MdsFormPanel.


        :param name: The name of this MdsFormPanel.  # noqa: E501
        :type: str
        """
        if name is None:
            raise ValueError("Invalid value for `name`, must not be `None`")  # noqa: E501

        self._name = name

    @property
    def style_name(self):
        """Gets the style_name of this MdsFormPanel.  # noqa: E501


        :return: The style_name of this MdsFormPanel.  # noqa: E501
        :rtype: str
        """
        return self._style_name

    @style_name.setter
    def style_name(self, style_name):
        """Sets the style_name of this MdsFormPanel.


        :param style_name: The style_name of this MdsFormPanel.  # noqa: E501
        :type: str
        """
        if style_name is None:
            raise ValueError("Invalid value for `style_name`, must not be `None`")  # noqa: E501

        self._style_name = style_name

    @property
    def label(self):
        """Gets the label of this MdsFormPanel.  # noqa: E501


        :return: The label of this MdsFormPanel.  # noqa: E501
        :rtype: str
        """
        return self._label

    @label.setter
    def label(self, label):
        """Sets the label of this MdsFormPanel.


        :param label: The label of this MdsFormPanel.  # noqa: E501
        :type: str
        """
        if label is None:
            raise ValueError("Invalid value for `label`, must not be `None`")  # noqa: E501

        self._label = label

    @property
    def layout(self):
        """Gets the layout of this MdsFormPanel.  # noqa: E501


        :return: The layout of this MdsFormPanel.  # noqa: E501
        :rtype: str
        """
        return self._layout

    @layout.setter
    def layout(self, layout):
        """Sets the layout of this MdsFormPanel.


        :param layout: The layout of this MdsFormPanel.  # noqa: E501
        :type: str
        """
        if layout is None:
            raise ValueError("Invalid value for `layout`, must not be `None`")  # noqa: E501

        self._layout = layout

    @property
    def on_create(self):
        """Gets the on_create of this MdsFormPanel.  # noqa: E501


        :return: The on_create of this MdsFormPanel.  # noqa: E501
        :rtype: bool
        """
        return self._on_create

    @on_create.setter
    def on_create(self, on_create):
        """Sets the on_create of this MdsFormPanel.


        :param on_create: The on_create of this MdsFormPanel.  # noqa: E501
        :type: bool
        """
        if on_create is None:
            raise ValueError("Invalid value for `on_create`, must not be `None`")  # noqa: E501

        self._on_create = on_create

    @property
    def on_update(self):
        """Gets the on_update of this MdsFormPanel.  # noqa: E501


        :return: The on_update of this MdsFormPanel.  # noqa: E501
        :rtype: bool
        """
        return self._on_update

    @on_update.setter
    def on_update(self, on_update):
        """Sets the on_update of this MdsFormPanel.


        :param on_update: The on_update of this MdsFormPanel.  # noqa: E501
        :type: bool
        """
        if on_update is None:
            raise ValueError("Invalid value for `on_update`, must not be `None`")  # noqa: E501

        self._on_update = on_update

    @property
    def multi_upload(self):
        """Gets the multi_upload of this MdsFormPanel.  # noqa: E501


        :return: The multi_upload of this MdsFormPanel.  # noqa: E501
        :rtype: bool
        """
        return self._multi_upload

    @multi_upload.setter
    def multi_upload(self, multi_upload):
        """Sets the multi_upload of this MdsFormPanel.


        :param multi_upload: The multi_upload of this MdsFormPanel.  # noqa: E501
        :type: bool
        """
        if multi_upload is None:
            raise ValueError("Invalid value for `multi_upload`, must not be `None`")  # noqa: E501

        self._multi_upload = multi_upload

    @property
    def order(self):
        """Gets the order of this MdsFormPanel.  # noqa: E501


        :return: The order of this MdsFormPanel.  # noqa: E501
        :rtype: str
        """
        return self._order

    @order.setter
    def order(self, order):
        """Sets the order of this MdsFormPanel.


        :param order: The order of this MdsFormPanel.  # noqa: E501
        :type: str
        """
        if order is None:
            raise ValueError("Invalid value for `order`, must not be `None`")  # noqa: E501

        self._order = order

    @property
    def properties(self):
        """Gets the properties of this MdsFormPanel.  # noqa: E501


        :return: The properties of this MdsFormPanel.  # noqa: E501
        :rtype: list[MdsFormProperty]
        """
        return self._properties

    @properties.setter
    def properties(self, properties):
        """Sets the properties of this MdsFormPanel.


        :param properties: The properties of this MdsFormPanel.  # noqa: E501
        :type: list[MdsFormProperty]
        """
        if properties is None:
            raise ValueError("Invalid value for `properties`, must not be `None`")  # noqa: E501

        self._properties = properties

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
        if issubclass(MdsFormPanel, dict):
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
        if not isinstance(other, MdsFormPanel):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
