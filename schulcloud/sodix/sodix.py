
import requests
from schulcloud import util

needed_envs = ['SODIX_USER', 'SODIX_PASSWORD']


class SodixApi:
    URL_LOGIN = 'https://api.sodix.de/gql/auth/login'
    URL_GRAPHQL = 'https://api.sodix.de/gql/graphql'

    def __init__(self):
        env = util.Environment(env_vars=needed_envs)
        self.user = env['SODIX_USER']
        self.password = env['SODIX_PASSWORD']
        self.access_token = ''
        self.login()

    def login(self):
        response = requests.post(
            self.URL_LOGIN,
            headers={'Content-Type': 'application/json'},
            data=f'{{"login": "{self.user}", "password": "{self.password}"}}'
        )
        body = response.json()
        if response.status_code != 200 or body['error'] is not None:
            raise RuntimeError(f'login failed: {response.text}')
        self.access_token = body['access_token']

    def make_request(self, graphql_request: str) -> dict:
        if not self.access_token:
            raise RuntimeError('No access token. Not logged in?')
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.access_token}'
        }
        body = {'query': graphql_request}
        response = requests.post(self.URL_GRAPHQL, headers=headers, json=body)
        response.raise_for_status()
        return response.json()
