import logging
from pprint import pp

import requests
from converter import env
from loguru import logger


class EduSharingSourceTemplateHelper:
    """
    Helper class for retrieving (whitelisted) metadata properties from an edu-sharing crawler "source template"
    (= "Quellen-Datensatz"-Template) from a specified edu-sharing repository.
    The retrieved metadata properties will later be used as a fallback for crawler items when a crawler couldn't
    scrape a specific metadata property by itself.

    This feature REQUIRES an API endpoint in the edu-sharing repository (available in v8.1 or higher)!
    """

    _edu_sharing_base_url: str = "https://localhost:8000/edu-sharing/"
    _api_path: str = "rest/search/v1/queries/"
    _repository: str = "-home-"
    _meta_data_set: str = "mds_oeh"
    _api_endpoint: str = "wlo_crawler_element"
    _api_endpoint_params: str = "propertyFilter=-all-"
    _url: str = (
        f"{_edu_sharing_base_url}{_api_path}{_repository}"
        f"/{_meta_data_set}"
        f"/{_api_endpoint}?{_api_endpoint_params}"
    )

    _headers: dict = {
        "accept": "application/json",
        "Content-Type": "application/json",
    }
    _crawler_name: str = None
    _payload: dict = dict()

    # ToDo:
    #  - code cleanup (improve readability of logging messages)
    #  - implement pytest test-scenarios

    def __init__(self, crawler_name: str = None):
        """
        Initialize the 'source template'-helper class with the provided settings from the '.env'-file and prepare the
        API queryy.

        After initiating the EduSharingSourceTemplateHelper class,
        call "get_whitelisted_metadata_properties()" on its instance.
        Example:

        >>> esth = EduSharingSourceTemplateHelper(crawler_name="zum_klexikon_spider")
        >>> whitelisted_properties: dict = esth.get_whitelisted_metadata_properties()

        :param crawler_name: the spider_name ('spider.friendlyName'), e.g. "zum_klexikon_spider"
        """
        if crawler_name:
            self._set_crawler_name_for_payload(crawler_name=crawler_name)
        self._initiate_from_dotenv()
        self._build_payload()

    def _initiate_from_dotenv(self):
        edu_sharing_source_template_repository_from_dotenv: str = env.get(
            key="EDU_SHARING_SOURCE_TEMPLATE_BASE_URL", allow_null=True, default=None
        )
        edu_sharing_base_url_from_dot_env: str = env.get(key="EDU_SHARING_BASE_URL", allow_null=True, default=None)
        if edu_sharing_source_template_repository_from_dotenv:
            # explicitly specify from which edu-sharing repository a "Quellen-Datensatz"-Template should be retrieved
            # (e.g., if you're crawling against pre-Staging, but want to fetch the template from either Prod or Staging)
            self._set_edu_sharing_url(edu_sharing_source_template_repository_from_dotenv)
        elif edu_sharing_base_url_from_dot_env:
            # fallback for convenience: if no repository was explicitly set in the .env, we assume that the crawler
            # source template shall be fetched from the same edu-sharing repository that is used for storing the items
            # (e.g., crawling against production)
            self._set_edu_sharing_url(edu_sharing_base_url_from_dot_env)
        else:
            logger.info(
                f"Could not read '.env'-Setting 'EDU_SHARING_BASE_URL'. Please check your '.env'-file! "
                f"(For additional help, see: oeh-search-etl/converter/.env.example )."
            )
            pass

    def _set_edu_sharing_url(self, edu_sharing_source_template_repository: str):
        self._edu_sharing_base_url = edu_sharing_source_template_repository
        self._url = (
            f"{self._edu_sharing_base_url}{self._api_path}"
            f"{self._repository}/"
            f"{self._meta_data_set}/"
            f"{self._api_endpoint}?{self._api_endpoint_params}"
        )

    def _set_crawler_name_for_payload(self, crawler_name: str):
        self._crawler_name = crawler_name

    def _build_payload(self) -> dict | None:
        """
        Build JSON payload object. Class variable 'crawler_name' needs to be set beforehand.

        :return: payload object as 'dict' or None.
        """
        if self._crawler_name:
            payload: dict = {
                "criteria": [
                    {
                        "property": "ccm:general_identifier",
                        "values": [f"{self._crawler_name}"],
                    }
                ],
            }
            self._payload = payload
            return payload
        else:
            logger.error(
                f"Cannot build query payload without valid crawler_name. Please make sure that you instantiate "
                f"EduSharingTemplateHelper with a valid 'crawler_name'-parameter!"
            )
            return None

    def _retrieve_whitelisted_metadata_properties(self) -> dict | None:
        """
        Query the edu-sharing repository for a crawler 'source dataset'-template (= "Quellen-Datensatz"-Template) and
        return the whitelisted metadata properties as a dict.
        If the response was invalid for whatever reason, return None.

        :return: whitelisted metadata properties as dict or None.
        """
        response: requests.Response = requests.request("POST", url=self._url, json=self._payload, headers=self._headers)

        status_code: int = response.status_code
        if status_code == 200:
            # ToDo: even if the crawler_name doesn't exist, the edu-sharing response will be HTTP-Status-Code 200:
            #   - ALWAYS check validity of 'nodes' and 'pagination'! (-> 'nodes' is empty & 'pagination.count' == 0)
            try:
                result_dict = response.json()
            except requests.exceptions.JSONDecodeError as jde:
                logger.error(f"The edu-sharing response could not be parsed as JSON. Response:\n" f"{response.text}")
                raise jde

            try:
                pagination: dict = result_dict["pagination"]
                pagination_total = pagination["total"]
                pagination_count = pagination["count"]
            except KeyError:
                logger.error(
                    f"Missing 'pagination'-object in edu-sharing response. "
                    f"Aborting EduSharingSourceTemplateHelper process..."
                )
                raise KeyError

            if pagination_count and pagination_total and pagination_count == 1 and pagination_total == 1:
                # this is our happy case:
                # 'count' and 'total' should BOTH be 1 if there is a (valid) crawler source dataset
                pass
            else:
                # unexpected API behavior -> abort here by returning None
                logger.error(
                    f"The edu-sharing API returned an unexpected number of crawler 'source template' results:\n"
                    f"Expected 'pagination.count': 1 (received: {pagination_count} ) // "
                    f"expected 'pagination.total': 1 (received: {pagination_total} )"
                )
                if pagination_count == 0 and pagination_total == 0:
                    logger.error(
                        f"Please make sure that a 'source template' ('Quellen-Datensatz'-template) for crawler "
                        f"'{self._crawler_name}' exists within the specified edu-sharing repository "
                        f"{self._edu_sharing_base_url} !"
                    )
                if pagination_count > 1 or pagination_total > 1:
                    logger.error(
                        f"edu-sharing returned more than one 'crawler source template' for the specified "
                        f"crawler '{self._crawler_name}'. "
                    )
                return None

            nodes_list: list[dict] = result_dict["nodes"]
            if nodes_list and isinstance(nodes_list, list) and len(nodes_list) == 1:
                # 'nodes' should contain exactly 1 dict -> if more are returned, the API shows unexpected behaviour
                nodes: dict = nodes_list[0]
                nodes_properties: dict = nodes["properties"]
                _whitelisted_properties: dict = dict()
                _oeh_cdi: str = "ccm:oeh_crawler_data_inherit"
                """The property 'ccm:oeh_crawler_data_inherit' contains all whitelisted property keys, but NOT their 
                values!"""
                try:
                    if _oeh_cdi in nodes_properties:
                        # checking if "ccm:oeh_crawler_data_inherit" is part of the API response
                        # the whitelist-property should be available within 'nodes[0].properties' and might look like:
                        # "ccm:oeh_crawler_data_inherit": [
                        # 					"ccm:containsAdvertisement",
                        # 					"ccm:oeh_quality_login",
                        # 					"ccm:oeh_languageTarget",
                        # 					"ccm:oeh_languageLevel"
                        # 				]
                        whitelist_keys: list[str] = nodes_properties[_oeh_cdi]
                        logger.info(f"'{_oeh_cdi}' contains the following properties: \n" f"{whitelist_keys}")
                        if whitelist_keys and isinstance(whitelist_keys, list):
                            for whitelist_key in whitelist_keys:
                                # the values for each property need to be looked up separately
                                whitelisted_property_value: list[str] = nodes_properties.get(whitelist_key)
                                # ToDo: implement check for empty properties / strings?
                                #  OR: trust that the edu-sharing API response is always valid?
                                if whitelisted_property_value:
                                    _whitelisted_properties.update({f"{whitelist_key}": whitelisted_property_value})
                        else:
                            logger.error(
                                f"Received unexpected value type of metadata property '{_oeh_cdi}': "
                                f"{type(whitelist_keys)} . (Expected type: 'list[str]')"
                            )
                    else:
                        logger.error(
                            f"Could not find '{_oeh_cdi}' in edu-sharing API response. "
                            f"Source template retrieval FAILED!"
                        )
                        logger.debug(response.text)
                except KeyError as ke:
                    raise ke

                # the result dict with all whitelisted metadata properties might look like this example:
                # _whitelisted_properties = {
                #     "ccm:oeh_quality_login": ["1"],
                #     "ccm:oeh_quality_protection_of_minors": ["0"],
                #     "ccm:taxonid": [
                #         "http://w3id.org/openeduhub/vocabs/discipline/720",
                #         "http://w3id.org/openeduhub/vocabs/discipline/120",
                #     ],
                #     "cclom:general_keyword": ["Kinderlexikon", "Lexikon"],
                # }

                return _whitelisted_properties
            else:
                logger.error(
                    f"edu-sharing API returned an unexpected 'nodes'-object:"
                    f"Expected list[dict] of length 1, received length: {len(nodes_list)} .\n"
                    f"Please make sure that a 'source template' ('Quellendatensatz'-template) for crawler "
                    f"{self._crawler_name} exists within the edu-sharing repository {self._edu_sharing_base_url} !"
                )
                return None
        else:
            # sad-case: we catch unexpected HTTP responses here
            logger.error(
                f"Received unexpected HTTP response (status code: {status_code} ) from the edu-sharing "
                f"repository while trying to retrieve whitelisted 'source template'-metadata-properties."
            )
            if status_code == 401:
                # ToDo: specify exact edu-sharing version that provides the necessary API endpoint
                logger.error(
                    f"edu-sharing API returned HTTP Status Code {status_code}. "
                    f"(This might happen when the necessary API endpoint might not be available (yet) in the "
                    f"edu-sharing repository (edu-sharing v8.1+ required).)"
                )
            if status_code == 500:
                # code 500 might be accompanied by 'java.lang.NullPointerException' -> print whole response
                # happens when the payload of our submitted request was empty
                logger.error(f"edu-sharing API returned HTTP status code {status_code}:\n" f"{response.text}")
                response.raise_for_status()
            # ToDo: extend Error-Handling for additional edge-cases (as / if they occur)
            return None

    def get_whitelisted_metadata_properties(self) -> dict | None:
        """
        Retrieve whitelisted metadata properties from a specified edu-sharing repository by using a 'source template'
        (= "Quellen-Datensatz"-Template) which is expected to contain a "ccm:oeh_crawler_data_inherit"-property.

        :return: a 'dict' containing whitelisted metadata property key-value pairs or None
        """
        # check user-defined .env Setting first if 'crawler source dataset' should be ignored:
        est_enabled: bool = env.get_bool(key="EDU_SHARING_SOURCE_TEMPLATE_ENABLED", allow_null=True, default=None)
        if est_enabled:
            logger.info(
                f".env setting 'EDU_SHARING_SOURCE_TEMPLATE_ENABLED' is ACTIVE. Trying to retrieve whitelisted "
                f"properties..."
            )
            self._payload = self._build_payload()
            if self._payload:
                whitelisted_properties: dict = self._retrieve_whitelisted_metadata_properties()
                if whitelisted_properties:
                    return whitelisted_properties
                else:
                    # intentionally raising a ValueError to stop a crawl process when the 'source template'-setting
                    # is active. (If the .env variable is explicitly set, we expect whitelisted properties to be
                    # available and DO NOT want to crawl without them.)
                    raise ValueError(
                        "Failed to retrieve whitelisted metadata properties from edu-sharing "
                        "'source template' (= 'Quellendatensatz-Template')! "
                        "Aborting crawl process..."
                    )
            else:
                logger.error(
                    f"Could not build payload object to retrieve 'source template'-properties from "
                    f"edu-sharing repository. "
                    f"\nJSON Payload for crawler_name '{self._crawler_name}' was:\n"
                    f"{self._payload}"
                    f"\n(payload REQUIRES a valid 'crawler_name'!)"
                )
                logger.info(
                    "Aborting crawl... (If you didn't mean to retrieve an edu-sharing 'source template', please "
                    "set the .env variable 'EDU_SHARING_SOURCE_TEMPLATE_ENABLED' to False!)"
                )
                return None
        else:
            # if the setting is explicitly disabled, do nothing -> continue with normal crawler behaviour
            logger.info(
                f"Recognized '.env'-Setting EDU_SHARING_SOURCE_TEMPLATE_ENABLED: '{est_enabled}'.\n"
                f"Crawler source dataset will be IGNORED. Continuing with default crawler behaviour..."
            )
            return None


if __name__ == "__main__":
    crawler_name_for_testing: str = "zum_deutschlernen_spider"
    # crawler_name_for_testing: str = "does_not_exist_spider"
    est_helper: EduSharingSourceTemplateHelper = EduSharingSourceTemplateHelper(crawler_name=crawler_name_for_testing)
    whitelisted_props: dict | None = est_helper.get_whitelisted_metadata_properties()
    print("Whitelisted properties: ")
    pp(whitelisted_props, indent=4)
