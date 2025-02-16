from adapter.outbound.dynamodb.dynamodb_context import DynamoDBContext
from adapter.outbound.dynamodb.operations import (
    DynamoDBUserCreateOp,
    DynamoDBUserDeleteOp,
)
from domain.user.model import User
from domain.user.repository import UserRepository


class DynamoDBUserRepository(UserRepository):
    def __init__(self, ddb_context: DynamoDBContext):
        self.ddb_context = ddb_context

    def create(self, user: User):
        self.ddb_context.add(DynamoDBUserCreateOp(user))

    def delete(self, user: User):
        self.ddb_context.add(DynamoDBUserDeleteOp(user))
