from abc import ABC
from uuid import UUID

from hundred import Aggregate


class InMemoryRepository[A: Aggregate](ABC):
    __slots__ = ("data",)

    def __init__(self) -> None:
        self.data = dict[UUID, A]()

    async def get(self, uuid: UUID, /) -> A | None:
        return self.data.get(uuid)

    async def save(self, aggregate: A, /) -> None:
        self.data[aggregate.id] = aggregate

    async def delete(self, uuid: UUID, /) -> None:
        self.data.pop(uuid, None)
