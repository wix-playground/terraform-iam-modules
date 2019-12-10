module example_file_source {
  source = "../../"

  name        = "example_file_source"
  source_file = "${path.module}/iam_policy_document.json"
}
