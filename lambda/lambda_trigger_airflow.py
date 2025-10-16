import json
import boto3
import requests

MWAA_ENV_NAME = "my-mwaa-env"
DAG_NAME = "data_pipeline"
REGION = "us-east-1"

def lambda_handler(event, context):
    client = boto3.client('mwaa', region_name=REGION)
    response = client.create_cli_token(Name=MWAA_ENV_NAME)
    mwaa_cli_token = response['CliToken']
    mwaa_web_server_hostname = response['WebServerHostname']

    # Airflow REST API call to trigger DAG
    url = f"https://{mwaa_web_server_hostname}/aws_mwaa/cli"
    payload = {
        "command": f"airflow dags trigger {DAG_NAME}"
    }
    headers = {
        "Authorization": f"Bearer {mwaa_cli_token}"
    }
    r = requests.post(url, json=payload, headers=headers)
    return {
        'statusCode': r.status_code,
        'body': r.text
    }