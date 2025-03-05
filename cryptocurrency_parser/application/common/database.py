from abc import ABC, abstractmethod
from typing import AsyncContextManager, Generic, TypeVar

SessionType = TypeVar("SessionType")


class Database(ABC, Generic[SessionType]):
    @abstractmethod
    async def get_session(self) -> AsyncContextManager[SessionType]:
        pass

    @abstractmethod
    async def dispose(self) -> None:
        pass
