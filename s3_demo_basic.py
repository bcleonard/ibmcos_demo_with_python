#!/usr/bin/python3

import argparse
import configparser
import sys
import time

from boto3 import client
from botocore.exceptions import ClientError

#
# source inspiration of script
# https://dev.to/nelsoncode/aws-s3-with-python-3bnn
#

#
# global variables
#
CONFIG_FILE = "demo_config.txt"


# parse cli
def parse_args(args):
    parser = argparse.ArgumentParser(description="conduct a very basic IBM "
                                     "COS s3 demo")
    parser.add_argument("-c", "--config",
                        help="Alternate configuration file",
                        required=False,
                        default="")
    return parser.parse_args(args)


#
# defined functions
#
def list_buckets(clientS3):
    try:
        response = clientS3.list_buckets()  # noqa
        print('Existing buckets:')
        for bucket in response['Buckets']:
            print(f'  {bucket["Name"]}')
        return "success"
    except ClientError as e:
        return e.response["Error"]


def create_bucket(clientS3, bucket: str):
    try:
        response = clientS3.create_bucket(Bucket=bucket)  # noqa
        return response
    except ClientError as e:
        return e.response["Error"]


def list_bucket_contents(clientS3, bucket: str):
    # print the contects of the bucket
    try:
        objects = clientS3.list_objects_v2(Bucket=bucket)  # noqa
        fileCount = objects['KeyCount']
        if fileCount == 0:
            print('bucket', bucket, 'is empty.')
        else:
            print('bucket', bucket, 'has ', fileCount, ' objects.')
            for obj in objects['Contents']:
                print(' object name: ', obj['Key'])
        return "success"
    except ClientError as e:
        return e.response["Error"]


def delete_file(clientS3, bucket: str, filename: str):
    try:
        response = clientS3.delete_object(Bucket=bucket, Key=filename)  # noqa
        return response
    except ClientError as e:
        return e.response["Error"]


def delete_bucket(clientS3, bucket: str):
    try:
        objects = clientS3.list_objects_v2(Bucket=bucket)  # noqa
        fileCount = objects['KeyCount']
        if fileCount == 0:
            print('bucket', bucket, 'is empty.')
        else:
            print('bucket', bucket, 'has ', fileCount, ' objects.')
            for obj in objects['Contents']:
                print(' deleting object: ', obj['Key'])
                delete_file(clientS3, bucket, obj['Key'])

        response = clientS3.delete_bucket(Bucket=bucket)  # noqa
        return response
    except ClientError as e:
        return e.response["Error"]


# define main function
def main():
    #
    # parse command line
    #
    argument = parse_args(sys.argv[1:])

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
    list_buckets(clientS3)

    # create bucket
    create_bucket(clientS3, bucket)

    # wait for bucket to be created
    print('sleep 60 seconds, waiting for bucket to be created')
    time.sleep(60)

    # Retrieve the list of existing buckets
    list_buckets(clientS3)

    # list contents of bucket
    list_bucket_contents(clientS3, bucket)

    # upload files
    with open('/usr/bin/dockerd', 'rb') as data:
        clientS3.upload_fileobj(data, bucket, 'dockerd')

    # list contents of bucket
    list_bucket_contents(clientS3, bucket)

    # Retrieve the list of existing buckets
    list_buckets(clientS3)

    print('sleep 60 seconds, waiting for you to check out the bucket')
    time.sleep(60)

    # delete bucket
    delete_bucket(clientS3, bucket)

    print('sleep 60 seconds, waiting for bucket to be deleted')
    time.sleep(60)

    # Retrieve the list of existing buckets
    list_buckets(clientS3)


# Execute main() function
if __name__ == '__main__':
    main()
