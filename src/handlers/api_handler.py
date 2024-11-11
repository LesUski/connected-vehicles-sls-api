import json
import os
from aws_lambda_powertools import Logger, Tracer, Metrics
from aws_lambda_powertools.utilities.typing import LambdaContext
from aws_lambda_powertools.utilities.data_classes import APIGatewayProxyEvent
import boto3

logger = Logger()
tracer = Tracer()
metrics = Metrics()

sfn = boto3.client("stepfunctions")
STATE_MACHINE_ARN = os.environ["STATE_MACHINE_ARN"]


@logger.inject_lambda_context
@tracer.capture_lambda_handler
@metrics.log_metrics
def handle(event: APIGatewayProxyEvent, context: LambdaContext):
    try:
        body = json.loads(event["body"])

        # Extract operation type and entity type from path parameters
        path_parameters = event.get("pathParameters", {})
        operation = path_parameters.get("operation", "create")
        entity_type = path_parameters.get("entity_type", "vehicle")

        # Prepare input for step function
        step_function_input = {
            "operation": operation,
            "entity_type": entity_type,
            "data": body,
        }

        # Start step function execution
        execution = sfn.start_execution(
            stateMachineArn=STATE_MACHINE_ARN, input=json.dumps(step_function_input)
        )

        return {
            "statusCode": 202,
            "body": json.dumps(
                {
                    "message": "Request accepted",
                    "executionArn": execution["executionArn"],
                }
            ),
        }
    except Exception as e:
        logger.exception("Error processing request")
        return {"statusCode": 500, "body": json.dumps({"error": str(e)})}
