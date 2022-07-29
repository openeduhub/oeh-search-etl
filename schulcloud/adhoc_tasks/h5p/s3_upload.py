import os
import sys

import tqdm
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
    files = sys.argv[1:]

    response = client.list_buckets()
    for bucket in response['Buckets']:
        if bucket['Name'] == bucket_name:
            break
    else:
        raise RuntimeError(f'Bucket {bucket_name} does not exist')

    response = client.list_objects_v2(Bucket=bucket_name)
    objects = response['Contents']

    print(f'Upload {len(files)} object(s) to bucket {bucket_name}')
    total_size = 0
    for file in files:
        total_size += os.stat(file).st_size
    progress_bar = tqdm.tqdm(total=total_size, unit='B', unit_scale=True, unit_divisor=1024)
    for file in files:
        progress_bar.set_description(file)
        client.upload_file(Bucket=bucket_name, Filename=file, Key=os.path.basename(file), Callback=lambda n: progress_bar.update(n))
    progress_bar.close()


if __name__ == '__main__':
    main()
