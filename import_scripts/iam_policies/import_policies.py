#!/usr/bin/env python3

import boto3
import jinja2
import argparse
from re import match

module_source="./modules/aws_iam_group"
import_path="module.us-east-1.module"

def generate_terraform_code(iam_group, module_source, template):
    return template.render(
        iam_policy = iam_policy,
        safe_name = iam_policy.policy_name.replace("@", "-").replace(".", "-"),
        module_source = args.module_source,
        policy_document = iam.PolicyVersion(policy["arn"], iam_policy.default_version.version_id).document
    )

def generate_import_statement(iam_policy, import_path):
    safe_name = iam_policy.policy_name.replace("@", "-").replace(".", "-")

    return "terraform import '{}{}' {}".format(
        f"{import_path}." if import_path else "",
        ".".join([f"policy_{safe_name}", "aws_iam_policy", "this[0]"]),
        iam_policy.arn
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--policy-name",
        help="name of the group you would like to import into terraform. Imports all IAM groups by default.")
    parser.add_argument("-m", "--module-source",
        help="indicates where terraform should look for IAM policy module source code",
        default="github.com/vladyslav-tripatkhi/terraform-iam-modules/modules/aws_iam_policy")
    parser.add_argument("-i", "--import-path",
        help="terraform state path to import IAM polcies to. Defaults to state's root which is empty",
        default="")
    parser.add_argument("-s", "--skip-path",
        help="terraform state path to import IAM polcies to. Defaults to state's root which is empty",
        default="")
    parser.add_argument("-o", "--code-output",
        help="specifies output destination for generated terraform code. Defaults to /dev/stdout",
        default="/dev/stdout")
    parser.add_argument("--import-string-only", action="store_true",
        help="if specified, this helper will only generate import statements for the select IAM policies." +
        " Setting this parameter together with --generate-code-only will result in an error.")
    parser.add_argument("--generate-code-only", action="store_true",
        help="if set, this helper will only generate terraform module code for the select IAM policies." +
        " Setting this parameter together with --import-string-only will result in an error.")

    args = parser.parse_args()

    if args.generate_code_only and args.import_string_only:
        print("You have provided both --import-string-only and --generate-code-only. The programm will now exit")
        exit(1)

    if not args.generate_code_only and not args.import_string_only:
        args.generate_code_only=True
        args.import_string_only=True
    
    session = boto3.Session()

    iam = session.resource("iam")
    import_statements = []
    terraform_module_declarations = []

    user_policies = [{
        "name": policy["PolicyName"],
        "arn": policy["Arn"],
        "path": policy["Path"]
    } for policy in session.client("iam").list_policies(Scope="Local")["Policies"]]

    policy_list = list(filter(
        lambda policy: policy["name"] == args.policy_name, user_policies
    )) if args.policy_name else user_policies

    template = jinja2.Environment(
        loader=jinja2.FileSystemLoader(searchpath="./")
    ).get_template("iam_policy_template.j2")

    for policy in policy_list:
        if "path" in policy and args.skip_path and match(args.skip_path, policy["path"]):
            print("Skipping role {} from import process.".format(policy["name"]))
            continue
        iam_policy = iam.Policy(policy["arn"])
        if args.import_string_only:
            import_statements.append(
                generate_import_statement(iam_policy , args.import_path)
            )
        if args.generate_code_only:
            terraform_module_declarations.append(
                generate_terraform_code(iam_policy, args.module_source, template)
            )
    
    if args.import_string_only:
        print("<<<<<<<<<< Generating import statements for terraform - START >>>>>>>>>>\n\n")
        print("\n".join(import_statements))
        print("\n\n<<<<<<<<<< Generating import statements for terraform - FINISH >>>>>>>>>>\n\n")

    if args.generate_code_only:
        print("<<<<<<<<<< Generating terraform code for IAM policies - START >>>>>>>>>>\n\n")
        if args.code_output != "/dev/stdout":
            print("Saved imported IAM policies into {}".format(args.code_output))
            import_file = open(args.code_output, "w+")
            import_file.write("\n\n".join(terraform_module_declarations))
            import_file.close()
        else:
            print("\n\n".join(terraform_module_declarations))
        print("\n\n<<<<<<<<<< Generating terraform code for IAM policies - FINISH >>>>>>>>>>\n\n")

