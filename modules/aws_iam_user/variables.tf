variable create_iam_user {
  type        = bool
  default     = true
  description = "Determines whether terraform should create a new IAM user or work with the existing one instead."
}

variable name {
  type        = string
  description = "Trhe users's name. Case-insensetive."
}

variable path {
  type        = string
  default     = "/"
  description = "(Optional) Path in which to create the user."
}

variable force_destroy {
  type        = bool
  default     = false
  description = "(Optional) When destroying this user, destroy even if it has non-Terraform-managed IAM access keys, login profile or MFA devices."
}

variable permissions_boundary {
  type        = string
  default     = ""
  description = " (Optional) The ARN of the policy that is used to set the permissions boundary for the user."
}

variable tags {
  type        = map
  default     = {}
  description = "Key-value mapping of tags for the IAM user."
}

variable create_iam_user_login_profile {
  type        = bool
  default     = false
  description = "This variable decides if user's login profile should be created alongside with the user."
}

variable pgp_key {
  type        = string
  default     = ""
  description = "Either a base-64 encoded PGP public key, or a keybase username in the form keybase:username."
}

variable password_length {
  type        = number
  default     = 20
  description = "(Optional) The length of the generated password on resource creation."
}

variable password_reset_required {
  type        = bool
  default     = true
  description = "(Optional) Whether the user should be forced to reset the generated password on resource creation."
}

variable create_iam_access_key {
  type        = bool
  default     = false
  description = "If set to true, will create AWS IAM access key after user creation is complete"
}

variable access_key_status {
  type        = string
  default     = "Active"
  description = "The access key status to apply. Can be either Active or Inactive."
}

variable create_ssh_key {
  type        = bool
  default     = false
  description = "Regulates whether ssh key for user should be set up after user's creation is complete."
}

variable encoding {
  type        = string
  default     = "SSH"
  description = "Specifies the public key encoding format to use in the response. Can be either SSH or PEM."
}

variable public_key {
  type        = string
  default     = ""
  description = "The SSH public key. The public key must be encoded in either ssh-rsa or PEM format."
}

variable ssh_key_status {
  type        = string
  default     = "active"
  description = "(Optional) The status to assign to the SSH public key."
}

variable attached_policy_arns {
  type        = list(string)
  default     = []
  description = "(Optional) List of IAM policy ARNs to attach to this role"
}

variable inline_policy_name {
  type        = string
  default     = null
  description = "(Optional) IAM policy name. Incompatible with name_prefix variable."
}

variable inline_policy_name_prefix {
  type        = string
  default     = null
  description = "(Optional) Creates a unique name beginning with the specified prefix."
}

variable inline_policy_heredoc_string {
  type        = string
  default     = ""
  description = "(Optional) Multiline (or single line with escaped double-quotes) content of the IAM policy document."
}

variable inline_policy_statements {
  default     = []
  description = "(Optional) Array of statements, that comprise IAM policy content. Feeds directly into aws_iam_policy_document data source"
}

variable inline_policy_source_file {
  type        = string
  default     = ""
  description = "(Optional) Path to file that contains the complete IAM policy document."
}

variable inline_policy_template_file {
  type        = string
  default     = ""
  description = "(Optional) Path to file that contains the template for IAM policy document."
}

variable inline_policy_template_variables {
  type        = map
  default     = {}
  description = "(Optional) Map of variables template_file needs to render IAM policy document."
}

variable group_names {
  type        = list(string)
  default     = []
  description = "(Optional) List of IAM group names that user should be a member of"
}