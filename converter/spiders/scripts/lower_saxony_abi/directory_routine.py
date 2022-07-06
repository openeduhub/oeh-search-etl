import glob
import logging
import os
import pathlib
import pprint
import zipfile
from dataclasses import dataclass


@dataclass
class PathStorage:
    parent_directory: str = None
    path_to_download_directory: str = None
    path_to_extraction_directory: str = None

    pp = pprint.PrettyPrinter(indent=4)

    def print_all_directories(self):
        self.pp.pprint("Working-directories that this script will be using:")
        self.pp.pprint(self.parent_directory)
        self.pp.pprint(self.path_to_download_directory)
        self.pp.pprint(self.path_to_extraction_directory)

    pass


class DirectoryInitializer:
    """
    This class makes sure that the 3 directories that will be frequently used actually exist - and if they don't will
    create those directories and save them to our 'PathStorage'-dataclass.
    After the DirectoryInitializer class is done with its work, the folder structure should look like this:
    /<parent_dir_of_this_project>/
    /<parent_dir_of_this_project>/zip_download              <- this is where the 'to be extracted' .zips should be
    /<parent_dir_of_this_project>/zip_download/zip_extract/ <- this is where the extracted files end up
    """
    path_storage = PathStorage()

    def __init__(self):
        self.initialize_required_directories()

    def check_download_folder_for_zip_files(self) -> dict:
        """
        Checks the /zip_download/-folder for .zip files and returns a list with their filenames and size in megabyte.
        """
        file_dict = dict()
        os.chdir(self.path_storage.path_to_download_directory)
        logging.debug("Checking " + os.getcwd() + " for zip files")
        if os.getcwd().endswith('zip_download'):
            temp_list = os.listdir(os.getcwd())
            # since the temp_list will hold folder names as well, we're checking for files only:
            file_list = list()
            for file_entry in temp_list:
                if os.path.isfile(file_entry):
                    if file_entry.endswith('.zip'):
                        file_list.append(file_entry)
            for file in file_list:
                file_size_temp = os.path.getsize(file)
                file_size_megabyte = file_size_temp / (1000 * 1000)
                file_size_megabyte = str(file_size_megabyte) + "MB"
                # file size in Mebibyte:
                # file_size_mebibyte = file_size_temp / (1024 * 1024)
                file_dict_entry = {
                    file: file_size_megabyte
                }
                file_dict.update(file_dict_entry)
            logging.debug(".zip files detected inside the '/zip_download/'-directory: ")
            logging.debug(file_dict)
        return file_dict

    def create_zip_download_directory(self):
        os.chdir(self.path_storage.parent_directory)
        logging.debug("Creating '/zip_download/-directory ...")
        os.mkdir('zip_download')
        if os.path.exists('zip_download'):
            print("Please provide a suitable .zip-file inside the '/zip_download/'-directory and rerun the script")
            self.path_storage.path_to_download_directory = os.path.join(os.getcwd(), 'zip_download')

    def create_zip_extraction_directory(self):
        os.chdir(self.path_storage.path_to_download_directory)
        logging.debug("Creating '/zip_extract/'-directory ...")
        os.mkdir('zip_extract')
        os.chdir('zip_extract')
        self.path_storage.path_to_extraction_directory = os.getcwd()
        os.chdir('..')

    def detect_extraction_directory(self):
        """
        Checks if there is a /zip_extract/-subdirectory inside the /zip_download/ folder and saves the folder path to
        the class attributes. If there isn't a subdirectory, it'll create one by calling the corresponding method.
        """
        logging.debug("Detecting 'zip_extract'-sub-folder ...")
        os.chdir(self.path_storage.path_to_download_directory)
        if os.path.exists('zip_extract'):
            logging.debug("SUCCESS! Detected '/zip_extract/'-directory, continuing ...")
            os.chdir('zip_extract')
            self.path_storage.path_to_extraction_directory = os.getcwd()
            os.chdir('..')
        else:
            self.create_zip_extraction_directory()

    def detect_zip_directory(self) -> bool:
        if os.path.exists('zip_download'):
            os.chdir('zip_download')
            zip_directory = os.path.join(os.getcwd())
            logging.debug("SUCCESS! Detected 'zip_download'-directory in: " + zip_directory)
            self.path_storage.path_to_download_directory = zip_directory
            return True
        else:
            self.create_zip_download_directory()
            return False

    def get_path_storage(self):
        return self.path_storage

    def initialize_folders(self):
        logging.debug("Looking for 'zip_download/'-directory ...")
        if self.detect_zip_directory():
            self.detect_extraction_directory()

    def initialize_required_directories(self):
        self.path_storage.parent_directory = os.getcwd()
        self.initialize_folders()
        self.path_storage.print_all_directories()
        os.chdir(self.path_storage.parent_directory)
        return self


