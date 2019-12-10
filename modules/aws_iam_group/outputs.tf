output id {
  value       = concat(aws_iam_group.this.*.id, [""])[0]
  description = "Id of the newly-created IAM group. Returns empty if create_iam_group is set to false."
}

output unique_id {
  value       = concat(aws_iam_group.this.*.unique_id, [""])[0]
  description = "Unique id of the newly-created IAM group. Returns empty if create_iam_group is set to false."
}

output arn {
  value       = concat(aws_iam_group.this.*.arn, [""])[0]
  description = "ARN of the newly-created IAM group. Returns empty if create_iam_group is set to false."
}

output name {
  value       = concat(aws_iam_group.this.*.name, [""])[0]
  description = "Name of the newly-created IAM group. Returns empty if create_iam_group is set to false."
}

output path {
  value       = concat(aws_iam_group.this.*.path, [""])[0]
  description = "Name of the newly-created IAM group. Returns empty if create_iam_group is set to false."
}

output inline_policy_id {
  value = concat(
    aws_iam_group_policy.this.*.id,
    [""]
  )[0]
  description = "The group inline policy ID, in the form of group_name:group_policy_name."
}

output inline_policy_name {
  value = concat(
    aws_iam_group_policy.this.*.name,
    [""]
  )[0]
  description = "The name of the inline policy."
}

output inline_policy_json {
  value = concat(
    aws_iam_group_policy.this.*.policy,
    [""]
  )[0]
  description = "The inline policy document attached to the group."
}
