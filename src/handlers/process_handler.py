"""
Process handler module for handling DynamoDB operations through Step Functions.

This module handles the processing of validated data for different entity types
and operations using the DynamoDB service.
"""

from typing import Dict, Any
from aws_lambda_powertools import Logger, Tracer
from aws_lambda_powertools.utilities.typing import LambdaContext

from src.services.dynamodb_service import DynamoDBService
from src.utils.exceptions import ProcessingError

logger = Logger()
tracer = Tracer()


@logger.inject_lambda_context
@tracer.capture_lambda_handler
def handle(event: Dict[str, Any], context: LambdaContext) -> Dict[str, Any]:
    """
    Handle the processing of validated data for DynamoDB operations.

    Args:
        event (Dict[str, Any]): Event data containing operation, entity type, and data
        context (LambdaContext): Lambda context object

    Returns:
        Dict[str, Any]: Processed result with original event data

    Raises:
        ProcessingError: When processing fails or invalid operation/entity type
    """
    try:
        operation = event["operation"]
        entity_type = event["entity_type"]
        data = event["data"]

        logger.debug(
            "Processing request",
            extra={"operation": operation, "entity_type": entity_type},
        )

        dynamodb_service = DynamoDBService()
        result = process_request(dynamodb_service, entity_type, operation, data)

        return {**event, "result": result}

    except KeyError as key_err:
        error_msg = f"Missing required field: {str(key_err)}"
        logger.error(error_msg)
        raise ProcessingError(error_msg)
    except Exception as exc:
        error_msg = f"Processing failed: {str(exc)}"
        logger.exception(error_msg)
        raise ProcessingError(error_msg) from exc


def process_request(
    dynamodb_service: DynamoDBService,
    entity_type: str,
    operation: str,
    data: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Process the request based on entity type and operation.

    Args:
        dynamodb_service (DynamoDBService): Instance of DynamoDB service
        entity_type (str): Type of entity (vehicle, user, etc.)
        operation (str): Operation to perform (create, create_feature, etc.)
        data (Dict[str, Any]): Data to process

    Returns:
        Dict[str, Any]: Result of the processing operation

    Raises:
        ProcessingError: When invalid entity type or operation is provided
    """
    if entity_type == "vehicle":
        return process_vehicle_request(dynamodb_service, operation, data)
    elif entity_type == "user":
        return process_user_request(dynamodb_service, operation, data)
    else:
        error_msg = f"Unsupported entity type: {entity_type}"
        logger.error(error_msg)
        raise ProcessingError(error_msg)


def process_vehicle_request(
    dynamodb_service: DynamoDBService, operation: str, data: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Process vehicle-related requests.

    Args:
        dynamodb_service (DynamoDBService): Instance of DynamoDB service
        operation (str): Operation to perform
        data (Dict[str, Any]): Vehicle data to process

    Returns:
        Dict[str, Any]: Result of the vehicle operation

    Raises:
        ProcessingError: When invalid operation is provided
    """
    if operation == "create":
        return dynamodb_service.create_vehicle(data)
    elif operation == "create_feature":
        return dynamodb_service.create_vehicle_feature(
            vehicle_id=data["vehicle_id"],
            feature_type=data["feature_type"],
            feature_data=data["feature_data"],
        )
    else:
        error_msg = f"Unsupported operation for vehicle: {operation}"
        logger.error(error_msg)
        raise ProcessingError(error_msg)


def process_user_request(
    dynamodb_service: DynamoDBService, operation: str, data: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Process user-related requests.

    Args:
        dynamodb_service (DynamoDBService): Instance of DynamoDB service
        operation (str): Operation to perform
        data (Dict[str, Any]): User data to process

    Returns:
        Dict[str, Any]: Result of the user operation

    Raises:
        ProcessingError: When invalid operation is provided
    """
    # Add user operations here when needed
    error_msg = f"Unsupported operation for user: {operation}"
    logger.error(error_msg)
    raise ProcessingError(error_msg)
