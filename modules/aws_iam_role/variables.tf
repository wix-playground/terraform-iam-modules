variable create_iam_role {
  type        = bool
  default     = true
  description = "Determines whether terraform should create a new IAM role or work with the existing one instead."
}

variable name {
  type        = string
  default     = null
  description = "(Optional) IAM policy name. Incompatible with name_prefix variable."
}

variable name_prefix {
  type        = string
  default     = null
  description = "(Optional) Creates a unique name beginning with the specified prefix."
}

variable path {
  type        = string
  default     = "/"
  description = "(Optional) Path in which to create the policy."
}

variable description {
  type        = string
  default     = ""
  description = "(Optional) Description of the IAM policy."
}

variable permissions_boundary {
  type        = string
  default     = ""
  description = "(Optional) The ARN of the policy that is used to set the permissions boundary for the role."
}

variable force_detach_policies {
  type        = bool
  default     = false
  description = "(Optional) Specifies to force detaching any policies the role has before destroying it."
}

variable session_duration_hours {
  type        = number
  default     = 1
  description = "(Optional) The maximum session duration in hours that you want to set for the specified role."
}

variable attached_policy_arns {
  type        = list(string)
  default     = []
  description = "(Optional) List of IAM policy ARNs to attach to this role"
}

variable tags {
  type        = map
  default     = {}
  description = "(Optional) Key-value mapping of tags for the IAM role."
}

variable assume_role_principals {
  type = list(object({
    type        = string
    identifiers = list(string)
  }))
  default     = []
  description = "A list of principal objects that could assume this IAM role."
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

variable create_instance_profile {
  type        = bool
  default     = false
  description = "If set to true, terraform will use create an AWS instance profile based of that role."
}

variable instance_profile_name {
  type        = string
  default     = null
  description = "(Optional) IAM instance profile name. Incompatible with name_prefix variable."
}

variable instance_profile_name_prefix {
  type        = string
  default     = null
  description = "(Optional) Creates a unique name for the instance profile beginning with the specified prefix."
}

variable instance_profile_path {
  type        = string
  default     = "/"
  description = "(Optional) Path in which to create the instance profile."
}