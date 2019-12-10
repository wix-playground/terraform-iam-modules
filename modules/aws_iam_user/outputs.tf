output name {
  value       = data.aws_iam_user.this.user_name
  description = "Name of the newly-created IAM user. Returns empty string if create_iam_user is set to false."
}

output arn {
  value       = data.aws_iam_user.this.arn
  description = "ARN of the newly-created IAM user. Returns empty string if create_iam_user is set to false."
}

output unique_id {
  value       = data.aws_iam_user.this.user_id
  description = "Unique id of the newly-created IAM user. Returns empty string if create_iam_user is set to false."
}

output login_profile_key_fingerprint {
  value       = concat(aws_iam_user_login_profile.this.*.key_fingerprint, [""])[0]
  description = "The fingerprint of the PGP key used to encrypt the password."
}

output login_profile_encrypted_password {
  value       = concat(aws_iam_user_login_profile.this.*.encrypted_password, [""])[0]
  description = "The encrypted password, base64 encoded."
}

output iam_access_key_id {
  value       = concat(aws_iam_access_key.this.*.id, [""])[0]
  description = "The access key ID."
}

output iam_access_key_key_fingerprint {
  value       = concat(aws_iam_access_key.this.*.key_fingerprint, [""])[0]
  description = "The fingerprint of the PGP key used to encrypt the secret."
}

output iam_access_key_secret {
  value       = concat(aws_iam_access_key.this.*.secret, [""])[0]
  description = "The secret access key."
}

output iam_access_key_encrypted_secret {
  value       = concat(aws_iam_access_key.this.*.encrypted_secret, [""])[0]
  description = "The encrypted secret, base64 encoded."
}

output iam_access_key_ses_smtp_password {
  value       = concat(aws_iam_access_key.this.*.ses_smtp_password, [""])[0]
  description = "The secret access key converted into an SES SMTP password."
}

output inline_policy_id {
  value = concat(
    aws_iam_user_policy.this.*.id,
    [""]
  )[0]
  description = "The role inline policy ID, in the form of user_name:user_policy_name."
}

output inline_policy_name {
  value = concat(
    aws_iam_user_policy.this.*.name,
    [""]
  )[0]
  description = "The name of the inline policy."
}

output inline_policy_json {
  value = concat(
    aws_iam_user_policy.this.*.policy,
    [""]
  )[0]
  description = "The inline policy document attached to the user."
}

output ssh_key_public_key_id {
  value       = concat(aws_iam_user_ssh_key.this.*.ssh_public_key_id, [""])[0]
  description = " The unique identifier for the SSH public key."
}

output ssh_key_fingerprint {
  value       = concat(aws_iam_user_ssh_key.this.*.fingerprint, [""])[0]
  description = "The MD5 message digest of the SSH public key."
}