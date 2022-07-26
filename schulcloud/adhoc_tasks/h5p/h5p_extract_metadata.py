
import os
import re
import zipfile
from typing import List, Union, IO

import openpyxl


class Metadata:
    def __init__(self, title: str, publisher: str, keywords: List[str], order: str, rating: str, collection: str):
        self.title = title
        self.publisher = publisher
        self.keywords = keywords
        self.order = order
        self.rating = rating
        self.collection = collection


class MetadataFile:
    def __init__(self, file: Union[str, IO]):
        self.workbook = openpyxl.load_workbook(filename=file, data_only=True)
        self.o_sheet = self.workbook["Tabelle1"]

    def get_metadata(self, h5p_file: str):
        for i in range(1, self.o_sheet.max_row + 1):
            file_name_sheet = self.o_sheet.cell(row=i, column=5)

            if file_name_sheet.value == h5p_file:
                collection = self.o_sheet.cell(row=i, column=1).value
                order = self.o_sheet.cell(row=i, column=2).value
                rating = self.o_sheet.cell(row=i, column=3).value
                title = self.o_sheet.cell(row=i, column=4).value
                keywords = self.o_sheet.cell(row=i, column=6).value
                publisher = self.o_sheet.cell(row=i, column=7).value

                # TODO: validate all data coming from excel file

                keywords = re.findall(r'[^,; ]+', keywords)
                break
        else:
            raise RuntimeError(f'No metadata found for {h5p_file}')

        return Metadata(title, publisher, keywords, order, rating, collection)
