
import json

from schulcloud.sodix.sodix import SodixApi


query_string = '''
{
    publishers {
        id
        title
    }
}
'''


def main():
    api = SodixApi()
    response = api.make_request(query_string)
    file = open('schulcloud/sodix/all_publishers.json', 'w')
    file.write(json.dumps(response['data']['publishers'], indent=4))
    file.close()


if __name__ == '__main__':
    main()
