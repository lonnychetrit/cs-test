terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 2.70"
    }
  }
}

provider "aws" {
  profile = "lonny-cs"
  region  = "eu-central-1"
}

resource "aws_iam_role" "role-for-lambda-copy-shared-snapshot-to-local" {
  name = "role-for-lambda-copy-shared-snapshot-to-local"

  assume_role_policy = <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
          "Action": "sts:AssumeRole",
          "Principal": {
           "Service": "lambda.amazonaws.com"
          },
          "Effect": "Allow",
          "Sid": ""
        }
    ]
}
EOF
}


resource "aws_iam_policy" "ManageRDSSnapshots-Prod-Us" {
  name        = "ManageRDSSnapshots-Prod-Us"
  path        = "/"
  description = "This policy is used by the Lambda function that is responsible to copy the shared snapshot to local to be able to recover from them in case of a disaster"

  policy = <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": "kms:*",
            "Resource": "*"
        },
        {
            "Effect": "Allow",
            "Action": [
                "rds:AddTagsToResource",
                "rds:DeleteDBClusterSnapshot",
                "rds:DescribeDBSnapshots",
                "rds:CopyDBSnapshot",
                "rds:CopyDBClusterSnapshot",
                "rds:DescribeDBClusterSnapshots",
                "rds:DeleteDBSnapshot",
                "rds:ModifyDBClusterSnapshotAttribute",
                "rds:ModifyDBSnapshotAttribute"
            ],
            "Resource": "*",
            "Condition": {
                "StringEquals": {
                    "aws:RequestedRegion": "us-east-1"
                }
            }
        }
    ]
}
EOF
}

resource "aws_iam_policy" "ManageRDSSnapshots-Int" {
  name        = "ManageRDSSnapshots-Int"
  path        = "/"
  description = "This policy is used by the Lambda function that is responsible to copy the shared snapshot to local to be able to recover from them in case of a disaster"

  policy = <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": "kms:*",
            "Resource": "*"
        },
        {
            "Effect": "Allow",
            "Action": [
                "rds:AddTagsToResource",
                "rds:DeleteDBClusterSnapshot",
                "rds:DescribeDBSnapshots",
                "rds:CopyDBSnapshot",
                "rds:CopyDBClusterSnapshot",
                "rds:DescribeDBClusterSnapshots",
                "rds:DeleteDBSnapshot",
                "rds:ModifyDBClusterSnapshotAttribute",
                "rds:ModifyDBSnapshotAttribute"
            ],
            "Resource": "*",
            "Condition": {
                "StringEquals": {
                    "aws:RequestedRegion": "eu-central-1"
                }
            }
        }
    ]
}
EOF
}

resource "aws_iam_policy" "Manage-Lambda-Logs" {
  name        = "Manage_Lambda_Logs"
  path        = "/"
  description = "This policy will be attached to Lambda function to be able to manage the logs"

  policy = <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": "logs:CreateLogGroup",
            "Resource": "*"
        },
        {
            "Effect": "Allow",
            "Action": [
                "logs:CreateLogStream",
                "logs:PutLogEvents"
            ],
            "Resource": "*"
        }
    ]
}
EOF
}

resource "aws_iam_role_policy_attachment" "ManageRDSSnapshots-Prod-Us_attachment" {
  role       = aws_iam_role.role-for-lambda-copy-shared-snapshot-to-local.name
  policy_arn = aws_iam_policy.ManageRDSSnapshots-Prod-Us.arn
}
resource "aws_iam_role_policy_attachment" "ManageRDSSnapshots-Int_attachment" {
  role       = aws_iam_role.role-for-lambda-copy-shared-snapshot-to-local.name
  policy_arn = aws_iam_policy.ManageRDSSnapshots-Int.arn
}

resource "aws_iam_role_policy_attachment" "Manage-Lambda-Logs-attachment" {
  role       = aws_iam_role.role-for-lambda-copy-shared-snapshot-to-local.name
  policy_arn = aws_iam_policy.Manage-Lambda-Logs.arn
}

resource "aws_lambda_function" "copy-shared-snapshot-to-local" {
  filename      = "lambda/copy-shared-snapshot-to-local/copy-shared-snapshot-to-local.zip"
  function_name = "copy-shared-snapshot-to-local"
  role          = aws_iam_role.role-for-lambda-copy-shared-snapshot-to-local.arn
  handler       = "lambda_function.lambda_handler"
  timeout       = 900
  source_code_hash = filebase64sha256("lambda/copy-shared-snapshot-to-local/copy-shared-snapshot-to-local.zip")
  runtime = "python3.8"
}

resource "aws_cloudwatch_event_rule" "every-twelve-hours" {
  name                = "every-twelve-hours"
  description         = "Fires every twelve hours"
  schedule_expression = "rate(12 hours)"
}

resource "aws_cloudwatch_event_target" "copy-shared-snapshot-to-local-every-twelve-hours" {
  rule      = aws_cloudwatch_event_rule.every-twelve-hours.name
  target_id = "copy-shared-snapshot-to-local"
  arn       = aws_lambda_function.copy-shared-snapshot-to-local.arn
}

resource "aws_lambda_permission" "allow-cloudwatch-to-call-copy-shared-snapshot-to-local" {
  statement_id  = "AllowExecutionFromCloudWatch"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.copy-shared-snapshot-to-local.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.every-twelve-hours.arn
}

resource "aws_db_parameter_group" "prod-mysql-5-6" {
  name   = "prod-mysql-5-6"
  family = "mysql5.6"
  parameter {
    name  = "character_set_client"
    value = "utf8"
    apply_method = "immediate"
  }
  parameter {
    name  = "character_set_connection"
    value = "utf8"
    apply_method = "immediate"
  }
  parameter {
    name  = "character_set_database"
    value = "utf8"
    apply_method = "immediate"
  }
  parameter {
    name  = "character_set_filesystem"
    value = "binary"
    apply_method = "immediate"
  }
  parameter {
    name  = "character_set_results"
    value = "utf8"
    apply_method = "immediate"
  }
  parameter {
    name  = "character_set_server"
    value = "utf8"
    apply_method = "immediate"
  }
  parameter {
    name  = "collation_connection"
    value = "utf8_general_ci"
    apply_method = "immediate"
  }
  parameter {
    name  = "collation_server"
    value = "utf8_general_ci"
    apply_method = "immediate"
  }
  parameter {
    name  = "innodb_buffer_pool_dump_at_shutdown"
    value = "1"
    apply_method = "immediate"
  }
  parameter {
    name  = "innodb_buffer_pool_load_at_startup"
    value = "1"
    apply_method = "pending-reboot"
  }
  parameter {
    name  = "innodb_flush_log_at_trx_commit"
    value = "1"
    apply_method = "immediate"
  }
  parameter {
    name  = "innodb_support_xa"
    value = "1"
    apply_method = "immediate"
  }
  parameter {
    name  = "log_bin_trust_function_creators"
    value = "1"
    apply_method = "immediate"
  }
  parameter {
    name  = "log_output"
    value = "FILE"
    apply_method = "immediate"
  }
  parameter {
    name  = "log_queries_not_using_indexes"
    value = "1"
    apply_method = "immediate"
  }
  parameter {
    name  = "long_query_time"
    value = "15"
    apply_method = "immediate"
  }
  parameter {
    name  = "slow_query_log"
    value = "1"
    apply_method = "immediate"
  }
}

