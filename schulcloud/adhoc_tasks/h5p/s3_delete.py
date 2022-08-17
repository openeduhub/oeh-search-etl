import sys

import boto3

import util


def main():
    env = util.Environment()

    client = boto3.client(
        's3',
        endpoint_url=env['S3_ENDPOINT_URL'],
        aws_access_key_id=env['S3_ACCESS_KEY'],
        aws_secret_access_key=env['S3_SECRET_KEY'],
    )
    bucket_name = env['S3_BUCKET_NAME']

    if len(sys.argv) < 2 or '--help' in sys.argv:
        print(f'Usage: {sys.argv[0]} OBJECT')
        sys.exit()

    response = client.delete_object(Bucket=bucket_name, Key=sys.argv[1])
    if not 200 <= response['ResponseMetadata']['HTTPStatusCode'] < 300:
        raise RuntimeError(f'Error. Status code {response["ResponseMetadata"]["HTTPStatusCode"]}')


if __name__ == '__main__':
    main()
