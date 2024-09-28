from secrets.secrets_manager import get_secret
import boto3

def get_s3_client():
    secrets = get_secret(f"ripikutils/aws_params")
    s3_client = boto3.client('s3',
                             aws_access_key_id=secrets['aws_access_key_id'],
                             aws_secret_access_key=secrets['aws_secret_access_key'],
                             region_name=secrets['region_name'])
    return s3_client