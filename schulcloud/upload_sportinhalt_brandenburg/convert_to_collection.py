from tqdm import tqdm

from schulcloud.upload_sportinhalt_brandenburg.sportinhalt_utils import get_api


def identify_collections_in_directory(directory_node_id: str):
    """
    This is a method to identify and return any collections in a given directory node id.

    We *only* consider combinations of directories, which contain the children of a given collection, and files,
     which are the parents of the aforementioned collections. All remaining files and directories will be ignored.
    """
    nodes = get_api().get_children(directory_node_id)

    collections = {}
    for node in nodes:
        # Directory or filename (removing any extensions).
        name = node.name.rsplit(".", 1)[0]
        if name not in collections:
            collections[name] = {}
        if node.is_directory:
            collections[name]["directory"] = node.obj
        else:
            collections[name]["parent"] = node.obj

    full_collections = {}
    for key in collections:
        if len(collections[key]) > 1:
            full_collections[key] = collections[key]

    return full_collections


def get_directory_elements(directory_node_id: str):
    nodes = get_api().get_children(directory_node_id)
    nodes_by_id = {}

    for node in nodes:
        if not node.is_directory:
            print(node.name)
            nodes_by_id[node.id] = node.obj
    return nodes_by_id


def convert_to_collection(parent_element, children_elements):
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
            get_api().set_property(node_id, property_name, [elements[node_id][property_name]])
        # edusharing_change_metadata(auth_response, node_id, "relation", elements[node_id]["relation"], is_array=True)
