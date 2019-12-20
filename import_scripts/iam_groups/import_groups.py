#!/usr/bin/env python3
import boto3
import jinja2
import argparse
from re import match

module_source="./modules/aws_iam_group"
import_path="module.us-east-1.module"

def generate_terraform_code(iam_group, module_source, template):
    return template.render(
        safe_name = iam_group.name.replace("@", "-").replace(".", "-"),
        module_source = module_source,
        iam_group = iam_group,
        attached_policy_arns = [policy.arn for policy in iam_group.attached_policies.all()],
        inline_policies = list(iam_group.policies.all())
    )

def generate_import_statement(iam_group, import_path):
    safe_name = iam_group.name.replace("@", "-").replace(".", "-")

    result = [
        "terraform import '{}{}' {}".format(
            f"{import_path}." if import_path else "",
            ".".join([f"group_{safe_name}", "aws_iam_group", "this[0]"]),
            iam_group.name
        )
    ]

    count = 0
    for policy in iam_group.attached_policies.all():
        result.append("terraform import '{}{}' {}".format(
            f"{import_path}." if import_path else "",
            ".".join([f"group_{safe_name}", "aws_iam_group_policy_attachment", f"this[{count}]"]),
            f"{iam_group.name}/{policy.arn}"
        ))
        count += 1

    inline_policies = list(iam_group.policies.all())
    if inline_policies and len(inline_policies) > 0:
        result.append("terraform import '{}{}' {}".format(
            f"{import_path}." if import_path else "",
            ".".join([f"group_{safe_name}", "aws_iam_group_policy", "this[0]"]),
            f"{iam_group.name}:{inline_policies[0].name}"
        ))

    if inline_policies and len(inline_policies) > 1:
        count = 0
        for inline_policy in inline_policies[1:]:
            result.append("terraform import '{}{}' {}".format(
                f"{import_path}." if import_path else "",
                ".".join([f"group_{safe_name}_{inline_policy.name}", "aws_iam_group_policy", f"this[{count}]"]),
                f"{iam_group.name}:{inline_policy.name}"
            ))
        count += 1

    return "\n".join(result)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--group-name",
        help="name of the group you would like to import into terraform. Imports all IAM groups by default.")
    parser.add_argument("-m", "--module-source",
        help="indicates where terraform should look for IAM policy module source code",
        default="./modules/aws_iam_group")
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

    if args.group_name:
        print("Importing only {}".format(args.group_name))
    group_list = [{"name": args.group_name}] if args.group_name else [
        {"name": group["GroupName"], "path": group["Path"]} for group in session.client("iam").list_groups()["Groups"]
    ]

    template = jinja2.Environment(
        loader=jinja2.FileSystemLoader(searchpath="./")
    ).get_template("iam_group_template.j2")

    for group in group_list:
        if "path" in group and args.skip_path and match(args.skip_path, group["path"]):
            print("Skipping role {} from import process.".format(group["name"]))
            continue
        iam_group = iam.Group(group["name"])
        if args.import_string_only:
            import_statements.append(
                generate_import_statement(iam_group , args.import_path)
            )
        if args.generate_code_only:
            terraform_module_declarations.append(
                generate_terraform_code(iam_group, args.module_source, template)
            )

    if args.import_string_only:
        print("<<<<<<<<<< Generating import statements for terraform - START >>>>>>>>>>\n\n")
        print("\n".join(import_statements))
        print("\n\n<<<<<<<<<< Generating import statements for terraform - FINISH >>>>>>>>>>\n\n")

    if args.generate_code_only:
        print("<<<<<<<<<< Generating terraform code for IAM policies - START >>>>>>>>>>\n\n")
        if args.code_output != "/dev/stdout":
            print("Saved imported IAM groups into {}".format(args.code_output))
            import_file = open(args.code_output, "w+")
            import_file.write("\n".join(terraform_module_declarations))
            import_file.close()
        else:
            print("\n".join(terraform_module_declarations))
        print("\n\n<<<<<<<<<< Generating terraform code for IAM policies - FINISH >>>>>>>>>>\n\n")
