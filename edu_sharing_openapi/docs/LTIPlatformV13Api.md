# edu_sharing_client.LTIPlatformV13Api

All URIs are relative to *https://stable.demo.edu-sharing.net/edu-sharing/rest*

Method | HTTP request | Description
------------- | ------------- | -------------
[**auth**](LTIPlatformV13Api.md#auth) | **GET** /ltiplatform/v13/auth | LTI Platform oidc endpoint. responds to a login authentication request
[**auth_token_endpoint**](LTIPlatformV13Api.md#auth_token_endpoint) | **GET** /ltiplatform/v13/token | LTIPlatform auth token endpoint
[**change_content**](LTIPlatformV13Api.md#change_content) | **POST** /ltiplatform/v13/content | Custom edu-sharing endpoint to change content of node.
[**convert_to_resourcelink**](LTIPlatformV13Api.md#convert_to_resourcelink) | **POST** /ltiplatform/v13/convert2resourcelink | manual convertion of an io to an resource link without deeplinking
[**deep_linking_response**](LTIPlatformV13Api.md#deep_linking_response) | **POST** /ltiplatform/v13/deeplinking-response | receiving deeplink response messages.
[**generate_login_initiation_form**](LTIPlatformV13Api.md#generate_login_initiation_form) | **GET** /ltiplatform/v13/generateLoginInitiationForm | generate a form used for Initiating Login from a Third Party. Use thes endpoint when starting a lti deeplink flow.
[**generate_login_initiation_form_resource_link**](LTIPlatformV13Api.md#generate_login_initiation_form_resource_link) | **GET** /ltiplatform/v13/generateLoginInitiationFormResourceLink | generate a form used for Initiating Login from a Third Party. Use thes endpoint when starting a lti resourcelink flow.
[**get_content**](LTIPlatformV13Api.md#get_content) | **GET** /ltiplatform/v13/content | Custom edu-sharing endpoint to get content of node.
[**manual_registration**](LTIPlatformV13Api.md#manual_registration) | **POST** /ltiplatform/v13/manual-registration | manual registration endpoint for registration of tools.
[**open_id_registration**](LTIPlatformV13Api.md#open_id_registration) | **POST** /ltiplatform/v13/openid-registration | registration endpoint the tool uses to register at platform.
[**openid_configuration**](LTIPlatformV13Api.md#openid_configuration) | **GET** /ltiplatform/v13/openid-configuration | LTIPlatform openid configuration
[**start_dynamic_registration**](LTIPlatformV13Api.md#start_dynamic_registration) | **POST** /ltiplatform/v13/start-dynamic-registration | starts lti dynamic registration.
[**start_dynamic_registration_get**](LTIPlatformV13Api.md#start_dynamic_registration_get) | **GET** /ltiplatform/v13/start-dynamic-registration | starts lti dynamic registration.
[**test_token**](LTIPlatformV13Api.md#test_token) | **PUT** /ltiplatform/v13/testToken | test creates a token signed with homeapp.
[**tools**](LTIPlatformV13Api.md#tools) | **GET** /ltiplatform/v13/tools | List of tools registered


# **auth**
> str auth(scope, response_type, login_hint, state, response_mode, nonce, prompt, redirect_uri, client_id=client_id, lti_message_hint=lti_message_hint)

LTI Platform oidc endpoint. responds to a login authentication request

### Example


```python
import edu_sharing_client
from edu_sharing_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://stable.demo.edu-sharing.net/edu-sharing/rest
# See configuration.py for a list of all supported configuration parameters.
configuration = edu_sharing_client.Configuration(
    host = "https://stable.demo.edu-sharing.net/edu-sharing/rest"
)


# Enter a context with an instance of the API client
with edu_sharing_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = edu_sharing_client.LTIPlatformV13Api(api_client)
    scope = 'scope_example' # str | scope
    response_type = 'response_type_example' # str | response_type
    login_hint = 'login_hint_example' # str | login_hint
    state = 'state_example' # str | state
    response_mode = 'response_mode_example' # str | response_mode
    nonce = 'nonce_example' # str | nonce
    prompt = 'prompt_example' # str | prompt
    redirect_uri = 'redirect_uri_example' # str | redirect_uri
    client_id = 'client_id_example' # str | optional parameter client_id specifies the client id for the authorization server that should be used to authorize the subsequent LTI message request (optional)
    lti_message_hint = 'lti_message_hint_example' # str | Similarly to the login_hint parameter, lti_message_hint value is opaque to the tool. If present in the login initiation request, the tool MUST include it back in the authentication request unaltered (optional)

    try:
        # LTI Platform oidc endpoint. responds to a login authentication request
        api_response = api_instance.auth(scope, response_type, login_hint, state, response_mode, nonce, prompt, redirect_uri, client_id=client_id, lti_message_hint=lti_message_hint)
        print("The response of LTIPlatformV13Api->auth:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling LTIPlatformV13Api->auth: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **scope** | **str**| scope | 
 **response_type** | **str**| response_type | 
 **login_hint** | **str**| login_hint | 
 **state** | **str**| state | 
 **response_mode** | **str**| response_mode | 
 **nonce** | **str**| nonce | 
 **prompt** | **str**| prompt | 
 **redirect_uri** | **str**| redirect_uri | 
 **client_id** | **str**| optional parameter client_id specifies the client id for the authorization server that should be used to authorize the subsequent LTI message request | [optional] 
 **lti_message_hint** | **str**| Similarly to the login_hint parameter, lti_message_hint value is opaque to the tool. If present in the login initiation request, the tool MUST include it back in the authentication request unaltered | [optional] 

### Return type

**str**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/html

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK. |  -  |
**400** | Preconditions are not present. |  -  |
**401** | Authorization failed. |  -  |
**403** | Session user has insufficient rights to perform this operation. |  -  |
**404** | Ressources are not found. |  -  |
**500** | Fatal error occured. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **auth_token_endpoint**
> auth_token_endpoint()

LTIPlatform auth token endpoint

### Example


```python
import edu_sharing_client
from edu_sharing_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://stable.demo.edu-sharing.net/edu-sharing/rest
# See configuration.py for a list of all supported configuration parameters.
configuration = edu_sharing_client.Configuration(
    host = "https://stable.demo.edu-sharing.net/edu-sharing/rest"
)


# Enter a context with an instance of the API client
with edu_sharing_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = edu_sharing_client.LTIPlatformV13Api(api_client)

    try:
        # LTIPlatform auth token endpoint
        api_instance.auth_token_endpoint()
    except Exception as e:
        print("Exception when calling LTIPlatformV13Api->auth_token_endpoint: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK. |  -  |
**400** | Preconditions are not present. |  -  |
**401** | Authorization failed. |  -  |
**403** | Session user has insufficient rights to perform this operation. |  -  |
**404** | Ressources are not found. |  -  |
**500** | Fatal error occured. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **change_content**
> NodeEntry change_content(jwt, mimetype, version_comment=version_comment, file=file)

Custom edu-sharing endpoint to change content of node.

Change content of node.

### Example


```python
import edu_sharing_client
from edu_sharing_client.models.node_entry import NodeEntry
from edu_sharing_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://stable.demo.edu-sharing.net/edu-sharing/rest
# See configuration.py for a list of all supported configuration parameters.
configuration = edu_sharing_client.Configuration(
    host = "https://stable.demo.edu-sharing.net/edu-sharing/rest"
)


# Enter a context with an instance of the API client
with edu_sharing_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = edu_sharing_client.LTIPlatformV13Api(api_client)
    jwt = 'jwt_example' # str | jwt containing the claims appId, nodeId, user previously send with ResourceLinkRequest or DeeplinkRequest. Must be signed by tool
    mimetype = 'mimetype_example' # str | MIME-Type
    version_comment = 'version_comment_example' # str | comment, leave empty = no new version, otherwise new version is generated (optional)
    file = None # bytearray | file upload (optional)

    try:
        # Custom edu-sharing endpoint to change content of node.
        api_response = api_instance.change_content(jwt, mimetype, version_comment=version_comment, file=file)
        print("The response of LTIPlatformV13Api->change_content:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling LTIPlatformV13Api->change_content: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **jwt** | **str**| jwt containing the claims appId, nodeId, user previously send with ResourceLinkRequest or DeeplinkRequest. Must be signed by tool | 
 **mimetype** | **str**| MIME-Type | 
 **version_comment** | **str**| comment, leave empty &#x3D; no new version, otherwise new version is generated | [optional] 
 **file** | **bytearray**| file upload | [optional] 

### Return type

[**NodeEntry**](NodeEntry.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: multipart/form-data
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK. |  -  |
**400** | Preconditions are not present. |  -  |
**401** | Authorization failed. |  -  |
**403** | Session user has insufficient rights to perform this operation. |  -  |
**404** | Ressources are not found. |  -  |
**500** | Fatal error occured. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **convert_to_resourcelink**
> convert_to_resourcelink(node_id, app_id)

manual convertion of an io to an resource link without deeplinking

io conversion to resourcelink

### Example


```python
import edu_sharing_client
from edu_sharing_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://stable.demo.edu-sharing.net/edu-sharing/rest
# See configuration.py for a list of all supported configuration parameters.
configuration = edu_sharing_client.Configuration(
    host = "https://stable.demo.edu-sharing.net/edu-sharing/rest"
)


# Enter a context with an instance of the API client
with edu_sharing_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = edu_sharing_client.LTIPlatformV13Api(api_client)
    node_id = 'node_id_example' # str | nodeId
    app_id = 'app_id_example' # str | appId of a lti tool

    try:
        # manual convertion of an io to an resource link without deeplinking
        api_instance.convert_to_resourcelink(node_id, app_id)
    except Exception as e:
        print("Exception when calling LTIPlatformV13Api->convert_to_resourcelink: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **node_id** | **str**| nodeId | 
 **app_id** | **str**| appId of a lti tool | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK. |  -  |
**400** | Preconditions are not present. |  -  |
**401** | Authorization failed. |  -  |
**403** | Session user has insufficient rights to perform this operation. |  -  |
**404** | Ressources are not found. |  -  |
**409** | Duplicate Entity/Node conflict (Node with same name exists) |  -  |
**500** | Fatal error occured. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **deep_linking_response**
> str deep_linking_response(jwt)

receiving deeplink response messages.

deeplink response

### Example


```python
import edu_sharing_client
from edu_sharing_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://stable.demo.edu-sharing.net/edu-sharing/rest
# See configuration.py for a list of all supported configuration parameters.
configuration = edu_sharing_client.Configuration(
    host = "https://stable.demo.edu-sharing.net/edu-sharing/rest"
)


# Enter a context with an instance of the API client
with edu_sharing_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = edu_sharing_client.LTIPlatformV13Api(api_client)
    jwt = 'jwt_example' # str | JWT

    try:
        # receiving deeplink response messages.
        api_response = api_instance.deep_linking_response(jwt)
        print("The response of LTIPlatformV13Api->deep_linking_response:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling LTIPlatformV13Api->deep_linking_response: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **jwt** | **str**| JWT | 

### Return type

**str**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/x-www-form-urlencoded
 - **Accept**: text/html

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK. |  -  |
**400** | Preconditions are not present. |  -  |
**401** | Authorization failed. |  -  |
**403** | Session user has insufficient rights to perform this operation. |  -  |
**404** | Ressources are not found. |  -  |
**409** | Duplicate Entity/Node conflict (Node with same name exists) |  -  |
**500** | Fatal error occured. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **generate_login_initiation_form**
> str generate_login_initiation_form(app_id, parent_id, node_id=node_id)

generate a form used for Initiating Login from a Third Party. Use thes endpoint when starting a lti deeplink flow.

### Example


```python
import edu_sharing_client
from edu_sharing_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://stable.demo.edu-sharing.net/edu-sharing/rest
# See configuration.py for a list of all supported configuration parameters.
configuration = edu_sharing_client.Configuration(
    host = "https://stable.demo.edu-sharing.net/edu-sharing/rest"
)


# Enter a context with an instance of the API client
with edu_sharing_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = edu_sharing_client.LTIPlatformV13Api(api_client)
    app_id = 'app_id_example' # str | appId of the tool
    parent_id = 'parent_id_example' # str | the folder id the lti node will be created in. is required for lti deeplink.
    node_id = 'node_id_example' # str | the nodeId when tool has custom content option. (optional)

    try:
        # generate a form used for Initiating Login from a Third Party. Use thes endpoint when starting a lti deeplink flow.
        api_response = api_instance.generate_login_initiation_form(app_id, parent_id, node_id=node_id)
        print("The response of LTIPlatformV13Api->generate_login_initiation_form:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling LTIPlatformV13Api->generate_login_initiation_form: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **app_id** | **str**| appId of the tool | 
 **parent_id** | **str**| the folder id the lti node will be created in. is required for lti deeplink. | 
 **node_id** | **str**| the nodeId when tool has custom content option. | [optional] 

### Return type

**str**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/html

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK. |  -  |
**400** | Preconditions are not present. |  -  |
**401** | Authorization failed. |  -  |
**403** | Session user has insufficient rights to perform this operation. |  -  |
**404** | Ressources are not found. |  -  |
**500** | Fatal error occured. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **generate_login_initiation_form_resource_link**
> str generate_login_initiation_form_resource_link(node_id, edit_mode=edit_mode, version=version, launch_presentation=launch_presentation, jwt=jwt)

generate a form used for Initiating Login from a Third Party. Use thes endpoint when starting a lti resourcelink flow.

### Example


```python
import edu_sharing_client
from edu_sharing_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://stable.demo.edu-sharing.net/edu-sharing/rest
# See configuration.py for a list of all supported configuration parameters.
configuration = edu_sharing_client.Configuration(
    host = "https://stable.demo.edu-sharing.net/edu-sharing/rest"
)


# Enter a context with an instance of the API client
with edu_sharing_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = edu_sharing_client.LTIPlatformV13Api(api_client)
    node_id = 'node_id_example' # str | the nodeid of a node that contains a lti resourcelink. is required for lti resourcelink
    edit_mode = True # bool | for tools with content option, this param sends changeContentUrl (true) else contentUrl will be excluded (optional) (default to True)
    version = 'version_example' # str | the version. for tools with contentoption. (optional)
    launch_presentation = 'launch_presentation_example' # str | launchPresentation. how the resourcelink will be embedded. valid values: window,iframe (optional)
    jwt = 'jwt_example' # str | jwt for checking access in lms context (optional)

    try:
        # generate a form used for Initiating Login from a Third Party. Use thes endpoint when starting a lti resourcelink flow.
        api_response = api_instance.generate_login_initiation_form_resource_link(node_id, edit_mode=edit_mode, version=version, launch_presentation=launch_presentation, jwt=jwt)
        print("The response of LTIPlatformV13Api->generate_login_initiation_form_resource_link:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling LTIPlatformV13Api->generate_login_initiation_form_resource_link: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **node_id** | **str**| the nodeid of a node that contains a lti resourcelink. is required for lti resourcelink | 
 **edit_mode** | **bool**| for tools with content option, this param sends changeContentUrl (true) else contentUrl will be excluded | [optional] [default to True]
 **version** | **str**| the version. for tools with contentoption. | [optional] 
 **launch_presentation** | **str**| launchPresentation. how the resourcelink will be embedded. valid values: window,iframe | [optional] 
 **jwt** | **str**| jwt for checking access in lms context | [optional] 

### Return type

**str**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/html

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK. |  -  |
**400** | Preconditions are not present. |  -  |
**401** | Authorization failed. |  -  |
**403** | Session user has insufficient rights to perform this operation. |  -  |
**404** | Ressources are not found. |  -  |
**500** | Fatal error occured. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_content**
> str get_content(jwt)

Custom edu-sharing endpoint to get content of node.

Get content of node.

### Example


```python
import edu_sharing_client
from edu_sharing_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://stable.demo.edu-sharing.net/edu-sharing/rest
# See configuration.py for a list of all supported configuration parameters.
configuration = edu_sharing_client.Configuration(
    host = "https://stable.demo.edu-sharing.net/edu-sharing/rest"
)


# Enter a context with an instance of the API client
with edu_sharing_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = edu_sharing_client.LTIPlatformV13Api(api_client)
    jwt = 'jwt_example' # str | jwt containing the claims appId, nodeId, user previously send with ResourceLinkRequest or DeeplinkRequest. Must be signed by tool

    try:
        # Custom edu-sharing endpoint to get content of node.
        api_response = api_instance.get_content(jwt)
        print("The response of LTIPlatformV13Api->get_content:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling LTIPlatformV13Api->get_content: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **jwt** | **str**| jwt containing the claims appId, nodeId, user previously send with ResourceLinkRequest or DeeplinkRequest. Must be signed by tool | 

### Return type

**str**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: */*, text/html

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK. |  -  |
**400** | Preconditions are not present. |  -  |
**401** | Authorization failed. |  -  |
**403** | Session user has insufficient rights to perform this operation. |  -  |
**404** | Ressources are not found. |  -  |
**500** | Fatal error occured. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **manual_registration**
> manual_registration(manual_registration_data)

manual registration endpoint for registration of tools.

tool registration

### Example


```python
import edu_sharing_client
from edu_sharing_client.models.manual_registration_data import ManualRegistrationData
from edu_sharing_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://stable.demo.edu-sharing.net/edu-sharing/rest
# See configuration.py for a list of all supported configuration parameters.
configuration = edu_sharing_client.Configuration(
    host = "https://stable.demo.edu-sharing.net/edu-sharing/rest"
)


# Enter a context with an instance of the API client
with edu_sharing_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = edu_sharing_client.LTIPlatformV13Api(api_client)
    manual_registration_data = edu_sharing_client.ManualRegistrationData() # ManualRegistrationData | registrationData

    try:
        # manual registration endpoint for registration of tools.
        api_instance.manual_registration(manual_registration_data)
    except Exception as e:
        print("Exception when calling LTIPlatformV13Api->manual_registration: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **manual_registration_data** | [**ManualRegistrationData**](ManualRegistrationData.md)| registrationData | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK. |  -  |
**400** | Preconditions are not present. |  -  |
**401** | Authorization failed. |  -  |
**403** | Session user has insufficient rights to perform this operation. |  -  |
**404** | Ressources are not found. |  -  |
**409** | Duplicate Entity/Node conflict (Node with same name exists) |  -  |
**500** | Fatal error occured. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **open_id_registration**
> OpenIdRegistrationResult open_id_registration(body)

registration endpoint the tool uses to register at platform.

tool registration

### Example


```python
import edu_sharing_client
from edu_sharing_client.models.open_id_registration_result import OpenIdRegistrationResult
from edu_sharing_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://stable.demo.edu-sharing.net/edu-sharing/rest
# See configuration.py for a list of all supported configuration parameters.
configuration = edu_sharing_client.Configuration(
    host = "https://stable.demo.edu-sharing.net/edu-sharing/rest"
)


# Enter a context with an instance of the API client
with edu_sharing_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = edu_sharing_client.LTIPlatformV13Api(api_client)
    body = 'body_example' # str | registrationpayload

    try:
        # registration endpoint the tool uses to register at platform.
        api_response = api_instance.open_id_registration(body)
        print("The response of LTIPlatformV13Api->open_id_registration:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling LTIPlatformV13Api->open_id_registration: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | **str**| registrationpayload | 

### Return type

[**OpenIdRegistrationResult**](OpenIdRegistrationResult.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK. |  -  |
**400** | Preconditions are not present. |  -  |
**401** | Authorization failed. |  -  |
**403** | Session user has insufficient rights to perform this operation. |  -  |
**404** | Ressources are not found. |  -  |
**409** | Duplicate Entity/Node conflict (Node with same name exists) |  -  |
**500** | Fatal error occured. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **openid_configuration**
> OpenIdConfiguration openid_configuration()

LTIPlatform openid configuration

### Example


```python
import edu_sharing_client
from edu_sharing_client.models.open_id_configuration import OpenIdConfiguration
from edu_sharing_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://stable.demo.edu-sharing.net/edu-sharing/rest
# See configuration.py for a list of all supported configuration parameters.
configuration = edu_sharing_client.Configuration(
    host = "https://stable.demo.edu-sharing.net/edu-sharing/rest"
)


# Enter a context with an instance of the API client
with edu_sharing_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = edu_sharing_client.LTIPlatformV13Api(api_client)

    try:
        # LTIPlatform openid configuration
        api_response = api_instance.openid_configuration()
        print("The response of LTIPlatformV13Api->openid_configuration:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling LTIPlatformV13Api->openid_configuration: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**OpenIdConfiguration**](OpenIdConfiguration.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK. |  -  |
**400** | Preconditions are not present. |  -  |
**401** | Authorization failed. |  -  |
**403** | Session user has insufficient rights to perform this operation. |  -  |
**404** | Ressources are not found. |  -  |
**500** | Fatal error occured. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **start_dynamic_registration**
> str start_dynamic_registration(url)

starts lti dynamic registration.

start dynmic registration

### Example


```python
import edu_sharing_client
from edu_sharing_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://stable.demo.edu-sharing.net/edu-sharing/rest
# See configuration.py for a list of all supported configuration parameters.
configuration = edu_sharing_client.Configuration(
    host = "https://stable.demo.edu-sharing.net/edu-sharing/rest"
)


# Enter a context with an instance of the API client
with edu_sharing_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = edu_sharing_client.LTIPlatformV13Api(api_client)
    url = 'url_example' # str | url

    try:
        # starts lti dynamic registration.
        api_response = api_instance.start_dynamic_registration(url)
        print("The response of LTIPlatformV13Api->start_dynamic_registration:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling LTIPlatformV13Api->start_dynamic_registration: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **url** | **str**| url | 

### Return type

**str**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/x-www-form-urlencoded
 - **Accept**: text/html

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK. |  -  |
**400** | Preconditions are not present. |  -  |
**401** | Authorization failed. |  -  |
**403** | Session user has insufficient rights to perform this operation. |  -  |
**404** | Ressources are not found. |  -  |
**500** | Fatal error occured. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **start_dynamic_registration_get**
> str start_dynamic_registration_get(url)

starts lti dynamic registration.

start dynmic registration

### Example


```python
import edu_sharing_client
from edu_sharing_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://stable.demo.edu-sharing.net/edu-sharing/rest
# See configuration.py for a list of all supported configuration parameters.
configuration = edu_sharing_client.Configuration(
    host = "https://stable.demo.edu-sharing.net/edu-sharing/rest"
)


# Enter a context with an instance of the API client
with edu_sharing_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = edu_sharing_client.LTIPlatformV13Api(api_client)
    url = 'url_example' # str | url

    try:
        # starts lti dynamic registration.
        api_response = api_instance.start_dynamic_registration_get(url)
        print("The response of LTIPlatformV13Api->start_dynamic_registration_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling LTIPlatformV13Api->start_dynamic_registration_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **url** | **str**| url | 

### Return type

**str**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/html

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK. |  -  |
**400** | Preconditions are not present. |  -  |
**401** | Authorization failed. |  -  |
**403** | Session user has insufficient rights to perform this operation. |  -  |
**404** | Ressources are not found. |  -  |
**500** | Fatal error occured. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **test_token**
> str test_token(request_body)

test creates a token signed with homeapp.

test token.

### Example


```python
import edu_sharing_client
from edu_sharing_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://stable.demo.edu-sharing.net/edu-sharing/rest
# See configuration.py for a list of all supported configuration parameters.
configuration = edu_sharing_client.Configuration(
    host = "https://stable.demo.edu-sharing.net/edu-sharing/rest"
)


# Enter a context with an instance of the API client
with edu_sharing_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = edu_sharing_client.LTIPlatformV13Api(api_client)
    request_body = {'key': 'request_body_example'} # Dict[str, str] | properties

    try:
        # test creates a token signed with homeapp.
        api_response = api_instance.test_token(request_body)
        print("The response of LTIPlatformV13Api->test_token:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling LTIPlatformV13Api->test_token: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **request_body** | [**Dict[str, str]**](str.md)| properties | 

### Return type

**str**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK. |  -  |
**400** | Preconditions are not present. |  -  |
**401** | Authorization failed. |  -  |
**403** | Session user has insufficient rights to perform this operation. |  -  |
**404** | Ressources are not found. |  -  |
**409** | Duplicate Entity/Node conflict (Node with same name exists) |  -  |
**500** | Fatal error occured. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **tools**
> Tools tools()

List of tools registered

### Example


```python
import edu_sharing_client
from edu_sharing_client.models.tools import Tools
from edu_sharing_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://stable.demo.edu-sharing.net/edu-sharing/rest
# See configuration.py for a list of all supported configuration parameters.
configuration = edu_sharing_client.Configuration(
    host = "https://stable.demo.edu-sharing.net/edu-sharing/rest"
)


# Enter a context with an instance of the API client
with edu_sharing_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = edu_sharing_client.LTIPlatformV13Api(api_client)

    try:
        # List of tools registered
        api_response = api_instance.tools()
        print("The response of LTIPlatformV13Api->tools:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling LTIPlatformV13Api->tools: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**Tools**](Tools.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK. |  -  |
**400** | Preconditions are not present. |  -  |
**401** | Authorization failed. |  -  |
**403** | Session user has insufficient rights to perform this operation. |  -  |
**404** | Ressources are not found. |  -  |
**500** | Fatal error occured. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

