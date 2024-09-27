import inspect
import logging
from contextlib import AbstractContextManager
from typing import Callable, List, cast, Optional

from psycopg2.errors import UniqueViolation
from pydantic import NonNegativeInt, BaseModel
from sqlalchemy import update, insert, select
from sqlalchemy.exc import IntegrityError, OperationalError
from sqlalchemy.orm import Session

from core.animal.repository.animal import IAnimalRepository
from core.animal.schema.animal import AnimalSchema
from core.utils import types
from core.utils.exceptions import DuplicatedRepoError, NotFoundRepoError, ValidationRepoError
from .model.animal import AnimalORM


class SqlAlchemyAnimalRepository(IAnimalRepository):
    session_factory: Callable[..., AbstractContextManager[Session]]

    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]):
        self.session_factory = session_factory

    def get_by_user_id(self, user_id: NonNegativeInt) -> List[AnimalSchema]:
        try:
            with self.session_factory() as session:
                query = select(AnimalORM).filter_by(user_id=user_id)
                res = session.execute(query).scalars().all()
                if len(res) == 0:
                    raise NotFoundRepoError(detail=f"not found by user_id: {user_id}")
                return [AnimalSchema.model_validate(row.to_schema(), from_attributes=True) for row in res]
        except OperationalError as e:
            logging.error('DB connection error')
            raise e

    def get_all(self, skip: int = 0, limit: Optional[int] = None) -> List[AnimalSchema]:
        try:
            with self.session_factory() as session:
                if limit is None:
                    query = select(AnimalORM).offset(skip)
                else:
                    query = select(AnimalORM).offset(skip).limit(limit)
                rows = session.execute(query).scalars().all()
                return [AnimalSchema.model_validate(row.to_schema(), from_attributes=True) for row in rows]
        except OperationalError as e:
            logging.error('DB connection error')
            raise e

    def get_by_id(self, id: NonNegativeInt) -> AnimalSchema:
        try:
            with self.session_factory() as session:
                query = select(AnimalORM).filter_by(id=id)
                row = session.execute(query).scalar()
                if row is None:
                    raise NotFoundRepoError(detail=f"not found id : {id}")
                return AnimalSchema.model_validate(row.to_schema(), from_attributes=True)
        except OperationalError as e:
            logging.error('DB connection error')
            raise e

    def create(self, other: AnimalSchema) -> AnimalSchema:
        try:
            with self.session_factory() as session:
                other_dict = self.get_dict(other, exclude=['id'])
                stmt = insert(AnimalORM).values(other_dict).returning(AnimalORM.id)
                try:
                    result = session.execute(stmt)
                    session.commit()
                except IntegrityError as e:
                    if isinstance(e.orig, UniqueViolation):
                        raise DuplicatedRepoError(detail=str(e.orig))
                    raise ValidationRepoError(detail=str(e.orig))
                row = result.fetchone()
                return self.get_by_id(row[0])
        except OperationalError as e:
            logging.error('DB connection error')
            raise e

    @staticmethod
    def get_dict(other: BaseModel, exclude: List[str] | None = None) -> dict:
        dct = dict()
        for field in other.model_fields.keys():
            field_value = getattr(other, field)
            if exclude is None or field not in exclude:
                if type(field_value).__name__ in tuple(x[0] for x in inspect.getmembers(types, inspect.isclass)):
                    # if getattr(field_value, '__module__', None) == types.__name__:
                    #     f = fields(field_value)[0]
                    val = getattr(field_value, 'value')
                    dct[field] = val
                else:
                    dct[field] = field_value
        return dct

    def update(self, other: AnimalSchema) -> AnimalSchema:
        try:
            with self.session_factory() as session:
                other_dict = self.get_dict(other, exclude=['id'])
                stmt = update(AnimalORM).where(cast("ColumnElement[bool]", other.id.eq_int(AnimalORM.id))).values(other_dict).returning(AnimalORM.id)
                try:
                    result = session.execute(stmt)
                    session.commit()
                except IntegrityError as e:
                    if isinstance(e.orig, UniqueViolation):
                        raise DuplicatedRepoError(detail=str(e.orig))
                    raise ValidationRepoError(detail=str(e.orig))
                row = result.fetchone()
                if row is None:
                    raise NotFoundRepoError(detail=f"not found id : {id}")
                return self.get_by_id(row[0])
        except OperationalError as e:
            logging.error('DB connection error')
            raise e

    def delete(self, id: NonNegativeInt) -> None:
        with self.session_factory() as session:
            query = select(AnimalORM).filter_by(id=id)
            row = session.execute(query).scalar()
            if row is None:
                raise NotFoundRepoError(detail=f"not found id : {id}")
            session.delete(row)
            session.commit()
