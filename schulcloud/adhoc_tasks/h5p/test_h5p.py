import hashlib
import time
import unittest
import zipfile
import os

from schulcloud.adhoc_tasks.h5p.edusharing import EdusharingAPI, NotFoundException
from schulcloud.adhoc_tasks.h5p.h5p_upload import util
from schulcloud.adhoc_tasks.h5p.h5p_upload import S3Downloader
from schulcloud.adhoc_tasks.h5p.h5p_upload import Uploader
from schulcloud.adhoc_tasks.h5p.h5p_upload import generate_node_properties
from schulcloud.adhoc_tasks.h5p.h5p_extract_metadata import Metadata
from schulcloud.adhoc_tasks.h5p.h5p_extract_metadata import MetadataFile, ParsingError

EXPECTED_ENV_VARS = [
    'EDU_SHARING_BASE_URL',
    'EDU_SHARING_USERNAME',
    'EDU_SHARING_PASSWORD',
    'S3_ENDPOINT_URL',
    'S3_ACCESS_KEY',
    'S3_SECRET_KEY',
    'S3_BUCKET_NAME',
    'S3_BUCKET_NAME_TEST'
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
        env['S3_BUCKET_NAME_TEST']
    )
    downloaderFail = S3Downloader(
        env['S3_ENDPOINT_URL'],
        env['S3_ACCESS_KEY'],
        env['S3_SECRET_KEY'],
        'h5p-content-test-fail'
    )
    uploader = Uploader()
    metadata = Metadata

    test_folder_node_id = ""
    test_file_node_id = ""

    def test_edusharing001_make_request(self):
        url = f'/admin/v1/applications'
        response = self.api.make_request('GET', url)

        self.assertEqual(200, response.status_code, 'Can\'t connect to Edusharing')

    def test_edusharing002_create_user(self):
        # ToDo: Why get a '400' status code of this method back, although the user is created?
        name = 'TestUser'
        self.api.create_user(name, '123456', 'system')
        url_check = f'/iam/v1/people/-home-/{name}'
        result = self.api.make_request('GET', url_check)
        result = result.json()
        self.assertEqual('TestUser', result['person']['userName'], "TestUser NOT successfully created.")

        url_delete = f'/iam/v1/people/-home-/{name}?force=true'
        self.api.make_request('DELETE', url_delete)

    def test_edusharing003_find_node_by_name(self):
        parent_id = "-userhome-"
        child_name = "SYNC_OBJ"
        folder_exist = False

        node = self.api.find_node_by_name(parent_id, child_name)
        if node is not None:
            folder_exist = True
        self.assertTrue(folder_exist, "The Sync_Obj-Folder does not exist.")

    def test_edusharing004_get_or_create_folder(self):
        parent_id = "-userhome-"
        child_name = "SYNC_OBJ"
        folder_exist = False

        folder = self.api.get_or_create_folder(parent_id, child_name)
        if folder is not None:
            folder_exist = True
        self.assertTrue(folder_exist, "The Sync_Obj-Folder does not exist.")

    def test_edusharing005_get_sync_obj_folder(self):
        folder = self.api.get_sync_obj_folder()
        folder_exist = False
        if folder is not None:
            folder_exist = True
        self.assertTrue(folder_exist, "The Sync_Obj-Folder does not exist.")

    def test_edusharing006_get_children(self):
        folder = self.api.get_sync_obj_folder()
        nodes = self.api.get_children(folder.id)
        nodes_exist = False
        if nodes is not None:
            nodes_exist = True
        self.assertTrue(nodes_exist, "There are no children of this node.")

    def test_edusharing007_create_folder(self):
        parent_id = self.api.get_sync_obj_folder().id
        name = "test_folder"
        node = self.api.create_folder(parent_id, name)
        TestH5P.test_folder_node_id = node.id
        node_exist = False
        if node is not None:
            node_exist = True
        self.assertTrue(node_exist, "Can\'t create folder.")

    def test_edusharing008_set_permission(self):
        groups = ['Thuringia-public', 'Brandenburg-public', 'LowerSaxony-public']
        node = self.api.find_node_by_name(self.api.get_sync_obj_folder().id, 'test_folder')
        self.api.set_permissions(node.id, groups, True)

        url_permission = f'/node/v1/nodes/-home-/{node.id}/permissions'
        response = self.api.make_request('GET', url_permission)
        response = response.json()
        permission_set = []
        for i in range(3):
            response_raw = response['permissions']['localPermissions']['permissions'][i]['authority']['authorityName']
            response_clean = str(response_raw).replace("GROUP_", "")
            permission_set.append(response_clean)

        for permission in permission_set:
            self.assertTrue(permission in groups, 'Permission not found.')

    def test_edusharing009_get_metadata_of_node(self):
        node_id = self.api.get_sync_obj_folder().id
        response = self.api.get_metadata_of_node(node_id)
        self.assertEqual("SYNC_OBJ", response['node']['name'], "Can\'t get metadata of node.")

    def test_edusharing010_sync_node(self):
        name = "test_file"
        folder_name = "test_folder"
        properties = {
            "access": [
                "Read",
                "ReadAll",
                "Comment",
                "Feedback",
                "AddChildren",
                "ChangePermissions",
                "Write",
                "Delete",
                "CCPublish"
            ],
            "cm:name": [name],
            "cm:title": [name],
            "cm:edu_metadataset": ["mds_oeh"],
            "cm:edu_forcemetadataset": ["true"],
            "ccm:replicationsource": [folder_name],
            "ccm:replicationsourceid": [hashlib.sha1(name.encode()).hexdigest()],
            "ccm:lom_relation": [""],
        }
        response = self.api.sync_node(folder_name, properties, ['ccm:replicationsource', 'ccm:replicationsourceid'])
        sub_str = "file"
        res = response.name[:response.name.index(sub_str) + len(sub_str)]
        TestH5P.test_file_node_id = response.id
        self.assertEqual(name, res, "Can\'t create node.")

    def test_edusharing011_file_exists(self):
        parent_id = ""
        name = "test_file"
        # Don't stress Edusharing
        time.sleep(15)
        response = self.api.file_exists(parent_id, name=name)
        self.assertTrue(response, "Can\'t find file.")

    def test_edusharing012_search_custom(self):
        metadata_property = "name"
        name = "test_folder"
        # Don't stress Edusharing
        time.sleep(10)
        response = self.api.search_custom(metadata_property, name, 50, 'FOLDERS')
        self.assertEqual(name, response[0].name, "Can\'t find folder.")

    def test_edusharing013_set_preview_thumbnail(self):
        node_id = TestH5P.test_file_node_id
        self.api.set_preview_thumbnail(node_id=node_id,
                                       filename='.\\thumbnail\\H5Pthumbnail.png')

        url_check_prop = f'/node/v1/nodes/-home-/{node_id}/prepareUsage'
        response = self.api.make_request('POST', url_check_prop)
        response = response.json()
        response = response['node']['preview']['type']
        self.assertEqual("TYPE_USERDEFINED", response, 'The thumbnail were not set.')

    def test_edusharing014_delete_node(self):
        node_id = TestH5P.test_folder_node_id
        self.api.delete_node(node_id)
        not_found = False

        try:
            self.api.find_node_by_name(self.api.get_sync_obj_folder().id, 'test_folder')
        except NotFoundException:
            not_found = True
        self.assertTrue(not_found, 'Node is not deleted.')

    def test_extract_metadata001_metadata(self):
        path = '.\\h5p_test_files\\test_excel_file.xlsx'
        metadata = MetadataFile(file=path)
        self.assertEqual('test_collection', metadata.get_collection(), 'Wrong collection.')
        self.assertEqual('THR', metadata.get_collection_permission(), 'Wrong permission.')
        self.assertEqual(['test_keyword_01'], metadata.get_keywords(), 'Wrong keywords.')
        self.assertEqual('test_publisher', metadata.get_publisher(), 'Wrong publisher.')
        self.assertEqual('CC BY-NC-SA 4.0', metadata.get_license(), 'Wrong licence.')

    def test_extract_metadata002_metadata_from_file(self):
        path_excel = '.\\h5p_test_files\\test_excel_file.xlsx'
        metadata = MetadataFile(file=path_excel)
        element_test = 'test.h5p'
        metadata_file = metadata.get_metadata(element_test)

        self.assertEqual('test_collection', metadata_file.collection, 'Wrong collection.')
        self.assertEqual(['THR'], metadata_file.permission, 'Wrong permission.')
        self.assertEqual(['test_keyword_01'], metadata_file.keywords, 'Wrong keywords.')
        self.assertEqual('test_publisher', metadata_file.publisher, 'Wrong publisher.')
        self.assertEqual('CC BY-NC-SA 4.0', metadata_file.license, 'Wrong license.')
        self.assertEqual('01 test_title_01', metadata_file.title, 'Wrong title.')
        self.assertEqual(1, metadata_file.order, 'Wrong order.')

    def test_extract_metadata003_metadata_by_file_name(self):
        path_excel = '.\\h5p_test_files\\test_excel_file.xlsx'
        metadata = MetadataFile(file=path_excel)
        element_test = 'test.h5p'
        metadata_file = metadata.find_metadata_by_file_name(element_test)
        self.assertEqual(1, metadata_file, 'Multiple metadata matches.')

    def test_extract_metadata004_check_for_files(self):
        path_excel = '.\\h5p_test_files\\test_excel_file.xlsx'
        metadata = MetadataFile(file=path_excel)
        filenames = ['test.h5p', 'test02.h5p', 'test03.h5p', 'test_false.h5p']
        file_exist = True
        try:
            metadata.check_for_files(filenames=filenames)
        except ParsingError:
            file_exist = False
        self.assertFalse(file_exist, "Files aren\'t present in the Excel-Sheet")

    def test_extract_metadata005_fill_zeros(self):
        path_excel = '.\\h5p_test_files\\test_excel_file.xlsx'
        metadata = MetadataFile(file=path_excel)
        res = metadata.fill_zeros('4')
        self.assertEqual('04', res, 'Wrong upfilling zeros.')

# h5p_upload
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
                               'ccm:wwwurl': properties.get('ccm:wwwurl'),
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
