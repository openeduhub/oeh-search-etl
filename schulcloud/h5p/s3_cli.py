import sys
import os
from typing import List

import tqdm
import boto3

HELP = '''
s3_cli list [ARGS]
s3_cli upload <FILES...> [ARGS]
s3_cli download <FILES...> [ARGS]
s3_cli delete <FILES...> [ARGS]
s3_cli copy <FILES...> -bd <BUCKET_NAME_DESTINATION> [ARGS]
s3_cli bucket list [ARGS]
s3_cli bucket create <NAME> [ARGS] 
s3_cli bucket delete <NAME> [ARGS]
'''


class CLI:
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
            if response['IsTruncated']:
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
        return filtered

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

    def copy_objects(self, bucket_name: str, bucket_name_destination: str, objects: List[str]):
        self.ensure_bucket(bucket_name)
        self.ensure_bucket(bucket_name_destination)
        for object in objects:
            copy_source = {
                'Bucket': f'{bucket_name}',
                'Key': f'{object}'
            }
            self.client.copy(copy_source, bucket_name_destination, object)
        print(f'Object was copied successfully from bucket {bucket_name} to bucket {bucket_name_destination}.')

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
    cli = CLI(*vars)

    if sys.argv[1] == 'bucket':
        if len(sys.argv) < 3:
            print(HELP)
            sys.exit(1)
        command = 'bucket_' + sys.argv[2]
        i = 3
    else:
        command = sys.argv[1]
        i = 2

    bucket = ''
    bucket_destination = ''
    rest = []
    while i < len(sys.argv):
        arg = sys.argv[i]
        if arg == '-b':
            bucket = sys.argv[i + 1]
            i += 1
        elif arg == '-bd':
            bucket_destination = sys.argv[i + 1]
            i += 1
        else:
            rest.append(arg)
        i += 1

    if command in ['list', 'download', 'upload', 'delete'] and not bucket:
        bucket = get_vars(['S3_BUCKET_NAME'])[0]

    if command == 'list':
        cli.list_objects(bucket)
    elif command == 'upload':
        cli.upload_objects(bucket, rest)
    elif command == 'download':
        dir = '.' if len(rest) == 1 else 'downloaded'
        cli.download_objects(dir, bucket, rest)
    elif command == 'delete':
        cli.delete_objects(bucket, rest)
    elif command == 'copy':
        cli.copy_objects(bucket, bucket_destination, rest)
    elif command == 'bucket_list':
        cli.list_buckets()
    elif command == 'bucket_create':
        if not len(rest) == 1:
            print('Invalid arguments')
            print(HELP)
            sys.exit(1)
        cli.create_bucket(rest[0])
    elif command == 'bucket_delete':
        if not len(rest) == 1:
            print('Invalid arguments')
            print(HELP)
            sys.exit(1)
        cli.delete_bucket(rest[0])
    else:
        print('Unknown command')
        print(HELP)
        sys.exit(1)


if __name__ == '__main__':
    main()
