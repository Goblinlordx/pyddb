from adapter.outbound.dynamodb.dynamodb_context import DynamoDBContext
from adapter.outbound.dynamodb.operations import (
    DynamoDBUserCreateOp,
    DynamoDBUserDeleteOp,
)
from adapter.outbound.dynamodb.serialize import dynamo_to_python, python_to_dynamo
from domain.user.model import User
from domain.user.repository import UserRepository


class DynamoDBUserRepository(UserRepository):
    def __init__(self, context: DynamoDBContext):
        self._context = context

    def get_by_id(self, id: str):
        res = self._context.client.get_item(
            TableName=self._context.table_name,
            Key=python_to_dynamo(
                {
                    "PK": f"USER#{id}",
                    "SK": f"USER#{id}",
                }
            ),
        )
        item = res.get("Item")
        return User(**dynamo_to_python(item)) if item else None

    def create(self, user: User):
        self._context.add(DynamoDBUserCreateOp(user))

    def delete(self, user: User):
        self._context.add(DynamoDBUserDeleteOp(user))
