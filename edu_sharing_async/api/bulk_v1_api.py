# coding: utf-8

"""
    edu-sharing Repository REST API

    The public restful API of the edu-sharing repository.  # noqa: E501

    OpenAPI spec version: 1.1
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

from __future__ import absolute_import

import re  # noqa: F401

# python 2 and python 3 compatibility library
import six

from edu_sharing_async.api_client import ApiClient


class BULKV1Api(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    Ref: https://github.com/swagger-api/swagger-codegen
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    def find(self, body, **kwargs):  # noqa: E501
        """gets a given node  # noqa: E501

        Get a given node based on the posted, multiple criterias. Make sure that they'll provide an unique result  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.find(body, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param dict(str, list[str]) body: properties that must match (with "AND" concatenated) (required)
        :return: NodeEntry
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.find_with_http_info(body, **kwargs)  # noqa: E501
        else:
            (data) = self.find_with_http_info(body, **kwargs)  # noqa: E501
            return data

    def find_with_http_info(self, body, **kwargs):  # noqa: E501
        """gets a given node  # noqa: E501

        Get a given node based on the posted, multiple criterias. Make sure that they'll provide an unique result  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.find_with_http_info(body, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param dict(str, list[str]) body: properties that must match (with "AND" concatenated) (required)
        :return: NodeEntry
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['body']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method find" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'body' is set
        if ('body' not in params or
                params['body'] is None):
            raise ValueError("Missing the required parameter `body` when calling `find`")  # noqa: E501

        collection_formats = {}

        path_params = {}

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'body' in params:
            body_params = params['body']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['*/*'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['*/*'])  # noqa: E501

        # Authentication setting
        auth_settings = []  # noqa: E501

        return self.api_client.call_api(
            '/bulk/v1/find', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='NodeEntry',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def sync(self, body, match, type, group, **kwargs):  # noqa: E501
        """Create or update a given node  # noqa: E501

        Depending on the given \"match\" properties either a new node will be created or the existing one will be updated  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.sync(body, match, type, group, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param dict(str, list[str]) body: properties, they'll not get filtered via mds, so be careful what you add here (required)
        :param list[str] match: The properties that must match to identify if this node exists. Multiple properties will be and combined and compared (required)
        :param str type: type of node. If the node already exists, this will not change the type afterwards (required)
        :param str group: The group to which this node belongs to. Used for internal structuring. Please use simple names only (required)
        :param list[str] group_by: The properties on which the imported nodes should be grouped (for each value, a folder with the corresponding data is created)
        :param list[str] aspects: aspects of node
        :param bool reset_version: reset all versions (like a complete reimport), all data inside edu-sharing will be lost
        :return: NodeEntry
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.sync_with_http_info(body, match, type, group, **kwargs)  # noqa: E501
        else:
            (data) = self.sync_with_http_info(body, match, type, group, **kwargs)  # noqa: E501
            return data

    def sync_with_http_info(self, body, match, type, group, **kwargs):  # noqa: E501
        """Create or update a given node  # noqa: E501

        Depending on the given \"match\" properties either a new node will be created or the existing one will be updated  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.sync_with_http_info(body, match, type, group, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param dict(str, list[str]) body: properties, they'll not get filtered via mds, so be careful what you add here (required)
        :param list[str] match: The properties that must match to identify if this node exists. Multiple properties will be and combined and compared (required)
        :param str type: type of node. If the node already exists, this will not change the type afterwards (required)
        :param str group: The group to which this node belongs to. Used for internal structuring. Please use simple names only (required)
        :param list[str] group_by: The properties on which the imported nodes should be grouped (for each value, a folder with the corresponding data is created)
        :param list[str] aspects: aspects of node
        :param bool reset_version: reset all versions (like a complete reimport), all data inside edu-sharing will be lost
        :return: NodeEntry
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['body', 'match', 'type', 'group', 'group_by', 'aspects', 'reset_version']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method sync" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'body' is set
        if ('body' not in params or
                params['body'] is None):
            raise ValueError("Missing the required parameter `body` when calling `sync`")  # noqa: E501
        # verify the required parameter 'match' is set
        if ('match' not in params or
                params['match'] is None):
            raise ValueError("Missing the required parameter `match` when calling `sync`")  # noqa: E501
        # verify the required parameter 'type' is set
        if ('type' not in params or
                params['type'] is None):
            raise ValueError("Missing the required parameter `type` when calling `sync`")  # noqa: E501
        # verify the required parameter 'group' is set
        if ('group' not in params or
                params['group'] is None):
            raise ValueError("Missing the required parameter `group` when calling `sync`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'group' in params:
            path_params['group'] = params['group']  # noqa: E501

        query_params = []
        if 'match' in params:
            query_params.append(('match', params['match']))  # noqa: E501
            collection_formats['match'] = 'multi'  # noqa: E501
        if 'group_by' in params:
            query_params.append(('groupBy', params['group_by']))  # noqa: E501
            collection_formats['groupBy'] = 'multi'  # noqa: E501
        if 'type' in params:
            query_params.append(('type', params['type']))  # noqa: E501
        if 'aspects' in params:
            query_params.append(('aspects', params['aspects']))  # noqa: E501
            collection_formats['aspects'] = 'multi'  # noqa: E501
        if 'reset_version' in params:
            query_params.append(('resetVersion', params['reset_version']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'body' in params:
            body_params = params['body']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['*/*'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['*/*'])  # noqa: E501

        # Authentication setting
        auth_settings = []  # noqa: E501

        return self.api_client.call_api(
            '/bulk/v1/sync/{group}', 'PUT',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='NodeEntry',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)
