
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

    response = client.list_buckets()
    for bucket in response['Buckets']:
        if bucket['Name'] == bucket_name:
            break
    else:
        raise RuntimeError(f'Bucket {bucket_name} does not exist')

    response = client.list_objects_v2(Bucket=bucket_name)
    objects = response['Contents']

    print(f'Objects in bucket {bucket_name}:')
    print(f'{"Name":>40}{"Size":>16}{"Last Modified":>32}')
    for obj in objects:
        print(f'{obj["Key"]:>40}{obj["Size"]:>16}{obj["LastModified"].ctime():>32}')


if __name__ == '__main__':
    main()
