output iam_policy_arn {
  value       = module.example_only_policy_document.arn
  description = "ARN of the newly-created IAM policy."
}

output iam_policy_document {
  value       = module.example_only_policy_document.json
  description = "Contents of the IAM policy document."
}
