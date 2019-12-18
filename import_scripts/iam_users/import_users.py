#!/usr/bin/env python3
import boto3
import jinja2
import argparse
from re import match

def generate_import_statement(iam_user, import_path):
    safe_name = iam_user.name.replace("@", "-").replace(".", "-")

    result = [
        "terraform import '{}{}' {}".format(
            f"{import_path}." if import_path else "",
            ".".join([f"user_{safe_name}", "aws_iam_user", "this[0]"]),
            iam_user.name
        )
    ]

    count = 0
    for policy in iam_user.attached_policies.all():
        result.append("terraform import '{}{}' {}".format(
            f"{import_path}." if import_path else "",
            ".".join([f"user_{safe_name}", "aws_iam_user_policy_attachment", f"this[{count}]"]),
            f"{iam_user.name}/{policy.arn}"
        ))
        count = count + 1

    inline_policies = list(iam_user.policies.all())
    if inline_policies and len(inline_policies) > 0:
        result.append("terraform import '{}{}' {}".format(
            f"{import_path}." if import_path else "",
            ".".join([f"user_{safe_name}", "aws_iam_user_policy", "this[0]"]),
            f"{iam_user.name}:{inline_policies[0].name}"
        ))

    if inline_policies and len(inline_policies) > 1:
        count = 0
        for inline_policy in inline_policies[1:]:
            result.append("terraform import '{}{}' {}".format(
                f"{import_path}." if import_path else "",
                ".".join([f"user_{safe_name}_{inline_policy.name}", "aws_iam_user_policy", f"this[{count}]"]),
                f"{iam_user.name}:{inline_policy.name}"
            ))
        count += 1
    
    user_groups = list(iam_user.groups.all())
    if user_groups:
        result.append("terraform import '{}{}' {}".format(
            f"{import_path}." if import_path else "",
            ".".join([f"user_{safe_name}", "aws_iam_user_group_membership", "this[0]"]),
            "/".join([iam_user.name] + [group.name for group in user_groups])
        ))

    return "\n".join(result)

def generate_terraform_code(iam_user, module_source, template):
    try:
        login_profile = iam.LoginProfile(iam_user.name).load()
        force_destroy = True
    except:
        force_destroy = bool(list(iam_user.access_keys.all()))

    return template.render(
        iam_user = iam_user,
        safe_name = iam_user.name.replace("@", "-").replace(".", "-"),
        module_source = module_source,
        force_destroy = force_destroy,
        attached_policy_arns = [policy.arn for policy in iam_user.attached_policies.all()],
        inline_policy_list = iam_user.policies.all(),
        group_names = [group.name for group in iam_user.groups.all()]
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--user-name",
        help="name of the user you would like to import into terraform. Imports all IAM users by default.")
    parser.add_argument("-m", "--module-source",
        help="indicates where terraform should look for IAM policy module source code",
        default="./modules/aws_iam_user")
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
        print("Daym, son")
        exit(1)

    if not args.generate_code_only and not args.import_string_only:
        args.generate_code_only=True
        args.import_string_only=True
    
    session = boto3.Session(
        profile_name="default",
        region_name="us-east-1"
    )

    if args.user_name:
        print("Exporting only {}".format(args.user_name))
    user_list = [{"name": args.user_name}] if args.user_name else [
        {"name": user["UserName"], "path": user["Path"]} for user in session.client("iam").list_users()["Users"]
    ]

    iam = session.resource("iam")
    import_statements = []
    terraform_module_declarations = []

    template = jinja2.Environment(
        loader=jinja2.FileSystemLoader(searchpath="./")
    ).get_template("iam_user_template.j2")

    for user in user_list:
        if "path" in user and args.skip_path and match(args.skip_path, user["path"]):
            print("Skipping role {} from import process.".format(user["name"]))
            continue
        iam_user = iam.User(user["name"])
        if args.import_string_only:
            import_statements.append(
                generate_import_statement(iam_user , args.import_path)
            )
        if args.generate_code_only:
            terraform_module_declarations.append(
                generate_terraform_code(iam_user, args.module_source, template)
            )

    if args.import_string_only:
        print("<<<<<<<<<< Generating import statements for terraform - START >>>>>>>>>>\n\n")
        print("\n".join(import_statements))
        print("\n\n<<<<<<<<<< Generating import statements for terraform - FINISH >>>>>>>>>>\n\n")

    if args.generate_code_only:
        print("<<<<<<<<<< Generating terraform code for IAM policies - START >>>>>>>>>>\n\n")
        if args.code_output != "/dev/stdout":
            print("Saved imported IAM users into {}".format(args.code_output))
            import_file = open(args.code_output, "w+")
            import_file.write("\n".join(terraform_module_declarations))
            import_file.close()
        else:
            print("\n".join(terraform_module_declarations))
        print("\n\n<<<<<<<<<< Generating terraform code for IAM policies - FINISH >>>>>>>>>>\n\n")
        