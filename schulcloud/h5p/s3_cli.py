import mimetypes
import sys
import os
from typing import List

import tqdm
import boto3
import converter.env as env

HELP = '''
To execute with .env, take oeh-search-etl as root dir and type: python -m schulcloud.h5p.s3_cli <command>
s3_cli list [ARGS] (List all objects in bucket, but max. 1000 entries)
s3_cli print_list [ARGS] (Prints all objects in bucket in a text file)
s3_cli upload <FILES...> [ARGS] (Upload files to bucket)
s3_cli upload_directory <DIRECTORY ABSOLUTE PATH...> [ARGS] (Upload a complete directory to bucket with subdirectories)
s3_cli download <FILES...> [ARGS] (Download files from bucket to local folder)
s3_cli delete <FILES...> [ARGS] (Deletes files from bucket)
s3_cli copy <FILES...> -bd <BUCKET_NAME_DESTINATION> [ARGS] (Copy files from one bucket to another)
s3_cli bucket list [ARGS] (List all buckets)
s3_cli bucket create <NAME> [ARGS] (Create a bucket)
s3_cli bucket delete <NAME> [ARGS] (Delete a bucket)
'''


def get_object_type(object_key: str):
    if mimetypes.guess_type(object_key)[0] is not None:
        return mimetypes.guess_type(object_key)[0]
    else:
        return "application/octet-stream"


