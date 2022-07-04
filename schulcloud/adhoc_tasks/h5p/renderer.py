
import util
import edusharing


ENV_VARS = ['EDU_SHARING_BASE_URL', 'EDU_SHARING_USERNAME', 'EDU_SHARING_PASSWORD']


def main():
    environment = util.Environment(ENV_VARS, ask_for_missing=True)

    api = edusharing.EdusharingAPI(
        environment['EDU_SHARING_BASE_URL'],
        environment['EDU_SHARING_USERNAME'],
        environment['EDU_SHARING_PASSWORD'])

    repository = '-home-'
    node_id = '0857f50e-7bd2-40bd-a3a2-b9eca661d254'
    # version=-1 (query param)
    url = f'/rendering/v1/details/{repository}/{node_id}'
    response = api.make_request('GET', url)
    response.raise_for_status()
    snippet = response.json()['detailsSnippet']

    file = open('snippet.html', 'w')
    file.write(snippet)
    file.close()


if __name__ == '__main__':
    main()
