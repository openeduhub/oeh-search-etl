import logging
import os
from _datetime import datetime

import scrapy

from .base_classes import LomBase
from .scripts.lower_saxony_abi.directory_routine import DirectoryInitializer, UnZipper, \
    DirectoryScanner
from .scripts.lower_saxony_abi.keyword_mapper import LoSaxKeywordMapper
from ..constants import Constants
from ..items import BaseItemLoader, LomBaseItemloader, LomGeneralItemloader, LomTechnicalItemLoader, \
    LomLifecycleItemloader, LomEducationalItemLoader, LicenseItemLoader, ResponseItemLoader, \
    ValuespaceItemLoader


class NiedersachsenAbiSpider(scrapy.Spider, LomBase):
    name = 'niedersachsen_abi_spider'

    allowed_domains = ['za-aufgaben.nibis.de']
    start_urls = ['https://za-aufgaben.nibis.de']
    version = "0.0.3"  # last update: 2022-04-12
    # Default values for the 2 expected parameters. Parameter "filename" is always required, "skip_unzip" is optional.
    filename = None
    skip_unzip = False
    pdf_dictionary_general = dict()
    pdf_dictionary_additional = dict()

    # Running the crawler from the command line with the exact filename as a parameter:
    #   scrapy crawl niedersachsen_abi_spider -a filename="za-download-6e05cbbb6e07250c69ebe95ae972fe8a.zip"
    #   -a skip_unzip="yes"
    # Make sure that there is a corresponding .zip file inside the /zip_download/-folder in the project root

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s - %(message)s')
        # logging.disable(logging.DEBUG)
        directory_paths = DirectoryInitializer()
        zip_file_dictionary = directory_paths.check_download_folder_for_zip_files()

        # only extract files if a "filename"-parameter was given:
        if self.filename is not None:
            zip_selection = self.filename

            logging.debug(f"Selected .zip file by CLI-parameter: {zip_selection}")
            logging.debug(f"User wants to skip the unzipping? {self.skip_unzip}")
            # by default, the script should always unzip the desired .zip file,
            # but unzipping the nested .zip files is only done when requested by parameter
            if self.skip_unzip == "no":
                self.skip_unzip = False
            if self.skip_unzip == "yes":
                self.skip_unzip = True
            logging.debug(f"skip_unzip variable: {self.skip_unzip}")

            if self.skip_unzip is False:
                un_zipper = UnZipper()
                un_zipper.directory_paths = directory_paths.get_path_storage()
                un_zipper.zip_file_dictionary = zip_file_dictionary
                zip_file_chosen_by_user = \
                    un_zipper.compare_selected_zip_file_with_recognized_files(zip_selection=zip_selection)

                if zip_file_chosen_by_user is not None:
                    un_zipper.unzip_all_zips_within_the_initial_zip(zip_file=zip_file_chosen_by_user,
                                                                    skip_unzip=self.skip_unzip)

                    logging.debug(f"Extracted the following zip files:")
                    logging.debug(un_zipper.zip_files_already_extracted)

        # always scan the /zip_extract/-directory for pdfs and try to extract metadata
        logging.debug(
            f"Analyzing file paths for '.pdf'-files inside "
            f"{directory_paths.path_storage.path_to_extraction_directory}")
        pdfs_in_directory: dict = \
            DirectoryScanner.scan_directory_for_pdfs(directory_paths.path_storage.path_to_extraction_directory)
        # logging.debug(pp.pformat(pdfs_in_directory))
        logging.debug(f"Total .pdf items in the above mentioned directory: {len(pdfs_in_directory.keys())}")
        if len(pdfs_in_directory.keys()) == 0:
            raise Exception(f"No .pdf files found inside {directory_paths.path_storage.path_to_extraction_directory}. "
                            f"Please make sure that you've run the crawler with '-a filename=<zip filename>' "
                            f"parameter first and that there's actual .pdf files inside the extraction directory")
        kw_mapper = LoSaxKeywordMapper()
        pdf_dict1, pdf_dict2 = kw_mapper.extract_pdf_metadata(pdfs_in_directory)
        self.pdf_dictionary_general = pdf_dict1
        self.pdf_dictionary_additional = pdf_dict2

    def getId(self, response=None) -> str:
        pass

    def getHash(self, response=None) -> str:
        pass

    def parse(self, response, **kwargs):
        logging.debug(f"The .pdf (general) dictionary has {len(self.pdf_dictionary_general.keys())} files")
        logging.debug(f"The dictionary for additional .pdf files has "
                      f"{len(self.pdf_dictionary_additional.keys())} entries")

        # first we're scraping all the .pdf files that follow the more general RegEx syntax
        for pdf_item in self.pdf_dictionary_general:
            current_dict: dict = self.pdf_dictionary_general.get(pdf_item)
            base = BaseItemLoader()
            base.add_value('sourceId', pdf_item)
            hash_temp = str(f"{datetime.now().isoformat()}{self.version}")
            base.add_value('hash', hash_temp)
            base.add_value('binary', self.get_binary(current_dict, pdf_item))

            lom = LomBaseItemloader()

            general = LomGeneralItemloader()
            title_long: str = ' '.join(current_dict.get('keywords'))
            general.add_value('title', title_long)
            general.add_value('identifier', pdf_item)
            general.add_value('keyword', current_dict.get('keywords'))
            lom.add_value('general', general.load_item())

            technical = LomTechnicalItemLoader()
            technical.add_value('format', 'application/pdf')
            lom.add_value('technical', technical.load_item())

            lifecycle = LomLifecycleItemloader()
            lifecycle.add_value('role', 'publisher')
            lifecycle.add_value('organization', 'Niedersächsisches Kultusministerium')
            lom.add_value('lifecycle', lifecycle.load_item())

            educational = LomEducationalItemLoader()
            lom.add_value('educational', educational.load_item())

            base.add_value('lom', lom.load_item())

            vs = ValuespaceItemLoader()
            # all files are considered "Abituraufgaben"
            vs.add_value('new_lrt', "9cf3c183-f37c-4b6b-8beb-65f530595dff")
            # "Klausur, Klassenarbeit und Test"
            if current_dict.get('discipline') is not None:
                vs.add_value('discipline', current_dict.get('discipline'))
            if current_dict.get('intendedEndUserRole') is not None:
                vs.add_value('intendedEndUserRole', current_dict.get('intendedEndUserRole'))
                if current_dict.get("intendedEndUserRole") == "teacher":
                    # filenames that are ending with "L" or "Lehrer" are always
                    # "Erwartungshorizont/Bewertungsmuster"-type of pdfs, therefore we can derive the new_lrt from
                    # the filename
                    vs.add_value('new_lrt', "7c236821-bfae-4eeb-bc79-590bf8ea1d96")
                    # "Lösungs(beispiel) und Erwartungshorizont"
            base.add_value('valuespaces', vs.load_item())

            lic = LicenseItemLoader()
            base.add_value('license', lic.load_item())

            permissions = LomBase.getPermissions(self)
            base.add_value('permissions', permissions.load_item())

            response_loader = ResponseItemLoader()
            base.add_value('response', response_loader.load_item())

            yield base.load_item()

        # Making sure that we also grab the additional .pdf files that don't follow the general filename syntax
        for pdf_item in self.pdf_dictionary_additional:
            current_dict: dict = self.pdf_dictionary_additional.get(pdf_item)
            base = BaseItemLoader()
            base.add_value('sourceId', pdf_item)
            hash_temp = str(f"{datetime.now().isoformat()}{self.version}")
            base.add_value('hash', hash_temp)
            base.add_value('binary', self.get_binary(current_dict, pdf_item))

            lom = LomBaseItemloader()

            general = LomGeneralItemloader()
            general.add_value('title', pdf_item.split('.')[:-1])
            general.add_value('identifier', pdf_item)
            general.add_value('keyword', current_dict.get('keywords'))
            lom.add_value('general', general.load_item())

            technical = LomTechnicalItemLoader()
            technical.add_value('format', 'application/pdf')
            lom.add_value('technical', technical.load_item())

            lifecycle = LomLifecycleItemloader()
            lifecycle.add_value('role', 'publisher')
            lifecycle.add_value('organization', 'Niedersächsisches Kultusministerium')
            lom.add_value('lifecycle', lifecycle.load_item())

            educational = LomEducationalItemLoader()
            lom.add_value('educational', educational.load_item())

            base.add_value('lom', lom.load_item())

            vs = ValuespaceItemLoader()
            if current_dict.get('discipline') is not None:
                vs.add_value('discipline', current_dict.get('discipline'))
            # all files are considered "Abituraufgaben":
            vs.add_value('new_lrt', "9cf3c183-f37c-4b6b-8beb-65f530595dff")
            # "Klausur, Klassenarbeit und Test"
            if current_dict.get("intendedEndUserRole") == "teacher":
                # filenames that are ending with "L" or "Lehrer" are always "Erwartungshorizont/Bewertungsmuster"-type
                # of pdfs, therefore we can derive the new_lrt from the filename
                vs.add_value('new_lrt', "7c236821-bfae-4eeb-bc79-590bf8ea1d96")
                # "Lösungs(beispiel) und Erwartungshorizont"
            base.add_value('valuespaces', vs.load_item())

            lic = LicenseItemLoader()
            base.add_value('license', lic.load_item())

            permissions = LomBase.getPermissions(self)
            base.add_value('permissions', permissions.load_item())

            response_loader = ResponseItemLoader()
            base.add_value('response', response_loader.load_item())

            yield base.load_item()

    @staticmethod
    def get_binary(current_dict, pdf_item):
        filepath_full = current_dict.get('pdf_path') + os.path.sep + pdf_item
        file = open(filepath_full, mode='rb')
        binary = file.read()
        file.close()
        return binary
