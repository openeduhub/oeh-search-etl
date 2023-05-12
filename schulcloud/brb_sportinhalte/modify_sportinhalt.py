# This file assumes all Sportinhalt videos have been manually uploaded to an Edu-Sharing directory, the node-id of which is provided in config.yml
import copy
import os
from tqdm import tqdm

from converter.es_connector import EduSharing
from schulcloud.upload_sportinhalt_brandenburg.convert_to_collection import \
    identify_collections_in_directory, get_directory_elements, convert_to_collection

from schulcloud.upload_sportinhalt_brandenburg.sportinhalt_utils import get_configuration, get_api


def add_attributes_to_nodes(node):
    configuration = get_configuration()

    node_id = node['ref']['id']
    filename = get_clean_filename(node)
    # 01.1 Curriculum Erwaermung.mp4 --> 01.1 --> 01 --> 1
    # 0 Trailer.mp4 --> 0 --> 0 --> 0
    chapter = filename.split(" ")[0].split(".")[-1]
    keywords = list(configuration["general_keywords"])
    if chapter in configuration["keywords_per_chapter"]:
        keywords += configuration["keywords_per_chapter"][chapter]
    metadata = {
        'ccm:wwwurl': [node["downloadUrl"]],  # node["content"]["url"]
        'cclom:title': [filename],
        "ccm:replicationsource": ["Brandenburg (Sportinhalt)"],
        'ccm:replicationsourceuuid': [EduSharing().buildUUID(filename + configuration["salt"])],
        'cclom:general_keyword': keywords,
        "ccm:hpi_searchable": ["1"],
        "ccm:hpi_lom_general_aggregationlevel": ["1"],
        "ccm:hpi_lom_relation": ["{}"],
    }

    get_api().set_property(node_id, 'cm:edu_forcemetadataset', ['true'])
    for name in metadata:
        get_api().set_property(node_id, name, metadata[name])
    for property_name in metadata:
        node[property_name] = metadata[property_name]


def get_clean_filename(node):
    filename = os.path.splitext(node["name"])[0]

    # XXX: Decide to remove chapter prefix?
    # filename = " ".join(filename.split(" ")[1:])

    replacements = {
        '_': ' ',
        'ae': 'ä',
        'ue': 'ü',
        'oe': 'ö'
    }

    for old, repl in replacements.items():
        filename = filename.replace(old, repl)

    return filename


def process_collections():
    configuration = get_configuration()
    # Step 1
    print("Collecting elements.")
    # TODO: Identify directory structure
    collections = identify_collections_in_directory(configuration["directory_node_id"])
    print("Collected " + str(len(collections.keys())) + " collections.")

    # Step 2
    for key, value in collections.items():
        parent = value["parent"]
        directory = value["directory"]
        children = get_directory_elements(directory["ref"]["id"])

        # parent_and_children = copy.deepcopy(children)
        parent_and_children = copy.copy(children)
        parent_and_children[parent["ref"]["id"]] = parent

        for node_id in tqdm(sorted(list(parent_and_children.keys()), key=lambda x: parent_and_children[x]["name"]),
                            desc="Adding properties to elements"):
            add_attributes_to_nodes(parent_and_children[node_id])

        convert_to_collection(parent, children)

        for node_id in tqdm(parent_and_children.keys(), desc="Setting up permissions: "):
            get_api().set_permissions(node_id, [], True)


def process_non_collection_files():
    configuration = get_configuration()

    print("Collecting elements.")
    nodes = get_directory_elements(configuration["directory_node_id"])
    print("Collected " + str(len(nodes.keys())) + " elements.")

    for node_id in tqdm(sorted(list(nodes.keys()), key=lambda x: nodes[x]["name"]),
                        desc="Adding properties and permissions to elements"):
        add_attributes_to_nodes(nodes[node_id])
        get_api().set_permissions(node_id, [], True)


if __name__ == '__main__':
    configuration = get_configuration()

    if configuration["execution_mode"] == "collections":
        process_collections()
    else:
        process_non_collection_files()
