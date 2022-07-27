
import os
import re
import sys
import zipfile
from typing import List, Union, IO

import openpyxl
from openpyxl.utils import get_column_letter

class Metadata:
    def __init__(self, title: str, publisher: str, keywords: List[str], order: str, rating: str, collection: str):
        self.title = title
        self.publisher = publisher
        self.keywords = keywords
        self.order = order
        self.rating = rating
        self.collection = collection


class MetadataFile:
    class COLUMN:
        COLLECTION = 1
        ORDER = 2
        RATING = 3
        TITLE = 4
        FILENAME = 5
        KEYWORDS = 6
        PUBLISHER = 7
        COUNT = 7

    def __init__(self, file: Union[str, IO]):
        self.workbook = openpyxl.load_workbook(filename=file, data_only=True)
        self.o_sheet = self.workbook["Tabelle1"]
        self.validate_sheet()

    def validate_sheet(self):
        collection = self.get_collection()
        for row in range(1, self.o_sheet.max_row + 1):
            for column in range(1, self.COLUMN.COUNT + 1):
                if column == self.COLUMN.KEYWORDS:
                    continue
                if not self.o_sheet.cell(row=row, column=column).value:
                    raise ParsingError(f'Empty cell: {get_column_letter(column)}{row}')
        if not collection:
            raise ParsingError('No collection')
        for row in range(1, self.o_sheet.max_row + 1):
            other_collection = self.o_sheet.cell(row=row, column=self.COLUMN.COLLECTION).value
            if not other_collection == collection:
                raise ParsingError('Multiple collection in one excel file')

    def check_for_files(self, filenames: List[str]):
        existing_filenames = []
        missing_filenames = []
        for row in range(1, self.o_sheet.max_row + 1):
            existing_filenames.append(self.o_sheet.cell(row=row, column=self.COLUMN.FILENAME).value)
        for filename in filenames:
            if filename not in existing_filenames:
                missing_filenames.append(filename)
        if missing_filenames:
            print('Missing in excel file:', file=sys.stderr)
            for filename in missing_filenames:
                print(f'  {filename}', file=sys.stderr)
            raise ParsingError('The excel file is missing metadata')

    def get_collection(self):
        return self.o_sheet.cell(row=1, column=self.COLUMN.COLLECTION).value

    def get_metadata(self, h5p_file: str):
        for row in range(1, self.o_sheet.max_row + 1):
            file_name_sheet = self.o_sheet.cell(row=row, column=self.COLUMN.FILENAME)

            if file_name_sheet.value == h5p_file:
                collection = self.o_sheet.cell(row=row, column=self.COLUMN.COLLECTION).value
                order = self.o_sheet.cell(row=row, column=self.COLUMN.ORDER).value
                rating = self.o_sheet.cell(row=row, column=self.COLUMN.RATING).value
                title = self.o_sheet.cell(row=row, column=self.COLUMN.TITLE).value
                keywords = self.o_sheet.cell(row=row, column=self.COLUMN.KEYWORDS).value
                publisher = self.o_sheet.cell(row=row, column=self.COLUMN.PUBLISHER).value

                keywords = re.findall(r'[^,; ]+', keywords)
                break
        else:
            raise RuntimeError(f'No metadata found for {h5p_file}')

        return Metadata(title, publisher, keywords, order, rating, collection)


class ParsingError(Exception):
    def __init__(self, msg: str):
        super(ParsingError, self).__init__(msg)
