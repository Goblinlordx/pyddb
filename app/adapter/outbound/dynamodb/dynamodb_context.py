from adapter.outbound.dynamodb.operations import DynamoDBOp
from adapter.outbound.dynamodb.transaction import DynamoDBTransactOps
from boto3 import client
from domain.external.transactional import (
    CommitableReversableContext,
)
from mypy_boto3_dynamodb import DynamoDBClient

dynamo_client = client("dynamodb")


class DynamoDBContext(CommitableReversableContext):
    def __init__(self, client: DynamoDBClient, table_name: str):
        self.client = client
        self.table_name = table_name
        self._transact_ops: list[DynamoDBOp] = []
        super().__init__()

    def add(self, op: DynamoDBOp):
        self._transact_ops.append(op)

    def commit(self):
        self._commitable_ops.append(
            DynamoDBTransactOps(client=dynamo_client, ops=self._transact_ops)
        )
        return super().commit()
