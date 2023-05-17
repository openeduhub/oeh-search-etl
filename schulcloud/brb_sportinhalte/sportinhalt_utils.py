import base64
import os
import pathlib
from http.client import HTTPSConnection
from urllib.parse import urlparse

import requests
import requests.auth
import json
import yaml

import converter.env as env
from schulcloud.edusharing import EdusharingAPI


api = None


def get_api():
    global api
    if not api:
        configuration = get_configuration()
        api = EdusharingAPI(
            configuration['parsed_edusharing_url'].geturl(),
            configuration['username'],
            configuration['password']
        )
    return api


def edusharing_set_property2(node_id, property_name, property_value, auth_response):
    configuration = get_configuration()
    session = get_session()

    if type(property_value) not in (list, set):
        property_value = [property_value]

    at_uri = "/edu-sharing/rest/node/v1/nodes/-home-/" + node_id + "/property?property=" + property_name + "&value=" + \
            '&value='.join(map(lambda x: str(x), property_value))

    at_url = configuration["parsed_edusharing_url"].scheme + "://" + configuration["hostname"] + at_uri
    r = session.request("POST", at_url, allow_redirects=False)
    if r.status_code != 200:
        print("Problem with " + node_id + " when setting " + property_name + " to " + str(property_value) + "\n")
        print(r.text)


def edusharing_change_metadata2(auth_response, node_id, key, value, is_array=False):
    headers = get_base_headers(auth_response)
    configuration = get_configuration()

    at_uri = "/edu-sharing/rest/node/v1/nodes/-home-/" + node_id + "/metadata"
    at_url = configuration["parsed_edusharing_url"].scheme + "://" + configuration["hostname"] + at_uri

    if not is_array:
        data = json.dumps({key: [value]})
    else:
        data = json.dumps({key: value})

    r = requests.request("PUT", at_url, data=data, headers=headers, allow_redirects=False)


def get_configuration():
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

    execution_mode = config["execution_mode"]

    # General and subject-specific keywords.
    general_keywords = config["general_keywords"]
    keywords_per_chapter = config["keywords_per_chapter"]

    # Used for the generation of ccm:replicationsourceuuid
    salt = "-schulcloud"

    configuration = {
      "username": username,
      "password": password,
      "parsed_edusharing_url": parsed_edusharing_url,
      "hostname": hostname,
      "user_and_pass": user_and_pass,
      "current_path": current_path,
      "config": config,
      "directory_node_id": directory_node_id,
      "general_keywords": general_keywords,
      "keywords_per_chapter": keywords_per_chapter,
      "salt": salt,
      "execution_mode": execution_mode
    }
    return configuration
