output "id" {
  value = concat(
    aws_iam_policy.this.*.id,
    [""]
  )[0]
  description = "Id of the newly-created IAM policy. Returns empty string if create_document_only is set to true."
}

output "arn" {
  value = concat(
    aws_iam_policy.this.*.arn,
    [""]
  )[0]
  description = "ARN of the newly-created IAM policy. Returns empty string if create_document_only is set to true."
}

output "name" {
  value = concat(
    aws_iam_policy.this.*.name,
    [""]
  )[0]
  description = "Name of the newly-created IAM policy. Returns empty string if create_document_only is set to true."
}

output "path" {
  value = concat(
    aws_iam_policy.this.*.path,
    [""]
  )[0]
  description = "Path of the newly-created IAM policy. Returns empty string if create_document_only is set to true."
}


output json {
  value       = local.policy_json
  description = "Contents of the IAM policy document."
}
