import boto3
import json
from botocore import exceptions as botoex


def create_iam_user(username):
    '''
    creates a single IAM user
    :param username:
    :return:
    '''
    iam = boto3.client('iam')
    try:
        iam.create_user(UserName=username)
        print(f"Created new IAM user: {username}")
        return True
    except botoex.ClientError as e:
        if e.response['Error']['Code'] == 'EntityAlreadyExists':
            print(f"The username {username} already exists in your AWS account.")
            return False
        else:
            print(f"Error creating user {username}: {e}")
            raise


def create_access_key(username):
    '''
    Creates Access/secrett key pairs for the new user
    :param username:
    :return:
    '''
    iam = boto3.client('iam')
    try:
        response = iam.create_access_key(UserName=username)
        return response['AccessKey']
    except botoex.ClientError as e:
        print(f"Error creating access key for {username}: {e}")
        raise


def store_secret(username, access_key):
    '''
    Stores the credntial key pairs in AWS secretsmanger
    :param username:
    :param access_key:
    :return:
    '''
    secretsmanager = boto3.client('secretsmanager')
    secret_name = f"{username}-credentials"
    secret_value = json.dumps({
        'accessKeyId': access_key['AccessKeyId'],
        'secretAccessKey': access_key['SecretAccessKey']
    })
    try:
        response = secretsmanager.create_secret(
            Name=secret_name,
            Description=f"Access credentials for IAM user {username}",
            SecretString=secret_value
        )
        print(f"Stored credentials for {username} in Secrets Manager under secret name: {secret_name}")
        return response['ARN']
    except botoex.ClientError as e:
        print(f"Error storing secret for {username}: {e}")
        raise


def attach_rotation_lambda(secret_arn, lambda_arn):
    '''
    helps to attach an exisiting AWS lambda function
    :param secret_arn:
    :param lambda_arn:
    :return:
    '''
    secretsmanager = boto3.client('secretsmanager')
    secretsmanager.rotate_secret(
        SecretId=secret_arn,
        RotationLambdaARN=lambda_arn,
        RotationRules={'AutomaticallyAfterDays': 90})
    return None


def create_iam_users(users):
    '''
    Creates new IAM users , credentials for them and rotates these credentials
    :param users:
    :return:
    '''
    results = {}
    access_key, secret_arn = '', ''
    for user in users:
        if create_iam_user(user):
            access_key = create_access_key(user)
            if access_key:
                secret_arn = store_secret(user, access_key)
                attach_rotation_lambda(secret_arn, 'arn:aws:lambda:us-east-1:xxxxx:function:CredentionalRotation')
        results[user] = {'access_key': access_key, 'secret_arn': secret_arn}
    return results


