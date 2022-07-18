import os
import zipfile
import json
import shutil


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


def main():
    # create local folder 'unzipped'
    UnzipLocalFile.create_local_folder(folder_name='unzipped')
    print("Create folder \'unzipped\'.")

    # unzip the h5p-file
    UnzipLocalFile.unzip_local_file(file_path="h5p_files/bob.h5p", unzipped_dir="unzipped")

    # read out the lines, e.g. title
    metadata = json.loads(UnzipLocalFile.read_file(file_path="unzipped/content/content.json"))

    # ToDO: Check if this schema is the same for all h5p-files (content.json).
    #  If not, create JSON-attribute-search-method.
    title = metadata["interactiveVideo"]["video"]["files"][0]["copyright"]["title"]
    download_url = metadata["interactiveVideo"]["video"]["files"][0]["path"]
    copyright_licence = metadata["interactiveVideo"]["video"]["files"][0]["copyright"]["license"]
    author = metadata["interactiveVideo"]["video"]["files"][0]["copyright"]["author"]
    ext_source = metadata["interactiveVideo"]["video"]["files"][0]["copyright"]["source"]

    print(metadata)
    print(f'title: {title}')
    print(f'download_url: {download_url}')
    print(f'copyright_license: {copyright_licence}')
    print(f'author: {author}')
    print(f'external_source: {ext_source}')

    # delete the 'unzipped'-folder including all files
    UnzipLocalFile.delete_local_folder(folder_name="unzipped")
    print("Delete folder \'unzipped\'")


if __name__ == '__main__':
    main()
