import hashlib
import time
import unittest
import zipfile
import os

from schulcloud.edusharing import EdusharingAPI, NotFoundException
from schulcloud import util
from schulcloud.h5p.upload import S3Downloader, MetadataNotFoundError
from schulcloud.h5p.upload import Uploader
from schulcloud.h5p.extract_metadata import MetadataFile

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

    test_folder = api.get_or_create_node('-userhome-', 'test1', type='folder')

    def test_edusharing001_make_request(self):
        url = f'/admin/v1/applications'
        response = self.api.make_request('GET', url)

        self.assertEqual(200, response.status_code, 'Can\'t connect to Edusharing')

    def test_edusharing005_get_sync_obj_folder(self):
        self.assertTrue(self.api.get_sync_obj_folder(), 'Could not get SYNC_OBJ folder.')

    def test_edusharing002_create_delete_user(self):
        # ToDo: Why get a '400' status code of this method back, although the user is created?
        name = 'TestUser'
        self.api.create_user(name, '123456', 'system')
        try:
            username = self.api.get_user(name)['person']['userName']
        except NotFoundException:
            username = None

        self.api.delete_user(name)
        try:
            self.api.get_user(name)
            self.fail('User found after deletion')
        except NotFoundException:
            pass

        self.assertEqual('TestUser', username, 'TestUser NOT successfully created.')

    def test_edusharing007_create_delete_node_get_children(self):
        new_folder = self.api.create_node(self.test_folder.id, 'test_folder', type='folder')
        new_file = self.api.create_node(self.test_folder.id, 'test_file', type='file')
        children = self.api.get_children(self.test_folder.id)
        self.api.delete_node(new_folder.id)
        self.api.delete_node(new_file.id)
        children_after_delete = self.api.get_children(self.test_folder.id)
        self.assertTrue(new_folder in children, 'Created folder not found')
        self.assertTrue(new_file in children, 'Created file not found')
        self.assertTrue(new_folder not in children_after_delete, 'Folder still exists after delete')
        self.assertTrue(new_file not in children_after_delete, 'File still exists after delete')

    def test_edusharing004_get_or_create_folder(self):
        folder_name = 'test_folder0'

        new_folder = self.api.get_or_create_node(self.test_folder.id, folder_name, type='folder')

        children = self.api.get_children(self.test_folder.id)
        for child in children:
            if child.id == new_folder.id:
                break
        else:
            self.fail('Could not create folder')

        new_folder2 = self.api.get_or_create_node(self.test_folder.id, folder_name, type='folder')

        self.api.delete_node(new_folder.id)

        self.assertTrue(new_folder.id == new_folder2.id, 'get_or_create_node() does not return the same folder')

    def test_edusharing003_find_node_by_name(self):
        node_name = 'test_folder1'
        created_node = self.api.create_node(self.test_folder.id, node_name, 'folder')
        node = self.api.find_node_by_name(self.test_folder.id, node_name)
        self.api.delete_node(created_node.id)
        self.assertTrue(created_node == node and node.name == node_name, 'find_node_by_name() returned unexpected node')

    def test_edusharing008_set_permission(self):
        groups = ['Thuringia-public', 'Brandenburg-public', 'LowerSaxony-public']
        self.api.set_permissions(self.test_folder.id, groups, True)
        permissions = self.api.get_permissions(self.test_folder.id)
        permitted_groups = []
        for permission_entry in permissions['permissions']['localPermissions']['permissions']:
            permitted_groups.append(permission_entry['authority']['authorityName'].replace('GROUP_', ''))

        for group in groups:
            self.assertTrue(group in permitted_groups, 'Permission not found.')

    def test_edusharing009_get_metadata(self):
        response = self.api.get_metadata(self.test_folder.id)
        self.assertEqual(self.test_folder.name, response['node']['name'], 'Can\'t get metadata of node.')

    def test_edusharing010_sync_node(self):
        name = 'test_file'
        folder_name = 'test_folder'
        properties = {
            'access': [
                'Read',
                'ReadAll',
                'Comment',
                'Feedback',
                'AddChildren',
                'ChangePermissions',
                'Write',
                'Delete',
                'CCPublish'
            ],
            'cm:name': [name],
            'cm:title': [name],
            'cm:edu_metadataset': ['mds_oeh'],
            'cm:edu_forcemetadataset': ['true'],
            'ccm:replicationsource': [folder_name],
            'ccm:replicationsourceid': [hashlib.sha1(name.encode()).hexdigest()],
            'ccm:lom_relation': ['']
        }
        response = self.api.sync_node(folder_name, properties, ['ccm:replicationsource', 'ccm:replicationsourceid'])
        sub_str = 'file'
        res = response.name[:response.name.index(sub_str) + len(sub_str)]
        self.api.delete_node(response.id)
        self.assertEqual(name, res, 'Can\'t create node.')

    def test_edusharing011_file_exists(self):
        name = 'test_file'
        node = self.api.create_node(self.test_folder.id, name)
        time.sleep(5)
        response = self.api.file_exists(self.test_folder.id, name=name)
        self.api.delete_node(node.id)
        self.assertTrue(response, 'Can\'t find file.')

    def test_edusharing012_search_custom(self):
        node_name = 'searchable_file'
        node = self.api.create_node(self.test_folder.id, 'searchable_file')
        time.sleep(10)
        response = self.api.search_custom('name', node_name, 50, 'FILES')
        self.api.delete_node(node.id)
        if response:
            self.assertEqual(node_name, response[0].name, 'Can\'t find folder.')
        else:
            self.fail('Can\'t find folder.')

    def test_edusharing014_set_preview_thumbnail(self):
        node = self.api.create_node(self.test_folder.id, 'thumbnail_file')
        self.api.set_preview_thumbnail(node.id, 'schulcloud/h5p/H5Pthumbnail.png')

        url_check_prop = f'/node/v1/nodes/-home-/{node.id}/prepareUsage'
        response = self.api.make_request('POST', url_check_prop).json()

        self.api.delete_node(node.id)

        self.assertEqual('TYPE_USERDEFINED', response['node']['preview']['type'], 'The thumbnail were not set.')

    def test_extract_metadata001_metadata(self):
        path = 'schulcloud/h5p/h5p_test_files/test_excel_file.xlsx'
        metadata = MetadataFile(file=path)
        collection = metadata.collections[0]
        self.assertEqual('test_collection', collection.name, 'Wrong collection.')
        self.assertEqual({'THR'}, collection.permissions, 'Wrong permission.')
        self.assertTrue(len(collection.keywords) == 10, 'Wrong keywords.')
        for keyword in collection.keywords:
            if not (keyword.startswith('test_keyword_') and len(keyword) == len('test_keyword_01')):
                self.fail('Keywords are not as expected.')
        self.assertEqual({'test_publisher'}, collection.publishers, 'Wrong publisher.')
        self.assertEqual({'CC BY-NC-SA 4.0', 'CC BY-NC-SA 4.1', 'CC BY-NC-SA 4.2', 'CC BY-NC-SA 4.3', 'CC BY-NC-SA 4.4'}, collection.licenses, 'Wrong licence.')

    def test_extract_metadata002_metadata_from_file(self):
        path_excel = 'schulcloud/h5p/h5p_test_files/test_excel_file.xlsx'
        metadata = MetadataFile(file=path_excel)
        for file in metadata.collections[0].children:
            if file.filepath == 'test.h5p':
                break
        else:
            self.fail('Could not find test.h5p in test metadata')

        self.assertEqual('test_collection', file.collection.name, 'Wrong collection.')
        self.assertEqual(['THR'], file.permission, 'Wrong permission.')
        self.assertEqual(['test_keyword_01'], file.keywords, 'Wrong keywords.')
        self.assertEqual('test_publisher', file.publisher, 'Wrong publisher.')
        self.assertEqual('CC BY-NC-SA 4.0', file.license, 'Wrong license.')
        self.assertEqual('01. test_title_01', file.title, 'Wrong title.')
        self.assertEqual('1', file.order, 'Wrong order.')

    def test_h5p_upload_setup_destination_folder(self):
        folder_name = 'h5p_test_folder'
        sync_obj = self.api.get_sync_obj_folder()
        self.uploader.setup_destination_folder(folder_name)
        try:
            node = self.api.find_node_by_name(sync_obj.id, folder_name)
        except NotFoundException as exc:
            self.fail('Failed to setup destination folder! ' + str(exc))
        self.api.delete_node(node.id)

    def test_h5p_upload_get_metadata_and_excel_file(self):
        path = os.path.join('schulcloud/h5p/h5p_test_files', 'test_upload_collection.zip')
        zip = zipfile.ZipFile(path)
        try:
            metadata_file = self.uploader.get_metadata_file(zip)
        except RuntimeError:
            self.fail('Failed to get metadata file and excel file!')
        self.assertTrue(metadata_file is not None, 'Failed to get metadata file and excel file!')

    def test_h5p_upload_no_excel_get_metadata_and_excel_file(self):
        path = os.path.join('schulcloud/h5p/h5p_test_files', 'test_get_metadata.zip')
        zip = zipfile.ZipFile(path)
        try:
            metadata_file = self.uploader.get_metadata_file(zip)
        except MetadataNotFoundError:
            pass
        else:
            self.fail('Failed: Created excel file without an excel file in the zip!')

    # S3 Download
    def test_h5p_upload_check_bucket_exists(self):
        try:
            self.downloader.check_bucket_exists()
        except RuntimeError:
            self.fail('Failed to find an existing s3 bucket')

    def test_h5p_upload_check_bucket_exists_fail(self):
        test = False
        try:
            self.downloaderFail.check_bucket_exists()
        except RuntimeError:
            test = True
        self.assertTrue(test, 'Failed: Found not existing s3 bucket.')

    def test_h5p_upload_get_object_list(self):
        obj_list = self.downloader.get_object_list()
        key_list = []
        for obj in obj_list:
            key_list.append(obj['Key'])
        self.assertEqual(['h5pTest/test_upload_collection.zip', 'h5pTest/test_upload_non_collection.zip'], key_list,
                         'Failed to get object list!')


if __name__ == '__main__':
    unittest.main()
