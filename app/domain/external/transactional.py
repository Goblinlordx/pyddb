from abc import ABC, abstractmethod

from domain.external.exception import (
    RollbackException,
    RollbackFailedException,
)
from domain.user.repository import UserRepository


class ReversableOperation(ABC):
    @abstractmethod
    def up(self): ...

    @abstractmethod
    def down(self): ...


class CommitableReversableContext(ABC):
    def __init__(self) -> None:
        self._committed_ops: list[ReversableOperation] = []
        self._commitable_ops: list[ReversableOperation] = []

    def commit(self):
        current: ReversableOperation | None = None
        try:
            while self._commitable_ops:
                current = self._commitable_ops[0]
                current.up()
                self._committed_ops.append(self._commitable_ops.pop(0))
        except Exception as err:
            self.rollback()
            raise RollbackException(f"commit rolled back\nop: {current}") from err

    def rollback(self):
        current: ReversableOperation | None = None
        try:
            while self._committed_ops:
                current = self._committed_ops[-1]
                current.down()
                self._commitable_ops.append(self._committed_ops.pop(-1))
        except Exception as err:
            raise RollbackFailedException("rollback failed") from err


class UnitOfWork(ABC):
    users: UserRepository

    @abstractmethod
    def commit(self): ...

    @abstractmethod
    def __enter__(self, *args, **kwargs): ...

    @abstractmethod
    def __exit__(self, *args, **kwargs): ...
