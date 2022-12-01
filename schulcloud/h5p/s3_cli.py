import sys
import os
from typing import List

import tqdm
import boto3

HELP = '''
Usage:
s3_cli list                                     list all buckets
s3_cli create <BUCKET_NAME>                     create new bucket
s3_cli delete <BUCKET_NAME>                     delete bucket
s3_cli -b [BUCKET] list                         list content of bucket
s3_cli -b [BUCKET] upload <FILES...>            upload files to bucket
s3_cli -b [BUCKET] download <FILES...>          download files from bucket
s3_cli -b [BUCKET] delete <FILES...>            delete files from bucket
'''


class S3CLI:
    def __init__(self, url: str, access_key: str, secret: str):
        self.client = boto3.client(
            's3',
            endpoint_url=url,
            aws_access_key_id=access_key,
            aws_secret_access_key=secret,
        )

    def ensure_bucket(self, bucket_name: str):
        response = self.client.list_buckets()
        for bucket in response['Buckets']:
            if bucket['Name'] == bucket_name:
                break
        else:
            raise RuntimeError(f'Bucket {bucket_name} does not exist')

    def get_objects(self, bucket_name: str):
        remote_objects = []
        continuation_token = ''
        while True:
            response = self.client.list_objects_v2(Bucket=bucket_name, ContinuationToken=continuation_token)
            remote_objects.extend(response['Contents'])
            if response['isTruncated']:
                continuation_token = response['NextContinuationToken']
            else:
                break
        return remote_objects

    def get_objects_matching(self, bucket_name: str, objects: List[str]):
        remote_objects = self.get_objects(bucket_name)
        filtered = []
        for obj in objects:
            if obj.endswith('*'):
                prefix = obj[:-1]
                for remote_obj in remote_objects:
                    if remote_obj['Key'].startswith(prefix):
                        filtered.append(remote_obj)
            else:
                for remote_obj in remote_objects:
                    if remote_obj['Key'] == obj:
                        filtered.append(remote_obj)
                        break
                else:
                    raise RuntimeError(f'Object {obj} not found in {bucket_name}')

    def list_objects(self, bucket_name: str):
        self.ensure_bucket(bucket_name)
        response = self.client.list_objects_v2(Bucket=bucket_name)
        if 'Contents' not in response:
            print('Bucket seems to be empty.')
        else:
            print(f'Objects in bucket {bucket_name}:')
            print(f'{"Name":>40}{"Size":>16}{"Last Modified":>32}')
            for obj in response['Contents']:
                print(f'{obj["Key"]:>40}{obj["Size"]:>16}{obj["LastModified"].ctime():>32}')

    def upload_objects(self, bucket_name: str, objects: List[str]):
        self.ensure_bucket(bucket_name)
        print(f'Upload {len(objects)} object(s) to bucket {bucket_name}')
        total_size = 0
        for file in objects:
            total_size += os.stat(file).st_size
        progress_bar = tqdm.tqdm(total=total_size, unit='B', unit_scale=True, unit_divisor=1024)
        for file in objects:
            progress_bar.set_description(file)
            self.client.upload_file(Bucket=bucket_name, Filename=file, Key=os.path.basename(file),
                                    Callback=lambda n: progress_bar.update(n))
        progress_bar.close()

    def download_objects(self, dir_name: str, bucket_name: str, objects: List[str]):
        self.ensure_bucket(bucket_name)
        remote_objects = self.get_objects_matching(bucket_name, objects)

        print(f'Download {len(remote_objects)} objects from bucket {bucket_name}')
        total_size = sum([obj['Size'] for obj in remote_objects])
        progress_bar = tqdm.tqdm(total=total_size, unit='B', unit_scale=True, unit_divisor=1024)
        for obj in remote_objects:
            progress_bar.set_description(obj['Key'])
            filename = os.path.join(dir_name, obj['Key'])
            if not os.path.exists(os.path.dirname(filename)):
                os.makedirs(os.path.dirname(filename))
            fileobj = open(filename, 'wb')
            self.client.download_fileobj(
                Bucket=bucket_name,
                Key=obj['Key'],
                Fileobj=fileobj,
                Callback=lambda n: progress_bar.update(n)
            )
        progress_bar.close()
        print(f'Objects saved to {dir_name}')

    def delete_objects(self, bucket_name: str, objects: List[str]):
        self.ensure_bucket(bucket_name)
        remote_objects = self.get_objects_matching(bucket_name, objects)
        for object in remote_objects:
            response = self.client.delete_object(Bucket=bucket_name, Key=object['Key'])
            print(response)

    def list_buckets(self):
        response = self.client.list_buckets()
        for bucket in response['Buckets']:
            print(bucket['Name'])

    def create_bucket(self, bucket_name: str):
        self.client.create_bucket(Bucket=bucket_name)

    def delete_bucket(self, bucket_name: str):
        self.ensure_bucket(bucket_name)
        answer = input(f'Are you sure to delete {bucket_name} (y/N)? ')
        if answer.lower() in ('y', 'yes', 'j', 'ja'):
            self.client.delete_bucket(Bucket=bucket_name)


def get_vars(var_names: List[str]):
    vars = []
    for var_name in var_names:
        vars.append(os.getenv(var_name))
    for i in range(len(vars)):
        if not vars[i]:
            print(f'{var_names[i]} not found in environment variables')
    for i in range(len(vars)):
        while not vars[i]:
            vars[i] = input(f'{var_names[i]}: ')
    return vars


def main():
    if '-h' in sys.argv or '--help' in sys.argv or len(sys.argv) <= 1:
        print(HELP)
        sys.exit()

    vars = get_vars(['S3_ENDPOINT_URL', 'S3_ACCESS_KEY', 'S3_SECRET_KEY'])
    s3 = S3CLI(*vars)

    if sys.argv[1] == 'list':
        pass
    if sys.argv[1] == 'create':
        pass
    if sys.argv[1] == 'delete':
        pass
    if sys.argv[1] == '-b':
        bucket_name = sys.argv[2]
        if sys.argv[3] == 'list':
            s3.list_objects(bucket_name)
        elif sys.argv[3] == 'upload':
            s3.upload_objects(bucket_name, sys.argv[4:])
        elif sys.argv[3] == 'download':
            s3.download_objects('.', bucket_name, sys.argv[4:])
        elif sys.argv[3] == 'delete':
            s3.delete_objects(bucket_name, sys.argv[4:])
    else:
        print('Unknown command')
        print(HELP)
        sys.exit(1)


if __name__ == '__main__':
    main()
