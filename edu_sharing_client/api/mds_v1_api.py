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

from edu_sharing_client.api_client import ApiClient


class MDSV1Api(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    Ref: https://github.com/swagger-api/swagger-codegen
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    def get_metadata_set_v2(self, repository, metadataset, **kwargs):  # noqa: E501
        """Get metadata set new.  # noqa: E501

        Get metadata set new.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_metadata_set_v2(repository, metadataset, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str repository: ID of repository (or \"-home-\" for home repository) (required)
        :param str metadataset: ID of metadataset (or \"-default-\" for default metadata set) (required)
        :return: MdsV2
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_metadata_set_v2_with_http_info(repository, metadataset, **kwargs)  # noqa: E501
        else:
            (data) = self.get_metadata_set_v2_with_http_info(repository, metadataset, **kwargs)  # noqa: E501
            return data

    def get_metadata_set_v2_with_http_info(self, repository, metadataset, **kwargs):  # noqa: E501
        """Get metadata set new.  # noqa: E501

        Get metadata set new.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_metadata_set_v2_with_http_info(repository, metadataset, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str repository: ID of repository (or \"-home-\" for home repository) (required)
        :param str metadataset: ID of metadataset (or \"-default-\" for default metadata set) (required)
        :return: MdsV2
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['repository', 'metadataset']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_metadata_set_v2" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'repository' is set
        if ('repository' not in params or
                params['repository'] is None):
            raise ValueError("Missing the required parameter `repository` when calling `get_metadata_set_v2`")  # noqa: E501
        # verify the required parameter 'metadataset' is set
        if ('metadataset' not in params or
                params['metadataset'] is None):
            raise ValueError("Missing the required parameter `metadataset` when calling `get_metadata_set_v2`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'repository' in params:
            path_params['repository'] = params['repository']  # noqa: E501
        if 'metadataset' in params:
            path_params['metadataset'] = params['metadataset']  # noqa: E501

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['*/*'])  # noqa: E501

        # Authentication setting
        auth_settings = []  # noqa: E501

        return self.api_client.call_api(
            '/mds/v1/metadatasetsV2/{repository}/{metadataset}', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='MdsV2',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_metadata_sets_v2(self, repository, **kwargs):  # noqa: E501
        """Get metadata sets V2 of repository.  # noqa: E501

        Get metadata sets V2 of repository.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_metadata_sets_v2(repository, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str repository: ID of repository (or \"-home-\" for home repository) (required)
        :return: MdsEntriesV2
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_metadata_sets_v2_with_http_info(repository, **kwargs)  # noqa: E501
        else:
            (data) = self.get_metadata_sets_v2_with_http_info(repository, **kwargs)  # noqa: E501
            return data

    def get_metadata_sets_v2_with_http_info(self, repository, **kwargs):  # noqa: E501
        """Get metadata sets V2 of repository.  # noqa: E501

        Get metadata sets V2 of repository.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_metadata_sets_v2_with_http_info(repository, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str repository: ID of repository (or \"-home-\" for home repository) (required)
        :return: MdsEntriesV2
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['repository']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_metadata_sets_v2" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'repository' is set
        if ('repository' not in params or
                params['repository'] is None):
            raise ValueError("Missing the required parameter `repository` when calling `get_metadata_sets_v2`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'repository' in params:
            path_params['repository'] = params['repository']  # noqa: E501

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['*/*'])  # noqa: E501

        # Authentication setting
        auth_settings = []  # noqa: E501

        return self.api_client.call_api(
            '/mds/v1/metadatasetsV2/{repository}', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='MdsEntriesV2',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_values4_keys_v2(self, repository, metadataset, **kwargs):  # noqa: E501
        """Get values for keys.  # noqa: E501

        Get values for keys.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_values4_keys_v2(repository, metadataset, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str repository: ID of repository (or \"-home-\" for home repository) (required)
        :param str metadataset: ID of metadataset (or \"-default-\" for default metadata set) (required)
        :param list[str] body: keys
        :param str query: query
        :param str _property: property
        :return: Suggestions
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_values4_keys_v2_with_http_info(repository, metadataset, **kwargs)  # noqa: E501
        else:
            (data) = self.get_values4_keys_v2_with_http_info(repository, metadataset, **kwargs)  # noqa: E501
            return data

    def get_values4_keys_v2_with_http_info(self, repository, metadataset, **kwargs):  # noqa: E501
        """Get values for keys.  # noqa: E501

        Get values for keys.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_values4_keys_v2_with_http_info(repository, metadataset, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str repository: ID of repository (or \"-home-\" for home repository) (required)
        :param str metadataset: ID of metadataset (or \"-default-\" for default metadata set) (required)
        :param list[str] body: keys
        :param str query: query
        :param str _property: property
        :return: Suggestions
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['repository', 'metadataset', 'body', 'query', '_property']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_values4_keys_v2" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'repository' is set
        if ('repository' not in params or
                params['repository'] is None):
            raise ValueError("Missing the required parameter `repository` when calling `get_values4_keys_v2`")  # noqa: E501
        # verify the required parameter 'metadataset' is set
        if ('metadataset' not in params or
                params['metadataset'] is None):
            raise ValueError("Missing the required parameter `metadataset` when calling `get_values4_keys_v2`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'repository' in params:
            path_params['repository'] = params['repository']  # noqa: E501
        if 'metadataset' in params:
            path_params['metadataset'] = params['metadataset']  # noqa: E501

        query_params = []
        if 'query' in params:
            query_params.append(('query', params['query']))  # noqa: E501
        if '_property' in params:
            query_params.append(('property', params['_property']))  # noqa: E501

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
            '/mds/v1/metadatasetsV2/{repository}/{metadataset}/values_for_keys', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='Suggestions',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_values_v2(self, repository, metadataset, **kwargs):  # noqa: E501
        """Get values.  # noqa: E501

        Get values.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_values_v2(repository, metadataset, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str repository: ID of repository (or \"-home-\" for home repository) (required)
        :param str metadataset: ID of metadataset (or \"-default-\" for default metadata set) (required)
        :param SuggestionParam body: suggestionParam
        :return: Suggestions
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_values_v2_with_http_info(repository, metadataset, **kwargs)  # noqa: E501
        else:
            (data) = self.get_values_v2_with_http_info(repository, metadataset, **kwargs)  # noqa: E501
            return data

    def get_values_v2_with_http_info(self, repository, metadataset, **kwargs):  # noqa: E501
        """Get values.  # noqa: E501

        Get values.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_values_v2_with_http_info(repository, metadataset, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str repository: ID of repository (or \"-home-\" for home repository) (required)
        :param str metadataset: ID of metadataset (or \"-default-\" for default metadata set) (required)
        :param SuggestionParam body: suggestionParam
        :return: Suggestions
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['repository', 'metadataset', 'body']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_values_v2" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'repository' is set
        if ('repository' not in params or
                params['repository'] is None):
            raise ValueError("Missing the required parameter `repository` when calling `get_values_v2`")  # noqa: E501
        # verify the required parameter 'metadataset' is set
        if ('metadataset' not in params or
                params['metadataset'] is None):
            raise ValueError("Missing the required parameter `metadataset` when calling `get_values_v2`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'repository' in params:
            path_params['repository'] = params['repository']  # noqa: E501
        if 'metadataset' in params:
            path_params['metadataset'] = params['metadataset']  # noqa: E501

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
            '/mds/v1/metadatasetsV2/{repository}/{metadataset}/values', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='Suggestions',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)