class UnZipper:
    directory_paths: PathStorage = None
    zip_file_dictionary: dict = None
    zip_files_already_extracted = set()
    zip_files_to_extract = set()
    zip_files_to_extract_dict = dict()

    pp = pprint.PrettyPrinter(indent=4)

    def compare_selected_zip_file_with_recognized_files(self, zip_selection=None):
        # TODO: maybe prettify the zip list output
        self.pp.pprint(f"The following .zip files were recognized by the script: {self.zip_file_dictionary}")
        if zip_selection is not None:
            if zip_selection in self.zip_file_dictionary.keys():
                zip_file_name = zip_selection
                zip_file_size_megabytes = self.zip_file_dictionary.get(zip_selection)
                print(f"Selected the following file:\t {zip_file_name} \t size: {zip_file_size_megabytes}")
                zip_file = zipfile.ZipFile(zip_file_name)
                return zip_file
            else:
                logging.warning(f"Selected .zip file '{zip_selection}' not found in "
                                f"'{self.directory_paths.path_to_download_directory}'!\n"
                                f"These are the available .zip files: {self.zip_file_dictionary}.\n"
                                f"Please make sure that your CLI-parameter input for --filename='file.zip' is valid.")

    def unzip_all_zips_within_the_initial_zip(self, zip_file: zipfile, skip_unzip=False):
        """
        Unzips the initially selected .zip file and checks if the user wants to also extract all .zip files in its
        subdirectories.
        Keeps track of which files were already extracted by using a set() of their filenames.
        :param zip_file: the user-specified zip file that needs extraction
        :param skip_unzip: in case the user wants to only unzip the initial .zip file and nothing else
        :return: a list() of all .zip files that were found within the initial .zip file
        """
        zips_inside_zip: list = list()
        zip_files_list: list = zip_file.namelist()
        zip_file.extractall(path='zip_extract')
        filename_full_path = os.path.abspath(zip_file.filename)
        self.zip_files_already_extracted.add(filename_full_path)

        for zip_item in zip_files_list:
            if zip_item.endswith('.zip'):
                zips_inside_zip.append(zip_item)

        if len(zips_inside_zip) > 0:
            logging.debug(f"Found additional .zip files inside {zip_file.filename}:")
            logging.debug(zips_inside_zip)
            if skip_unzip is False:
                self.unzip_everything(self.directory_paths.path_to_extraction_directory)
            elif skip_unzip is True:
                print(f"Okay. Skipping extraction of nested .zip files within {zip_file.filename}")
        elif len(zips_inside_zip) == 0:
            return zips_inside_zip

    def unzip_everything(self, directory_as_string):
        """
        Tries to recursively unzip all .zip files within a directory.
        :param directory_as_string: the filepath in which to look for .zip files
        """
        extract_dir = directory_as_string
        os.chdir(extract_dir)
        zip_inside_zip_counter = 0
        for folder_name, sub_folder, filenames in os.walk(extract_dir):
            if len(sub_folder) == 0 and folder_name.endswith('zip_extract'):
                for filename_top_level in filenames:
                    current_full_path = os.path.abspath(filename_top_level)
                    if filename_top_level.endswith(
                            '.zip') and current_full_path not in self.zip_files_already_extracted:
                        print(folder_name)
                        print(filename_top_level)
                        self.zip_files_already_extracted.add(current_full_path)
                        current_zip = zipfile.ZipFile(filename_top_level)
                        zip_files_inside = current_zip.namelist()
                        for zip_file_inside in zip_files_inside:
                            if zip_file_inside.endswith('.zip'):
                                zip_inside_zip_counter += 1
                        current_zip.extractall()
                if zip_inside_zip_counter > 0:
                    if extract_dir is not None:
                        self.unzip_everything(extract_dir)
                    else:
                        extract_dir = self.directory_paths.path_to_extraction_directory
                        self.unzip_everything(extract_dir)
            for _ in sub_folder:
                for filename in filenames:
                    current_full_path = os.path.abspath(filename)
                    if filename.endswith('.zip') and current_full_path not in self.zip_files_already_extracted:
                        self.zip_files_to_extract.add(filename)
                        self.zip_files_to_extract_dict.update({filename: folder_name})

        for item in self.zip_files_to_extract_dict.keys():
            if item not in self.zip_files_already_extracted:
                print(f"Unzipping: {item}")
                temp_filepath_full = self.zip_files_to_extract_dict.get(item) + os.path.sep + item
                temp_path = self.zip_files_to_extract_dict.get(item)
                temp_zip: zipfile = zipfile.ZipFile(temp_filepath_full)
                temp_zip.extractall(path=temp_path)
                self.zip_files_already_extracted.add(item)
        pass


class DirectoryScanner:

    @staticmethod
    def scan_directory_for_pdfs(target_directory):
        """
        Returns a dict() of .pdf files and their filepath.
        :param target_directory: the directory in which to look for .pdf files
        :return: a dictionary consisting of two strings: a unique filename and the corresponding directory, e.g.:
        dict() = { filename : directory }
        """
        directory_to_scan = target_directory
        pdf_dictionary_temp = dict()
        pdf_iterator = glob.iglob(f"{directory_to_scan}/**/*.pdf", recursive=True)
        for pdf_item in pdf_iterator:
            pdf_pure_path = pathlib.PurePath(pdf_item)
            pdf_name = pdf_pure_path.name
            pdf_directory = str(pdf_pure_path.parent)
            pdf_dictionary_temp.update({pdf_name: pdf_directory})
        return pdf_dictionary_temp
