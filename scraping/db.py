import boto3
import os

s3_client = boto3.client(
    's3',
    endpoint_url='https://s3.us-west-1.wasabisys.com/',
    aws_access_key_id=os.environ.get('WASABI_ACCESS_KEY'),
    aws_secret_access_key=os.environ.get('WASABI_SECRET_KEY')
)

def upload_object_to_wasabi(data, key, bucket='hackathon'):
    s3_client.put_object(Bucket=bucket, Key=key, Body=data)

def upload_file_to_wasabi(key, filename, bucket_name='hackathon'):
    s3_client.upload_file(key, bucket_name, filename)


if __name__ == '__main__':
    # upload a file to wasabi
    upload_file_to_wasabi('screenshot.png', 'screenshot.png')