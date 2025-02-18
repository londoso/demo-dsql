from aws_lambda_powertools.event_handler import APIGatewayRestResolver
from aws_lambda_powertools.utilities.typing import LambdaContext
from aws_lambda_powertools.logging import correlation_paths
from aws_lambda_powertools import Logger
import boto3
import os
import psycopg2

app = APIGatewayRestResolver()
logger = Logger()

region = os.environ["REGION"]
cluster_endpoint = os.environ["DSQL_CLUSTER_ENDPOINT"]

def generate_token(cluster_endpoint, region):
    client = boto3.client("dsql", region_name=region)
    token = client.generate_db_connect_admin_auth_token(cluster_endpoint, region)
    return token

def get_connection(cluster_endpoint):
    conn = psycopg2.connect(dbname = "postgres",
                        user = "admin", 
                        host= cluster_endpoint,
                        password = generate_token(cluster_endpoint, region),
                        port = 5432,
                        sslmode= 'require',
                        connect_timeout=3)
    return conn

@app.get("/get-data")
def get_data():
    conn = get_connection(cluster_endpoint)
    cursor = conn.cursor()

    sql = "SELECT * FROM test_table limit 5;"

    cursor.execute(sql)

    result = cursor.fetchall()

    return {"body":result}

# Enrich logging with contextual information from Lambda
@logger.inject_lambda_context(correlation_id_path=correlation_paths.API_GATEWAY_REST)

def lambda_handler(event: dict, context: LambdaContext) -> dict:
    return app.resolve(event, context)
