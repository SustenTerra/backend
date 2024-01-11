from typing import Any, Generic, Optional, TypeVar

from sqlalchemy.orm import Query, Session
from sqlalchemy.orm.decl_api import DeclarativeMeta

ModelClass = TypeVar("ModelClass", bound=DeclarativeMeta)


class BaseRepository(Generic[ModelClass]):
    def __init__(
        self,
        model_class: ModelClass,
        session: Session,
    ):
        self.model_class = model_class
        self.session = session

    @property
    def default_query(self) -> Query:
        return self.session.query(self.model_class)

    def get(self) -> Query:
        return self.default_query

    def get_all(self) -> list[ModelClass]:
        return self.default_query.all()

    def get_by_id(self, id: int) -> Optional[ModelClass]:
        return self.default_query.filter_by(id=id).first()

    def add(self, model: ModelClass) -> ModelClass:
        self.session.add(model)
        self.session.commit()
        return model

    def update(self, id: int, values: dict[str, Any]) -> Optional[ModelClass]:
        self.default_query.filter_by(id=id).update(values)  # type: ignore
        self.session.commit()
        return self.get_by_id(id)

    def delete(self, id: int) -> None:
        self.default_query.filter_by(id=id).delete()
        self.session.commit()
