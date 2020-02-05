#!/usr/bin/env python3

# ToDo: rename variables: import_string_only -> generate_import_statements; generate_code_only -> generate_terraform_code
# ToDo: perhaps, create a class or struct for IAM generic object, that contains resource's name, safe_name, path and arn
# ToDo: add function result and variable type declarations to this module

import boto3
import jinja2
import argparse
from re import match
from enum import Enum, auto
from abc import ABC, abstractmethod

GITHUB_REPO_URL="github.com/vladyslav-tripatkhi/terraform-iam-modules"

class ResourceTypes(Enum):
    iam_policy = "aws_iam_policy"
    iam_user = "aws_iam_user"
    iam_group = "aws_iam_group"
    iam_role = "aws_iam_role"
    all = "all"

class AbstractIamResourceImporter(ABC):
    def __init__(self, boto3_session, resource_type, name=None, skip_path=None, module_source=None, import_path=None):
        self._iam_resource = boto3_session.resource("iam")
        self._resource_type = resource_type
        template_file = f"{resource_type}.j2"
        self._resource_prefix = resource_type.split("_").pop()

        self._template = jinja2.Environment(
            loader=jinja2.FileSystemLoader(searchpath="./templates/")
        ).get_template(template_file)

        self._module_source = module_source if module_source else f"{GITHUB_REPO_URL}/modules/{resource_type}"
        self._import_path = import_path if import_path else ""

        self._resource_list = self._import_resources(boto3_session, name, skip_path)
        super().__init__()

    @abstractmethod
    def _import_resources(self, boto3_session, name, skip_path):
        pass

    # ToDo: this method should be able to import base instance of resource.
    # For iam_policy it should only import iam_policy, for iam_group - the group itself etc.
    def generate_import_statement(self, state_destination, resource_name):
        return f"terraform import '{state_destination}' {resource_name}"

    def _generate_import_statement(self, resource):
        state_destination = "{}{}".format(
            f"{self._import_path}." if self._import_path else "",
            ".".join([f"{self._resource_prefix}_{resource['safe_name']}", self._resource_type, "this[0]"]),
        )
        return f"terraform import '{state_destination}' {resource['arn']}"

    @abstractmethod
    def generate_terraform_code(self, resource):
        pass

    def _render_template(self, **template_parameters):
        return self._template.render(template_parameters)

    # ToDo: move generate_import_statements and generate_terraform_code to private functions
    # Consider moving everything into class private attributes or passing kwargs to this function?
    # Rename this function.
    def test_function(self, import_string_only, generate_code_only, code_output):
        import_statements = []
        terraform_module_declarations = []

        for resource in self._resource_list:
            print(resource)
            if import_string_only:
                import_statements.append(
                    self._generate_import_statement(resource)
                )
            if generate_code_only:
                terraform_module_declarations.append(
                    self.generate_terraform_code(resource)
                )
            
        if args.import_string_only:
            print("<<<<<<<<<< Generating import statements for terraform - START >>>>>>>>>>\n\n")
            print("\n".join(import_statements))
            print("\n\n<<<<<<<<<< Generating import statements for terraform - FINISH >>>>>>>>>>\n\n")

        if args.generate_code_only:
            print("<<<<<<<<<< Generating terraform code for IAM policies - START >>>>>>>>>>\n\n")
            if args.code_output != "/dev/stdout":
                import_file = open(args.code_output, "w+")
                import_file.write("\n\n".join(terraform_module_declarations))
                import_file.close()
                print("Saved imported IAM policies into {}".format(args.code_output))
            else:
                print("\n\n".join(terraform_module_declarations))
            print("\n\n<<<<<<<<<< Generating terraform code for IAM policies - FINISH >>>>>>>>>>\n\n")

