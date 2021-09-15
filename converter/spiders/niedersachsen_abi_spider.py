import os
from _datetime import datetime
import logging
import pprint

import scrapy

from .scripts.lower_saxony_abi.directory_routine import DirectoryInitializer, UnZipper, \
    DirectoryScanner
from .scripts.lower_saxony_abi.keyword_mapper import LoSaxKeywordMapper
from ..items import BaseItemLoader, LomBaseItemloader, LomGeneralItemloader, LomTechnicalItemLoader, \
    LomLifecycleItemloader, LomEducationalItemLoader, LicenseItemLoader, PermissionItemLoader, ResponseItemLoader, \
    ValuespaceItemLoader


class NiedersachsenAbiSpider(scrapy.Spider):
    name = 'niedersachsen_abi_spider'

    allowed_domains = ['https://za-aufgaben.nibis.de']
    start_urls = ['https://za-aufgaben.nibis.de']
    version = "0.0.1"
    # Default values for the 2 expected parameters. filename is always required, skip_unzip optional.
    filename = None
    skip_unzip = False
    pdf_dictionary_general = dict()
    pdf_dictionary_additional = dict()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s - %(message)s')
        # logging.disable(logging.DEBUG)
        if self.filename is not None:
            zip_selection = self.filename

            logging.debug(f"Selected .zip file by CLI-parameter: {zip_selection}")
            logging.debug(f"User wants to skip the unzipping? {self.skip_unzip}")
            # by default, the script should always unzip the desired .zip file
            if self.skip_unzip == "no":
                self.skip_unzip = False
            if self.skip_unzip == "yes":
                self.skip_unzip = True
            logging.debug(f"skip_unzip variable: {self.skip_unzip}")

            directory_paths = DirectoryInitializer()
            zip_file_dictionary = directory_paths.check_download_folder_for_zip_files()

            if self.skip_unzip is False:
                un_zipper = UnZipper()
                un_zipper.directory_paths = directory_paths.get_path_storage()
                un_zipper.zip_file_dictionary = zip_file_dictionary
                zip_file_chosen_by_user = un_zipper.show_zip_list(zip_selection=zip_selection)

                if zip_file_chosen_by_user is not None:
                    un_zipper.unzip_all_zips_within_the_initial_zip(zip_file=zip_file_chosen_by_user,
                                                                    skip_unzip=self.skip_unzip)

                    logging.debug(f"Extracted the following zip files:")
                    logging.debug(un_zipper.zip_files_already_extracted)

            print(
                f"Analyzing file paths for '.pdf'-files inside "
                f"{directory_paths.path_storage.path_to_extraction_directory}")
            pdfs_in_directory: dict = \
                DirectoryScanner.scan_directory_for_pdfs(directory_paths.path_storage.path_to_extraction_directory)
            # logging.debug(pp.pformat(pdfs_in_directory))
            print(f"Total .pdf items in the above mentioned directory: {len(pdfs_in_directory.keys())}")

            kw_mapper = LoSaxKeywordMapper()
            pdf_dict1, pdf_dict2 = kw_mapper.extract_pdf_metadata(pdfs_in_directory)
            self.pdf_dictionary_general = pdf_dict1
            self.pdf_dictionary_additional = pdf_dict2

    def parse(self, response, **kwargs):
        print(f"Hello world!")
        print(f"filename = {self.filename}")
        print(f"skip_unzip = {self.skip_unzip}")
        print(f"The .pdf (general) dictionary has {len(self.pdf_dictionary_general.keys())} files")
        print(f"The dictionary for additional .pdf files has {len(self.pdf_dictionary_additional.keys())} entries")

        # first we're scraping all the .pdf files that follow the more general RegEx syntax
        for pdf_item in self.pdf_dictionary_general:
            current_dict: dict = self.pdf_dictionary_general.get(pdf_item)
            pprint.pprint(current_dict)
            base = BaseItemLoader()
            base.add_value('sourceId', pdf_item)
            hash_temp = str(f"{datetime.now().isoformat()}{self.version}")
            base.add_value('hash', hash_temp)

            lom = LomBaseItemloader()

            general = LomGeneralItemloader()
            general.add_value('title', pdf_item)
            general.add_value('identifier', pdf_item)
            general.add_value('keyword', current_dict.get('keywords'))
            lom.add_value('general', general.load_item())

            technical = LomTechnicalItemLoader()
            filepath_full = current_dict.get('pdf_path') + os.path.sep + pdf_item
            technical.add_value('location', filepath_full)
            lom.add_value('technical', technical.load_item())

            lifecycle = LomLifecycleItemloader()
            lom.add_value('lifecycle', lifecycle.load_item())

            educational = LomEducationalItemLoader()
            lom.add_value('educational', educational.load_item())

            base.add_value('lom', lom.load_item())

            vs = ValuespaceItemLoader()
            if current_dict.get('discipline') is not None:
                vs.add_value('discipline', current_dict.get('discipline'))
            if current_dict.get('intendedEndUserRole') is not None:
                vs.add_value('intendedEndUserRole', current_dict.get('intendedEndUserRole'))
            base.add_value('valuespaces', vs.load_item())

            lic = LicenseItemLoader()
            base.add_value('license', lic.load_item())

            permissions = PermissionItemLoader()
            base.add_value('permissions', permissions.load_item())

            response_loader = ResponseItemLoader()
            base.add_value('response', response_loader.load_item())

            yield base.load_item()

        # Making sure that we also grab the additional .pdf files that don't follow the general filename syntax
        for pdf_item in self.pdf_dictionary_additional:
            current_dict: dict = self.pdf_dictionary_additional.get(pdf_item)
            pprint.pprint(current_dict)
            base = BaseItemLoader()
            base.add_value('sourceId', pdf_item)
            hash_temp = str(f"{datetime.now().isoformat()}{self.version}")
            base.add_value('hash', hash_temp)

            lom = LomBaseItemloader()

            general = LomGeneralItemloader()
            general.add_value('title', pdf_item)
            general.add_value('identifier', pdf_item)
            general.add_value('keyword', current_dict.get('keywords'))
            lom.add_value('general', general.load_item())

            technical = LomTechnicalItemLoader()
            filepath_full = current_dict.get('pdf_path') + os.path.sep + pdf_item
            technical.add_value('location', filepath_full)
            lom.add_value('technical', technical.load_item())

            lifecycle = LomLifecycleItemloader()
            lom.add_value('lifecycle', lifecycle.load_item())

            educational = LomEducationalItemLoader()
            lom.add_value('educational', educational.load_item())

            base.add_value('lom', lom.load_item())

            vs = ValuespaceItemLoader()
            if current_dict.get('discipline') is not None:
                vs.add_value('discipline', current_dict.get('discipline'))
            base.add_value('valuespaces', vs.load_item())

            lic = LicenseItemLoader()
            base.add_value('license', lic.load_item())

            permissions = PermissionItemLoader()
            base.add_value('permissions', permissions.load_item())

            response_loader = ResponseItemLoader()
            base.add_value('response', response_loader.load_item())

            yield base.load_item()