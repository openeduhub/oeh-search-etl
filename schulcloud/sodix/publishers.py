
import json
import requests

from schulcloud.util import Environment


query_string = '''
{
    publishers {
        id
        title
    }
}
'''


class SodixDownloader:
    URL_LOGIN = 'https://api.sodix.de/gql/auth/login'
    URL_REQUEST = 'https://api.sodix.de/gql/graphql'

    def __init__(self):
        environment = Environment(['SODIX_USER', 'SODIX_PASSWORD'], ask_for_missing=True)
        self.user = environment['SODIX_USER']
        self.password = environment['SODIX_PASSWORD']
        self.access_token = ''

    def get_headers(self):
        return {
            'Authorization': 'Bearer ' + self.access_token,
            'Content-Type': 'application/json'
        }

    def get_body(self):
        return json.dumps({'query': query_string})

    def login(self):
        response = requests.post(
            self.URL_LOGIN,
            headers={'Content-Type': 'application/json'},
            data=f'{{"login": "{self.user}", "password": "{self.password}"}}'
        )
        try:
            if not response.json()['error']:
                self.access_token = response.json()['access_token']
            else:
                raise UnexpectedResponseError(f'Unexpected login response: {response.json()}')
        except (KeyError, UnexpectedResponseError):
            raise UnexpectedResponseError(f'Unexpected login response: {response.json()}')

    def download(self):
        self.login()
        response = requests.post(self.URL_REQUEST, self.get_body(), headers=self.get_headers())
        file = open('schulcloud/sodix/all_publishers.json', 'w')
        file.write(json.dumps(response.json()['data']['publishers'], indent=4))
        file.close()
        print('Success.')


class UnexpectedResponseError(Exception):
    pass


if __name__ == '__main__':
    SodixDownloader().download()
