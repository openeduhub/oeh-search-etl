import os
import zipfile
import json
import shutil
from typing import Dict
import openpyxl


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
            "copyright_license": ""
        }

        try:
            metadata_h5p["title"] = metadata["title"]
            metadata_h5p["copyright_license"] = metadata["license"]
        except KeyError:
            print(f'KeyError: The JSON schema of the file doesn\'t match with the method schema.')

        return metadata_h5p

    def extract_metadata_from_excel(excel_file_path: str, file_name: str):
        metadata_h5p = {
            "package": "",
            "order": "",
            "task": "",
            "keywords": ""
        }

        wb = openpyxl.load_workbook(filename=excel_file_path, data_only=True)
        o_sheet = wb["Tabelle1"]

        for i in range(1, o_sheet.max_row + 1, 1):
            file_name_sheet = o_sheet.cell(row=i, column=4)

            if file_name_sheet.value == file_name:
                metadata_h5p["package"] = o_sheet.cell(row=i, column=1).value
                metadata_h5p["order"] = o_sheet.cell(row=i, column=2).value
                metadata_h5p["task"] = o_sheet.cell(row=i, column=3).value
                metadata_h5p["keywords"] = o_sheet.cell(row=i, column=5).value

        return metadata_h5p


def main():
    # create local folder 'unzipped'
    UnzipLocalFile.create_local_folder(folder_name='unzipped')
    print("Create folder \'unzipped\'.")

    # unzip the h5p-file
    h5p_file = "alice.h5p"
    UnzipLocalFile.unzip_local_file(file_path=f"h5p_files/{h5p_file}", unzipped_dir="unzipped")

    # read out the lines, e.g. title
    metadata = json.loads(UnzipLocalFile.read_file(file_path="unzipped/h5p.json"))
    metadata_h5p = UnzipLocalFile.extract_metadata_from_json(metadata=metadata)

    print(metadata)
    print(f'title: {metadata_h5p["title"]}')
    print(f'copyright_license: {metadata_h5p["copyright_license"]}')

    # delete the 'unzipped'-folder including all files
    UnzipLocalFile.delete_local_folder(folder_name="unzipped")
    print("Delete folder \'unzipped\'")

    # extract metadata from excel_file
    file_name = "bio7v2_17_koerpermerkmale-von-schnecken-interaktive-wissensvermittlung.h5p"
    excel_file_path = 'h5p_files/Biologie 7 Vol 2 - Wirbellose.xlsx'

    metadata_excel = UnzipLocalFile.extract_metadata_from_excel(excel_file_path=excel_file_path, file_name=file_name)
    print(metadata_excel)


if __name__ == '__main__':
    main()
