from abc import ABC, abstractmethod
from typing import List, TypeVar, Union, Generic, Dict
from uuid import UUID


MODEL = TypeVar('MODEL')


class BaseRepository(ABC, Generic[MODEL]):

    @property
    @abstractmethod
    def model(self) -> MODEL:
        """
        Abstract property that should be overridden in subclasses to
        specify the data model or schema the repository will handle.
        """
        pass

    @abstractmethod
    async def get(self, id: Union[UUID, int, str], **kwargs):
        """
        To retrieve a single entity based on its identifier (ID).

        :param id:search by id obj.
        """
        pass

    @abstractmethod
    async def add(self, entity: MODEL):
        """
        To add a new entity to the database.

        :param entity: adding new entity to the DB
        """
        pass

    @abstractmethod
    async def update(self, id: Union[UUID, int, str], entity: MODEL, **kwargs):
        """
        To update an existing entity based on its ID.

        :param id: identifiers to search by and update
        :param entity: what to update
        :param kwargs: for diffirent type of storage
        (NoSQL could require sort key)
        """
        pass

    @abstractmethod
    async def delete(self, id: Union[UUID, int, str]):
        """
        To delete an entity based on its ID.

        :param id: identifiers to search by and delete
        """
        pass

    @abstractmethod
    async def query(self, filters: Union[List, None] = None):
        """
        To retrieve a list of entities, optionally based on some filters.

        :param filters: Optional filters for query customization.
        """
        pass

    @abstractmethod
    async def query_paginated(self,
                              page_number: int,
                              page_size: int,
                              filters: Union[List, None] = None):
        """
        Retrieves entities in a paginated format.

        :param page_number: The current page number.
        :param page_size: The number of items per page.
        :param filters: Optional filters for query customization.
        """
        pass

    @abstractmethod
    async def add_bulk(self, entities: List[MODEL]):
        """
        Adds multiple entities to the database in a single operation.

        :param entities: A list of entities to add.
        """
        pass

    @abstractmethod
    async def update_bulk(self, entities: List[MODEL]):
        """
        Updates multiple entities in the database in a single operation.

        :param entities: A list of entity updates.
        """
        pass

    @abstractmethod
    async def save(self) -> None:
        """
        Commits any pending changes to the database. This method might be used
        to commit a transaction or just to ensure that changes are persisted.
        """
        pass
