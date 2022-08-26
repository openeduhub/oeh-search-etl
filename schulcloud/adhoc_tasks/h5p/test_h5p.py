import unittest
import zipfile
import os
import uuid

from schulcloud.adhoc_tasks.h5p.edusharing import EdusharingAPI, NotFoundException
from schulcloud.adhoc_tasks.h5p.h5p_upload import util
from schulcloud.adhoc_tasks.h5p.h5p_upload import S3Downloader
from schulcloud.adhoc_tasks.h5p.h5p_upload import Uploader
from schulcloud.adhoc_tasks.h5p.h5p_upload import generate_node_properties
from schulcloud.adhoc_tasks.h5p.h5p_extract_metadata import Metadata
from datetime import datetime

EXPECTED_ENV_VARS = [
    'EDU_SHARING_BASE_URL',
    'EDU_SHARING_USERNAME',
    'EDU_SHARING_PASSWORD',
    'S3_ENDPOINT_URL',
    'S3_ACCESS_KEY',
    'S3_SECRET_KEY',
    'S3_BUCKET_NAME'
]


class TestH5P(unittest.TestCase):
    env = util.Environment(EXPECTED_ENV_VARS, ask_for_missing=False)

    api = EdusharingAPI(
        env['EDU_SHARING_BASE_URL'],
        env['EDU_SHARING_USERNAME'],
        env['EDU_SHARING_PASSWORD'])
    downloader = S3Downloader(
        env['S3_ENDPOINT_URL'],
        env['S3_ACCESS_KEY'],
        env['S3_SECRET_KEY'],
        env['S3_BUCKET_NAME']
    )
    downloaderFail = S3Downloader(
        env['S3_ENDPOINT_URL'],
        env['S3_ACCESS_KEY'],
        env['S3_SECRET_KEY'],
        'h5p-conten-test-fail'
    )
    uploader = Uploader()
    metadata = Metadata

    def test_h5p_upload_setup_destination_folder(self):
        folder_name = "h5p_test_folder"
        sync_obj = self.api.get_sync_obj_folder()
        self.uploader.setup_destination_folder(folder_name)
        try:
            node = self.api.find_node_by_name(sync_obj.id, folder_name)
        except NotFoundException as exc:
            self.fail("Failed to setup destination folder! " + str(exc))
        self.api.delete_node(node.id)

    def test_h5p_upload_get_metadata_and_excel_file(self):
        path = os.path.join("h5p_test_files", "test_upload_collection.zip")
        zip = zipfile.ZipFile(path)
        try:
            files = self.uploader.get_metadata_and_excel_file(zip)
        except RuntimeError:
            self.fail("Failed to get metadata file and excel file!")
        self.assertTrue(files is not None, "Failed to get metadata file and excel file!")

    def test_h5p_upload_no_excel_get_metadata_and_excel_file(self):
        path = os.path.join("h5p_test_files", "test_get_metadata.zip")
        zip = zipfile.ZipFile(path)
        try:
            files = self.uploader.get_metadata_and_excel_file(zip)
        except RuntimeError:
            pass
        else:
            self.fail("Failed: Created excel file without an excel file in the zip!")

    def test_h5p_upload_get_permitted_groups(self):
        permitted_groups = self.uploader.get_permitted_groups(["THR", "BRB"])
        self.assertEqual(permitted_groups, ["Thuringia-public", "Brandenburg-public"], "Returned wrong groups!")

    def test_h5p_upload_get_permitted_groups_all(self):
        permitted_groups = self.uploader.get_permitted_groups(["ALLE"])
        self.assertEqual(['Thuringia-public', 'Brandenburg-public', 'LowerSaxony-public'], permitted_groups,
                         "Returned wrong groups!")

    def test_h5p_upload_upload_h5p_non_collection(self):
        path = os.path.join("h5p_test_files", "test_upload_non_collection.zip")
        zip = zipfile.ZipFile(path)

        files = self.uploader.get_metadata_and_excel_file(zip)
        metadata_file = files[0]
        excel_file = files[1]

        folder_name = "h5p_test_folder"
        sync_obj = self.api.get_sync_obj_folder()
        self.api.get_or_create_folder(sync_obj.id, folder_name)
        folder_node = self.api.find_node_by_name(sync_obj.id, folder_name)
        self.uploader.setup_destination_folder(folder_name)

        self.uploader.upload_h5p_non_collection(folder_name, metadata_file, excel_file, zip)
        try:
            nodes_list = self.api.get_children(folder_node.id)
            self.assertEqual(3, len(nodes_list), "Failed: test upload of a non collection zip!")
        except NotFoundException:
            self.fail("Failed: test upload of a non collection zip!")
        self.api.delete_node(folder_node.id)

    def test_h5p_upload_upload_h5p_collection(self):
        path = os.path.join("h5p_test_files", "test_upload_collection.zip")
        zip = zipfile.ZipFile(path)

        files = self.uploader.get_metadata_and_excel_file(zip)
        metadata_file = files[0]
        excel_file = files[1]

        folder_name = "h5p_test_folder"
        sync_obj = self.api.get_sync_obj_folder()
        self.api.get_or_create_folder(sync_obj.id, folder_name)
        folder_node = self.api.find_node_by_name(sync_obj.id, folder_name)
        self.uploader.setup_destination_folder(folder_name)

        self.uploader.upload_h5p_collection(folder_name, metadata_file, excel_file, zip)
        try:
            nodes_list = self.api.get_children(folder_node.id)
            self.assertEqual(4, len(nodes_list), "Failed: test upload of a collection zip!")
        except NotFoundException:
            self.fail("Failed: test upload of a collection zip!")
        self.api.delete_node(folder_node.id)

    def test_h5p_upload_upload_h5p_file_collection(self):
        path = os.path.join("h5p_test_files", "test_upload_collection.zip")
        zip = zipfile.ZipFile(path)
        metadata = Metadata("Test Nummer 1", "Tester", ["h5p", "test"], "1", ['ALLE'])

        folder_name = "h5p_test_folder"
        sync_obj = self.api.get_sync_obj_folder()
        self.api.get_or_create_folder(sync_obj.id, folder_name)
        folder_node = self.api.find_node_by_name(sync_obj.id, folder_name)
        self.uploader.setup_destination_folder(folder_name)

        file = zip.open("test1.h5p")
        properties = generate_node_properties(
            "test", "test", "Tester", "Test-Lizenz", ["H5P", "Test"],
            folder_name, format="text/html", aggregation_level=2, aggregation_level_hpi=2
        )
        collection_rep_source_uuid = properties['ccm:replicationsourceuuid']
        relation = f"{{'kind': 'ispartof', 'resource': {{'identifier': {collection_rep_source_uuid}}}}}"

        result = self.uploader.upload_h5p_file(folder_name, "test1.h5p", metadata, file=file, relation=relation)

        node_id, rep_source_uuid = result
        nodes_list = self.api.get_children(folder_node.id)
        self.assertTrue(nodes_list[0].id == node_id)
        self.api.delete_node(folder_node.id)

    def test_h5p_upload_upload_h5p_file_non_collection(self):
        path = os.path.join("h5p_test_files", "test_upload_non_collection.zip")
        zip = zipfile.ZipFile(path)
        metadata = Metadata("Test Nummer 1", "Tester", ["h5p", "test"], "1", ['ALLE'])
        file = zip.open("test1.h5p")

        folder_name = "h5p_test_folder"
        sync_obj = self.api.get_sync_obj_folder()
        self.api.get_or_create_folder(sync_obj.id, folder_name)
        folder_node = self.api.find_node_by_name(sync_obj.id, folder_name)
        self.uploader.setup_destination_folder(folder_name)

        result = self.uploader.upload_h5p_file(folder_name, "test1.h5p", metadata, file=file)

        node_id, rep_source_uuid = result
        nodes_list = self.api.get_children(folder_node.id)
        self.assertTrue(nodes_list[0].id == node_id)
        self.api.delete_node(folder_node.id)

    def test_h5p_upload_generate_node_properties(self):
        properties = generate_node_properties("Test Nummer 1", "Test Nummer 1", "Tester", "Test-Lizenz",
                                              ["H5P", "Test"], "h5p_test_folder")
        expected_properties = {'access': ['Read', 'ReadAll', 'Comment', 'Feedback', 'AddChildren', 'ChangePermissions',
                                          'Write', 'Delete', 'CCPublish'], 'cm:name': ['Test Nummer 1'],
                               'cm:edu_metadataset': ['mds_oeh'], 'cm:edu_forcemetadataset': ['true'],
                               'ccm:ph_invited': ['GROUP_public'], 'ccm:ph_action': ['PERMISSION_ADD'],
                               'ccm:objecttype': ['MATERIAL'], 'ccm:replicationsource': ['h5p_test_folder'],
                               'ccm:replicationsourceid': ['d8e21eb13c9b5b7f4c80e928457558efb4687a8b'],
                               'ccm:replicationsourcehash': properties.get('ccm:replicationsourcehash'),
                               'ccm:replicationsourceuuid': properties.get('ccm:replicationsourceuuid'),
                               'ccm:commonlicense_key': ['Test-Lizenz'], 'ccm:hpi_searchable': ['1'],
                               'ccm:hpi_lom_general_aggregationlevel': ['1'], 'cclom:title': ['Test Nummer 1'],
                               'cclom:aggregationlevel': ['1'], 'cclom:general_language': ['de'],
                               'cclom:general_keyword': ['H5P', 'Test'],
                               'ccm:lom_annotation': ["{'description': 'searchable==1', 'entity': 'crawler'}"],
                               'ccm:wwwurl': [''],
                               'ccm:hpi_lom_relation': ["{'kind': 'ispartof', 'resource': {'identifier': []}}"],
                               'ccm:lom_relation': ["{'kind': 'ispartof', 'resource': {'identifier': []}}"],
                               'ccm:create_version': ['false'], 'ccm:lifecyclecontributer_publisherFN': ['Tester']}
        self.assertEqual(expected_properties, properties, "Failed to generate node properties!")

    # S3 Download
    def test_h5p_upload_check_bucket_exists(self):
        try:
            self.downloader.check_bucket_exists()
        except RuntimeError:
            self.fail("Failed to find an existing s3 bucket")

    def test_h5p_upload_check_bucket_exists_fail(self):
        test = False
        try:
            self.downloaderFail.check_bucket_exists()
        except RuntimeError:
            test = True
        self.assertTrue(test, "Failed: Found not existing s3 bucket.")

    def test_h5p_upload_get_object_list(self):
        obj_list = self.downloader.get_object_list()
        key_list = []
        for obj in obj_list:
            key_list.append(obj['Key'])
        self.assertEqual(["test_upload_collection.zip", "test_upload_non_collection.zip"], key_list,
                         "Failed to get object list!")

    def test_h5p_upload_download_object(self):
        self.downloader.download_object("test_upload_collection.zip", "h5p_temp")
        obj_list = os.listdir("h5p_temp")
        self.assertEqual(["test_upload_collection.zip"], obj_list, "Failed to download object!")
        path = os.path.join("h5p_temp", "test_upload_collection.zip")
        os.remove(path)


if __name__ == '__main__':
    unittest.main()
