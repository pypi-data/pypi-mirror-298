from abc import ABC
from typing import ClassVar, Self
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class Entity(BaseModel, ABC):
    id: UUID = Field(frozen=True)

    model_config: ClassVar[ConfigDict] = ConfigDict(validate_assignment=True)


class Aggregate(Entity, ABC):
    version: int = Field(default=1, gt=0)

    def bump_version(self) -> Self:
        self.version += 1
        return self
