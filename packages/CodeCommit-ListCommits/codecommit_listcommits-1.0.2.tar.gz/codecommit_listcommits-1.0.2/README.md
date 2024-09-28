![pypl](https://img.shields.io/pypi/v/CodeCommit-ListCommits)
![Welcome PR](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)
![MIT license](https://img.shields.io/github/license/hermgerm29/qdbg?color=blue)

# CodeCommit-ListCommits

日本語はこちら: [README_JP.md](https://github.com/clcl777/CodeCommit-ListCommits/blob/main/README_JP.md)

CodeCommit-ListCommits is a Python library designed to facilitate the retrieval of commit history from AWS CodeCommit repositories using the Dulwich library. Unlike boto3, which does not allow for the bulk retrieval of all commits from a repository, this library enables you to clone a repository and extract all commit information in bulk, making it easier to analyze commit histories efficiently.


## Features
- **Bulk Commit Retrieval:** Retrieve all commits from a repository in bulk, making it easier and more efficient to analyze the entire commit history at once.
- **Branch-Specific Retrieval:** Retrieve commits from either the default or a specified branch.
- **Secure Repository Cloning:** Clone AWS CodeCommit repositories securely using HTTPS credentials.
- **Automatic Cleanup:** Automatically remove the cloned repository after the process completes, ensuring no leftover files.

## Installation

```bash
pip install CodeCommitListCommits
```

## Simple Demo

```Python
from CodeCommitListCommits import CodeCommitListCommits

USERNAME = "xxxxxxx"
PASSWORD = "xxxxxxx"
region = "ap-northeast-1"
repository_name = "repository_name"

# Retrieve commits from the default branch
client = CodeCommitListCommits(USERNAME, PASSWORD, region)
commits_default = client.list_commits(repository_name)
print(commits_default)

# Retrieve commits from a specific branch (e.g., "branch1")
commits_branch1 = client.list_commits(repository_name, "branch1")
print(commits_branch1)
```

## Generate HTTPS Git Credentials for CodeCommit

1. Log in to the AWS Management Console.
1. Go to Security credentials, and select AWS CodeCommit credentials.
1. Click on Generate credentials under the HTTPS GIt credentials for AWS CodeCommit section to create a username and password.
1. Save the generated username and password. These will be used to authenticate when clone the repository.

## Requirements

- `dulwich` library
- AWS CodeCommit credentials

