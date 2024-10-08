# coding: utf-8

"""
    edu-sharing Repository REST API

    The public restful API of the edu-sharing repository.

    The version of the OpenAPI document: 1.1
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501

import warnings
from pydantic import validate_call, Field, StrictFloat, StrictStr, StrictInt
from typing import Any, Dict, List, Optional, Tuple, Union
from typing_extensions import Annotated

from pydantic import Field, StrictBool, StrictStr
from typing import Dict, List, Optional
from typing_extensions import Annotated
from edu_sharing_client.models.node_entry import NodeEntry

from edu_sharing_client.api_client import ApiClient, RequestSerialized
from edu_sharing_client.api_response import ApiResponse
from edu_sharing_client.rest import RESTResponseType


class BULKV1Api:
    """NOTE: This class is auto generated by OpenAPI Generator
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    def __init__(self, api_client=None) -> None:
        if api_client is None:
            api_client = ApiClient.get_default()
        self.api_client = api_client


    @validate_call
    def find(
        self,
        request_body: Annotated[Dict[str, List[StrictStr]], Field(description="properties that must match (with \"AND\" concatenated)")],
        resolve_node: Annotated[Optional[StrictBool], Field(description="Return the full node. If you don't need the data, set to false to only return the id (will improve performance)")] = None,
        _request_timeout: Union[
            None,
            Annotated[StrictFloat, Field(gt=0)],
            Tuple[
                Annotated[StrictFloat, Field(gt=0)],
                Annotated[StrictFloat, Field(gt=0)]
            ]
        ] = None,
        _request_auth: Optional[Dict[StrictStr, Any]] = None,
        _content_type: Optional[StrictStr] = None,
        _headers: Optional[Dict[StrictStr, Any]] = None,
        _host_index: Annotated[StrictInt, Field(ge=0, le=0)] = 0,
    ) -> NodeEntry:
        """gets a given node

        Get a given node based on the posted, multiple criteria. Make sure that they'll provide an unique result

        :param request_body: properties that must match (with \"AND\" concatenated) (required)
        :type request_body: Dict[str, List[str]]
        :param resolve_node: Return the full node. If you don't need the data, set to false to only return the id (will improve performance)
        :type resolve_node: bool
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :type _request_timeout: int, tuple(int, int), optional
        :param _request_auth: set to override the auth_settings for an a single
                              request; this effectively ignores the
                              authentication in the spec for a single request.
        :type _request_auth: dict, optional
        :param _content_type: force content-type for the request.
        :type _content_type: str, Optional
        :param _headers: set to override the headers for a single
                         request; this effectively ignores the headers
                         in the spec for a single request.
        :type _headers: dict, optional
        :param _host_index: set to override the host_index for a single
                            request; this effectively ignores the host_index
                            in the spec for a single request.
        :type _host_index: int, optional
        :return: Returns the result object.
        """ # noqa: E501

        _param = self._find_serialize(
            request_body=request_body,
            resolve_node=resolve_node,
            _request_auth=_request_auth,
            _content_type=_content_type,
            _headers=_headers,
            _host_index=_host_index
        )

        _response_types_map: Dict[str, Optional[str]] = {
            '200': "NodeEntry",
            '400': "ErrorResponse",
            '401': "ErrorResponse",
            '403': "ErrorResponse",
            '404': "ErrorResponse",
            '500': "ErrorResponse",
        }
        response_data = self.api_client.call_api(
            *_param,
            _request_timeout=_request_timeout
        )
        response_data.read()
        return self.api_client.response_deserialize(
            response_data=response_data,
            response_types_map=_response_types_map,
        ).data


    @validate_call
    def find_with_http_info(
        self,
        request_body: Annotated[Dict[str, List[StrictStr]], Field(description="properties that must match (with \"AND\" concatenated)")],
        resolve_node: Annotated[Optional[StrictBool], Field(description="Return the full node. If you don't need the data, set to false to only return the id (will improve performance)")] = None,
        _request_timeout: Union[
            None,
            Annotated[StrictFloat, Field(gt=0)],
            Tuple[
                Annotated[StrictFloat, Field(gt=0)],
                Annotated[StrictFloat, Field(gt=0)]
            ]
        ] = None,
        _request_auth: Optional[Dict[StrictStr, Any]] = None,
        _content_type: Optional[StrictStr] = None,
        _headers: Optional[Dict[StrictStr, Any]] = None,
        _host_index: Annotated[StrictInt, Field(ge=0, le=0)] = 0,
    ) -> ApiResponse[NodeEntry]:
        """gets a given node

        Get a given node based on the posted, multiple criteria. Make sure that they'll provide an unique result

        :param request_body: properties that must match (with \"AND\" concatenated) (required)
        :type request_body: Dict[str, List[str]]
        :param resolve_node: Return the full node. If you don't need the data, set to false to only return the id (will improve performance)
        :type resolve_node: bool
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :type _request_timeout: int, tuple(int, int), optional
        :param _request_auth: set to override the auth_settings for an a single
                              request; this effectively ignores the
                              authentication in the spec for a single request.
        :type _request_auth: dict, optional
        :param _content_type: force content-type for the request.
        :type _content_type: str, Optional
        :param _headers: set to override the headers for a single
                         request; this effectively ignores the headers
                         in the spec for a single request.
        :type _headers: dict, optional
        :param _host_index: set to override the host_index for a single
                            request; this effectively ignores the host_index
                            in the spec for a single request.
        :type _host_index: int, optional
        :return: Returns the result object.
        """ # noqa: E501

        _param = self._find_serialize(
            request_body=request_body,
            resolve_node=resolve_node,
            _request_auth=_request_auth,
            _content_type=_content_type,
            _headers=_headers,
            _host_index=_host_index
        )

        _response_types_map: Dict[str, Optional[str]] = {
            '200': "NodeEntry",
            '400': "ErrorResponse",
            '401': "ErrorResponse",
            '403': "ErrorResponse",
            '404': "ErrorResponse",
            '500': "ErrorResponse",
        }
        response_data = self.api_client.call_api(
            *_param,
            _request_timeout=_request_timeout
        )
        response_data.read()
        return self.api_client.response_deserialize(
            response_data=response_data,
            response_types_map=_response_types_map,
        )


    @validate_call
    def find_without_preload_content(
        self,
        request_body: Annotated[Dict[str, List[StrictStr]], Field(description="properties that must match (with \"AND\" concatenated)")],
        resolve_node: Annotated[Optional[StrictBool], Field(description="Return the full node. If you don't need the data, set to false to only return the id (will improve performance)")] = None,
        _request_timeout: Union[
            None,
            Annotated[StrictFloat, Field(gt=0)],
            Tuple[
                Annotated[StrictFloat, Field(gt=0)],
                Annotated[StrictFloat, Field(gt=0)]
            ]
        ] = None,
        _request_auth: Optional[Dict[StrictStr, Any]] = None,
        _content_type: Optional[StrictStr] = None,
        _headers: Optional[Dict[StrictStr, Any]] = None,
        _host_index: Annotated[StrictInt, Field(ge=0, le=0)] = 0,
    ) -> RESTResponseType:
        """gets a given node

        Get a given node based on the posted, multiple criteria. Make sure that they'll provide an unique result

        :param request_body: properties that must match (with \"AND\" concatenated) (required)
        :type request_body: Dict[str, List[str]]
        :param resolve_node: Return the full node. If you don't need the data, set to false to only return the id (will improve performance)
        :type resolve_node: bool
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :type _request_timeout: int, tuple(int, int), optional
        :param _request_auth: set to override the auth_settings for an a single
                              request; this effectively ignores the
                              authentication in the spec for a single request.
        :type _request_auth: dict, optional
        :param _content_type: force content-type for the request.
        :type _content_type: str, Optional
        :param _headers: set to override the headers for a single
                         request; this effectively ignores the headers
                         in the spec for a single request.
        :type _headers: dict, optional
        :param _host_index: set to override the host_index for a single
                            request; this effectively ignores the host_index
                            in the spec for a single request.
        :type _host_index: int, optional
        :return: Returns the result object.
        """ # noqa: E501

        _param = self._find_serialize(
            request_body=request_body,
            resolve_node=resolve_node,
            _request_auth=_request_auth,
            _content_type=_content_type,
            _headers=_headers,
            _host_index=_host_index
        )

        _response_types_map: Dict[str, Optional[str]] = {
            '200': "NodeEntry",
            '400': "ErrorResponse",
            '401': "ErrorResponse",
            '403': "ErrorResponse",
            '404': "ErrorResponse",
            '500': "ErrorResponse",
        }
        response_data = self.api_client.call_api(
            *_param,
            _request_timeout=_request_timeout
        )
        return response_data.response


    def _find_serialize(
        self,
        request_body,
        resolve_node,
        _request_auth,
        _content_type,
        _headers,
        _host_index,
    ) -> RequestSerialized:

        _host = None

        _collection_formats: Dict[str, str] = {
        }

        _path_params: Dict[str, str] = {}
        _query_params: List[Tuple[str, str]] = []
        _header_params: Dict[str, Optional[str]] = _headers or {}
        _form_params: List[Tuple[str, str]] = []
        _files: Dict[str, Union[str, bytes]] = {}
        _body_params: Optional[bytes] = None

        # process the path parameters
        # process the query parameters
        if resolve_node is not None:
            
            _query_params.append(('resolveNode', resolve_node))
            
        # process the header parameters
        # process the form parameters
        # process the body parameter
        if request_body is not None:
            _body_params = request_body


        # set the HTTP header `Accept`
        if 'Accept' not in _header_params:
            _header_params['Accept'] = self.api_client.select_header_accept(
                [
                    'application/json'
                ]
            )

        # set the HTTP header `Content-Type`
        if _content_type:
            _header_params['Content-Type'] = _content_type
        else:
            _default_content_type = (
                self.api_client.select_header_content_type(
                    [
                        'application/json'
                    ]
                )
            )
            if _default_content_type is not None:
                _header_params['Content-Type'] = _default_content_type

        # authentication setting
        _auth_settings: List[str] = [
        ]

        return self.api_client.param_serialize(
            method='POST',
            resource_path='/bulk/v1/find',
            path_params=_path_params,
            query_params=_query_params,
            header_params=_header_params,
            body=_body_params,
            post_params=_form_params,
            files=_files,
            auth_settings=_auth_settings,
            collection_formats=_collection_formats,
            _host=_host,
            _request_auth=_request_auth
        )




    @validate_call
    def sync(
        self,
        group: Annotated[StrictStr, Field(description="The group to which this node belongs to. Used for internal structuring. Please use simple names only")],
        match: Annotated[List[StrictStr], Field(description="The properties that must match to identify if this node exists. Multiple properties will be and combined and compared")],
        type: Annotated[StrictStr, Field(description="type of node. If the node already exists, this will not change the type afterwards")],
        request_body: Annotated[Dict[str, List[StrictStr]], Field(description="properties, they'll not get filtered via mds, so be careful what you add here")],
        group_by: Annotated[Optional[List[StrictStr]], Field(description="The properties on which the imported nodes should be grouped (for each value, a folder with the corresponding data is created)")] = None,
        aspects: Annotated[Optional[List[StrictStr]], Field(description="aspects of node")] = None,
        resolve_node: Annotated[Optional[StrictBool], Field(description="Return the generated or updated node. If you don't need the data, set to false to only return the id (will improve performance)")] = None,
        reset_version: Annotated[Optional[StrictBool], Field(description="reset all versions (like a complete reimport), all data inside edu-sharing will be lost")] = None,
        _request_timeout: Union[
            None,
            Annotated[StrictFloat, Field(gt=0)],
            Tuple[
                Annotated[StrictFloat, Field(gt=0)],
                Annotated[StrictFloat, Field(gt=0)]
            ]
        ] = None,
        _request_auth: Optional[Dict[StrictStr, Any]] = None,
        _content_type: Optional[StrictStr] = None,
        _headers: Optional[Dict[StrictStr, Any]] = None,
        _host_index: Annotated[StrictInt, Field(ge=0, le=0)] = 0,
    ) -> NodeEntry:
        """Create or update a given node

        Depending on the given \"match\" properties either a new node will be created or the existing one will be updated

        :param group: The group to which this node belongs to. Used for internal structuring. Please use simple names only (required)
        :type group: str
        :param match: The properties that must match to identify if this node exists. Multiple properties will be and combined and compared (required)
        :type match: List[str]
        :param type: type of node. If the node already exists, this will not change the type afterwards (required)
        :type type: str
        :param request_body: properties, they'll not get filtered via mds, so be careful what you add here (required)
        :type request_body: Dict[str, List[str]]
        :param group_by: The properties on which the imported nodes should be grouped (for each value, a folder with the corresponding data is created)
        :type group_by: List[str]
        :param aspects: aspects of node
        :type aspects: List[str]
        :param resolve_node: Return the generated or updated node. If you don't need the data, set to false to only return the id (will improve performance)
        :type resolve_node: bool
        :param reset_version: reset all versions (like a complete reimport), all data inside edu-sharing will be lost
        :type reset_version: bool
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :type _request_timeout: int, tuple(int, int), optional
        :param _request_auth: set to override the auth_settings for an a single
                              request; this effectively ignores the
                              authentication in the spec for a single request.
        :type _request_auth: dict, optional
        :param _content_type: force content-type for the request.
        :type _content_type: str, Optional
        :param _headers: set to override the headers for a single
                         request; this effectively ignores the headers
                         in the spec for a single request.
        :type _headers: dict, optional
        :param _host_index: set to override the host_index for a single
                            request; this effectively ignores the host_index
                            in the spec for a single request.
        :type _host_index: int, optional
        :return: Returns the result object.
        """ # noqa: E501

        _param = self._sync_serialize(
            group=group,
            match=match,
            type=type,
            request_body=request_body,
            group_by=group_by,
            aspects=aspects,
            resolve_node=resolve_node,
            reset_version=reset_version,
            _request_auth=_request_auth,
            _content_type=_content_type,
            _headers=_headers,
            _host_index=_host_index
        )

        _response_types_map: Dict[str, Optional[str]] = {
            '200': "NodeEntry",
            '400': "ErrorResponse",
            '401': "ErrorResponse",
            '403': "ErrorResponse",
            '404': "ErrorResponse",
            '500': "ErrorResponse",
        }
        response_data = self.api_client.call_api(
            *_param,
            _request_timeout=_request_timeout
        )
        response_data.read()
        return self.api_client.response_deserialize(
            response_data=response_data,
            response_types_map=_response_types_map,
        ).data


    @validate_call
    def sync_with_http_info(
        self,
        group: Annotated[StrictStr, Field(description="The group to which this node belongs to. Used for internal structuring. Please use simple names only")],
        match: Annotated[List[StrictStr], Field(description="The properties that must match to identify if this node exists. Multiple properties will be and combined and compared")],
        type: Annotated[StrictStr, Field(description="type of node. If the node already exists, this will not change the type afterwards")],
        request_body: Annotated[Dict[str, List[StrictStr]], Field(description="properties, they'll not get filtered via mds, so be careful what you add here")],
        group_by: Annotated[Optional[List[StrictStr]], Field(description="The properties on which the imported nodes should be grouped (for each value, a folder with the corresponding data is created)")] = None,
        aspects: Annotated[Optional[List[StrictStr]], Field(description="aspects of node")] = None,
        resolve_node: Annotated[Optional[StrictBool], Field(description="Return the generated or updated node. If you don't need the data, set to false to only return the id (will improve performance)")] = None,
        reset_version: Annotated[Optional[StrictBool], Field(description="reset all versions (like a complete reimport), all data inside edu-sharing will be lost")] = None,
        _request_timeout: Union[
            None,
            Annotated[StrictFloat, Field(gt=0)],
            Tuple[
                Annotated[StrictFloat, Field(gt=0)],
                Annotated[StrictFloat, Field(gt=0)]
            ]
        ] = None,
        _request_auth: Optional[Dict[StrictStr, Any]] = None,
        _content_type: Optional[StrictStr] = None,
        _headers: Optional[Dict[StrictStr, Any]] = None,
        _host_index: Annotated[StrictInt, Field(ge=0, le=0)] = 0,
    ) -> ApiResponse[NodeEntry]:
        """Create or update a given node

        Depending on the given \"match\" properties either a new node will be created or the existing one will be updated

        :param group: The group to which this node belongs to. Used for internal structuring. Please use simple names only (required)
        :type group: str
        :param match: The properties that must match to identify if this node exists. Multiple properties will be and combined and compared (required)
        :type match: List[str]
        :param type: type of node. If the node already exists, this will not change the type afterwards (required)
        :type type: str
        :param request_body: properties, they'll not get filtered via mds, so be careful what you add here (required)
        :type request_body: Dict[str, List[str]]
        :param group_by: The properties on which the imported nodes should be grouped (for each value, a folder with the corresponding data is created)
        :type group_by: List[str]
        :param aspects: aspects of node
        :type aspects: List[str]
        :param resolve_node: Return the generated or updated node. If you don't need the data, set to false to only return the id (will improve performance)
        :type resolve_node: bool
        :param reset_version: reset all versions (like a complete reimport), all data inside edu-sharing will be lost
        :type reset_version: bool
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :type _request_timeout: int, tuple(int, int), optional
        :param _request_auth: set to override the auth_settings for an a single
                              request; this effectively ignores the
                              authentication in the spec for a single request.
        :type _request_auth: dict, optional
        :param _content_type: force content-type for the request.
        :type _content_type: str, Optional
        :param _headers: set to override the headers for a single
                         request; this effectively ignores the headers
                         in the spec for a single request.
        :type _headers: dict, optional
        :param _host_index: set to override the host_index for a single
                            request; this effectively ignores the host_index
                            in the spec for a single request.
        :type _host_index: int, optional
        :return: Returns the result object.
        """ # noqa: E501

        _param = self._sync_serialize(
            group=group,
            match=match,
            type=type,
            request_body=request_body,
            group_by=group_by,
            aspects=aspects,
            resolve_node=resolve_node,
            reset_version=reset_version,
            _request_auth=_request_auth,
            _content_type=_content_type,
            _headers=_headers,
            _host_index=_host_index
        )

        _response_types_map: Dict[str, Optional[str]] = {
            '200': "NodeEntry",
            '400': "ErrorResponse",
            '401': "ErrorResponse",
            '403': "ErrorResponse",
            '404': "ErrorResponse",
            '500': "ErrorResponse",
        }
        response_data = self.api_client.call_api(
            *_param,
            _request_timeout=_request_timeout
        )
        response_data.read()
        return self.api_client.response_deserialize(
            response_data=response_data,
            response_types_map=_response_types_map,
        )


    @validate_call
    def sync_without_preload_content(
        self,
        group: Annotated[StrictStr, Field(description="The group to which this node belongs to. Used for internal structuring. Please use simple names only")],
        match: Annotated[List[StrictStr], Field(description="The properties that must match to identify if this node exists. Multiple properties will be and combined and compared")],
        type: Annotated[StrictStr, Field(description="type of node. If the node already exists, this will not change the type afterwards")],
        request_body: Annotated[Dict[str, List[StrictStr]], Field(description="properties, they'll not get filtered via mds, so be careful what you add here")],
        group_by: Annotated[Optional[List[StrictStr]], Field(description="The properties on which the imported nodes should be grouped (for each value, a folder with the corresponding data is created)")] = None,
        aspects: Annotated[Optional[List[StrictStr]], Field(description="aspects of node")] = None,
        resolve_node: Annotated[Optional[StrictBool], Field(description="Return the generated or updated node. If you don't need the data, set to false to only return the id (will improve performance)")] = None,
        reset_version: Annotated[Optional[StrictBool], Field(description="reset all versions (like a complete reimport), all data inside edu-sharing will be lost")] = None,
        _request_timeout: Union[
            None,
            Annotated[StrictFloat, Field(gt=0)],
            Tuple[
                Annotated[StrictFloat, Field(gt=0)],
                Annotated[StrictFloat, Field(gt=0)]
            ]
        ] = None,
        _request_auth: Optional[Dict[StrictStr, Any]] = None,
        _content_type: Optional[StrictStr] = None,
        _headers: Optional[Dict[StrictStr, Any]] = None,
        _host_index: Annotated[StrictInt, Field(ge=0, le=0)] = 0,
    ) -> RESTResponseType:
        """Create or update a given node

        Depending on the given \"match\" properties either a new node will be created or the existing one will be updated

        :param group: The group to which this node belongs to. Used for internal structuring. Please use simple names only (required)
        :type group: str
        :param match: The properties that must match to identify if this node exists. Multiple properties will be and combined and compared (required)
        :type match: List[str]
        :param type: type of node. If the node already exists, this will not change the type afterwards (required)
        :type type: str
        :param request_body: properties, they'll not get filtered via mds, so be careful what you add here (required)
        :type request_body: Dict[str, List[str]]
        :param group_by: The properties on which the imported nodes should be grouped (for each value, a folder with the corresponding data is created)
        :type group_by: List[str]
        :param aspects: aspects of node
        :type aspects: List[str]
        :param resolve_node: Return the generated or updated node. If you don't need the data, set to false to only return the id (will improve performance)
        :type resolve_node: bool
        :param reset_version: reset all versions (like a complete reimport), all data inside edu-sharing will be lost
        :type reset_version: bool
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :type _request_timeout: int, tuple(int, int), optional
        :param _request_auth: set to override the auth_settings for an a single
                              request; this effectively ignores the
                              authentication in the spec for a single request.
        :type _request_auth: dict, optional
        :param _content_type: force content-type for the request.
        :type _content_type: str, Optional
        :param _headers: set to override the headers for a single
                         request; this effectively ignores the headers
                         in the spec for a single request.
        :type _headers: dict, optional
        :param _host_index: set to override the host_index for a single
                            request; this effectively ignores the host_index
                            in the spec for a single request.
        :type _host_index: int, optional
        :return: Returns the result object.
        """ # noqa: E501

        _param = self._sync_serialize(
            group=group,
            match=match,
            type=type,
            request_body=request_body,
            group_by=group_by,
            aspects=aspects,
            resolve_node=resolve_node,
            reset_version=reset_version,
            _request_auth=_request_auth,
            _content_type=_content_type,
            _headers=_headers,
            _host_index=_host_index
        )

        _response_types_map: Dict[str, Optional[str]] = {
            '200': "NodeEntry",
            '400': "ErrorResponse",
            '401': "ErrorResponse",
            '403': "ErrorResponse",
            '404': "ErrorResponse",
            '500': "ErrorResponse",
        }
        response_data = self.api_client.call_api(
            *_param,
            _request_timeout=_request_timeout
        )
        return response_data.response


    def _sync_serialize(
        self,
        group,
        match,
        type,
        request_body,
        group_by,
        aspects,
        resolve_node,
        reset_version,
        _request_auth,
        _content_type,
        _headers,
        _host_index,
    ) -> RequestSerialized:

        _host = None

        _collection_formats: Dict[str, str] = {
            'match': 'multi',
            'groupBy': 'multi',
            'aspects': 'multi',
        }

        _path_params: Dict[str, str] = {}
        _query_params: List[Tuple[str, str]] = []
        _header_params: Dict[str, Optional[str]] = _headers or {}
        _form_params: List[Tuple[str, str]] = []
        _files: Dict[str, Union[str, bytes]] = {}
        _body_params: Optional[bytes] = None

        # process the path parameters
        if group is not None:
            _path_params['group'] = group
        # process the query parameters
        if match is not None:
            
            _query_params.append(('match', match))
            
        if group_by is not None:
            
            _query_params.append(('groupBy', group_by))
            
        if type is not None:
            
            _query_params.append(('type', type))
            
        if aspects is not None:
            
            _query_params.append(('aspects', aspects))
            
        if resolve_node is not None:
            
            _query_params.append(('resolveNode', resolve_node))
            
        if reset_version is not None:
            
            _query_params.append(('resetVersion', reset_version))
            
        # process the header parameters
        # process the form parameters
        # process the body parameter
        if request_body is not None:
            _body_params = request_body


        # set the HTTP header `Accept`
        if 'Accept' not in _header_params:
            _header_params['Accept'] = self.api_client.select_header_accept(
                [
                    'application/json'
                ]
            )

        # set the HTTP header `Content-Type`
        if _content_type:
            _header_params['Content-Type'] = _content_type
        else:
            _default_content_type = (
                self.api_client.select_header_content_type(
                    [
                        'application/json'
                    ]
                )
            )
            if _default_content_type is not None:
                _header_params['Content-Type'] = _default_content_type

        # authentication setting
        _auth_settings: List[str] = [
        ]

        return self.api_client.param_serialize(
            method='PUT',
            resource_path='/bulk/v1/sync/{group}',
            path_params=_path_params,
            query_params=_query_params,
            header_params=_header_params,
            body=_body_params,
            post_params=_form_params,
            files=_files,
            auth_settings=_auth_settings,
            collection_formats=_collection_formats,
            _host=_host,
            _request_auth=_request_auth
        )


