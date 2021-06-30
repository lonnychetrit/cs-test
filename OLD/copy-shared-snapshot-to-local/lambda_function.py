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


INSTANCES = {
      "prod-db-5-7-replica":   {
          "engine": "MYSQL",
          "region": "us-east-1",
          "kms_key": "34d55511-9290-4272-9f0c-c315d6e6aac1",
          "retention_period": 30
      },
    #   "integration-cluster":   {
    #       "engine": "AURORA",
    #       "region": "eu-central-1",
    #       "kms_key": "557c6ad1-4ab5-49eb-8fb2-7fce9895a2df",
    #       "share_with": "863187190921"
    #   }
    
}

LOGLEVEL = os.getenv('LOG_LEVEL', 'ERROR').strip()
logger = logging.getLogger()
logger.setLevel(LOGLEVEL.upper())

def create_manual_copy(rds, instance, kms_key, engine):
    print("Creating manual copy of the most recent shared snapshot of {}".format(instance))
    snapshots = RDS_TOOLS.get_snapshots(rds, instance, "shared", engine)
    latest = RDS_TOOLS.get_latest_snapshot(snapshots, engine)
    if latest == False:
        print("No snapshot to copy")
        return False
    latest_snapshot_identifier = RDS_TOOLS.get_snapshot_identifier(latest, engine)
    latest_snapshot_arn = RDS_TOOLS.get_snapshot_arn(latest, engine)
    newName = latest_snapshot_identifier.replace("encrypted-copy-", "dr-automated-")
    snapshot_exists = RDS_TOOLS.check_snapshot_exists(rds, instance, newName, 'manual', engine)
    if snapshot_exists:
        print("The snapshot {} already exists, no need to copy".format(newName))
        return False
    tags = [{
            'Key': 'Source',
            'Value': 'Lambda function: copy-shared-snapshot-to-local'
        }]
    
    RDS_TOOLS.copy_db_snapshot(rds,latest_snapshot_arn, newName, tags, kms_key, engine)
    print("Snapshot {} is being copied to {}".format(latest_snapshot_identifier, newName))
    return True


# Delete old snapshot
def delete_old_manuals(rds, instance, retention_period, engine):
    print("Deleting old manual snapshots for {}".format(instance))
    manuals = RDS_TOOLS.get_snapshots(rds, instance, 'manual', engine)
    sorted_manuals = sorted(manuals, key=RDS_TOOLS.get_snap_date)
    manuals_length = len(sorted_manuals)
    number_of_snapshot_to_remove = len(sorted_manuals) - retention_period
    if number_of_snapshot_to_remove > 0:
        for manual in sorted_manuals[0:number_of_snapshot_to_remove]:
            # Only check Failsafe manual snapshots
            snaphot_identifier = RDS_TOOLS.get_snapshot_identifier(manual, engine)
            if (snaphot_identifier[:13] != "dr-automated-"):
                print("Ignoring {}".format(snaphot_identifier))
                continue
            print("Deleting {}".format(snaphot_identifier))
            RDS_TOOLS.delete_snapshot(rds, snaphot_identifier, engine)
    else:
        print("There is no snapshot to remove!")

def lambda_handler(event, context):
    if len(INSTANCES) > 0:
        for instance_name, instance in INSTANCES.items():
            print("Working on {}".format(instance_name))
            if instance["engine"] == "MYSQL":
                rds = client("rds", region_name=instance["region"])
            elif instance["engine"] == "AURORA":
                rds = boto3.client('rds', region_name=instance["region"])
            copy_name = create_manual_copy(rds, instance_name, instance["kms_key"], instance["engine"])
            delete_old_manuals(rds, instance_name, instance["retention_period"], instance["engine"])
    else:
        print("No instance to treat")
    return True

    