class IamPolicyImporter(AbstractIamResourceImporter):
    def __init__(self, boto3_session, name=None, skip_path=None, module_source=None, import_path=None):
        super().__init__(boto3_session, ResourceTypes.iam_policy.value, name, skip_path, module_source, import_path)

    def generate_terraform_code(self, resource):
        aws_iam_policy = self._iam_resource.Policy(resource["arn"])
        aws_iam_policy_document = self._iam_resource.PolicyVersion(
            aws_iam_policy.arn,
            aws_iam_policy.default_version.version_id
        ).document

        return super()._render_template(**{
            "iam_policy": aws_iam_policy,
            "safe_name": resource["safe_name"],
            "module_source": self._module_source,
            "policy_document": aws_iam_policy_document
        })

    def _import_resources(self, boto3_session, name, skip_path):
        resource_list = [{
            "name": policy["PolicyName"],
            "safe_name": policy["PolicyName"].replace("@", "-").replace(".", "-"),
            "arn": policy["Arn"],
            "path": policy["Path"]
        } for policy in boto3_session.client("iam").list_policies(Scope="Local")["Policies"]]

        if name is not None:
            return list(filter(
                lambda policy: policy["name"] == name, resource_list
            ))
        
        if skip_path is not None:
            return list(filter(
                lambda policy: not match(skip_path, policy["path"]), resource_list
            ))

        return resource_list

class IamGroupImporter(AbstractIamResourceImporter):
    def __init__(self, boto3_session, name=None, skip_path=None, module_source=None, import_path=None):
        super().__init__(boto3_session, ResourceTypes.iam_policy.value, name, skip_path, module_source, import_path)

    def _import_resources(self, boto3_session, name, skip_path):
        resource_list = [{
            "name": group["GroupName"],
            "safe_name": group["GroupName"].replace("@", "-").replace(".", "-"),
            "arn": group["Arn"],
            "path": group["Path"]} for group in boto3_session.client("iam").list_groups()["Groups"]
        ]

        if name is not None:
            resource_list = list(filter(
                lambda group: group["name"] == name, resource_list
            ))
        
        if skip_path is not None:
            resource_list = list(filter(
                lambda group: not match(skip_path, group["path"]), resource_list
            ))

        iam = boto3_session.resource("iam")
        for resource in resource_list:
            iam_group = iam.Group(resource["name"])
            resource["attached_policy_arns"] = [policy.arn for policy in iam_group.attached_policies.all()]
            resource["inline_policies"] = list(iam_group.policies.all())

        return resource_list

    
    def generate_import_statement(self, resource):
        result = [
            self._generate_import_statement(resource)
        ]

        return "\n".join(result)
    
    def generate_terraform_code(self, resource):
        return ""



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--resource-type",
    help="Specify resource type you would like to import.", type=ResourceTypes, choices=list(ResourceTypes), default=ResourceTypes.all)
    parser.add_argument("-n", "--resource-name",
        help="name of the resource you would like to import into terraform. Imports all IAM resources of the specified type by default.",
        default=None)
    parser.add_argument("-m", "--module-source",
        help="indicates where terraform should look for IAM policy module source code",
        default=None)
    parser.add_argument("-i", "--import-path",
        help="terraform state path to import IAM polcies to. Defaults to state's root which is empty",
        default="")
    parser.add_argument("-s", "--skip-path",
        help="terraform state path to import IAM polcies to. Defaults to state's root which is empty",
        default=None)
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

    if args.resource_type is ResourceTypes.all and args.resource_name is not None:
        print("You cannot specify the name of the resource while omitting it's type. The program will now exit")
        exit(1)

    if args.generate_code_only and args.import_string_only:
        print("You have provided both --import-string-only and --generate-code-only. The program will now exit")
        exit(1)

    if not args.generate_code_only and not args.import_string_only:
        args.generate_code_only=True
        args.import_string_only=True
    
    session = boto3.Session()

    # iam_policy_importer = IamPolicyImporter(session, args.resource_name, args.skip_path,
    #     None,
    #     args.import_path)

    # iam_policy_importer.test_function(
    #     args.import_string_only,
    #     args.generate_code_only,
    #     args.code_output)

    iam_group_importer = IamGroupImporter(session, args.resource_name, args.skip_path,
        None,
        args.import_path)