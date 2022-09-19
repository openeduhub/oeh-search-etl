import os
import sys

import boto3
import tqdm

import util


HELP = '''
s3_upload.py FOLDER_NAME FILES...

The folder name is used internally for s3 as well as edusharing.
'''

EXPECTED_ENV_VARS = [
    'S3_ENDPOINT_URL',
    'S3_ACCESS_KEY',
    'S3_SECRET_KEY',
    'S3_BUCKET_NAME'
]


def main():
    env = util.Environment(EXPECTED_ENV_VARS)
    client = boto3.client(
        's3',
        endpoint_url=env['S3_ENDPOINT_URL'],
        aws_access_key_id=env['S3_ACCESS_KEY'],
        aws_secret_access_key=env['S3_SECRET_KEY']
    )
    bucket_name = env['S3_BUCKET_NAME']

    if len(sys.argv) < 3:
        print(HELP)
        sys.exit()

    folder_name = sys.argv[1]
    if not folder_name.isalnum():
        print('Folder name should only contain alphanumerical characters')
        sys.exit(1)

    files = sys.argv[2:]
    for file in files:
        if not os.path.exists(file):
            print(f'{file} does not exist')
            sys.exit(2)

    total_size = 0
    for file in files:
        total_size += os.stat(file).st_size
    progress_bar = tqdm.tqdm(total=total_size, unit='B', unit_scale=True, unit_divisor=1024)
    for file in files:
        progress_bar.set_description(file)
        client.upload_file(
            Bucket=bucket_name,
            Filename=file,
            Key=f'{folder_name}/{os.path.basename(file)}',
            Callback=lambda n: progress_bar.update(n)
        )
    progress_bar.close()


if __name__ == '__main__':
    main()
