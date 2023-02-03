import time
import unittest

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
    bucket_name = 'fwu-test-folder'

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

    def test_FWU_Uploader_002_get_data(self):
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

    def test_FWU_Uploader_003_validate_result(self):
        wrong_class = 'wrong'
        empty_result = ''

        try:
            self.uploader.validate_result(wrong_class, empty_result)
        except RuntimeError as e:
            self.assertEqual(type(e), RuntimeError)
        else:
            self.fail('RuntimeError not raised.')

    def test_FWU_Uploader_004_sanitize_string(self):
        test_string = "Äüöß'ä"
        response = self.uploader.sanitize_string(test_string)
        self.assertEqual(response, "Aeueoessae", f'The string were not sanitized right,')


if __name__ == '__main__':
    unittest.main()
