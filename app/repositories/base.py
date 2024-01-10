from typing import Any, Dict, Generic, List, Optional, TypeVar
from uuid import UUID

from sqlalchemy import Column
from sqlalchemy.orm import Query, Session
from sqlalchemy.orm.decl_api import DeclarativeMeta

T = TypeVar("T", bound=DeclarativeMeta)
ID = TypeVar("ID")

CREATE = TypeVar("CREATE")
UPDATE = TypeVar("UPDATE")
RETURN = TypeVar("RETURN")


class BaseRepository(Generic[T]):
    filterable_fields: Optional[List[Column]]

    def __init__(
        self,
        model_class: T,
        db: Session,
    ):
        self.model_class = model_class
        self.db = db

    @property
    def default_query(self) -> Query:
        return self.db.query(self.model_class)

    def get(self) -> Query:
        return self.default_query

    def get_all(self) -> list[T]:
        return self.default_query.all()

    def get_by_id(self, id: int) -> Optional[T]:
        return self.default_query.get(id)

    def add(self, model: T) -> T:
        self.db.add(model)
        self.db.commit()
        return model

    def update(self, id: int, values: dict[str, Any]) -> Optional[T]:
        self.default_query.filter_by(id=id).update(values)  # type: ignore
        self.db.commit()
        return self.get_by_id(id)

    def delete(self, id: int) -> None:
        self.default_query.filter_by(id=id).delete()
