# IAM policy document only example
Configuration in this directory creates only IAM policy document using terraform `aws_iam_policy_document` data source. IAM policy is not created in this example.

This module configures a policy document that allows listing any s3 bucket.

## Usage
To run this example you have to set AWS-related environment variables, at least `AWS_PROFILE` and `AWS_DEFAULT_REGION`. After that you need to execute following commands:
```
$ terraform init
$ terraform plan
$ terraform apply
```
**Note:** this example does not create resources that may cost money as long as you store your state locally. However, if you use s3 as backend, run `terraform destroy` after you no longer need this policy document to not get billed for S3 storage

## Outputs
| Name | Description |
|------|-------------|
| iam_policy_arn | ARN of the newly-created IAM policy. |
| iam_policy_document | Contents of the IAM policy document. |

**Note:** `iam_policy_arn` output should be empty and included here only to show that this module does not create any resources, only generating IAM policy document.