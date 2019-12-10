output iam_policy_id {
  value       = module.example_heredoc_policy.id
  description = "Id of the newly-created IAM policy."
}

output iam_policy_arn {
  value       = module.example_heredoc_policy.arn
  description = "ARN of the newly-created IAM policy."
}

output iam_policy_name {
  value       = module.example_heredoc_policy.name
  description = "Name of the newly-created IAM policy."
}

output iam_policy_path {
  value       = module.example_heredoc_policy.path
  description = "Path of the newly-created IAM policy."
}

output iam_policy_document {
  value       = module.example_heredoc_policy.json
  description = "Contents of the IAM policy document."
}
