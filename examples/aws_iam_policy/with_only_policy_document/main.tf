module example_only_policy_document {
  source = "../.."

  create_document_only = true

  statements = [{
    sid       = "ExampleS3List"
    actions   = ["s3:List*"]
    resources = ["*"]
  }]
}