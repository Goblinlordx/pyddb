from abc import ABC

from domain.user.model import User


class UserRepository(ABC):
    def create(self, user: User): ...
    def delete(self, user: User): ...
