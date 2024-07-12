# AWS IAM User Management Tool

This Python script provides functionality to create IAM users in AWS, generate access keys, store credentials in AWS Secrets Manager, and set up automatic credential rotation using AWS Lambda.

## Features

- Create IAM users
- Generate access keys for IAM users
- Store user credentials securely in AWS Secrets Manager
- Attach a Lambda function for automatic credential rotation
- Batch creation of multiple IAM users

## Prerequisites

- Python 3.x
- boto3 library
- AWS CLI configured with appropriate permissions

## Installation

1. Clone this repository or download the script.
2. Install the required Python packages: pip install boto3
3. Ensure your AWS CLI is configured with the necessary permissions to create IAM users, access keys, and manage Secrets Manager.

## Usage

1. Import the necessary functions from the script:

```python
from iam_user_management import create_iam_users
users = ['user1', 'user2', 'user3']
results = create_iam_users(users)
print(results)
```
## Security Considerations

This script generates and stores IAM user credentials. Ensure you have appropriate security measures in place.
The Lambda function ARN for credential rotation is hardcoded. Make sure to replace it with your own Lambda function ARN.
Access keys are stored in Secrets Manager. Ensure you have proper access controls on your Secrets Manager.

## Error Handling
The script includes basic error handling for common AWS exceptions. Additional error handling may be required for production use.
