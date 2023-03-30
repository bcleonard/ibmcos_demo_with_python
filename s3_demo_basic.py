#!/usr/bin/python3

import argparse
import configparser
import os
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
    parser.add_argument("-p", "--pause",
                        help="Pause during the demo instead of waiting for "
                        "60 seconds",
                        required=False,
                        action="store_true",
                        default="")
    return parser.parse_args(args)


#
# defined functions
#
def list_buckets(clientS3):
    try:
        response = clientS3.list_buckets()  # noqa
        print('List of existing buckets:')
        for bucket in response['Buckets']:
            print(f'  {bucket["Name"]}')

        print("\n")
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
            print('\nBucket', bucket, 'is empty.')
        else:
            print('\nBucket', bucket, 'has ', fileCount, ' objects.')
            for obj in objects['Contents']:
                print('  object name: ', obj['Key'])
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
            print('Bucket', bucket, 'is empty.')
        else:
            print('Bucket', bucket, 'has ', fileCount, ' objects.')
            for obj in objects['Contents']:
                print('  Deleting object: ', obj['Key'])
                delete_file(clientS3, bucket, obj['Key'])

            print("\n")

        print('Deleting bucket: ', bucket)
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
    filename = config['s3_demo_basic']['file']

    print("\ns3_demo_basic Configuration:")
    print("         Access Key: ", access_key)
    print("  Secret Access Key: ", secret_access_key)
    print("       Accesser URL: ", accesser)
    print("             Bucket: ", bucket)
    print("           Filename: ", filename)
    print("")

    #
    # run demo
    #

    # create connection
    clientS3 = client("s3",
                      aws_access_key_id=access_key,
                      aws_secret_access_key=secret_access_key,
                      endpoint_url=accesser)

    print("\nThere are three (3) parts to the demo.\n")
    print("\nPART 1:  This part of the demo will create a bucket.")
    print("It will list existing buckets, create the bucket, and list "
          "the existing buckets again.\n")

    # retrieve the list of existing buckets
    list_buckets(clientS3)

    # create bucket
    print("Creating bucket:     ", bucket)
    create_bucket(clientS3, bucket)
    time.sleep(1)
    print("")

    # Retrieve the list of existing buckets
    list_buckets(clientS3)

    if argument.pause:
        input("\nPress enter to continue...")
    else:
        print("\nWaiting for 60 seconds for you to check the GUI for the "
              "existence of the bucket.\n")
        time.sleep(60)

    print("\nPART 2:  This part of the demo will upload a file to the newly "
          "created bucket.")
    print("It will list the contents of the bucket, upload an object, and "
          "then list the contents of the bucket again.\n")

    # list contents of bucket
    list_bucket_contents(clientS3, bucket)
    print("")

    # upload files
    print("Uploading file to bucket:     ", bucket)
    with open(filename, 'rb') as data:
        clientS3.upload_fileobj(data, bucket, os.path.basename(filename))

    # list contents of bucket
    list_bucket_contents(clientS3, bucket)

    if argument.pause:
        input("\nPress enter to continue...")
    else:
        print("\nWaiting for 60 seconds for you to check the bucket for "
              "for the existence of the newly uploaded object.\n")
        time.sleep(60)

    print("\nPART 3:  This part of the demo will delete a bucket.")
    print("It will list existing buckets, list the contents of the bucket, "
          "delete the bucket, and list the existing buckets again.\n")

    # Retrieve the list of existing buckets
    list_buckets(clientS3)

    # delete bucket
    delete_bucket(clientS3, bucket)
    print("")

    # Retrieve the list of existing buckets
    list_buckets(clientS3)


# Execute main() function
if __name__ == '__main__':
    main()
