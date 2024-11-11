from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute
import os


class BaseModel(Model):
    class Meta:
        table_name = os.environ.get("TABLE_NAME")
        region = os.environ.get("AWS_REGION")
        billing_mode = "PAY_PER_REQUEST"

    PK = UnicodeAttribute(hash_key=True)
    SK = UnicodeAttribute(range_key=True)