class CLI:
    def __init__(self, url: str, access_key: str, secret: str):
        self.client = boto3.client(
            's3',
            endpoint_url=url,
            aws_access_key_id=access_key,
            aws_secret_access_key=secret,
        )
        self.s3 = boto3.resource(
            's3',
            endpoint_url=url,
            aws_access_key_id=access_key,
            aws_secret_access_key=secret,
        )

    def ensure_bucket(self, bucket_name: str):
        """
        Check, if the bucket exists on AWS S3.
        @param bucket_name: Name of the bucket on AWS S3
        """
        response = self.client.list_buckets()
        for bucket in response['Buckets']:
            if bucket['Name'] == bucket_name:
                break
        else:
            raise RuntimeError(f'Bucket {bucket_name} does not exist')

    def get_objects(self, bucket_name: str):
        """
        Return a list with max. 1000 objects from AWS S3 bucket.
        @param bucket_name: Name of the bucket on AWS S3
        """
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

    def get_all_objects(self, bucket_name: str):
        """
        Get all objects from AWS S3 bucket and print the object keys into the file '[bucket_name]_all_objects-txt'.
        @param bucket_name: Name of the bucket on AWS S3
        """
        bucket = self.s3.Bucket(bucket_name)
        files_list = []
        counter = 0

        for object in bucket.objects.all():
            files = object.key
            files_list.append(files)
            counter += 1

        file_name = f'{bucket_name}_all_objects.txt'
        if os.path.exists(file_name):
            os.remove(file_name)
        file = open(file_name, 'w')
        file.write(f'Objects in bucket {bucket_name}:\n')
        file.write(f'Name:\n')

        for object in files_list:
            file.write(f'{object}\n')

        file.write(f'\n')
        file.write(f'Totally {counter} objects.')
        file.close()
        print(f'Objects in bucket {bucket_name} were printed to {file_name} in this directory.')

    def get_objects_matching(self, bucket_name: str, objects: List[str]):
        """
        Return a filtered list, which contains the matching objects between a matching list and the remote objects
        on AWS S3 bucket.
        @param bucket_name: Name of the bucket on AWS S3
        @param objects: List of matching objects
        """
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
        """
        Print max. 1000 objects from the AWS S3 bucket into the console.
        @param bucket_name: Name of the bucket on AWS S3
        """
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
        """
        Upload local files from the list to the AWS S3 bucket.
        @param bucket_name: Name of the bucket on AWS S3
        @param objects: List of local objects for the upload
        """
        self.ensure_bucket(bucket_name)
        print(f'Upload {len(objects)} object(s) to bucket {bucket_name}')
        total_size = 0
        for file in objects:
            total_size += os.stat(file).st_size
        progress_bar = tqdm.tqdm(total=total_size, unit='B', unit_scale=True, unit_divisor=1024)
        for file in objects:
            progress_bar.set_description(file)
            file_key = os.path.basename(file)
            self.client.upload_file(Bucket=bucket_name, Filename=file, Key=file_key,
                                    Callback=lambda n: progress_bar.update(n), ContentType=get_object_type(file_key))
        progress_bar.close()

    def upload_directory(self, bucket_name, root_path):
        """
        Upload the content from a local directory to the AWS S3 bucket.
        @param bucket_name: Name of the bucket on AWS S3
        @param root_path: Path to the local directory
        """
        self.ensure_bucket(bucket_name)
        file_counter = 0

        for path, subdirs, files in os.walk(root_path):
            path = path.replace("\\", "/")
            total_size = 0
            for file in files:
                file_counter += 1
                if len(path) > len(root_path):
                    total_size += os.stat(path + '/' + file).st_size
                else:
                    total_size += os.stat(root_path + '/' + file).st_size
            progress_bar = tqdm.tqdm(total=total_size, unit='B', unit_scale=True, unit_divisor=1024)

            for file in files:
                # Extract the last direction name of the root_path with subdirections for the S3-key
                root_path = root_path.replace("\\", "/")
                if len(path) > len(root_path):
                    head_root, tail_root = os.path.splitdrive(root_path)
                    filename_sanitize_root = os.path.basename(tail_root)
                    direction = path.replace(root_path, "")
                    filename_sanitize = filename_sanitize_root + direction
                else:
                    head_root, tail_root = os.path.splitdrive(root_path)
                    filename_sanitize = os.path.basename(tail_root)

                progress_bar.set_description(file)
                file_key = filename_sanitize + '/' + file
                self.client.upload_file(Filename=os.path.join(path, file),
                                        Bucket=bucket_name,
                                        Key=file_key,
                                        Callback=lambda n: progress_bar.update(n),
                                        ExtraArgs={'ContentType': get_object_type(file_key)})
            progress_bar.close()

        print(f'Sucessfully upload {file_counter} files from {root_path} to bucket {bucket_name}.')

    def download_objects(self, dir_name: str, bucket_name: str, objects: List[str]):
        """
        Download all objects from the AWS S3 bucket matching with the list objects to a local directory.
        @param dir_name: Local directory to download the objects to
        @param bucket_name: Name of the bucket on AWS S3
        @param objects: List of objects for the download
        """
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
        """
        Delete all objects from the AWS S3 bucket matching with the list objects.
        @param bucket_name: Name of the bucket on AWS S3
        @param objects: List of objects for deletion
        """
        self.ensure_bucket(bucket_name)
        remote_objects = self.get_objects_matching(bucket_name, objects)
        for object in remote_objects:
            response = self.client.delete_object(Bucket=bucket_name, Key=object['Key'])
            print(response)

    def copy_objects(self, bucket_name: str, bucket_name_destination: str, objects: List[str]):
        """
        Copy all objects from one AWS S3 bucket to another AWS S3 bucket.
        @param bucket_name: Name of the bucket on AWS S3 to copy from
        @param bucket_name_destination: Name of the bucket on AWS S3 to copy to
        @param objects: List of objects for the download
        """
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
        """
        Print the existing AWS S3 buckets from the AWS account into the console.
        """
        response = self.client.list_buckets()
        for bucket in response['Buckets']:
            print(bucket['Name'])

    def create_bucket(self, bucket_name: str):
        """
        Copy all objects from one AWS S3 bucket to another AWS S3 bucket.
        @param bucket_name: Name of the bucket on AWS S3
        """
        self.client.create_bucket(Bucket=bucket_name)

    def delete_bucket(self, bucket_name: str):
        """
        Delete a bucket with content from AWS S3.
        @param bucket_name: Name of the bucket on AWS S3
        """
        self.ensure_bucket(bucket_name)
        answer = input(f'Are you sure to delete {bucket_name} (y/N)? ')
        if answer.lower() in ('y', 'yes', 'j', 'ja'):
            self.client.delete_bucket(Bucket=bucket_name)


def get_vars(var_names: List[str]):
    """
    Get all required environment variables from the list.
    @param var_names: List of environment variables
    """
    vars = []
    for var_name in var_names:
        vars.append(env.get(var_name))
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

    if command in ['list', 'print_list', 'upload', 'upload_directory', 'download', 'delete'] and not bucket:
        bucket = get_vars(['S3_BUCKET_NAME'])[0]

    if command == 'list':
        cli.list_objects(bucket)
    elif command == 'print_list':
        cli.get_all_objects(bucket)
    elif command == 'upload':
        cli.upload_objects(bucket, rest)
    elif command == 'upload_directory':
        cli.upload_directory(bucket, rest[0])
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
