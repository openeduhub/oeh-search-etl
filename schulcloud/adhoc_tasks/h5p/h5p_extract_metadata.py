import sys
from typing import List, Union, IO, Optional
import re
import openpyxl
from openpyxl.utils import get_column_letter


class Metadata:
    def __init__(self, title: str, publisher: str, keywords: List[str], order: str, rating: str, permission: List[str],
                 collection: Optional[str] = None, licence: Optional[str] = None):
        self.title = title
        self.publisher = publisher
        self.keywords = keywords
        self.order = order
        self.rating = rating
        self.collection = collection
        self.license = licence
        self.permission = permission


class MetadataFile:
    class COLUMN:
        COLLECTION = 1
        ORDER = 2
        RATING = 3
        TITLE = 4
        FILENAME = 5
        KEYWORDS = 6
        PUBLISHER = 7
        LICENSE = 8
        PERMISSION = 9
        COUNT = 9

    def __init__(self, file: Union[str, IO]):
        self.workbook = openpyxl.load_workbook(filename=file, data_only=True)
        self.o_sheet = self.workbook["Tabelle1"]
        self.validate_sheet(file=file)

    def validate_sheet(self, file: Union[str, IO]):
        # Check required fields
        required_fields = [self.COLUMN.TITLE, self.COLUMN.FILENAME]
        for row in range(1, self.o_sheet.max_row + 1):
            for column in range(1, self.COLUMN.COUNT + 1):
                if column in required_fields:
                    if not self.o_sheet.cell(row=row, column=column).value:
                        raise ParsingError(f'Empty required cell: {get_column_letter(column)}{row} at {file.name}')

        # Check for collection
        if self.o_sheet.cell(row=1, column=self.COLUMN.COLLECTION).value:
            collection = self.o_sheet.cell(row=1, column=self.COLUMN.COLLECTION).value
            for row in range(1, self.o_sheet.max_row + 1):
                other_collection = self.o_sheet.cell(row=row, column=self.COLUMN.COLLECTION).value
                if not other_collection == collection:
                    raise ParsingError(f'Multiple collection or spelling mistake in row {row} at {file.name}.')

        # Check permission
        permissions_raw = self.o_sheet.cell(row=1, column=self.COLUMN.PERMISSION).value
        permissions = re.findall(r'\w+', permissions_raw)
        for i in permissions:
            if i != "NDS" and i != "BRB" and i != "THR" and i != "ALLE" and i != "":
                raise ParsingError(f'Spelling mistake or unknown permission: {i} at {file.name}')

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

    def get_keywords(self):
        keywords_raw = self.o_sheet.cell(row=1, column=self.COLUMN.KEYWORDS).value
        keywords = re.findall(r'\w+', keywords_raw)
        return keywords

    def find_metadata_by_file_name(self, h5p_file: str):
        result = []
        # looking for exact match
        for row in range(1, self.o_sheet.max_row + 1):
            if self.o_sheet.cell(row=row, column=self.COLUMN.FILENAME).value == h5p_file:
                result.append(row)
        if not result:
            # looking for rough match (like relative paths etc.)
            for row in range(1, self.o_sheet.max_row + 1):
                if h5p_file in self.o_sheet.cell(row=row, column=self.COLUMN.FILENAME).value:
                    result.append(row)
            if not result:
                raise RuntimeError(f'No metadata found for {h5p_file}')

        if len(result) == 1:
            return result[0]
        elif len(result) > 1:
            raise RuntimeError(f'Multiple metadata matches for {h5p_file}')

    def get_metadata(self, h5p_file: str):
        row = self.find_metadata_by_file_name(h5p_file)

        collection = self.o_sheet.cell(row=row, column=self.COLUMN.COLLECTION).value
        order = self.o_sheet.cell(row=row, column=self.COLUMN.ORDER).value
        rating = self.o_sheet.cell(row=row, column=self.COLUMN.RATING).value
        prefix = self.fill_zeros(str(rating)) + ' ' if rating else ""
        title = prefix + str(self.o_sheet.cell(row=row, column=self.COLUMN.TITLE).value)
        keywords_raw = self.o_sheet.cell(row=row, column=self.COLUMN.KEYWORDS).value
        keywords = re.findall(r'\w+', keywords_raw)
        publisher = self.o_sheet.cell(row=row, column=self.COLUMN.PUBLISHER).value
        licence = self.o_sheet.cell(row=row, column=self.COLUMN.LICENSE).value
        permission = self.o_sheet.cell(row=row, column=self.COLUMN.PERMISSION).value

        return Metadata(title, publisher, keywords, order, rating, collection, licence, permission)

    def fill_zeros(self, rating: str):
        max_length = len(str(self.o_sheet.max_row))
        zero = (max_length - len(rating)) * '0'
        return zero + rating


class ParsingError(Exception):
    def __init__(self, msg: str):
        super(ParsingError, self).__init__(msg)
