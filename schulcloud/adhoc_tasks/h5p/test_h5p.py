import hashlib
import time
import unittest
from schulcloud.adhoc_tasks.h5p.edusharing import EdusharingAPI, NotFoundException
from schulcloud.adhoc_tasks.h5p.h5p_upload import util
from schulcloud.adhoc_tasks.h5p.h5p_upload import S3Downloader
from schulcloud.adhoc_tasks.h5p.h5p_extract_metadata import MetadataFile, ParsingError

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

    def test_edusharing013_set_property_relation(self):
        node_id = TestH5P.test_file_node_id
        metadata_property = 'ccm:lom_relation'
        value = ['value01', 'value02', 'value03']
        self.api.set_property_relation(node_id, metadata_property, value)
        url_check_prop = f'/node/v1/nodes/-home-/{node_id}/prepareUsage'
        response = self.api.make_request('POST', url_check_prop)
        response = response.json()
        response = response['node']['properties']['ccm:lom_relation'][0]
        compare_array = []
        compare_array.append(response[49:56]), compare_array.append(response[60:67])
        compare_array.append(response[71:78])
        self.assertListEqual(value, compare_array, 'Relations were not set right.')

    def test_edusharing014_set_preview_thumbnail(self):
        node_id = TestH5P.test_file_node_id
        self.api.set_preview_thumbnail(node_id=node_id,
                                       filename='..\\thumbnail\\H5P-Inhalt_MitIcons_TafelInTSPblau.png')

        url_check_prop = f'/node/v1/nodes/-home-/{node_id}/prepareUsage'
        response = self.api.make_request('POST', url_check_prop)
        response = response.json()
        response = response['node']['preview']['type']
        self.assertEqual("TYPE_USERDEFINED", response, 'The thumbnail were not set.')

    def test_edusharing015_delete_node(self):
        node_id = TestH5P.test_folder_node_id
        self.api.delete_node(node_id)
        not_found = False

        try:
            self.api.find_node_by_name(self.api.get_sync_obj_folder().id, 'test_folder')
        except NotFoundException:
            not_found = True
        self.assertTrue(not_found, 'Node is not deleted.')

    def test_extract_metadata001_metadata(self):
        path = '..\\h5p_test_files\\test_excel_file.xlsx'
        metadata = MetadataFile(file=path)
        self.assertEqual('test_collection', metadata.get_collection(), 'Wrong collection.')
        self.assertEqual('THR', metadata.get_collection_permission(), 'Wrong permission.')
        self.assertEqual(['test_keyword_01'], metadata.get_keywords(), 'Wrong keywords.')
        self.assertEqual('test_publisher', metadata.get_publisher(), 'Wrong publisher.')
        self.assertEqual('CC BY-NC-SA 4.0', metadata.get_license(), 'Wrong licence.')

    def test_extract_metadata002_metadata_from_file(self):
        path_excel = '..\\h5p_test_files\\test_excel_file.xlsx'
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
        path_excel = '..\\h5p_test_files\\test_excel_file.xlsx'
        metadata = MetadataFile(file=path_excel)
        element_test = 'test.h5p'
        metadata_file = metadata.find_metadata_by_file_name(element_test)
        self.assertEqual(1, metadata_file, 'Multiple metadata matches.')

    def test_extract_metadata004_check_for_files(self):
        path_excel = '..\\h5p_test_files\\test_excel_file.xlsx'
        metadata = MetadataFile(file=path_excel)
        filenames = ['test.h5p', 'test02.h5p', 'test03.h5p', 'test_false.h5p']
        file_exist = True
        try:
            metadata.check_for_files(filenames=filenames)
        except ParsingError:
            file_exist = False
        self.assertFalse(file_exist, "Files aren\'t present in the Excel-Sheet")

    def test_extract_metadata005_fill_zeros(self):
        path_excel = '..\\h5p_test_files\\test_excel_file.xlsx'
        metadata = MetadataFile(file=path_excel)
        res = metadata.fill_zeros('4')
        self.assertEqual('04', res, 'Wrong upfilling zeros.')


if __name__ == '__main__':
    unittest.main()
