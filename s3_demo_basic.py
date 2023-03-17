#!/usr/bin/python3

from boto3 import client
import configparser
from botocore.exceptions import ClientError
import time
import argparse

#
# source inspiration of script
# https://dev.to/nelsoncode/aws-s3-with-python-3bnn
#

#
# global variables
#
CONFIG_FILE = "demo_config.txt"

#
# defined functions
#
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
            print(f'bucket', bucket, 'has ', fileCount, ' objects.')
            for obj in objects['Contents']:
                print(f' object name: ', obj['Key'])
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
            print(f'bucket', bucket, 'has ', fileCount, ' objects.')
            for obj in objects['Contents']:
                print(' deleting object: ', obj['Key'])
                delete_file(bucket, obj['Key'])

        response = clientS3.delete_bucket(Bucket=bucket)
        return response
    except ClientError as e:
        return e.response["Error"]


#
# parse command line
#
parser = argparse.ArgumentParser(description="conduct a very basic IBM COS "
                                 "s3 demo")
parser.add_argument("-c", "--config",
                    help="Alternate configuration file",
                    required=False,
                    default="")
argument = parser.parse_args()

if (argument.config):
    CONFIG_FILE = format(argument.config)
    print("\nUsing alternate configuration file: ", CONFIG_FILE)

#
# parse configuration file
#
config = configparser.ConfigParser()
config.read(CONFIG_FILE)
access_key = config['s3_demo_basic']['access_key_id']
secret_access_key = config['s3_demo_basic']['secret_access_key']
accesser = config['s3_demo_basic']['accesser_url']
bucket = config['s3_demo_basic']['bucket']

print("\ns3_demo_basic Configuration:")
print("         Access Key: ", access_key)
print("  Secret Access Key: ", secret_access_key)
print("       Accesser URL: ", accesser)
print("             Bucket: ", bucket)
print("")

#
# run demo
#

# create connection
clientS3 = client("s3",
                  aws_access_key_id=access_key,
                  aws_secret_access_key=secret_access_key,
                  endpoint_url=accesser)

# retrieve the list of existing buckets
list_buckets()

# create bucket
create_bucket(bucket)

# wait for bucket to be created
print('sleep 60 seconds, waiting for bucket to be created')
time.sleep(60)

# Retrieve the list of existing buckets
list_buckets()

# list contents of bucket
list_bucket_contents(bucket)

# upload files
with open('/usr/bin/dockerd', 'rb') as data:
    clientS3.upload_fileobj(data, bucket, 'dockerd')

# list contents of bucket
list_bucket_contents(bucket)

# Retrieve the list of existing buckets
list_buckets()

print('sleep 60 seconds, waiting for you to check out the bucket')
time.sleep(60)

# delete bucket
delete_bucket(bucket)

print('sleep 60 seconds, waiting for bucket to be deleted')
time.sleep(60)

# Retrieve the list of existing buckets
list_buckets()

exit()
