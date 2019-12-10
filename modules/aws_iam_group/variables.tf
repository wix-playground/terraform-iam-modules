variable create_iam_group {
  type        = bool
  default     = true
  description = "Determines whether terraform should create a new IAM group or work with the existing one instead."
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