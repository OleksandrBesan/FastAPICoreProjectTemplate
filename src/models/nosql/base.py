from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute, NumberAttribute
from pynamodb.exceptions import DoesNotExist
from abc import ABC, abstractmethod
from core.config import get_app_settings
from core.settings.app import AppSettings

settings: AppSettings = get_app_settings()


class AbstractPynamoDBModel(Model, ABC):
    """
    Abstract base class for PynamoDB models.
    """

    class Meta:
        table_name = 'abstract_table'
        region = settings.AWS_DEFAULT_REGION

    # Define common attributes here
    id = UnicodeAttribute(hash_key=True)
    created_at = UnicodeAttribute()
    updated_at = UnicodeAttribute()

#n = AbstractPynamoDBModel()
#n.query