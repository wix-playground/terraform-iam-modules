output id {
  value = concat(
    aws_iam_role.this.*.id,
    [""]
  )[0]
  description = "Id of the newly-created IAM role."
}

output unique_id {
  value = concat(
    aws_iam_role.this.*.unique_id,
    [""]
  )[0]
  description = "Unique id of the newly-created IAM role."
}

output arn {
  value = concat(
    aws_iam_role.this.*.arn,
    [""]
  )[0]
  description = "ARN of the newly-created IAM role."
}

output name {
  value = concat(
    aws_iam_role.this.*.name,
    [""]
  )[0]
  description = "Name of the newly-created IAM role."
}

output inline_policy_id {
  value = concat(
    aws_iam_role_policy.this.*.id,
    [""]
  )[0]
  description = "The role inline policy ID, in the form of role_name:role_policy_name."
}

output inline_policy_name {
  value = concat(
    aws_iam_role_policy.this.*.name,
    [""]
  )[0]
  description = "The name of the inline policy."
}

output inline_policy_json {
  value = concat(
    aws_iam_role_policy.this.*.policy,
    [""]
  )[0]
  description = "The inline policy document attached to the role."
}