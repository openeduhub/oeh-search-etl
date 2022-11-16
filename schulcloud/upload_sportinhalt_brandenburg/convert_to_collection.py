import json
from http.client import HTTPResponse
import requests
from schulcloud.adhoc_tasks.upload_sportinhalt_brandenburg.sportinhalt_utils import get_configuration, get_base_headers, \
    edusharing_set_property, edusharing_change_metadata
from tqdm import tqdm

def identify_collections_in_directory(auth_response, directory_node_id):
    """
    This is a method to identify and return any collections in a given directory node id.

    We *only* consider combinations of directories, which contain the children of a given collection, and files,
     which are the parents of the aforementioned collections. All remaining files and directories will be ignored.
    """

    configuration = get_configuration()

    at_uri = "/edu-sharing/rest/node/v1/nodes/-home-/" + directory_node_id + "/children?maxItems=500&skipCount=0"
    at_url = configuration["parsed_edusharing_url"].scheme + "://" + configuration["hostname"] + at_uri

    headers = get_base_headers(auth_response)
    r = requests.request("GET", at_url, headers=headers, allow_redirects=False)

    response_dict = json.loads(r.text)

    collections = {}
    for response in response_dict["nodes"]:
        # Directory or filename (removing any extensions).
        name = response["name"].rsplit(".", 1)[0]
        if name not in collections:
            collections[name] = {}
        if response["isDirectory"]:
            collections[name]["directory"] = response
        else:
            collections[name]["parent"] = response

    full_collections = {}
    for key in collections:
        if len(collections[key]) > 1:
            full_collections[key] = collections[key]

    return full_collections

def get_directory_elements(auth_response: HTTPResponse, directory_node_id: str):
    at_uri = "/edu-sharing/rest/node/v1/nodes/-home-/" + directory_node_id + "/children?maxItems=500&skipCount=0"

    configuration = get_configuration()
    at_url = configuration["parsed_edusharing_url"].scheme + "://" + configuration["hostname"] + at_uri

    headers = get_base_headers(auth_response)
    r = requests.request("GET", at_url, headers=headers, allow_redirects=False)

    response_dict = json.loads(r.text)

    node_id_to_reponse = {}

    for response in response_dict["nodes"]:
        if response["isDirectory"] is False:
            print(response["name"])
            node_id_to_reponse[response["ref"]["id"]] = response
    return node_id_to_reponse

def convert_to_collection(auth_response, parent_element, children_elements):
    # Overwrite some attributes' default values.

    # Is the following needed?
    # artificial_element_suffix = "000000"
    # parent_element["id"] = parent_element["id"] + artificial_element_suffix

    parent_element["ccm:hpi_searchable"] = 1
    parent_element["ccm:hpi_lom_general_aggregationlevel"] = 2
    for node_id in sorted(children_elements):
        children_elements[node_id]["ccm:hpi_searchable"] = 0
        children_elements[node_id]["ccm:hpi_lom_general_aggregationlevel"] = 1

    # Copied from Mediothek Pixiothek - Add connections from "parent" to "children" elements.
    parent_element["ccm:hpi_lom_relation"] = [
        {
            "kind": "haspart",
            "resource": {
                "identifier": [
                    # Use the ccm:replicationsourceuuid to refer to the children elements.
                    children_elements[node_id]["ccm:replicationsourceuuid"] for node_id in sorted(children_elements)
                ]
            }
        }
    ]

    # Add connections from "children" elements to "parent".
    for node_id in sorted(children_elements):
        children_elements[node_id]["ccm:hpi_lom_relation"] = [
            {
                "kind": "ispartof",
                "resource": {
                    # Use the ccm:replicationsourceuuid to refer to the parent element.
                    "identifier": [parent_element["ccm:replicationsourceuuid"]]
                }
            }
        ]

    # Apply changes for parent and children to Edu-Sharing
    elements = {}
    elements.update(children_elements)
    elements[parent_element["ref"]["id"]] = parent_element
    for node_id in tqdm(sorted(elements), desc="Converting elements into collection"):
        for property_name in ["ccm:hpi_searchable", "ccm:hpi_lom_general_aggregationlevel", "ccm:hpi_lom_relation"]:
            # Apply changes.
            edusharing_set_property(node_id, property_name, elements[node_id][property_name], auth_response)
        # edusharing_change_metadata(auth_response, node_id, "relation", elements[node_id]["relation"], is_array=True)