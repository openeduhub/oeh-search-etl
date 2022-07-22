import os
import zipfile
import shutil
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

    def extract_metadata_from_excel(excel_file_path: str, file_name: str):
        metadata_h5p = {
            "collection": "",
            "order": "",
            "title": "",
            "keywords": "",
            "publisher": ""
        }

        wb = openpyxl.load_workbook(filename=excel_file_path, data_only=True)
        o_sheet = wb["Tabelle1"]

        for i in range(1, o_sheet.max_row + 1, 1):
            file_name_sheet = o_sheet.cell(row=i, column=5)

            if file_name_sheet.value == file_name:
                metadata_h5p["collection"] = o_sheet.cell(row=i, column=1).value
                metadata_h5p["order"] = o_sheet.cell(row=i, column=2).value
                metadata_h5p["title"] = o_sheet.cell(row=i, column=4).value
                metadata_h5p["keywords"] = o_sheet.cell(row=i, column=6).value
                metadata_h5p["publisher"] = o_sheet.cell(row=i, column=7).value

        return metadata_h5p

