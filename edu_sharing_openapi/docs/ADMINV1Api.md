# edu_sharing_client.ADMINV1Api

All URIs are relative to *https://stable.demo.edu-sharing.net/edu-sharing/rest*

Method | HTTP request | Description
------------- | ------------- | -------------
[**add_application**](ADMINV1Api.md#add_application) | **PUT** /admin/v1/applications/xml | register/add an application via xml file
[**add_application1**](ADMINV1Api.md#add_application1) | **PUT** /admin/v1/applications | register/add an application
[**add_toolpermission**](ADMINV1Api.md#add_toolpermission) | **POST** /admin/v1/toolpermissions/add/{name} | add a new toolpermissions
[**apply_template**](ADMINV1Api.md#apply_template) | **POST** /admin/v1/applyTemplate | apply a folder template
[**cancel_job**](ADMINV1Api.md#cancel_job) | **DELETE** /admin/v1/jobs/{job} | cancel a running job
[**change_logging**](ADMINV1Api.md#change_logging) | **POST** /admin/v1/log/config | Change the loglevel for classes at runtime.
[**clear_cache**](ADMINV1Api.md#clear_cache) | **POST** /admin/v1/cache/clearCache | clear cache
[**create_preview**](ADMINV1Api.md#create_preview) | **GET** /admin/v1/nodes/preview/{node} | create preview.
[**delete_person**](ADMINV1Api.md#delete_person) | **PUT** /admin/v1/deletePersons | delete persons
[**export_by_lucene**](ADMINV1Api.md#export_by_lucene) | **GET** /admin/v1/lucene/export | Search for custom lucene query and choose specific properties to load
[**export_lom**](ADMINV1Api.md#export_lom) | **GET** /admin/v1/export/lom | Export Nodes with LOM Metadata Format
[**get_all_jobs**](ADMINV1Api.md#get_all_jobs) | **GET** /admin/v1/jobs/all | get all available jobs
[**get_all_toolpermissions**](ADMINV1Api.md#get_all_toolpermissions) | **GET** /admin/v1/toolpermissions/{authority} | get all toolpermissions for an authority
[**get_application_xml**](ADMINV1Api.md#get_application_xml) | **GET** /admin/v1/applications/{xml} | list any xml properties (like from homeApplication.properties.xml)
[**get_applications**](ADMINV1Api.md#get_applications) | **GET** /admin/v1/applications | list applications
[**get_cache_entries**](ADMINV1Api.md#get_cache_entries) | **GET** /admin/v1/cache/cacheEntries/{id} | Get entries of a cache
[**get_cache_info**](ADMINV1Api.md#get_cache_info) | **GET** /admin/v1/cache/cacheInfo/{id} | Get information about a cache
[**get_catalina_out**](ADMINV1Api.md#get_catalina_out) | **GET** /admin/v1/catalina | Get last info from catalina out
[**get_cluster**](ADMINV1Api.md#get_cluster) | **GET** /admin/v1/clusterInfo | Get information about the Cluster
[**get_clusters**](ADMINV1Api.md#get_clusters) | **GET** /admin/v1/clusterInfos | Get information about the Cluster
[**get_config**](ADMINV1Api.md#get_config) | **GET** /admin/v1/repositoryConfig | get the repository config object
[**get_config_file**](ADMINV1Api.md#get_config_file) | **GET** /admin/v1/configFile | get a base system config file (e.g. edu-sharing.conf)
[**get_enabled_plugins**](ADMINV1Api.md#get_enabled_plugins) | **GET** /admin/v1/plugins | get enabled system plugins
[**get_global_groups**](ADMINV1Api.md#get_global_groups) | **GET** /admin/v1/globalGroups | Get global groups
[**get_jobs**](ADMINV1Api.md#get_jobs) | **GET** /admin/v1/jobs | get all running jobs
[**get_lightbend_config**](ADMINV1Api.md#get_lightbend_config) | **GET** /admin/v1/config/merged | 
[**get_logging_runtime**](ADMINV1Api.md#get_logging_runtime) | **GET** /admin/v1/log/config | get the logger config
[**get_oai_classes**](ADMINV1Api.md#get_oai_classes) | **GET** /admin/v1/import/oai/classes | Get OAI class names
[**get_property_to_mds**](ADMINV1Api.md#get_property_to_mds) | **GET** /admin/v1/propertyToMds | Get a Mds Valuespace for all values of the given properties
[**get_statistics**](ADMINV1Api.md#get_statistics) | **GET** /admin/v1/statistics | get statistics
[**get_version**](ADMINV1Api.md#get_version) | **GET** /admin/v1/version | get detailed version information
[**import_collections**](ADMINV1Api.md#import_collections) | **POST** /admin/v1/import/collections | import collections via a xml file
[**import_excel**](ADMINV1Api.md#import_excel) | **POST** /admin/v1/import/excel | Import excel data
[**import_oai**](ADMINV1Api.md#import_oai) | **POST** /admin/v1/import/oai | Import oai data
[**import_oai_xml**](ADMINV1Api.md#import_oai_xml) | **POST** /admin/v1/import/oai/xml | Import single xml via oai (for testing)
[**refresh_app_info**](ADMINV1Api.md#refresh_app_info) | **POST** /admin/v1/refreshAppInfo | refresh app info
[**refresh_cache**](ADMINV1Api.md#refresh_cache) | **POST** /admin/v1/import/refreshCache/{folder} | Refresh cache
[**refresh_edu_group_cache**](ADMINV1Api.md#refresh_edu_group_cache) | **POST** /admin/v1/cache/refreshEduGroupCache | Refresh the Edu Group Cache
[**remove_application**](ADMINV1Api.md#remove_application) | **DELETE** /admin/v1/applications/{id} | remove an application
[**remove_cache_entry**](ADMINV1Api.md#remove_cache_entry) | **POST** /admin/v1/cache/removeCacheEntry | remove cache entry
[**remove_oai_imports**](ADMINV1Api.md#remove_oai_imports) | **DELETE** /admin/v1/import/oai | Remove deleted imports
[**search_by_elastic_dsl**](ADMINV1Api.md#search_by_elastic_dsl) | **GET** /admin/v1/elastic | Search for custom elastic DSL query
[**search_by_lucene**](ADMINV1Api.md#search_by_lucene) | **GET** /admin/v1/lucene | Search for custom lucene query
[**server_update_list**](ADMINV1Api.md#server_update_list) | **GET** /admin/v1/serverUpdate/list | list available update tasks
[**server_update_list1**](ADMINV1Api.md#server_update_list1) | **POST** /admin/v1/serverUpdate/run/{id} | Run an update tasks
[**set_config**](ADMINV1Api.md#set_config) | **PUT** /admin/v1/repositoryConfig | set/update the repository config object
[**set_toolpermissions**](ADMINV1Api.md#set_toolpermissions) | **PUT** /admin/v1/toolpermissions/{authority} | set toolpermissions for an authority
[**start_job**](ADMINV1Api.md#start_job) | **POST** /admin/v1/job/{jobClass} | Start a Job.
[**start_job_sync**](ADMINV1Api.md#start_job_sync) | **POST** /admin/v1/job/{jobClass}/sync | Start a Job.
[**switch_authority**](ADMINV1Api.md#switch_authority) | **POST** /admin/v1/authenticate/{authorityName} | switch the session to a known authority name
[**test_mail**](ADMINV1Api.md#test_mail) | **POST** /admin/v1/mail/{receiver}/{template} | Test a mail template
[**update_application_xml**](ADMINV1Api.md#update_application_xml) | **PUT** /admin/v1/applications/{xml} | edit any properties xml (like homeApplication.properties.xml)
[**update_config_file**](ADMINV1Api.md#update_config_file) | **PUT** /admin/v1/configFile | update a base system config file (e.g. edu-sharing.conf)
[**upload_temp**](ADMINV1Api.md#upload_temp) | **PUT** /admin/v1/upload/temp/{name} | Upload a file


# **add_application**
> str add_application(xml)

register/add an application via xml file

register the xml file provided.

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
    api_instance = edu_sharing_client.ADMINV1Api(api_client)
    xml = None # object | XML file for app to register

    try:
        # register/add an application via xml file
        api_response = api_instance.add_application(xml)
        print("The response of ADMINV1Api->add_application:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ADMINV1Api->add_application: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **xml** | [**object**](object.md)| XML file for app to register | 

### Return type

**str**

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

# **add_application1**
> str add_application1(url)

register/add an application

register the specified application.

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
    api_instance = edu_sharing_client.ADMINV1Api(api_client)
    url = 'url_example' # str | Remote application metadata url

    try:
        # register/add an application
        api_response = api_instance.add_application1(url)
        print("The response of ADMINV1Api->add_application1:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ADMINV1Api->add_application1: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **url** | **str**| Remote application metadata url | 

### Return type

**str**

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

# **add_toolpermission**
> Node add_toolpermission(name)

add a new toolpermissions

### Example


```python
import edu_sharing_client
from edu_sharing_client.models.node import Node
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
    api_instance = edu_sharing_client.ADMINV1Api(api_client)
    name = 'name_example' # str | Name/ID of toolpermission

    try:
        # add a new toolpermissions
        api_response = api_instance.add_toolpermission(name)
        print("The response of ADMINV1Api->add_toolpermission:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ADMINV1Api->add_toolpermission: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **name** | **str**| Name/ID of toolpermission | 

### Return type

[**Node**](Node.md)

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

# **apply_template**
> apply_template(template, group, folder=folder)

apply a folder template

apply a folder template.

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
    api_instance = edu_sharing_client.ADMINV1Api(api_client)
    template = 'template_example' # str | Template Filename
    group = 'group_example' # str | Group name (authority name)
    folder = 'folder_example' # str | Folder name (optional)

    try:
        # apply a folder template
        api_instance.apply_template(template, group, folder=folder)
    except Exception as e:
        print("Exception when calling ADMINV1Api->apply_template: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **template** | **str**| Template Filename | 
 **group** | **str**| Group name (authority name) | 
 **folder** | **str**| Folder name | [optional] 

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

# **cancel_job**
> cancel_job(job, force=force)

cancel a running job

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
    api_instance = edu_sharing_client.ADMINV1Api(api_client)
    job = 'job_example' # str | 
    force = True # bool |  (optional)

    try:
        # cancel a running job
        api_instance.cancel_job(job, force=force)
    except Exception as e:
        print("Exception when calling ADMINV1Api->cancel_job: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **job** | **str**|  | 
 **force** | **bool**|  | [optional] 

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

# **change_logging**
> change_logging(name, loglevel, appender=appender)

Change the loglevel for classes at runtime.

Root appenders are used. Check the appender treshold.

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
    api_instance = edu_sharing_client.ADMINV1Api(api_client)
    name = 'name_example' # str | name
    loglevel = 'loglevel_example' # str | loglevel
    appender = 'ConsoleAppender' # str | appender (optional) (default to 'ConsoleAppender')

    try:
        # Change the loglevel for classes at runtime.
        api_instance.change_logging(name, loglevel, appender=appender)
    except Exception as e:
        print("Exception when calling ADMINV1Api->change_logging: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **name** | **str**| name | 
 **loglevel** | **str**| loglevel | 
 **appender** | **str**| appender | [optional] [default to &#39;ConsoleAppender&#39;]

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

# **clear_cache**
> clear_cache(bean=bean)

clear cache

clear cache

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
    api_instance = edu_sharing_client.ADMINV1Api(api_client)
    bean = 'bean_example' # str | bean (optional)

    try:
        # clear cache
        api_instance.clear_cache(bean=bean)
    except Exception as e:
        print("Exception when calling ADMINV1Api->clear_cache: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **bean** | **str**| bean | [optional] 

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

# **create_preview**
> create_preview(node)

create preview.

create preview.

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
    api_instance = edu_sharing_client.ADMINV1Api(api_client)
    node = 'node_example' # str | ID of node

    try:
        # create preview.
        api_instance.create_preview(node)
    except Exception as e:
        print("Exception when calling ADMINV1Api->create_preview: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **node** | **str**| ID of node | 

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

# **delete_person**
> PersonReport delete_person(username, person_delete_options=person_delete_options)

delete persons

delete the given persons. Their status must be set to \"todelete\"

### Example


```python
import edu_sharing_client
from edu_sharing_client.models.person_delete_options import PersonDeleteOptions
from edu_sharing_client.models.person_report import PersonReport
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
    api_instance = edu_sharing_client.ADMINV1Api(api_client)
    username = ['username_example'] # List[str] | names of the users to delete
    person_delete_options = edu_sharing_client.PersonDeleteOptions() # PersonDeleteOptions | options object what and how to delete user contents (optional)

    try:
        # delete persons
        api_response = api_instance.delete_person(username, person_delete_options=person_delete_options)
        print("The response of ADMINV1Api->delete_person:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ADMINV1Api->delete_person: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **username** | [**List[str]**](str.md)| names of the users to delete | 
 **person_delete_options** | [**PersonDeleteOptions**](PersonDeleteOptions.md)| options object what and how to delete user contents | [optional] 

### Return type

[**PersonReport**](PersonReport.md)

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
**500** | Fatal error occured. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **export_by_lucene**
> str export_by_lucene(query=query, sort_properties=sort_properties, sort_ascending=sort_ascending, properties=properties, store=store, authority_scope=authority_scope)

Search for custom lucene query and choose specific properties to load

e.g. @cm\\:name:\"*\"

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
    api_instance = edu_sharing_client.ADMINV1Api(api_client)
    query = '@cm\\:name:"*"' # str | query (optional) (default to '@cm\\:name:"*"')
    sort_properties = ['sort_properties_example'] # List[str] | sort properties (optional)
    sort_ascending = [True] # List[bool] | sort ascending, true if not set. Use multiple values to change the direction according to the given property at the same index (optional)
    properties = ['properties_example'] # List[str] | properties to fetch, use parent::<property> to include parent property values (optional)
    store = 'store_example' # str | store, workspace or archive (optional)
    authority_scope = ['authority_scope_example'] # List[str] | authority scope to search for (optional)

    try:
        # Search for custom lucene query and choose specific properties to load
        api_response = api_instance.export_by_lucene(query=query, sort_properties=sort_properties, sort_ascending=sort_ascending, properties=properties, store=store, authority_scope=authority_scope)
        print("The response of ADMINV1Api->export_by_lucene:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ADMINV1Api->export_by_lucene: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **query** | **str**| query | [optional] [default to &#39;@cm\\:name:&quot;*&quot;&#39;]
 **sort_properties** | [**List[str]**](str.md)| sort properties | [optional] 
 **sort_ascending** | [**List[bool]**](bool.md)| sort ascending, true if not set. Use multiple values to change the direction according to the given property at the same index | [optional] 
 **properties** | [**List[str]**](str.md)| properties to fetch, use parent::&lt;property&gt; to include parent property values | [optional] 
 **store** | **str**| store, workspace or archive | [optional] 
 **authority_scope** | [**List[str]**](str.md)| authority scope to search for | [optional] 

### Return type

**str**

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

# **export_lom**
> export_lom(filter_query, target_dir, sub_object_handler)

Export Nodes with LOM Metadata Format

Export Nodes with LOM Metadata Format.

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
    api_instance = edu_sharing_client.ADMINV1Api(api_client)
    filter_query = 'filter_query_example' # str | filterQuery
    target_dir = 'target_dir_example' # str | targetDir
    sub_object_handler = True # bool | subObjectHandler

    try:
        # Export Nodes with LOM Metadata Format
        api_instance.export_lom(filter_query, target_dir, sub_object_handler)
    except Exception as e:
        print("Exception when calling ADMINV1Api->export_lom: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **filter_query** | **str**| filterQuery | 
 **target_dir** | **str**| targetDir | 
 **sub_object_handler** | **bool**| subObjectHandler | 

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

# **get_all_jobs**
> str get_all_jobs()

get all available jobs

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
    api_instance = edu_sharing_client.ADMINV1Api(api_client)

    try:
        # get all available jobs
        api_response = api_instance.get_all_jobs()
        print("The response of ADMINV1Api->get_all_jobs:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ADMINV1Api->get_all_jobs: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

**str**

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

# **get_all_toolpermissions**
> str get_all_toolpermissions(authority)

get all toolpermissions for an authority

Returns explicit (rights set for this authority) + effective (resulting rights for this authority) toolpermission

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
    api_instance = edu_sharing_client.ADMINV1Api(api_client)
    authority = 'authority_example' # str | Authority to load (user or group)

    try:
        # get all toolpermissions for an authority
        api_response = api_instance.get_all_toolpermissions(authority)
        print("The response of ADMINV1Api->get_all_toolpermissions:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ADMINV1Api->get_all_toolpermissions: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **authority** | **str**| Authority to load (user or group) | 

### Return type

**str**

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

# **get_application_xml**
> str get_application_xml(xml)

list any xml properties (like from homeApplication.properties.xml)

list any xml properties (like from homeApplication.properties.xml)

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
    api_instance = edu_sharing_client.ADMINV1Api(api_client)
    xml = 'xml_example' # str | Properties Filename (*.xml)

    try:
        # list any xml properties (like from homeApplication.properties.xml)
        api_response = api_instance.get_application_xml(xml)
        print("The response of ADMINV1Api->get_application_xml:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ADMINV1Api->get_application_xml: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **xml** | **str**| Properties Filename (*.xml) | 

### Return type

**str**

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

# **get_applications**
> str get_applications()

list applications

List all registered applications.

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
    api_instance = edu_sharing_client.ADMINV1Api(api_client)

    try:
        # list applications
        api_response = api_instance.get_applications()
        print("The response of ADMINV1Api->get_applications:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ADMINV1Api->get_applications: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

**str**

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

# **get_cache_entries**
> str get_cache_entries(id)

Get entries of a cache

Get entries of a cache.

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
    api_instance = edu_sharing_client.ADMINV1Api(api_client)
    id = 'id_example' # str | Id/bean name of the cache

    try:
        # Get entries of a cache
        api_response = api_instance.get_cache_entries(id)
        print("The response of ADMINV1Api->get_cache_entries:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ADMINV1Api->get_cache_entries: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| Id/bean name of the cache | 

### Return type

**str**

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

# **get_cache_info**
> CacheInfo get_cache_info(id)

Get information about a cache

Get information about a cache.

### Example


```python
import edu_sharing_client
from edu_sharing_client.models.cache_info import CacheInfo
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
    api_instance = edu_sharing_client.ADMINV1Api(api_client)
    id = 'id_example' # str | Id/bean name of the cache

    try:
        # Get information about a cache
        api_response = api_instance.get_cache_info(id)
        print("The response of ADMINV1Api->get_cache_info:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ADMINV1Api->get_cache_info: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| Id/bean name of the cache | 

### Return type

[**CacheInfo**](CacheInfo.md)

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

# **get_catalina_out**
> str get_catalina_out()

Get last info from catalina out

Get catalina.out log.

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
    api_instance = edu_sharing_client.ADMINV1Api(api_client)

    try:
        # Get last info from catalina out
        api_response = api_instance.get_catalina_out()
        print("The response of ADMINV1Api->get_catalina_out:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ADMINV1Api->get_catalina_out: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

**str**

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

# **get_cluster**
> CacheCluster get_cluster()

Get information about the Cluster

Get information the Cluster

### Example


```python
import edu_sharing_client
from edu_sharing_client.models.cache_cluster import CacheCluster
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
    api_instance = edu_sharing_client.ADMINV1Api(api_client)

    try:
        # Get information about the Cluster
        api_response = api_instance.get_cluster()
        print("The response of ADMINV1Api->get_cluster:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ADMINV1Api->get_cluster: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**CacheCluster**](CacheCluster.md)

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

# **get_clusters**
> CacheCluster get_clusters()

Get information about the Cluster

Get information the Cluster

### Example


```python
import edu_sharing_client
from edu_sharing_client.models.cache_cluster import CacheCluster
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
    api_instance = edu_sharing_client.ADMINV1Api(api_client)

    try:
        # Get information about the Cluster
        api_response = api_instance.get_clusters()
        print("The response of ADMINV1Api->get_clusters:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ADMINV1Api->get_clusters: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**CacheCluster**](CacheCluster.md)

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

# **get_config**
> RepositoryConfig get_config()

get the repository config object

### Example


```python
import edu_sharing_client
from edu_sharing_client.models.repository_config import RepositoryConfig
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
    api_instance = edu_sharing_client.ADMINV1Api(api_client)

    try:
        # get the repository config object
        api_response = api_instance.get_config()
        print("The response of ADMINV1Api->get_config:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ADMINV1Api->get_config: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**RepositoryConfig**](RepositoryConfig.md)

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

# **get_config_file**
> str get_config_file(filename, path_prefix)

get a base system config file (e.g. edu-sharing.conf)

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
    api_instance = edu_sharing_client.ADMINV1Api(api_client)
    filename = 'filename_example' # str | filename to fetch
    path_prefix = 'path_prefix_example' # str | path prefix this file belongs to

    try:
        # get a base system config file (e.g. edu-sharing.conf)
        api_response = api_instance.get_config_file(filename, path_prefix)
        print("The response of ADMINV1Api->get_config_file:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ADMINV1Api->get_config_file: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **filename** | **str**| filename to fetch | 
 **path_prefix** | **str**| path prefix this file belongs to | 

### Return type

**str**

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

# **get_enabled_plugins**
> str get_enabled_plugins()

get enabled system plugins

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
    api_instance = edu_sharing_client.ADMINV1Api(api_client)

    try:
        # get enabled system plugins
        api_response = api_instance.get_enabled_plugins()
        print("The response of ADMINV1Api->get_enabled_plugins:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ADMINV1Api->get_enabled_plugins: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

**str**

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

# **get_global_groups**
> str get_global_groups()

Get global groups

Get global groups (groups across repositories).

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
    api_instance = edu_sharing_client.ADMINV1Api(api_client)

    try:
        # Get global groups
        api_response = api_instance.get_global_groups()
        print("The response of ADMINV1Api->get_global_groups:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ADMINV1Api->get_global_groups: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

**str**

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

# **get_jobs**
> str get_jobs()

get all running jobs

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
    api_instance = edu_sharing_client.ADMINV1Api(api_client)

    try:
        # get all running jobs
        api_response = api_instance.get_jobs()
        print("The response of ADMINV1Api->get_jobs:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ADMINV1Api->get_jobs: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

**str**

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

# **get_lightbend_config**
> object get_lightbend_config()



Get the fully merged & parsed (lightbend) backend config

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
    api_instance = edu_sharing_client.ADMINV1Api(api_client)

    try:
        api_response = api_instance.get_lightbend_config()
        print("The response of ADMINV1Api->get_lightbend_config:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ADMINV1Api->get_lightbend_config: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

**object**

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

# **get_logging_runtime**
> LoggerConfigResult get_logging_runtime(filters=filters, only_config=only_config)

get the logger config

### Example


```python
import edu_sharing_client
from edu_sharing_client.models.logger_config_result import LoggerConfigResult
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
    api_instance = edu_sharing_client.ADMINV1Api(api_client)
    filters = ['filters_example'] # List[str] | filters (optional)
    only_config = True # bool | onlyConfig if true only loggers defined in log4j.xml or at runtime are returned (optional)

    try:
        # get the logger config
        api_response = api_instance.get_logging_runtime(filters=filters, only_config=only_config)
        print("The response of ADMINV1Api->get_logging_runtime:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ADMINV1Api->get_logging_runtime: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **filters** | [**List[str]**](str.md)| filters | [optional] 
 **only_config** | **bool**| onlyConfig if true only loggers defined in log4j.xml or at runtime are returned | [optional] 

### Return type

[**LoggerConfigResult**](LoggerConfigResult.md)

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

# **get_oai_classes**
> str get_oai_classes()

Get OAI class names

Get available importer classes for OAI import.

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
    api_instance = edu_sharing_client.ADMINV1Api(api_client)

    try:
        # Get OAI class names
        api_response = api_instance.get_oai_classes()
        print("The response of ADMINV1Api->get_oai_classes:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ADMINV1Api->get_oai_classes: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

**str**

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

# **get_property_to_mds**
> str get_property_to_mds(properties)

Get a Mds Valuespace for all values of the given properties

Get a Mds Valuespace for all values of the given properties.

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
    api_instance = edu_sharing_client.ADMINV1Api(api_client)
    properties = ['properties_example'] # List[str] | one or more properties

    try:
        # Get a Mds Valuespace for all values of the given properties
        api_response = api_instance.get_property_to_mds(properties)
        print("The response of ADMINV1Api->get_property_to_mds:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ADMINV1Api->get_property_to_mds: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **properties** | [**List[str]**](str.md)| one or more properties | 

### Return type

**str**

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

# **get_statistics**
> AdminStatistics get_statistics()

get statistics

get statistics.

### Example


```python
import edu_sharing_client
from edu_sharing_client.models.admin_statistics import AdminStatistics
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
    api_instance = edu_sharing_client.ADMINV1Api(api_client)

    try:
        # get statistics
        api_response = api_instance.get_statistics()
        print("The response of ADMINV1Api->get_statistics:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ADMINV1Api->get_statistics: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**AdminStatistics**](AdminStatistics.md)

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

# **get_version**
> RepositoryVersionInfo get_version()

get detailed version information

detailed information about the running system version

### Example


```python
import edu_sharing_client
from edu_sharing_client.models.repository_version_info import RepositoryVersionInfo
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
    api_instance = edu_sharing_client.ADMINV1Api(api_client)

    try:
        # get detailed version information
        api_response = api_instance.get_version()
        print("The response of ADMINV1Api->get_version:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ADMINV1Api->get_version: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**RepositoryVersionInfo**](RepositoryVersionInfo.md)

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

# **import_collections**
> CollectionsResult import_collections(xml, parent=parent)

import collections via a xml file

xml file must be structured as defined by the xsd standard

### Example


```python
import edu_sharing_client
from edu_sharing_client.models.collections_result import CollectionsResult
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
    api_instance = edu_sharing_client.ADMINV1Api(api_client)
    xml = None # object | XML file to parse (or zip file containing exactly 1 xml file to parse)
    parent = 'parent_example' # str | Id of the root to initialize the collection structure, or '-root-' to inflate them on the first level (optional)

    try:
        # import collections via a xml file
        api_response = api_instance.import_collections(xml, parent=parent)
        print("The response of ADMINV1Api->import_collections:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ADMINV1Api->import_collections: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **xml** | [**object**](object.md)| XML file to parse (or zip file containing exactly 1 xml file to parse) | 
 **parent** | **str**| Id of the root to initialize the collection structure, or &#39;-root-&#39; to inflate them on the first level | [optional] 

### Return type

[**CollectionsResult**](CollectionsResult.md)

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

# **import_excel**
> ExcelResult import_excel(parent, add_to_collection, excel)

Import excel data

Import excel data.

### Example


```python
import edu_sharing_client
from edu_sharing_client.models.excel_result import ExcelResult
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
    api_instance = edu_sharing_client.ADMINV1Api(api_client)
    parent = 'parent_example' # str | parent
    add_to_collection = False # bool | addToCollection (default to False)
    excel = None # object | Excel file to import

    try:
        # Import excel data
        api_response = api_instance.import_excel(parent, add_to_collection, excel)
        print("The response of ADMINV1Api->import_excel:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ADMINV1Api->import_excel: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **parent** | **str**| parent | 
 **add_to_collection** | **bool**| addToCollection | [default to False]
 **excel** | [**object**](object.md)| Excel file to import | 

### Return type

[**ExcelResult**](ExcelResult.md)

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

# **import_oai**
> import_oai(base_url, set, metadata_prefix, class_name, metadataset=metadataset, importer_class_name=importer_class_name, record_handler_class_name=record_handler_class_name, binary_handler_class_name=binary_handler_class_name, persistent_handler_class_name=persistent_handler_class_name, file_url=file_url, oai_ids=oai_ids, force_update=force_update, var_from=var_from, until=until, period_in_days=period_in_days)

Import oai data

Import oai data.

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
    api_instance = edu_sharing_client.ADMINV1Api(api_client)
    base_url = 'base_url_example' # str | base url
    set = 'set_example' # str | set/catalog id
    metadata_prefix = 'metadata_prefix_example' # str | metadata prefix
    class_name = 'org.edu_sharing.repository.server.jobs.quartz.ImporterJob' # str | importer job class name (call /classes to obtain a list) (default to 'org.edu_sharing.repository.server.jobs.quartz.ImporterJob')
    metadataset = 'metadataset_example' # str | id metadataset (optional)
    importer_class_name = 'org.edu_sharing.repository.server.importer.OAIPMHLOMImporter' # str | importer class name (call /classes to obtain a list) (optional) (default to 'org.edu_sharing.repository.server.importer.OAIPMHLOMImporter')
    record_handler_class_name = 'org.edu_sharing.repository.server.importer.RecordHandlerLOM' # str | RecordHandler class name (optional) (default to 'org.edu_sharing.repository.server.importer.RecordHandlerLOM')
    binary_handler_class_name = 'binary_handler_class_name_example' # str | BinaryHandler class name (may be empty for none) (optional)
    persistent_handler_class_name = 'persistent_handler_class_name_example' # str | PersistentHandlerClassName class name (may be empty for none) (optional)
    file_url = 'file_url_example' # str | url to file (optional)
    oai_ids = 'oai_ids_example' # str | OAI Ids to import, can be null than the whole set will be imported (optional)
    force_update = False # bool | force Update of all entries (optional) (default to False)
    var_from = 'var_from_example' # str | from: datestring yyyy-MM-dd) (optional)
    until = 'until_example' # str | until: datestring yyyy-MM-dd) (optional)
    period_in_days = 'period_in_days_example' # str | periodInDays: internal sets from and until. only effective if from/until not set) (optional)

    try:
        # Import oai data
        api_instance.import_oai(base_url, set, metadata_prefix, class_name, metadataset=metadataset, importer_class_name=importer_class_name, record_handler_class_name=record_handler_class_name, binary_handler_class_name=binary_handler_class_name, persistent_handler_class_name=persistent_handler_class_name, file_url=file_url, oai_ids=oai_ids, force_update=force_update, var_from=var_from, until=until, period_in_days=period_in_days)
    except Exception as e:
        print("Exception when calling ADMINV1Api->import_oai: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **base_url** | **str**| base url | 
 **set** | **str**| set/catalog id | 
 **metadata_prefix** | **str**| metadata prefix | 
 **class_name** | **str**| importer job class name (call /classes to obtain a list) | [default to &#39;org.edu_sharing.repository.server.jobs.quartz.ImporterJob&#39;]
 **metadataset** | **str**| id metadataset | [optional] 
 **importer_class_name** | **str**| importer class name (call /classes to obtain a list) | [optional] [default to &#39;org.edu_sharing.repository.server.importer.OAIPMHLOMImporter&#39;]
 **record_handler_class_name** | **str**| RecordHandler class name | [optional] [default to &#39;org.edu_sharing.repository.server.importer.RecordHandlerLOM&#39;]
 **binary_handler_class_name** | **str**| BinaryHandler class name (may be empty for none) | [optional] 
 **persistent_handler_class_name** | **str**| PersistentHandlerClassName class name (may be empty for none) | [optional] 
 **file_url** | **str**| url to file | [optional] 
 **oai_ids** | **str**| OAI Ids to import, can be null than the whole set will be imported | [optional] 
 **force_update** | **bool**| force Update of all entries | [optional] [default to False]
 **var_from** | **str**| from: datestring yyyy-MM-dd) | [optional] 
 **until** | **str**| until: datestring yyyy-MM-dd) | [optional] 
 **period_in_days** | **str**| periodInDays: internal sets from and until. only effective if from/until not set) | [optional] 

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

# **import_oai_xml**
> Node import_oai_xml(record_handler_class_name=record_handler_class_name, binary_handler_class_name=binary_handler_class_name, xml=xml)

Import single xml via oai (for testing)

### Example


```python
import edu_sharing_client
from edu_sharing_client.models.node import Node
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
    api_instance = edu_sharing_client.ADMINV1Api(api_client)
    record_handler_class_name = 'org.edu_sharing.repository.server.importer.RecordHandlerLOM' # str | RecordHandler class name (optional) (default to 'org.edu_sharing.repository.server.importer.RecordHandlerLOM')
    binary_handler_class_name = 'binary_handler_class_name_example' # str | BinaryHandler class name (may be empty for none) (optional)
    xml = None # object |  (optional)

    try:
        # Import single xml via oai (for testing)
        api_response = api_instance.import_oai_xml(record_handler_class_name=record_handler_class_name, binary_handler_class_name=binary_handler_class_name, xml=xml)
        print("The response of ADMINV1Api->import_oai_xml:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ADMINV1Api->import_oai_xml: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **record_handler_class_name** | **str**| RecordHandler class name | [optional] [default to &#39;org.edu_sharing.repository.server.importer.RecordHandlerLOM&#39;]
 **binary_handler_class_name** | **str**| BinaryHandler class name (may be empty for none) | [optional] 
 **xml** | [**object**](object.md)|  | [optional] 

### Return type

[**Node**](Node.md)

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

# **refresh_app_info**
> refresh_app_info()

refresh app info

Refresh the application info.

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
    api_instance = edu_sharing_client.ADMINV1Api(api_client)

    try:
        # refresh app info
        api_instance.refresh_app_info()
    except Exception as e:
        print("Exception when calling ADMINV1Api->refresh_app_info: %s\n" % e)
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

# **refresh_cache**
> refresh_cache(folder, sticky)

Refresh cache

Refresh importer cache.

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
    api_instance = edu_sharing_client.ADMINV1Api(api_client)
    folder = '-userhome-' # str | refresh cache root folder id (default to '-userhome-')
    sticky = False # bool | sticky (default to False)

    try:
        # Refresh cache
        api_instance.refresh_cache(folder, sticky)
    except Exception as e:
        print("Exception when calling ADMINV1Api->refresh_cache: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **folder** | **str**| refresh cache root folder id | [default to &#39;-userhome-&#39;]
 **sticky** | **bool**| sticky | [default to False]

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

# **refresh_edu_group_cache**
> refresh_edu_group_cache(keep_existing=keep_existing)

Refresh the Edu Group Cache

Refresh the Edu Group Cache.

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
    api_instance = edu_sharing_client.ADMINV1Api(api_client)
    keep_existing = False # bool | keep existing (optional) (default to False)

    try:
        # Refresh the Edu Group Cache
        api_instance.refresh_edu_group_cache(keep_existing=keep_existing)
    except Exception as e:
        print("Exception when calling ADMINV1Api->refresh_edu_group_cache: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **keep_existing** | **bool**| keep existing | [optional] [default to False]

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

# **remove_application**
> remove_application(id)

remove an application

remove the specified application.

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
    api_instance = edu_sharing_client.ADMINV1Api(api_client)
    id = 'id_example' # str | Application id

    try:
        # remove an application
        api_instance.remove_application(id)
    except Exception as e:
        print("Exception when calling ADMINV1Api->remove_application: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| Application id | 

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

# **remove_cache_entry**
> remove_cache_entry(cache_index=cache_index, bean=bean)

remove cache entry

remove cache entry

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
    api_instance = edu_sharing_client.ADMINV1Api(api_client)
    cache_index = 56 # int | cacheIndex (optional)
    bean = 'bean_example' # str | bean (optional)

    try:
        # remove cache entry
        api_instance.remove_cache_entry(cache_index=cache_index, bean=bean)
    except Exception as e:
        print("Exception when calling ADMINV1Api->remove_cache_entry: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **cache_index** | **int**| cacheIndex | [optional] 
 **bean** | **str**| bean | [optional] 

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

# **remove_oai_imports**
> remove_oai_imports(base_url, set, metadata_prefix)

Remove deleted imports

Remove deleted imports.

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
    api_instance = edu_sharing_client.ADMINV1Api(api_client)
    base_url = 'base_url_example' # str | base url
    set = 'set_example' # str | set/catalog id
    metadata_prefix = 'metadata_prefix_example' # str | metadata prefix

    try:
        # Remove deleted imports
        api_instance.remove_oai_imports(base_url, set, metadata_prefix)
    except Exception as e:
        print("Exception when calling ADMINV1Api->remove_oai_imports: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **base_url** | **str**| base url | 
 **set** | **str**| set/catalog id | 
 **metadata_prefix** | **str**| metadata prefix | 

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

# **search_by_elastic_dsl**
> SearchResultElastic search_by_elastic_dsl(dsl=dsl)

Search for custom elastic DSL query

### Example


```python
import edu_sharing_client
from edu_sharing_client.models.search_result_elastic import SearchResultElastic
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
    api_instance = edu_sharing_client.ADMINV1Api(api_client)
    dsl = 'dsl_example' # str | dsl query (json encoded) (optional)

    try:
        # Search for custom elastic DSL query
        api_response = api_instance.search_by_elastic_dsl(dsl=dsl)
        print("The response of ADMINV1Api->search_by_elastic_dsl:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ADMINV1Api->search_by_elastic_dsl: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **dsl** | **str**| dsl query (json encoded) | [optional] 

### Return type

[**SearchResultElastic**](SearchResultElastic.md)

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

# **search_by_lucene**
> SearchResult search_by_lucene(query=query, max_items=max_items, skip_count=skip_count, sort_properties=sort_properties, sort_ascending=sort_ascending, property_filter=property_filter, store=store, authority_scope=authority_scope)

Search for custom lucene query

e.g. @cm\\:name:\"*\"

### Example


```python
import edu_sharing_client
from edu_sharing_client.models.search_result import SearchResult
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
    api_instance = edu_sharing_client.ADMINV1Api(api_client)
    query = '@cm\\:name:"*"' # str | query (optional) (default to '@cm\\:name:"*"')
    max_items = 10 # int | maximum items per page (optional) (default to 10)
    skip_count = 0 # int | skip a number of items (optional) (default to 0)
    sort_properties = ['sort_properties_example'] # List[str] | sort properties (optional)
    sort_ascending = [True] # List[bool] | sort ascending, true if not set. Use multiple values to change the direction according to the given property at the same index (optional)
    property_filter = ['property_filter_example'] # List[str] | property filter for result nodes (or \"-all-\" for all properties) (optional)
    store = 'store_example' # str | store, workspace or archive (optional)
    authority_scope = ['authority_scope_example'] # List[str] | authority scope to search for (optional)

    try:
        # Search for custom lucene query
        api_response = api_instance.search_by_lucene(query=query, max_items=max_items, skip_count=skip_count, sort_properties=sort_properties, sort_ascending=sort_ascending, property_filter=property_filter, store=store, authority_scope=authority_scope)
        print("The response of ADMINV1Api->search_by_lucene:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ADMINV1Api->search_by_lucene: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **query** | **str**| query | [optional] [default to &#39;@cm\\:name:&quot;*&quot;&#39;]
 **max_items** | **int**| maximum items per page | [optional] [default to 10]
 **skip_count** | **int**| skip a number of items | [optional] [default to 0]
 **sort_properties** | [**List[str]**](str.md)| sort properties | [optional] 
 **sort_ascending** | [**List[bool]**](bool.md)| sort ascending, true if not set. Use multiple values to change the direction according to the given property at the same index | [optional] 
 **property_filter** | [**List[str]**](str.md)| property filter for result nodes (or \&quot;-all-\&quot; for all properties) | [optional] 
 **store** | **str**| store, workspace or archive | [optional] 
 **authority_scope** | [**List[str]**](str.md)| authority scope to search for | [optional] 

### Return type

[**SearchResult**](SearchResult.md)

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

# **server_update_list**
> str server_update_list()

list available update tasks

list available update tasks

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
    api_instance = edu_sharing_client.ADMINV1Api(api_client)

    try:
        # list available update tasks
        api_response = api_instance.server_update_list()
        print("The response of ADMINV1Api->server_update_list:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ADMINV1Api->server_update_list: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

**str**

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

# **server_update_list1**
> str server_update_list1(id, execute)

Run an update tasks

Run a specific update task (test or full update).

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
    api_instance = edu_sharing_client.ADMINV1Api(api_client)
    id = 'id_example' # str | Id of the update task
    execute = False # bool | Actually execute (if false, just runs in test mode) (default to False)

    try:
        # Run an update tasks
        api_response = api_instance.server_update_list1(id, execute)
        print("The response of ADMINV1Api->server_update_list1:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ADMINV1Api->server_update_list1: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| Id of the update task | 
 **execute** | **bool**| Actually execute (if false, just runs in test mode) | [default to False]

### Return type

**str**

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

# **set_config**
> set_config(repository_config=repository_config)

set/update the repository config object

### Example


```python
import edu_sharing_client
from edu_sharing_client.models.repository_config import RepositoryConfig
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
    api_instance = edu_sharing_client.ADMINV1Api(api_client)
    repository_config = edu_sharing_client.RepositoryConfig() # RepositoryConfig |  (optional)

    try:
        # set/update the repository config object
        api_instance.set_config(repository_config=repository_config)
    except Exception as e:
        print("Exception when calling ADMINV1Api->set_config: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **repository_config** | [**RepositoryConfig**](RepositoryConfig.md)|  | [optional] 

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
**500** | Fatal error occured. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **set_toolpermissions**
> str set_toolpermissions(authority, request_body=request_body)

set toolpermissions for an authority

If a toolpermission has status UNDEFINED, it will remove explicit permissions for the authority

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
    api_instance = edu_sharing_client.ADMINV1Api(api_client)
    authority = 'authority_example' # str | Authority to set (user or group)
    request_body = {'key': 'request_body_example'} # Dict[str, str] |  (optional)

    try:
        # set toolpermissions for an authority
        api_response = api_instance.set_toolpermissions(authority, request_body=request_body)
        print("The response of ADMINV1Api->set_toolpermissions:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ADMINV1Api->set_toolpermissions: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **authority** | **str**| Authority to set (user or group) | 
 **request_body** | [**Dict[str, str]**](str.md)|  | [optional] 

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
**500** | Fatal error occured. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **start_job**
> start_job(job_class, request_body)

Start a Job.

Start a Job.

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
    api_instance = edu_sharing_client.ADMINV1Api(api_client)
    job_class = 'job_class_example' # str | jobClass
    request_body = None # Dict[str, object] | params

    try:
        # Start a Job.
        api_instance.start_job(job_class, request_body)
    except Exception as e:
        print("Exception when calling ADMINV1Api->start_job: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **job_class** | **str**| jobClass | 
 **request_body** | [**Dict[str, object]**](object.md)| params | 

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

# **start_job_sync**
> object start_job_sync(job_class, request_body)

Start a Job.

Start a Job. Wait for the result synchronously

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
    api_instance = edu_sharing_client.ADMINV1Api(api_client)
    job_class = 'job_class_example' # str | jobClass
    request_body = None # Dict[str, object] | params

    try:
        # Start a Job.
        api_response = api_instance.start_job_sync(job_class, request_body)
        print("The response of ADMINV1Api->start_job_sync:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ADMINV1Api->start_job_sync: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **job_class** | **str**| jobClass | 
 **request_body** | [**Dict[str, object]**](object.md)| params | 

### Return type

**object**

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

# **switch_authority**
> switch_authority(authority_name)

switch the session to a known authority name

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
    api_instance = edu_sharing_client.ADMINV1Api(api_client)
    authority_name = 'authority_name_example' # str | the authority to use (must be a person)

    try:
        # switch the session to a known authority name
        api_instance.switch_authority(authority_name)
    except Exception as e:
        print("Exception when calling ADMINV1Api->switch_authority: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **authority_name** | **str**| the authority to use (must be a person) | 

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

# **test_mail**
> test_mail(receiver, template)

Test a mail template

Sends the given template as a test to the given receiver.

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
    api_instance = edu_sharing_client.ADMINV1Api(api_client)
    receiver = 'receiver_example' # str | 
    template = 'template_example' # str | 

    try:
        # Test a mail template
        api_instance.test_mail(receiver, template)
    except Exception as e:
        print("Exception when calling ADMINV1Api->test_mail: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **receiver** | **str**|  | 
 **template** | **str**|  | 

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

# **update_application_xml**
> update_application_xml(xml, request_body=request_body)

edit any properties xml (like homeApplication.properties.xml)

if the key exists, it will be overwritten. Otherwise, it will be created. You only need to transfer keys you want to edit

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
    api_instance = edu_sharing_client.ADMINV1Api(api_client)
    xml = 'xml_example' # str | Properties Filename (*.xml)
    request_body = {'key': 'request_body_example'} # Dict[str, str] |  (optional)

    try:
        # edit any properties xml (like homeApplication.properties.xml)
        api_instance.update_application_xml(xml, request_body=request_body)
    except Exception as e:
        print("Exception when calling ADMINV1Api->update_application_xml: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **xml** | **str**| Properties Filename (*.xml) | 
 **request_body** | [**Dict[str, str]**](str.md)|  | [optional] 

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
**500** | Fatal error occured. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_config_file**
> update_config_file(filename, path_prefix, body=body)

update a base system config file (e.g. edu-sharing.conf)

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
    api_instance = edu_sharing_client.ADMINV1Api(api_client)
    filename = 'filename_example' # str | filename to fetch
    path_prefix = 'path_prefix_example' # str | path prefix this file belongs to
    body = 'body_example' # str |  (optional)

    try:
        # update a base system config file (e.g. edu-sharing.conf)
        api_instance.update_config_file(filename, path_prefix, body=body)
    except Exception as e:
        print("Exception when calling ADMINV1Api->update_config_file: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **filename** | **str**| filename to fetch | 
 **path_prefix** | **str**| path prefix this file belongs to | 
 **body** | **str**|  | [optional] 

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
**500** | Fatal error occured. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **upload_temp**
> UploadResult upload_temp(name, file)

Upload a file

Upload a file to tomcat temp directory, to use it on the server (e.g. an update)

### Example


```python
import edu_sharing_client
from edu_sharing_client.models.upload_result import UploadResult
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
    api_instance = edu_sharing_client.ADMINV1Api(api_client)
    name = 'name_example' # str | filename
    file = None # object | file to upload

    try:
        # Upload a file
        api_response = api_instance.upload_temp(name, file)
        print("The response of ADMINV1Api->upload_temp:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ADMINV1Api->upload_temp: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **name** | **str**| filename | 
 **file** | [**object**](object.md)| file to upload | 

### Return type

[**UploadResult**](UploadResult.md)

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

