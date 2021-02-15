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

class WidgetV2(object):
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
        'link': 'str',
        'subwidgets': 'list[Subwidget]',
        'condition': 'Condition',
        'maxlength': 'int',
        'id': 'str',
        'caption': 'str',
        'bottom_caption': 'str',
        'icon': 'str',
        'type': 'str',
        'template': 'str',
        'has_values': 'bool',
        'values': 'list[ValueV2]',
        'placeholder': 'str',
        'unit': 'str',
        'min': 'int',
        'max': 'int',
        'default_min': 'int',
        'default_max': 'int',
        'step': 'int',
        'is_required': 'str',
        'allowempty': 'bool',
        'defaultvalue': 'str',
        'is_extended': 'bool',
        'is_searchable': 'bool'
    }

    attribute_map = {
        'link': 'link',
        'subwidgets': 'subwidgets',
        'condition': 'condition',
        'maxlength': 'maxlength',
        'id': 'id',
        'caption': 'caption',
        'bottom_caption': 'bottomCaption',
        'icon': 'icon',
        'type': 'type',
        'template': 'template',
        'has_values': 'hasValues',
        'values': 'values',
        'placeholder': 'placeholder',
        'unit': 'unit',
        'min': 'min',
        'max': 'max',
        'default_min': 'defaultMin',
        'default_max': 'defaultMax',
        'step': 'step',
        'is_required': 'isRequired',
        'allowempty': 'allowempty',
        'defaultvalue': 'defaultvalue',
        'is_extended': 'isExtended',
        'is_searchable': 'isSearchable'
    }

    def __init__(self, link=None, subwidgets=None, condition=None, maxlength=None, id=None, caption=None, bottom_caption=None, icon=None, type=None, template=None, has_values=False, values=None, placeholder=None, unit=None, min=None, max=None, default_min=None, default_max=None, step=None, is_required=None, allowempty=False, defaultvalue=None, is_extended=False, is_searchable=False):  # noqa: E501
        """WidgetV2 - a model defined in Swagger"""  # noqa: E501
        self._link = None
        self._subwidgets = None
        self._condition = None
        self._maxlength = None
        self._id = None
        self._caption = None
        self._bottom_caption = None
        self._icon = None
        self._type = None
        self._template = None
        self._has_values = None
        self._values = None
        self._placeholder = None
        self._unit = None
        self._min = None
        self._max = None
        self._default_min = None
        self._default_max = None
        self._step = None
        self._is_required = None
        self._allowempty = None
        self._defaultvalue = None
        self._is_extended = None
        self._is_searchable = None
        self.discriminator = None
        if link is not None:
            self.link = link
        if subwidgets is not None:
            self.subwidgets = subwidgets
        if condition is not None:
            self.condition = condition
        if maxlength is not None:
            self.maxlength = maxlength
        if id is not None:
            self.id = id
        if caption is not None:
            self.caption = caption
        if bottom_caption is not None:
            self.bottom_caption = bottom_caption
        if icon is not None:
            self.icon = icon
        if type is not None:
            self.type = type
        if template is not None:
            self.template = template
        if has_values is not None:
            self.has_values = has_values
        if values is not None:
            self.values = values
        if placeholder is not None:
            self.placeholder = placeholder
        if unit is not None:
            self.unit = unit
        if min is not None:
            self.min = min
        if max is not None:
            self.max = max
        if default_min is not None:
            self.default_min = default_min
        if default_max is not None:
            self.default_max = default_max
        if step is not None:
            self.step = step
        if is_required is not None:
            self.is_required = is_required
        if allowempty is not None:
            self.allowempty = allowempty
        if defaultvalue is not None:
            self.defaultvalue = defaultvalue
        if is_extended is not None:
            self.is_extended = is_extended
        if is_searchable is not None:
            self.is_searchable = is_searchable

    @property
    def link(self):
        """Gets the link of this WidgetV2.  # noqa: E501


        :return: The link of this WidgetV2.  # noqa: E501
        :rtype: str
        """
        return self._link

    @link.setter
    def link(self, link):
        """Sets the link of this WidgetV2.


        :param link: The link of this WidgetV2.  # noqa: E501
        :type: str
        """

        self._link = link

    @property
    def subwidgets(self):
        """Gets the subwidgets of this WidgetV2.  # noqa: E501


        :return: The subwidgets of this WidgetV2.  # noqa: E501
        :rtype: list[Subwidget]
        """
        return self._subwidgets

    @subwidgets.setter
    def subwidgets(self, subwidgets):
        """Sets the subwidgets of this WidgetV2.


        :param subwidgets: The subwidgets of this WidgetV2.  # noqa: E501
        :type: list[Subwidget]
        """

        self._subwidgets = subwidgets

    @property
    def condition(self):
        """Gets the condition of this WidgetV2.  # noqa: E501


        :return: The condition of this WidgetV2.  # noqa: E501
        :rtype: Condition
        """
        return self._condition

    @condition.setter
    def condition(self, condition):
        """Sets the condition of this WidgetV2.


        :param condition: The condition of this WidgetV2.  # noqa: E501
        :type: Condition
        """

        self._condition = condition

    @property
    def maxlength(self):
        """Gets the maxlength of this WidgetV2.  # noqa: E501


        :return: The maxlength of this WidgetV2.  # noqa: E501
        :rtype: int
        """
        return self._maxlength

    @maxlength.setter
    def maxlength(self, maxlength):
        """Sets the maxlength of this WidgetV2.


        :param maxlength: The maxlength of this WidgetV2.  # noqa: E501
        :type: int
        """

        self._maxlength = maxlength

    @property
    def id(self):
        """Gets the id of this WidgetV2.  # noqa: E501


        :return: The id of this WidgetV2.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this WidgetV2.


        :param id: The id of this WidgetV2.  # noqa: E501
        :type: str
        """

        self._id = id

    @property
    def caption(self):
        """Gets the caption of this WidgetV2.  # noqa: E501


        :return: The caption of this WidgetV2.  # noqa: E501
        :rtype: str
        """
        return self._caption

    @caption.setter
    def caption(self, caption):
        """Sets the caption of this WidgetV2.


        :param caption: The caption of this WidgetV2.  # noqa: E501
        :type: str
        """

        self._caption = caption

    @property
    def bottom_caption(self):
        """Gets the bottom_caption of this WidgetV2.  # noqa: E501


        :return: The bottom_caption of this WidgetV2.  # noqa: E501
        :rtype: str
        """
        return self._bottom_caption

    @bottom_caption.setter
    def bottom_caption(self, bottom_caption):
        """Sets the bottom_caption of this WidgetV2.


        :param bottom_caption: The bottom_caption of this WidgetV2.  # noqa: E501
        :type: str
        """

        self._bottom_caption = bottom_caption

    @property
    def icon(self):
        """Gets the icon of this WidgetV2.  # noqa: E501


        :return: The icon of this WidgetV2.  # noqa: E501
        :rtype: str
        """
        return self._icon

    @icon.setter
    def icon(self, icon):
        """Sets the icon of this WidgetV2.


        :param icon: The icon of this WidgetV2.  # noqa: E501
        :type: str
        """

        self._icon = icon

    @property
    def type(self):
        """Gets the type of this WidgetV2.  # noqa: E501


        :return: The type of this WidgetV2.  # noqa: E501
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """Sets the type of this WidgetV2.


        :param type: The type of this WidgetV2.  # noqa: E501
        :type: str
        """

        self._type = type

    @property
    def template(self):
        """Gets the template of this WidgetV2.  # noqa: E501


        :return: The template of this WidgetV2.  # noqa: E501
        :rtype: str
        """
        return self._template

    @template.setter
    def template(self, template):
        """Sets the template of this WidgetV2.


        :param template: The template of this WidgetV2.  # noqa: E501
        :type: str
        """

        self._template = template

    @property
    def has_values(self):
        """Gets the has_values of this WidgetV2.  # noqa: E501


        :return: The has_values of this WidgetV2.  # noqa: E501
        :rtype: bool
        """
        return self._has_values

    @has_values.setter
    def has_values(self, has_values):
        """Sets the has_values of this WidgetV2.


        :param has_values: The has_values of this WidgetV2.  # noqa: E501
        :type: bool
        """

        self._has_values = has_values

    @property
    def values(self):
        """Gets the values of this WidgetV2.  # noqa: E501


        :return: The values of this WidgetV2.  # noqa: E501
        :rtype: list[ValueV2]
        """
        return self._values

    @values.setter
    def values(self, values):
        """Sets the values of this WidgetV2.


        :param values: The values of this WidgetV2.  # noqa: E501
        :type: list[ValueV2]
        """

        self._values = values

    @property
    def placeholder(self):
        """Gets the placeholder of this WidgetV2.  # noqa: E501


        :return: The placeholder of this WidgetV2.  # noqa: E501
        :rtype: str
        """
        return self._placeholder

    @placeholder.setter
    def placeholder(self, placeholder):
        """Sets the placeholder of this WidgetV2.


        :param placeholder: The placeholder of this WidgetV2.  # noqa: E501
        :type: str
        """

        self._placeholder = placeholder

    @property
    def unit(self):
        """Gets the unit of this WidgetV2.  # noqa: E501


        :return: The unit of this WidgetV2.  # noqa: E501
        :rtype: str
        """
        return self._unit

    @unit.setter
    def unit(self, unit):
        """Sets the unit of this WidgetV2.


        :param unit: The unit of this WidgetV2.  # noqa: E501
        :type: str
        """

        self._unit = unit

    @property
    def min(self):
        """Gets the min of this WidgetV2.  # noqa: E501


        :return: The min of this WidgetV2.  # noqa: E501
        :rtype: int
        """
        return self._min

    @min.setter
    def min(self, min):
        """Sets the min of this WidgetV2.


        :param min: The min of this WidgetV2.  # noqa: E501
        :type: int
        """

        self._min = min

    @property
    def max(self):
        """Gets the max of this WidgetV2.  # noqa: E501


        :return: The max of this WidgetV2.  # noqa: E501
        :rtype: int
        """
        return self._max

    @max.setter
    def max(self, max):
        """Sets the max of this WidgetV2.


        :param max: The max of this WidgetV2.  # noqa: E501
        :type: int
        """

        self._max = max

    @property
    def default_min(self):
        """Gets the default_min of this WidgetV2.  # noqa: E501


        :return: The default_min of this WidgetV2.  # noqa: E501
        :rtype: int
        """
        return self._default_min

    @default_min.setter
    def default_min(self, default_min):
        """Sets the default_min of this WidgetV2.


        :param default_min: The default_min of this WidgetV2.  # noqa: E501
        :type: int
        """

        self._default_min = default_min

    @property
    def default_max(self):
        """Gets the default_max of this WidgetV2.  # noqa: E501


        :return: The default_max of this WidgetV2.  # noqa: E501
        :rtype: int
        """
        return self._default_max

    @default_max.setter
    def default_max(self, default_max):
        """Sets the default_max of this WidgetV2.


        :param default_max: The default_max of this WidgetV2.  # noqa: E501
        :type: int
        """

        self._default_max = default_max

    @property
    def step(self):
        """Gets the step of this WidgetV2.  # noqa: E501


        :return: The step of this WidgetV2.  # noqa: E501
        :rtype: int
        """
        return self._step

    @step.setter
    def step(self, step):
        """Sets the step of this WidgetV2.


        :param step: The step of this WidgetV2.  # noqa: E501
        :type: int
        """

        self._step = step

    @property
    def is_required(self):
        """Gets the is_required of this WidgetV2.  # noqa: E501


        :return: The is_required of this WidgetV2.  # noqa: E501
        :rtype: str
        """
        return self._is_required

    @is_required.setter
    def is_required(self, is_required):
        """Sets the is_required of this WidgetV2.


        :param is_required: The is_required of this WidgetV2.  # noqa: E501
        :type: str
        """
        allowed_values = ["mandatory", "mandatoryForPublish", "optional", "ignore"]  # noqa: E501
        if is_required not in allowed_values:
            raise ValueError(
                "Invalid value for `is_required` ({0}), must be one of {1}"  # noqa: E501
                .format(is_required, allowed_values)
            )

        self._is_required = is_required

    @property
    def allowempty(self):
        """Gets the allowempty of this WidgetV2.  # noqa: E501


        :return: The allowempty of this WidgetV2.  # noqa: E501
        :rtype: bool
        """
        return self._allowempty

    @allowempty.setter
    def allowempty(self, allowempty):
        """Sets the allowempty of this WidgetV2.


        :param allowempty: The allowempty of this WidgetV2.  # noqa: E501
        :type: bool
        """

        self._allowempty = allowempty

    @property
    def defaultvalue(self):
        """Gets the defaultvalue of this WidgetV2.  # noqa: E501


        :return: The defaultvalue of this WidgetV2.  # noqa: E501
        :rtype: str
        """
        return self._defaultvalue

    @defaultvalue.setter
    def defaultvalue(self, defaultvalue):
        """Sets the defaultvalue of this WidgetV2.


        :param defaultvalue: The defaultvalue of this WidgetV2.  # noqa: E501
        :type: str
        """

        self._defaultvalue = defaultvalue

    @property
    def is_extended(self):
        """Gets the is_extended of this WidgetV2.  # noqa: E501


        :return: The is_extended of this WidgetV2.  # noqa: E501
        :rtype: bool
        """
        return self._is_extended

    @is_extended.setter
    def is_extended(self, is_extended):
        """Sets the is_extended of this WidgetV2.


        :param is_extended: The is_extended of this WidgetV2.  # noqa: E501
        :type: bool
        """

        self._is_extended = is_extended

    @property
    def is_searchable(self):
        """Gets the is_searchable of this WidgetV2.  # noqa: E501


        :return: The is_searchable of this WidgetV2.  # noqa: E501
        :rtype: bool
        """
        return self._is_searchable

    @is_searchable.setter
    def is_searchable(self, is_searchable):
        """Sets the is_searchable of this WidgetV2.


        :param is_searchable: The is_searchable of this WidgetV2.  # noqa: E501
        :type: bool
        """

        self._is_searchable = is_searchable

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
        if issubclass(WidgetV2, dict):
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
        if not isinstance(other, WidgetV2):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
