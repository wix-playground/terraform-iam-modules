module example_heredoc_policy {
  source = "../../"

  name           = "example_heredoc_policy"
  heredoc_string = <<POLICY
{
    "Version": "2012-10-17",
    "Statement": [{
        "Sid": "ExampleS3List",
        "Effect": "Allow",
        "Action": "s3:List*",
        "Resource": [
            "*"
        ]
    }]
}
    POLICY
}
