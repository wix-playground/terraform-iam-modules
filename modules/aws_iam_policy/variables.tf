variable create_document_only {
  type        = bool
  default     = false
  description = "Indicates whether this module should create IAM policy or IAM policy document only."
}

variable name {
  type        = string
  default     = null
  description = "IAM policy name. Incompatible with name_prefix variable."
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

variable heredoc_string {
  type        = string
  default     = ""
  description = "(Optional) Multiline (or single line with escaped double-quotes) content of the IAM policy document."
}

variable configuration_version {
  type        = string
  default     = "2012-10-17"
  description = "(Optional) IAM policy document version. Valid values: 2008-10-17, 2012-10-17."
}

variable source_json {
  type        = string
  default     = null
  description = "(Optional) An IAM policy document to import as a base for the current policy document."
}

variable override_json {
  type        = string
  default     = null
  description = "(Optional) An IAM policy document to import and override the current policy document."
}

variable statements {
  default     = []
  description = "(Optional) Array of statements, that comprise IAM policy content. Feeds directly into aws_iam_policy_document data source"
}

variable source_file {
  type        = string
  default     = ""
  description = "(Optional) Path to file that contains the complete IAM policy document."
}

variable template_file {
  type        = string
  default     = ""
  description = "(Optional) Path to file that contains the template for IAM policy document."
}

variable template_variables {
  type        = map
  default     = {}
  description = "(Optional) Map of variables template_file needs to render IAM policy document."
}