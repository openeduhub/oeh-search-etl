# This file assumes all Sportinhalt videos have been manually uploaded to an Edu-Sharing directory, the node-id of which is provided in config.yml
import base64
import copy
import json
import os
from http.client import HTTPSConnection, HTTPResponse
from urllib.parse import urlparse

import requests
import yaml
from tqdm import tqdm

import converter.env as env
from converter.es_connector import EduSharing
from schulcloud.adhoc_tasks.upload_sportinhalt_brandenburg.sportinhalt_permissions import \
    edusharing_add_to_permission_groups, edusharing_get_permission_groups

import pathlib

# Load information required to connect to Edu-Sharing.
from schulcloud.adhoc_tasks.upload_sportinhalt_brandenburg.sportinhalt_utils import get_base_headers

username = env.get("EDU_SHARING_USERNAME")
password = env.get("EDU_SHARING_PASSWORD")

parsed_edusharing_url = urlparse(env.get("EDU_SHARING_BASE_URL"))
hostname = parsed_edusharing_url.hostname

user_and_pass = base64.b64encode((username + ':' + password).encode()).decode()

# Load configuration
current_path = pathlib.Path(__file__).parent.absolute()
config = yaml.safe_load(open(os.path.join(current_path, "config.yml")))

# Select directory for which to prepare its files
directory_node_id = config["directory_node_id"]

# General and subject-specific keywords.
general_keywords = config["general_keywords"]
keywords_per_chapter = config["keywords_per_chapter"]

# Used for the generation of ccm:replicationsourceuuid
salt = "-schulcloud"

def authenticate():
    at_uri = "/edu-sharing/rest/authentication/v1/validateSession"

    c = HTTPSConnection(hostname)
    headers = {'Authorization': 'Basic %s' % user_and_pass}
    c.request('GET', at_uri, headers=headers)

    res = c.getresponse()
    return res


def get_directory_elements(auth_response: HTTPResponse):
    at_uri = "/edu-sharing/rest/node/v1/nodes/-home-/" + directory_node_id + "/children?maxItems=500&skipCount=0"
    at_url = parsed_edusharing_url.scheme + "://" + hostname + at_uri

    headers = get_base_headers(auth_response)
    r = requests.request("GET", at_url, headers=headers, allow_redirects=False)

    response_dict = json.loads(r.text)

    node_id_to_reponse = {}

    for response in response_dict["nodes"]:
        if response["isDirectory"] is False:
            print(response["name"])
            node_id_to_reponse[response["ref"]["id"]] = response
    return node_id_to_reponse


def add_attributes_to_nodes(auth_response, node_id_to_response):
    attribute_values = {
        "ccm:hpi_searchable": "1",
        "ccm:hpi_lom_general_aggregationlevel": "1",
        "ccm:hpi_lom_relation": "{}",
        "ccm:wwwurl": None,
        "cclom:title": None,
        "ccm:replicationsource": "Brandenburg (Sportinhalt)",
        "ccm:replicationsourceuuid": None,
        "cclom:general_keyword": None
    }
    for node_id in tqdm(sorted(list(node_id_to_response.keys()), key=lambda x: node_id_to_response[x]["name"]),
                        desc="Adding properties to elements"):
        node_name = node_id_to_response[node_id]["name"]
        for k, v in attribute_values.items():
            if k == "ccm:wwwurl":
                property_name = k
                # property_value = node_id_to_reponse[node_id]["content"]["url"]
                property_value = node_id_to_response[node_id]["downloadUrl"]
                edusharing_change_metadata(node_id, property_name, property_value)

            elif k == "cclom:title":
                property_name = k
                property_value = get_filename(node_id, node_id_to_response)
                edusharing_change_metadata(node_id, property_name, property_value)

            elif k == "ccm:replicationsourceuuid":
                property_name = k

                filename = get_filename(node_id, node_id_to_response)
                property_value = EduSharing().buildUUID(filename + salt)

                edusharing_set_property(node_id, property_name, property_value, auth_response)

            elif k == "cclom:general_keyword":
                property_name = k

                filename = get_filename(node_id, node_id_to_response)

                # e.g.,
                # 01.1 Curriculum Erwaermung.mp4 --> 01.1 --> 01 --> 1
                # 0 Trailer.mp4 --> 0 --> 0 --> 0
                chapter = filename.split(" ")[0].split(".")[-1]

                property_value = copy.deepcopy(general_keywords)
                if chapter in keywords_per_chapter:
                    property_value += keywords_per_chapter[chapter]

                edusharing_change_metadata(node_id, property_name, property_value, True)

            else:
                property_name = k.replace(":", "%3A")
                property_value = str(v)
                edusharing_set_property(node_id, property_name, property_value, auth_response)


def get_filename(node_id, node_id_to_response):
    file = node_id_to_response[node_id]["name"]
    # Remove file extension
    filename = os.path.splitext(file)[0]

    # XXX: Decide to remove chapter prefix?
    # filename = " ".join(filename.split(" ")[1:])

    # Replace underscores with empty space
    filename = filename.replace("_", " ")

    # Replace non-umlaut form to umlaut
    filename = filename.replace("ae", "ä").replace("ue", "ü").replace("ö", "oe")
    property_value = filename

    return property_value


def edusharing_set_property(node_id, property_name, property_value, auth_response):
    headers = get_base_headers(auth_response)
    if type(property_value) == str:
        at_uri = "/edu-sharing/rest/node/v1/nodes/-home-/" + node_id + "/property?property=" + property_name + "&value=" + property_value
    elif type(property_value) == list or type(property_value) == set:
        at_uri = "/edu-sharing/rest/node/v1/nodes/-home-/" + node_id + "/property?property=" + property_name + "&value=" + \
            '&value='.join(map(lambda x: str(x), property_value))
    else:
        at_uri = "/edu-sharing/rest/node/v1/nodes/-home-/" + node_id + "/property?property=" + property_name + "&value=" + str(property_value)
    at_url = parsed_edusharing_url.scheme + "://" + hostname + at_uri
    r = requests.request("POST", at_url, headers=headers, allow_redirects=False)


def edusharing_change_metadata(node_id, key, value, is_array=False):
    headers = get_base_headers(auth_response)
    at_uri = "/edu-sharing/rest/node/v1/nodes/-home-/" + node_id + "/metadata"
    at_url = parsed_edusharing_url.scheme + "://" + hostname + at_uri

    if is_array is False:
        data = json.dumps({key: [value]})
    else:
        data = json.dumps({key: value})

    r = requests.request("PUT", at_url, data=data, headers=headers, allow_redirects=False)



def add_permissions_to_nodes(node_id_to_response, auth_response):
    """
    Add the right permissions, which should be also reflected to ccm:ph_invited on individual elements.
    """

    for node_id in tqdm(node_id_to_response.keys(), desc="Setting up permissions: "):
        # Get current permissions of a node.
        total_permissions, permissions_response_dict = edusharing_get_permission_groups(hostname, parsed_edusharing_url,
                                                                                        auth_response, node_id)

        # Add the remaining permissions that we require to the node.
        edusharing_add_to_permission_groups(config, hostname, auth_response, node_id, total_permissions,
                                            permissions_response_dict)


if __name__ == '__main__':
    auth_response = authenticate()

    print("Collecting elements.")
    node_id_to_response = get_directory_elements(auth_response)
    print("Collected " + str(len(node_id_to_response.keys())) + " elements.")

    add_attributes_to_nodes(auth_response, node_id_to_response)

    add_permissions_to_nodes(node_id_to_response, auth_response)
