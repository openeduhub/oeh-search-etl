import sys
from typing import List, Union, IO, Optional

import openpyxl
from openpyxl.utils import get_column_letter


class Metadata:
    def __init__(self, title: str, publisher: str, keywords: List[str], order: str, rating: str, collection: Optional[str] = None):
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
        title = self.get_title_with_rating(self.o_sheet.cell(row=row, column=self.COLUMN.TITLE).value, rating)
        keywords = self.o_sheet.cell(row=row, column=self.COLUMN.KEYWORDS).value
        publisher = self.o_sheet.cell(row=row, column=self.COLUMN.PUBLISHER).value

        # keywords = re.findall(r'[^,; ]+', keywords)

        return Metadata(title, publisher, keywords, order, rating, collection)

    def get_title_with_rating(self, title_table, rating):
        rating_title = str(rating) + " "

        if 9 < self.o_sheet.max_row + 1 < 100:
            if rating < 10:
                rating_title = '0' + rating_title
        elif 99 < self.o_sheet.max_row + 1 < 1000:
            if rating < 10:
                rating_title = '00' + rating_title
            elif 9 < rating < 100:
                rating_title = '0' + rating_title
        elif 999 < self.o_sheet.max_row + 1 < 10000:
            if rating < 10:
                rating_title = '000' + rating_title
            elif 9 < rating < 100:
                rating_title = '00' + rating_title
            elif 99 < rating < 1000:
                rating_title = '0' + rating_title

        return rating_title + title_table


class ParsingError(Exception):
    def __init__(self, msg: str):
        super(ParsingError, self).__init__(msg)
