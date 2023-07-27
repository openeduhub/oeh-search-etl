import csv
import logging

import requests

from converter import env


class SodixSourcesHelperUtility:
    """
    Helper utility to collect an up-to-date SODIX 'source.id' and 'source.name' dictionary and write the data to a .csv
    file. (This is a temporary workaround until crawlers are able to write edu-sharing subdirectory titles in the same
    way that 'ccm:replicationsourceorigin' is written into the folder property 'cm:name').
    """

    logging.basicConfig(
        format="%(asctime)s\t%(levelname)s: %(message)s",
        level=logging.DEBUG,
    )

    @staticmethod
    def request_access_token():
        access_token = requests.post(
            "https://api.sodix.de/gql/auth/login",
            None,
            {
                "login": env.get("SODIX_SPIDER_USERNAME"),
                "password": env.get("SODIX_SPIDER_PASSWORD"),
            },
        ).json()["access_token"]
        return access_token

    @staticmethod
    def query_sources(access_token: str):
        url = "https://api.sodix.de/gql/graphql"
        payload = (
            '{"query":"query sources {\\n\\tsources {\\n\\t\\tid\\n\\t\\tname\\n\\t}\\n}\\n",'
            '"operationName":"sources"}'
        )
        authorization_str: str = f"Bearer {access_token}"
        headers = {
            "Content-Type": "application/json",
            "Authorization": authorization_str,
        }

        response = requests.request("POST", url, data=payload, headers=headers)
        response_dict = response.json()
        return response_dict

    @staticmethod
    def query_sources_count(access_token: str):
        url = "https://api.sodix.de/gql/graphql"
        payload = '{"query":"query countSources {\\n\\tcountSources\\n}","operationName":"countSources"}'
        authorization_str: str = f"Bearer {access_token}"
        headers = {
            "Content-Type": "application/json",
            "Authorization": authorization_str,
        }

        response = requests.request("POST", url, data=payload, headers=headers)
        logging.debug(response.text)
        response_dict: dict = response.json()
        sources_counter: str = response_dict["data"]["countSources"]
        return sources_counter

    @staticmethod
    def write_sources_to_csv(sources_response: dict):
        with open("sodix_sources.csv", mode="w") as csv_file:
            fieldnames = ["oldValue", "newValue"]
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()

            sources_list: list[dict] = sources_response["data"]["sources"]
            logging.info(
                f"Received a list of {len(sources_list)} sources from SODIX. Writing results to '.csv' ..."
            )
            for source in sources_list:
                source_id: str = source["id"]
                source_name: str = source["name"]
                writer.writerow({"oldValue": source_id, "newValue": source_name})
        pass

    # @staticmethod
    # def import_json_and_write_to_csv():
    #     with open("sodix_sources.csv", mode="w") as csv_file:
    #         fieldnames = ["oldValue", "newValue"]
    #         writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    #         writer.writeheader()
    #
    #         with open("sodix_sources_all.json") as json_file:
    #             data = json.load(json_file)
    #             sources_list: list[dict] = data["data"]["sources"]
    #             print(
    #                 f"Received a list of {len(sources_list)} sources from SODIX. Writing results to '.csv' ..."
    #             )
    #             for source in sources_list:
    #                 source_id: str = source["id"]
    #                 source_name: str = source["name"]
    #                 writer.writerow({"oldValue": source_id, "newValue": source_name})
    #             pass
    #     pass


def main():
    sodix_helper = SodixSourcesHelperUtility()
    access_token = sodix_helper.request_access_token()

    sources_dict_raw: dict = sodix_helper.query_sources(access_token=access_token)
    sodix_helper.write_sources_to_csv(sources_response=sources_dict_raw)

    expected_amount: str = sodix_helper.query_sources_count(access_token=access_token)
    logging.info(
        f"Expected amount of sources, according to SODIX 'countSources'-query: {expected_amount}"
    )
    pass


if __name__ == "__main__":
    main()
