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


LOGLEVEL = os.getenv('LOG_LEVEL', 'ERROR').strip()
logger = logging.getLogger()
logger.setLevel(LOGLEVEL.upper())

class RDS_TOOLS():
    @staticmethod
    def get_snapshot_identifier(snapshot, engine):
        if engine == "MYSQL":
            return snapshot["DBSnapshotIdentifier"].split(":")[-1]
        elif engine == "AURORA":
            return snapshot["DBClusterSnapshotIdentifier"].split(":")[-1]
        return False
        
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

            
    # Delete the snapshot passed in param
    def delete_snapshot(rds, snapshot_identifier, engine):
        try:
            print("Sharing {}".format(snapshot_identifier))
            if engine == "MYSQL":
                print("MYSQL")
                rds.delete_db_snapshot(
                    DBSnapshotIdentifier=snapshot_identifier
                )
            elif engine == "AURORA":
                print("AURORA")
                rds.delete_db_cluster_snapshot(
                    DBClusterSnapshotIdentifier=snapshot_identifier
                )
        except Exception as e:
            logger.error('Exception deleting {}: {}'.format(snapshot_identifier, e))
            
            
    
    # Share snapshot with dest_account
    def share_snapshot(rds, snapshot_identifier, aws_account_id_to_share_with, engine):
        try:
            print("Sharing {}".format(snapshot_identifier))
            if engine == "MYSQL":
                rds.modify_db_snapshot_attribute(
                    DBSnapshotIdentifier=snapshot_identifier,
                    AttributeName='restore',
                    ValuesToAdd=[
                        aws_account_id_to_share_with
                    ]
                )
            elif engine == "AURORA":
                response_modify = rds.modify_db_cluster_snapshot_attribute(
                    DBClusterSnapshotIdentifier=snapshot_identifier,
                    AttributeName='restore',
                    ValuesToAdd=[
                        aws_account_id_to_share_with
                    ]
                )
        except Exception as e:
            logger.error('Exception sharing {}: {}'.format(snapshot_identifier, e))
            
    def check_snapshot_exists(rds, instance, snapshot_name, snapshot_type, engine):
        snapshots = RDS_TOOLS.get_snapshots(rds, instance, snapshot_type, engine)
        for snapshot in snapshots:
            snaphot_identifier = RDS_TOOLS.get_snapshot_identifier(snapshot, engine)
            if snaphot_identifier == snapshot_name:
                return snapshot
        return False

    def wait_until_available(rds, instance, snapshot_name, snapshot_type, engine):
        print("Waiting for copy of {} to complete.".format(snapshot_name))
        available = False
        while not available:
            time.sleep(10)
            snapshots = RDS_TOOLS.get_snapshots(rds, instance, snapshot_type, engine)
            for snapshot in snapshots:
                snapshot_identifier = RDS_TOOLS.get_snapshot_identifier(snapshot, engine)
                if snapshot_identifier == snapshot_name:
                    if snapshot['Status'] == "available":
                        available = True
                        break


    # Get latest snapshot
    def get_latest_snapshot(snapshots, engine):
        newest = False
        latest_snapshot = {}
        for snapshot in snapshots:
            snapshots = sorted(snapshots, key=RDS_TOOLS.get_snap_date)
            newest = snapshots[-1]
        return newest

                
    def get_snap_date(snap):
        # If snapshot is still being created it doesn't have a SnapshotCreateTime
        if snap['Status'] != "available":
            return datetime.now()
        else:
            return snap['SnapshotCreateTime']

    def get_snapshots(rds, instance, snap_type, engine):
        response = []
        if engine == "MYSQL":
            snapshots = rds.describe_db_snapshots(
                        SnapshotType=snap_type,
                        IncludeShared=True)['DBSnapshots']
        elif engine == "AURORA":
            snapshots = rds.describe_db_cluster_snapshots(
                        SnapshotType=snap_type,
                        IncludeShared=True)['DBClusterSnapshots']
        for snapshot in snapshots:
            if ("DBInstanceIdentifier" in snapshot and snapshot["DBInstanceIdentifier"] == instance) or ("DBClusterIdentifier" in snapshot and snapshot["DBClusterIdentifier"] == instance):
                response.append(snapshot)
        return response

