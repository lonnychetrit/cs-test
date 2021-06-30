from __future__ import print_function
from datetime import tzinfo, timedelta, datetime
import time
from boto3 import client
import boto3
import json
import os
import logging
import re
import pprint;
import string
import random


LOGLEVEL = os.getenv('LOG_LEVEL', 'ERROR').strip()
logger = logging.getLogger()
logger.setLevel(LOGLEVEL.upper())

class Tools():
    @staticmethod
    def generatePassword(snapshot, engine):
        """ Function that generates a password """
        symbols = ['*', '%', '£'] # Can add more
        password = ""
        for _ in range(9):
            password += random.choice(string.ascii_lowercase)
        password += random.choice(string.ascii_uppercase)
        password += random.choice(string.digits)
        password += random.choice(symbols)
        print(password)
        
    def get_snapshot_arn(snapshot, engine):
        if engine == "MYSQL":
            return snapshot["DBSnapshotArn"]
        elif engine == "AURORA":
            return snapshot["DBClusterSnapshotArn"]
        return False
        
        
    def copy_db_snapshot(rds,sourceSnapshotIdentifier, targetSnapshotIdentifier, tags, kms_key, engine):
        try:
            if engine == "MYSQL":
                rds.copy_db_snapshot(
                    SourceDBSnapshotIdentifier=sourceSnapshotIdentifier,
                    TargetDBSnapshotIdentifier=targetSnapshotIdentifier,
                    KmsKeyId = kms_key,
                    Tags = tags
                )
            elif engine == "AURORA":
                response = rds.copy_db_cluster_snapshot(
                    SourceDBClusterSnapshotIdentifier=sourceSnapshotIdentifier,
                    TargetDBClusterSnapshotIdentifier=targetSnapshotIdentifier,
                    KmsKeyId=kms_key,
                    # SourceRegion=REGION,
                    # CopyTags=True,
                    Tags = tags
                )
        except Exception as e:
            logger.error('Exception copying {} to {}: {}'.format(sourceSnapshotIdentifier, targetSnapshotIdentifier, e))
