import hashlib
import time
import unittest

from schulcloud.edusharing import EdusharingAPI
from schulcloud.fwu.upload_fwu import Uploader, S3Downloader, EdusharingAPI
import converter.env as env


class TestH5P(unittest.TestCase):
    api = EdusharingAPI(
        env.get('EDU_SHARING_BASE_URL'),
        env.get('EDU_SHARING_USERNAME'),
        env.get('EDU_SHARING_PASSWORD')
    )
    downloader = S3Downloader(
        env.get('S3_ENDPOINT_URL'),
        env.get('S3_ACCESS_KEY'),
        env.get('S3_SECRET_KEY'),
        env.get('S3_BUCKET_NAME')
    )
    uploader = Uploader()

    bucket_name = 'lernstore-test'

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
        username = self.api.get_user(name)['person']['userName']

        self.api.delete_user(name)
        self.api.get_user(name)
        self.fail('User found after deletion')

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
        time.sleep(10)
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

    # Test-cases for S3Download
    def test_s3Download_001_check_bucket_exists(self):
        response = self.downloader.check_bucket_exists(self.bucket_name)
        self.assertTrue(response, 'Bucket does not exist.')

    def test_s3Download_002_get_all_objects(self):
        response = self.downloader.get_all_objects()
        self.assertTrue(len(response) > 0, 'Don\'t get any object from bucket.')

    def test_s3Download_003_read_object(self):
        object_key = '5501191/index.html'
        response = self.downloader.read_object(object_key)
        self.assertTrue(len(response) > 0, f'Can\'t read object {object_key}.')

    # Test-cases for Uploader
    def test_FWU_Uploader_001_setup_destination_folder(self):
        test_folder_name = "fwu-test-folder"
        self.uploader.setup_destination_folder(test_folder_name)
        time.sleep(10)
        response = self.api.search_custom('name', test_folder_name, 10, 'FOLDERS')
        self.api.delete_node(response[0].id)
        self.assertEqual(response[0].name, test_folder_name, f'Can\'t find folder {test_folder_name}')

    def test_FWU_Uploader_002_upload(self):
        # test_folder_name = "fwu-test-folder"
        # files_index = ['test']
        # bucket_name = 'lernstore-test'
        # self.uploader.upload(files_index)
        # self.assertEqual('', test_folder_name, f'Can\'t find folder {test_folder_name}')
        pass

    def test_FWU_Uploader_003_get_data(self):
        body = '<!doctype html><!--[if lt IE 7]> <html class="no-js lt-ie9 lt-ie8 lt-ie7" lang="en"><div ' \
               'class="wrapper startwrapper"><div class="wrapper_inner"><div class="pname">Test Titel</div><div ' \
               'class="player_outer shadow border" onclick="window.location=\'menue/mainseq_1.html\'" ' \
               'style=\"background:url(test.jpg) no-repeat; background-size: cover;\"><a class=\"pskip\" ' \
               'href=\"menue/mainseq_1.html\"><img src=\'test.jpg\' alt=\'\' /></a><div class=\"player_wrapper\" ' \
               'style=\"position:relative; width:100%; height:100%;\"></div></div><div class=\"ptext\">Test ' \
               'Description</div></div></div></body></html>'
        title = self.uploader.get_data(body, 'pname')
        description = self.uploader.get_data(body, 'ptext')
        thumbnail_path = self.uploader.get_data(body, 'player_outer')

        self.assertEqual(title, "Test Titel", f'Wrong title.')
        self.assertEqual(description, "Test Description", f'Wrong description.')
        self.assertEqual(thumbnail_path, "test.jpg", f'Wrong thumbnail path.')

    def test_FWU_Uploader_004_validate_result(self):
        wrong_class = 'wrong'
        empty_result = ''

        try:
            self.uploader.validate_result(wrong_class, empty_result)
        except RuntimeError as e:
            self.assertEqual(type(e), RuntimeError)
        else:
            self.fail('RuntimeError not raised.')


    def test_FWU_Uploader_005_sanitize_string(self):
        test_string = "Äüöß'ä"
        response = self.uploader.sanitize_string(test_string)
        self.assertEqual(response, "Aeueoessae", f'The string were not sanitized right,')


if __name__ == '__main__':
    unittest.main()
