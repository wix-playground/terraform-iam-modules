module example_without_name {
  source = "../.."

  statements = [{
    sid       = "ExampleS3List"
    actions   = ["s3:List*"]
    resources = ["*"]
  }]
}