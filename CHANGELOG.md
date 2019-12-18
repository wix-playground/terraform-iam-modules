## Unreleased


### ToDo: 
* Check changes via tests in the future.
* Move this module to terraform-iam-modules repo, where iam-user, iam-group and iam-role repos will also be present
* After that is complete, rewrive import script to be able to work with all these resources
* Add proper README.md and examples.
* Unify import scripts so that only one/a couple of python files will remain. Add import commands to Makefile.

## v0.2.2 2019-12-18
* Removed aws_iam_user data source as it was being recreadted every terraform run, which led to constant resource re-creation.
* Changed outputs to reflect these changes.
* Fixed iam_user import template to properly utilize user's safe_name. 
* Removed an unnecessary requirements.txt from aws_iam_user import script.

## v0.2.1 2019-12-18
* Removed aws_iam_group data source as it was being recreadted every terraform run, which led to constant resource re-creation.
* Changed outputs to reflect these changes.
* Added scripts to makefile that create and destroy python virtualenv.
* Fixed iam_role imports:
    * Encased instance profile import statement in single quotes;
    * Fixed syntax of inline policy import statements;

## v0.2.0 2019-12-10
* Added iam_user, iam_group and iam_role modules to this repo. Renamed it to `terraform-iam-modules`.
* Added a dummy readme into each module folder and the repo itself.
* Examples and dummy tests folders as well Makefile, CHANGELOG.md and LICENSE have been put into project root.
* Added import scripts for every module.

## v0.1.8 2019-12-05
* Rewritten IAM policy import script in Python 3 instead of bash

## v0.1.7 2019-12-02
* Added helper script that simplifies importing your existing AWS resources into the terraform state.

## v0.1.6 2019-11-29
* Changed default values for name and name_prefix to `null` in order to get rid of a second conditional `iam_policy` resource and simplify code. If default is left to `""`, terraform would fail, saying that both name and name_prefix shouldn't be defined in a single resource.
* Changed IAM policy document value from `""` to `"{}"` in order to be able to re-use this resource in other modules. This was done to determine, whether other IAM resources (groups, roles, users) should have an inline policy attached to them or not.

## v0.1.5 2019-11-27
* Added LICENSE, .gitignore, versions.tf files
* Added examples for various use cases for that module
* Allow terraform to assign random name to IAM policy if both name and name_preifx are empty
* Changes to README.md to reflect a lot of things

## v0.1.0 2019-11-27
* Creaded README.md
* Created iam-group module
* Initial commit
