# Synopsis

Here are all the instructions to use this terraform script
## Prerequisites
### IAM user for terraform
First, you need to create the IAM user that terraform will use to create/update/delete resources
This is the policy that you will need to attach to this "terraform" user
```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": [
                "lambda:CreateFunction",
                "lambda:TagResource",
                "lambda:DeleteProvisionedConcurrencyConfig",
                "iam:CreateRole",
                "events:PutRule",
                "events:RemoveTargets",
                "events:ListTargetsByRule",
                "events:PutTargets",
                "events:DeleteRule",
                "events:ListTagsForResource",
                "events:DescribeRule",
                "iam:DetachRolePolicy",
                "iam:ListAttachedRolePolicies",
                "iam:DeletePolicy",
                "iam:ListAttachedRolePolicies",
                "iam:AttachRolePolicy",
                "iam:ListPolicyVersions",
                "iam:GetPolicyVersion",
                "iam:CreatePolicyVersion",
                "lambda:GetFunctionConfiguration",
                "lambda:EnableReplication",
                "lambda:ListProvisionedConcurrencyConfigs",
                "lambda:DisableReplication",
                "lambda:GetProvisionedConcurrencyConfig",
                "lambda:ListLayers",
                "lambda:ListLayerVersions",
                "lambda:DeleteFunction",
                "lambda:GetAlias",
                "lambda:ListCodeSigningConfigs",
                "lambda:UpdateFunctionEventInvokeConfig",
                "lambda:DeleteFunctionCodeSigningConfig",
                "iam:GetRole",
                "lambda:ListFunctions",
                "lambda:GetEventSourceMapping",
                "lambda:InvokeFunction",
                "lambda:ListAliases",
                "iam:DeleteRole",
                "iam:GetPolicy",
                "lambda:AddLayerVersionPermission",
                "lambda:GetFunctionCodeSigningConfig",
                "lambda:UpdateAlias",
                "lambda:UpdateFunctionCode",
                "lambda:ListFunctionEventInvokeConfigs",
                "lambda:ListFunctionsByCodeSigningConfig",
                "lambda:GetFunctionConcurrency",
                "lambda:PutProvisionedConcurrencyConfig",
                "lambda:ListEventSourceMappings",
                "lambda:PublishVersion",
                "lambda:DeleteEventSourceMapping",
                "lambda:CreateAlias",
                "lambda:ListVersionsByFunction",
                "lambda:GetLayerVersion",
                "lambda:PublishLayerVersion",
                "lambda:InvokeAsync",
                "lambda:GetAccountSettings",
                "lambda:CreateEventSourceMapping",
                "lambda:GetLayerVersionPolicy",
                "lambda:UntagResource",
                "lambda:RemoveLayerVersionPermission",
                "lambda:PutFunctionConcurrency",
                "lambda:DeleteCodeSigningConfig",
                "iam:ListInstanceProfilesForRole",
                "iam:PassRole",
                "lambda:ListTags",
                "lambda:DeleteLayerVersion",
                "lambda:PutFunctionEventInvokeConfig",
                "lambda:DeleteFunctionEventInvokeConfig",
                "lambda:CreateCodeSigningConfig",
                "lambda:PutFunctionCodeSigningConfig",
                "lambda:UpdateEventSourceMapping",
                "lambda:UpdateFunctionCodeSigningConfig",
                "lambda:GetFunction",
                "lambda:UpdateFunctionConfiguration",
                "lambda:UpdateCodeSigningConfig",
                "iam:CreatePolicy",
                "lambda:AddPermission",
                "lambda:GetFunctionEventInvokeConfig",
                "lambda:DeleteAlias",
                "lambda:DeleteFunctionConcurrency",
                "lambda:GetCodeSigningConfig",
                "lambda:RemovePermission",
                "lambda:GetPolicy"
            ],
            "Resource": "*"
        }
    ]
}
```
### AWS Credentials
Then, you need to configure the AWS credentials by running the following, you will need to provide the ACCESS_KEY and SECRET_KEY of the "terraform" user that you've just created
```
aws configure
```

### Update the AWS profile in terraform config
Finally, you need to update the terraform config to make it use the AWS profile you've just created.
To do that, you need to update the provider.profile field in the main.tf file.



## Use the terraform script
Here are the main command to use this terraform script
```
// Only for the before the first run
terraform init

// To preview the changes that are going to be applied 
terraform plan

// To effectively apply the changes
terraform apply
```

### Lamnda functions 
To update the lambda function, you need to zip the code before applying the terraform script
```
// First need to go to the lambda function folder
cd lambda/<LAMBDA_FUNCTION_NAME>

// Compressing the lambda function
zip <LAMBDA_FUNCTION_NAME>.zip -r *.py
```


