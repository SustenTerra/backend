from typing import Generic, Optional, TypeVar

from pydantic import BaseModel
from sqlalchemy.orm.decl_api import DeclarativeMeta

from app.repositories.base import BaseRepository

ModelClass = TypeVar("ModelClass", bound=DeclarativeMeta)
ModelRepository = TypeVar("ModelRepository", bound=BaseRepository)
CreateSchema = TypeVar("CreateSchema", bound=BaseModel)
UpdateSchema = TypeVar("UpdateSchema", bound=BaseModel)


class BaseController(
    Generic[ModelClass, ModelRepository, CreateSchema, UpdateSchema]
):
    def __init__(self, model_class: ModelClass, repository: ModelRepository):
        self.model_class = model_class
        self.repository: ModelRepository = repository

    def get_all(self) -> list[ModelClass]:
        return self.repository.get_all()

    def get_by_id(self, id: int) -> Optional[ModelClass]:
        return self.repository.get_by_id(id)

    def create(self, schema: CreateSchema) -> ModelClass:
        return self.repository.add(
            self.model_class(**schema.model_dump(exclude_unset=True))
        )

    def update(self, id: int, schema: UpdateSchema, set_to_exclude: Optional[set[str]] = None) -> Optional[ModelClass]:
        return self.repository.update(
            id, schema.model_dump(
                exclude_none=True,
                exclude_unset=True,
                exclude=set_to_exclude,
                by_alias=True)
        )

    def delete(self, id: int) -> None:
        self.repository.delete(id)
