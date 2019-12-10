module example_complete_statement {
  source = "../.."

  name = "example_complete_statement"

  statements = [{
    sid       = "ExampleS3List"
    actions   = ["s3:List*"]
    resources = ["*"]
    }, {
    sid         = "ExampleConditionAndNotActions"
    not_actions = ["s3:Get*"]
    conditions = [{
      test     = "BoolIfExists"
      variable = "aws:MultiFactorAuthPresent"
      values   = ["false"]
    }]
    resources = ["*"]
    }, {
    actions       = ["logs:DescribeLogStreams"]
    not_resources = ["arn:aws:logs:*:*:no_resources"]
  }]
}