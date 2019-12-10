# IAM policy with complete statement example
Configuration in this directory creates IAM policy and IAM policy document using terraform `aws_iam_policy_document` data source.

This policy contains following set of rules:
* Straightfoward rule that allows listing any s3 bucket.
* Rule that denies every get-action on any s3 bucket if user has not assigned an MFA device
* Rule without sid, to check that by default it will be set to `rule.index + 1` does not allow describing log streams on `arn:aws:logs:*:*:no_resources` stream.

## Usage
To run this example you have to set AWS-related environment variables, at least `AWS_PROFILE` and `AWS_DEFAULT_REGION`. After that you need to execute following commands:
```
$ terraform init
$ terraform plan
$ terraform apply
```
**Note:** this example creates resources that may cost money. So, after you have no need in these resources, run `terraform destroy` to get rid of them.

## Outputs
| Name | Description |
|------|-------------|
| iam_policy_id | Id of the newly-created IAM policy. |
| iam_policy_arn | ARN of the newly-created IAM policy. |
| iam_policy_name | Name of the newly-created IAM policy. |
| iam_policy_path | Path of the newly-created IAM policy. |
| iam_policy_document | Contents of the IAM policy document. |