# GitLab Manager
## Overview https://pypi.org/project/gitlab-manager/
gitlab-manager is a Python script that provides a command-line interface for managing GitLab variables. It includes two subcommands: create_variable and create_variable_from_file. These subcommands allow users to create variables directly or from an environment file, simplifying the process of managing project variables on GitLab.


## Usage

### Subcommands
1. create_variable
This subcommand creates a GitLab variable with the specified parameters.

python gitlab_manager.py create_variable --api_url <GitLab API URL> --project_id <Project ID> --private_token <Private Token> --key <Variable Key> --value <Variable Value> --type <Variable Type> --masked --protected --environment_scope <Environment Scope>
* --api_url: GitLab API URL.
* --project_id: Project ID where the variable will be created.
* --private_token: Private Token for authentication.
* --key: Key for the variable.
* --value: Value for the variable.
* --type: Variable Type (default: 'env_var').
* --masked: Flag to indicate if the variable should be masked.
* --protected: Flag to indicate if the variable should be protected.
* --environment_scope: Environment Scope for the variable (default: '*').

## Example
```
gitlab_manager create_variable_from_file --api_url https://gitlab.example.com --project_id 123 --private_token ABC123 --key PathToFile --masked --protected
```

2. create_variable_from_file
This subcommand creates GitLab variables from an environment file.


python gitlab_manager.py create_variable_from_file --api_url <GitLab API URL> --project_id <Project ID> --private_token <Private Token> --file <Path to Env File> --type <Variable Type> --masked --protected --environment_scope <Environment Scope>
* --api_url: GitLab API URL.
* --project_id: Project ID where the variables will be created.
* --private_token: Private Token for authentication.
* --file: Path to the environment file containing variables.
* --type: Variable Type (default: 'env_var').
* --masked: Flag to indicate if the variables should be masked.
* --protected: Flag to indicate if the variables should be protected.
* --environment_scope: Environment Scope for the variables (default: '*').


## Example
```
gitlab_manager create_variable_from_file --api_url https://gitlab.example.com --project_id 123 --private_token ABC123 --key PathToFile --masked --protected
```

2. get_variables
This subcommand get GitLab variables from specific scope.


python gitlab_manager.py get_variables --api_url <GitLab API URL> --project_id <Project ID> --private_token <Private Token> --environment_scope <Environment Scope>
* --api_url: GitLab API URL.
* --project_id: Project ID where the variables will be created.
* --private_token: Private Token for authentication.
* --environment_scope: Environment Scope for the variables (default: '*').


## Example
```
gitlab_manager get_variables --api_url https://gitlab.example.com --project_id 123 --private_token ABC123 ---environment_scope prod
```
