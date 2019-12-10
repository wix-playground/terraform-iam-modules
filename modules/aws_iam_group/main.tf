locals {
  create_inline_policy = (
    length(var.inline_policy_statements) != 0
    || var.inline_policy_template_file != ""
    || var.inline_policy_source_file != ""
    || var.inline_policy_heredoc_string != ""
  )
}

resource aws_iam_group this {
  count = var.create_iam_group ? 1 : 0

  name = var.name
  path = var.path
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

resource aws_iam_group_policy this {
  count = local.create_inline_policy ? 1 : 0

  name        = var.inline_policy_name
  name_prefix = var.inline_policy_name_prefix

  group  = var.name
  policy = module.inline_policy.json

  depends_on = [aws_iam_group.this]
}

resource aws_iam_group_policy_attachment this {
  count = length(var.attached_policy_arns)

  group      = var.name
  policy_arn = var.attached_policy_arns[count.index]

  depends_on = [aws_iam_group.this]
}