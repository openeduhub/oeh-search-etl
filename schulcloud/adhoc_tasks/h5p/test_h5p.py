import unittest
from schulcloud.adhoc_tasks.h5p.edusharing import EdusharingAPI
from schulcloud.adhoc_tasks.h5p.h5p_upload import util
from schulcloud.adhoc_tasks.h5p.h5p_upload import S3Downloader

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

    def test_edusharing_make_request(self):
        url = f'/admin/v1/applications'
        response = self.api.make_request('GET', url)

        self.assertEqual(200, response.status_code, 'Can\'t connect to Edusharing')

    def test_edusharing_create_user(self):
        # ToDo: Why get a '400' status code of this method back, although the user is created?
        name = 'TestUser'
        self.api.create_user(name, '123456', 'system')
        url_check = f'/iam/v1/people/-home-/{name}'
        result = self.api.make_request('GET', url_check)
        result = result.json()
        self.assertEqual('TestUser', result['person']['userName'], "TestUser NOT successfully created.")

        url_delete = f'/iam/v1/people/-home-/{name}'
        self.api.make_request('GET', url_delete)


if __name__ == '__main__':
    unittest.main()
