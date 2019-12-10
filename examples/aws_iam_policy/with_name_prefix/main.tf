module example_name_prefix {
  source = "../.."

  name_prefix = "example_name_prefix"

  statements = [{
    sid       = "ExampleS3List"
    actions   = ["s3:List*"]
    resources = ["*"]
  }]
}