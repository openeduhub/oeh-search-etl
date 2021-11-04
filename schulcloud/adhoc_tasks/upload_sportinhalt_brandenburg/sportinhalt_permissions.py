import copy
import json

import requests

from schulcloud.adhoc_tasks.upload_sportinhalt_brandenburg.sportinhalt_utils import get_base_headers


def edusharing_add_to_permission_groups(config, hostname, auth_response, node_id, total_permissions, permissions_response_dict):
    groups = config.get("group_permissions")

    at_uri = "/edu-sharing/rest/node/v1/nodes/-home-/"+node_id+"/permissions?sendMail=false&sendCopy=false"
    at_url = "https://" + hostname + at_uri

    headers = get_base_headers(auth_response)

    permission_template = None
    # In case we want to consider existing permissions. (We could consider both cases of local and inherited
    # permissions.)
    # if len(total_permissions) > 0 and len(permissions_response_dict["permissions"]["localPermissions"]) > 0:
    #     permission_template = permissions_response_dict["permissions"]["localPermissions"]["permissions"][0]
    # elif len(total_permissions) > 0 and len(permissions_response_dict["permissions"]["inheritedPermissions"]) > 0:
    #     permission_template = permissions_response_dict["permissions"]["inheritedPermissions"]["permissions"][0]
    if permission_template is None:
        permission_template = config.get("permission_template")

    if "localPermissions" not in permissions_response_dict["permissions"]:
        permissions_response_dict["permissions"]["localPermissions"] = {
            "inherited": "true" if len(
                permissions_response_dict["permissions"]["inheritedPermissions"]) > 0 else "false",
            "permissions": []
        }

    for group_name, group_properties in groups.items():
        if group_name not in total_permissions:
            new_permission = copy.deepcopy(permission_template)

            new_permission["authority"]["authorityName"] = group_properties["authority"]["authorityName"]
            new_permission["authority"]["authorityType"] = group_properties["authority"]["authorityType"]
            new_permission["group"]["displayName"] = group_properties["group"]["displayName"]
            new_permission["permissions"] = group_properties["permissions"]

            permissions_response_dict["permissions"]["localPermissions"]["permissions"].append(new_permission)


    # Unfortunately, Edu-Sharing does not accept several of the fields it gives us when retrieving the current group
    # permissions to be set when we insert group permissions. This means we have to remove redundant attributes prior to
    # inserting the group permissions we desire. Therefore,
    #
    # Remove redundant attributes:
    for permission in permissions_response_dict["permissions"]["localPermissions"]["permissions"]:

        permission = remove_empty_attributes(permission)
        permission["authority"] = remove_empty_attributes(permission["authority"])

        # Remove redundant attributes under authority attribute field.
        for redundant_authority_attr in ["editable", "profile"]:
            if redundant_authority_attr in permission["authority"]:
                del permission["authority"][redundant_authority_attr]

        if "group" in permission:
            permission["group"] = remove_empty_attributes(permission["group"])

    r = requests.request("POST", at_url, data=json.dumps(permissions_response_dict["permissions"]["localPermissions"]),
                         headers=headers, allow_redirects=False)
    from schulcloud.adhoc_tasks.upload_sportinhalt_brandenburg.modify_sportinhalt import edusharing_set_property
    edusharing_set_property(node_id, "ccm:ph_invited", total_permissions, auth_response)


def remove_empty_attributes(permission):
    attributes_to_delete = set()
    for k, v in permission.items():
        if v == "null" or v is None:
            attributes_to_delete.add(k)
    for attr in attributes_to_delete:
        del permission[attr]
    return permission


def edusharing_get_permission_groups(hostname, parsed_edusharing_url, auth_response, node_id):
    at_uri = "/edu-sharing/rest/node/v1/nodes/-home-/" + node_id + "/permissions"
    at_url = parsed_edusharing_url.scheme + "://" + hostname + at_uri

    total_permissions = set()

    headers = get_base_headers(auth_response)

    r = requests.request("GET", at_url, headers=headers, allow_redirects=False)

    response_dict = json.loads(r.text)

    # Save the current group names, which follow the form "GROUP_X"
    for permission in response_dict["permissions"]["localPermissions"]["permissions"]:
        total_permissions.add(permission["authority"]["authorityName"])

    return total_permissions, response_dict