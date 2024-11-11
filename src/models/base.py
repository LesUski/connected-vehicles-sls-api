"""Base model for DynamoDB tables."""

import os
from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute


class BaseModel(Model):
    """Base model with common attributes and configuration."""

    class Meta:
        table_name = os.environ.get("TABLE_NAME")
        region = os.environ.get("AWS_REGION", "eu-central-1")
        billing_mode = "PAY_PER_REQUEST"

        # Support for local DynamoDB
        if os.environ.get("STAGE") == "local":
            host = os.environ.get("DYNAMODB_ENDPOINT", "http://localhost:8000")
            aws_access_key_id = "LOCAL"
            aws_secret_access_key = "LOCAL"

    PK = UnicodeAttribute(hash_key=True)
    SK = UnicodeAttribute(range_key=True)
