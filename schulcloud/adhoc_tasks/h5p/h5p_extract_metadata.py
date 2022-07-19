import os
import zipfile
import json
import shutil
from typing import Dict


class UnzipLocalFile:

    def __init__(self):
        pass

    def create_local_folder(folder_name: str):
        os.mkdir(f'{folder_name}')

    def delete_local_folder(folder_name: str):
        shutil.rmtree(f'{folder_name}')

    def unzip_local_file(file_path: str, unzipped_dir: str):
        with zipfile.ZipFile(f'{file_path}', 'r') as zip_ref:
            zip_ref.extractall(f'{unzipped_dir}')

    def read_file(file_path: str):
        file = open(f'{file_path}')
        data = file.read()
        file.close()
        return data

    def extract_metadata_from_json(metadata: [Dict]):
        metadata_h5p = {
            "title": "",
            "download_url": "",
            "copyright_license": "",
            "author": "",
            "ext_source": ""
        }

        # ToDO: Check if this schema is the same for all h5p-files (content.json).
        #  If not, create JSON-attribute-search-method.

        try:
            metadata_h5p["title"] = metadata["interactiveVideo"]["video"]["files"][0]["copyright"]["title"]
            metadata_h5p["download_url"] = metadata["interactiveVideo"]["video"]["files"][0]["path"]
            metadata_h5p["copyright_license"] = metadata["interactiveVideo"]["video"]["files"][0]["copyright"]["license"]
            metadata_h5p["author"] = metadata["interactiveVideo"]["video"]["files"][0]["copyright"]["author"]
            metadata_h5p["ext_source"] = metadata["interactiveVideo"]["video"]["files"][0]["copyright"]["source"]
        except KeyError:
            print(f'KeyError: The JSON schema of the file doesn\'t match with the method schema.')

        return metadata_h5p


def main():
    # create local folder 'unzipped'
    UnzipLocalFile.create_local_folder(folder_name='unzipped')
    print("Create folder \'unzipped\'.")

    # unzip the h5p-file
    h5p_file = "alice.h5p"
    UnzipLocalFile.unzip_local_file(file_path=f"h5p_files/{h5p_file}", unzipped_dir="unzipped")

    # read out the lines, e.g. title
    metadata = json.loads(UnzipLocalFile.read_file(file_path="unzipped/content/content.json"))
    metadata_h5p = UnzipLocalFile.extract_metadata_from_json(metadata=metadata)

    print(metadata)
    print(f'title: {metadata_h5p["title"]}')
    print(f'download_url: {metadata_h5p["download_url"]}')
    print(f'copyright_license: {metadata_h5p["copyright_license"]}')
    print(f'author: {metadata_h5p["author"]}')
    print(f'external_source: {metadata_h5p["ext_source"]}')

    # delete the 'unzipped'-folder including all files
    UnzipLocalFile.delete_local_folder(folder_name="unzipped")
    print("Delete folder \'unzipped\'")


if __name__ == '__main__':
    main()
