from domain.exception import NotFoundException
from domain.external.transactional import UnitOfWork
from domain.user.commands import (
    UserCreateCommand,
    UserCreateCommandResult,
    UserDeleteCommand,
    UserDeleteCommandResult,
)
from domain.user.model import User
from ulid import ulid


def handle_user_create(
    command: UserCreateCommand, unit_of_work: UnitOfWork
) -> UserCreateCommandResult:
    id = ulid()

    user = User(id=id, email=command.email)
    with unit_of_work:
        unit_of_work.users.create(user)
        unit_of_work.commit()

    return UserCreateCommandResult(id=id)


def handle_user_delete(
    command: UserDeleteCommand, unit_of_work: UnitOfWork
) -> UserDeleteCommandResult:
    with unit_of_work:
        user = unit_of_work.users.get_by_id(command.id)
        if not user:
            raise NotFoundException(f"user: {command.id}")
        unit_of_work.users.delete(user)
        unit_of_work.commit()

    return UserDeleteCommandResult()
