import os

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
    directory = env['S3_DOWNLOAD_DIRECTORY']

    if not os.path.exists(directory):
        os.makedirs(directory)

    response = client.list_buckets()
    for bucket in response['Buckets']:
        if bucket['Name'] == bucket_name:
            break
    else:
        raise RuntimeError(f'Bucket {bucket_name} does not exist')

    response = client.list_objects_v2(Bucket=bucket_name)
    objects = response['Contents']

    print(f'Download all objects from bucket {bucket_name}')
    total_size = sum([obj['Size'] for obj in objects])
    progress_bar = tqdm.tqdm(total=total_size, unit='B', unit_scale=True, unit_divisor=1024)
    for obj in objects:
        progress_bar.set_description(obj['Key'])
        filename = os.path.join(directory, obj['Key'])
        client.download_file(
            Bucket=bucket_name,
            Key=obj['Key'],
            Filename=filename,
            Callback=lambda n: progress_bar.update(n)
        )
    progress_bar.close()


if __name__ == '__main__':
    main()
