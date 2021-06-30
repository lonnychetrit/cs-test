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
from rds_tools import *

# List of database identifiers
INSTANCES = {
      "prod-db-5-7-replica":   {
          "engine": "MYSQL",
          "region": "us-east-1",
          "kms_key": "arn:aws:kms:us-east-1:184806450101:key/a7bc183a-0452-4a84-873e-dd2a7e7f16e8",
          "share_with": "863187190921"
      },
    #   "integration-cluster":   {
    #       "engine": "AURORA",
    #       "region": "eu-central-1",
    #       "kms_key": "arn:aws:kms:eu-central-1:184806450101:key/3cf56829-8f3e-4232-b7f4-5cb6c341be84",
    #       "share_with": "863187190921"
    #   }
}


LOGLEVEL = os.getenv('LOG_LEVEL', 'ERROR').strip()
logger = logging.getLogger()
logger.setLevel(LOGLEVEL.upper())

def create_manual_copy(rds, instance, engine, kms_key):
    print("Creating manual copy of the most recent auto snapshot of {}".format(instance))
    autos = RDS_TOOLS.get_snapshots(rds, instance, 'automated', engine)
    newest = RDS_TOOLS.get_latest_snapshot(autos, engine)
    newestName = newest['DBSnapshotIdentifier'][4:]
    encryptedCopyName = "encrypted-copy-"+newestName
    snapshot_exists = RDS_TOOLS.check_snapshot_exists(rds, instance, encryptedCopyName, 'manual', engine)
    if snapshot_exists:
        # The snapshot already exists, now let's check if the snapshot is available
        if snapshot_exists["Status"] == "available":
            print("The snapshot {} already exists, we are going to share it".format(encryptedCopyName))
            return encryptedCopyName
        else:
            # Returning False because we can't share it for the moment
            return False
    tags = [{
            'Key': 'Source',
            'Value': 'Lambda function: share-rds-snapshots-with-dr-account'
        }]
    
    RDS_TOOLS.copy_db_snapshot(rds,newest['DBSnapshotIdentifier'], encryptedCopyName, tags, kms_key, engine)
    # we don't want to wait because it can take multiple hours for our production db, instead, we are triggering the copy 
    # and the next invokation of this Lambda function will share the copied snapshot with the DR aws acount
    ## RDS_TOOLS.wait_until_available(rds, instance, encryptedCopyName, 'manual', engine)
    print("Snapshot {} is being copied to {}".format(newestName, encryptedCopyName))
    return False


# Delete all manual copies that have been shared with our DR aws account except the last one
def delete_old_manuals(rds, instance, engine):
    print("Deleting old manual snapshots for {}".format(instance))
    manuals = RDS_TOOLS.get_snapshots(rds, instance, 'manual', engine)
    autos = RDS_TOOLS.get_snapshots(rds, instance, 'automated', engine)
    latest_snapshot = RDS_TOOLS.get_latest_snapshot(autos, engine)
    latest_snapshot_identifier = latest_snapshot['DBSnapshotIdentifier'][4:]
    latest_snapshot_identifier = "encrypted-copy-"+latest_snapshot_identifier
    for manual in manuals:
        snaphot_identifier = RDS_TOOLS.get_snapshot_identifier(manual, engine)
        # Only check for "encrypted-copy*" manual snapshots
        if (snaphot_identifier[:14] != "encrypted-copy") or (snaphot_identifier[:14] == "encrypted-copy" and snaphot_identifier == latest_snapshot_identifier):
            print("Ignoring {}".format(snaphot_identifier))
            continue
        print("Deleting {}".format(snaphot_identifier))
        RDS_TOOLS.delete_snapshot(rds, snaphot_identifier, engine)


def lambda_handler(event, context):
    if len(INSTANCES) > 0:
        for instance_name, instance in INSTANCES.items():
            print("Working on {}".format(instance_name))
            if instance["engine"] == "MYSQL":
                rds = client("rds", region_name=instance["region"])
            elif instance["engine"] == "AURORA":
                rds = boto3.client('rds', region_name=instance["region"])
            copy_name = create_manual_copy(rds, instance_name, instance["engine"], instance["kms_key"])
            if copy_name:
                RDS_TOOLS.share_snapshot(rds, copy_name, instance["share_with"], instance["engine"])
                delete_old_manuals(rds, instance_name, instance["engine"])
    else:
        print("No instances to copy")
    return True
