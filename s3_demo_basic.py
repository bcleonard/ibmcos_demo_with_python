import boto3
from boto3 import client
import configparser
from os import getenv
from botocore.exceptions import ClientError
from typing import BinaryIO
import time

#
# source inspiration of script
# https://dev.to/nelsoncode/aws-s3-with-python-3bnn
#

BUCKET_NAME = 'bclcliapitestbucket'

def list_buckets():
    try:
        response = clientS3.list_buckets()
        print('Existing buckets:')
        for bucket in response['Buckets']:
          print(f'  {bucket["Name"]}')
        return "success"
    except ClientError as e:
        return e.response["Error"]

def create_bucket(bucket: str):
    try:
        response = clientS3.create_bucket(Bucket=bucket)
        return response
    except ClientError as e:
        return e.response["Error"]

def list_bucket_contents(bucket: str):
     # print the contects of the bucket
    try:
        objects = clientS3.list_objects_v2(Bucket=bucket)
        fileCount = objects['KeyCount']
        if fileCount == 0:
           print(f'bucket', bucket, 'is empty.')
        else:
           key = []
           print(f'bucket', bucket, 'has ',fileCount,' objects.')
           for obj in objects['Contents']:
            print(f' object name: ',obj['Key']) 
        return "success"
    except ClientError as e:
        return e.response["Error"]

def delete_file(bucket: str, filename: str):
    try:
        response = clientS3.delete_object(Bucket=bucket, Key=filename)
        return response
    except ClientError as e:
        return e.response["Error"]

def delete_bucket(bucket: str):
    try:
        objects = clientS3.list_objects_v2(Bucket=bucket)
        fileCount = objects['KeyCount']
        if fileCount == 0:
           print(f'bucket', bucket, 'is empty.')
        else:
           key = []
           print(f'bucket', bucket, 'has ',fileCount,' objects.')
           for obj in objects['Contents']:
            print(f' deleting object: ',obj['Key'])
            delete_file(bucket,obj['Key'])

        response = clientS3.delete_bucket(Bucket=bucket)
        return response
    except ClientError as e:
        return e.response["Error"]

# create the connection
#clientS3 = client("s3",
#                  aws_access_key_id=ACCESS_KEY,
#                  aws_secret_access_key=SECRET_ACCESS_KEY,
#                  endpoint_url=ACCESSER_URL
#                  )

session = boto3.Session(profile_name="ibmcos")
credentials = session.get_credentials()
print("AWS_ACCESS_KEY_ID = {}".format(credentials.access_key))
print("AWS_SECRET_ACCESS_KEY = {}".format(credentials.secret_key))
print("AWS_SESSION_TOKEN = {}".format(credentials.token))

config = configparser.ConfigParser()
config.read('../.aws/config')
endpoint_url=config['profile ibmcos']['endpoint_url']
print(endpoint_url)
endpoint_url.strip("'")
print(endpoint_url)

clientS3 = client("s3",
    aws_access_key_id=credentials.access_key,
    aws_secret_access_key=credentials.secret_key,
    endpoint_url=endpoint_url)

# retrieve the list of existing buckets
list_buckets()

# create bucket
create_bucket(BUCKET_NAME)

# wait for bucket to be created
print(f'sleep 60 seconds, waiting for bucket to be created')
time.sleep(60)

# Retrieve the list of existing buckets
list_buckets()

# list contents of bucket
list_bucket_contents(BUCKET_NAME)

# upload files
with open('/usr/bin/dockerd', 'rb') as data:
    clientS3.upload_fileobj(data, BUCKET_NAME, 'dockerd')

# list contents of bucket
list_bucket_contents(BUCKET_NAME)

# Retrieve the list of existing buckets
list_buckets()

print(f'sleep 60 seconds, waiting for you to check out the bucket')
time.sleep(60)

# delete bucket
delete_bucket(BUCKET_NAME)

print(f'sleep 60 seconds, waiting for bucket to be deleted')
time.sleep(60)

# Retrieve the list of existing buckets
list_buckets()

exit()
