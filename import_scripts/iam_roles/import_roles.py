#!/usr/bin/env python3
import boto3
import jinja2
from json import dumps
import argparse
from re import match

PRINCIPAL_TYPES = ["AWS", "Service"]

class TerraformPrincipal:
    def __init__(self, aws_principal):
        self._name = "shit"
        self._statements = []
        for principal_type in PRINCIPAL_TYPES:
            if principal_type in aws_principal:
                identifiers = aws_principal[principal_type]

                self._statements.append(dict(
                    type = principal_type,
                    identifiers = identifiers if type(identifiers) is list else [identifiers]
                ))
    
    def format(self):
        return ",".join(["{{ type = {}, identifiers = {} }}".format(
            dumps(statement["type"]),
            dumps(statement["identifiers"])
        ) for statement in self._statements])

def generate_terraform_code(iam_role, module_source, template):
    try:
        instance_profile = list(iam_role.instance_profiles.all())[0]
    except:
        instance_profile = None

    principals = []
    for statement in iam_role.assume_role_policy_document.get("Statement", []):
        principals.append(TerraformPrincipal(statement.get("Principal")).format())


    return template.render(
        iam_role = iam_role,
        safe_name = iam_role.name.replace("@", "-").replace(".", "-"),
        module_source = module_source,
        attached_policy_arns = [policy.arn for policy in iam_role.attached_policies.all()],
        instance_profile = instance_profile,
        inline_policies = list(iam_role.policies.all()),
        session_duration_hours = int(iam_role.max_session_duration / 3600),
        assume_role_principals = "[{}]".format(",".join(principals))
    )

def generate_import_statement(iam_role, import_path):
    safe_name = iam_role.name.replace("@", "-").replace(".", "-")

    result = [
        "terraform import '{}{}' {}".format(
            f"{import_path}." if import_path else "",
            ".".join([f"role_{iam_role.name}", "aws_iam_role", "this[0]"]),
            iam_role.name
        )
    ]

    count = 0
    for policy in iam_role.attached_policies.all():
        result.append("terraform import '{}{}' {}".format(
            f"{import_path}." if import_path else "",
            ".".join([f"role_{iam_role.name}", "aws_iam_role_policy_attachment", f"this[{count}]"]),
            f"{iam_role.name}/{policy.arn}"
        ))
        count = count + 1


    inline_policies = list(iam_role.policies.all())
    if inline_policies and len(inline_policies) > 0:
        result.append("terraform import '{}{}' {}".format(
            f"{import_path}." if import_path else "",
            ".".join([f"role_{safe_name}", "aws_iam_role_policy", "this[0]"]),
            f"{iam_role.name}:{inline_policies[0].name}"
        ))

    if inline_policies and len(inline_policies) > 1:
        count = 0
        for inline_policy in inline_policies[1:]:
            result.append("terraform import '{}{}' {}".format(
                f"{import_path}." if import_path else "",
                ".".join([f"role_{safe_name}_{inline_policy.name}", "aws_iam_role_policy", f"this[{count}]"]),
                f"{iam_role.name}:{inline_policy.name}"
            ))
        count += 1

    try:
        instance_profile = list(iam_role.instance_profiles.all())[0]
        result.append("terraform import '{}{}' {}".format(
            f"{import_path}." if import_path else "",
            ".".join([f"role_{iam_role.name}", "aws_iam_instance_profile", "this[0]"]),
            f"{instance_profile.name}"
        ))
    except:
        instance_profile = None

    return "\n".join(result)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--role-name",
        help="name of the role you would like to import into terraform. Imports all IAM roles by default.")
    parser.add_argument("-m", "--module-source",
        help="indicates where terraform should look for IAM policy module source code",
        default="github.com/vladyslav-tripatkhi/terraform-iam-modules/modules/aws_iam_role")
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

    iam = session.resource("iam")
    import_statements = []
    terraform_module_declarations = []

    if args.role_name:
        print("Importing only {}".format(args.role_name))
    role_list = [{"name": args.role_name}] if args.role_name else [
        {"name": role["RoleName"], "path": role["Path"]} for role in session.client("iam").list_roles()["Roles"]
    ]

    template = jinja2.Environment(
        loader=jinja2.FileSystemLoader(searchpath="./")
    ).get_template("iam_role_template.j2")

    for role in role_list:
        if "path" in role and args.skip_path and match(args.skip_path, role["path"]):
            print("Skipping role {} from import process.".format(role["name"]))
            continue
        iam_role = iam.Role(role["name"])
        if args.import_string_only:
            import_statements.append(
                generate_import_statement(iam_role , args.import_path)
            )
        if args.generate_code_only:
            terraform_module_declarations.append(
                generate_terraform_code(iam_role, args.module_source, template)
            )

    if args.import_string_only:
        print("<<<<<<<<<< Generating import statements for terraform - START >>>>>>>>>>\n\n")
        print("\n".join(import_statements))
        print("\n\n<<<<<<<<<< Generating import statements for terraform - FINISH >>>>>>>>>>\n\n")

    if args.generate_code_only:
        print("<<<<<<<<<< Generating terraform code for IAM policies - START >>>>>>>>>>\n\n")
        if args.code_output != "/dev/stdout":
            print("Saved imported IAM roles into {}".format(args.code_output))
            import_file = open(args.code_output, "w+")
            import_file.write("\n".join(terraform_module_declarations))
            import_file.close()
        else:
            print("\n".join(terraform_module_declarations))
        print("\n\n<<<<<<<<<< Generating terraform code for IAM policies - FINISH >>>>>>>>>>\n\n")
