from aws_lambda_powertools import Logger, Tracer
from aws_lambda_powertools.utilities.typing import LambdaContext
from src.services.validation_service import ValidationService, ValidationError

logger = Logger()
tracer = Tracer()


@logger.inject_lambda_context
@tracer.capture_lambda_handler
def handle(event: dict, context: LambdaContext):
    try:
        operation = event["operation"]
        entity_type = event["entity_type"]
        data = event["data"]

        validation_service = ValidationService()

        if entity_type == "vehicle":
            if operation == "create":
                validation_service.validate_vehicle_data(data)
            elif operation == "create_feature":
                validation_service.validate_feature_data(
                    data["feature_type"], data["feature_data"]
                )
        elif entity_type == "user":
            if operation == "create":
                validation_service.validate_user_data(data)
            elif operation == "create_preference":
                validation_service.validate_feature_data(
                    data["feature_type"], data["feature_data"]
                )

        return event
    except ValidationError as e:
        logger.exception("Validation failed")
        raise Exception(f"ValidationError: {str(e)}")
    except Exception as e:
        logger.exception("Unexpected error during validation")
        raise Exception(f"ValidationError: {str(e)}")
