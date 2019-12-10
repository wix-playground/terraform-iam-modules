module example_template_file {
  source = "../../"

  name          = "example_template_file"
  template_file = "${path.module}/iam_policy_document.tmpl"
  template_variables = {
    sid           = "ExampleS3List"
    action_list   = "[\"s3:List*\"]"
    resource_list = "[\"*\"]"
  }
}
