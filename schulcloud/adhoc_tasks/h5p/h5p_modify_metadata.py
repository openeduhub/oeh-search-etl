import json
from typing import List

import edusharing
import requests.auth
import requests
import os
import converter.env as env
from converter.es_connector import EduSharing

ENV_VARS = ['EDU_SHARING_BASE_URL', 'EDU_SHARING_USERNAME', 'EDU_SHARING_PASSWORD']


def main():
    # ToDO: Authentification with edusharing.py
    # Authentification
    username = env.get('EDU_SHARING_USERNAME')
    password = env.get('EDU_SHARING_PASSWORD')
    base_url = env.get('EDU_SHARING_BASE_URL')
    headers = {'Accept': 'application/json'}
    session = requests.Session()
    session.auth = requests.auth.HTTPBasicAuth(username, password)

    # node_id of the H5P-element-folder
    folder_node_id = ""
    modify_metadata(base_url, session, headers, folder_node_id)


def modify_metadata(base_url, session, headers, folder_node_id):
    # add ccm:replicationsourceuuid
    property_name = "ccm:replicationsourceuuid"
    filename = "Fruits"
    property_value = EduSharing().buildUUID(filename + "-lernstore")

    if not (type(property_value) == list or type(property_value) == set):
        property_value = [property_value]

    uri = "rest/node/v1/nodes/-home-/" + folder_node_id + "/property?property=" + property_name + "&value=" + \
          '&value='.join(map(lambda x: str(x), property_value))
    url_metadata = base_url + uri

    s = session.request("POST", url_metadata, headers=headers, allow_redirects=False)

    print(url_metadata)
    print("Statuscode: " + str(s.status_code))
    if s.status_code != 200:
        print(s.json())


if __name__ == '__main__':
    main()
