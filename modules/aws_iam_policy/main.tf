data aws_iam_policy_document this {
  count = length(var.statements) != 0 ? 1 : 0

  version = var.configuration_version

  source_json   = var.source_json
  override_json = var.override_json

  dynamic "statement" {
    for_each = var.statements
    content {
      sid           = lookup(statement.value, "sid", statement.key + 1)
      effect        = lookup(statement.value, "effect", "Allow")
      actions       = lookup(statement.value, "actions", [])
      not_actions   = lookup(statement.value, "not_actions", [])
      resources     = lookup(statement.value, "resources", [])
      not_resources = lookup(statement.value, "not_resources", [])

      dynamic "condition" {
        for_each = lookup(statement.value, "conditions", [])
        content {
          test     = lookup(condition.value, "test", "StringLike")
          variable = condition.value.variable
          values   = condition.value.values
        }
      }

      dynamic "principals" {
        for_each = lookup(statement.value, "principals", [])
        content {
          type        = principals.value.type
          identifiers = principals.value.identifiers
        }
      }

      dynamic "not_principals" {
        for_each = lookup(statement.value, "not_principals", [])
        content {
          type        = not_principals.value.type
          identifiers = not_principals.value.identifiers
        }
      }
    }
  }
}

locals {
  template_rendered = var.template_file != "" ? templatefile(
    var.template_file, var.template_variables
  ) : ""

  file_contents = var.source_file != "" ? file(var.source_file) : ""

  policy_json = compact(concat(
    data.aws_iam_policy_document.this.*.json,
    list(var.heredoc_string),
    list(local.template_rendered),
    list(local.file_contents),
    ["{}"]
  ))[0]
}


resource "aws_iam_policy" "this" {
  count = ! var.create_document_only ? 1 : 0

  name        = var.name
  name_prefix = var.name_prefix

  path        = var.path
  description = var.description

  policy = local.policy_json
}