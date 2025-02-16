import arguably
from adapter.outbound.aws_unit_of_work import AWSUnitOfWork
from boto3 import client
from domain.user.commands import UserCreateCommand, UserDeleteCommand
from domain.user.handlers import (
    handle_user_create,
    handle_user_delete,
)

dynamo_client = client("dynamodb")

unit_of_work = AWSUnitOfWork(
    dynamo_client=dynamo_client,
    table_name="test-tx-st",
)


@arguably.command
def ping():
    print("pong")


@arguably.command
def user_create(email: str):
    res = handle_user_create(
        command=UserCreateCommand(
            email=email,
        ),
        unit_of_work=unit_of_work,
    )
    print(res)


@arguably.command
def user_delete(id: str):
    handle_user_delete(
        command=UserDeleteCommand(id=id),
        unit_of_work=unit_of_work,
    )
    print("user deleted successfuly")


if __name__ == "__main__":
    arguably.run()
