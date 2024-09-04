# Values


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**supported_languages** | **List[str]** |  | [optional] 
**extension** | **str** |  | [optional] 
**login_url** | **str** |  | [optional] 
**login_allow_local** | **bool** |  | [optional] 
**login_providers_url** | **str** |  | [optional] 
**login_provider_target_url** | **str** |  | [optional] 
**register** | [**Register**](Register.md) |  | [optional] 
**recover_password_url** | **str** |  | [optional] 
**imprint_url** | **str** |  | [optional] 
**privacy_information_url** | **str** |  | [optional] 
**help_url** | **str** |  | [optional] 
**whats_new_url** | **str** |  | [optional] 
**edit_profile_url** | **str** |  | [optional] 
**edit_profile** | **bool** |  | [optional] 
**workspace_columns** | **List[str]** |  | [optional] 
**workspace_shared_to_me_default_all** | **bool** |  | [optional] 
**hide_main_menu** | **List[str]** |  | [optional] 
**logout** | [**LogoutInfo**](LogoutInfo.md) |  | [optional] 
**menu_entries** | [**List[MenuEntry]**](MenuEntry.md) |  | [optional] 
**custom_options** | [**List[ContextMenuEntry]**](ContextMenuEntry.md) |  | [optional] 
**user_menu_overrides** | [**List[ContextMenuEntry]**](ContextMenuEntry.md) |  | [optional] 
**allowed_licenses** | **List[str]** |  | [optional] 
**custom_licenses** | [**List[License]**](License.md) |  | [optional] 
**workflow** | [**ConfigWorkflow**](ConfigWorkflow.md) |  | [optional] 
**license_dialog_on_upload** | **bool** |  | [optional] 
**node_report** | **bool** |  | [optional] 
**branding** | **bool** |  | [optional] 
**rating** | [**ConfigRating**](ConfigRating.md) |  | [optional] 
**publishing_notice** | **bool** |  | [optional] 
**site_title** | **str** |  | [optional] 
**user_display_name** | **str** |  | [optional] 
**user_secondary_display_name** | **str** |  | [optional] 
**user_affiliation** | **bool** |  | [optional] 
**default_username** | **str** |  | [optional] 
**default_password** | **str** |  | [optional] 
**banner** | [**Banner**](Banner.md) |  | [optional] 
**available_mds** | [**List[AvailableMds]**](AvailableMds.md) |  | [optional] 
**available_repositories** | **List[str]** |  | [optional] 
**search_view_type** | **int** |  | [optional] 
**workspace_view_type** | **int** |  | [optional] 
**items_per_request** | **int** |  | [optional] 
**rendering** | [**Rendering**](Rendering.md) |  | [optional] 
**session_expired_dialog** | **object** |  | [optional] 
**login_default_location** | **str** |  | [optional] 
**search_group_results** | **bool** |  | [optional] 
**mainnav** | [**Mainnav**](Mainnav.md) |  | [optional] 
**search_sidenav_mode** | **str** |  | [optional] 
**guest** | [**Guest**](Guest.md) |  | [optional] 
**collections** | [**Collections**](Collections.md) |  | [optional] 
**license_agreement** | [**LicenseAgreement**](LicenseAgreement.md) |  | [optional] 
**services** | [**Services**](Services.md) |  | [optional] 
**help_menu_options** | [**List[HelpMenuOptions]**](HelpMenuOptions.md) |  | [optional] 
**images** | [**List[Image]**](Image.md) |  | [optional] 
**icons** | [**List[FontIcon]**](FontIcon.md) |  | [optional] 
**stream** | [**Stream**](Stream.md) |  | [optional] 
**admin** | [**Admin**](Admin.md) |  | [optional] 
**simple_edit** | [**SimpleEdit**](SimpleEdit.md) |  | [optional] 
**frontpage** | [**ConfigFrontpage**](ConfigFrontpage.md) |  | [optional] 
**upload** | [**ConfigUpload**](ConfigUpload.md) |  | [optional] 
**publish** | [**ConfigPublish**](ConfigPublish.md) |  | [optional] 
**remote** | [**ConfigRemote**](ConfigRemote.md) |  | [optional] 
**custom_css** | **str** |  | [optional] 
**theme_colors** | [**ConfigThemeColors**](ConfigThemeColors.md) |  | [optional] 
**privacy** | [**ConfigPrivacy**](ConfigPrivacy.md) |  | [optional] 
**tutorial** | [**ConfigTutorial**](ConfigTutorial.md) |  | [optional] 

## Example

```python
from edu_sharing_client.models.values import Values

# TODO update the JSON string below
json = "{}"
# create an instance of Values from a JSON string
values_instance = Values.from_json(json)
# print the JSON string representation of the object
print(Values.to_json())

# convert the object into a dict
values_dict = values_instance.to_dict()
# create an instance of Values from a dict
values_from_dict = Values.from_dict(values_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


