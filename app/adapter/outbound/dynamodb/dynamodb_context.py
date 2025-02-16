from adapter.outbound.dynamodb.operations import DynamoDBOp, DynamoDBTransactOps
from boto3 import client
from domain.external.transactional import (
    CommitableReversableContext,
)
from mypy_boto3_dynamodb import DynamoDBClient

ddb_client: DynamoDBClient = client("dynamodb")


class DynamoDBContext(CommitableReversableContext):
    def __init__(self):
        self._transact_ops: list[DynamoDBOp] = []
        super().__init__()

    def add(self, op: DynamoDBOp):
        self._transact_ops.append(op)

    def commit(self):
        self._commitable_ops.append(
            DynamoDBTransactOps(client=ddb_client, ops=self._transact_ops)
        )
        return super().commit()
