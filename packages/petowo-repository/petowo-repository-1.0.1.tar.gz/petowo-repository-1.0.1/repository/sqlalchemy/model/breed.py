from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from core.breed.schema.breed import BreedSchema
from core.utils.types import ID, BreedName
from repository.sqlalchemy.model.base import Base


class BreedORM(Base):
    __tablename__ = "breed"

    id: Mapped[int] = mapped_column(primary_key=True)
    species_id: Mapped[int] = mapped_column(ForeignKey(column="species.id"))
    name: Mapped[str] = mapped_column(String, nullable=False)

    def to_schema(self) -> BreedSchema:
        return BreedSchema(
            id=ID(self.id),
            species_id=ID(self.species_id),
            name=BreedName(self.name)
        )
