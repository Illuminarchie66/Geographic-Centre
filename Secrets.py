import boto3
import json

def get_secrets():
    secret_name = "GeographicKeys"
    region_name = "eu-west-2"

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(service_name='secretsmanager', region_name=region_name)

    try:
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
    except Exception as e:
        raise e

    # Parse secret string
    secret_string = get_secret_value_response['SecretString']
    secrets = json.loads(secret_string)
    return secrets