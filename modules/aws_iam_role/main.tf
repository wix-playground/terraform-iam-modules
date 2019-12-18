locals {
  session_duration_seconds = var.session_duration_hours * 3600
  create_inline_policy = (
    length(var.inline_policy_statements) != 0
    || var.inline_policy_template_file != ""
    || var.inline_policy_source_file != ""
    || var.inline_policy_heredoc_string != ""
  )
}

module assume_role_policy {
  source = "../aws_iam_policy"

  create_document_only = true
  statements = [{
    actions    = ["sts:AssumeRole"]
    principals = var.assume_role_principals
  }]
}

resource aws_iam_role this {
  count = var.create_iam_role ? 1 : 0

  name        = var.name
  name_prefix = var.name_prefix

  path                 = var.path
  description          = var.description
  max_session_duration = local.session_duration_seconds

  assume_role_policy    = module.assume_role_policy.json
  force_detach_policies = var.force_detach_policies

  permissions_boundary = var.permissions_boundary

  tags = var.tags
}

module inline_policy {
  source = "../aws_iam_policy"

  create_document_only = true
  statements           = var.inline_policy_statements
  template_file        = var.inline_policy_template_file
  template_variables   = var.inline_policy_template_variables
  source_file          = var.inline_policy_source_file
  heredoc_string       = var.inline_policy_heredoc_string
}

resource aws_iam_role_policy this {
  count = local.create_inline_policy ? 1 : 0

  name        = var.inline_policy_name
  name_prefix = var.inline_policy_name_prefix

  role   = data.aws_iam_role.this.id
  policy = module.inline_policy.json
}

resource aws_iam_role_policy_attachment this {
  count = length(var.attached_policy_arns)

  role       = data.aws_iam_role.this.name
  policy_arn = var.attached_policy_arns[count.index]
}

resource aws_iam_instance_profile this {
  count = var.create_instance_profile ? 1 : 0

  name        = var.instance_profile_name
  name_prefix = var.instance_profile_name_prefix

  path = var.instance_profile_path

  role = data.aws_iam_role.this.name
}