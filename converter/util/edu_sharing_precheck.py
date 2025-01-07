import requests
from converter import env
from loguru import logger


class EduSharingPreCheck:
    """
    Helper class to continue previously aborted crawl processes where they left off (instead of crawling from the start
    and checking/updating each item individually during the parse method). Gathers 'ccm:replicationsourceid's from a
    pre-defined "saved search"-node-ID.

    Depending on the size of your "saved search", this pre-check might take a while. Each API response typically takes
    about ~12s and is NOT controlled by Scrapy's program flow.

    Please make sure that your .env file has (valid) settings for:
    EDU_SHARING_BASE -> this is typically the edu-sharing repository that you previously crawled against
    EDU_SHARING_PRECHECK_SAVED_SEARCH_ID -> the node-ID of a "saved search" needs to be created within the edu-sharing
    web-interface and can be looked up via the "debug"-view.
    """

    edu_sharing_url = "https://localhost:8000/edu-sharing/"
    # the edu_sharing_url will typically look like this:
    # "https://localhost:8000/edu-sharing/rest/search/v1/queries/load/f702baeb-c0c5-4abc-9171-95f9a5d3fac9"
    # "<base_url><edu_sharing_rest_api_path><saved_search_node_id>"

    edu_sharing_rest_api_path = "rest/search/v1/queries/load/"
    saved_search_node_id = "<nodeID_of_a_saved_search>"
    max_item_parameter = 500  # ToDo: keep an eye on connection timeouts depending on the request size
    skip_item_parameter = 0
    # ToDo: .env variables -> .env.example documentation
    # ToDo: (optional feature) caching to local file, so we don't have to wait every time for the full API Pagination

    querystring = {
        "contentType": "FILES",
        "propertyFilter": "ccm:replicationsourceid",
        "maxItems": f"{max_item_parameter}",
        f"skipCount": f"{skip_item_parameter}",
        "sortProperties": "cm:created",
        "sortAscending": "true",
    }

    payload = ""

    replication_source_id_list: list[str] = list()

    def __init__(self):
        self.set_edu_sharing_url_from_dot_env()
        self.build_query_string()

    def set_edu_sharing_url_from_dot_env(self):
        """
        Checks the '.env'-file for two required variables:
        EDU_SHARING_BASE_URL & EDU_SHARING_PRECHECK_SAVED_SEARCH_ID
        and sets the class member variable for API Pagination.
        """
        edu_sharing_url: str = env.get("EDU_SHARING_BASE_URL", True, None)
        saved_search_node_id: str = env.get("EDU_SHARING_PRECHECK_SAVED_SEARCH_ID", True, None)
        logger.info(
            f"PreCheck utility warmup: Checking '.env'-file for EDU_SHARING_BASE_URL and "
            f"EDU_SHARING_PRECHECK_SAVED_SEARCH_ID ..."
        )
        if edu_sharing_url and saved_search_node_id:
            url_combined: str = f"{edu_sharing_url}{self.edu_sharing_rest_api_path}{saved_search_node_id}"
            logger.info(
                f"PreCheck utility: Recognized .env settings for CONTINUED crawl. Assembled URL string: "
                f"{url_combined}"
            )
            self.edu_sharing_url = url_combined
            self.saved_search_node_id = saved_search_node_id
        else:
            logger.error(
                f"PreCheck utility: Could not retrieve valid .env settings for EDU_SHARING_BASE and "
                f"EDU_SHARING_PRECHECK_SAVED_SEARCH_ID. Please make sure that both settings are valid if "
                f"you want to COMPLETE/COMPLEMENT a previously aborted crawl."
            )

    def build_query_string(self):
        self.querystring = {
            "contentType": "FILES",
            "propertyFilter": "ccm:replicationsourceid",
            "maxItems": f"{self.max_item_parameter}",
            f"skipCount": f"{self.skip_item_parameter}",
            "sortProperties": "cm:created",
            "sortAscending": "true",
        }

    def collect_replication_source_ids_from_nodes(self, response: requests.Response):
        """
        Collects the 'ccm:replicationsourceid'-values from each node of the edu-sharing API response and queries the
        next API page.
        """
        json_response = response.json()
        nodes: list[dict] = json_response["nodes"]
        logger.info(f"Collecting 'ccm:replicationsourceid's from: {response.url}")
        if nodes:
            # as long as there are nodes, we haven't reached the final page of the API yet.
            for node in nodes:
                if "properties" in node:
                    id_list = node["properties"]["ccm:replicationsourceid"]
                    for replication_source_id in id_list:
                        if replication_source_id not in self.replication_source_id_list:
                            # since Python sets are more memory-expensive than lists, this basic if-check will do.
                            self.replication_source_id_list.append(replication_source_id)
            self.query_next_page()
        else:
            logger.info(
                f"Reached the last API page: {response.url} // \nTotal amount of ids collected: {len(self.replication_source_id_list)}"
            )

    def query_next_page(self):
        """
        Increments the API Pagination offset as specified by the 'max_item_parameter' and queries the next API page.
        """
        self.skip_item_parameter += self.max_item_parameter
        self.build_query_string()
        next_api_page: requests.Response = requests.request(
            "GET", self.edu_sharing_url, data=self.payload, params=self.querystring
        )
        self.collect_replication_source_ids_from_nodes(next_api_page)

    def try_to_retrieve_replication_source_id_list(self) -> list[str] | None:
        """
        If everything went smooth during API pagination, sorts the list of strings and returns it.
        If the list is empty for some reason, logs a warning.

        @return: a list of 'ccm:replicationsourceid's or None

        """
        if self.replication_source_id_list:
            logger.info(
                f"PreCheck utility: Successfully collected {len(self.replication_source_id_list)} "
                f"'ccm:replicationsourceid'-strings."
            )
            self.replication_source_id_list.sort()
            return self.replication_source_id_list
        else:
            logger.warning(
                f"PreCheck utility: The list of 'ccm:replicationsourceid'-strings appears to be empty. "
                f"This might happen if the API Pagination is interrupted by connection problems to the "
                f"edu-sharing repo."
            )

    def get_replication_source_id_list(self) -> list[str]:
        """
        The main loop of the edu-sharing PreCheck helper utility class. Use this method if you just want to grab a list
        of 'ccm:replicationsourceid's for a given "saved search"-nodeID.

        @return: a sorted list of 'ccm:replicationsourceid's

        """
        expected_response = requests.request("GET", self.edu_sharing_url, data=self.payload, params=self.querystring)
        self.collect_replication_source_ids_from_nodes(expected_response)
        sorted_result_list = self.try_to_retrieve_replication_source_id_list()
        return sorted_result_list


if __name__ == "__main__":
    es_id_collector = EduSharingPreCheck()
    replication_source_ids: list[str] = es_id_collector.get_replication_source_id_list()
    print(replication_source_ids)
