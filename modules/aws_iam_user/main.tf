locals {
  create_inline_policy = (
    length(var.inline_policy_statements) != 0
    || var.inline_policy_template_file != ""
    || var.inline_policy_source_file != ""
    || var.inline_policy_heredoc_string != ""
  )
}

resource aws_iam_user this {
  count = var.create_iam_user ? 1 : 0

  name                 = var.name
  path                 = var.path
  force_destroy        = var.force_destroy
  permissions_boundary = var.permissions_boundary

  tags = var.tags
}

resource aws_iam_user_login_profile this {
  count = var.create_iam_user && var.create_iam_user_login_profile && ! contains([null, ""], var.pgp_key) ? 1 : 0

  user                    = var.name
  pgp_key                 = var.pgp_key
  password_length         = var.password_length
  password_reset_required = var.password_reset_required

  depends_on = [aws_iam_user.this]
}

resource aws_iam_access_key this {
  count = var.create_iam_user && var.create_iam_access_key ? 1 : 0

  user    = var.name
  pgp_key = var.pgp_key
  status  = var.access_key_status

  depends_on = [aws_iam_user.this]
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

resource aws_iam_user_policy this {
  count = local.create_inline_policy ? 1 : 0

  name        = var.inline_policy_name
  name_prefix = var.inline_policy_name_prefix

  user   = var.name
  policy = module.inline_policy.json

  depends_on = [aws_iam_user.this]
}

resource aws_iam_user_policy_attachment this {
  count = length(var.attached_policy_arns)

  user       = var.name
  policy_arn = var.attached_policy_arns[count.index]

  depends_on = [aws_iam_user.this]
}

resource aws_iam_user_ssh_key this {
  count = var.create_iam_user && var.create_ssh_key && ! contains([null, ""], var.public_key) ? 1 : 0

  username   = var.name
  encoding   = var.encoding
  public_key = var.public_key
  status     = var.ssh_key_status

  depends_on = [aws_iam_user.this]
}

resource aws_iam_user_group_membership this {
  count = length(var.group_names) > 0 ? 1 : 0

  user   = var.name
  groups = var.group_names
  
  depends_on = [aws_iam_user.this]
}