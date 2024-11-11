"""Test cases for Lambda handlers."""

import pytest
from src.handlers.process_handler import handle
from src.models.vehicle import VehicleModel
from unittest.mock import patch
from aws_lambda_powertools.utilities.typing import LambdaContext


@pytest.fixture
def lambda_context():
    """Create a mock Lambda context."""

    class MockContext(LambdaContext):
        function_name = "test-function"
        memory_limit_in_mb = 128
        invoked_function_arn = "arn:aws:lambda:eu-west-1:809313241:function:test"
        aws_request_id = "52fdfc07-2182-154f-163f-5f0f9a621d72"

    return MockContext()


@pytest.fixture
def vehicle_event():
    """Create a sample vehicle event."""
    return {
        "operation": "create",
        "entity_type": "vehicle",
        "data": {
            "vehicle_id": "WDDJK7DA4FF954840",
            "torque": "308",
            "drivetrain": "4WD",
            "engine": "gasoline",
            "horsepower": "406",
        },
    }


def test_create_vehicle(lambda_context, vehicle_event):
    """Test creating a vehicle."""
    with patch.object(VehicleModel, "save") as mock_save:
        result = handle(vehicle_event, lambda_context)
        assert result["result"]["status"] == "success"
        mock_save.assert_called_once()


def test_invalid_operation(lambda_context, vehicle_event):
    """Test handling invalid operation."""
    vehicle_event["operation"] = "invalid_op"
    with pytest.raises(Exception) as exc_info:
        handle(vehicle_event, lambda_context)
    assert "Unsupported operation" in str(exc_info.value)
