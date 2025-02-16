from aws_lambda_powertools.event_handler import APIGatewayRestResolver
from aws_lambda_powertools.utilities.typing import LambdaContext
from aws_lambda_powertools.logging import correlation_paths
from aws_lambda_powertools import Logger

app = APIGatewayRestResolver()
logger = Logger()

@app.get("/get-data")
def get_data():

    logger.info("Hello world API - HTTP 200")
    return {"message": "hello world"}

# Enrich logging with contextual information from Lambda
@logger.inject_lambda_context(correlation_id_path=correlation_paths.API_GATEWAY_REST)

def lambda_handler(event: dict, context: LambdaContext) -> dict:
    return app.resolve(event, context)
