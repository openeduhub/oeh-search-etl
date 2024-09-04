# edu_sharing_client.LTIV13Api

All URIs are relative to *https://stable.demo.edu-sharing.net/edu-sharing/rest*

Method | HTTP request | Description
------------- | ------------- | -------------
[**generate_deep_linking_response**](LTIV13Api.md#generate_deep_linking_response) | **GET** /lti/v13/generateDeepLinkingResponse | generate DeepLinkingResponse
[**get_details_snippet**](LTIV13Api.md#get_details_snippet) | **GET** /lti/v13/details/{repository}/{node} | get a html snippet containing a rendered version of a node. this method can be called from a platform as a xhr request instead of doing the resource link flow
[**jwks_uri**](LTIV13Api.md#jwks_uri) | **GET** /lti/v13/jwks | LTI - returns repository JSON Web Key Sets
[**login_initiations**](LTIV13Api.md#login_initiations) | **POST** /lti/v13/oidc/login_initiations | lti authentication process preparation.
[**login_initiations_get**](LTIV13Api.md#login_initiations_get) | **GET** /lti/v13/oidc/login_initiations | lti authentication process preparation.
[**lti**](LTIV13Api.md#lti) | **POST** /lti/v13/lti13 | lti tool redirect.
[**lti_registration_dynamic**](LTIV13Api.md#lti_registration_dynamic) | **GET** /lti/v13/registration/dynamic/{token} | LTI Dynamic Registration - Initiate registration
[**lti_registration_url**](LTIV13Api.md#lti_registration_url) | **GET** /lti/v13/registration/url | LTI Dynamic Registration - generates url for platform
[**lti_target**](LTIV13Api.md#lti_target) | **POST** /lti/v13/lti13/{nodeId} | lti tool resource link target.
[**register_by_type**](LTIV13Api.md#register_by_type) | **POST** /lti/v13/registration/{type} | register LTI platform
[**register_test**](LTIV13Api.md#register_test) | **POST** /lti/v13/registration/static | register LTI platform
[**remove_lti_registration_url**](LTIV13Api.md#remove_lti_registration_url) | **DELETE** /lti/v13/registration/url/{token} | LTI Dynamic Regitration - delete url


# **generate_deep_linking_response**
> NodeLTIDeepLink generate_deep_linking_response(node_ids)

generate DeepLinkingResponse

### Example


```python
import edu_sharing_client
from edu_sharing_client.models.node_lti_deep_link import NodeLTIDeepLink
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
    api_instance = edu_sharing_client.LTIV13Api(api_client)
    node_ids = ['node_ids_example'] # List[str] | selected node id's

    try:
        # generate DeepLinkingResponse
        api_response = api_instance.generate_deep_linking_response(node_ids)
        print("The response of LTIV13Api->generate_deep_linking_response:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling LTIV13Api->generate_deep_linking_response: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **node_ids** | [**List[str]**](str.md)| selected node id&#39;s | 

### Return type

[**NodeLTIDeepLink**](NodeLTIDeepLink.md)

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

# **get_details_snippet**
> RenderingDetailsEntry get_details_snippet(repository, node, jwt, version=version, display_mode=display_mode)

get a html snippet containing a rendered version of a node. this method can be called from a platform as a xhr request instead of doing the resource link flow

get rendered html snippet for a node.

### Example


```python
import edu_sharing_client
from edu_sharing_client.models.rendering_details_entry import RenderingDetailsEntry
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
    api_instance = edu_sharing_client.LTIV13Api(api_client)
    repository = '-home-' # str | ID of repository (or \"-home-\" for home repository) (default to '-home-')
    node = 'node_example' # str | ID of node
    jwt = 'jwt_example' # str | jwt containing the claims aud (clientId of platform), deploymentId and a token. must be signed by platform
    version = 'version_example' # str | version of node (optional)
    display_mode = 'display_mode_example' # str | Rendering displayMode (optional)

    try:
        # get a html snippet containing a rendered version of a node. this method can be called from a platform as a xhr request instead of doing the resource link flow
        api_response = api_instance.get_details_snippet(repository, node, jwt, version=version, display_mode=display_mode)
        print("The response of LTIV13Api->get_details_snippet:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling LTIV13Api->get_details_snippet: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **repository** | **str**| ID of repository (or \&quot;-home-\&quot; for home repository) | [default to &#39;-home-&#39;]
 **node** | **str**| ID of node | 
 **jwt** | **str**| jwt containing the claims aud (clientId of platform), deploymentId and a token. must be signed by platform | 
 **version** | **str**| version of node | [optional] 
 **display_mode** | **str**| Rendering displayMode | [optional] 

### Return type

[**RenderingDetailsEntry**](RenderingDetailsEntry.md)

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

# **jwks_uri**
> RegistrationUrl jwks_uri()

LTI - returns repository JSON Web Key Sets

### Example


```python
import edu_sharing_client
from edu_sharing_client.models.registration_url import RegistrationUrl
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
    api_instance = edu_sharing_client.LTIV13Api(api_client)

    try:
        # LTI - returns repository JSON Web Key Sets
        api_response = api_instance.jwks_uri()
        print("The response of LTIV13Api->jwks_uri:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling LTIV13Api->jwks_uri: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**RegistrationUrl**](RegistrationUrl.md)

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

# **login_initiations**
> str login_initiations(iss, target_link_uri, client_id=client_id, login_hint=login_hint, lti_message_hint=lti_message_hint, lti_deployment_id=lti_deployment_id)

lti authentication process preparation.

preflight phase. prepares lti authentication process. checks it issuer is valid

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
    api_instance = edu_sharing_client.LTIV13Api(api_client)
    iss = 'iss_example' # str | Issuer of the request, will be validated
    target_link_uri = 'target_link_uri_example' # str | target url of platform at the end of the flow
    client_id = 'client_id_example' # str | Id of the issuer (optional)
    login_hint = 'login_hint_example' # str | context information of the platform (optional)
    lti_message_hint = 'lti_message_hint_example' # str | additional context information of the platform (optional)
    lti_deployment_id = 'lti_deployment_id_example' # str | A can have multiple deployments in a platform (optional)

    try:
        # lti authentication process preparation.
        api_response = api_instance.login_initiations(iss, target_link_uri, client_id=client_id, login_hint=login_hint, lti_message_hint=lti_message_hint, lti_deployment_id=lti_deployment_id)
        print("The response of LTIV13Api->login_initiations:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling LTIV13Api->login_initiations: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **iss** | **str**| Issuer of the request, will be validated | 
 **target_link_uri** | **str**| target url of platform at the end of the flow | 
 **client_id** | **str**| Id of the issuer | [optional] 
 **login_hint** | **str**| context information of the platform | [optional] 
 **lti_message_hint** | **str**| additional context information of the platform | [optional] 
 **lti_deployment_id** | **str**| A can have multiple deployments in a platform | [optional] 

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

# **login_initiations_get**
> str login_initiations_get(iss, target_link_uri, client_id=client_id, login_hint=login_hint, lti_message_hint=lti_message_hint, lti_deployment_id=lti_deployment_id)

lti authentication process preparation.

preflight phase. prepares lti authentication process. checks it issuer is valid

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
    api_instance = edu_sharing_client.LTIV13Api(api_client)
    iss = 'iss_example' # str | Issuer of the request, will be validated
    target_link_uri = 'target_link_uri_example' # str | target url of platform at the end of the flow
    client_id = 'client_id_example' # str | Id of the issuer (optional)
    login_hint = 'login_hint_example' # str | context information of the platform (optional)
    lti_message_hint = 'lti_message_hint_example' # str | additional context information of the platform (optional)
    lti_deployment_id = 'lti_deployment_id_example' # str | A can have multiple deployments in a platform (optional)

    try:
        # lti authentication process preparation.
        api_response = api_instance.login_initiations_get(iss, target_link_uri, client_id=client_id, login_hint=login_hint, lti_message_hint=lti_message_hint, lti_deployment_id=lti_deployment_id)
        print("The response of LTIV13Api->login_initiations_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling LTIV13Api->login_initiations_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **iss** | **str**| Issuer of the request, will be validated | 
 **target_link_uri** | **str**| target url of platform at the end of the flow | 
 **client_id** | **str**| Id of the issuer | [optional] 
 **login_hint** | **str**| context information of the platform | [optional] 
 **lti_message_hint** | **str**| additional context information of the platform | [optional] 
 **lti_deployment_id** | **str**| A can have multiple deployments in a platform | [optional] 

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

# **lti**
> str lti(id_token, state)

lti tool redirect.

lti tool redirect

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
    api_instance = edu_sharing_client.LTIV13Api(api_client)
    id_token = 'id_token_example' # str | Issuer of the request, will be validated
    state = 'state_example' # str | Issuer of the request, will be validated

    try:
        # lti tool redirect.
        api_response = api_instance.lti(id_token, state)
        print("The response of LTIV13Api->lti:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling LTIV13Api->lti: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id_token** | **str**| Issuer of the request, will be validated | 
 **state** | **str**| Issuer of the request, will be validated | 

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

# **lti_registration_dynamic**
> str lti_registration_dynamic(openid_configuration, token, registration_token=registration_token)

LTI Dynamic Registration - Initiate registration

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
    api_instance = edu_sharing_client.LTIV13Api(api_client)
    openid_configuration = 'openid_configuration_example' # str | the endpoint to the open id configuration to be used for this registration
    token = 'token_example' # str | one time usage token which is autogenerated with the url in edu-sharing admin gui.
    registration_token = 'registration_token_example' # str | the registration access token. If present, it must be used as the access token by the tool when making the registration request to the registration endpoint exposed in the openid configuration. (optional)

    try:
        # LTI Dynamic Registration - Initiate registration
        api_response = api_instance.lti_registration_dynamic(openid_configuration, token, registration_token=registration_token)
        print("The response of LTIV13Api->lti_registration_dynamic:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling LTIV13Api->lti_registration_dynamic: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **openid_configuration** | **str**| the endpoint to the open id configuration to be used for this registration | 
 **token** | **str**| one time usage token which is autogenerated with the url in edu-sharing admin gui. | 
 **registration_token** | **str**| the registration access token. If present, it must be used as the access token by the tool when making the registration request to the registration endpoint exposed in the openid configuration. | [optional] 

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

# **lti_registration_url**
> DynamicRegistrationTokens lti_registration_url(generate)

LTI Dynamic Registration - generates url for platform

### Example


```python
import edu_sharing_client
from edu_sharing_client.models.dynamic_registration_tokens import DynamicRegistrationTokens
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
    api_instance = edu_sharing_client.LTIV13Api(api_client)
    generate = False # bool | if to add a ne url to the list (default to False)

    try:
        # LTI Dynamic Registration - generates url for platform
        api_response = api_instance.lti_registration_url(generate)
        print("The response of LTIV13Api->lti_registration_url:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling LTIV13Api->lti_registration_url: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **generate** | **bool**| if to add a ne url to the list | [default to False]

### Return type

[**DynamicRegistrationTokens**](DynamicRegistrationTokens.md)

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

# **lti_target**
> str lti_target(node_id, id_token, state)

lti tool resource link target.

used by some platforms for direct (without oidc login_init) launch requests

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
    api_instance = edu_sharing_client.LTIV13Api(api_client)
    node_id = 'node_id_example' # str | edu-sharing node id
    id_token = 'id_token_example' # str | Issuer of the request, will be validated
    state = 'state_example' # str | Issuer of the request, will be validated

    try:
        # lti tool resource link target.
        api_response = api_instance.lti_target(node_id, id_token, state)
        print("The response of LTIV13Api->lti_target:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling LTIV13Api->lti_target: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **node_id** | **str**| edu-sharing node id | 
 **id_token** | **str**| Issuer of the request, will be validated | 
 **state** | **str**| Issuer of the request, will be validated | 

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

# **register_by_type**
> register_by_type(type, base_url, client_id=client_id, deployment_id=deployment_id)

register LTI platform

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
    api_instance = edu_sharing_client.LTIV13Api(api_client)
    type = 'type_example' # str | lti platform typ i.e. moodle
    base_url = 'base_url_example' # str | base url i.e. http://localhost/moodle used as platformId
    client_id = 'client_id_example' # str | client id (optional)
    deployment_id = 'deployment_id_example' # str | deployment id (optional)

    try:
        # register LTI platform
        api_instance.register_by_type(type, base_url, client_id=client_id, deployment_id=deployment_id)
    except Exception as e:
        print("Exception when calling LTIV13Api->register_by_type: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **type** | **str**| lti platform typ i.e. moodle | 
 **base_url** | **str**| base url i.e. http://localhost/moodle used as platformId | 
 **client_id** | **str**| client id | [optional] 
 **deployment_id** | **str**| deployment id | [optional] 

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

# **register_test**
> register_test(platform_id, client_id, deployment_id, authentication_request_url, keyset_url, auth_token_url, key_id=key_id)

register LTI platform

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
    api_instance = edu_sharing_client.LTIV13Api(api_client)
    platform_id = 'platform_id_example' # str | the issuer
    client_id = 'client_id_example' # str | client id
    deployment_id = 'deployment_id_example' # str | deployment id
    authentication_request_url = 'authentication_request_url_example' # str | oidc endpoint, authentication request url
    keyset_url = 'keyset_url_example' # str | jwks endpoint, keyset url
    auth_token_url = 'auth_token_url_example' # str | auth token url
    key_id = 'key_id_example' # str | jwks key id (optional)

    try:
        # register LTI platform
        api_instance.register_test(platform_id, client_id, deployment_id, authentication_request_url, keyset_url, auth_token_url, key_id=key_id)
    except Exception as e:
        print("Exception when calling LTIV13Api->register_test: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **platform_id** | **str**| the issuer | 
 **client_id** | **str**| client id | 
 **deployment_id** | **str**| deployment id | 
 **authentication_request_url** | **str**| oidc endpoint, authentication request url | 
 **keyset_url** | **str**| jwks endpoint, keyset url | 
 **auth_token_url** | **str**| auth token url | 
 **key_id** | **str**| jwks key id | [optional] 

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

# **remove_lti_registration_url**
> DynamicRegistrationTokens remove_lti_registration_url(token)

LTI Dynamic Regitration - delete url

### Example


```python
import edu_sharing_client
from edu_sharing_client.models.dynamic_registration_tokens import DynamicRegistrationTokens
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
    api_instance = edu_sharing_client.LTIV13Api(api_client)
    token = 'token_example' # str | the token of the link you have to remove

    try:
        # LTI Dynamic Regitration - delete url
        api_response = api_instance.remove_lti_registration_url(token)
        print("The response of LTIV13Api->remove_lti_registration_url:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling LTIV13Api->remove_lti_registration_url: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **token** | **str**| the token of the link you have to remove | 

### Return type

[**DynamicRegistrationTokens**](DynamicRegistrationTokens.md)

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

