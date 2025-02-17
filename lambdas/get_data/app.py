from aws_lambda_powertools.event_handler import APIGatewayRestResolver
from aws_lambda_powertools.utilities.typing import LambdaContext
from aws_lambda_powertools.logging import correlation_paths
from aws_lambda_powertools import Logger
import boto3
import os

app = APIGatewayRestResolver()
logger = Logger()

region = os.environ["REGION"]
cluster_endpoint = os.environ["DSQL_CLUSTER_ENDPOINT"]

def generate_token(cluster_endpoint, region):
    client = boto3.client("dsql", region_name=region)
    token = client.generate_db_connect_admin_auth_token(cluster_endpoint, region)
    print(token)
    return token

@app.get("/get-data")
def get_data():

    logger.info("Hello world API - HTTP 200")
    return {"message": generate_token(cluster_endpoint, region)}

# Enrich logging with contextual information from Lambda
@logger.inject_lambda_context(correlation_id_path=correlation_paths.API_GATEWAY_REST)

def lambda_handler(event: dict, context: LambdaContext) -> dict:
    return app.resolve(event, context)
