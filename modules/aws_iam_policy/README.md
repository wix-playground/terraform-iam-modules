# AWS IAM Policy

This terraform module does two things:
* Created AWS IAM policy document using one of the ways that are allowed by terraform.
* Creates AWS IAM policy using policy document generated earlier.

## Policy document generation
This module can generate IAM policy document in the following ways:
* Using single line with escaped double quotes or a multiline string. This string should be passed to `heredoc_string` variable.
* Using file that contains a complete policy document json. If you want to use this approach, please pont the variable `source_file` to the location of your policy-file.
* By rendering terraform template using `templatefile` function. To do that, you'll have to point `template_file` variable to the location of your file that contains policy document template and populate `template_variables` var parameters that are required to render the said template.
* Last, but not least, using Terraform's `aws_iam_policy_document` data source. In that case, you will have to create an array of statement objecst, structure of which will be explained below.

### Statement object structure
The statement object, used to create IAM policy document has the following structure:
```hcl
{
    sid = "A short description of your statement. Defaults to (it's index in array + 1)"
    effect = "Effect, your statement will have. Can be Allow or Deny. Defaults to Allow."
    actions = "An array of AWS actions that are allowed or denied by that statement. Defaults to an empty array"
    not_actions = "A list of actions that this statement does not apply to. Defaults to an empty array"
    resources = "A list of resource ARNs that this statement applies to. Defaults to an empty array"
    not_resources = "A list of resource ARNs that this statement does not apply to. Defaults to an empty array"

    condition { 
        // dynamic block of configuration that is omitted entirely, if not explicitly set
        test = "The name of the IAM condition operator</a> to evaluate. Defaults to 'StringLike'"
        variable = "The name of a Context Variable to apply the condition to."
        values = "List of values to evaluate the condition against."
    }

    principals/not_principals {
        // dynamic block of configuration that is omitted entirely, if not explicitly set
        type = "The type of principal. For AWS ARNs this is 'AWS'. For AWS services (e.g. Lambda), this is 'Service'." 
        identifiers = "List of identifiers for principals. Can be either ARN's if type is AWS or service role names otherwise"
    }
}
```
List of IAM condition operators can be found [here](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_elements_condition_operators.html). 

**NOTE:** If you pay close attention to statements variable type, you'll see that it is not set. It was done because terraform doesn't allow element of a list type to have different types. Which would not allow us to declate statements with dynamic structure.

### Using this module to only generate IAM policy document
This module can be also used to just generate AWS IAM policy document. In order to do that, just set `create_document_only` variable to `true` and enjoy. 
You will be able to get IAM policy document json in `<MODULE_NAME>.json` output, which can be useful for things like inline policies. 

## Examples
* [IAM policy with a complex statement](https://github.com/vladyslav-tripatkhi/terraform-iam-policy/tree/master/examples/with_complete_statement) using `aws_iam_policy_document` data source.
* [IAM policy that uses file as a source for IAM policy document configuration](https://github.com/vladyslav-tripatkhi/terraform-iam-policy/tree/master/examples/with_file_source).
* [IAM policy that reads document parameters from input multiline string](https://github.com/vladyslav-tripatkhi/terraform-iam-policy/tree/master/examples/with_heredoc_string).
* [IAM policy with name prefix](https://github.com/vladyslav-tripatkhi/terraform-iam-policy/tree/master/examples/with_name_prefix) to create unique names and uses `aws_iam_policy_document` data source for policy configuration.
* [IAM policy document](https://github.com/vladyslav-tripatkhi/terraform-iam-policy/tree/master/examples/with_only_policy_document) that uses `aws_iam_policy_document` for configuration but does not create AWS IAM policy.
* [IAM policy that renders template file for configuring it's permissions](https://github.com/vladyslav-tripatkhi/terraform-iam-policy/tree/master/examples/with_template_file).
* [IAM policy with random unique name](https://github.com/vladyslav-tripatkhi/terraform-iam-policy/tree/master/examples/with_random_name) which is achieved by leaving both `name` and `name_prefix` variables empty.

## Importing
In order to simplify importing existing AWS resources compatible with this module into terraform state, tere is a small helper script located at `import_script/import.py`.
It has a detailed help section, which can be accessed by executing this script with `--help` flag. A quick example on script's usage can be found right below:
```
python3 ./import_script/import.py --policy-name test-policy
```
This example will generate both import statement for terraform as well as HCL code, that can be used to add this IAM policy to your state.

**NOTE:** This script requires boto3 and jinja2 to be installed. If you have pip, then you could set up all the dependencies using the following command:
```
pip install -r ./import_script/requirements.txt
```
Also, you should configure you AWS credentials for CLI usage. Instructions can be found [here](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html).

## Input variables

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|----------|
| create_document_only | Indicates whether this module should create IAM policy or IAM policy document only. | bool | false | no | 
| name | IAM policy name. Incompatible with name_prefix variable. | string | null | no |
| name_prefix | Creates a unique name beginning with the specified prefix. | string | null | no |
| path | Path in which to create the policy. | string | "/" | no |
| description | Description of the IAM policy. | string | "" | no |
| heredoc_string | Multiline (or single line with escaped double-quotes) content of the IAM policy document. | string | "" | no |
| configuration_version | IAM policy document version. | string | "2012-10-17" | no |
| source_json | An IAM policy document to import as a base for the current policy document | string | null | no |
| override_json | An IAM policy document to import and override the current policy document. | string | null | no |
| statements | Array of statements, that comprise IAM policy content. | null | [] | no |
| source_file | Path to file that contains the complete IAM policy document. | string | "" | no |
| template_file | Path to file that contains the template for IAM policy document. | string | "" | no |
| template_variables| Map of variables template_file needs to render IAM policy document. | map | {} | no |

## Outputs

| Name | Description |
|------|-------------|
| id   | Id of the newly-created IAM policy. Returns empty string if create_document_only is set to true. |
| arn  | ARN of the newly-created IAM policy. Returns empty string if create_document_only is set to true. |
| name | Name of the newly-created IAM policy. Returns empty string if create_document_only is set to true. |
| path | Path of the newly-created IAM policy. Returns empty string if create_document_only is set to true. |
| json | Contents of the IAM policy document. |

## Troubleshooting
* Despite this module having several different ways of configuring IAM policy document, it has a strict order in which these data sources are processed. Which is as follows:
```
aws_iam_policy_document -> heredoc_string -> rendered_template_file -> source_file_contents
```
* A quick note about template_variables. This module uses `templatefile` function, which means that standart limitations of terraform templating apply here. For example, terraform template engine requires for all the variables in a map have primitive types. References [here](https://www.terraform.io/docs/providers/template/d/file.html#vars) and [here](https://www.terraform.io/docs/configuration/functions/templatefile.html).

# License
Apache 2 Licensed. See [LICENSE](https://github.com/vladyslav-tripatkhi/terraform-iam-policy/tree/master/LICENSE) for full details.
