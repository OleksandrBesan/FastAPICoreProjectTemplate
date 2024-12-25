from repositories.base import BaseRepository
from models.nosql.base import AbstractPynamoDBModel
from uuid import UUID
from typing import List, Union
from pydantic import BaseModel
from schemas.errors.pynamodb import NotFoundIdentifier


class BaseDynamoDBRepository(BaseRepository):
    model: AbstractPynamoDBModel

    async def get(self, id: Union[UUID, int, str], **kwargs):
        sort_key = kwargs.get('sort_key', None)
        try:
            return self.model.get(id, sort_key)
        except NotFoundIdentifier:
            return None

    async def add(self, entity: BaseModel):
        instance = self.model()

        for key, value in entity.model_dump().items():
            setattr(instance, key, value)

        instance.save()
        return instance

    async def update(self,
                     id: Union[UUID, int, str],
                     entity: BaseModel,
                     **kwargs):
        sort_key = kwargs.get('sort_key', None)
        for key, value in entity.items():
            setattr(self, key, value)

        item = self.model.get(id, sort_key)

        for key, value in entity.model_dump().items():
            if hasattr(item, key):
                setattr(item, key, value)

        item.save()

    async def delete(self, id: Union[UUID, int, str]):
        instance = self.get(id)
        instance.delete()

    async def query(self, filters: Union[List, None] = None):

    async def query_paginated(self, page_number: int, page_size: int, filters: Union[List, None] = None):

    async def add_bulk(self, entities: List[AbstractPynamoDBModel]):

    async def update_bulk(self, entities: List[BaseModel]):

    async def save(self) -> None:
        self.model.save()
 
    :
    @classmethod
    def update_model_bulk(cls, items):
        """
        Update multiple model instances.
        """
        with cls.batch_write() as batch:
            for item in items:
                batch.save(item)

    @classmethod
    def delete_model_bulk(cls, ids):
        """
        Delete multiple model instances by IDs.
        """
        with cls.batch_write() as batch:
            for id in ids:
                item = cls.get_model(id)
                if item:
                    batch.delete(item)

    @classmethod
    def query_model(cls, **kwargs):
        """
        Query model instances.
        """
        return cls.query(**kwargs)

    @classmethod
    def query_model_paginated(cls, limit, **kwargs):
        """
        Query model instances with pagination.
        """
        return cls.query(**kwargs).limit(limit)

    @classmethod
    def add_model_bulk(cls, items):
        """
        Add multiple model instances.
        """
        with cls.batch_write() as batch:
            for item in items:
                batch.save(item)
