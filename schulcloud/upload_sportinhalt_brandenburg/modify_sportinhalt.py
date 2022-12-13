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


from converter.es_connector import EduSharing
from schulcloud.upload_sportinhalt_brandenburg.convert_to_collection import \
    identify_collections_in_directory, get_directory_elements, convert_to_collection
from schulcloud.upload_sportinhalt_brandenburg.sportinhalt_permissions import \
    edusharing_add_to_permission_groups, edusharing_get_permission_groups

import pathlib

# Load information required to connect to Edu-Sharing.
from schulcloud.upload_sportinhalt_brandenburg.sportinhalt_utils import get_base_headers, get_configuration, \
    authenticate, edusharing_change_metadata, edusharing_set_property


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
    configuration = get_configuration()

    for node_id in tqdm(sorted(list(node_id_to_response.keys()), key=lambda x: node_id_to_response[x]["name"]),
                        desc="Adding properties to elements"):
        node_name = node_id_to_response[node_id]["name"]
        for k, v in attribute_values.items():
            if k == "ccm:wwwurl":
                property_name = k
                # property_value = node_id_to_reponse[node_id]["content"]["url"]
                property_value = node_id_to_response[node_id]["downloadUrl"]
                edusharing_change_metadata(auth_response, node_id, property_name, property_value)

            elif k == "cclom:title":
                property_name = k
                property_value = get_filename(node_id, node_id_to_response)
                edusharing_change_metadata(auth_response,node_id, property_name, property_value)

            elif k == "ccm:replicationsourceuuid":
                property_name = k
                # property_name = k.replace(":", "%3A")

                filename = get_filename(node_id, node_id_to_response)
                property_value = EduSharing().buildUUID(filename + configuration["salt"])

                edusharing_set_property(node_id, property_name, property_value, auth_response)

            elif k == "cclom:general_keyword":
                property_name = k

                filename = get_filename(node_id, node_id_to_response)

                # e.g.,
                # 01.1 Curriculum Erwaermung.mp4 --> 01.1 --> 01 --> 1
                # 0 Trailer.mp4 --> 0 --> 0 --> 0
                chapter = filename.split(" ")[0].split(".")[-1]

                property_value = copy.deepcopy(configuration["general_keywords"])
                if chapter in configuration["keywords_per_chapter"]:
                    property_value += configuration["keywords_per_chapter"][chapter]

                edusharing_change_metadata(auth_response, node_id, property_name, property_value, True)

            else:
                property_name = k.replace(":", "%3A")
                property_value = str(v)
                edusharing_set_property(node_id, property_name, property_value, auth_response)
            node_id_to_response[node_id][k] = property_value


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



def add_permissions_to_nodes(auth_response, node_id_to_response):
    """
    Add the right permissions, which should be also reflected to ccm:ph_invited on individual elements.
    """
    configuration = get_configuration()

    for node_id in tqdm(node_id_to_response.keys(), desc="Setting up permissions: "):
        # Get current permissions of a node.
        total_permissions, permissions_response_dict = edusharing_get_permission_groups(configuration["hostname"],
                                                        configuration["parsed_edusharing_url"], auth_response, node_id)

        # Add the remaining permissions that we require to the node.
        edusharing_add_to_permission_groups(configuration["config"], configuration["hostname"], auth_response, node_id, total_permissions,
                                            permissions_response_dict)


def process_collections():
    auth_response = authenticate()

    configuration = get_configuration()
    # Step 1
    print("Collecting elements.")
    # TODO: Identify directory structure
    collections = identify_collections_in_directory(auth_response, configuration["directory_node_id"])
    print("Collected " + str(len(collections.keys())) + " collections.")

    # Step 2
    for key, value in collections.items():
        parent = value["parent"]
        directory = value["directory"]
        children = get_directory_elements(auth_response, directory["ref"]["id"])

        # parent_and_children = copy.deepcopy(children)
        parent_and_children = copy.copy(children)
        parent_and_children[parent["ref"]["id"]] = parent

        add_attributes_to_nodes(auth_response, parent_and_children)

        convert_to_collection(auth_response, parent, children)

        add_permissions_to_nodes(auth_response, parent_and_children)


def process_non_collection_files():
    auth_response = authenticate()

    configuration = get_configuration()

    print("Collecting elements.")
    node_id_to_response = get_directory_elements(auth_response, configuration["directory_node_id"])
    print("Collected " + str(len(node_id_to_response.keys())) + " elements.")

    add_attributes_to_nodes(auth_response, node_id_to_response)
    add_permissions_to_nodes(auth_response, node_id_to_response)

if __name__ == '__main__':
    configuration = get_configuration()

    if configuration["execution_mode"] == "collections":
        process_collections()
    else:
        process_non_collection_files()
